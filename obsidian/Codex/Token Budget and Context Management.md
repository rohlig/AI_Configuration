# Token Budget and Context Management

## Goal

Keep long-running AI coding work below the long-context pricing boundary whenever the task can be completed without carrying all historical context forward.

## Known boundary

The official GPT-5.6 Sol model page states that prompts over **272k input tokens** are priced at 2× input and 1.5× output for the full request. The same page lists a 1.05M context window, so crossing the boundary is usually a cost event rather than an immediate context-capacity failure. The exact pricing behavior must be checked for the selected model; do not assume that every model has the same rule.

## Repository policy

The portable config sets `model_auto_compact_token_limit = 240000` as an early-warning buffer and limits retained tool output with `tool_output_token_limit = 12000`. These settings reduce risk but cannot guarantee a precise request size because system instructions, tool wrappers, files, and reasoning overhead vary.

Use these operating bands:

| Input-context estimate | Action |
|---:|---|
| `< 200k` | Continue normally; keep reads targeted. |
| `200k–240k` | Stop broad exploration; checkpoint decisions and avoid repeating prior context. |
| `240k–260k` | Compact at a milestone or start a fresh continuation from a concise checkpoint. |
| `260k–272k` | Treat as a hard warning; reduce context or split independent work before the next large request. |
| `> 272k` | Avoid unless explicitly justified, model pricing is verified, and the user accepts the cost. |

## When to compact

Compact after a meaningful milestone: discovery, architecture decision, implementation batch, or validation phase. A compact checkpoint should retain:

- objective and acceptance criteria;
- decisions and assumptions;
- changed files and unresolved issues;
- validation evidence and next action;
- only the source excerpts needed for the next step.

For delegated workers, the checkpoint is also a durability boundary: send it to the parent after each meaningful milestone and before compaction, timeout, handoff, or credit exhaustion. The parent records it in the project audit or checkpoint before starting another phase. Read-only workers should report rather than edit; documentation writes require explicit scope.

Do not compact every turn. Repeated compaction can add overhead and can discard useful detail. The API supports an explicit input-token count endpoint and a Responses compaction endpoint; use those in API-backed applications when available.

## When to split across agents

Split only when the work has independent information or file boundaries, for example:

- one agent reviews security while another reviews tests;
- separate services can be inspected independently;
- research and implementation can proceed without sharing a long transcript.

Keep one primary integrator. Pass specialists a short brief, relevant paths, constraints, and an expected output format. Ask for concise evidence, not a copied transcript. Do not split a tightly coupled debugging or design decision merely to reduce context; duplicate input can cost more than it saves.

## API-aware pattern

For an API-backed workflow:

1. Count the exact input with the model’s token-count endpoint before a large request.
2. If it is near the safety band, remove redundant history, replace verbose tool output with a checkpoint, or compact the conversation.
3. Keep the same task instructions when resuming after compaction to reduce behavior drift.
4. Re-count after adding files, tool results, or agent handoffs.
5. Use prompt caching for repeated stable prefixes where supported, but do not treat caching as permission to cross a long-context pricing boundary.

For Codex desktop/CLI work, use the context indicator and the same policy manually; the repository cannot inspect every internal request before the client sends it.

## Why not always use many agents?

Every agent receives instructions and task context, and every result must be integrated. More agents can therefore increase total input, coordination, and review cost. Delegation is a tool for parallel independent work, not a default response to a large context.
