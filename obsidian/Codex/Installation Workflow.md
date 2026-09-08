# Installation Workflow

## New machine

1. Clone this repository.
2. Inspect the Codex source and run `./codex/scripts/sync-config.sh --list`.
3. Run `./codex/scripts/sync-config.sh --check`.
4. Run `./codex/scripts/sync-config.sh --install` and approve each proposed write.
5. Restart or relaunch the Codex client if it does not pick up changed instructions immediately.
6. Record the result in [[Operations/Checkpoint]].

## Existing machine

The script never assumes that the repository should win. It reports missing, current, or different targets. `AGENTS.md` receives only the managed runtime-routing and context-policy blocks; other local instruction text remains in place. `config.toml` receives only managed portable root keys, feature flags, agent defaults, and namespaced registrations. Existing MCP, plugin, project-trust, desktop, and other settings remain in place. Existing managed files are backed up before an update.

The AGENTS merge also removes duplicate copies of its managed blocks and compares the computed merged result with the original target. This prevents a stale target from being incorrectly reported as current when local or another job has changed the managed instructions.

## Rollback

Before replacing an existing file, the installer writes a copy under:

```text
$CODEX_HOME/backups/ai-configuration/YYYYMMDD-HHMMSS/
```

Restore a backup only after checking its contents and confirming the exact target. The script does not delete backups.

## Commands

```sh
./codex/scripts/sync-config.sh --check
./codex/scripts/sync-config.sh --install
./codex/scripts/sync-config.sh --install --yes
CODEX_HOME=/path/to/test-home ./codex/scripts/sync-config.sh --check
```

Use `--yes` only in a reviewed, intentional deployment step. A test home is useful for validating the workflow without touching the real machine.
