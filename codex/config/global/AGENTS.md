Global model-routing policy:

Primary/direct-chat routing and delegated-agent routing are different:

- The primary assistant handling the user's direct chat should normally start with `gpt-5.6-luna` at Medium effort and announce that route.
- The Luna startup requirement applies to the primary/direct assistant only. It must not be copied into a delegated worker's task as a requirement to restart or refuse work.
- Delegated agents may use any model and effort supported by the current runtime, including Luna, Sol, Terra, or another available model. The parent agent should choose an appropriate route when useful; explicit model/effort settings for a delegated task take precedence over the primary default.
- If a preferred delegated model or delegation tool is unavailable, continue with the best available model/tool. Never claim that no work was done merely because Sol or another preferred route is unavailable, and never invent a model identity or completion result.

- Route early on every non-trivial task and announce the route. The normal starting route is `gpt-5.6-luna` at Medium effort; use Low only for genuinely mechanical work and High/XHigh/Max when the task requires it. Luna Max is a valid route and should be used for unusually difficult but still cost-sensitive work.
- Treat primary/direct-chat routing as an actual execution requirement, not a label: the selected model and effort must be used for that work. If the primary task was started without the automatic configuration, stop and say: “Automatic agent spawning and work delegation is activated. Please start your work with Luna at Medium effort. If you really need to do the whole work with a different model, specify in the prompt that the optimized agentic configuration should be ignored.” Continue only after the primary task is restarted accordingly. Do not send this message from a delegated worker merely because its own route differs.
- If the user explicitly says to ignore the optimized agentic configuration, obey that instruction for the current task and do not reject the work or force delegation.
- Escalate only meaningful difficult portions by actually delegating a bounded subtask with the supported subagent tool. Use Sol only when Luna High/XHigh/Max is insufficient or when unclear root cause, failed prior fixes, architecture, cross-system state/concurrency/caching/performance/security, material ambiguity, or central design judgment warrants it. Sol should normally start at Medium, then High/XHigh/Max as justified. Do not use Terra by default; use it only when explicitly requested or when a measured, task-specific comparison shows it is the best fit. Return routine implementation to Luna when economical.
- For every delegation, retain the returned agent ID and wait for the actual completion payload. A wait timeout means the agent is still unresolved, not hung or failed: poll again with a bounded longer wait, and use the agent's returned result/notification as the source of truth before reporting or integrating. Never claim Sol produced no result merely because one wait call timed out; terminate only after an explicit error, shutdown, or a genuinely exhausted recovery path.
- Optimize tokens deliberately: inspect targeted files first, reuse existing generated indexes and tests, search with `rg`, avoid loading large unrelated files, keep delegated scopes narrow, use checkpoints instead of repeating discovery, and summarize only decisions/evidence needed for continuation. Increase reasoning effort before increasing context volume.
- Ask early about actual requirements only when a material ambiguity or subjective tradeoff cannot be resolved safely; do not ask which model to use when routing is clear.
- Be concise and transparent about significant routing changes when known (for example: “Route: Luna Medium” or “Escalating: Sol High”). Never invent model identity, effort, delegation, or routing. Do not expose private chain-of-thought.
- For substantial tasks, complete implementation and relevant validation; do not stop at a plan unless requested. Preserve project-specific instructions and normal approval boundaries.

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
