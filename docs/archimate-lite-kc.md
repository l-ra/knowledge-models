# ArchiMate Lite — package a API pro nástroje

> Obecný integrační návod: [integration/client-guide.md](../integration/client-guide.md).  
> Tento dokument je **doménově specifický kontrakt** pro nástroje nad ArchiMate Lite.

Tento dokument je kontrakt pro **samostatný nástroj** (export/import Open Exchange, validační CLI, editor), který pracuje **jen přes HTTP API knowledge-core**. Jádro KC neobsahuje ArchiMate typy; generické mezery P0–P2 jsou ve [fázi 19](../specs/phase-19-graph-api.md).

Rozsah modelování (L0–L4): [archimate-lite.md](archimate-lite.md).  
Foundation: [`kc-base/`](../kc-base/) (`instanceOf`, usage anotace, `StringEnum`).  
Datový katalog: [`archimate-lite/catalog.json`](../archimate-lite/catalog.json).  
Release bundles: [`kc-base-1.1.0`](../kc-base/releases/kc-base-1.1.0.bundle.json), [`archimate-lite-3.1.0`](../archimate-lite/releases/archimate-lite-3.1.0.bundle.json), [`archimate-ui-traversal-1.0.0`](../archimate-ui-traversal/releases/archimate-ui-traversal-1.0.0.bundle.json).  
Nahrání přes API: [`archimate-lite/load.py`](../archimate-lite/load.py) (načte i `kc-base`). Po nahrání/importu je **zdroj pravdy v KC**, ne JSON v gitu.

## Hranice

| Vrstva | Kde | ArchiMate? |
|--------|-----|------------|
| knowledge-core | `internal/`, migrace, `/v1/*` | Ne. Obecný graf (IRI entity/property/class, statement, package, shape, lens). |
| Package `kc-base` | data v KC | Ne. Globální typing, usage anotace, mechanismus string enumů. |
| Package `archimate-lite` | data v KC | Ano. Třídy, vlastnosti, tvary, anotace tříd, lite matice, enum *hodnoty*, exchange poznámky. Závisí na `kc-base`. UI traversal je v `archimate-ui-traversal`. |
| Package `archimate-ui-traversal` | data v KC | Ne ArchiMate. IT Map navigační profil, šablony, stage, přechody, add akce. Závisí na `kc-base` + `archimate-lite`. |
| Instance packages | data v KC | Ano. Konkrétní systémy, sdílené služby, views. |
| Exchange XML nástroj | mimo KC | Ano. Čte/zapisuje `/v1`, emituje ArchiMate XML. |

**Stabilní public ID** = plná IRI (`iriBase` + `iriLocal`), např. `https://knowledge-core.local/archimate-lite/ApplicationComponent`.  
Krátké zobrazení v UI: `archimate-lite:ApplicationComponent`. Fallback bez zadaného `iriLocal`: `e_<snowflake>` / `p_<snowflake>` / …

Default `iriBase`: `https://knowledge-core.local/archimate-lite/` (není well-known RDF namespace jádra).

## Autentizace

Všechny cesty pod `/v1` vyžadují identitu ([post-install](../ops/post-install.md)).

- Bootstrap: `Authorization: Bearer <heslo>` nebo `X-Admin-Password`
- Dev: `X-Subject` + `X-Roles: admin`
- OIDC: `Authorization: Bearer <access_token>`

Zápisy: `Content-Type: application/json`. Volitelně `X-Validation-Mode: relaxed` (default) / `strict` / `off`.  
Odpovědi create: `{ "data": { ... }, "changeSet": { ... } }`. GET entity/package obvykle **bez** obálky `data`.

## Bootstrap metamodelu

### Import release bundle (UI / promotion)

```bash
# 1) foundation
curl -X POST "$KC_BASE_URL/v1/releases/import" \
  -H "Authorization: Bearer $KC_TOKEN" \
  -H "Content-Type: application/json" \
  --data-binary @kc-base/releases/kc-base-1.1.0.bundle.json
# 2) ArchiMate Lite (manifest.dependencies → kc-base@1.1.0)
curl -X POST "$KC_BASE_URL/v1/releases/import" \
  -H "Authorization: Bearer $KC_TOKEN" \
  -H "Content-Type: application/json" \
  --data-binary @archimate-lite/releases/archimate-lite-3.1.0.bundle.json
```

UI: **Packages → Import release bundle** — nejdřív `kc-base`, pak `archimate-lite`.  
Po importu kc-base knowledge-core automaticky nastaví `instanceOfProperty` na  
`https://knowledge-core.local/kc-base/instanceOf`, pokud bylo prázdné.

