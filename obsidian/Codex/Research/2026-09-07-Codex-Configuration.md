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
- The API exposes input-token counting and Responses compaction operations; compaction should be used at milestones rather than mechanically on every turn.

## Design impact

The repository now manages a portable `config.toml` baseline and three custom agents. The existing machine configuration was reviewed for categories but not copied wholesale; secrets, local paths, MCP runtime state, and project-specific trust settings remain excluded. The installer uses `$CODEX_HOME` and asks before machine-level writes.

The baseline now also sets a 240k auto-compaction target and a 12k tool-output retention limit. These are conservative policy choices, not guarantees about the final request size.

## Model-routing update — 2026-09-28; runtime policy correction — 2026-10-01

Current [OpenAI model guidance](https://developers.openai.com/api/docs/models) identifies `gpt-6-luna` for efficient, focused work, `gpt-6-sol` for complex coding and agentic workflows, and `gpt-6-astra` for the hardest end-to-end work. The [Luna](https://developers.openai.com/api/docs/models/gpt-6-luna), [Sol](https://developers.openai.com/api/docs/models/gpt-6-sol), and [Astra](https://developers.openai.com/api/docs/models/gpt-6-astra) model pages all list Computer Use support. The [model guide](https://developers.openai.com/api/docs/guides/latest-model) calls Astra state-of-the-art for computer use, and the [September 25 changelog](https://developers.openai.com/api/docs/changelog) reports image-encoding improvements for Luna and Sol that affect visual tasks including computer use. This supports routing simple UI work to Luna and more complex sequences to Sol High, reserving Astra for extreme cases; it does not establish a blanket comparative win over the previous generation for every model and UI task.

The portable config requests Luna Medium as the session default, but this does not let the assistant inspect the model or effort actually selected by the host. Do not infer identity from a config value, and never stop or request a restart because the runtime does not expose model metadata. Treat the current conversation as the main/planning thread unless explicitly marked as a worker. The routing matrix is for spawned workers: Luna High/Max is the cost-conscious middle step for difficult but bounded reasoning and demanding UI workflows; use Sol High when uncertainty, recovery, or cross-system reasoning warrants it, and Astra only for extreme tasks. Select a specific model/effort only when the spawn mechanism supports it.

Delegate substantial work by default when independent, bounded workstreams make parallelism materially better. Keep short, sequential, shared-state, or tightly coupled work in the main thread: official [multi-agent guidance](https://developers.openai.com/api/docs/guides/responses-multi-agent) notes that subagents increase token use and are less useful for dependent steps or shared mutable state.

On 2026-10-01, the routing instructions were corrected after a thread falsely treated missing runtime model metadata as proof of a bad start and asked for a restart. The assistant has no model/effort introspection tool in this task's available tool surface; therefore, the portable policy does not attempt to self-verify runtime identity. Continue in the current main/planning role unless the host explicitly identifies a worker. This observation is about the available runtime surface, not a claim that every Codex product or future version lacks model metadata.

Official model pages checked on this date list standard prices per million tokens as Luna $0.10 input/$0.50 output, Sol $2/$10, and Astra $10/$50. All three document the 2× input/cache and 1.5× output pricing for prompts exceeding 272k input tokens. Check again before future routing changes because prices and availability may change.

## Research limits

This note does not claim that every desktop-app preference, plugin connection, skill cache, model entitlement, or account state is portable through these files. Re-check the official docs before adding new managed targets.
