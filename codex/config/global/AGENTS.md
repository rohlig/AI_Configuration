Global model-routing policy:

Runtime identity and routing:

- Treat each conversation as its current main/planning thread unless the platform explicitly identifies it as a delegated worker or supplies a bounded worker assignment. “Act as Sol 6.1 xhigh” alone is not evidence that another task should be created.
- Instructions and config defaults do not reveal the model or effort actually selected for this turn. Do not guess, announce, or claim a runtime model/effort unless the platform explicitly exposes it.
- Never stop, refuse, or ask the user to restart because model identity is missing or appears different from a configured default. Continue the assigned task with the current runtime; if a needed capability is unavailable, use a supported delegation or explain the concrete limitation.
- The model/effort matrix below is for selecting spawned/delegated workers, not for reclassifying or restarting the current main thread. Select a specific route only when the spawn mechanism supports it; if it does not, use the available mechanism without claiming an unverified model or effort.
- Delegated agents may use any model and effort supported by the current runtime. The normal worker default is `gpt-6.1-sol` at xhigh effort. Use Luna Low/Medium for simple work and Luna Medium for routine, cost-sensitive work. Route difficult and very hard work to Sol 6.1 at xhigh or max effort. Astra is used only when the user specifically requests it. Explicit per-task model/effort settings take precedence over the worker default.
- If a preferred delegated model or delegation tool is unavailable, continue with the best available model/tool. Never claim that no work was done merely because Sol or another preferred route is unavailable, and never invent a model identity or completion result.
- A delegated worker must recognize that it is a worker, not the primary assistant: execute only the assigned bounded subtask, do not restart the task, reinterpret the user's request as a new direct task, or spawn another worker by default. A worker must not create, fork, list, open, or wait on another chat/thread/task to perform its assigned work. Nested delegation requires an explicit instruction from the parent and a separately bounded scope; otherwise report the need back to the parent.

- Keep the main thread responsible for the plan, integration, and final answer. For substantial work that can be split into independent, bounded workstreams, normally delegate at least one useful workstream when a supported spawn mechanism is available and parallel work materially improves speed, coverage, or quality. Keep sequential, tightly coupled, shared-state, or small tasks in the main thread; account for duplicated context and token cost rather than spawning reflexively.
- Choose spawned-worker routes by task: use `gpt-6-luna` Low/Medium for simple bounded work and Luna Medium for routine, cost-sensitive tasks. Use `gpt-6.1-sol` at xhigh or max for difficult reasoning, uncertain state, complex recovery, architecture, security, concurrency, cross-system work, and very hard tasks. Use Astra only when the user specifically requests Astra. Use the lowest effort likely to handle the assigned scope safely; do not downgrade the model from Sol 6.1 due only to task difficulty.
- If the user explicitly says to ignore the optimized agentic configuration, obey that instruction for the current task and do not force delegation.
- For every delegation made by the primary parent, retain the returned agent ID and wait for the actual completion payload. A wait timeout means the agent is still unresolved, not hung or failed: poll again with a bounded longer wait, and use the agent's returned result/notification as the source of truth before reporting or integrating. A worker must not apply this parent responsibility to itself. Never claim Sol produced no result merely because one wait call timed out; terminate only after an explicit error, shutdown, or a genuinely exhausted recovery path.
- Optimize tokens deliberately: inspect targeted files first, reuse existing generated indexes and tests, search with `rg`, avoid loading large unrelated files, keep delegated scopes narrow, use checkpoints instead of repeating discovery, and summarize only decisions/evidence needed for continuation. Increase reasoning effort before increasing context volume.
- Ask early about actual requirements only when a material ambiguity or subjective tradeoff cannot be resolved safely; do not ask which model to use when routing is clear.
- Be concise and transparent about actual delegation when it occurs. Never invent model identity, effort, delegation, or routing. Do not expose private chain-of-thought.
- For substantial tasks, complete implementation and relevant validation; do not stop at a plan unless requested. Preserve project-specific instructions and normal approval boundaries.

Delegation handoff contract:

- The primary parent must mark delegated prompts explicitly with `WORKER TASK — DO NOT DELEGATE` and include the bounded scope, read/write permission, expected completion payload, and parent task/agent ID when available.
- A worker receiving that marker must remain in the current task until completion. A request to “act as Sol 6.1 xhigh” changes the worker's model/effort or review role; it does not authorize creating another task.
- If the runtime does not expose worker identity or the delegation marker is missing, do not create a task to resolve the ambiguity. Continue the current bounded work and report the ambiguity to the parent.

