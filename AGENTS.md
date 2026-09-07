# AI Configuration Repository Instructions

## Purpose

This repository is the portable source of truth for reusable AI-assisted development configuration and its documentation. Keep it safe to clone onto a new machine and understandable to a human without relying on hidden local state.

## Working agreements

- Inspect the current repository state before changing files.
- Treat `config/global/` as source files and the user’s Codex home as a deployment target.
- Before running a command that writes to `~/.codex` or another machine-level location, explain the files and paths involved and ask for confirmation. The sync script already implements this safeguard.
- Prefer a dry run or `--check` before installation. Preserve backups when replacing an existing file.
- Never store credentials, personal data, machine-specific absolute paths, or plugin secrets in Git.
- Keep project-specific instructions in the project that needs them; keep this repository’s global instructions broadly reusable.
- When changing configuration, update the relevant Obsidian notes and the working checkpoint.
- When researching current behavior, cite the primary source and record the date checked.

## Validation

Run:

```sh
./scripts/sync-config.sh --check
./scripts/sync-config.sh --help
./scripts/audit-public.sh
```

For shell changes, also run `bash -n scripts/sync-config.sh` and exercise the check mode against a temporary `CODEX_HOME`.

## Documentation contract

The Obsidian base in `obsidian/` must cover scope, architecture, data/control flow, dependencies, operational paths, constraints, tests, decisions, and unresolved issues. Update `obsidian/Operations/Checkpoint.md` before handoff.
