# ArchiMate Lite (data, ne jádro)

Metamodel pro popis systémů podmnožinou ArchiMate (L0–L4), matice povolených vazeb a Open Exchange.
**Není** součástí Go služby. Závisí na package **`kc-base`**.

UI traversal (IT Map navigace) je od **3.0.0** v samostatném package [`archimate-ui-traversal`](../archimate-ui-traversal/).
Volitelná auditní metadata migrace: [`architecture-migration`](../architecture-migration/).

| Soubor | Účel |
|--------|------|
| [catalog.json](catalog.json) | Seed slovníku (třídy, properties, tvary, matice, enumy, exchange) |
| [build_bundle.py](build_bundle.py) | Portable release bundle (resolvuje IRI z kc-base) |
| [releases/archimate-lite-3.2.0.bundle.json](releases/archimate-lite-3.2.0.bundle.json) | Aktuální bundle |
| [releases/archimate-lite-3.1.0.bundle.json](releases/archimate-lite-3.1.0.bundle.json) | Předchozí 3.1 (actorKind / organizationScope) |
| [RELEASE_NOTES-3.2.0.md](RELEASE_NOTES-3.2.0.md) | BusinessEvent / Collaboration / Object, processLevel, BIA source |
| [RELEASE_NOTES-3.1.0.md](RELEASE_NOTES-3.1.0.md) | Breaking migrace actorKind / organizationScope |
| [load.py](load.py) | Nahraje catalog + `kc-base` přes API |
| [docs/archimate-lite.md](../docs/archimate-lite.md) | Granularita L0–L4 |
| [docs/archimate-lite-kc.md](../docs/archimate-lite-kc.md) | Kontrakt pro nástroje nad API |

Public ID = `iriBase` + `iriLocal` (`https://knowledge-core.local/archimate-lite/…`).

## Import (nová instalace)

1. [`kc-base` 1.1.0](../kc-base/releases/kc-base-1.1.0.bundle.json)
2. Tento package `releases/archimate-lite-3.2.0.bundle.json`
3. [`archimate-ui-traversal` 1.0.0](../archimate-ui-traversal/releases/archimate-ui-traversal-1.0.0.bundle.json)
4. (volitelně) [`architecture-migration` 1.0.0](../architecture-migration/releases/architecture-migration-1.0.0.bundle.json)

**Neimportujte** 3.1.0+ přes existující 3.0.0 bez migrace statements (`compat_breaking` — viz release notes 3.1.0).  
**Neimportujte** 3.0.0+ přes existující 2.3.1 (`compat_breaking` — UI objekty v 3.x chybí).

```bash
python3 kc-base/build_bundle.py
python3 archimate-lite/build_bundle.py
python3 archimate-lite/load.py
```
