#!/usr/bin/env python3
"""Generate RE-117 lara-runtime-control proof-first audit artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

RE116_HANDOFF = "docs/reverse/generated/re116-scripted-runtime-handoff.csv"
RE077_AUDIT = "docs/reverse/generated/re077-gameflow-runtime-proof-first-audit.csv"
AUDIT_CSV = "docs/reverse/generated/re117-lara-runtime-control-proof-first-audit.csv"
SUBCLUSTERS_CSV = "docs/reverse/generated/re117-lara-runtime-control-subclusters.csv"
TICKET_PLAN_CSV = "docs/reverse/generated/re117-lara-runtime-control-ticket-plan.csv"
MD_OUTPUT = "docs/reverse/functions/re117-lara-runtime-control-proof-first-audit.md"
STORY_OUTPUT = "docs/stories/RE-117-lara-runtime-control-proof-first-audit.md"
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
class TicketPlanRow:
    story_id: str
    topic: str
    goal: str


@dataclass(frozen=True)
class LaraRuntimeAudit:
    story_id: str
    upstream_ticket: str
    domain_id: str
    cluster: str
    subcluster: str
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


def implementation_status(repo: Path, file_name: str, function: str) -> str:
    text = (repo / file_name).read_text(encoding="utf-8", errors="ignore")
    marker = f"void {function}("
    start = text.find(marker)
    if start < 0:
        return "missing-source"
    next_func = text.find("\nvoid ", start + len(marker))
    body = text[start: next_func if next_func > start else len(text)]
    return "unimplemented-stub" if "UNIMPLEMENTED" in body else "implemented-source"


def build_ticket_plan() -> tuple[TicketPlanRow, ...]:
    plans = [
        ("RE-118", "lara-runtime-caller-side-effect-map", "Map LaraControl callers, callees, Lara globals, item state, water/movement state, and side-effect surfaces."),
        ("RE-119", "lara-runtime-argument-state-taxonomy", "Classify LaraControl argument shape, Lara state, item state, room/water state, and animation side effects."),
        ("RE-120", "lara-runtime-comparison-gate", "Define symbolic comparison requirements without raw binary evidence."),
        ("RE-121", "lara-runtime-reconstruction-plan", "Convert ready rows into a minimal reconstruction plan or keep documentation-only blocker."),
        ("RE-122", "lara-runtime-source-patch-gate", "Apply safe patch only if rows are proof-ready; otherwise publish denial gate."),
        ("RE-123", "lara-runtime-validation-regression", "Record tests, metadata guards, and regression validation."),
        ("RE-124", "lara-runtime-closure-or-handoff", "Close lara-runtime-control or hand off to the next gameflow runtime subcluster."),
    ]
    return tuple(TicketPlanRow(*row) for row in plans)


def build_lara_runtime_audit(repo: Path) -> LaraRuntimeAudit:
    repo = Path(repo)
    handoff = read_csv(repo / RE116_HANDOFF)[0]
    if handoff["next_ticket"] != "RE-117" or handoff["next_subcluster"] != "lara-runtime-control":
        raise ValueError("RE-116 handoff no longer points to RE-117 lara-runtime-control")
    audit_rows = [row for row in read_csv(repo / RE077_AUDIT) if row["subcluster"] == "lara-runtime-control"]
    order = {"LaraControl": 0}
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
                object_family="lara-runtime-state",
                subcluster="lara-runtime-control",
                role="pivot-lara-runtime-control" if function == "LaraControl" else "lara-runtime-support",
                readiness="proof-first-audit-needed",
                code_change_ready="no",
                marker_ready="no",
                blocker="Lara runtime state contract and symbolic equivalence proof missing",
                next_probe="RE-118 Lara runtime caller and side-effect map",
            )
        )
    return LaraRuntimeAudit(
        story_id="RE-117",
        upstream_ticket="RE-116",
        domain_id="module-game",
        cluster="gameflow-runtime-control",
        subcluster="lara-runtime-control",
        pivot="LaraControl",
        readiness="blocked",
        code_change_ready_count=0,
        marker_ready_count=0,
        next_ticket="RE-118",
        rows=tuple(rows),
        ticket_plan=build_ticket_plan(),
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


def write_all_artifacts(audit: LaraRuntimeAudit, repo: Path) -> dict[str, Path]:
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
        "object_family": "lara-runtime-state",
        "readiness": "best-initial-proof-subcluster",
        "blocker": "Lara runtime state contract and symbolic equivalence proof missing",
        "recommended_next_ticket": audit.next_ticket,
    }])
    write_csv(paths["ticket_plan_csv"], ["story_id", "topic", "goal", "scope", "code_change_readiness", "exit_condition"], [
        {"story_id": plan.story_id, "topic": plan.topic, "goal": plan.goal, "scope": audit.subcluster, "code_change_readiness": "blocked-until-proof", "exit_condition": "artifact published or terminal proof blocker recorded"}
        for plan in audit.ticket_plan
    ])
    md = [
        "# RE-117 — Lara runtime control proof-first audit", "",
        f"Domain: `{audit.domain_id}`", f"Cluster: `{audit.cluster}`", f"Subcluster: `{audit.subcluster}`", f"Pivot: `{audit.pivot}`", f"Readiness: `{audit.readiness}`", "",
        "## Progress tracker", "", "- [x] RE-116 handoff consumed.", "- [x] RE-077 lara-runtime rows selected.", "- [x] Metadata-only readiness checked.", "- [x] RE-118..RE-124 ticket plan emitted.", "",
        "## Findings", "",
    ]
    for row in audit.rows:
        md.append(f"- `{row.function}` — `{row.implementation_status}`; readiness `{row.readiness}`; blocker `{row.blocker}`")
    md.extend(["", "No production source or marker change is authorized by this audit."])
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text("\n".join(md) + "\n", encoding="utf-8")
    story = [
        "# RE-117 — Lara runtime control proof-first audit", "", "Status: Done", "", "## Goal", "", "Open `lara-runtime-control` after the RE-116 scripted-runtime handoff as a metadata-only proof-first audit.", "", "## Progress tracker", "", "- [x] RE-116 handoff consumed.", "- [x] Lara runtime pivot selected.", "- [x] Readiness and blockers recorded.", "- [x] Follow-up ticket plan published.", "", "## Readiness decision", "", "- decision: `proof-first-audit-blocked`", "- code change readiness: `blocked`", "- next ticket: `RE-118`", "", "## Validation", "", "- `python3 -m pytest tests/reverse/test_re117_lara_runtime_audit.py -q`", "- `python3 -m pytest tests/reverse -q`", "- metadata-only guard over RE-117 artifacts", "",
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
    audit = build_lara_runtime_audit(args.repo)
    for key, path in write_all_artifacts(audit, args.repo).items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
