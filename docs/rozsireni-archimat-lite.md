# Zadání rozšíření ArchiMate Lite pro model ORGX

## 1. Účel změny

Rozšířit metamodel `archimate-lite` tak, aby umožnil konzistentně uložit cílový architektonický model ORGX a podporoval zejména:

* organizační strukturu,
* role a odpovědnosti,
* business funkce,
* hierarchii business procesů,
* business služby,
* business události,
* business informace,
* aplikační komponenty a služby,
* integrační a datové vazby,
* technologickou infrastrukturu,
* vazby na lokality,
* BIA,
* BCM,
* CIP,
* HA/DR analýzu,
* auditovatelnou transformaci původního ArchiMate modelu do cílového modelu.

Cílem není implementovat kompletní ArchiMate specifikaci. `archimate-lite` má zůstat záměrně omezeným profilem obsahujícím pouze prvky a vztahy potřebné pro architektonické modelování ORGX.

Cílový základní řetězec modelu je:

```text
BusinessActor / BusinessRole
        ↓
BusinessFunction
        ↓
BusinessProcess
        ↓
ApplicationService
        ↓
ApplicationComponent
        ↓
TechnologyService / SystemSoftware / Node
        ↓
Facility
        ↓
Location
```

Vedle tohoto řetězce musí být možné modelovat:

```text
BusinessEvent
BusinessObject
DataObject
Flow
Triggering
Access
```

---

# 2. Požadované nové elementy

## 2.1 BusinessEvent

Do business vrstvy doplnit element:

```text
BusinessEvent
```

Charakteristika:

```text
subClassOf = ArchiMateElement
archiLayer = business
```

`BusinessEvent` je standardní a trvalou součástí cílového modelu. Není pouze pomocným prvkem pro migraci.

Použití:

* událost zahajující business proces,
* událost vznikající jako výsledek procesu,
* významná změna stavu relevantní pro business chování.

Typické příklady:

```text
Přijetí dat měření
Přijetí nominace
Uzavření trhu
Vznik požadavku
Přijetí regulačního rozhodnutí
```

Minimálně povolit:

```text
Triggering BusinessEvent → BusinessProcess
Triggering BusinessProcess → BusinessEvent
```

Druhá varianta se použije tam, kde proces explicitně vytváří další business událost.

Pokud stávající metamodel používá společné properties pro behavior elementy, má je `BusinessEvent` zdědit stejným způsobem jako ostatní business behavior prvky.

---

## 2.2 BusinessCollaboration

Doplnit element:

```text
BusinessCollaboration
```

Charakteristika:

```text
subClassOf = ArchiMateElement
archiLayer = business
```

Element se používá pouze tehdy, pokud architektonický objekt skutečně reprezentuje společné působení více business aktérů.

Nemá být používán jako obecný způsob reprezentace externí organizace.

Například:

```text
ORGY
ORGZ
Microsoft
T-Mobile
banka
dodavatel
```

jsou typicky:

```text
BusinessActor
actorKind = organization
organizationScope = external
```

nikoliv `BusinessCollaboration`.

Pro `BusinessCollaboration` povolit minimálně:

```text
Composition BusinessCollaboration → BusinessActor
Assignment BusinessCollaboration → BusinessProcess
Assignment BusinessCollaboration → BusinessFunction
```

Podle potřeby je možné povolit také:

```text
Realization BusinessCollaboration → BusinessService
```

pokud to odpovídá již používané sémantice `archimate-lite`.

---

## 2.3 BusinessObject

Doplnit element:

```text
BusinessObject
```

Charakteristika:

```text
subClassOf = ArchiMateElement
archiLayer = business
```

`BusinessObject` reprezentuje význam informace z pohledu businessu.

Příklady:

```text
Měřená data
Nominace
Výsledky trhu
Smlouva
Faktura
Platební příkaz
Účetní doklad
Požadavek zákazníka
```

Je nutné zachovat významové rozlišení:

```text
BusinessObject
```

= business význam informace,

zatímco:

```text
DataObject
```

= její aplikační nebo technická reprezentace.

Minimálně povolit:

```text
Access BusinessProcess → BusinessObject
Access BusinessFunction → BusinessObject
```

Doporučeně také:

```text
Access BusinessService → BusinessObject
```

