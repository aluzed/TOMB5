#!/usr/bin/env python3
"""Generate RE-093 dynamic-light-control proof-first audit artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

RE092_HANDOFF = "docs/reverse/generated/re092-object-runtime-handoff.csv"
RE085_AUDIT = "docs/reverse/generated/re085-object-runtime-control-proof-first-audit.csv"
AUDIT_CSV = "docs/reverse/generated/re093-dynamic-light-control-proof-first-audit.csv"
SUBCLUSTERS_CSV = "docs/reverse/generated/re093-dynamic-light-control-subclusters.csv"
TICKET_PLAN_CSV = "docs/reverse/generated/re093-dynamic-light-control-ticket-plan.csv"
MD_OUTPUT = "docs/reverse/functions/re093-dynamic-light-control-proof-first-audit.md"
STORY_OUTPUT = "docs/stories/RE-093-dynamic-light-control-proof-first-audit.md"
FORBIDDEN = ("0x", "payload", "opcode", "machine word", "raw call target")


@dataclass(frozen=True)
class AuditRow:
    function: str
    file: str
    line: int
    implementation_status: str
    object_family: str
    subcluster: str
    role: str
    readiness: str
    code_change_ready: str
    marker_ready: str
    blocker: str
    next_probe: str


@dataclass(frozen=True)
class DynamicLightAudit:
    story_id: str
    domain_id: str
    cluster: str
    subcluster: str
    pivot: str
    readiness: str
    code_change_ready_count: int
    marker_ready_count: int
    next_ticket: str
    rows: tuple[AuditRow, ...]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def implementation_status(repo: Path, file_name: str, function: str) -> str:
    text = (repo / file_name).read_text(encoding="utf-8", errors="ignore")
    marker = f"void {function}("
    start = text.find(marker)
    if start < 0:
        return "missing-source"
    next_func = text.find("\nvoid ", start + len(marker))
    body = text[start: next_func if next_func > start else len(text)]
    return "unimplemented-stub" if "UNIMPLEMENTED" in body else "implemented-source"


def build_dynamic_light_audit(repo: Path) -> DynamicLightAudit:
    repo = Path(repo)
    handoff = read_csv(repo / RE092_HANDOFF)[0]
    if handoff["next_ticket"] != "RE-093" or handoff["next_subcluster"] != "dynamic-light-control":
        raise ValueError("RE-092 handoff no longer points to RE-093 dynamic-light-control")
    audit_rows = [row for row in read_csv(repo / RE085_AUDIT) if row["subcluster"] == "dynamic-light-control"]
    order = {"ControlElectricalLight": 0, "ControlStrobeLight": 1}
    audit_rows.sort(key=lambda row: (order.get(row["function"], 99), row["function"]))
    rows = []
    for row in audit_rows:
        function = row["function"]
        rows.append(
            AuditRow(
                function=function,
                file=row["file"],
                line=int(row["line"]),
                implementation_status=implementation_status(repo, row["file"], function),
                object_family=row["object_family"],
                subcluster="dynamic-light-control",
                role="pivot-dynamic-light-control" if function == "ControlElectricalLight" else "strobe-light-control-support",
                readiness="proof-first-audit-needed",
                code_change_ready="no",
                marker_ready="no",
                blocker="dynamic light object state contract and symbolic equivalence proof missing",
                next_probe="RE-094 dynamic light caller and side-effect map",
            )
        )
    return DynamicLightAudit(
        story_id="RE-093",
        domain_id="module-game",
        cluster="gameflow-runtime-control",
        subcluster="dynamic-light-control",
        pivot="ControlElectricalLight",
        readiness="blocked",
        code_change_ready_count=0,
        marker_ready_count=0,
        next_ticket="RE-094",
        rows=tuple(rows),
    )


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow({field: row.get(field, "") for field in fields})


def assert_clean(path: Path) -> None:
    text = path.read_text(encoding="utf-8").lower()
    hits = [x for x in FORBIDDEN if x in text]
    if hits:
        raise ValueError(f"forbidden metadata fragments in {path}: {hits}")


def write_all_artifacts(audit: DynamicLightAudit, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "audit_csv": repo / AUDIT_CSV,
        "subclusters_csv": repo / SUBCLUSTERS_CSV,
        "ticket_plan_csv": repo / TICKET_PLAN_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY_OUTPUT,
    }
    write_csv(paths["audit_csv"], list(AuditRow.__dataclass_fields__), [row.__dict__ for row in audit.rows])
    write_csv(paths["subclusters_csv"], ["subcluster", "candidate_count", "top_function", "representative_functions", "object_family", "readiness", "blocker", "recommended_next_ticket"], [{
        "subcluster": audit.subcluster,
        "candidate_count": len(audit.rows),
        "top_function": audit.pivot,
        "representative_functions": ";".join(row.function for row in audit.rows),
        "object_family": "dynamic-light-object-state",
        "readiness": "best-initial-proof-subcluster",
        "blocker": "dynamic light object state contract and symbolic equivalence proof missing",
        "recommended_next_ticket": audit.next_ticket,
    }])
    plan = [
        ("RE-094", "dynamic-light-caller-side-effect-map", "Map ControlElectricalLight/ControlStrobeLight callers, callees, light globals, and side-effect surfaces."),
        ("RE-095", "dynamic-light-argument-state-taxonomy", "Classify item, trigger flag, light color, room, and dynamic-light write dependencies."),
        ("RE-096", "dynamic-light-comparison-gate", "Decide whether symbolic source/binary evidence admits source or marker changes."),
        ("RE-097", "dynamic-light-reconstruction-plan", "Convert ready rows into a minimal reconstruction plan or keep documentation-only blocker."),
        ("RE-098", "dynamic-light-source-patch-gate", "Apply safe patch only if rows are proof-ready; otherwise publish denial gate."),
        ("RE-099", "dynamic-light-validation-regression", "Record tests, metadata guards, and regression validation."),
        ("RE-100", "dynamic-light-closure-or-handoff", "Close dynamic-light-control or hand off to the next object runtime subcluster."),
    ]
    write_csv(paths["ticket_plan_csv"], ["story_id", "topic", "goal", "scope", "code_change_readiness", "exit_condition"], [
        {"story_id": sid, "topic": topic, "goal": goal, "scope": audit.subcluster, "code_change_readiness": "blocked-until-proof", "exit_condition": "artifact published or terminal proof blocker recorded"}
        for sid, topic, goal in plan
    ])
    md = [
        "# RE-093 — Dynamic light control proof-first audit", "",
        f"Domain: `{audit.domain_id}`", f"Cluster: `{audit.cluster}`", f"Subcluster: `{audit.subcluster}`", f"Pivot: `{audit.pivot}`", f"Readiness: `{audit.readiness}`", "",
        "## Progress tracker", "", "- [x] RE-092 handoff consumed.", "- [x] RE-085 dynamic-light rows selected.", "- [x] Metadata-only readiness checked.", "- [x] RE-094..RE-100 ticket plan emitted.", "",
        "## Findings", "",
    ]
    for row in audit.rows:
        md.append(f"- `{row.function}` — `{row.implementation_status}`; readiness `{row.readiness}`; blocker `{row.blocker}`")
    md.extend(["", "No production source or marker change is authorized by this audit."])
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text("\n".join(md) + "\n", encoding="utf-8")
    story = [
        "# RE-093 — Dynamic light control proof-first audit", "", "Status: Done", "", "## Goal", "", "Open `dynamic-light-control` from the RE-092 handoff as a metadata-only proof-first audit.", "", "## Progress tracker", "", "- [x] Upstream handoff verified.", "- [x] Pivot and sibling controls selected.", "- [x] Readiness and blockers recorded.", "- [x] Follow-up ticket plan published.", "", "## Readiness decision", "", "- decision: `proof-first-audit-blocked`", "- code change readiness: `blocked`", "- next ticket: `RE-094`", "", "## Validation", "", "- `python3 -m pytest tests/reverse/test_re093_dynamic_light_audit.py -q`", "- `python3 -m pytest tests/reverse -q`", "- metadata-only guard over RE-093 artifacts", "",
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
    audit = build_dynamic_light_audit(args.repo)
    for key, path in write_all_artifacts(audit, args.repo).items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
