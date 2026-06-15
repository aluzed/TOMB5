#!/usr/bin/env python3
"""Generate RE-085 object runtime control proof-first audit artifacts."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


RE084_HANDOFF_CSV = "docs/reverse/generated/re084-gameflow-runtime-handoff.csv"
RE077_AUDIT_CSV = "docs/reverse/generated/re077-gameflow-runtime-proof-first-audit.csv"
AUDIT_CSV = "docs/reverse/generated/re085-object-runtime-control-proof-first-audit.csv"
SUBCLUSTER_CSV = "docs/reverse/generated/re085-object-runtime-control-subclusters.csv"
PLAN_CSV = "docs/reverse/generated/re085-object-runtime-control-ticket-plan.csv"
MD_OUTPUT = "docs/reverse/functions/re085-object-runtime-control-proof-first-audit.md"
STORY_OUTPUT = "docs/stories/RE-085-object-runtime-control-proof-first-audit.md"
C_KEYWORD_ARTIFACTS = {"if", "for", "while", "switch", "else", "do"}
FORBIDDEN_FRAGMENTS = ("0x", "payload", "opcode", "machine word", "raw call target")


@dataclass(frozen=True)
class AuditSummary:
    candidate_count: int
    nd_count: int
    runtime_count: int
    subcluster_count: int
    selected_subcluster: str
    patch_ready_count: int
    marker_ready_count: int


@dataclass(frozen=True)
class Candidate:
    function: str
    file: str
    line: int
    status: str
    markers: str
    bucket: str
    score: int
    caller_count: int
    callee_count: int
    object_family: str
    subcluster: str
    role: str
    readiness: str
    code_change_ready: str
    marker_ready: str
    blocker: str
    next_probe: str


@dataclass(frozen=True)
class Subcluster:
    subcluster: str
    candidate_count: int
    top_function: str
    representative_functions: tuple[str, ...]
    object_family: str
    readiness: str
    blocker: str
    recommended_next_ticket: str


@dataclass(frozen=True)
class TicketPlanItem:
    story_id: str
    topic: str
    goal: str
    scope: str
    code_change_readiness: str
    exit_condition: str


@dataclass(frozen=True)
class ObjectRuntimeControlAudit:
    story_id: str
    domain_id: str
    cluster: str
    subcluster: str
    pivot_function: str
    status: str
    depends_on: tuple[str, ...]
    decision: str
    code_change_readiness: str
    next_ticket: str
    progress: tuple[str, ...]
    summary: AuditSummary
    candidates: tuple[Candidate, ...]
    subclusters: tuple[Subcluster, ...]
    ticket_plan: tuple[TicketPlanItem, ...]


def parse_int(text: str | None) -> int:
    try:
        return int(text or "0")
    except ValueError:
        return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def verify_handoff(repo: Path) -> None:
    rows = read_csv(repo / RE084_HANDOFF_CSV)
    if not rows or rows[0].get("next_ticket") != "RE-085":
        raise ValueError("RE-084 handoff to RE-085 is missing")
    if rows[0].get("next_cluster") != "object-runtime-control":
        raise ValueError("RE-084 handoff is no longer object-runtime-control")


def object_subcluster_for(function: str, file: str) -> tuple[str, str]:
    haystack = f"{file} {function}".upper()
    if "FLMTORCH" in haystack or "LARAFLAR" in haystack or "FLARE" in haystack or "TORCH" in haystack:
        return "torch-and-flare-control", "fire-and-flare-object-state"
    if "OBJLIGHT" in haystack or "LIGHT" in haystack:
        return "dynamic-light-control", "dynamic-light-object-state"
    if "PICKUP" in haystack or "SEARCH" in haystack:
        return "pickup-search-control", "pickup-query-object-state"
    return "object-control-mixed", "mixed-object-runtime-state"


def role_for(function: str) -> str:
    if function == "FlameTorchControl":
        return "pivot-object-control"
    if "Light" in function:
        return "light-control-support"
    if "Flare" in function:
        return "flare-control-support"
    if "Search" in function:
        return "pickup-search-support"
    return "object-control-support"


def readiness_for(function: str, subcluster: str) -> tuple[str, str, str]:
    if function == "FlameTorchControl":
        return (
            "proof-first-audit-needed",
            "top object runtime candidate but object state and equivalence proof are not established",
            "RE-086 object runtime caller and side-effect map",
        )
    return (
        "subcluster-proof-needed",
        f"{subcluster} needs object state contract and equivalence proof before source or marker changes",
        "include in RE-086/RE-087 object runtime proof map",
    )


def build_candidates(repo: Path) -> list[Candidate]:
    rows: list[Candidate] = []
    for row in read_csv(repo / RE077_AUDIT_CSV):
        if row.get("subcluster") != "object-runtime-control":
            continue
        function = row.get("function", "")
        if function in C_KEYWORD_ARTIFACTS:
            continue
        subcluster, family = object_subcluster_for(function, row.get("file", ""))
        readiness, blocker, next_probe = readiness_for(function, subcluster)
        rows.append(
            Candidate(
                function=function,
                file=row.get("file", ""),
                line=parse_int(row.get("line")),
                status=row.get("status", ""),
                markers=row.get("markers", "") or "none",
                bucket=row.get("bucket", ""),
                score=parse_int(row.get("score")),
                caller_count=parse_int(row.get("caller_count")),
                callee_count=parse_int(row.get("callee_count")),
                object_family=family,
                subcluster=subcluster,
                role=role_for(function),
                readiness=readiness,
                code_change_ready="no",
                marker_ready="no",
                blocker=blocker,
                next_probe=next_probe,
            )
        )
    priority = {
        "FlameTorchControl": 0,
        "SearchObjectControl": 1,
        "ControlElectricalLight": 2,
        "FlareControl": 3,
        "ControlStrobeLight": 4,
    }
    rows.sort(key=lambda item: (priority.get(item.function, 99), -item.score, item.file, item.line, item.function))
    return rows


def build_subclusters(candidates: list[Candidate]) -> list[Subcluster]:
    grouped: dict[str, list[Candidate]] = defaultdict(list)
    for row in candidates:
        grouped[row.subcluster].append(row)
    output: list[Subcluster] = []
    for subcluster, rows in grouped.items():
        rows.sort(key=lambda item: (0 if item.function == "FlameTorchControl" else 1, -item.score, item.function))
        readiness = "proof-needed"
        blocker = "object control subcluster needs source state contract and equivalence proof"
        next_ticket = "defer"
        if subcluster == "torch-and-flare-control":
            readiness = "best-initial-proof-subcluster"
            blocker = "FlameTorchControl/FlareControl need object state, caller, and equivalence proof before source or marker changes"
            next_ticket = "RE-086"
        output.append(
            Subcluster(
                subcluster=subcluster,
                candidate_count=len(rows),
                top_function=rows[0].function,
                representative_functions=tuple(row.function for row in rows),
                object_family=rows[0].object_family,
                readiness=readiness,
                blocker=blocker,
                recommended_next_ticket=next_ticket,
            )
        )
    order = {"torch-and-flare-control": 0, "pickup-search-control": 1, "dynamic-light-control": 2}
    output.sort(key=lambda item: (order.get(item.subcluster, 99), -item.candidate_count, item.subcluster))
    return output


def build_ticket_plan() -> tuple[TicketPlanItem, ...]:
    specs = (
        ("RE-086", "object-runtime-caller-side-effect-map", "Map FlameTorchControl/FlareControl and sibling object runtime callers, callees, object globals, and side-effect surfaces.", "torch-and-flare-control initial subcluster", "blocked-until-proof", "caller/side-effect matrix published or terminal proof blocker recorded"),
        ("RE-087", "object-runtime-argument-state-taxonomy", "Classify object runtime arguments, item/object state dependencies, animation/light/fire state transitions, and write targets.", "selected object runtime source contract", "blocked-until-proof", "taxonomy separates source-backed object state from candidate-only state"),
        ("RE-088", "object-runtime-comparison-gate", "Decide whether symbolic binary/source equivalence evidence is sufficient for any source or marker change.", "comparison readiness gate", "blocked-until-proof", "patch-ready rows identified or explicit no-patch blocker published"),
        ("RE-089", "object-runtime-reconstruction-plan", "Convert ready rows into a minimal reconstruction plan with tests, guards, and rollback boundaries.", "only rows admitted by RE-088", "blocked-until-proof", "source patch plan exists or chain remains documentation-only"),
        ("RE-090", "object-runtime-source-patch-gate", "Apply the smallest safe source or marker patch only if RE-088/RE-089 made rows patch-ready; otherwise publish denial gate.", "conditional source patch gate", "blocked-until-proof", "patch validated or no-source-change decision recorded"),
        ("RE-091", "object-runtime-validation-regression", "Run build/tests/guards for the selected object runtime subcluster and record validation status.", "validation and regression evidence", "blocked-until-proof", "validation log published with pass/fail and remaining blockers"),
        ("RE-092", "object-runtime-closure-or-handoff", "Close the object runtime subcluster or hand off to the next runtime control subcluster with a refreshed plan.", "closure and reprioritization", "blocked-until-proof", "subcluster closure, handoff, or terminal blocker recorded"),
    )
    return tuple(TicketPlanItem(*spec) for spec in specs)


def build_object_runtime_control_audit(repo: Path) -> ObjectRuntimeControlAudit:
    repo = Path(repo)
    verify_handoff(repo)
    candidates = tuple(build_candidates(repo))
    subclusters = tuple(build_subclusters(list(candidates)))
    summary = AuditSummary(
        candidate_count=len(candidates),
        nd_count=0,
        runtime_count=sum(1 for row in candidates if row.role.endswith("support")),
        subcluster_count=len(subclusters),
        selected_subcluster="object-runtime-control",
        patch_ready_count=0,
        marker_ready_count=0,
    )
    return ObjectRuntimeControlAudit(
        story_id="RE-085",
        domain_id="module-game",
        cluster="gameflow-runtime-control",
        subcluster="object-runtime-control",
        pivot_function="FlameTorchControl",
        status="proof-first-audit-published",
        depends_on=("RE-077", "RE-078..RE-084"),
        decision="object-runtime-control-proof-needed",
        code_change_readiness="blocked",
        next_ticket="RE-086",
        progress=(
            "RE-084 handoff consumed.",
            "RE-077 object runtime candidates filtered.",
            "Object runtime subclusters classified.",
            "RE-086..RE-092 follow-up plan emitted.",
            "Forbidden evidence excluded from generated artifacts.",
        ),
        summary=summary,
        candidates=candidates,
        subclusters=subclusters,
        ticket_plan=build_ticket_plan(),
    )


def write_dict_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def assert_metadata_only(path: Path) -> None:
    text = path.read_text(encoding="utf-8").lower()
    hits = [fragment for fragment in FORBIDDEN_FRAGMENTS if fragment in text]
    if hits:
        raise ValueError(f"forbidden evidence fragments in {path}: {hits}")


def write_audit_csv(path: Path, audit: ObjectRuntimeControlAudit) -> None:
    fields = ["function", "file", "line", "status", "markers", "bucket", "score", "caller_count", "callee_count", "object_family", "subcluster", "role", "readiness", "code_change_ready", "marker_ready", "blocker", "next_probe"]
    write_dict_csv(path, fields, [row.__dict__ for row in audit.candidates])


def write_subcluster_csv(path: Path, audit: ObjectRuntimeControlAudit) -> None:
    fields = ["subcluster", "candidate_count", "top_function", "representative_functions", "object_family", "readiness", "blocker", "recommended_next_ticket"]
    write_dict_csv(path, fields, [{**row.__dict__, "representative_functions": ";".join(row.representative_functions)} for row in audit.subclusters])


def write_plan_csv(path: Path, audit: ObjectRuntimeControlAudit) -> None:
    fields = ["story_id", "topic", "goal", "scope", "code_change_readiness", "exit_condition"]
    write_dict_csv(path, fields, [row.__dict__ for row in audit.ticket_plan])


def write_markdown(path: Path, audit: ObjectRuntimeControlAudit) -> None:
    lines = [
        "# RE-085 — Object runtime control proof-first audit",
        "",
        f"Domain: `{audit.domain_id}`",
        f"Cluster: `{audit.cluster}`",
        f"Subcluster: `{audit.subcluster}`",
        f"Pivot: `{audit.pivot_function}`",
        f"Status: `{audit.status}`",
        f"Decision: `{audit.decision}`",
        f"Next ticket: `{audit.next_ticket}`",
        "",
        "## Progress tracker",
        "",
    ]
    for item in audit.progress:
        lines.append(f"- [x] {item}")
    lines.extend([
        "",
        "## Summary",
        "",
        f"- candidates: `{audit.summary.candidate_count}`",
        f"- ND candidates: `{audit.summary.nd_count}`",
        f"- subclusters: `{audit.summary.subcluster_count}`",
        f"- code-change-ready rows: `{audit.summary.patch_ready_count}`",
        f"- marker-ready rows: `{audit.summary.marker_ready_count}`",
        "",
        "## Candidates",
        "",
    ])
    for row in audit.candidates:
        lines.append(f"- `{row.function}` — `{row.subcluster}` / `{row.role}` / readiness `{row.readiness}` / blocker `{row.blocker}`")
    lines.extend(["", "## Follow-up plan", ""])
    for item in audit.ticket_plan:
        lines.append(f"- `{item.story_id}` — `{item.topic}` — `{item.code_change_readiness}`")
    lines.extend([
        "",
        "## Readiness decision",
        "",
        f"- decision: `{audit.decision}`",
        f"- code change readiness: `{audit.code_change_readiness}`",
        f"- next ticket: `{audit.next_ticket}`",
        "",
        "Do not patch production source or add/remove proof markers from this story alone.",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_story(path: Path, audit: ObjectRuntimeControlAudit) -> None:
    lines = [
        "# RE-085 — Object runtime control proof-first audit",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Open the object runtime control proof chain from the RE-084 handoff and select a bounded follow-up plan.",
        "",
        "## Progress tracker",
        "",
    ]
    for item in audit.progress:
        lines.append(f"- [x] {item}")
    lines.extend([
        "",
        "## Generated artifacts",
        "",
        f"- `{AUDIT_CSV}`",
        f"- `{SUBCLUSTER_CSV}`",
        f"- `{PLAN_CSV}`",
        f"- `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- selected pivot: `{audit.pivot_function}`",
        f"- candidate count: `{audit.summary.candidate_count}`",
        "- object runtime source-level metadata is available, but source and marker edits remain blocked until proof closes.",
        "",
        "## Readiness decision",
        "",
        f"- decision: `{audit.decision}`",
        f"- code change readiness: `{audit.code_change_readiness}`",
        f"- next ticket: `{audit.next_ticket}`",
        "",
        "## Follow-up tickets",
        "",
    ])
    for item in audit.ticket_plan:
        lines.append(f"- `{item.story_id}` — `{item.topic}`: {item.goal}")
    lines.extend([
        "",
        "## Validation",
        "",
        "- `python3 -m pytest tests/reverse/test_re085_object_runtime_control_audit.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over generated RE-085 artifacts",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_all_artifacts(audit: ObjectRuntimeControlAudit, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "audit_csv": repo / AUDIT_CSV,
        "subcluster_csv": repo / SUBCLUSTER_CSV,
        "plan_csv": repo / PLAN_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY_OUTPUT,
    }
    write_audit_csv(paths["audit_csv"], audit)
    write_subcluster_csv(paths["subcluster_csv"], audit)
    write_plan_csv(paths["plan_csv"], audit)
    write_markdown(paths["md"], audit)
    write_story(paths["story"], audit)
    for path in paths.values():
        assert_metadata_only(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    audit = build_object_runtime_control_audit(args.repo)
    for key, path in write_all_artifacts(audit, args.repo).items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