pokud je takový vztah kompatibilní s koncepcí `archimate-lite`.

Do budoucna může být vhodné vytvořit explicitní vazbu mezi `BusinessObject` a `DataObject`, ale tato vazba není podmínkou první verze rozšíření.

---

# 3. Rozšíření AllowedRelationship matrix

`archimate-lite` používá explicitní `AllowedRelationship` matici pro kontrolu povolených kombinací typu vztahu, zdrojové třídy a cílové třídy. Rozšíření proto musí kromě definice elementů vždy obsahovat i odpovídající položky této matice.

## 3.1 Hierarchie business procesů

Doplnit:

```text
Composition
source = BusinessProcess
target = BusinessProcess
```

Tento vztah je nezbytný pro hierarchickou dekompozici procesů:

```text
L0
 └── L1
      └── L2
           └── L3
```

Například:

```text
Provoz trhu
  └─ Vyhodnocení trhu
       └─ Vyhodnocení odchylek
```

Pro strukturální hierarchii procesů je preferovaný vztah `Composition`.

`Aggregation` se pro základní procesní hierarchii ORGX nemá používat.

---

## 3.2 BusinessEvent

Doplnit:

```text
Triggering BusinessEvent → BusinessProcess
Triggering BusinessProcess → BusinessEvent
```

Doporučeně také:

```text
Triggering BusinessEvent → BusinessFunction
```

pouze pokud má být v `archimate-lite` podporováno spouštění celé business funkce událostí.

Pro první implementaci není tato třetí kombinace nutná.

---

## 3.3 BusinessCollaboration

Doplnit:

```text
Composition BusinessCollaboration → BusinessActor
Assignment BusinessCollaboration → BusinessProcess
Assignment BusinessCollaboration → BusinessFunction
```

Volitelně:

```text
Realization BusinessCollaboration → BusinessService
```

---

## 3.4 BusinessObject

Doplnit:

```text
Access BusinessProcess → BusinessObject
Access BusinessFunction → BusinessObject
```

Doporučeně:

```text
Access BusinessService → BusinessObject
```

---

# 4. Procesní hierarchie

Doplnit property:

```text
processLevel
```

Použitelná minimálně na:

```text
BusinessProcess
```

Doporučený hodnotový prostor:

```text
L0
L1
L2
L3
```

Případně:

```text
L4
```

pokud bude později potřebná detailnější procesní úroveň.

Význam:

```text
L0 = nejvyšší business oblast / procesní doména
L1 = hlavní proces
L2 = proces
L3 = podproces / detailní proces
```

Hodnota musí vyjadřovat úroveň procesu, nikoliv technologickou úroveň modelu.

`processLevel` proto nesmí nahrazovat existující obecnou property:

```text
modelingDepth
```

Oba atributy mají rozdílný význam.

---

# 5. Organizační model

Stávající `BusinessActor`, `BusinessRole`, `BusinessFunction` a `BusinessProcess` mají být zachovány.

Pro cílový koncept musí být podporován následující modelovací vzor:

```text
BusinessActor
   └─ Composition → BusinessActor

BusinessActor
   └─ Assignment → BusinessRole

BusinessRole
   ├─ Assignment → BusinessFunction
   └─ Assignment → BusinessProcess
```

Pro organizační strukturu musí zůstat podporováno:

```text
Composition BusinessActor → BusinessActor
```

`BusinessActor` se používá pro:

```text
organizaci,
organizační útvar,
externí organizaci,
osobu.
```

Stávající properties:

```text
actorKind
organizationScope
```

zachovat a používat k rozlišení těchto významů.

Doporučené hodnotové principy:

```text
actorKind:
  organization
  organizationalUnit
  person

organizationScope:
  internal
  external
```

Pokud současná implementace již definuje konkrétní enum nebo slovník pro tyto properties, zachovat existující hodnoty a pouze ověřit, že výše uvedené případy pokrývají.

Nevytvářet duplicitní properties se stejným významem.

---

# 6. Business funkce a procesy

Musí zůstat podporovány stávající vztahy:

```text
Composition BusinessFunction → BusinessProcess
Assignment BusinessRole → BusinessFunction
Assignment BusinessRole → BusinessProcess
Realization BusinessFunction → BusinessService
Realization BusinessProcess → BusinessService
```

Doplněním:

