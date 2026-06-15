#!/usr/bin/env python3
"""Generate RE-214 maths-render-support proof-first audit artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

UPSTREAM_HANDOFF = "docs/reverse/generated/re213-post-module-spec-psxpc-n-domain-selection-handoff.csv"
SOURCE_PRIORITY = "docs/reverse/generated/function-priority.csv"
AUDIT_CSV = "docs/reverse/generated/re214-maths-render-support-proof-first-audit.csv"
CLUSTERS_CSV = "docs/reverse/generated/re214-maths-render-support-clusters.csv"
PLAN_CSV = "docs/reverse/generated/re214-maths-render-support-ticket-plan.csv"
HANDOFF_CSV = "docs/reverse/generated/re214-maths-render-support-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re214-maths-render-support-proof-first-audit.md"
STORY_OUTPUT = "docs/stories/RE-214-maths-render-support-proof-first-audit.md"

EXPECTED_SCOPE = ("mTranslateXYZ", "DrawPhaseGame", "mTranslateXYZ", "mPushUnitMatrix", "mPushUnitMatrix")
FORBIDDEN = (
    "word_le_hex",
    "payload_offset",
    "dump row",
    "opcode",
    "machine word",
    "call_address",
    "branch target",
    "call target",
    "0x800",
)
STALE_FRAGMENTS = (
    "module-spec_psxpc_n-exhausted",
    "post-module-spec-psxpc-n domain selection",
    "open re-214",
)
DOMAIN_RULES = (
    ("audio-effects", ("EFFECT", "SFX", "SOUND")),
    ("collision", ("COLLIDE", "COLLISION")),
    ("inventory", ("NEWINV", "INVENTORY", "REQUEST")),
    ("camera", ("CAMERA", "SPOTCAM")),
    ("input", ("INPUT", "PSXINPUT")),
    ("lara-combat", ("LARAFIRE", "WEAPON", "MISSILE")),
    ("traps-switches-doors", ("TRAPS", "SWITCH", "DOOR")),
    ("animation-items", ("ANIMITEM", "ANIM")),
    ("maths-render-support", ("MATHS", "DRAW", "GPU")),
)
SUBCLUSTER_ORDER = ("matrix-transform-core", "gpu-scene-support", "object-draw-support", "draw-phase-support")


@dataclass(frozen=True)
class AuditRow:
    function: str
    file: str
    line: int
    bucket: str
    status: str
    score: int
    caller_count: int
    callee_count: int
    nd: str
    runtime_focus: str
    subcluster: str
    proof_status: str
    code_change_ready: str
    marker_ready: str
    blocker: str


@dataclass(frozen=True)
class ClusterRow:
    subcluster: str
    rank: int
    candidate_count: int
    mapped_count: int
    nd_count: int
    runtime_count: int
    top_function: str
    top_file: str
    readiness: str
    blocker: str
    next_ticket: str


@dataclass(frozen=True)
class TicketPlanRow:
    story_id: str
    topic: str
    goal: str
    scope: str
    code_change_readiness: str
    exit_condition: str


@dataclass(frozen=True)
class HandoffRow:
    next_ticket: str
    next_topic: str
    selected_domain: str
    selected_subcluster: str
    selected_pivot: str
    outcome: str
    reason: str
    dependency: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class MathsRenderAudit:
    story_id: str
    upstream_ticket: str
    domain_id: str
    pivot: str
    status: str
    code_change_readiness: str
    marker_readiness: str
    candidate_count: int
    mapped_count: int
    nd_count: int
    runtime_count: int
    next_ticket: str
    next_topic: str
    scope_rows: tuple[AuditRow, ...]
    cluster_rows: tuple[ClusterRow, ...]
    plan_rows: tuple[TicketPlanRow, ...]
    handoff: HandoffRow


def parse_int(text: str | None) -> int:
    try:
        return int(text or "0")
    except ValueError:
        return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_upstream_handoff(rows: list[dict[str, str]]) -> None:
    if len(rows) != 1:
        raise ValueError("RE-213 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "next_ticket": "RE-214",
        "next_topic": "maths-render-support-proof-first-audit",
        "selected_domain": "maths-render-support",
        "selected_pivot": "mTranslateXYZ",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-213 handoff drift: expected {key}={value!r}, got {row.get(key)!r}")


def classify_domain(row: dict[str, str]) -> str:
    haystack = f"{row.get('file', '')} {row.get('repo_function', '')}".upper()
    for domain_id, terms in DOMAIN_RULES:
        if any(term in haystack for term in terms):
            return domain_id
    module = row.get("file", ".").split("/", 1)[0]
    return f"module-{module.lower()}"


def classify_subcluster(row: dict[str, str]) -> str:
    haystack = f"{row.get('file', '')} {row.get('repo_function', '')}".upper()
    name = row.get("repo_function", "")
    if "MATHS" in haystack or name.startswith("m"):
        return "matrix-transform-core"
    if "GPU" in haystack:
        return "gpu-scene-support"
    if "DRAWPHAS" in haystack:
        return "draw-phase-support"
    if "DRAWOBJ" in haystack or "DRAW" in haystack:
        return "object-draw-support"
    return "object-draw-support"


def build_scope_rows(priority_rows: list[dict[str, str]]) -> tuple[AuditRow, ...]:
    rows = [row for row in priority_rows if classify_domain(row) == "maths-render-support"]
    rows.sort(key=lambda row: (-parse_int(row.get("score")), row.get("file", ""), parse_int(row.get("line")), row.get("repo_function", "")))
    audit_rows = tuple(
        AuditRow(
            function=row.get("repo_function", ""),
            file=row.get("file", ""),
            line=parse_int(row.get("line")),
            bucket=row.get("bucket", ""),
            status=row.get("status", ""),
            score=parse_int(row.get("score")),
            caller_count=parse_int(row.get("caller_count")),
            callee_count=parse_int(row.get("callee_count")),
            nd=row.get("nd", "no") or "no",
            runtime_focus=row.get("runtime_focus", "no") or "no",
            subcluster=classify_subcluster(row),
            proof_status="source-priority-metadata-only",
            code_change_ready="no",
            marker_ready="no",
            blocker="missing-maths-render-source-contract-and-non-raw-equivalence-proof",
        )
        for row in rows
    )
    if len(audit_rows) != 92:
        raise ValueError(f"maths-render-support scope drifted: {len(audit_rows)}")
    if tuple(row.function for row in audit_rows[:5]) != EXPECTED_SCOPE:
        raise ValueError(f"maths-render-support top scope drifted: {[row.function for row in audit_rows[:5]]}")
    return audit_rows


def build_cluster_rows(scope_rows: tuple[AuditRow, ...]) -> tuple[ClusterRow, ...]:
    grouped = {name: [row for row in scope_rows if row.subcluster == name] for name in SUBCLUSTER_ORDER}
    rows: list[ClusterRow] = []
    for rank, name in enumerate(SUBCLUSTER_ORDER, start=1):
        members = grouped[name]
        if not members:
            raise ValueError(f"empty maths-render subcluster: {name}")
        top = members[0]
        rows.append(ClusterRow(
            subcluster=name,
            rank=rank,
            candidate_count=len(members),
            mapped_count=sum(row.bucket in {"P0", "P1", "P2"} for row in members),
            nd_count=sum(row.nd == "yes" for row in members),
            runtime_count=sum(row.runtime_focus == "yes" for row in members),
            top_function=top.function,
            top_file=top.file,
            readiness="proof-needed",
            blocker="cluster needs source-level state contract and non-raw binary equivalence proof",
            next_ticket="RE-215" if name == "matrix-transform-core" else "TBD",
        ))
    if rows[0].candidate_count != 37 or rows[0].top_function != "mTranslateXYZ":
        raise ValueError("matrix-transform-core scope drifted")
    return tuple(rows)


def build_plan_rows() -> tuple[TicketPlanRow, ...]:
    data = (
        ("RE-215", "maths-render-support-matrix-transform-chain", "Batch matrix transform helpers beginning at mTranslateXYZ.", "matrix-transform-core source-backed candidate rows", "Matrix transform proof chain emits state/equivalence/patch gates"),
        ("RE-216", "maths-render-support-gpu-scene-chain", "Batch GPU scene/order-table support helpers after matrix transform closure.", "gpu-scene-support candidate rows", "GPU scene proof chain emits readiness and no-patch/patch gate"),
        ("RE-217", "maths-render-support-object-draw-chain", "Batch object draw support helpers after GPU scene closure.", "object-draw-support candidate rows", "Object draw proof chain emits readiness and no-patch/patch gate"),
        ("RE-218", "maths-render-support-draw-phase-chain", "Batch draw phase support helpers after object draw closure.", "draw-phase-support candidate rows", "Draw phase proof chain emits readiness and no-patch/patch gate"),
        ("RE-219", "maths-render-support-cross-platform-reconciliation", "Reconcile duplicated platform maths/render rows across SPEC_PSXPC_N, SPEC_PSXPC, and SPEC_PSX.", "cross-platform duplicate rows", "Duplicate handling is documented before source or marker changes"),
        ("RE-220", "maths-render-support-source-patch-gate", "Authorize source/marker edits only for rows made ready by prior proof gates.", "ready maths-render-support rows only", "Patch/build/tests pass or no-patch blocker is published"),
        ("RE-221", "post-maths-render-support-domain-selection", "Select the next proof domain after maths-render-support closes or blocks.", "remaining RE-162 domain shortlist after maths-render-support", "Next domain handoff artifact names the next objective"),
    )
    return tuple(TicketPlanRow(story_id, topic, goal, scope, "blocked-until-proof", exit_condition) for story_id, topic, goal, scope, exit_condition in data)


def build_audit(repo: Path) -> MathsRenderAudit:
    repo = Path(repo)
    validate_upstream_handoff(read_csv(repo / UPSTREAM_HANDOFF))
    scope_rows = build_scope_rows(read_csv(repo / SOURCE_PRIORITY))
    cluster_rows = build_cluster_rows(scope_rows)
    plan_rows = build_plan_rows()
    handoff = HandoffRow(
        next_ticket="RE-215",
        next_topic="maths-render-support-matrix-transform-chain",
        selected_domain="maths-render-support",
        selected_subcluster="matrix-transform-core",
        selected_pivot="mTranslateXYZ",
        outcome="maths-render-support-opened-with-proof-blocker",
        reason="matrix-transform-core is the first bounded subcluster for the maths-render-support proof chain",
        dependency="RE-214 maths-render-support proof-first audit",
        code_change_readiness="blocked",
        stop_condition="matrix-transform chain emitted",
    )
    return MathsRenderAudit(
        story_id="RE-214",
        upstream_ticket="RE-213",
        domain_id="maths-render-support",
        pivot="mTranslateXYZ",
        status="maths-render-support-proof-first-audit-ready",
        code_change_readiness="blocked",
        marker_readiness="blocked",
        candidate_count=len(scope_rows),
        mapped_count=sum(row.bucket in {"P0", "P1", "P2"} for row in scope_rows),
        nd_count=sum(row.nd == "yes" for row in scope_rows),
        runtime_count=sum(row.runtime_focus == "yes" for row in scope_rows),
        next_ticket=handoff.next_ticket,
        next_topic=handoff.next_topic,
        scope_rows=scope_rows,
        cluster_rows=cluster_rows,
        plan_rows=plan_rows,
        handoff=handoff,
    )


def write_dict_csv(path: Path, cls: type, rows: list[dict[str, object]]) -> None:
    fields = list(cls.__dataclass_fields__)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_markdown(path: Path, audit: MathsRenderAudit) -> None:
    lines = [
        "# RE-214 maths-render-support proof-first audit",
        "",
        f"Status: `{audit.status}`",
        f"Selected domain: `{audit.domain_id}`",
        f"Selected pivot: `{audit.pivot}`",
        f"candidate count: `{audit.candidate_count}`",
        f"mapped count: `{audit.mapped_count}`",
        f"ND count: `{audit.nd_count}`",
        f"runtime count: `{audit.runtime_count}`",
        f"code-change readiness: `{audit.code_change_readiness}`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-213 handoff consumed.",
        "- [x] Existing priority metadata filtered to maths-render-support.",
        "- [x] Subclusters and follow-up ticket plan emitted.",
        "- [x] Source and marker changes blocked pending non-raw proof gates.",
        "",
        "## Subclusters",
        "",
    ]
    for row in audit.cluster_rows:
        lines.append(
            f"- #{row.rank} `{row.subcluster}` / `{row.top_function}`: {row.candidate_count} candidate(s), readiness `{row.readiness}`, next `{row.next_ticket}`."
        )
    lines.extend([
        "",
        "## Decision",
        "",
        "Selected subcluster: `matrix-transform-core`",
        "Selected pivot: `mTranslateXYZ`",
        "Recommended next ticket: `RE-215`",
        "No production source or marker change is authorized by this opening audit.",
        "",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story(path: Path, audit: MathsRenderAudit) -> None:
    lines = [
        "# RE-214 — maths-render-support proof-first audit",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Open the maths-render-support proof domain and select the first bounded subcluster without authorizing source or marker changes.",
        "",
        "## Scope",
        "",
        "- depends on: `RE-213`, `function-priority.csv`",
        f"- candidates: `{audit.candidate_count}`; mapped: `{audit.mapped_count}`; ND: `{audit.nd_count}`; runtime: `{audit.runtime_count}`",
        "- safety contract: metadata-only generated rows; no instruction text, proprietary dump records, or raw address literals in outputs",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-213 handoff consumed.",
        "- [x] Maths/render candidates filtered from priority metadata.",
        "- [x] Subcluster readiness matrix emitted.",
        "- [x] Follow-up ticket plan emitted.",
        "- [x] Source patch authorization withheld pending proof gates.",
        "",
        "## Generated artifacts",
        "",
        f"- `{AUDIT_CSV}`",
        f"- `{CLUSTERS_CSV}`",
        f"- `{PLAN_CSV}`",
        f"- `{HANDOFF_CSV}`",
        f"- `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        "- selected subcluster: `matrix-transform-core`",
        "- selected pivot: `mTranslateXYZ`",
        "- blocker: `missing-maths-render-source-contract-and-non-raw-equivalence-proof`",
        "- all rows remain blocked for source or marker changes until a subcluster-specific proof gate runs",
        "",
        "## Readiness decision",
        "",
        f"Recommended next ticket: `{audit.next_ticket}`",
        f"Code-change readiness: `{audit.code_change_readiness}`",
        "No production source or marker change is authorized by this opening audit.",
        "",
        "## Validation",
        "",
        "- `python3 -m pytest tests/reverse/test_re214_maths_render_support_audit.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over RE-214 outputs",
        "",
        "## Next step",
        "",
        "RE-215: execute `maths-render-support-matrix-transform-chain` for `matrix-transform-core` / `mTranslateXYZ`.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_all_artifacts(audit: MathsRenderAudit, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "audit_csv": repo / AUDIT_CSV,
        "clusters_csv": repo / CLUSTERS_CSV,
        "plan_csv": repo / PLAN_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY_OUTPUT,
    }
    write_dict_csv(paths["audit_csv"], AuditRow, [row.__dict__ for row in audit.scope_rows])
    write_dict_csv(paths["clusters_csv"], ClusterRow, [row.__dict__ for row in audit.cluster_rows])
    write_dict_csv(paths["plan_csv"], TicketPlanRow, [row.__dict__ for row in audit.plan_rows])
    write_dict_csv(paths["handoff_csv"], HandoffRow, [audit.handoff.__dict__])
    write_markdown(paths["md"], audit)
    write_story(paths["story"], audit)
    return paths


def assert_metadata_only(paths: dict[str, Path]) -> None:
    fragments = tuple(fragment.lower() for fragment in FORBIDDEN + STALE_FRAGMENTS)
    for path in paths.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in fragments:
            if fragment in text:
                raise ValueError(f"forbidden metadata fragment {fragment!r} in {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="repository root")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    audit = build_audit(repo)
    written = write_all_artifacts(audit, repo)
    assert_metadata_only(written)
    print(f"selected_domain={audit.domain_id}")
    print(f"selected_subcluster={audit.handoff.selected_subcluster}")
    print(f"next_ticket={audit.next_ticket}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
