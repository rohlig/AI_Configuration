# Installation Workflow

## New machine

1. Clone this repository.
2. Inspect the source and run `./scripts/sync-config.sh --list`.
3. Run `./scripts/sync-config.sh --check`.
4. Run `./scripts/sync-config.sh --install` and approve each proposed write.
5. Restart or relaunch the Codex client if it does not pick up changed instructions immediately.
6. Record the result in [[Operations/Checkpoint]].

## Existing machine

The script never assumes that the repository should win. It reports missing, current, or different targets. `AGENTS.md` receives only the managed context-policy block; `config.toml` receives only managed root keys, feature flags, agent defaults, and namespaced registrations. Existing MCP, plugin, project-trust, desktop, and other settings remain in place. Existing managed files are backed up before an update.

## Rollback

Before replacing an existing file, the installer writes a copy under:

```text
$CODEX_HOME/backups/ai-configuration/YYYYMMDD-HHMMSS/
```

Restore a backup only after checking its contents and confirming the exact target. The script does not delete backups.

## Commands

```sh
./scripts/sync-config.sh --check
./scripts/sync-config.sh --install
./scripts/sync-config.sh --install --yes
CODEX_HOME=/path/to/test-home ./scripts/sync-config.sh --check
```

Use `--yes` only in a reviewed, intentional deployment step. A test home is useful for validating the workflow without touching the real machine.