```text
Composition BusinessProcess → BusinessProcess
```

vznikne cílový vzor:

```text
BusinessFunction
   └─ Composition → BusinessProcess
                         └─ Composition → BusinessProcess
```

Je třeba zachovat významové rozlišení:

```text
BusinessFunction
```

= stabilní oblast odpovědnosti nebo capability-like business chování,

```text
BusinessProcess
```

= konkrétní opakovatelný proces s průběhem nebo výsledkem.

---

# 7. Business služby

Zachovat:

```text
BusinessService
```

a vztahy:

```text
Realization BusinessProcess → BusinessService
Realization BusinessFunction → BusinessService
```

Business služba představuje výsledek nebo službu poskytovanou konzumentovi, nikoliv samotný interní proces.

---

# 8. Aplikační vrstva

Stávající koncepty:

```text
ApplicationComponent
ApplicationService
ApplicationInterface
ApplicationFunction
ApplicationProcess
ApplicationEvent
ApplicationCollaboration
DataObject
```

není nutné pro potřeby této změny odstraňovat.

Pro core profil ORGX jsou zásadní:

```text
ApplicationComponent
ApplicationService
DataObject
```

Musí zůstat podporován základní vzor:

```text
ApplicationComponent
   └─ Realization → ApplicationService

ApplicationService
   ├─ Serving → BusinessProcess
   └─ Serving → BusinessFunction
```

Pokud některá z těchto kombinací v aktuální `AllowedRelationship` matrix chybí, doplnit ji.

Konkrétní aplikace nebo informační systém se modeluje jako:

```text
ApplicationComponent
```

nikoliv jako `ApplicationService`.

Například:

```text
SAP
Jira
O365
SYSA
SIEM
SYSB
```

mají být typicky `ApplicationComponent`.

`ApplicationService` reprezentuje funkci/službu, kterou aplikace poskytuje businessu.

---

# 9. Aplikační datové toky

Zachovat a podporovat:

```text
Flow ApplicationComponent → ApplicationComponent
```

Každý integrační `Flow` musí umožňovat minimálně následující properties:

```text
flowLabel
flowKind
messageOrObject
protocol
synchronous
authentication
dependencyType
dependencyStrength
```

Pokud některá z těchto properties již v `archimate-lite` existuje, nesmí vzniknout duplicitní property.

Minimálně `flowLabel` musí být dostupné pro `Flow`.

Typický příklad:

```text
SYSA
   ── Flow ──>
SYSB
```

s properties:

```text
flowLabel = "Data měření"
flowKind = data
dependencyType = data
dependencyStrength = mandatory
```

Více `Flow` mezi stejnými dvěma komponentami musí být povoleno.

Například:

```text
SYSA → SYSB : Data měření
SYSA → SYSB : Data DUF
```

jsou dva různé vztahy a nemají být automaticky považovány za duplicitu.

---

# 10. Technologická vrstva

Pro cílový model zachovat podporu minimálně následujících elementů:

```text
TechnologyService
SystemSoftware
Node
Device
CommunicationNetwork
Facility
Location
Artifact
```

Musí být možné sestavit minimálně řetězec:

```text
ApplicationComponent
   └─ DeployedOn → SystemSoftware

SystemSoftware
   └─ Assignment → Node

Node
   ├─ Association → CommunicationNetwork
   ├─ Association → Facility
   └─ Realization → TechnologyService

Facility
   └─ Association → Location

TechnologyService
   ├─ Serving → ApplicationComponent
   └─ Serving → ApplicationService
```

Aktuální `archimate-lite` již obsahuje část těchto kombinací, například:

```text
DeployedOn ApplicationComponent → SystemSoftware
Assignment SystemSoftware → Node
Association Node → Facility
Association Facility → Location
Association Node → CommunicationNetwork
Serving TechnologyService → ApplicationComponent
```

Při implementaci změny je nutné porovnat celý cílový vzor s aktuální `AllowedRelationship` matrix a doplnit pouze skutečně chybějící kombinace.

Nevytvářet duplicitní definice existujících vztahů.

---

# 11. BIA / BCM / HA / DR properties

Stávající properties relevantní pro analytický model zachovat.

Patří mezi ně zejména:

```text
criticality
rto
rpo
dependencyType
dependencyStrength
degradedMode
businessImpact
```

