#!/usr/bin/env python3
"""Add the repository's portable instruction sections without replacing local rules."""

from pathlib import Path
import re
import sys


check_only = sys.argv[1] == "--check"
arguments = sys.argv[2:] if check_only else sys.argv[1:]
source_path, target_path = map(Path, arguments)
source = source_path.read_text()
target = target_path.read_text() if target_path.exists() else ""
original_target = target

runtime_start = "<!-- AI_CONFIGURATION:BEGIN runtime-routing-contract -->"
runtime_end = "<!-- AI_CONFIGURATION:END runtime-routing-contract -->"
marker_start = "<!-- AI_CONFIGURATION:BEGIN context-cost-policy -->"
marker_end = "<!-- AI_CONFIGURATION:END context-cost-policy -->"
heading = "## Context and cost discipline"


def managed_block(text, start_marker, end_marker):
    if start_marker not in text or end_marker not in text:
        return None
    return text[text.index(start_marker):text.index(end_marker) + len(end_marker)]


def merge_managed_block(text, managed, start_marker, end_marker):
    """Replace all copies of a managed block with one canonical copy."""
    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        re.DOTALL,
    )
    matches = list(pattern.finditer(text))
    if not matches:
        return text.rstrip() + ("\n\n" if text.strip() else "") + managed + "\n"

    insertion_at = matches[0].start()
    without_blocks = pattern.sub("", text)
    before = without_blocks[:insertion_at].rstrip()
    after = without_blocks[insertion_at:].lstrip()
    return before + "\n\n" + managed + ("\n\n" + after if after else "\n")


runtime_managed = managed_block(source, runtime_start, runtime_end)
if runtime_managed is not None:
    target = merge_managed_block(target, runtime_managed, runtime_start, runtime_end)

if marker_start in source and marker_end in source:
    managed = source[source.index(marker_start):source.index(marker_end) + len(marker_end)]
else:
    section_start = source.index(heading)
    managed = "\n".join(
        [marker_start, source[section_start:].rstrip(), marker_end]
    )

result = merge_managed_block(target, managed, marker_start, marker_end)

if check_only:
    raise SystemExit(0 if result == original_target else 1)
target_path.write_text(result)
