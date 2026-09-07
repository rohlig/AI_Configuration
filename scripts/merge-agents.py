#!/usr/bin/env python3
"""Add the repository's portable instruction sections without replacing local rules."""

from pathlib import Path
import sys


check_only = sys.argv[1] == "--check"
arguments = sys.argv[2:] if check_only else sys.argv[1:]
source_path, target_path = map(Path, arguments)
source = source_path.read_text()
target = target_path.read_text() if target_path.exists() else ""

marker_start = "<!-- AI_CONFIGURATION:BEGIN context-cost-policy -->"
marker_end = "<!-- AI_CONFIGURATION:END context-cost-policy -->"
heading = "## Context and cost discipline"

if marker_start in source and marker_end in source:
    managed = source[source.index(marker_start):source.index(marker_end) + len(marker_end)]
else:
    section_start = source.index(heading)
    managed = "\n".join(
        [marker_start, source[section_start:].rstrip(), marker_end]
    )

if marker_start in target and marker_end in target:
    before = target[:target.index(marker_start)].rstrip()
    after = target[target.index(marker_end) + len(marker_end):].lstrip()
    result = before + "\n\n" + managed + ("\n\n" + after if after else "\n")
elif marker_start not in target and heading not in target:
    result = target.rstrip() + ("\n\n" if target.strip() else "") + managed + "\n"
else:
    result = target

if check_only:
    raise SystemExit(0 if result == target else 1)
target_path.write_text(result)
