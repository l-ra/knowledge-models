# ArchiMate UI Traversal — package kontrakt

Navigační metadata pro IT Map column-browser. **Není** ArchiMate vocabulary.

- Seed: [`archimate-ui-traversal/catalog.json`](../archimate-ui-traversal/catalog.json)
- Instances: [`ui-profile-seed.json`](../archimate-ui-traversal/ui-profile-seed.json)
- Bundle: [`archimate-ui-traversal-1.0.0`](../archimate-ui-traversal/releases/archimate-ui-traversal-1.0.0.bundle.json)
- IRI base: `https://knowledge-core.local/archimate-ui-traversal/`
- Závislosti: `kc-base@1.1.0`, `archimate-lite@3.1.0`

## Třídy

| `iriLocal` | Účel |
|------------|------|
| `UiTraversalMeta` | Kořen (ne ArchiMate) |
| `UiNavigationProfile` | Profil navigace |
| `UiTraversalTemplate` | Šablona sloupců |
| `UiStage` | Jeden sloupec |
| `UiTransition` | Hrana mezi stage |
| `UiAddAction` | Položka create menu |

## Výchozí seed

`iriLocal=ui-profile-itmap-default` (`profileCode=itmap-default`, `isSystemDefault=true`) se třemi šablonami: `business-exploration`, `application-impact`, `infrastructure`.

Org package-root (`kc-base:Package`) může odkazovat na aktivní profil přes `orgNavigationProfile` (domain `Package`, definováno v tomto package).

```text
GET /v1/entities?package=archimate-ui-traversal&iriLocal=ui-profile-itmap-default
GET /v1/entities?package=archimate-ui-traversal&instanceOf={UiTraversalTemplateIri}
GET /v1/entities/{orgPackageRootIri}/statements?property={orgNavigationProfileIri}
```

## Migrace z archimate-lite 2.3.1

Do 2.3.1 žila UI metadata v `archimate-lite`. Klientská mapa IRI: [`migrations/`](../migrations/).
