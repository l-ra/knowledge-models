# ArchiMate UI Traversal (data, ne jádro)

IT Map column-browser navigace: profily, šablony, stage, přechody a add akce.
**Není** součástí Go služby. Závisí na **`kc-base`** a **`archimate-lite`** ^3.0.0.

| Soubor | Účel |
|--------|------|
| [catalog.json](catalog.json) | Seed: Ui* třídy, properties, tvary, enumy |
| [ui-profile-seed.json](ui-profile-seed.json) | Výchozí IT Map profil (3 šablony) |
| [generate_ui_profile_seed.py](generate_ui_profile_seed.py) | Generátor seedu |
| [build_bundle.py](build_bundle.py) | Portable release bundle |
| [releases/archimate-ui-traversal-1.0.0.bundle.json](releases/archimate-ui-traversal-1.0.0.bundle.json) | Bundle pro UI import |
| [load.py](load.py) | Nahraje catalog (+ závislosti) přes API |

`iriBase`: `https://knowledge-core.local/archimate-ui-traversal/`

## Import

1. `kc-base` 1.1.0
2. `archimate-lite` 3.0.0
3. Tento package 1.0.0

Klientská migrace ze starých IRI pod `archimate-lite` (2.3.1): viz [`../migrations/`](../migrations/).

```bash
python3 archimate-ui-traversal/build_bundle.py
python3 archimate-ui-traversal/load.py
```
