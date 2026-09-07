# Current Configuration

**Checked:** 2026-09-07

## Repository state

The repository began empty apart from Git. The initial portable baseline now consists of:

- `config/global/AGENTS.md`: the current reusable global routing and continuity instructions.
- `config/global/config.toml`: portable baseline with model, approval, sandbox, cached web search, feature, and current `[agents]` defaults.
- `config/global/agents/*.toml`: reviewer, researcher, and implementer definitions installed under the `ai-configuration` namespace.
- The existing machine file was not copied wholesale because it includes machine-specific paths, runtime integration values, and sensitive environment-related values.

## Machine targets

Official Codex documentation identifies these user-level targets:

- `~/.codex/AGENTS.md` (or `$CODEX_HOME/AGENTS.md`) for global instructions.
- `~/.codex/config.toml` (or `$CODEX_HOME/config.toml`) for user-level settings.

The current repository has not installed or overwritten either target. Run `./scripts/sync-config.sh --check` to compare the managed source with the current machine.

## Existing machine inventory

The inspected machine currently contains:

- `AGENTS.md` with model-routing and Obsidian continuity policy; this is now versioned as the global source.
- `config.toml` sections for model and reasoning defaults, subagent defaults, notifications/service tier, feature flags, trusted project paths, marketplace/plugin enablement, desktop preferences, and MCP/runtime integrations.
- Other state such as authentication, databases, session indexes, caches, rules, and plugin/runtime files.

The portable baseline manages the first category plus the safe model/agent/feature settings. Synchronization is additive: project trust paths, MCP runtime configuration, plugin installation state, credentials, and runtime state remain machine-local and are preserved during installation.

## Baseline decisions

- Global instructions are conservative and tool-agnostic.
- Portable configuration contains only reviewed, non-secret defaults; machine-specific configuration remains documented but excluded.
- Installation requires confirmation per file unless the operator explicitly uses `--yes`.
