# AI Configuration Repository Instructions

## Purpose

This repository is the portable source of truth for reusable AI-assisted development configuration and its documentation. Keep it safe to clone onto a new machine and understandable to a human without relying on hidden local state.

## Working agreements

- Inspect the current repository state before changing files.
- Treat `codex/config/` as Codex source files and the user’s Codex home as a deployment target. Keep general AI practices under `obsidian/General/`.
- Before running a command that writes to `~/.codex` or another machine-level location, explain the files and paths involved and ask for confirmation. The sync script already implements this safeguard.
- Prefer a dry run or `--check` before installation. Preserve backups when replacing an existing file.
- Never store credentials, personal data, machine-specific absolute paths, or plugin secrets in Git.
- Keep project-specific instructions in the project that needs them; keep this repository’s global instructions broadly reusable.
- When changing configuration, update the relevant Obsidian notes and the working checkpoint.
- When researching current behavior, cite the primary source and record the date checked.

## Validation

Run:

```sh
./codex/scripts/sync-config.sh --check
./codex/scripts/sync-config.sh --help
./scripts/audit-public.sh
```

For Codex shell changes, also run `bash -n codex/scripts/sync-config.sh` and exercise the check mode against a temporary `CODEX_HOME`.

## Documentation contract

The Obsidian base in `obsidian/` must distinguish general AI practices from Codex-specific configuration, architecture, data/control flow, dependencies, operational paths, constraints, tests, decisions, and unresolved issues. Update `obsidian/Codex/Operations/Checkpoint.md` before handoff.
