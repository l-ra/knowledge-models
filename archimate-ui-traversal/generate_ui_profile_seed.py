#!/usr/bin/env python3
"""Generate ui-profile-seed.json from IT Map templates.ts semantics (1:1)."""

from __future__ import annotations

import json
from pathlib import Path

PROFILE_IRI = "ui-profile-itmap-default"

TEMPLATES = [
    {
        "code": "business-exploration",
        "labelCs": "Business exploration",
        "isDefault": True,
        "sortOrder": 1,
        "startStage": "organization",
        "stages": [
            {"code": "organization", "labelCs": "Organizace", "classes": ["BusinessActor"], "actorKinds": ["organizationalUnit"]},
            {"code": "people-roles", "labelCs": "Lidé / Role", "classes": ["BusinessActor", "BusinessRole"], "actorKinds": ["person"]},
            {"code": "functions", "labelCs": "Oblasti odpovědnosti", "classes": ["BusinessFunction"]},
            {"code": "processes", "labelCs": "Procesy", "classes": ["BusinessProcess"]},
            {"code": "biz-services", "labelCs": "Business služby", "classes": ["BusinessService"]},
            {"code": "app-services", "labelCs": "Aplikační služby", "classes": ["ApplicationService"]},
            {"code": "applications", "labelCs": "Aplikace", "classes": ["ApplicationComponent"]},
            {"code": "data", "labelCs": "Data", "classes": ["DataObject"]},
            {"code": "tech", "labelCs": "Technologie", "classes": ["SystemSoftware", "TechnologyService"]},
            {"code": "nodes", "labelCs": "Uzly", "classes": ["Node", "Device"]},
            {"code": "network", "labelCs": "Síť", "classes": ["CommunicationNetwork", "Path"]},
            {"code": "facilities", "labelCs": "Lokality", "classes": ["Facility", "Location"]},
        ],
        "transitions": [
            {"from": "organization", "to": "people-roles", "relationship": "Composition", "direction": "model", "edgeLabelCs": "Obsahuje"},
            {"from": "organization", "to": "people-roles", "relationship": "Assignment", "direction": "model", "edgeLabelCs": "Má roli"},
            {"from": "people-roles", "to": "people-roles", "relationship": "Assignment", "direction": "model", "edgeLabelCs": "Přiřazeno"},
            {"from": "people-roles", "to": "functions", "relationship": "Assignment", "direction": "model", "edgeLabelCs": "Odpovídá za"},
            {"from": "organization", "to": "functions", "relationship": "Assignment", "direction": "model", "edgeLabelCs": "Odpovídá za"},
            {"from": "functions", "to": "processes", "relationship": "Composition", "direction": "model", "edgeLabelCs": "Obsahuje"},
            {"from": "functions", "to": "biz-services", "relationship": "Realization", "direction": "model", "edgeLabelCs": "Realizuje"},
            {"from": "processes", "to": "biz-services", "relationship": "Realization", "direction": "model", "edgeLabelCs": "Realizuje"},
            {"from": "processes", "to": "app-services", "relationship": "Serving", "direction": "inverse", "edgeLabelCs": "Podporováno"},
            {"from": "functions", "to": "app-services", "relationship": "Serving", "direction": "inverse", "edgeLabelCs": "Podporováno"},
            {"from": "biz-services", "to": "app-services", "relationship": "Serving", "direction": "inverse", "edgeLabelCs": "Podporováno"},
            {"from": "app-services", "to": "applications", "relationship": "Realization", "direction": "inverse", "edgeLabelCs": "Realizováno"},
            {"from": "applications", "to": "data", "relationship": "Access", "direction": "model", "edgeLabelCs": "Přistupuje"},
            {"from": "applications", "to": "tech", "relationship": "DeployedOn", "direction": "model", "edgeLabelCs": "Běží na"},
            {"from": "applications", "to": "tech", "relationship": "Serving", "direction": "inverse", "edgeLabelCs": "Závisí na"},
            {"from": "tech", "to": "nodes", "relationship": "Assignment", "direction": "model", "edgeLabelCs": "Na uzlu"},
            {"from": "nodes", "to": "network", "relationship": "Association", "direction": "model", "edgeLabelCs": "Síť"},
            {"from": "nodes", "to": "facilities", "relationship": "Association", "direction": "model", "edgeLabelCs": "Umístění"},
            {"from": "facilities", "to": "facilities", "relationship": "Association", "direction": "model", "edgeLabelCs": "Lokace"},
        ],
        "addActions": [
            {"stage": "organization", "code": "add-dept", "labelCs": "Organizační jednotka", "createsClass": "BusinessActor", "defaults": {"actorKind": "organizationalUnit", "organizationScope": "internal"}, "derivesRelationship": "Composition", "relationshipDirection": "from-selected-to-new"},
            {"stage": "people-roles", "code": "add-person", "labelCs": "Osoba", "createsClass": "BusinessActor", "defaults": {"actorKind": "person", "organizationScope": "internal"}, "derivesRelationship": "Composition", "relationshipDirection": "from-selected-to-new"},
            {"stage": "people-roles", "code": "add-role", "labelCs": "Role", "createsClass": "BusinessRole", "derivesRelationship": "Assignment", "relationshipDirection": "from-selected-to-new"},
            {"stage": "functions", "code": "add-function", "labelCs": "Oblast odpovědnosti", "createsClass": "BusinessFunction", "derivesRelationship": "Assignment", "relationshipDirection": "from-selected-to-new"},
            {"stage": "processes", "code": "add-process", "labelCs": "Proces / aktivita", "createsClass": "BusinessProcess", "derivesRelationship": "Composition", "relationshipDirection": "from-selected-to-new"},
            {"stage": "biz-services", "code": "add-biz-service", "labelCs": "Business služba", "createsClass": "BusinessService", "derivesRelationship": "Realization", "relationshipDirection": "from-selected-to-new"},
            {"stage": "app-services", "code": "add-app-service", "labelCs": "Aplikační služba", "createsClass": "ApplicationService", "derivesRelationship": "Serving", "relationshipDirection": "from-new-to-selected"},
            {"stage": "applications", "code": "add-app", "labelCs": "Aplikace / systém", "createsClass": "ApplicationComponent", "defaults": {"ownership": "internal"}, "derivesRelationship": "Realization", "relationshipDirection": "from-new-to-selected"},
            {"stage": "data", "code": "add-data", "labelCs": "Datový objekt", "createsClass": "DataObject", "derivesRelationship": "Access", "relationshipDirection": "from-selected-to-new", "relationshipDefaults": {"accessMode": "readWrite"}},
            {"stage": "tech", "code": "add-syssoft", "labelCs": "System software / runtime", "createsClass": "SystemSoftware", "derivesRelationship": "DeployedOn", "relationshipDirection": "from-selected-to-new"},
            {"stage": "tech", "code": "add-tech-svc", "labelCs": "Technologická služba", "createsClass": "TechnologyService", "derivesRelationship": "Serving", "relationshipDirection": "from-new-to-selected"},
            {"stage": "nodes", "code": "add-node", "labelCs": "Uzel / cluster", "createsClass": "Node", "derivesRelationship": "Assignment", "relationshipDirection": "from-selected-to-new"},
            {"stage": "network", "code": "add-network", "labelCs": "Síťový segment", "createsClass": "CommunicationNetwork", "defaults": {"networkKind": "vlan", "networkRole": "production"}, "derivesRelationship": "Association", "relationshipDirection": "from-selected-to-new", "relationshipDefaults": {"associationKind": "memberOf"}},
            {"stage": "facilities", "code": "add-facility", "labelCs": "Areál / DC", "createsClass": "Facility", "derivesRelationship": "Association", "relationshipDirection": "from-selected-to-new", "relationshipDefaults": {"associationKind": "locatedIn"}},
            {"stage": "facilities", "code": "add-location", "labelCs": "Geografická lokace", "createsClass": "Location", "derivesRelationship": "Association", "relationshipDirection": "from-selected-to-new"},
        ],
    },
    {
        "code": "application-impact",
        "labelCs": "Application impact",
        "sortOrder": 2,
        "stages": [
            {"code": "applications", "labelCs": "Aplikace", "classes": ["ApplicationComponent"]},
            {"code": "app-services", "labelCs": "Aplikační služby", "classes": ["ApplicationService"]},
            {"code": "processes", "labelCs": "Procesy", "classes": ["BusinessProcess", "BusinessFunction"]},
            {"code": "people-roles", "labelCs": "Role", "classes": ["BusinessRole"]},
            {"code": "organization", "labelCs": "Organizace", "classes": ["BusinessActor"]},
        ],
        "transitions": [
            {"from": "applications", "to": "app-services", "relationship": "Realization", "direction": "model", "edgeLabelCs": "Realizuje"},
            {"from": "app-services", "to": "processes", "relationship": "Serving", "direction": "model", "edgeLabelCs": "Podporuje"},
            {"from": "processes", "to": "people-roles", "relationship": "Assignment", "direction": "inverse", "edgeLabelCs": "Přiřazeno"},
            {"from": "people-roles", "to": "organization", "relationship": "Composition", "direction": "inverse", "edgeLabelCs": "Součást"},
        ],
        "addActions": [],
    },
    {
        "code": "infrastructure",
        "labelCs": "Infrastructure",
        "sortOrder": 3,
        "stages": [
            {"code": "nodes", "labelCs": "Uzly", "classes": ["Node"]},
            {"code": "tech", "labelCs": "Software", "classes": ["SystemSoftware"]},
            {"code": "applications", "labelCs": "Aplikace", "classes": ["ApplicationComponent"]},
            {"code": "app-services", "labelCs": "Služby", "classes": ["ApplicationService"]},
            {"code": "network", "labelCs": "Síť", "classes": ["CommunicationNetwork"]},
            {"code": "facilities", "labelCs": "Lokality", "classes": ["Facility", "Location"]},
        ],
        "transitions": [
            {"from": "nodes", "to": "tech", "relationship": "Assignment", "direction": "inverse", "edgeLabelCs": "Hostuje"},
            {"from": "tech", "to": "applications", "relationship": "DeployedOn", "direction": "inverse", "edgeLabelCs": "Nasazeno"},
            {"from": "applications", "to": "app-services", "relationship": "Realization", "direction": "model", "edgeLabelCs": "Realizuje"},
            {"from": "nodes", "to": "network", "relationship": "Association", "direction": "model", "edgeLabelCs": "Síť"},
            {"from": "nodes", "to": "facilities", "relationship": "Association", "direction": "model", "edgeLabelCs": "Umístění"},
        ],
        "addActions": [],
    },
]


