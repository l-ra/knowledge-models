# Architecture migration (optional)

Volitelný package s **auditními properties** pro dokumentaci transformace
architektury (např. legacy ArchiMate → cílový `archimate-lite` ORGX model).

**Není** ArchiMate sémantika. Po dokončení migrace package není potřeba —
`archimate-lite` na něm nezávisí.

| Soubor | Účel |
|--------|------|
| [catalog.json](catalog.json) | Migrační properties + enumy |
| [build_bundle.py](build_bundle.py) | Portable release bundle |
| [releases/architecture-migration-1.0.0.bundle.json](releases/architecture-migration-1.0.0.bundle.json) | Aktuální bundle |
| [load.py](load.py) | Nahraje catalog + závislosti přes API |

Public ID = `iriBase` + `iriLocal` (`https://knowledge-core.local/architecture-migration/…`).

## Závislosti

1. [`kc-base` 1.1.0](../kc-base/releases/kc-base-1.1.0.bundle.json)
2. [`archimate-lite` 3.2.0](../archimate-lite/releases/archimate-lite-3.2.0.bundle.json)
3. Tento package `releases/architecture-migration-1.0.0.bundle.json`

## Properties

Doména všech properties: `ArchiMateConcept` (elementy, vztahy, views).

| Property | Poznámka |
|----------|----------|
| `migrationStatus` | unchanged / transformed / split / merged / created / deprecated / needsReview / rejected |
| `migrationAction` | doporučený slovník (TYPE_CHANGED, …) |
| `migrationRule` | id pravidla |
| `migrationSourceId` | primární zdroj (1×) |
| `migrationSourceIds` | všechny zdroje (multi-value) |
| `migrationSourceType` | typ ve zdroji |
| `migrationSourceName` | název ve zdroji |
| `migrationConfidence` | high / medium / low / manual |
| `migrationBatch` | dávka / běh |
| `migrationTimestamp` | ISO-8601 |
| `migrationNotes` | volný text |

```bash
python3 architecture-migration/build_bundle.py
python3 architecture-migration/load.py
```
