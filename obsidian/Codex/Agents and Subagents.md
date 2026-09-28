# Agents and Subagents

## Global defaults

`codex/config/global/config.toml` registers the current `[agents]` configuration and custom roles. The three files are role prompts, not model variants. They intentionally omit `model` and `model_reasoning_effort`, so they inherit the subagent defaults or can be launched with an explicit model/effort for the individual task. The primary default is GPT-6 Luna Medium; the worker default is GPT-6 Sol High, with up to six concurrently open spawned-agent threads.

## Routing matrix

| Situation | Recommended model | Effort |
|---|---|---|
| Mechanical lookup, narrow review, small bounded edit | `gpt-6-luna` | `low` |
| Normal implementation, research, or review | `gpt-6-luna` | `medium` |
| Difficult but bounded reasoning where cost matters | `gpt-6-luna` | `high` or `max` |
| Difficult architecture, security, concurrency, or cross-system reasoning | `gpt-6-sol` | `high` |
| Simple, well-bounded computer use | `gpt-6-luna` | `low` or `medium` |
| Demanding but bounded multi-step computer use | `gpt-6-luna` | `high` or `max` |
| Computer control with uncertain state, complex recovery, or cross-app reasoning | `gpt-6-sol` | `high` or `xhigh` |
| Extreme end-to-end work or computer control beyond Sol | `gpt-6-astra` | `high`, `xhigh`, or `max` |

This is a routing policy, not four copies of every role. The role determines how the agent works; the spawn-time model and effort determine how much reasoning it uses. Explicit spawn values take precedence over `[agents]` defaults.

## Primary versus delegated routing

GPT-6 Luna Medium is the primary assistant default. Delegated workers default to GPT-6 Sol High. For difficult but bounded work where Luna is likely sufficient, use Luna High or Max before escalating to Sol; simple subtasks can use Luna Low or Medium. Explicit model and effort settings on a delegated task take precedence over these defaults.

All three GPT-6 models support Computer Use. Use Luna Low/Medium for straightforward UI operations and Luna High/Max for demanding but bounded interaction sequences. Use Sol High when the UI state is uncertain, recovery is complex, or several applications require coordinated reasoning. Reserve Astra for extreme workflows beyond Sol. OpenAI describes Astra as state-of-the-art for computer use; the official guidance does not claim that every GPT-6 model outperforms the prior generation in every UI task. Astra's per-token price is higher, so reserve it for workflows that need its capability.

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
Use gpt-6-luna at high effort for difficult but bounded work where Luna is likely sufficient. Use gpt-6-sol at high effort when the task needs stronger reasoning across uncertain state, recovery, or systems. The parent may specify another route.
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
