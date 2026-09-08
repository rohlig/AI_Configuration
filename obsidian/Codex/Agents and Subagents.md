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
| Extreme end-to-end work or complex computer control | `gpt-6-astra` | `high`, `xhigh`, or `max` |

This is a routing policy, not four copies of every role. The role determines how the agent works; the spawn-time model and effort determine how much reasoning it uses. Explicit spawn values take precedence over `[agents]` defaults.

## Primary versus delegated routing

The Luna Medium default is for the primary assistant handling the direct user conversation. It is not a restriction on delegated workers. A parent agent may assign a delegated task to any model and effort supported by the current runtime, including Luna, Sol, Terra, GPT-6 Astra, or another available model, when that is appropriate for the task. Explicit model and effort settings on a delegated task take precedence over the primary default.

GPT-6 Astra is an escalation route, not a new default: use it for extreme end-to-end tasks or complex computer-control workflows where its additional capability is justified. Start at the lowest suitable effort and avoid using it for routine work because its cost is materially higher.

If a preferred model or delegation tool is unavailable, the worker must continue with the best available route and report what was actually used. It must not refuse work, claim that no files were inspected, or emit the primary-chat restart message solely because Sol or another preferred route is unavailable.

## Worker identity and nested delegation

Every delegated task starts as a worker task, even when its assigned model is Sol or another high-capability model. The worker executes only the bounded scope supplied by its parent and must not reinterpret the request as a new primary chat. It must not create, fork, list, open, or wait on another chat/thread/task, and must not spawn another worker by default. Nested delegation is allowed only when the parent explicitly authorizes it and gives a separate bounded scope; otherwise the worker reports the need back to the parent.

The parent should prefix each delegated prompt with `WORKER TASK — DO NOT DELEGATE` and provide the scope, read/write permission, expected completion payload, and parent task/agent ID when available. “Act as Sol High” selects the worker's route; it is not permission to create another task. If the marker or runtime worker identity is missing, the current task continues and the ambiguity is reported rather than resolved by spawning another task.

## Milestones and durable handoffs

For substantial work, the worker returns a concise checkpoint after discovery, each major decision or implementation batch, and validation. Each checkpoint contains: objective, completed work, evidence and file paths, decisions/assumptions, unresolved risks, and next step. The parent persists meaningful checkpoints in the project audit or `obsidian/Codex/Operations/Checkpoint.md` before continuing. A final completion payload is not the only durable handoff.

Read-only workers report these checkpoints through the parent/task channel and do not edit documentation. If the parent explicitly grants documentation write access, the worker updates only the smallest relevant checkpoint or audit note. Near context, time, or credit limits, the worker stops broad exploration and sends a compact checkpoint immediately.

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
