#!/usr/bin/env python3
"""Generate RE-170 module SPEC_PSXPC_N closure-or-handoff artifacts.

This gate consumes the RE-169 next-cluster selection. Because geometry-support
still lacks caller/state and non-raw equivalence proof, the module domain is not
closed and no source or marker changes are authorized. Instead, RE-170 emits a
bounded geometry-support follow-up plan beginning at RE-171.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

UPSTREAM_HANDOFF = "docs/reverse/generated/re169-module-spec-psxpc-n-next-cluster-handoff.csv"
UPSTREAM_SELECTION = "docs/reverse/generated/re169-module-spec-psxpc-n-next-cluster-selection.csv"
SOURCE_AUDIT = "docs/reverse/generated/re163-module-spec-psxpc-n-proof-first-audit.csv"
SOURCE_PLAN = "docs/reverse/generated/re163-module-spec-psxpc-n-ticket-plan.csv"
SCOPE_CSV = "docs/reverse/generated/re170-module-spec-psxpc-n-geometry-support-scope.csv"
PLAN_CSV = "docs/reverse/generated/re170-geometry-support-ticket-plan.csv"
DECISION_CSV = "docs/reverse/generated/re170-module-spec-psxpc-n-closure-or-handoff.csv"
HANDOFF_CSV = "docs/reverse/generated/re170-geometry-support-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re170-module-spec-psxpc-n-closure-or-handoff.md"
STORY_OUTPUT = "docs/stories/RE-170-module-spec-psxpc-n-closure-or-handoff.md"

DOMAIN_ID = "module-spec_psxpc_n"
SELECTED_CLUSTER = "geometry-support"
SELECTED_PIVOT = "GetBoundsAccurate"

FORBIDDEN = (
    "word_le_hex",
    "payload_offset",
    "dump row",
    "opcode",
    "machine word",
    "call_address",
    "branch target",
    "call target",
    "0x",
)

ORDER = (
    "GetBoundsAccurate",
    "CalcClipWindow_ONGTE",
    "InterpolateMatrix_CL",
    "GetFrames_CL",
    "GetBestFrame",
    "GetChange",
    "DecodeTrack",
)


@dataclass(frozen=True)
class ScopeRow:
    function: str
    file: str
    line: int
    cluster: str
    role: str
    source_status: str
    source_marker: str
    prior_score: int
    caller_count: int
    callee_count: int
    code_change_readiness: str
    marker_readiness: str
    source_patch_decision: str
    marker_change_decision: str
    blocker: str
    recommended_first_proof: str


@dataclass(frozen=True)
class TicketPlanItem:
    story_id: str
    topic: str
    goal: str
    scope: str
    code_change_readiness: str
    exit_condition: str


@dataclass(frozen=True)
class ClosureDecisionRow:
    story_id: str
    domain_id: str
    selected_cluster: str
    selected_pivot: str
    domain_decision: str
    code_change_readiness: str
    source_patch_ready_count: int
    marker_ready_count: int
    next_ticket: str
    next_topic: str
    blocker: str


@dataclass(frozen=True)
class HandoffRow:
    next_ticket: str
    next_topic: str
    selected_cluster: str
    selected_pivot: str
    outcome: str
    reason: str
    dependency: str
    stop_condition: str


@dataclass(frozen=True)
class ClosureOrHandoff:
    story_id: str
    upstream_ticket: str
    domain_id: str
    selected_cluster: str
    selected_pivot: str
    domain_decision: str
    code_change_readiness: str
    source_patch_ready_count: int
    marker_ready_count: int
    next_ticket: str
    next_topic: str
    scope_rows: tuple[ScopeRow, ...]
    ticket_plan: tuple[TicketPlanItem, ...]
    decision_row: ClosureDecisionRow
    handoff: HandoffRow


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_int(value: str | None) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def validate_re169_handoff(rows: list[dict[str, str]]) -> dict[str, str]:
    if len(rows) != 1:
        raise ValueError("RE-169 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "next_ticket": "RE-170",
        "next_topic": "module-spec-psxpc-n-closure-or-handoff",
        "selected_cluster": SELECTED_CLUSTER,
        "selected_pivot": SELECTED_PIVOT,
        "outcome": "next-cluster-selected-source-patch-blocked",
        "dependency": "RE-169 next-cluster selection",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-169 handoff drift: expected {key}={value!r}, got {row.get(key)!r}")
    return row


def validate_re169_selection(rows: list[dict[str, str]]) -> None:
    selected = [row for row in rows if row.get("selection_decision") == "selected"]
    if len(selected) != 1:
        raise ValueError("RE-169 selection must contain exactly one selected cluster")
    row = selected[0]
    if row.get("cluster") != SELECTED_CLUSTER or row.get("top_function") != SELECTED_PIVOT:
        raise ValueError("RE-169 selected cluster drifted from geometry-support / GetBoundsAccurate")
    if row.get("code_change_readiness") != "blocked":
        raise ValueError("RE-169 selected cluster unexpectedly became code-change ready")


def validate_re163_plan(rows: list[dict[str, str]]) -> None:
    by_id = {row.get("story_id"): row for row in rows}
    row = by_id.get("RE-170")
    if not row:
        raise ValueError("RE-163 ticket plan does not name RE-170")
    if row.get("topic") != "module-spec-psxpc-n-closure-or-handoff":
        raise ValueError("RE-170 ticket-plan topic drifted")
    if row.get("scope") != "module SPEC_PSXPC_N domain":
        raise ValueError("RE-170 ticket-plan scope drifted")


def build_scope_rows(audit_rows: list[dict[str, str]]) -> tuple[ScopeRow, ...]:
    by_function = {row.get("function", ""): row for row in audit_rows if row.get("cluster") == SELECTED_CLUSTER}
    missing = [function for function in ORDER if function not in by_function]
    extra = sorted(function for function in by_function if function not in ORDER)
    if missing or extra:
        raise ValueError(f"geometry-support scope drift: missing={missing}, extra={extra}")

    rows: list[ScopeRow] = []
    for index, function in enumerate(ORDER):
        row = by_function[function]
        rows.append(
            ScopeRow(
                function=function,
                file=row.get("file", ""),
                line=parse_int(row.get("line")),
                cluster=SELECTED_CLUSTER,
                role="pivot" if function == SELECTED_PIVOT else "supporting-candidate",
                source_status=row.get("status", ""),
                source_marker=row.get("markers", "") or "none",
                prior_score=parse_int(row.get("score")),
                caller_count=parse_int(row.get("caller_count")),
                callee_count=parse_int(row.get("callee_count")),
                code_change_readiness="blocked",
                marker_readiness="blocked",
                source_patch_decision="denied",
                marker_change_decision="denied",
                blocker="missing geometry-support caller/state and non-raw equivalence proof",
                recommended_first_proof=(
                    "geometry-support caller/state inventory"
                    if index == 0
                    else "include in geometry-support scope audit"
                ),
            )
        )
    return tuple(rows)


def build_ticket_plan() -> tuple[TicketPlanItem, ...]:
    rows = (
        (
            "RE-171",
            "geometry-support-proof-first-audit",
            "Open the geometry-support proof chain and publish exact scope, pivot, blockers, and source-backed inventory.",
            "GetBoundsAccurate plus geometry-support rows",
            "proof-first audit emitted with no source or marker changes",
        ),
        (
            "RE-172",
            "geometry-support-caller-state-map",
            "Map source-backed callers, state surfaces, return-value consumers, and helper dependencies for geometry-support rows.",
            "geometry-support source-backed caller and state surfaces",
            "Caller/state map published with no synthetic edges",
        ),
        (
            "RE-173",
            "geometry-support-argument-taxonomy",
            "Classify coordinate, frame, bounds, and track argument families into stable metadata categories.",
            "geometry-support argument families",
            "Taxonomy separates source-backed shapes from unproven runtime assumptions",
        ),
        (
            "RE-174",
            "geometry-support-state-contract",
            "Document structure, matrix, frame, and bounds state contracts required before reconstruction or marker updates.",
            "geometry-support source state and helper contract rows",
            "State contract either unblocks comparison or records exact blockers",
        ),
        (
            "RE-175",
            "geometry-support-equivalence-gate",
            "Compare source-level contract rows against non-raw binary metadata without versioning raw evidence.",
            "geometry-support contract rows",
            "Readiness matrix names ready rows or remains blocked",
        ),
        (
            "RE-176",
            "geometry-support-source-patch-gate",
            "Apply a minimal patch only if RE-175 marks rows ready; otherwise emit a no-patch gate.",
            "patch-ready geometry-support rows only",
            "Patch/build/tests pass or no-patch blocker is published",
        ),
        (
            "RE-177",
            "module-spec-psxpc-n-post-geometry-next-cluster-selection",
            "Select the next SPEC_PSXPC_N cluster after geometry-support closes or blocks.",
            "remaining SPEC_PSXPC_N clusters after geometry-support",
            "Next cluster or domain handoff artifact names the next objective",
        ),
    )
    return tuple(
        TicketPlanItem(
            story_id=story_id,
            topic=topic,
            goal=goal,
            scope=scope,
            code_change_readiness="blocked-until-proof",
            exit_condition=exit_condition,
        )
        for story_id, topic, goal, scope, exit_condition in rows
    )


def build_closure_or_handoff(repo: Path) -> ClosureOrHandoff:
    repo = Path(repo)
    validate_re169_handoff(read_csv(repo / UPSTREAM_HANDOFF))
    validate_re169_selection(read_csv(repo / UPSTREAM_SELECTION))
    validate_re163_plan(read_csv(repo / SOURCE_PLAN))
    scope_rows = build_scope_rows(read_csv(repo / SOURCE_AUDIT))
    ticket_plan = build_ticket_plan()
    decision = ClosureDecisionRow(
        story_id="RE-170",
        domain_id=DOMAIN_ID,
        selected_cluster=SELECTED_CLUSTER,
        selected_pivot=SELECTED_PIVOT,
        domain_decision="module-spec-psxpc-n-not-closed-geometry-support-proof-chain-opened",
        code_change_readiness="documentation-only-handoff-gate",
        source_patch_ready_count=0,
        marker_ready_count=0,
        next_ticket="RE-171",
        next_topic="geometry-support-proof-first-audit",
        blocker="geometry-support needs caller/state and non-raw equivalence proof before source or marker changes",
    )
    handoff = HandoffRow(
        next_ticket=decision.next_ticket,
        next_topic=decision.next_topic,
        selected_cluster=SELECTED_CLUSTER,
        selected_pivot=SELECTED_PIVOT,
        outcome="geometry-support-proof-chain-opened",
        reason="module SPEC_PSXPC_N remains open; geometry-support needs caller/state and non-raw equivalence proof before source or marker changes",
        dependency="RE-170 closure-or-handoff gate",
        stop_condition="geometry-support proof-first audit emitted",
    )
    return ClosureOrHandoff(
        story_id="RE-170",
        upstream_ticket="RE-169",
        domain_id=DOMAIN_ID,
        selected_cluster=SELECTED_CLUSTER,
        selected_pivot=SELECTED_PIVOT,
        domain_decision=decision.domain_decision,
        code_change_readiness=decision.code_change_readiness,
        source_patch_ready_count=0,
        marker_ready_count=0,
        next_ticket=decision.next_ticket,
        next_topic=decision.next_topic,
        scope_rows=scope_rows,
        ticket_plan=ticket_plan,
        decision_row=decision,
        handoff=handoff,
    )


def write_dict_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, gate: ClosureOrHandoff) -> None:
    lines = [
        "# RE-170 module SPEC_PSXPC_N closure or handoff",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-169 geometry-support handoff consumed.",
        "- [x] Geometry-support scope loaded from RE-163 audit rows.",
        "- [x] Domain closure denied because selected cluster still needs proof.",
        "- [x] Bounded RE-171..RE-177 follow-up plan emitted.",
        "- [x] No source or marker changes authorized.",
        "",
        "## Decision",
        "",
        f"- domain: `{gate.domain_id}`",
        f"- selected cluster: `{gate.selected_cluster}`",
        f"- selected pivot: `{gate.selected_pivot}`",
        f"- domain decision: `{gate.domain_decision}`",
        f"- next ticket: `{gate.next_ticket}` `{gate.next_topic}`",
        f"- code-change readiness: `{gate.code_change_readiness}`",
        "- source-patch-ready rows: `0`",
        "- marker-ready rows: `0`",
        "",
        "No production source or marker change is authorized by this gate.",
        "",
        "## Geometry-support scope",
        "",
    ]
    for row in gate.scope_rows:
        lines.append(
            f"- `{row.function}` in `{row.file}`: `{row.role}`, source `{row.source_status}`, patch `{row.source_patch_decision}`."
        )
    lines.extend(["", "## Follow-up plan", ""])
    for item in gate.ticket_plan:
        lines.append(f"- `{item.story_id}` `{item.topic}` — {item.goal} Exit: {item.exit_condition}.")
    lines.extend(
        [
            "",
            "## Handoff",
            "",
            f"- next ticket: `{gate.handoff.next_ticket}`",
            f"- next topic: `{gate.handoff.next_topic}`",
            f"- reason: `{gate.handoff.reason}`",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story(path: Path, gate: ClosureOrHandoff) -> None:
    lines = [
        "# RE-170 — Module SPEC_PSXPC_N closure or handoff",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Consume the RE-169 next-cluster selection and either close module SPEC_PSXPC_N or hand off a bounded geometry-support proof chain.",
        "",
        "## Scope",
        "",
        "- depends on: `RE-169`, `RE-163`",
        "- safety contract: metadata-only closure/handoff decision; source and marker edits stay blocked",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-169 geometry-support handoff consumed.",
        "- [x] RE-163 geometry-support scope consumed.",
        "- [x] domain closure denied while proof blockers remain.",
        "- [x] RE-171..RE-177 follow-up plan emitted.",
        "- [x] Forbidden evidence excluded from generated artifacts.",
        "",
        "## Generated artifacts",
        "",
        f"- `{SCOPE_CSV}`",
        f"- `{PLAN_CSV}`",
        f"- `{DECISION_CSV}`",
        f"- `{HANDOFF_CSV}`",
        f"- `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- selected cluster: `{gate.selected_cluster}`",
        f"- selected pivot: `{gate.selected_pivot}`",
        "- domain closure denied: selected cluster still lacks caller/state and non-raw equivalence proof",
        "- source-patch-ready rows: `0`",
        "- marker-ready rows: `0`",
        "",
        "## Follow-up ticket breakdown",
        "",
    ]
    for item in gate.ticket_plan:
        lines.append(f"- `{item.story_id}` `{item.topic}`: {item.goal}")
    lines.extend(
        [
            "",
            "## Readiness decision",
            "",
            f"- decision: `{gate.domain_decision}`",
            f"- code change readiness: `{gate.code_change_readiness}`",
            f"- next ticket: `{gate.next_ticket}`",
            "",
            "No production source or marker change is authorized by this gate.",
            "",
            "## Validation",
            "",
            "- `python3 -m pytest tests/reverse/test_re170_module_spec_psxpc_n_closure_or_handoff.py -q`",
            "- `python3 -m pytest tests/reverse -q`",
            "- metadata-only guard over RE-170 outputs",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_all_artifacts(gate: ClosureOrHandoff, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "scope_csv": repo / SCOPE_CSV,
        "ticket_plan_csv": repo / PLAN_CSV,
        "decision_csv": repo / DECISION_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY_OUTPUT,
    }
    write_dict_csv(paths["scope_csv"], list(ScopeRow.__dataclass_fields__), [row.__dict__ for row in gate.scope_rows])
    write_dict_csv(paths["ticket_plan_csv"], list(TicketPlanItem.__dataclass_fields__), [row.__dict__ for row in gate.ticket_plan])
    write_dict_csv(paths["decision_csv"], list(ClosureDecisionRow.__dataclass_fields__), [gate.decision_row.__dict__])
    write_dict_csv(paths["handoff_csv"], list(HandoffRow.__dataclass_fields__), [gate.handoff.__dict__])
    write_markdown(paths["md"], gate)
    write_story(paths["story"], gate)
    assert_metadata_only(paths)
    return paths


def assert_metadata_only(paths: dict[str, Path]) -> None:
    for path in paths.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            if fragment in text:
                raise ValueError(f"forbidden metadata fragment {fragment!r} in {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="repository root")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    gate = build_closure_or_handoff(repo)
    write_all_artifacts(gate, repo)
    print(f"selected_cluster={gate.selected_cluster}")
    print(f"next_ticket={gate.next_ticket}")
    print(f"domain_decision={gate.domain_decision}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
