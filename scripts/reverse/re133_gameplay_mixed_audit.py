#!/usr/bin/env python3
"""Generate RE-133 gameplay-mixed proof-first audit artifacts."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path

RE132_HANDOFF = "docs/reverse/generated/re132-runtime-support-handoff.csv"
RE061_AUDIT = "docs/reverse/generated/re061-module-game-proof-first-audit.csv"
RE061_CLUSTERS = "docs/reverse/generated/re061-module-game-clusters.csv"
AUDIT_CSV = "docs/reverse/generated/re133-gameplay-mixed-proof-first-audit.csv"
CLUSTERS_CSV = "docs/reverse/generated/re133-gameplay-mixed-clusters.csv"
TICKET_PLAN_CSV = "docs/reverse/generated/re133-gameplay-mixed-ticket-plan.csv"
MD_OUTPUT = "docs/reverse/functions/re133-gameplay-mixed-proof-first-audit.md"
STORY_OUTPUT = "docs/stories/RE-133-gameplay-mixed-proof-first-audit.md"
FORBIDDEN = ("0x", "payload", "opcode", "machine word", "raw call target")
CLOSED_CLUSTERS = {"debris-object-breakage", "lara-movement-support", "gameflow-runtime-control"}
ORDER = {
    "Load_and_Init_Cutseq": 0,
    "CreateZone": 1,
    "special4_init": 2,
    "init_water_table": 3,
    "InitialiseSqrtTable": 4,
    "InitTarget": 5,
    "InitBinoculars": 6,
    "InitialiseFootPrints": 7,
    "LoadLevel": 8,
    "EscapeBox": 9,
    "InitPackNodes": 10,
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
class GameplayMixedAudit:
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
        ("RE-134", "gameplay-mixed-caller-side-effect-map", "Map gameplay-mixed callers, callees, cutscene/zone/setup state, and side-effect surfaces."),
        ("RE-135", "gameplay-mixed-argument-state-taxonomy", "Classify gameplay-mixed argument shapes, global gameplay state, cutscene state, level/setup state, and zone side effects."),
        ("RE-136", "gameplay-mixed-comparison-gate", "Decide if gameplay-mixed has enough non-raw equivalence proof for any source or marker change."),
        ("RE-137", "gameplay-mixed-reconstruction-plan", "Publish a source reconstruction plan if the proof gate remains blocked."),
        ("RE-138", "gameplay-mixed-source-patch-gate", "Keep source patch denied unless the comparison gate produces a symbolic equivalence proof."),
        ("RE-139", "gameplay-mixed-validation-regression", "Validate generated gameplay-mixed metadata and forbidden-evidence guards."),
        ("RE-140", "gameplay-mixed-closure-or-handoff", "Close gameplay-mixed or hand off to object-interaction with a refreshed plan."),
    ]
    return tuple(TicketPlanRow(story_id=sid, topic=topic, goal=goal) for sid, topic, goal in plans)


def verify_upstream(repo: Path) -> None:
    handoff = read_csv(repo / RE132_HANDOFF)[0]
    if handoff["next_subcluster"] != "gameflow-runtime-control-exhausted":
        raise ValueError("RE-132 handoff no longer exhausts gameflow-runtime-control")
    rows = read_csv(repo / RE061_CLUSTERS)
    remaining = [row for row in rows if row["cluster"] not in CLOSED_CLUSTERS]
    if not remaining or remaining[0]["cluster"] != "gameplay-mixed":
        raise ValueError("RE-061 module-game cluster ordering no longer selects gameplay-mixed after closed clusters")


def build_gameplay_mixed_audit(repo: Path) -> GameplayMixedAudit:
    repo = Path(repo)
    verify_upstream(repo)
    audit_rows = [row for row in read_csv(repo / RE061_AUDIT) if row["cluster"] == "gameplay-mixed"]
    audit_rows.sort(key=lambda row: (ORDER.get(row["function"], 99), row["function"]))
    rows: list[AuditRow] = []
    for row in audit_rows:
        function = row["function"]
        rows.append(AuditRow(
            function=function,
            file=row["file"],
            line=int(row["line"]),
            implementation_status=implementation_status(repo, row["file"], function),
            object_family="gameplay-state",
            cluster="gameplay-mixed",
            role="pivot-gameplay-mixed" if function == "Load_and_Init_Cutseq" else "gameplay-mixed-support",
            readiness="proof-first-audit-needed",
            code_change_ready="no",
            marker_ready="no",
            blocker="Gameplay mixed state contract and symbolic equivalence proof missing",
            next_probe="RE-134 Gameplay mixed caller and side-effect map",
        ))
    return GameplayMixedAudit(
        story_id="RE-133",
        upstream_ticket="RE-132",
        domain_id="module-game",
        cluster="gameplay-mixed",
        pivot="Load_and_Init_Cutseq",
        readiness="blocked",
        code_change_ready_count=0,
        marker_ready_count=0,
        next_ticket="RE-134",
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


def write_all_artifacts(audit: GameplayMixedAudit, repo: Path) -> dict[str, Path]:
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
        "object_family": "gameplay-state",
        "readiness": "best-next-module-game-cluster",
        "blocker": "Gameplay mixed state contract and symbolic equivalence proof missing",
        "recommended_next_ticket": audit.next_ticket,
    }])
    write_csv(paths["ticket_plan_csv"], ["story_id", "topic", "goal", "scope", "code_change_readiness", "exit_condition"], [
        {"story_id": plan.story_id, "topic": plan.topic, "goal": plan.goal, "scope": audit.cluster, "code_change_readiness": "blocked-until-proof", "exit_condition": "artifact published or terminal proof blocker recorded"}
        for plan in audit.ticket_plan
    ])
    md = [
        "# RE-133 — Gameplay mixed proof-first audit", "",
        f"Domain: `{audit.domain_id}`", f"Cluster: `{audit.cluster}`", f"Pivot: `{audit.pivot}`", f"Readiness: `{audit.readiness}`", "",
        "## Progress tracker", "", "- [x] RE-132 gameflow-runtime-control exhaustion consumed.", "- [x] RE-061 gameplay-mixed rows selected.", "- [x] Metadata-only readiness checked.", "- [x] RE-134..RE-140 ticket plan emitted.", "",
        "## Findings", "",
    ]
    for row in audit.rows:
        md.append(f"- `{row.function}` — `{row.implementation_status}`; readiness `{row.readiness}`; blocker `{row.blocker}`")
    md.extend(["", "No production source or marker change is authorized by this audit."])
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text("\n".join(md) + "\n", encoding="utf-8")
    story = [
        "# RE-133 — Gameplay mixed proof-first audit", "", "Status: Done", "", "## Goal", "", "Open `gameplay-mixed` after the RE-132 gameflow exhaustion handoff as a metadata-only proof-first audit.", "", "## Progress tracker", "", "- [x] RE-132 gameflow-runtime-control exhaustion consumed.", "- [x] RE-061 gameplay-mixed rows selected.", "- [x] Load_and_Init_Cutseq gameplay pivot selected.", "- [x] Readiness and blockers recorded.", "- [x] RE-134..RE-140 ticket plan emitted.", "", "## Readiness decision", "", "- decision: `proof-first-audit-blocked`", "- code change readiness: `blocked`", "- next ticket: `RE-134`", "", "## Validation", "", "- `python3 -m pytest tests/reverse/test_re133_gameplay_mixed_audit.py -q`", "- `python3 -m pytest tests/reverse -q`", "- metadata-only guard over RE-133 artifacts", "",
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
    audit = build_gameplay_mixed_audit(args.repo)
    for key, path in write_all_artifacts(audit, args.repo).items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
