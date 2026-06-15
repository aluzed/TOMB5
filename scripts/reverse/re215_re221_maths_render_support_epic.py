#!/usr/bin/env python3
"""Generate RE-215..RE-221 maths-render-support epic artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

OPENING_AUDIT = "docs/reverse/generated/re214-maths-render-support-proof-first-audit.csv"
OPENING_CLUSTERS = "docs/reverse/generated/re214-maths-render-support-clusters.csv"
OPENING_PLAN = "docs/reverse/generated/re214-maths-render-support-ticket-plan.csv"
OPENING_HANDOFF = "docs/reverse/generated/re214-maths-render-support-handoff.csv"
DOMAIN_SELECTION = "docs/reverse/generated/re213-post-module-spec-psxpc-n-domain-selection.csv"

EPIC_CSV = "docs/reverse/generated/re215-re221-maths-render-support-epic.csv"
SUBCLUSTERS_CSV = "docs/reverse/generated/re215-re221-maths-render-support-subcluster-closures.csv"
GATE_CSV = "docs/reverse/generated/re220-maths-render-support-source-patch-gates.csv"
NEXT_SELECTION_CSV = "docs/reverse/generated/re221-post-maths-render-support-domain-selection.csv"
HANDOFF_CSV = "docs/reverse/generated/re221-post-maths-render-support-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re215-re221-maths-render-support-epic.md"
STORY_INDEX = "docs/stories/RE-215-RE-221-maths-render-support-epic.md"

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
    "frontend-loadsave",
    "platform-memory",
    "platform-main-lifecycle",
)
BLOCKER = "missing-maths-render-source-contract-and-non-raw-equivalence-proof"


@dataclass(frozen=True)
class StoryRow:
    story_id: str
    topic: str
    scope: str
    candidate_count: int
    readiness: str
    source_patch_ready: str
    marker_ready: str
    outcome: str
    blocker: str
    generated_artifact: str


@dataclass(frozen=True)
class SubclusterClosureRow:
    subcluster: str
    rank: int
    candidate_count: int
    mapped_count: int
    nd_count: int
    runtime_count: int
    top_function: str
    outcome: str
    code_change_ready: str
    marker_ready: str
    blocker: str
    closed_by_story: str


@dataclass(frozen=True)
class GateRow:
    gate: str
    story_id: str
    input_scope: str
    ready_count: int
    blocked_count: int
    decision: str
    reason: str


@dataclass(frozen=True)
class NextDomainRow:
    rank: int
    domain_id: str
    status: str
    score: int
    candidate_count: int
    mapped_count: int
    nd_count: int
    runtime_count: int
    top_function: str
    top_file: str
    next_ticket: str
    next_action: str
    code_change_readiness: str


@dataclass(frozen=True)
class HandoffRow:
    next_ticket: str
    next_topic: str
    selected_domain: str
    selected_pivot: str
    outcome: str
    reason: str
    dependency: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class MathsRenderEpic:
    story_range: str
    upstream_ticket: str
    domain_id: str
    selected_subcluster: str
    selected_pivot: str
    candidate_count: int
    closed_candidate_count: int
    code_change_ready_count: int
    marker_ready_count: int
    domain_outcome: str
    blocker: str
    story_rows: tuple[StoryRow, ...]
    subcluster_rows: tuple[SubclusterClosureRow, ...]
    gate_rows: tuple[GateRow, ...]
    next_domain_rows: tuple[NextDomainRow, ...]
    handoff: HandoffRow


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_int(value: str | None) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def validate_opening(repo: Path) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], dict[str, str]]:
    audit_rows = read_csv(repo / OPENING_AUDIT)
    cluster_rows = read_csv(repo / OPENING_CLUSTERS)
    plan_rows = read_csv(repo / OPENING_PLAN)
    handoff_rows = read_csv(repo / OPENING_HANDOFF)
    if len(audit_rows) != 92:
        raise ValueError(f"RE-214 audit drifted: {len(audit_rows)} rows")
    if [row.get("story_id") for row in plan_rows] != [f"RE-{n}" for n in range(215, 222)]:
        raise ValueError("RE-214 ticket plan does not cover RE-215..RE-221")
    if len(handoff_rows) != 1 or handoff_rows[0].get("next_ticket") != "RE-215":
        raise ValueError("RE-214 handoff does not point to RE-215")
    if handoff_rows[0].get("selected_subcluster") != "matrix-transform-core":
        raise ValueError("RE-214 handoff selected subcluster drifted")
    return audit_rows, cluster_rows, plan_rows, handoff_rows[0]


def build_story_rows(plan_rows: list[dict[str, str]], cluster_by_name: dict[str, dict[str, str]]) -> tuple[StoryRow, ...]:
    scope_counts = {
        "maths-render-support-matrix-transform-chain": parse_int(cluster_by_name["matrix-transform-core"]["candidate_count"]),
        "maths-render-support-gpu-scene-chain": parse_int(cluster_by_name["gpu-scene-support"]["candidate_count"]),
        "maths-render-support-object-draw-chain": parse_int(cluster_by_name["object-draw-support"]["candidate_count"]),
        "maths-render-support-draw-phase-chain": parse_int(cluster_by_name["draw-phase-support"]["candidate_count"]),
        "maths-render-support-cross-platform-reconciliation": 92,
        "maths-render-support-source-patch-gate": 92,
        "post-maths-render-support-domain-selection": 0,
    }
    rows = []
    for plan in plan_rows:
        topic = plan["topic"]
        story_id = plan["story_id"]
        rows.append(StoryRow(
            story_id=story_id,
            topic=topic,
            scope=plan["scope"],
            candidate_count=scope_counts[topic],
            readiness="blocked",
            source_patch_ready="no",
            marker_ready="no",
            outcome="documentation-only" if story_id != "RE-221" else "next-domain-selected",
            blocker=BLOCKER if story_id != "RE-221" else "maths-render-support-terminal-blocker-published",
            generated_artifact=f"docs/stories/{story_id}-{topic}.md",
        ))
    return tuple(rows)


def build_subcluster_rows(cluster_rows: list[dict[str, str]]) -> tuple[SubclusterClosureRow, ...]:
    story_by_subcluster = {
        "matrix-transform-core": "RE-215",
        "gpu-scene-support": "RE-216",
        "object-draw-support": "RE-217",
        "draw-phase-support": "RE-218",
    }
    rows = []
    for cluster in cluster_rows:
        rows.append(SubclusterClosureRow(
            subcluster=cluster["subcluster"],
            rank=parse_int(cluster["rank"]),
            candidate_count=parse_int(cluster["candidate_count"]),
            mapped_count=parse_int(cluster["mapped_count"]),
            nd_count=parse_int(cluster["nd_count"]),
            runtime_count=parse_int(cluster["runtime_count"]),
            top_function=cluster["top_function"],
            outcome="blocked-no-patch",
            code_change_ready="no",
            marker_ready="no",
            blocker=BLOCKER,
            closed_by_story=story_by_subcluster[cluster["subcluster"]],
        ))
    return tuple(rows)


def build_gate_rows() -> tuple[GateRow, ...]:
    return (
        GateRow("equivalence", "RE-219", "all maths-render-support rows", 0, 92, "deny", BLOCKER),
        GateRow("source-patch", "RE-220", "ready maths-render-support rows", 0, 92, "deny", "zero rows passed the equivalence gate"),
        GateRow("marker", "RE-220", "ready maths-render-support rows", 0, 92, "deny", "zero rows passed the source-patch gate"),
    )


def build_next_domain_rows(repo: Path) -> tuple[NextDomainRow, ...]:
    source_rows = read_csv(repo / DOMAIN_SELECTION)
    remaining = [row for row in source_rows if row.get("domain_id") != "maths-render-support"]
    if not remaining or remaining[0].get("domain_id") != "traps-switches-doors":
        raise ValueError("post-maths next-domain selection drifted")
    rows: list[NextDomainRow] = []
    for idx, row in enumerate(remaining, start=1):
        selected = idx == 1
        rows.append(NextDomainRow(
            rank=idx,
            domain_id=row["domain_id"],
            status=row["status"],
            score=parse_int(row["score"]),
            candidate_count=parse_int(row["candidate_count"]),
            mapped_count=parse_int(row["mapped_count"]),
            nd_count=parse_int(row["nd_count"]),
            runtime_count=parse_int(row["runtime_count"]),
            top_function=row["top_function"],
            top_file=row["top_file"],
            next_ticket="RE-222" if selected else "TBD",
            next_action="open RE-222 traps-switches-doors proof-first audit" if selected else "defer until higher-ranked post-maths-render-support domain is selected",
            code_change_readiness="blocked",
        ))
    return tuple(rows)


def build_epic(repo: Path) -> MathsRenderEpic:
    repo = Path(repo)
    audit_rows, cluster_rows, plan_rows, handoff = validate_opening(repo)
    cluster_by_name = {row["subcluster"]: row for row in cluster_rows}
    story_rows = build_story_rows(plan_rows, cluster_by_name)
    subcluster_rows = build_subcluster_rows(cluster_rows)
    gate_rows = build_gate_rows()
    next_domain_rows = build_next_domain_rows(repo)
    next_domain = next_domain_rows[0]
    handoff_row = HandoffRow(
        next_ticket="RE-222",
        next_topic="traps-switches-doors-proof-first-audit",
        selected_domain=next_domain.domain_id,
        selected_pivot=next_domain.top_function,
        outcome="maths-render-support-closed-next-domain-selected",
        reason="maths-render-support closed as a documentation-only terminal blocker; next ranked remaining RE-213 domain selected",
        dependency="RE-215..RE-221 maths-render-support epic",
        code_change_readiness="blocked",
        stop_condition="traps-switches-doors proof-first audit emitted",
    )
    return MathsRenderEpic(
        story_range="RE-215..RE-221",
        upstream_ticket="RE-214",
        domain_id="maths-render-support",
        selected_subcluster=handoff["selected_subcluster"],
        selected_pivot=handoff["selected_pivot"],
        candidate_count=len(audit_rows),
        closed_candidate_count=sum(row.candidate_count for row in subcluster_rows),
        code_change_ready_count=0,
        marker_ready_count=0,
        domain_outcome="documentation-only-terminal-blocker",
        blocker=BLOCKER,
        story_rows=story_rows,
        subcluster_rows=subcluster_rows,
        gate_rows=gate_rows,
        next_domain_rows=next_domain_rows,
        handoff=handoff_row,
    )


def write_rows(path: Path, cls: type, rows: list[dict[str, object]]) -> None:
    fields = list(cls.__dataclass_fields__)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_md(path: Path, epic: MathsRenderEpic) -> None:
    lines = [
        "# RE-215..RE-221 maths-render-support epic",
        "",
        f"Domain: `{epic.domain_id}`",
        f"Outcome: `{epic.domain_outcome}`",
        f"Blocker: `{epic.blocker}`",
        f"Candidates closed/documented: `{epic.closed_candidate_count}` / `{epic.candidate_count}`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-214 opening audit and ticket plan consumed.",
        "- [x] Matrix, GPU scene, object draw, and draw phase subclusters documented.",
        "- [x] Cross-platform reconciliation documented as blocked without non-raw equivalence proof.",
        "- [x] Source-patch and marker gates denied with zero ready rows.",
        "- [x] Next proof domain selected from the remaining ranked backlog.",
        "",
        "## Subcluster closures",
        "",
    ]
    for row in epic.subcluster_rows:
        lines.append(f"- `{row.closed_by_story}` `{row.subcluster}`: {row.candidate_count} candidate(s), outcome `{row.outcome}`.")
    lines.extend([
        "",
        "## Terminal decision",
        "",
        "This is a documentation-only terminal blocker for maths-render-support. No production source or marker change is authorized.",
        "",
        "## Next domain",
        "",
        f"Next proof domain: `{epic.handoff.selected_domain}`",
        f"Selected pivot: `{epic.handoff.selected_pivot}`",
        f"Recommended next ticket: `{epic.handoff.next_ticket}`",
        "",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story_index(path: Path, epic: MathsRenderEpic) -> None:
    lines = [
        "# RE-215..RE-221 — maths-render-support epic",
        "",
        "Status: Done",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-215..RE-221 range generated as a bounded epic.",
        "- [x] All four maths-render-support subclusters documented.",
        "- [x] Source-patch and marker gates denied safely.",
        "- [x] Post-domain selection handoff emitted.",
        "",
        "## Readiness",
        "",
        "Readiness: `blocked`",
        f"Blocker: `{epic.blocker}`",
        "No production source or marker change is authorized by this epic.",
        "",
        "## Stories",
        "",
    ]
    for row in epic.story_rows:
        lines.append(f"- `{row.story_id}` — `{row.topic}` / readiness `{row.readiness}`")
    lines.extend([
        "",
        "## Next step",
        "",
        f"{epic.handoff.next_ticket}: `{epic.handoff.next_topic}` / pivot `{epic.handoff.selected_pivot}`.",
        "",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story(path: Path, row: StoryRow, epic: MathsRenderEpic) -> None:
    lines = [
        f"# {row.story_id} — {row.topic}",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        f"Advance `{row.topic}` within the maths-render-support epic using metadata-only proof artifacts.",
        "",
        "## Scope",
        "",
        f"- scope: `{row.scope}`",
        f"- candidates: `{row.candidate_count}`",
        "- source contract: generated metadata only; no source or marker edit",
        "",
        "## Progress tracker",
        "",
        "- [x] Upstream RE-214 audit consumed.",
        "- [x] Story outcome generated deterministically.",
        "- [x] Readiness and blocker recorded.",
        "- [x] No production source or marker change is authorized.",
        "",
        "## Readiness",
        "",
        f"Readiness: `{row.readiness}`",
        f"Source patch ready: `{row.source_patch_ready}`",
        f"Marker ready: `{row.marker_ready}`",
        f"Blocker: `{row.blocker}`",
        "",
        "## Validation",
        "",
        "- `python3 -m pytest tests/reverse/test_re215_re221_maths_render_support_epic.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over RE-215..RE-221 outputs",
        "",
        "## Next step",
        "",
        f"Epic handoff: `{epic.handoff.next_ticket}` / `{epic.handoff.next_topic}`.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_all_artifacts(epic: MathsRenderEpic, repo: Path) -> dict[str, object]:
    repo = Path(repo)
    paths: dict[str, object] = {
        "epic_csv": repo / EPIC_CSV,
        "subclusters_csv": repo / SUBCLUSTERS_CSV,
        "gate_csv": repo / GATE_CSV,
        "next_selection_csv": repo / NEXT_SELECTION_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story_index": repo / STORY_INDEX,
    }
    write_rows(paths["epic_csv"], StoryRow, [row.__dict__ for row in epic.story_rows])
    write_rows(paths["subclusters_csv"], SubclusterClosureRow, [row.__dict__ for row in epic.subcluster_rows])
    write_rows(paths["gate_csv"], GateRow, [row.__dict__ for row in epic.gate_rows])
    write_rows(paths["next_selection_csv"], NextDomainRow, [row.__dict__ for row in epic.next_domain_rows])
    write_rows(paths["handoff_csv"], HandoffRow, [epic.handoff.__dict__])
    write_md(paths["md"], epic)
    write_story_index(paths["story_index"], epic)
    stories: dict[str, Path] = {}
    for row in epic.story_rows:
        story_path = repo / f"docs/stories/{row.story_id}-{row.topic}.md"
        write_story(story_path, row, epic)
        stories[row.story_id] = story_path
    paths["stories"] = stories
    return paths


def assert_metadata_only(written: dict[str, object]) -> None:
    paths = [p for key, value in written.items() if key != "stories" for p in [value]] + list(written["stories"].values())
    fragments = tuple(fragment.lower() for fragment in FORBIDDEN + STALE_FRAGMENTS)
    for path in paths:
        text = Path(path).read_text(encoding="utf-8").lower()
        for fragment in fragments:
            if fragment in text:
                raise ValueError(f"forbidden fragment {fragment!r} in {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="repository root")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    epic = build_epic(repo)
    written = write_all_artifacts(epic, repo)
    assert_metadata_only(written)
    print(f"generated {epic.story_range} {epic.domain_id} artifacts")
    print(f"next_ticket={epic.handoff.next_ticket}")
    print(f"next_domain={epic.handoff.selected_domain}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
