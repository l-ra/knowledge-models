# archimate-lite 3.2.0 — release notes

**Zpětně kompatibilní** minor rozšíření vůči 3.1.0 (pouze aditivní třídy, properties a `AllowedRelationship` řádky).

## Co se změnilo

### Nové elementy (business)

- `BusinessEvent` — business událost (Triggering ↔ `BusinessProcess`, volitelně → `BusinessFunction`)
- `BusinessCollaboration` — společné působení aktérů (ne externí organizace)
- `BusinessObject` — business význam informace (≠ `DataObject`)

### Nové properties

- `processLevel` na `BusinessProcess` (`L0`–`L4`) — ortogonální k `modelingDepth`
- `criticalitySource` / `rtoSource` / `rpoSource` na `ArchiMateElement` (`declared` | `inherited` | `calculated`)

### Nové povolené vztahy

- `Composition` `BusinessProcess` → `BusinessProcess`
- `Triggering` `BusinessEvent` → `BusinessProcess` / `BusinessFunction`
- `Triggering` `BusinessProcess` → `BusinessEvent`
- `Composition` `BusinessCollaboration` → `BusinessActor`
- `Assignment` `BusinessCollaboration` → `BusinessProcess` / `BusinessFunction`
- `Realization` `BusinessCollaboration` → `BusinessService`
- `Access` `BusinessProcess` / `BusinessFunction` / `BusinessService` → `BusinessObject`

## Migrační metadata

Auditní properties **nejsou** v tomto package. Volitelný addon:

[`architecture-migration` 1.0.0](../architecture-migration/) — po dokončení migrace není potřeba.

## Import

1. `kc-base` 1.1.0  
2. `archimate-lite` 3.2.0  
3. (volitelně) `architecture-migration` 1.0.0  
4. `archimate-ui-traversal` 1.0.0 (beze změny vůči 3.1.0 taxonomii)

Modely proti 3.1.0 zůstávají načitatelné (aditivní změna).
