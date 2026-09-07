# Agents and Subagents

## Global defaults

`codex/config/global/config.toml` registers the current `[agents]` configuration and custom roles. The three files are role prompts, not model variants. They intentionally omit `model` and `model_reasoning_effort`, so they inherit the global defaults and can be launched with an explicit model/effort for the individual task. The repository defaults are Luna at medium effort, with up to six concurrently open spawned-agent threads.

## Routing matrix

| Situation | Recommended model | Effort |
|---|---|---|
| Mechanical lookup, narrow review, small bounded edit | `gpt-5.6-luna` | `low` |
| Normal implementation, research, or review | `gpt-5.6-luna` | `medium` |
| Ambiguous or multi-step work within the cost budget | `gpt-5.6-luna` | `high` or `max` |
| Difficult architecture, security, concurrency, or cross-system reasoning | `gpt-5.6-sol` / `gpt-5.6` | `medium` or `high` |

This is a routing policy, not four copies of every role. The role determines how the agent works; the spawn-time model and effort determine how much reasoning it uses. Explicit spawn values take precedence over `[agents]` defaults.

## Correct delegation pattern

1. Keep the main task moving locally; delegate only a bounded, non-overlapping subtask.
2. State the exact question or write scope, expected output, and constraints.
3. Use an explicit model and reasoning effort when the subtask needs different tradeoffs; do not escalate every task by default.
4. Retain the returned agent ID.
5. Wait for the actual completion payload before reporting or integrating the result.
6. Review returned changes or evidence, then update the checkpoint and unresolved-issues register.

Example prompt shape:

```text
Review only src/auth/ for security regressions introduced by the current diff.
Do not edit files. Return findings with file paths, severity, and evidence.
Use gpt-5.6-luna at medium effort.
```

## Custom agent files

Files under `codex/config/global/agents/` use the official schema and are installed under the `ai-configuration` namespace:

- `name` — stable role identifier.
- `description` — when the role is useful.
- `developer_instructions` — role behavior and boundaries.
- Optional supported overrides such as `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, or `skills.config`. Leave model and effort unset in reusable role prompts unless the role genuinely requires a fixed capability.

The main `config.toml` connects roles through `[agents.<role>]` and `config_file`. Relative paths resolve from the declaring config file. The installer places the files under `$CODEX_HOME/agents/ai-configuration/` so existing custom agents are not overwritten.

## Role guidance

- `portable_reviewer`: read-only risk and correctness review.
- `portable_researcher`: bounded, source-backed investigation.
- `portable_implementer`: bounded implementation with validation and explicit handoff.

Do not put credentials or machine-specific MCP endpoints in a shared agent file. If an agent needs a sensitive or local integration, configure it on the machine or project where it is used and document the boundary.
