# knowledge-models

Shared git repository for **data packages** used with [knowledge-core](https://github.com/l-ra/knowledge-core).
These are not part of the Go service. After import/load, **KC is the source of truth**.

## Packages

| Package | Version | Role |
|---------|---------|------|
| [`kc-base`](kc-base/) | 1.1.0 | Foundation: `instanceOf`, `Package`, usage annotations, `StringEnum` |
| [`archimate-lite`](archimate-lite/) | 3.2.1 | ArchiMate subset (L0–L4), allowed matrix, Open Exchange notes / foreign opaque |
| [`architecture-migration`](architecture-migration/) | 1.0.0 | Optional migration audit properties (drop after migration) |
| [`archimate-ui-traversal`](archimate-ui-traversal/) | 1.0.0 | IT Map navigation profiles / column-browser traversal |
| [`archimate-lite-demo`](archimate-lite-demo/) | 1.0.0 | Demo instances (depends on archimate-lite ^3.1.0) |

Dependency chain: `kc-base` ← `archimate-lite` ← `archimate-ui-traversal` / `archimate-lite-demo` / (optional) `architecture-migration`.

## Import order (new installs)

1. `kc-base/releases/kc-base-1.1.0.bundle.json`
2. `archimate-lite/releases/archimate-lite-3.2.1.bundle.json`
3. `archimate-ui-traversal/releases/archimate-ui-traversal-1.0.0.bundle.json`
4. (optional) `architecture-migration/releases/architecture-migration-1.0.0.bundle.json`

Do **not** import `archimate-lite@3.1.0` over an existing `3.0.0` without statement migration (`compat_breaking` — actorKind / organizationScope). See [`archimate-lite/RELEASE_NOTES-3.1.0.md`](archimate-lite/RELEASE_NOTES-3.1.0.md).  
Do **not** import `archimate-lite@3.0.0+` over an existing `2.3.1` release (`compat_breaking`). See [`migrations/`](migrations/).  
`archimate-lite@3.2.0` is additive over 3.1.0 — see [`archimate-lite/RELEASE_NOTES-3.2.0.md`](archimate-lite/RELEASE_NOTES-3.2.0.md).  
`archimate-lite@3.2.1` is additive over 3.2.0 (Open Exchange `inView` + opaque/foreign) — see [`archimate-lite/RELEASE_NOTES-3.2.1.md`](archimate-lite/RELEASE_NOTES-3.2.1.md).

## Build / load

```bash
python3 kc-base/build_bundle.py
python3 archimate-lite/build_bundle.py
python3 architecture-migration/build_bundle.py
python3 archimate-ui-traversal/build_bundle.py

export KC_BASE_URL=http://localhost:8080
export KC_TOKEN='…'
python3 archimate-lite/load.py              # pulls kc-base
python3 architecture-migration/load.py     # optional; pulls deps
python3 archimate-ui-traversal/load.py      # pulls deps
```

### Import release bundles (promotion)

Nahrání vyjmenovaných `*.bundle.json` přes `POST /v1/releases/import` (pořadí na CLI = pořadí importu).
Pro lokální `scripts/dev.sh` (bootstrap) stačí běžící KC — heslo se vezme z `KC_TOKEN` / `KC_ADMIN_PASSWORD` / `KC_BOOTSTRAP_PASSWORD_FILE`, jinak ze sibling `../knowledge-core/.tmp/admin.password`.

```bash
python3 import_bundles.py \
  kc-base/releases/kc-base-1.1.0.bundle.json \
  archimate-lite/releases/archimate-lite-3.2.1.bundle.json \
  archimate-ui-traversal/releases/archimate-ui-traversal-1.0.0.bundle.json
```

## Docs

- [`docs/archimate-lite.md`](docs/archimate-lite.md) — modeling granularity L0–L4
- [`docs/archimate-lite-kc.md`](docs/archimate-lite-kc.md) — tool contract over KC API
- [`docs/archimate-ui-traversal.md`](docs/archimate-ui-traversal.md) — UI traversal package
- [`docs/rozsireni-archimat-lite.md`](docs/rozsireni-archimat-lite.md) — ORGX extension brief (3.2.0)
- [`migrations/README.md`](migrations/README.md) — client IRI remaps

## Layout with knowledge-core

Expected sibling checkout:

```text
src/knowledge-core/
src/knowledge-models/   # this repo
```

KC tests resolve models via `KNOWLEDGE_MODELS_PATH` or `../knowledge-models`.