a další existující technologické nebo provozní properties.

Primární business hodnoty:

```text
criticality
rto
rpo
businessImpact
```

budou používány zejména na:

```text
BusinessProcess
```

případně:

```text
BusinessService
```

Aplikace a infrastruktura mohou později obsahovat hodnoty odvozené propagací závislostí.

---

# 12. Rozlišení deklarovaných a odvozených BIA hodnot

Doporučuje se doplnit properties:

```text
criticalitySource
rtoSource
rpoSource
```

Hodnotový prostor:

```text
declared
inherited
calculated
```

Význam:

```text
declared
```

= hodnota byla stanovena přímo vlastníkem nebo BIA analýzou,

```text
inherited
```

= hodnota byla převzata z nadřazeného nebo souvisejícího prvku,

```text
calculated
```

= hodnota byla vypočtena automatickou analýzou závislostí.

Tyto properties nejsou podmínkou pro samotnou konverzi stávajícího modelu, ale jejich zavedení je silně doporučeno před implementací automatické propagace BIA/HA/DR požadavků.

---

# 13. Migrační metadata

Transformace stávajícího ORGX modelu musí být auditovatelná.

Do metamodelu proto doplnit podporu migračních metadat.

Preferovaným řešením je vytvořit samostatné rozšíření nebo namespace, například:

```text
architecture-migration
```

Migrační metadata nemají být považována za standardní ArchiMate sémantiku.

Minimálně podporovat:

```text
migrationStatus
migrationAction
migrationRule
migrationSourceId
migrationSourceIds
migrationSourceType
migrationSourceName
migrationConfidence
migrationBatch
migrationTimestamp
migrationNotes
```

---

## 13.1 migrationStatus

Povolené hodnoty:

```text
unchanged
transformed
split
merged
created
deprecated
needsReview
rejected
```

---

## 13.2 migrationAction

Minimální doporučený slovník:

```text
TYPE_CHANGED
RELATIONSHIP_CHANGED
NAME_NORMALIZED
SPLIT_ELEMENT
MERGED_DUPLICATE
CREATED_INTERMEDIATE
REMOVED_ORPHAN
FIXED_REFERENCE
UNCHANGED
```

Není nutné implementovat jako uzavřený enum, pokud současná architektura properties preferuje ORGXvřený slovník.

---

## 13.3 migrationConfidence

Povolené hodnoty:

```text
high
medium
low
manual
```

Význam:

```text
high
```

= transformace je jednoznačně odvoditelná z původních dat,

```text
medium
```

= transformace je velmi pravděpodobná, ale vyžaduje kontrolu,

```text
low
```

= transformace je pouze pracovní hypotéza,

```text
manual
```

= transformace byla potvrzena člověkem.

---

# 14. Požadavky na použitelnost properties

Properties nemají být pouze globálně zaregistrovány.

Implementace musí umožnit určit:

* na jakých třídách mohou být použity,
* na jakých vztazích mohou být použity,
* doporučený datový typ,
* případný povolený hodnotový prostor,
* usage guidance,
* usage examples.

Pro nově přidané properties vytvořit dokumentaci stejným způsobem jako pro stávající properties `actorKind`, `organizationScope`, `criticality`, `rto`, `rpo`, `dependencyType` apod.

---

# 15. Požadavky na dokumentaci nových elementů

Pro každý nový element vytvořit minimálně:

```text
label
definition
usageGuidance
usageExamples
```

Případně další metadata podle konvence existujícího bundle.

Dokumentace musí vysvětlovat zejména hranice mezi podobnými koncepty.

---

## BusinessActor vs BusinessCollaboration

```text
BusinessActor
```

= jeden identifikovatelný aktér.

```text
BusinessCollaboration
```

= společné působení více aktérů.

---

## BusinessFunction vs BusinessProcess

```text
BusinessFunction
```

= stabilní oblast odpovědnosti nebo chování.

```text
BusinessProcess
```

= konkrétní průběh činnosti.

---

## BusinessObject vs DataObject

```text
BusinessObject
```

= business význam informace.

```text
DataObject
```

= aplikační nebo technická reprezentace informace.

---

## ApplicationComponent vs ApplicationService

```text
ApplicationComponent
```

= aplikace, systém nebo logická aplikační komponenta.

