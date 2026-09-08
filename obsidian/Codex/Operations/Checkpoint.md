# Working Checkpoint

**Date:** 2026-09-08
**Task:** Establish a portable AI configuration repository with a safe installation workflow and Obsidian knowledge base.
**Route:** Luna Medium.
**Delegations:** None.

## Latest routing clarification

The primary/direct-chat Luna Medium requirement must not be propagated as a restriction to delegated agents. Delegated agents may use any available model and effort, and must continue with the best available route if a preferred model such as Sol is unavailable. The primary-chat restart message applies only to the primary assistant.

The worker contract is now explicit: a delegated agent must stay within its assigned bounded subtask and must not spawn a further worker unless the parent explicitly authorizes nested delegation with a separate scope.

The contract now also forbids worker-side chat/thread/task management. Parent delegation prompts should carry an explicit `WORKER TASK — DO NOT DELEGATE` marker; model selection such as “Act as Sol High” does not authorize another task.

The active machine configuration was compared again after another job changed it. Only the portable legacy root aliases for subagent model and effort were added to the repository source; machine-specific notification, project-trust, plugin, desktop, and MCP values remain excluded. The AGENTS merge was also corrected so its check compares the computed merged result with the original target and manages a dedicated runtime-routing block. The global worker instructions were re-synchronized locally afterward.

Milestone durability is now explicit: substantial workers must send compact checkpoints after meaningful phases and before context, time, or credit risk becomes critical; the parent must persist them before continuing. Read-only workers report through the task channel, while documentation writes require explicit authorization.

GPT-6 Astra was added as an escalation route for extreme end-to-end work and complex computer-control workflows. Luna Medium remains the default; Astra is not a baseline setting and should use the lowest suitable effort.

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

## Structure update

- Moved all Codex-specific source and tooling under `codex/`.
- Separated general AI-assisted coding guidance into `obsidian/General/`.
- Grouped Codex-specific architecture, installation, agent, research, operations, and context-budget notes under `obsidian/Codex/`.
- Updated README, repository instructions, local personal instructions, and all validation paths.
- Corrected custom-agent identity fields to match their registered `portable_*` names and removed hard-coded Luna/Medium overrides so routing can vary per task.

## Validation completed

- `bash -n codex/scripts/sync-config.sh` passed.
- Help/list modes passed.
- `--check` correctly reported a missing file in an isolated temporary `CODEX_HOME`.
- `--install --yes` created the target in the temporary home.
- Replacing a different target created a timestamped backup and a subsequent check passed.
- Real-machine check reports all managed targets current after the structure-only source path update; no configuration content needed to change.
- Official research confirmed the GPT-5.6 Sol long-context pricing rule and API token-count/compaction capabilities.
- Read-only audit found no concrete personal paths, names, email addresses, credentials, or tokens in the repository.
- Active config parsing confirmed routing, context policy, agent registration, and preservation of existing MCP/plugin sections.

## Next step

Keep the public/general versus Codex-specific boundary clear when adding future documentation or configuration.
