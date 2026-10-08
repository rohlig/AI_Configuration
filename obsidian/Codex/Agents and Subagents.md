# Agents and Subagents

## Global defaults

`codex/config/global/config.toml` registers the current `[agents]` configuration and custom roles. The three files are role prompts, not model variants. They intentionally omit `model` and `model_reasoning_effort`, so they inherit the subagent defaults or can be launched with an explicit model/effort for the individual task. The portable config requests GPT-6 Luna Medium as the session default; spawned workers default to GPT-6.1 Sol xhigh, with up to six concurrently open spawned-agent threads. A config default is not runtime introspection and must not be used to infer the active model or effort.

## Routing matrix

| Situation | Recommended model | Effort |
|---|---|---|
| Mechanical lookup, narrow review, small bounded edit | `gpt-6-luna` | `low` |
| Normal implementation, research, or review | `gpt-6-luna` | `medium` |
| Routine, cost-sensitive work | `gpt-6-luna` | `medium` |
| Difficult reasoning, architecture, security, concurrency, recovery, or cross-system work | `gpt-6.1-sol` | `xhigh` or `max` |
| Simple, well-bounded computer use | `gpt-6-luna` | `low` or `medium` |
| Demanding multi-step computer use, uncertain state, recovery, or cross-app reasoning | `gpt-6.1-sol` | `xhigh` or `max` |
| Astra specifically requested by the user | `gpt-6-astra` | `high`, `xhigh`, or `max` |

This is a routing policy, not four copies of every role. The role determines how the agent works; the spawn-time model and effort determine how much reasoning it uses. Explicit spawn values take precedence over `[agents]` defaults.

## Current thread versus spawned-worker routing

Treat the current conversation as the main/planning thread unless the platform explicitly identifies it as a delegated worker or supplies a bounded worker assignment. Model/effort recommendations below apply when selecting spawned workers; they do not reclassify or restart the current thread. If runtime model metadata is missing, continue normally and do not guess or claim a model. If the spawn mechanism cannot select a model or effort, use the available mechanism without claiming an unverified route. Explicit supported spawn-time settings take precedence over worker defaults.

The main thread owns planning, integration, and the final answer. For substantial tasks, delegate at least one independent, bounded workstream when parallel work materially improves speed, coverage, or quality and a supported spawn mechanism is available. Keep small, sequential, tightly coupled, or shared-state work in the main thread; duplicated context and token cost count against delegation.

GPT-6 Luna, GPT-6.1 Sol, and GPT-6 Astra support Computer Use. Use Luna Low/Medium for straightforward UI operations. Use Sol 6.1 at xhigh or max for demanding sequences, uncertain UI state, complex recovery, cross-application reasoning, and very hard work. Use Astra only when the user specifically requests it. OpenAI describes Sol 6.1 as near-Astra performance at lower cost; the user-facing routing policy therefore keeps difficult work on Sol 6.1 unless Astra is specifically requested.

If a preferred model or delegation tool is unavailable, continue with the best available route and report the concrete limitation only when relevant. Do not refuse work, claim that no files were inspected, or emit a restart message because a preferred route or model label is unavailable.

## Worker identity and nested delegation

Every delegated task starts as a worker task, even when its assigned model is Sol or another high-capability model. The worker executes only the bounded scope supplied by its parent and must not reinterpret the request as a new primary chat. It must not create, fork, list, open, or wait on another chat/thread/task, and must not spawn another worker by default. Nested delegation is allowed only when the parent explicitly authorizes it and gives a separate bounded scope; otherwise the worker reports the need back to the parent.

The parent should prefix each delegated prompt with `WORKER TASK — DO NOT DELEGATE` and provide the scope, read/write permission, expected completion payload, and parent task/agent ID when available. “Act as Sol 6.1 xhigh” selects the worker's route; it is not permission to create another task. If the marker or runtime worker identity is missing, the current task continues and the ambiguity is reported rather than resolved by spawning another task.

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
Use `gpt-6-luna` at low or medium effort for simple or routine cost-sensitive work. Use `gpt-6.1-sol` at xhigh or max for difficult and very hard reasoning, uncertain state, recovery, or systems work. Use `gpt-6-astra` only when the user specifically requests it. The parent may specify another route.
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