```text
ApplicationService
```

= služba poskytovaná komponentou.

---

# 16. Core profil ORGX

Po rozšíření musí `archimate-lite` umožnit používat následující minimální profil.

## Business

```text
BusinessActor
BusinessRole
BusinessFunction
BusinessProcess
BusinessService
BusinessEvent
BusinessCollaboration
BusinessObject
```

## Application

```text
ApplicationComponent
ApplicationService
DataObject
```

## Technology

```text
TechnologyService
SystemSoftware
Node
Device
CommunicationNetwork
Facility
Location
```

## Relations

```text
Composition
Assignment
Realization
Serving
Access
Flow
Triggering
Association
DeployedOn
```

Ostatní již existující elementy `archimate-lite` není nutné odstraňovat.

Core profil pouze určuje preferovanou podmnožinu pro ORGX.

---

# 17. Referenční modelovací vzory

Po implementaci musí projít validací minimálně následující struktury.

## 17.1 Organizace

```text
ORGX : BusinessActor
 └─ Composition
      └─ Odbor ICT : BusinessActor

Odbor ICT
 └─ Assignment
      └─ Vedoucí odboru : BusinessRole

Vedoucí odboru
 └─ Assignment
      └─ Řízení ICT : BusinessFunction
```

---

## 17.2 Procesní struktura

```text
Řízení energetického trhu : BusinessFunction
 └─ Composition
      └─ Vyhodnocení trhu : BusinessProcess [L1]
           └─ Composition
                └─ Vyhodnocení odchylek : BusinessProcess [L2]
```

---

## 17.3 Událost

```text
Přijetí dat měření : BusinessEvent
 └─ Triggering
      └─ Zpracování dat měření : BusinessProcess
```

---

## 17.4 Business informace

```text
Zpracování dat měření : BusinessProcess
 └─ Access
      └─ Měřená data : BusinessObject
```

---

## 17.5 Aplikace

```text
SYSA : ApplicationComponent
 └─ Realization
      └─ Zpracování měřených dat : ApplicationService
           └─ Serving
                └─ Zpracování dat měření : BusinessProcess
```

---

## 17.6 Integrace

```text
SYSA : ApplicationComponent
 └─ Flow
      └─ SYSB : ApplicationComponent
```

Properties vztahu:

```text
flowLabel = "Data měření"
flowKind = data
dependencyType = data
dependencyStrength = mandatory
```

---

## 17.7 Technologie

```text
SYSA : ApplicationComponent
 └─ DeployedOn
      └─ SYSA runtime : SystemSoftware
           └─ Assignment
                └─ SYSA cluster : Node
                     └─ Association
                          └─ DC Praha : Facility
                               └─ Association
                                    └─ Praha : Location
```

---

# 18. Validační pravidla

Rozšířený `archimate-lite` by měl umožnit kontrolovat minimálně následující invariants.

## V1

Každý `BusinessActor`, který reprezentuje organizaci, útvar nebo osobu, může obsahovat:

```text
actorKind
organizationScope
```

## V2

Procesní hierarchie musí být vyjádřena:

```text
Composition BusinessProcess → BusinessProcess
```

## V3

Každý `BusinessProcess` může mít:

```text
processLevel
```

## V4

`ApplicationService` může být realizována:

```text
ApplicationComponent
```

## V5

`ApplicationService` může obsluhovat:

```text
BusinessProcess
BusinessFunction
```

## V6

`BusinessEvent` může pomocí `Triggering` spouštět `BusinessProcess`.

## V7

`BusinessProcess` a `BusinessFunction` mohou pomocí `Access` pracovat s `BusinessObject`.

## V8

`ApplicationComponent` může pomocí `Access` pracovat s `DataObject`.

## V9

`Flow ApplicationComponent → ApplicationComponent` musí být povolen.

## V10

Musí být možné uložit více různých `Flow` vztahů mezi stejnou dvojicí elementů.

## V11

Relace nesmí mít jinou relaci jako `relSource` nebo `relTarget`.

Zdroj i cíl architektonického vztahu musí být architektonický element.

---

# 19. Zpětná kompatibilita

Rozšíření nesmí:

* odstranit existující třídy,
* změnit existující public ID,
* změnit význam existujících properties,
* měnit existující `AllowedRelationship` z povoleného na zakázaný bez samostatného rozhodnutí,
* měnit identitu stávajících objektů,
* vytvářet duplicitní properties pouze kvůli jinému názvu.