Přegenerování: `python3 kc-base/build_bundle.py && python3 archimate-lite/build_bundle.py && python3 archimate-ui-traversal/build_bundle.py`.

### Load přes API (authoring)

```bash
export KC_BASE_URL=http://localhost:8080
export KC_TOKEN='<bootstrap-or-oidc>'
python3 archimate-lite/load.py   # nejdřív nahraje kc-base
```

Loader je idempotentní (`iriLocal` v package, `code` u shapes, `upsert` u policy statementů). Existující properties znovu zapíše constraints (`PATCH`, včetně `rangeClasses`). Tvary `aml-*` vytváří s `packageCode=archimate-lite`. Matice, enum *instance*, exchange a `layer`/`overlay`/`exchangeType` se uloží v `archimate-lite`; `StringEnum` / `usage*` / `instanceOf` žijí v `kc-base`.

Po nahrání:

1. `GET /v1/packages/kc-base` a `GET /v1/packages/archimate-lite`
2. `GET /v1/entities?package=archimate-lite&iriLocal=ApplicationComponent` — resoluce slovníku
3. `GET /v1/classes/{id}` / `GET /v1/properties/{id}` — id je plná IRI (v URL path-encode); obsahují `iriLocal`, `iri`, `packageCode`
4. `GET /v1/admin/schema-config` — `instanceOfProperty` musí být neprázdné. Loader `kc-base` ho nastaví, jen pokud bylo prázdné.
5. `GET /v1/shapes?package=archimate-lite` — `aml-element`, `aml-relationship`, `aml-view-connection`, `aml-allowed-relationship`, `aml-business-function`, `aml-business-actor`, `aml-association`, `aml-flow`, `aml-communication-network`, `aml-flow-network-detail`, UI tvary: `GET /v1/shapes?package=archimate-ui-traversal` — `aml-ui-navigation-profile`, `aml-ui-traversal-template`, `aml-ui-stage`, `aml-ui-transition`, `aml-ui-add-action`; `GET /v1/shapes?package=kc-base` — `string-enum`
6. Policy data viz [níže](#policy-data-v-kc) (`AllowedRelationship`, enum instance, `exchange-spec`, UI navigační profil)

`instanceOf` **není** ArchiMate predikát. Je v package `kc-base`. Nástroj ho vždy čte ze schema-config, nikdy ho nehardcoduje.

## Resoluce slovníku

Přímý lookup (preferovaný):

```text
GET /v1/entities?package=archimate-lite&iriLocal=relSource
GET /v1/entities?iri=https://knowledge-core.local/archimate-lite/ApplicationComponent
GET /v1/entities?package=archimate-lite&kind=class&limit=200
GET /v1/entities?package=archimate-lite&kind=property&limit=200
```

`iri` matchuje kanonické IRI (`iriBase` + `iriLocal`) nebo `entity_iri_alias`.  
Stránkování: `nextCursor` → `?cursor=`.

`GET /v1/entities/{id}` — `{id}` je plná IRI (path-encoded). Vrací `effectiveClasses` (instanceOf + předci).  
`GET /v1/classes/{id}` vrací `iriLocal`, `iri`, `packageCode`, `effectiveClasses` (self + předci).  
`GET /v1/properties/{id}` vrací `iriLocal`, `iri`, `packageCode`.

Tvary patří do package (a do release bundle, `objectType: "shape"`). Kódy v `archimate-lite`: `aml-element`, `aml-relationship`, `aml-view-connection`, `aml-allowed-relationship`, `aml-business-function`, `aml-business-actor`, `aml-association`, `aml-flow`, `aml-communication-network`, `aml-flow-network-detail`. V `kc-base`: `string-enum`. `document.requiredProperties` jsou IRI properties.

Podmínka `when` u `aml-flow-network-detail` (modelingDepth ≥ infrastructure/network) je v `catalog.json` jako nápověda pro nástroje; KC ji na shape dokumentu neukládá a shape se vztahuje na všechny instance `Flow` (warning bez `protocol`). `actorKind` a `organizationScope` u `BusinessActor` vynucuje class-specific shape `aml-business-actor`, ne rozšíření `aml-element`.

## Policy data v KC

KC matici a enumy **nevynucuje**. Tool si je načte z package a implementuje vlastní kontroly / XML mapování.

Public ID jsou stabilní IRI; pro lookup stačí `iriLocal` (ne hardcoduj cizí instalaci).

### Anotace tříd

Statementy na třídě prvku nebo vazby:

| `iriLocal` property | Význam |
|---------------------|--------|
| `archiLayer` | `business` / `application` / `technology` / … |
| `overlay` | např. `risk-and-security` u `Risk` |
| `exchangeType` | Open Exchange `xsi:type`; chybí u `DeployedOn` |
| `usageGuidance` | textový návod (property z `kc-base`) |
| `usageExamples` | konkrétní příklady (property z `kc-base`) |

```text
GET /v1/entities?package=archimate-lite&iriLocal=ApplicationComponent
GET /v1/entities/{classIri}/statements?property={archiLayerIri}
GET /v1/entities/{classOrPropertyIri}/statements?property={usageGuidanceIri}
```

`usageGuidance` / `usageExamples` jsou i na **property** entitách (nejen na třídách prvků a vazeb).

### Lite matice vazeb

Instance třídy `AllowedRelationship` (`iriLocal` tvaru `allowed/{type}/{source}/{target}`):

| property | hodnota |
|----------|---------|
| `allowedRelType` | IRI class podtřídy `ArchiMateRelationship` |
| `allowedSourceClass` | IRI class podtřídy `ArchiMateElement` |
| `allowedTargetClass` | IRI class podtřídy `ArchiMateElement` |

```text
GET /v1/entities?package=archimate-lite&instanceOf={AllowedRelationshipIri}
GET /v1/entities/{entityIri}/statements
```

### Enumy

Třída `StringEnum` a properties `enumeratesProperty` / `allowedValue` jsou v **`kc-base`**.  
Instance s hodnotami žijí v **`archimate-lite`** (`iriLocal` `enum/{name}`, obvykle shodné s property; výjimka `enum/flowDirection` pro property `direction`):

- `enumeratesProperty` → IRI property (typicky z `archimate-lite`)
- `allowedValue` — n× String

```text
GET /v1/entities?package=archimate-lite&iriLocal=enum/modelingDepth
GET /v1/entities?package=archimate-lite&iriLocal=enum/actorKind
GET /v1/entities?package=archimate-lite&iriLocal=enum/organizationScope
GET /v1/entities?package=archimate-lite&iriLocal=enum/flowDirection
GET /v1/entities?package=kc-base&iriLocal=StringEnum
```

Instance 2.1.0 (kromě již existujících `modelingDepth`, `dependencyStrength`, `accessMode`, `nodeKind`, `viewpoint`): `actorKind`, `ownership`, `associationKind`, `networkKind`, `networkRole`, `flowKind`, `flowDirection` (property `direction`), `dependencyType`.  
Od 3.1.0: `actorKind` = `person` | `organizationalUnit` | `organization`; nový enum `organizationScope` = `internal` | `external` (povinné na `BusinessActor`).  
Do 2.3.1 (v lite): `traverseDirection` (property `traverseDirection`), `relationshipDirection` (property `relationshipDirection`).

### Exchange poznámky

Jedna entita `iriLocal=exchange-spec` (`instanceOf` `ExchangeSpec`): `catalogVersion`, `exchangeFormat`, `exchangeElementXsiType`, `exchangeRelationshipXsiType`, `exchangeDeployedOn`, `exchangeRisk`, `exchangeViews`, `exchangeIdentifier`.

```text
GET /v1/entities?package=archimate-lite&iriLocal=exchange-spec
```

`catalog.json` / release bundle v gitu jsou seed. Runtime tool **nečte** JSON z disku, pokud má přístup k nahranému package.

### UI navigační profil (IT Map)

Od **archimate-ui-traversal 1.0.0** (dříve v archimate-lite 2.3.x). Detail: [archimate-ui-traversal.md](archimate-ui-traversal.md).

Klientská migrace IRI: [migrations/](../migrations/).

## Konvence instancí

| Package | Účel |
|---------|------|
| `archimate-lite` | Jen metamodel |
| např. `platform`, `network`, `locations` | Sdílené závislosti (IdP, DNS, DC, WAN) |
| jeden package na evidovaný systém | L0 `ApplicationComponent` = systém jako celek |
| volitelně landscape package | `DiagramView` napříč systémy |

Založení systémového package (závislost na metamodelu). JSON tagy jsou camelCase:

```http
POST /v1/packages
```

```json
{
  "code": "sys-crm",
  "lifecycle": "continuous",
  "iriBase": "https://example.org/systems/crm/",
  "labels": { "en": "CRM" },
  "dependencies": [
    { "dependsOnCode": "archimate-lite", "versionRange": "*" }
  ]
}
```

GET package vrací závislosti stejně (`dependsOnCode` / `versionRange`). Cross-package odkazy (Keycloak z `platform`) jsou v KC povolené.

`iriLocal` instance: stabilní slug (`crm`, `crm-backend`). Pro round-trip z Archi ulož původní identifier:

```http
PUT /v1/entities/{entityIri}/iri-aliases
```

```json
{ "aliases": [ { "iri": "https://archi.example/id-1234", "kind": "imported" } ] }
```

`kind`: `imported` | `sameAs` | `canonical_export`. IRI musí být absolutní `http(s)`.

Přesun do jiného package:

```http
POST /v1/entities/{entityIri}/move
{ "packageCode": "sys-crm" }
```

Přesune entitu a statementy subjektu, které byly ve stejném starém package. `409` při konfliktu `iriLocal` v cíli.

## Typing a statementy

Každý prvek, vazba i view uzel:

```http
POST /v1/entities
POST /v1/statements
```

```json
{
  "packageCode": "sys-crm",
  "labels": { "en": "CRM" },
  "iriLocal": "crm"
}
```

```json
{
  "packageCode": "sys-crm",
  "subject": "https://example.org/systems/crm/crm",
  "property": "https://knowledge-core.local/kc-base/instanceOf",
  "value": {
    "type": "EntityReference",
    "entityId": "https://knowledge-core.local/archimate-lite/ApplicationComponent"
  }
}
```

`property` = `instanceOfProperty` ze schema-config (typicky IRI `…/instanceOf`), `entityId` = IRI class `ApplicationComponent`.

Opakovaný zápis stejné trojice (subject + property + value) s `"upsert": true` vrátí existující statement (`200`), bez duplicity.

Hodnoty statementů:

| datatype | JSON value |
|----------|------------|
| EntityReference | `{ "type": "EntityReference", "entityId": "<IRI>" }` |
| String | `{ "type": "String", "string": "…" }` |
| Integer | `{ "type": "Integer", "int64": 5432 }` |
| Boolean | `{ "type": "Boolean", "bool": true }` |
| URI | `{ "type": "URI", "uri": "https://…" }` |
### Čtení grafu

| Účel | Endpoint |
|------|----------|
| Odchozí tvrzení | `GET /v1/entities/{iri}/statements?property={propertyIri}` |
| Příchozí tvrzení (kdo ukazuje na X) | `GET /v1/entities/{iri}/incoming?property={propertyIri}` |
| Okolí (outgoing + incoming + neighbors) | `GET /v1/entities/{iri}/graph?depth=1` (`depth` 1 nebo 2) |
| Instance třídy | `GET /v1/entities?instanceOf={classIri}&includeSubclasses=true` |

Dopadová analýza: `GET .../incoming` s property `relSource` nebo `relTarget` (IRI z resoluce slovníku). RDF dump (`GET /v1/projections/rdf`) zůstává volitelný.

## Vzory objektů

### Prvek

Entita + `instanceOf` → listová třída (`ApplicationComponent`, `Node`, …).  
Atributy = další statementy (`modelingDepth`, `criticality`, …).  
Popis = `descriptions` na entitě, ne statement.

`modelingDepth`: `catalog` | `dr_minimum` | `application_detail` | `infrastructure_detail` | `network_detail` (L0–L4). Je to vlastnost **prvku**, ne package.

### Vazba (first-class entita)

Entita + `instanceOf` → `Composition` / `Flow` / …  
Povinné: `relSource`, `relTarget` (EntityReference na prvky).  
Identita vazby = IRI entity (v XML `relationship/@identifier` typicky z `iriLocal` nebo aliasu).

```text
…/crm  instanceOf ApplicationComponent
…/fe   instanceOf ApplicationComponent
…/c1   instanceOf Composition
…/c1   relSource → …/crm
…/c1   relTarget → …/fe
```

`rangeClasses` na `relSource`/`relTarget` **nastavte** na `ArchiMateElement` (loader/bundle to dělá z catalog `range`). Validace range v KC bere `instanceOf` cíle a expanduje `subClassOf`. Lite matici vynucuje tool nad instancemi `AllowedRelationship` v KC.

`PATCH /v1/properties/{propertyIri}` `{ "constraints": { ... } }` upraví constraints po vytvoření.

`DeployedOn` je lite vztah; XML nástroj ho expanduje na `Assignment`.  
`Risk` je overlay; XML: overlay typ nebo `Assessment` + property.

### View

Architektura není ve view. View jen vybírá a kreslí.

- `DiagramView` — `viewpoint` volitelně
- `ViewNode` — `nodeKind` (`element`|`container`|`label`), `elementRef` (range `ArchiMateElement`), `boundsX/Y/W/H`, `parentNode` (range `ViewNode`), `style` (JSON string)
- `ViewConnection` — `relationshipRef` (range `ArchiMateRelationship`), `sourceNode`/`targetNode` (range `ViewNode`), `bendpoints` (JSON string)

## Endpointy, které nástroj potřebuje

| Metoda | Cesta | Účel |
|--------|-------|------|
| GET | `/healthz` | liveness |
| GET/POST | `/v1/packages`, `/v1/packages/{code}` | packages (`dependsOnCode` / `versionRange`) |
| PATCH | `/v1/packages/{code}` | `iriBase`, labels |
| GET | `/v1/entities` | `?package=&kind=&iriLocal=&iri=&instanceOf=&includeSubclasses=&q=&cursor=&limit=` |
| POST | `/v1/entities` | prvek / vazba / view |
| GET/PATCH | `/v1/entities/{id}` | id = IRI (path-encoded); GET: `effectiveClasses` |
| POST | `/v1/entities/{id}/deprecate` | status → `deprecated` |
| POST | `/v1/entities/{id}/delete` | logické smazání (`deleted`); 409 při příchozích refs |
| POST | `/v1/entities/{id}/move` | `{ packageCode }` |
| PUT | `/v1/entities/{id}/iri-aliases` | Archi identifier |
| GET | `/v1/entities/{id}/statements` | odchozí; `?property=` |
| GET | `/v1/entities/{id}/incoming` | příchozí; `?property=` |
| GET | `/v1/entities/{id}/graph` | `?depth=1\|2` |
| POST | `/v1/statements` | atributy, instanceOf, relSource…; `"upsert": true` |
| GET | `/v1/statements/{id}` | |
| POST | `/v1/statements/{id}/revise` | změna hodnoty |
| POST | `/v1/statements/{id}/deprecate` | status → `deprecated` |
| GET/POST | `/v1/classes`, `/v1/properties`, `/v1/shapes` | metamodel |
| GET | `/v1/classes/{id}`, `/v1/properties/{id}` | `iriLocal`, `iri` |
| PATCH | `/v1/properties/{id}` | `constraints` |
| GET | `/v1/shapes?package=` | tvary package |
| GET/PUT | `/v1/admin/schema-config` | `instanceOfProperty` |
| GET | `/v1/entities/{id}/validation` | shapes / domain / range |
| POST | `/v1/validation/reports` | dávka |
| GET | `/v1/projections/rdf` | dump pro analýzu mimo KC |
| POST | `/v1/packages/{code}/releases` | snapshot metamodelu (včetně shapes) |
| GET | `/v1/packages/{code}/releases/{version}/bundle` | přenositelný bundle |
| POST | `/v1/releases/import` | promotion bundle |

OpenAPI: [`api/openapi.yaml`](../../api/openapi.yaml) (0.2.2).

Lenses (`POST /v1/lenses`, `GET/PATCH .../instances/{key}`) jsou volitelné; nástroj může jít přímo na entity/statementy.

## Open Exchange — povinnosti nástroje (ne jádra)

- prvek → `<element identifier xsi:type="{iriLocal}">`
- vazba → `<relationship identifier xsi:type="{iriLocal}" source= target=>` (`relSource` / `relTarget`)
- literály properties → `<properties>`
- `DeployedOn` → `Assignment` řetězec
- `Risk` → overlay nebo Assessment
- View* → `<views><diagrams><view>`
- `<organizations>` z packages
- RDF projekce KC **není** ArchiMate XML

## Validace

KC `relaxed`: zápis projde, findings v odpovědi / `GET .../validation`.  
Shape `aml-relationship` vyžaduje `relSource`+`relTarget` (error).  
Shape `aml-element` varuje bez `modelingDepth`.  
Shape `aml-business-actor` vyžaduje `actorKind` a `organizationScope` (error).  
Shape `aml-flow` vyžaduje `flowLabel` (error).  
Shape `aml-association` varuje bez `associationKind`.  
Shape `aml-communication-network` varuje bez `networkKind`.  
Range `ArchiMateElement` na koncích vazby = jádro.  
Lite matice a „Flow jen mezi komponentami“ = logika nástroje nad instancemi `AllowedRelationship` (seed v catalog `allowedRelationships`). Enumy = instance `StringEnum`.

Demo instance (Compliance + síť) proti 2.1.0: [`archimate-lite-demo/`](../archimate-lite-demo/) (`python3 archimate-lite-demo/load.py`).

## Co nástroj nesmí dělat

- Přidávat ArchiMate typy do Go jádra, migrací nebo well-known RDF vocab
- Hardcodovat IRI z jiné instalace s jiným `iriBase`
- Modelovat L5 (pody, všechny IP, firewall rules) jako ArchiMate prvky
