# archimate-lite 3.2.1 — release notes

**Zpětně kompatibilní** patch vůči 3.2.0 (pouze aditivní třídy a properties pro Open Exchange round-trip).

## Co se změnilo

### Open Exchange passthrough

- `ExchangeForeignElement` / `ExchangeForeignRelationship` — typy mimo Lite slovník (např. `AndJunction`)
- `exchangeXsiType` — původní Exchange `xsi:type`
- `exchangeOpaqueProperties` — JSON bag nemapovaných properties/atributů
- `exchangeOpaqueFragment` — nestrukturované fragmenty (neznámé view konstrukty)
- `exchangeManaged` — označení instancí z Open Exchange importu (orphan review)

### Views

- `inView` — ViewNode / ViewConnection → DiagramView (membership pro reexport diagramů)

### Bez Junctions

`AndJunction` / `OrJunction` **nejsou** nativní Lite třídy; importují se jako `ExchangeForeignElement`.

## Import

1. `kc-base` 1.1.0  
2. `archimate-lite` **3.2.1**  
3. `archimate-ui-traversal` 1.0.0  

Nástroj Open Exchange I/O: IT Map → Packages (viz dokumentace v knowledge-itmap).
