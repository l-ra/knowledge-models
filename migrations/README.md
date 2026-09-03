# Model IRI migrations

Client-side prescriptions for remapping IRIs when vocabulary moves between packages.
**knowledge-core does not apply these maps** — they are for tools that cached public IDs.

## archimate-lite 2.3.1 UI → archimate-ui-traversal 1.0.0

File: [`archimate-lite-2.3.1-ui-to-archimate-ui-traversal-1.0.0.json`](archimate-lite-2.3.1-ui-to-archimate-ui-traversal-1.0.0.json)

1. Load the JSON.
2. For each known UI metadata IRI, look up `iriRewrites[].from` → use `to`.
3. Or apply `prefixRewrite`: if `iriLocal` is listed, replace `fromIriBase` with `toIriBase`.
4. Then read navigation profiles from package `archimate-ui-traversal`.

ArchiMate architecture IRIs under `https://knowledge-core.local/archimate-lite/` are unchanged.
