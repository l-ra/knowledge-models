# KC Base (data, ne jádro)

Znovupoužitelný foundation package pro metamodely. **Není** součástí Go služby.

| Soubor | Účel |
|--------|------|
| [catalog.json](catalog.json) | Seed: `instanceOf`, `Package` / `packageCode`, usage anotace, `StringEnum` + shapes |
| [build_bundle.py](build_bundle.py) | Portable release bundle |
| [releases/kc-base-1.1.0.bundle.json](releases/kc-base-1.1.0.bundle.json) | Bundle pro UI import (aktuální) |
| [load.py](load.py) | Nahraje catalog přes API |

## Obsah

- **`instanceOf`** — globální typing property (`https://knowledge-core.local/kc-base/instanceOf`). Knowledge-core ji po ingestu automaticky nastaví do `schema-config.instanceOfProperty`, pokud je prázdné.
- **`Package`** + **`packageCode`** + shape `package-root`
- **`usageGuidance` / `usageExamples`**
- **`StringEnum`** + `enumeratesProperty` / `allowedValue` + shape `string-enum`

## Import

```bash
python3 kc-base/build_bundle.py
export KC_BASE_URL=http://localhost:8080
export KC_TOKEN='…'
python3 kc-base/load.py
```