Preferovaný způsob je čistě aditivní změna metamodelu.

---

# 20. Verzování

Rozšíření má být vydáno jako nová verze `archimate-lite`.

Například:

```text
3.2.0
```

pokud verzovací konvence projektu považuje přidání nových elementů a properties za zpětně kompatibilní minor změnu.

Pokud projekt používá jiná pravidla semantic versioning, řídit se existující konvencí repository.

Bundle musí jednoznačně identifikovat novou verzi.

---

# 21. Minimální rozsah implementace

Za povinnou část první verze rozšíření považovat:

```text
BusinessEvent
BusinessCollaboration
BusinessObject
Composition BusinessProcess → BusinessProcess
processLevel
migration metadata
```

plus všechny `AllowedRelationship` potřebné pro používání těchto elementů.

---

# 22. Doporučená část

Doporučeně současně doplnit:

```text
criticalitySource
rtoSource
rpoSource
```

a případné chybějící `AllowedRelationship` kombinace potřebné pro celý referenční řetězec:

```text
Business
→ Application
→ Technology
→ Facility
→ Location
```

---

# 23. Akceptační kritéria

Úpravu `archimate-lite` lze považovat za dokončenou, pokud:

1. lze vytvořit instanci `BusinessEvent`;
2. lze vytvořit instanci `BusinessCollaboration`;
3. lze vytvořit instanci `BusinessObject`;
4. lze vytvořit hierarchii `BusinessProcess → Composition → BusinessProcess`;
5. `BusinessProcess` podporuje `processLevel`;
6. lze vytvořit `BusinessEvent → Triggering → BusinessProcess`;
7. lze vytvořit `BusinessProcess → Access → BusinessObject`;
8. lze vytvořit organizační model Actor → Role → Function/Process;
9. lze vytvořit řetězec ApplicationComponent → ApplicationService → BusinessProcess;
10. lze vytvořit Flow mezi dvěma ApplicationComponent;
11. lze vytvořit technologický řetězec od ApplicationComponent po Location;
12. lze u změněného elementu uložit migrační metadata;
13. nové elementy a properties mají usage guidance a příklady;
14. všechny nové kombinace vztahů jsou zaneseny v `AllowedRelationship` matrix;
15. změna nerozbije načtení modelů vytvořených proti předchozí verzi `archimate-lite`.

---

# 24. Co není předmětem této změny

V této fázi není požadováno:

* implementovat kompletní ArchiMate metamodel,
* automaticky transformovat současný ORGX model,
* automaticky vypočítávat RTO nebo RPO,
* automaticky propagovat criticality,
* automaticky detekovat SPOF,
* odstraňovat stávající elementy z `archimate-lite`,
* měnit vizualizační pravidla nad rámec toho, co je nutné pro zobrazení nových elementů.

Automatická transformace stávajícího modelu bude provedena až nad takto rozšířeným cílovým metamodellem.

---

# 25. Shrnutí požadovaných změn

## Nové elementy

```text
BusinessEvent
BusinessCollaboration
BusinessObject
```

## Nová property

```text
processLevel
```

## Nová povinná kombinace vztahu

```text
Composition BusinessProcess → BusinessProcess
```

## Nové vazby související s elementy

```text
Triggering BusinessEvent → BusinessProcess
Triggering BusinessProcess → BusinessEvent

Composition BusinessCollaboration → BusinessActor
Assignment BusinessCollaboration → BusinessProcess
Assignment BusinessCollaboration → BusinessFunction

Access BusinessProcess → BusinessObject
Access BusinessFunction → BusinessObject
```

## Migrační properties

```text
migrationStatus
migrationAction
migrationRule
migrationSourceId
migrationSourceIds
migrationSourceType
migrationSourceName
migrationConfidence
migrationBatch
migrationTimestamp
migrationNotes
```

## Doporučené BIA properties

```text
criticalitySource
rtoSource
rpoSource
```

Výsledný `archimate-lite` musí být schopen uložit cílový ORGX model bez nutnosti používat významově nesprávné typy elementů nebo vztahů.


Migracni properties musi byt v separatnim baliku, at je mozne je snadno odlisit. 