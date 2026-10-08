# Current Configuration

**Checked:** 2026-10-08

## Repository state

The repository began empty apart from Git. The initial portable baseline now consists of:

- `codex/config/global/AGENTS.md`: the current reusable global routing and continuity instructions.
- `codex/config/global/config.toml`: portable baseline with model, approval, sandbox, cached web search, feature, current `[agents]` defaults, and legacy root-level subagent aliases for compatibility with existing installations.
- `codex/config/global/agents/*.toml`: reviewer, researcher, and implementer definitions installed under the `ai-configuration` namespace.
- The existing machine file was not copied wholesale because it includes machine-specific paths, runtime integration values, and sensitive environment-related values.

## Machine targets

Official Codex documentation identifies these user-level targets:

- `~/.codex/AGENTS.md` (or `$CODEX_HOME/AGENTS.md`) for global instructions.
- `~/.codex/config.toml` (or `$CODEX_HOME/config.toml`) for user-level settings.

Run `./codex/scripts/sync-config.sh --check` to compare the managed Codex source with the current machine.

## Existing machine inventory

The inspected machine currently contains:

- `AGENTS.md` with model-routing and Obsidian continuity policy; this is now versioned as the global source.
- `config.toml` sections for model and reasoning defaults, subagent defaults, notifications/service tier, feature flags, trusted project paths, marketplace/plugin enablement, desktop preferences, and MCP/runtime integrations.
- Other state such as authentication, databases, session indexes, caches, rules, and plugin/runtime files.

The portable baseline manages the first category plus the safe model/agent/feature settings. Synchronization is additive: project trust paths, MCP runtime configuration, plugin installation state, credentials, and runtime state remain machine-local and are preserved during installation.

The portable `config.toml` requests GPT-6 Luna at medium effort as the session default; the configuration is not a way for an assistant to inspect the runtime-selected model or effort. The current conversation should continue as the main/planning thread unless explicitly identified as a worker. Spawned workers default to GPT-6.1 Sol xhigh. Use Luna Low/Medium for simple or routine cost-sensitive work; use Sol 6.1 xhigh/max for difficult and very hard work. Use Astra only when the user specifically requests it. Spawn-time routing recommendations apply only when the tool supports those selections. OpenAI's model guidance checked 2026-10-08 describes Sol 6.1 as near-Astra performance at lower cost: [model page](https://developers.openai.com/api/docs/models/gpt-6.1-sol).

A later active-machine comparison found root-level `default_subagent_model` and `default_subagent_reasoning_effort` alongside the `[agents]` values. Those two portable compatibility values are now versioned; notifications, project trust, plugins, desktop settings, and MCP paths remain excluded.

## Baseline decisions

- Global instructions are conservative and tool-agnostic.
- Portable configuration contains only reviewed, non-secret defaults; machine-specific configuration remains documented but excluded.
- Installation requires confirmation per file unless the operator explicitly uses `--yes`.
