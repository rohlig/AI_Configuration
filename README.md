# Portable AI Configuration

Portable, reviewable defaults for AI-assisted software development across machines.

This repository is designed to be public. It stores reusable Codex instructions, safe user-level defaults, custom agent roles, and an Obsidian-compatible handbook. It deliberately does not store credentials, chat history, plugin caches, databases, or machine-specific runtime state.

## Why this exists

AI development tools accumulate valuable configuration in a user directory. That configuration is easy to lose when changing computers and difficult to review when it lives only in an application profile. This repository makes the durable parts explicit:

- instructions that shape how AI agents collaborate and make changes;
- safe Codex defaults for approvals, sandboxing, web search, and context size;
- repeatable custom agent definitions for review, research, and implementation;
- documented practices for validation, delegation, compaction, and public sharing.

The repository is a source of truth, not a blind mirror of the entire Codex home directory.

## Quick start

```sh
git clone <repository-url> ~/Documents/Code/AI_Configuration
cd ~/Documents/Code/AI_Configuration

# Inspect the machine without changing it.
./scripts/sync-config.sh --check

# Check that the repository contains no obvious personal or secret material.
./scripts/audit-public.sh

# Review and approve each proposed machine-level change.
./scripts/sync-config.sh --install
```

The installer is interactive and creates timestamped backups before replacing existing files. Use `--yes` only after reviewing the planned changes.

## What is managed

| Repository source | Codex target | Purpose |
|---|---|---|
| `config/global/AGENTS.md` | `$CODEX_HOME/AGENTS.md` | Global working, delegation, and context-budget instructions |
| `config/global/config.toml` | `$CODEX_HOME/config.toml` | Portable user-level Codex defaults and agent registrations |
| `config/global/agents/*.toml` | `$CODEX_HOME/agents/ai-configuration/*.toml` | Namespaced custom reviewer, researcher, and implementer roles |

Codex uses more-specific project files in each project. Project-specific `.codex/config.toml` and `AGENTS.md` files should remain with those projects rather than being copied into this global repository.

## Agent and context policy

The default is one primary agent with small, bounded specialists only when work is genuinely independent. Agents receive only the files and facts they need, return concise structured results, and are integrated by the primary agent.

The configuration also enables early context compaction at `240000` input tokens and limits retained tool output to `12000` tokens. This is a cost-control buffer around the documented long-context pricing boundary; it is not a guarantee because system instructions and tool overhead also count.

Read [`obsidian/Agents and Subagents.md`](obsidian/Agents%20and%20Subagents.md) and [`obsidian/Token Budget and Context Management.md`](obsidian/Token%20Budget%20and%20Context%20Management.md) for the rationale and operating rules.

## What is intentionally excluded

Do not copy these into Git:

- API keys, tokens, cookies, authentication files, or private transcripts;
- absolute user paths and machine-specific project trust entries;
- MCP commands containing local installation paths or secrets;
- plugin caches, databases, session indexes, logs, generated files, and desktop state;
- settings that only make sense for one project or one operating system.

When a local setting is useful but not portable, document the category and the setup boundary in the Obsidian notes instead of copying the raw value.

## Documentation

- [`obsidian/Home.md`](obsidian/Home.md) — vault entry point.
- [`obsidian/Architecture.md`](obsidian/Architecture.md) — scope, data flow, dependencies, and constraints.
- [`obsidian/Current Configuration.md`](obsidian/Current%20Configuration.md) — human-readable current-state inventory.
- [`obsidian/Installation Workflow.md`](obsidian/Installation%20Workflow.md) — install, backup, rollback, and new-machine setup.
- [`obsidian/Best Practices/AI-Assisted Coding.md`](obsidian/Best%20Practices/AI-Assisted%20Coding.md) — coding workflow and review principles.
- [`obsidian/Operations/Unresolved Issues.md`](obsidian/Operations/Unresolved%20Issues.md) — open portability and research questions.

## Updating safely

1. Edit the versioned source under `config/global/`.
2. Run `./scripts/audit-public.sh`.
3. Parse and validate the TOML and shell files.
4. Run `./scripts/sync-config.sh --check`.
5. Review the diff and update the Obsidian checkpoint.
6. Run `./scripts/sync-config.sh --install` and approve the exact targets.

Official Codex behavior changes over time. The dated research note links to the primary documentation used for the current layout.
