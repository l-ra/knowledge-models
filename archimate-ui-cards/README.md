# ArchiMate UI Cards (data, ne jádro)

IT Map režim **Karty**: prezentační profily elementů a relation slots.
IT Map **Cards** mode: element presentation profiles and relationship slots.
**Není** součástí Go služby. Závisí na **`kc-base`** a **`archimate-lite`** ^3.2.0.

Odděleno od [`archimate-ui-traversal`](../archimate-ui-traversal/) (column browser).

| Soubor | Účel |
|--------|------|
| [catalog.json](catalog.json) | Třídy PresentationProfile / RelationSlot + properties |
| [ui-cards-seed.json](ui-cards-seed.json) | Systémové profily a relation slots |
| [build_bundle.py](build_bundle.py) | Portable release bundle |
| [releases/archimate-ui-cards-1.1.1.bundle.json](releases/archimate-ui-cards-1.1.1.bundle.json) | Bundle pro import |
| [load.py](load.py) | Nahraje catalog (+ závislosti) přes API |

`iriBase`: `https://knowledge-core.local/archimate-ui-cards/`

## Systémové profily (1.1.1)

`relationshipDefaults` na RelationSlot (JSON) — např. Association/`reportsTo`.

### BusinessActor (match properties)

| profileCode | Match | Label CS |
|-------------|-------|----------|
| `department` | organizationalUnit + internal | Oddělení |
| `person` | person + internal | Osoba |
| `externalOrganization` | organization + external | Externí organizace |
| `externalPerson` | person + external | Externí osoba |
| `internalOrganization` | organization + internal | Organizace |
| `externalUnit` | organizationalUnit + external | Externí jednotka |

### Ostatní elementy

| profileCode | AML typ | Label CS |
|-------------|---------|----------|
| `application` | ApplicationComponent | Aplikace |
| `businessProcess` | BusinessProcess | Proces |
| `businessCollaboration` | BusinessCollaboration | Business spolupráce |
| `businessEvent` | BusinessEvent | Business událost |
| `applicationService` | ApplicationService | Aplikační služba |
| `businessRole` | BusinessRole | Role |
| `businessFunction` | BusinessFunction | Oblast odpovědnosti |
| `businessService` | BusinessService | Business služba |
| `businessObject` | BusinessObject | Business objekt |
| `dataObject` | DataObject | Datový objekt |
| `applicationFunction` | ApplicationFunction | Aplikační funkce |
| `applicationProcess` | ApplicationProcess | Aplikační proces |
| `applicationCollaboration` | ApplicationCollaboration | Aplikační spolupráce |
| `technologyService` | TechnologyService | Technologická služba |
| `systemSoftware` | SystemSoftware | System software |
| `node` | Node | Uzel |
| `device` | Device | Zařízení |
| `artifact` | Artifact | Artefakt |
| `communicationNetwork` | CommunicationNetwork | Síť |
| `path` | Path | Spojení |
| `facility` | Facility | Areál |
| `location` | Location | Lokace |

**Záměrně bez profilu (raw ArchiMate karta):** ApplicationInterface, ApplicationEvent, TechnologyInterface, Gap, WorkPackage, Assessment, Requirement, Risk, ExchangeForeignElement.

## Import

1. `kc-base` 1.1.0
2. `archimate-lite` 3.2.1 (nebo ^3.2.0)
3. Tento package 1.1.1

```bash
python3 archimate-ui-cards/build_bundle.py
python3 archimate-ui-cards/load.py
```
