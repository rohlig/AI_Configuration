# Unresolved Issues

| Issue | Impact | Owner/next action | Status |
|---|---|---|---|
| Existing machine-level Codex settings are only partially represented | The versioned `config.toml` does not include MCP runtime wiring, plugin state, project trust paths, or desktop state | Promote each category only after deciding whether it is portable and safe | Open |
| Portable scope of desktop preferences, plugins, and skills is not established | Some app state may still need separate setup | Research each requested category before adding a sync target | Open |
| Repository remote/clone URL is unknown | README clone command is a placeholder | Replace after the remote is configured | Open |
| Long-context pricing behavior is model-specific | The 272k boundary is confirmed for GPT-5.6 Sol, not universally for every model or desktop route | Re-check the selected model’s official pricing page before changing the 240k policy buffer | Open |
