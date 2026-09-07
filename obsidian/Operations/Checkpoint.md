# Working Checkpoint

**Date:** 2026-09-07
**Task:** Establish a portable AI configuration repository with a safe installation workflow and Obsidian knowledge base.
**Route:** Luna Medium.
**Delegations:** None.

## Changed

- Added repository README and agent instructions.
- Added a versioned global `AGENTS.md` source.
- Added a portable `config.toml` baseline and reviewer, researcher, and implementer agent definitions using the current `[agents]` schema.
- Added context-cost controls: 240k auto-compaction target, 12k tool-output limit, and documented compaction/splitting policy around the 272k long-context pricing boundary.
- Added a public-facing README and a repeatable heuristic privacy/secrets audit.
- Changed synchronization from replacement to additive merge: managed instruction blocks and TOML keys are updated while unrelated local configuration is preserved; custom agents use an `ai-configuration` namespace.
- Installed the additive configuration into the active local Codex home; existing files were backed up and the final sync check reports all managed targets current.
- Added ignored `.codex/AGENTS.md` personal policy for automatic owner-local synchronization and change explanations; it is intentionally excluded from publication.
- Added an interactive/check-only sync script with timestamped backups.
- Added the Obsidian-compatible documentation base, current-state record, research note, best-practices note, and unresolved-issues register.

## Validation completed

- `bash -n scripts/sync-config.sh` passed.
- Help/list modes passed.
- `--check` correctly reported a missing file in an isolated temporary `CODEX_HOME`.
- `--install --yes` created the target in the temporary home.
- Replacing a different target created a timestamped backup and a subsequent check passed.
- Real-machine check correctly reports the expected differences: the repository now adds the new context-cost policy, portable `config.toml`, and custom agents; no real machine file was changed.
- Official research confirmed the GPT-5.6 Sol long-context pricing rule and API token-count/compaction capabilities.
- Read-only audit found no concrete personal paths, names, email addresses, credentials, or tokens in the repository.
- Active config parsing confirmed routing, context policy, agent registration, and preservation of existing MCP/plugin sections.

## Next step

After user confirmation, run the additive installer and verify that `--check` reports all managed entries current while the existing local MCP/plugin/project settings remain present.
