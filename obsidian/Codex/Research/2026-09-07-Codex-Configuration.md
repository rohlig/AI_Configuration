# Codex Configuration Research — 2026-09-07

## Sources checked

- [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)
- [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

## Findings

- User-level configuration is read from `~/.codex/config.toml`; `CODEX_HOME` can change the Codex home.
- Global instructions are read from `AGENTS.override.md` if present, otherwise `AGENTS.md`, in the Codex home.
- Repository `.codex/config.toml` files are project-scoped and only load when the project is trusted.
- Codex combines global and project `AGENTS.md` files from broader to more specific scope; closer files appear later and can refine earlier guidance.
- CLI flags and `--config` overrides have higher precedence than project, profile, user, and system settings.
- The documented common settings include `model`, `approval_policy`, `sandbox_mode`, and `web_search`.
- Current official agent configuration supports `[agents]` keys for `enabled`, `max_concurrent_threads_per_session`, `default_subagent_model`, `default_subagent_reasoning_effort`, and `interrupt_message`.
- Custom agents use `name`, `description`, and `developer_instructions`; they can also set supported config values such as `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, and `skills.config`.
- Explicit model and reasoning values supplied when spawning an agent take precedence over the global `[agents]` defaults.
- The official GPT-5.6 Sol model page states that prompts over 272k input tokens receive 2× input and 1.5× output pricing for the full request, despite the model exposing a 1.05M context window.
- The API exposes input-token counting and Responses compaction operations; compaction should be used at milestones rather than mechanically on every turn.

## Design impact

The repository now manages a portable `config.toml` baseline and three custom agents. The existing machine configuration was reviewed for categories but not copied wholesale; secrets, local paths, MCP runtime state, and project-specific trust settings remain excluded. The installer uses `$CODEX_HOME` and asks before machine-level writes.

The baseline now also sets a 240k auto-compaction target and a 12k tool-output retention limit. These are conservative policy choices, not guarantees about the final request size.

## Model-routing update — 2026-09-08

The official [GPT-6 Astra model documentation](https://developers.openai.com/api/docs/models/gpt-6-astra) describes Astra as OpenAI's most capable model for complex reasoning, coding, computer use, research, and document creation, with `low` through `max` reasoning effort. The routing policy therefore keeps Luna Medium as the default and reserves `gpt-6-astra` for extreme end-to-end tasks and complex computer-control workflows. This is an escalation rule, not a request to change the global baseline or use Astra for routine work.

## Research limits

This note does not claim that every desktop-app preference, plugin connection, skill cache, model entitlement, or account state is portable through these files. Re-check the official docs before adding new managed targets.