def tpl_iri(code: str) -> str:
    return f"ui-tpl-{code}"


def stage_iri(tpl_code: str, stage_code: str) -> str:
    return f"ui-stage-{tpl_code}-{stage_code}"


def trans_iri(tpl_code: str, idx: int) -> str:
    return f"ui-trans-{tpl_code}-{idx:02d}"


def add_iri(tpl_code: str, action_code: str) -> str:
    return f"ui-add-{tpl_code}-{action_code}"


def build_instances() -> list[dict]:
    out: list[dict] = [
        {
            "iriLocal": PROFILE_IRI,
            "class": "UiNavigationProfile",
            "labels": {"cs": "IT Map — výchozí navigace", "en": "IT Map default navigation"},
            "properties": {
                "profileCode": "itmap-default",
                "profileVersion": "1.0.0",
                "minCatalogVersion": "3.1.0",
                "isSystemDefault": True,
                "labelCs": "IT Map — výchozí navigace",
                "labelEn": "IT Map default navigation",
            },
        }
    ]

    for tpl in TEMPLATES:
        tpl_code = tpl["code"]
        tpl_local = tpl_iri(tpl_code)
        props: dict = {
            "parentProfile": PROFILE_IRI,
            "templateCode": tpl_code,
            "labelCs": tpl["labelCs"],
            "sortOrder": tpl["sortOrder"],
        }
        if tpl.get("isDefault"):
            props["isDefault"] = True
        if tpl.get("startStage"):
            props["startStage"] = stage_iri(tpl_code, tpl["startStage"])
        out.append({
            "iriLocal": tpl_local,
            "class": "UiTraversalTemplate",
            "labels": {"en": tpl["labelCs"]},
            "properties": props,
        })

        for order, stage in enumerate(tpl["stages"], start=1):
            stage_props: dict = {
                "parentTemplate": tpl_local,
                "stageCode": stage["code"],
                "stageOrder": order,
                "columnLabelCs": stage["labelCs"],
                "targetClasses": stage["classes"],
            }
            if stage.get("filter"):
                stage_props["instanceFilter"] = json.dumps(stage["filter"], ensure_ascii=False)
            if stage.get("actorKinds"):
                stage_props["actorKinds"] = ",".join(stage["actorKinds"])
            out.append({
                "iriLocal": stage_iri(tpl_code, stage["code"]),
                "class": "UiStage",
                "labels": {"cs": stage["labelCs"]},
                "properties": stage_props,
            })

        for idx, tr in enumerate(tpl["transitions"], start=1):
            tr_props = {
                "parentTemplate": tpl_local,
                "fromStage": stage_iri(tpl_code, tr["from"]),
                "toStage": stage_iri(tpl_code, tr["to"]),
                "relationshipClass": tr["relationship"],
                "traverseDirection": tr["direction"],
                "uiEdgeLabelCs": tr["edgeLabelCs"],
            }
            if tr.get("requireProperty"):
                tr_props["requireProperty"] = json.dumps(tr["requireProperty"], ensure_ascii=False)
            out.append({
                "iriLocal": trans_iri(tpl_code, idx),
                "class": "UiTransition",
                "labels": {"cs": tr["edgeLabelCs"]},
                "properties": tr_props,
            })

        for sort_idx, act in enumerate(tpl["addActions"], start=1):
            act_props: dict = {
                "parentTemplate": tpl_local,
                "stage": stage_iri(tpl_code, act["stage"]),
                "actionCode": act["code"],
                "domainLabelCs": act["labelCs"],
                "createsClass": act["createsClass"],
                "sortOrder": sort_idx,
            }
            if act.get("defaults"):
                act_props["defaultProperties"] = json.dumps(act["defaults"], ensure_ascii=False)
            if act.get("derivesRelationship"):
                act_props["derivesRelationship"] = act["derivesRelationship"]
            if act.get("relationshipDirection"):
                act_props["relationshipDirection"] = act["relationshipDirection"]
            if act.get("relationshipDefaults"):
                act_props["relationshipDefaults"] = json.dumps(act["relationshipDefaults"], ensure_ascii=False)
            out.append({
                "iriLocal": add_iri(tpl_code, act["code"]),
                "class": "UiAddAction",
                "labels": {"cs": act["labelCs"]},
                "properties": act_props,
            })

    return out


def main() -> int:
    out_path = Path(__file__).resolve().parent / "ui-profile-seed.json"
    instances = build_instances()
    out_path.write_text(json.dumps(instances, ensure_ascii=False, indent=2) + "\n")
    tpl_counts = {t["code"]: {"stages": len(t["stages"]), "transitions": len(t["transitions"]), "addActions": len(t["addActions"])} for t in TEMPLATES}
    print(f"wrote {out_path} ({len(instances)} entities)")
    for code, c in tpl_counts.items():
        print(f"  {code}: {c['stages']} stages, {c['transitions']} transitions, {c['addActions']} add actions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
