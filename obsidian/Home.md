# AI Configuration Knowledge Base

This vault documents general AI-assisted software practices separately from the Codex-specific configuration repository.

## General practices

- [[General/AI-Assisted Coding]] — tool-independent coding workflow, review, and safety principles.

## Codex-specific

- [[Codex/Architecture]] — what is versioned, what stays on a machine, and how precedence works.
- [[Codex/Current Configuration]] — current repository state and known machine-level targets.
- [[Codex/Installation Workflow]] — how to inspect, approve, install, and roll back configuration.
- [[Codex/Agents and Subagents]] — global defaults, custom roles, and safe delegation patterns.
- [[Codex/Token Budget and Context Management]] — compaction, splitting, and the long-context cost boundary.
- [[Codex/Research/2026-09-07-Codex-Configuration]] — dated official-source research.
- [[Codex/Operations/Checkpoint]] — continuity record for the current task.
- [[Codex/Operations/Unresolved Issues]] — open items that must not disappear between sessions.

## Maintenance rule

Every substantive configuration change updates the current-state note, the checkpoint, and (when applicable) the research note with a date and source.