<!-- AI_CONFIGURATION:BEGIN context-cost-policy -->
## Context and cost discipline

- Treat context as a budget. Prefer targeted file reads, short checkpoints, and compact handoffs over repeating the full conversation or repository state.
- If the context indicator or an API token count approaches 240k input tokens, stop adding broad history, compact or summarize at a milestone, and continue from the compact checkpoint.
- Keep a hard safety buffer below 272k input tokens for models where the provider applies a long-context pricing tier. Do not knowingly cross that boundary without an explicit reason and user approval.
- Split work only when the parts are genuinely independent or can use disjoint file scopes. Give each agent a short task brief and only the files or facts it needs; do not send the complete transcript to every agent.
- Prefer one primary agent plus a small number of bounded specialists. Ask specialists for concise structured results, then integrate once in the primary context.
- When an API is available, count input tokens before the request and use provider-supported compaction after major tool-heavy milestones. Never assume that “the model can fit it” means “the request is cost-efficient.”
<!-- AI_CONFIGURATION:END context-cost-policy -->

Obsidian codebase audit and continuity contract:

- Every substantial codebase must have an Obsidian-compatible Markdown representation explaining scope, architecture, intent, data/control flows, dependencies, operational paths, performance constraints, tests, and why significant changes were made. Keep it current after every substantive change, including work performed under an explicit configuration override.
- Before doing other work in a substantial codebase without that audit, tell the user that the Obsidian Markdown code audit is missing and ask whether it should be created now, later, or not needed. If the user chooses “not needed”, record that decision in the project `AGENTS.md` and do not ask again for that codebase.
- Maintain a lightweight working checkpoint in the audit (current task, files, decisions, validation, model/effort, delegations/agent IDs/status, and next step). Update it at meaningful milestones and before handoff or context exhaustion. Keep a separate unresolved-issues register; record every discovered problem that is not fixed immediately, surface open items in the final summary, and keep them until resolved or explicitly ignored.
- Final summaries and checkpoints must state what was changed, debugged, and validated, and identify the model and effort used for each meaningful portion. Do not claim a delegated result until its completion payload has been received.

<!-- AI_CONFIGURATION:BEGIN runtime-routing-contract -->
## AI Configuration runtime routing contract

This managed block is authoritative for runtime routing when earlier local instructions conflict:

- The portable `config.toml` may set GPT-6 Luna Medium as the installation's requested session default; this is not proof of the active model/effort and must not trigger self-routing or restart checks. Spawned workers normally default to GPT-6.1 Sol xhigh; bounded simple work may use Luna Low/Medium, and Astra is used only when specifically requested by the user. A delegated worker is already the current task's worker and must not restart the task or act as a new primary assistant.
- Use GPT-6 Luna Low/Medium for simple computer-use tasks and Luna Medium for routine work. Use GPT-6.1 Sol at xhigh or max for demanding UI workflows, uncertain state, complex recovery, cross-application reasoning, and very hard work. Use Astra only when the user specifically requests Astra.
- A delegated worker must stay within its assigned bounded scope. It must not create, fork, list, open, or wait on another chat, thread, or task, and must not spawn another worker by default.
- Nested delegation requires explicit authorization from the parent plus a separate bounded scope. “Act as Sol 6.1 xhigh” selects the current worker's route; it does not authorize another task.
- Parent prompts should begin with `WORKER TASK — DO NOT DELEGATE` and include scope, read/write permission, expected completion payload, and parent task/agent ID when available.
- If worker identity or the marker is missing, continue the current bounded work and report the ambiguity; do not create another task to resolve it.
- For substantial delegated work, emit a concise milestone checkpoint after discovery, each major decision or implementation batch, and validation. Include objective, completed work, evidence/files, decisions, unresolved risks, and next step. The parent must persist each meaningful checkpoint in the project audit or `obsidian/Codex/Operations/Checkpoint.md` before continuing.
- A read-only worker must report checkpoints through the parent/task channel and must not edit documentation unless write access was explicitly authorized. If documentation writes are authorized, update the smallest relevant checkpoint or audit note rather than creating verbose logs.
- When context, time, or credit risk becomes material, stop broad exploration and return a compact checkpoint immediately; do not wait for a final completion payload as the only durable record. The parent must save that checkpoint before starting more work or handing off.
<!-- AI_CONFIGURATION:END runtime-routing-contract -->
