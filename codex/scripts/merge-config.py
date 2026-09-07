#!/usr/bin/env python3
"""Merge only managed Codex settings; preserve unrelated local TOML content."""

from pathlib import Path
import re
import sys


check_only = sys.argv[1] == "--check"
arguments = sys.argv[2:] if check_only else sys.argv[1:]
source_path, target_path = map(Path, arguments)
source = source_path.read_text().splitlines()
target = target_path.read_text().splitlines() if target_path.exists() else []


def section_bounds(lines, name):
    header = f"[{name}]"
    start = next((i for i, line in enumerate(lines) if line.strip() == header), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("[")), len(lines))
    return start, end


def assignments(lines, bounds=None):
    start, end = bounds or (0, len(lines))
    found = {}
    for i in range(start, end):
        match = re.match(r"^([A-Za-z0-9_-]+)\s*=\s*(.*)$", lines[i])
        if match:
            found[match.group(1)] = i
    return found


def source_root_values():
    end = next((i for i, line in enumerate(source) if line.startswith("[")), len(source))
    return {key: source[index] for key, index in assignments(source, (0, end)).items()}


def source_section(name):
    bounds = section_bounds(source, name)
    if bounds is None:
        return []
    start, end = bounds
    return source[start:end]


def merge_section(lines, name, wanted_lines):
    bounds = section_bounds(lines, name)
    if bounds is None:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend(wanted_lines)
        return lines
    start, end = bounds
    existing = assignments(lines, bounds)
    wanted = {
        key: wanted_lines[index]
        for key, index in assignments(wanted_lines, (1, len(wanted_lines))).items()
    }
    insert_at = end
    for key, line in wanted.items():
        if key in existing:
            lines[existing[key]] = line
        else:
            lines.insert(insert_at, line)
            insert_at += 1
    return lines


# Root settings are intentionally limited to the portable policy keys in the source.
root_values = source_root_values()
root_bounds = (0, next((i for i, line in enumerate(target) if line.startswith("[")), len(target)))
root_existing = assignments(target, root_bounds)
for key, line in root_values.items():
    if key in root_existing:
        target[root_existing[key]] = line
    else:
        target.insert(root_bounds[1], line)
        root_bounds = (root_bounds[0], root_bounds[1] + 1)

# Merge the portable feature flags and agent defaults/registrations.
target = merge_section(target, "features", source_section("features"))
target = merge_section(target, "agents", source_section("agents"))
for role in ("portable_reviewer", "portable_researcher", "portable_implementer"):
    target = merge_section(target, f"agents.{role}", source_section(f"agents.{role}"))

# Preserve compatibility with existing Codex installations using legacy root keys.
agent_bounds = section_bounds(source, "agents")
if agent_bounds:
    agent_values = assignments(source, agent_bounds)
    legacy = {
        "default_subagent_model": agent_values.get("default_subagent_model"),
        "default_subagent_reasoning_effort": agent_values.get("default_subagent_reasoning_effort"),
    }
    target_root_bounds = (0, next((i for i, line in enumerate(target) if line.startswith("[")), len(target)))
    target_root_existing = assignments(target, target_root_bounds)
    for key, source_line in legacy.items():
        if source_line is None or key not in target_root_existing:
            continue
        target[target_root_existing[key]] = source[source_line]

result = "\n".join(target).rstrip() + "\n"
if check_only:
    existing = target_path.read_text() if target_path.exists() else ""
    raise SystemExit(0 if result == existing else 1)
target_path.write_text(result)
