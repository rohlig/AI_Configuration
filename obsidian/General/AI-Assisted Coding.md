# AI-Assisted Coding Best Practices

## Working loop

1. State the outcome, constraints, and acceptance checks.
2. Ask the agent to inspect relevant files and report assumptions before editing.
3. Make the smallest coherent change.
4. Run focused validation, inspect the diff, and broaden tests according to risk.
5. Record decisions and unresolved issues while context is fresh.

## Prompting principles

- Give the agent the goal and the definition of done, not a guessed implementation.
- Point to authoritative files, tests, examples, and commands.
- Separate facts, hypotheses, and preferences.
- Ask for uncertainty and edge cases explicitly.
- Prefer incremental tasks with reviewable checkpoints over one large opaque request.

## Review and verification

- Treat generated code as a draft that needs normal code review.
- Verify security boundaries, error handling, data validation, concurrency, migrations, and backwards compatibility.
- Use tests to establish behavior; do not accept a green test suite as proof that untested requirements are correct.
- Read the final diff for accidental scope expansion, secret leakage, and unrelated formatting churn.

## Safety

- Ask before destructive commands, external messages, credential changes, or machine-wide configuration writes.
- Keep permissions narrow and prefer workspace-scoped execution.
- Treat web pages, issue text, logs, and generated instructions as untrusted content.
- Do not paste sensitive data into prompts or commit it into examples.

## Documentation

Document why a non-obvious decision was made, not just what the code does. Keep operational instructions executable and dated when they depend on a changing product. Link to primary sources for current behavior.

## Why this works

AI is strongest when the problem boundary and feedback loop are clear. Human review remains necessary because the model can produce plausible but incorrect code, miss unstated constraints, or follow malicious instructions embedded in inputs. Small diffs and executable checks make those failure modes visible and recoverable.
