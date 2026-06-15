#!/usr/bin/env python3
"""Generate RE-141 object-interaction proof-first audit artifacts."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path

RE140_HANDOFF = "docs/reverse/generated/re140-gameplay-mixed-handoff.csv"
RE061_AUDIT = "docs/reverse/generated/re061-module-game-proof-first-audit.csv"
RE061_CLUSTERS = "docs/reverse/generated/re061-module-game-clusters.csv"
AUDIT_CSV = "docs/reverse/generated/re141-object-interaction-proof-first-audit.csv"
CLUSTERS_CSV = "docs/reverse/generated/re141-object-interaction-clusters.csv"
TICKET_PLAN_CSV = "docs/reverse/generated/re141-object-interaction-ticket-plan.csv"
MD_OUTPUT = "docs/reverse/functions/re141-object-interaction-proof-first-audit.md"
STORY_OUTPUT = "docs/stories/RE-141-object-interaction-proof-first-audit.md"
FORBIDDEN = ("0x", "payload", "opcode", "machine word", "raw call target")
CLOSED_CLUSTERS = {"debris-object-breakage", "lara-movement-support", "gameflow-runtime-control", "gameplay-mixed"}
ORDER = {
    "FindPlinth": 0,
    "CollectCarriedItems": 1,
    "BaddyObjects": 2,
    "InitialiseObjects": 3,
    "TrapObjects": 4,
    "ObjectObjects": 5,
}


@dataclass(frozen=True)
class AuditRow:
    function: str
    file: str
    line: int
    implementation_status: str
    object_family: str
    cluster: str
    role: str
    readiness: str
    code_change_ready: str
    marker_ready: str
    blocker: str
    next_probe: str


@dataclass(frozen=True)
class TicketPlanRow:
    story_id: str
    topic: str
    goal: str


@dataclass(frozen=True)
class ObjectInteractionAudit:
    story_id: str
    upstream_ticket: str
    domain_id: str
    cluster: str
    pivot: str
    readiness: str
    code_change_ready_count: int
    marker_ready_count: int
    next_ticket: str
    rows: tuple[AuditRow, ...]
    ticket_plan: tuple[TicketPlanRow, ...]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def function_body(repo: Path, file_name: str, function: str) -> str:
    path = repo / file_name
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(rf"\b{re.escape(function)}\s*\([^)]*\)", text)
    if not match:
        return ""
    brace = text.find("{", match.end())
    if brace < 0:
        return ""
    pos = brace + 1
    depth = 1
    while pos < len(text) and depth:
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
        pos += 1
    return text[brace + 1:pos - 1]


def implementation_status(repo: Path, file_name: str, function: str) -> str:
    body = function_body(repo, file_name, function)
    if not body.strip():
        return "missing-source"
    if "UNIMPLEMENTED" in body or "Unimpl" in body:
        if "#if PC_VERSION" in body or "#if !PC_VERSION" in body:
            return "platform-gated-source"
        return "unimplemented-stub"
    return "implemented-source"


def build_ticket_plan() -> tuple[TicketPlanRow, ...]:
    plans = [
        ("RE-142", "object-interaction-caller-side-effect-map", "Map object-interaction callers, pickup/object setup state, and side-effect surfaces."),
        ("RE-143", "object-interaction-argument-state-taxonomy", "Classify object-interaction argument shapes, item/object state, setup tables, and trap/baddy side effects."),
        ("RE-144", "object-interaction-comparison-gate", "Decide if object-interaction has enough non-raw equivalence proof for any source or marker change."),
        ("RE-145", "object-interaction-reconstruction-plan", "Publish a source reconstruction plan if the proof gate remains blocked."),
        ("RE-146", "object-interaction-source-patch-gate", "Keep source patch denied unless the comparison gate produces a symbolic equivalence proof."),
        ("RE-147", "object-interaction-validation-regression", "Validate generated object-interaction metadata and forbidden-evidence guards."),
        ("RE-148", "object-interaction-closure-or-handoff", "Close object-interaction or hand off to item-lighting-interaction with a refreshed plan."),
    ]
    return tuple(TicketPlanRow(story_id=sid, topic=topic, goal=goal) for sid, topic, goal in plans)


def verify_upstream(repo: Path) -> None:
    handoff = read_csv(repo / RE140_HANDOFF)[0]
    if handoff["next_ticket"] != "RE-141" or handoff["next_cluster"] != "object-interaction":
        raise ValueError("RE-140 handoff no longer selects RE-141 object-interaction")
    rows = read_csv(repo / RE061_CLUSTERS)
    remaining = [row for row in rows if row["cluster"] not in CLOSED_CLUSTERS]
    if not remaining or remaining[0]["cluster"] != "object-interaction":
        raise ValueError("RE-061 module-game cluster ordering no longer selects object-interaction after closed clusters")


def build_object_interaction_audit(repo: Path) -> ObjectInteractionAudit:
    repo = Path(repo)
    verify_upstream(repo)
    audit_rows = [row for row in read_csv(repo / RE061_AUDIT) if row["cluster"] == "object-interaction"]
    audit_rows.sort(key=lambda row: (ORDER.get(row["function"], 99), row["function"]))
    rows: list[AuditRow] = []
    for row in audit_rows:
        function = row["function"]
        rows.append(AuditRow(
            function=function,
            file=row["file"],
            line=int(row["line"]),
            implementation_status=implementation_status(repo, row["file"], function),
            object_family="object-setup-state" if function in {"BaddyObjects", "InitialiseObjects", "TrapObjects", "ObjectObjects"} else "object-interaction-state",
            cluster="object-interaction",
            role="pivot-object-interaction" if function == "FindPlinth" else "object-interaction-support",
            readiness="proof-first-audit-needed",
            code_change_ready="no",
            marker_ready="no",
            blocker="Object interaction state contract and symbolic equivalence proof missing",
            next_probe="RE-142 Object interaction caller and side-effect map",
        ))
    return ObjectInteractionAudit(
        story_id="RE-141",
        upstream_ticket="RE-140",
        domain_id="module-game",
        cluster="object-interaction",
        pivot="FindPlinth",
        readiness="blocked",
        code_change_ready_count=0,
        marker_ready_count=0,
        next_ticket="RE-142",
        rows=tuple(rows),
        ticket_plan=build_ticket_plan(),
    )


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def assert_clean(path: Path) -> None:
    text = path.read_text(encoding="utf-8").lower()
    hits = [item for item in FORBIDDEN if item in text]
    if hits:
        raise ValueError(f"forbidden metadata fragments in {path}: {hits}")


def write_all_artifacts(audit: ObjectInteractionAudit, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "audit_csv": repo / AUDIT_CSV,
        "clusters_csv": repo / CLUSTERS_CSV,
        "ticket_plan_csv": repo / TICKET_PLAN_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY_OUTPUT,
    }
    write_csv(paths["audit_csv"], list(AuditRow.__dataclass_fields__), [row.__dict__ for row in audit.rows])
    write_csv(paths["clusters_csv"], ["cluster", "candidate_count", "top_function", "representative_functions", "object_family", "readiness", "blocker", "recommended_next_ticket"], [{
        "cluster": audit.cluster,
        "candidate_count": len(audit.rows),
        "top_function": audit.pivot,
        "representative_functions": ";".join(row.function for row in audit.rows),
        "object_family": "object-interaction-state",
        "readiness": "best-next-module-game-cluster",
        "blocker": "Object interaction state contract and symbolic equivalence proof missing",
        "recommended_next_ticket": audit.next_ticket,
    }])
    write_csv(paths["ticket_plan_csv"], ["story_id", "topic", "goal", "scope", "code_change_readiness", "exit_condition"], [
        {"story_id": plan.story_id, "topic": plan.topic, "goal": plan.goal, "scope": audit.cluster, "code_change_readiness": "blocked-until-proof", "exit_condition": "artifact published or terminal proof blocker recorded"}
        for plan in audit.ticket_plan
    ])
    md = [
        "# RE-141 — Object interaction proof-first audit", "",
        f"Domain: `{audit.domain_id}`", f"Cluster: `{audit.cluster}`", f"Pivot: `{audit.pivot}`", f"Readiness: `{audit.readiness}`", "",
        "## Progress tracker", "", "- [x] RE-140 gameplay-mixed handoff consumed.", "- [x] RE-061 object-interaction rows selected.", "- [x] Metadata-only readiness checked.", "- [x] RE-142..RE-148 ticket plan emitted.", "",
        "## Findings", "",
    ]
    for row in audit.rows:
        md.append(f"- `{row.function}` — `{row.implementation_status}`; readiness `{row.readiness}`; blocker `{row.blocker}`")
    md.extend(["", "No production source or marker change is authorized by this audit."])
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text("\n".join(md) + "\n", encoding="utf-8")
    story = [
        "# RE-141 — Object interaction proof-first audit", "", "Status: Done", "", "## Goal", "", "Open `object-interaction` after the prior module-game handoff as a metadata-only proof-first audit.", "", "## Progress tracker", "", "- [x] RE-140 gameplay-mixed handoff consumed.", "- [x] RE-061 object-interaction rows selected.", "- [x] FindPlinth object-interaction pivot selected.", "- [x] Readiness and blockers recorded.", "- [x] RE-142..RE-148 ticket plan emitted.", "", "## Readiness decision", "", "- decision: `proof-first-audit-blocked`", "- code change readiness: `blocked`", "- next ticket: `RE-142`", "", "## Validation", "", "- `python3 -m pytest tests/reverse/test_re141_object_interaction_audit.py -q`", "- `python3 -m pytest tests/reverse -q`", "- metadata-only guard over RE-141 artifacts", "",
    ]
    paths["story"].parent.mkdir(parents=True, exist_ok=True)
    paths["story"].write_text("\n".join(story), encoding="utf-8")
    for path in paths.values():
        assert_clean(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    audit = build_object_interaction_audit(args.repo)
    for key, path in write_all_artifacts(audit, args.repo).items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
