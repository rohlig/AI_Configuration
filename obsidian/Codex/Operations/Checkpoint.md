# Working Checkpoint

**Date:** 2026-10-08
**Task:** Update routing to GPT-6.1 Sol at higher reasoning effort for very hard work and Astra only on explicit user request.
**Route:** GPT-6 Luna Medium for this bounded documentation/configuration task; actual runtime model/effort metadata was unavailable.
**Delegations:** None.

## Latest routing update (2026-10-08)

Portable worker defaults now use `gpt-6.1-sol` at xhigh. Difficult and very hard work stays on Sol 6.1, using xhigh or max; Astra is used only when specifically requested by the user. Luna Low/Medium remains for simple or routine cost-sensitive tasks. Updated source: `config.toml`, global `AGENTS.md`, README, and the routing/current-configuration/research notes. OpenAI's official model page checked 2026-10-08 describes Sol 6.1 as near-Astra performance for complex work at lower cost and lists xhigh and max reasoning efforts. The owner authorized standing automatic sync of validated portable Codex configuration changes to this machine; the repo instructions now record that preference. This update was installed to `~/.codex/AGENTS.md` and `~/.codex/config.toml`, with backups at `~/.codex/backups/ai-configuration/20261008-142705/`; final sync check reports all managed files current, and both legacy and `[agents]` defaults are Sol 6.1 xhigh. No unresolved issue was identified. Validation passed: TOML parsed with both worker aliases set to the expected model/effort; shell syntax check, help, public audit, and `git diff --check` passed. An isolated temporary Codex home correctly reported managed targets missing in `--check` mode.

## Latest routing clarification

Historical note (superseded 2026-10-08): earlier routing documentation used Luna High/Max as the middle step and the previous Sol model at High effort for harder reasoning, with Astra for extreme tasks. The current policy uses Sol 6.1 xhigh/max for difficult and very hard work, with Astra only on explicit request.

Historical note (superseded 2026-10-08): an earlier policy described Luna High/Max as an explicit performance/cost option for difficult work. Current routing uses Luna Low/Medium for simple or routine cost-sensitive work and Sol 6.1 xhigh/max for difficult and very hard work.

Previous versions incorrectly told the primary thread to restart when its runtime did not match Luna Medium. That rule is removed: a config default does not establish the active model, and the task should continue in the main/planning thread. Delegated agents may use any available model and effort and should continue if a preferred route such as Sol is unavailable.

Correction (2026-10-01): no instruction can establish the active model/effort when the runtime does not expose it. The current thread continues as main/planning unless explicitly identified as a worker; missing or unexpected model labels are never a reason to stop, refuse, or request a restart. Model/effort routing is for spawned workers only and is applied only when the spawn mechanism supports it. Delegate substantial work by default only when independent bounded workstreams benefit from parallelism; keep sequential/shared-state work together to limit duplicate context and cost.

The worker contract is now explicit: a delegated agent must stay within its assigned bounded subtask and must not spawn a further worker unless the parent explicitly authorizes nested delegation with a separate scope.

The contract now also forbids worker-side chat/thread/task management. Parent delegation prompts should carry an explicit `WORKER TASK — DO NOT DELEGATE` marker; model selection such as “Act as Sol 6.1 xhigh” does not authorize another task.

The active machine configuration was compared again after another job changed it. Only the portable legacy root aliases for subagent model and effort were added to the repository source; machine-specific notification, project-trust, plugin, desktop, and MCP values remain excluded. The AGENTS merge was also corrected so its check compares the computed merged result with the original target and manages a dedicated runtime-routing block. The global worker instructions were re-synchronized locally afterward.

Milestone durability is now explicit: substantial workers must send compact checkpoints after meaningful phases and before context, time, or credit risk becomes critical; the parent must persist them before continuing. Read-only workers report through the task channel, while documentation writes require explicit authorization.

Historical routing note (superseded 2026-10-08): the older policy routed uncertain computer use to Sol at High effort and reserved Astra for extreme cases. Current computer-use routing uses Sol 6.1 xhigh/max for demanding and very hard tasks; Astra is used only on explicit user request.

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

- Removed the unsupported primary-thread model/effort self-check and restart message; documented that current-thread role and runtime model identity are separate.
- Clarified that model/effort recommendations govern spawned workers only, and that model selection is claimed only when the spawn mechanism supports it.
- Added a complexity/decomposability threshold for proactive delegation to balance parallel benefit against duplicated context and token cost.
- Fixed an additive-sync idempotency defect found during isolated testing: a fresh AGENTS merge introduced leading blank lines, so the immediate `--check` failed until a second merge. The merge now omits the separator when inserting at the start of a file.
- Removed an old machine-specific absolute path from this public checkpoint after the privacy audit flagged it.

- Re-synced the changed global `AGENTS.md` additively into the local Codex home; the prior local file was backed up. The subsequent local `--check` passed.
- `--help`, public audit, Python syntax compilation, shell syntax check, `git diff --check`, and fresh temporary-`CODEX_HOME` install followed by `--check` passed after the idempotency fix.
- Repository search found no remaining `gpt-5` or `5.6` routing references.

- Updated the portable config, global routing policy, routing matrix, current-configuration note, research note, token-cost guidance, and this checkpoint to use only the GPT-6 model family.
- Set primary defaults to `gpt-6-luna` Medium and worker defaults to `gpt-6.1-sol` xhigh; documented Astra as opt-in by explicit user request.
- Official OpenAI model guidance confirms the three model IDs, their workload positioning, current prices, and the over-272k pricing boundary.

- `bash -n codex/scripts/sync-config.sh` passed.
- Help/list modes passed.
- `--check` correctly reported a missing file in an isolated temporary `CODEX_HOME`.
- `--install --yes` created the target in the temporary home.
- Replacing a different target created a timestamped backup and a subsequent check passed.
- Real-machine check reports all managed targets current after the structure-only source path update; no configuration content needed to change.
- Official research confirmed current GPT-6 long-context pricing and API token-count/compaction capabilities.
- Read-only audit found no concrete personal paths, names, email addresses, credentials, or tokens in the repository.
- Active config parsing confirmed routing, context policy, agent registration, and preservation of existing MCP/plugin sections.

## Next step

Keep the public/general versus Codex-specific boundary clear when adding future documentation or configuration.
