# Unresolved Issues

| Issue | Impact | Owner/next action | Status |
|---|---|---|---|
| Existing machine-level Codex settings are only partially represented | The versioned `config.toml` does not include MCP runtime wiring, plugin state, project trust paths, or desktop state | Promote each category only after deciding whether it is portable and safe | Open |
| Portable scope of desktop preferences, plugins, and skills is not established | Some app state may still need separate setup | Research each requested category before adding a sync target | Open |
| Repository remote/clone URL is unknown | README clone command is a placeholder | Replace after the remote is configured | Open |
| Long-context pricing behavior may differ by model and client | The 272k boundary is documented for GPT-6 Luna, Sol, and Astra API requests; Codex desktop billing and future model changes still need verification | Check the selected model and product's official pricing page before changing the 240k policy buffer | Open |
