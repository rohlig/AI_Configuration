# Current Configuration

**Checked:** 2026-09-08

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

GPT-6 Astra is available as an escalation route for extreme end-to-end work and complex computer-control workflows; Luna Medium remains the normal default and Astra is not configured as the baseline model.

A later active-machine comparison found root-level `default_subagent_model` and `default_subagent_reasoning_effort` alongside the `[agents]` values. Those two portable compatibility values are now versioned; notifications, project trust, plugins, desktop settings, and MCP paths remain excluded.

## Baseline decisions

- Global instructions are conservative and tool-agnostic.
- Portable configuration contains only reviewed, non-secret defaults; machine-specific configuration remains documented but excluded.
- Installation requires confirmation per file unless the operator explicitly uses `--yes`.
