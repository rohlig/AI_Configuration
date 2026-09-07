# Architecture

## Scope

This repository is a portable source-of-truth layer for reusable AI development instructions and documentation. It is not a backup of an entire application profile, chat history, credentials, plugin cache, or OS installation.

## Flow

```text
Git repository/config/global/
        |
        | explicit check or interactive install
        v
Codex home (~/.codex or $CODEX_HOME)
        |
        v
Codex loads global instructions/config + project-specific layers
```

## Managed mapping

| Source | Target | Policy |
|---|---|---|
| `config/global/AGENTS.md` | `$CODEX_HOME/AGENTS.md` | Managed; interactive install; existing file is backed up before replacement |
| `config/global/config.toml` | `$CODEX_HOME/config.toml` | Managed; contains the reviewed portable baseline and agent registrations |
| `config/global/agents/*.toml` | `$CODEX_HOME/agents/ai-configuration/*.toml` | Managed custom agent definitions in a collision-resistant namespace |

Codex project-local `.codex/config.toml` and project `AGENTS.md` files remain in their own repositories. More-specific project instructions are not copied into this global repository.

## Constraints

- The installer must not silently mutate machine-level state.
- Secrets and machine-specific paths are excluded from version control.
- Codex configuration behavior can change; dated research notes are evidence, not timeless guarantees.
- Existing files are recoverable through timestamped backups created by the installer.
- Installing `config.toml` merges only managed keys and agent registrations; unrelated user settings remain in place.

## Dependencies

- POSIX shell tools: `bash`, `cmp`, `cp`, `date`, `mkdir`.
- Git for versioning.
- Obsidian is optional; the notes are plain Markdown with standard wiki links.
