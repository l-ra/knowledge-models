# ArchiMate UI Cards (data, ne jádro)

IT Map režim **Karty**: prezentační profily elementů a relation slots.
IT Map **Cards** mode: element presentation profiles and relationship slots.
**Není** součástí Go služby. Závisí na **`kc-base`** a **`archimate-lite`** ^3.1.0.

Odděleno od [`archimate-ui-traversal`](../archimate-ui-traversal/) (column browser).

| Soubor | Účel |
|--------|------|
| [catalog.json](catalog.json) | Třídy PresentationProfile / RelationSlot + properties |
| [ui-cards-seed.json](ui-cards-seed.json) | Systémové profily: Oddělení, Osoba, Externí organizace, Aplikace |
| [build_bundle.py](build_bundle.py) | Portable release bundle |
| [releases/archimate-ui-cards-1.0.0.bundle.json](releases/archimate-ui-cards-1.0.0.bundle.json) | Bundle pro import |
| [load.py](load.py) | Nahraje catalog (+ závislosti) přes API |

`iriBase`: `https://knowledge-core.local/archimate-ui-cards/`

## Import

1. `kc-base` 1.1.0
2. `archimate-lite` 3.1.0
3. Tento package 1.0.0

```bash
python3 archimate-ui-cards/build_bundle.py
python3 archimate-ui-cards/load.py
```
