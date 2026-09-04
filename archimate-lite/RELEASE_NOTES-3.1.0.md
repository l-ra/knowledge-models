# archimate-lite 3.1.0 — release notes

**compat_breaking** vůči 3.0.0 (změna enum hodnot `actorKind` + nová povinná property `organizationScope`).

## Co se změnilo

- `actorKind`: `department` | `person` | `external` → `person` | `organizationalUnit` | `organization`
- Nová property `organizationScope` (`internal` | `external`), domain `BusinessActor`, required ve shape `aml-business-actor`
- `ownership` beze změny (provoz/vlastnictví ApplicationComponent / TechnologyService / CommunicationNetwork — ne klasifikace actora)

## Migrace instancí

| Staré `actorKind` | Nové `actorKind` | Nové `organizationScope` | Poznámka |
|-------------------|------------------|--------------------------|----------|
| `department` | `organizationalUnit` | `internal` | default; známý externí útvar → scope=`external` ručně |
| `person` | `person` | `internal` | default; konzultanti → `external` ručně |
| `external` | `organization` | `external` | typický význam starého „external“; pokud šlo o osobu → `person` + `external` ručně |

Existující org package: ChangeSet migrace statements `actorKind` + doplnění `organizationScope`.

## Import (čerstvá instalace)

1. `kc-base` 1.1.0  
2. `archimate-lite` 3.1.0  
3. `archimate-ui-traversal` 1.0.0 **s upraveným seedem** (nasadit současně — seed filtruje `organizationalUnit` / `person`, ne `department` / `external`)  
4. `archimate-lite-demo` (závislost `^3.1.0`)

Neimportujte 3.1.0 přes existující 3.0.0 bez migrace statements.

## UI traversal

Package verze zůstává **1.0.0**; `ui-profile-seed.json` (+ catalog usage texty) jsou upraveny pro 3.1.0 taxonomii. Seed musí být nasazen současně s AML 3.1.0.
