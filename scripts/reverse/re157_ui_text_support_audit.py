#!/usr/bin/env python3
"""Generate RE-157 ui-text-support proof-first audit artifacts."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path

RE156_HANDOFF = "docs/reverse/generated/re156-item-lighting-interaction-handoff.csv"
RE061_AUDIT = "docs/reverse/generated/re061-module-game-proof-first-audit.csv"
RE061_CLUSTERS = "docs/reverse/generated/re061-module-game-clusters.csv"
AUDIT_CSV = "docs/reverse/generated/re157-ui-text-support-proof-first-audit.csv"
CLUSTERS_CSV = "docs/reverse/generated/re157-ui-text-support-clusters.csv"
TICKET_PLAN_CSV = "docs/reverse/generated/re157-ui-text-support-ticket-plan.csv"
MD_OUTPUT = "docs/reverse/functions/re157-ui-text-support-proof-first-audit.md"
STORY_OUTPUT = "docs/stories/RE-157-ui-text-support-proof-first-audit.md"
FORBIDDEN = ("0x", "payload", "opcode", "machine word", "raw call target")
CLOSED_CLUSTERS = {
    "debris-object-breakage",
    "lara-movement-support",
    "gameflow-runtime-control",
    "gameplay-mixed",
    "object-interaction",
    "item-lighting-interaction",
}
EXPECTED_FUNCTIONS = ("InitFont",)


@dataclass(frozen=True)
class AuditRow:
    function: str
    file: str
    line: int
    implementation_status: str
    marker_status: str
    text_family: str
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
class UiTextSupportAudit:
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
        ("RE-158", "ui-text-support-caller-side-effect-map", "Map InitFont callers, marker status, and text/font state surfaces."),
        ("RE-159", "ui-text-support-argument-state-taxonomy", "Classify InitFont arguments, global font shade state, and marker proof needs."),
        ("RE-160", "ui-text-support-comparison-gate", "Decide whether InitFont has enough non-raw equivalence proof for marker or source changes."),
        ("RE-161", "ui-text-support-closure-or-handoff", "Close ui-text-support or hand off to the next module-game backlog domain."),
    ]
    return tuple(TicketPlanRow(story_id=sid, topic=topic, goal=goal) for sid, topic, goal in plans)


def verify_upstream(repo: Path) -> None:
    handoff = read_csv(repo / RE156_HANDOFF)[0]
    if handoff["next_ticket"] != "RE-157" or handoff["next_cluster"] != "ui-text-support" or handoff.get("pivot") != "InitFont":
        raise ValueError("RE-156 handoff no longer selects RE-157 ui-text-support / InitFont")
    rows = read_csv(repo / RE061_CLUSTERS)
    remaining = [row for row in rows if row["cluster"] not in CLOSED_CLUSTERS]
    if not remaining or remaining[0]["cluster"] != "ui-text-support" or remaining[0]["top_function"] != "InitFont":
        raise ValueError("RE-061 module-game cluster ordering no longer selects ui-text-support after closed clusters")


def build_ui_text_support_audit(repo: Path) -> UiTextSupportAudit:
    repo = Path(repo)
    verify_upstream(repo)
    audit_rows = [row for row in read_csv(repo / RE061_AUDIT) if row["cluster"] == "ui-text-support"]
    audit_rows.sort(key=lambda row: row["function"])
    selected = tuple(row["function"] for row in audit_rows)
    if selected != EXPECTED_FUNCTIONS:
        raise ValueError(f"RE-157 ui-text-support scope drifted: {selected}")
    rows: list[AuditRow] = []
    for row in audit_rows:
        function = row["function"]
        markers = row.get("markers", "none")
        if markers != "D;F;ND" or row.get("nd") != "yes":
            raise ValueError(f"RE-157 expected InitFont to remain an ND marker audit row: {row}")
        rows.append(AuditRow(
            function=function,
            file=row["file"],
            line=int(row["line"]),
            implementation_status=implementation_status(repo, row["file"], function),
            marker_status=markers,
            text_family="font-shade-initialization",
            cluster="ui-text-support",
            role="pivot-ui-text-support",
            readiness="nd-marker-proof-needed",
            code_change_ready="no",
            marker_ready="no",
            blocker="InitFont ND marker needs behavior proof before marker or source changes",
            next_probe="RE-158 UI text caller and side-effect map",
        ))
    return UiTextSupportAudit(
        story_id="RE-157",
        upstream_ticket="RE-156",
        domain_id="module-game",
        cluster="ui-text-support",
        pivot="InitFont",
        readiness="blocked",
        code_change_ready_count=0,
        marker_ready_count=0,
        next_ticket="RE-158",
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


def write_all_artifacts(audit: UiTextSupportAudit, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "audit_csv": repo / AUDIT_CSV,
        "clusters_csv": repo / CLUSTERS_CSV,
        "ticket_plan_csv": repo / TICKET_PLAN_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY_OUTPUT,
    }
    write_csv(paths["audit_csv"], list(AuditRow.__dataclass_fields__), [row.__dict__ for row in audit.rows])
    write_csv(paths["clusters_csv"], ["cluster", "candidate_count", "top_function", "representative_functions", "text_family", "readiness", "blocker", "recommended_next_ticket"], [{
        "cluster": audit.cluster,
        "candidate_count": len(audit.rows),
        "top_function": audit.pivot,
        "representative_functions": ";".join(row.function for row in audit.rows),
        "text_family": "font-shade-initialization",
        "readiness": "nd-marker-proof-needed",
        "blocker": "InitFont ND marker needs behavior proof before marker or source changes",
        "recommended_next_ticket": audit.next_ticket,
    }])
    write_csv(paths["ticket_plan_csv"], ["story_id", "topic", "goal", "scope", "code_change_readiness", "exit_condition"], [
        {"story_id": plan.story_id, "topic": plan.topic, "goal": plan.goal, "scope": audit.cluster, "code_change_readiness": "blocked-until-proof", "exit_condition": "artifact published or terminal proof blocker recorded"}
        for plan in audit.ticket_plan
    ])
    md = [
        "# RE-157 — UI text support proof-first audit", "",
        f"Domain: `{audit.domain_id}`", f"Cluster: `{audit.cluster}`", f"Pivot: `{audit.pivot}`", f"Readiness: `{audit.readiness}`", "",
        "## Progress tracker", "", "- [x] RE-156 item-lighting handoff consumed.", "- [x] RE-061 ui-text-support row selected.", "- [x] Metadata-only readiness checked.", "- [x] RE-158..RE-161 ticket plan emitted.", "",
        "## Findings", "",
    ]
    for row in audit.rows:
        md.append(f"- `{row.function}` — `{row.implementation_status}`; marker `{row.marker_status}`; family `{row.text_family}`; readiness `{row.readiness}`; blocker `{row.blocker}`")
    md.extend(["", "No production source or marker change is authorized by this audit."])
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text("\n".join(md) + "\n", encoding="utf-8")

    story = [
        "# RE-157 — UI text support proof-first audit", "", "Status: Done", "", "## Goal", "", "Open `ui-text-support` after the prior module-game handoff as a metadata-only proof-first audit.", "", "## Progress tracker", "", "- [x] RE-156 item-lighting handoff consumed.", "- [x] RE-061 ui-text-support row selected.", "- [x] InitFont UI text pivot selected.", "- [x] Readiness and blockers recorded.", "- [x] RE-158..RE-161 ticket plan emitted.", "", "## Generated artifacts", "", f"- `{AUDIT_CSV}`", f"- `{CLUSTERS_CSV}`", f"- `{TICKET_PLAN_CSV}`", f"- `{MD_OUTPUT}`", "", "## Readiness decision", "", "- decision: `proof-first-audit-blocked`", "- code change readiness: `blocked`", "- marker readiness: `blocked`", "- next ticket: `RE-158`", "- blocker: `InitFont ND marker needs behavior proof before marker or source changes`", "", "## Follow-up ticket breakdown", "",
    ]
    for plan in audit.ticket_plan:
        story.append(f"- `{plan.story_id}` — `{plan.topic}`: {plan.goal}")
    story.extend(["", "## Validation", "", "- `python3 -m pytest tests/reverse/test_re157_ui_text_support_audit.py -q`", "- `python3 -m pytest tests/reverse -q`", "- metadata-only guard over RE-157 artifacts", ""])
    paths["story"].parent.mkdir(parents=True, exist_ok=True)
    paths["story"].write_text("\n".join(story), encoding="utf-8")
    for path in paths.values():
        assert_clean(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    audit = build_ui_text_support_audit(args.repo)
    for key, path in write_all_artifacts(audit, args.repo).items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
