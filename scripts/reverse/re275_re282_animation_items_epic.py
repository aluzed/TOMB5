#!/usr/bin/env python3
"""Generate RE-275..RE-282 animation-items epic artifacts."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import asdict, dataclass, fields
from pathlib import Path

UPSTREAM_HANDOFF = "docs/reverse/generated/re274-post-camera-handoff.csv"
FUNCTION_PRIORITY = "docs/reverse/generated/function-priority.csv"

SELECTION_CSV = "docs/reverse/generated/re275-post-camera-domain-reprioritization.csv"
AUDIT_CSV = "docs/reverse/generated/re276-animation-items-proof-first-audit.csv"
SUBCLUSTERS_CSV = "docs/reverse/generated/re276-animation-items-subclusters.csv"
EPIC_CSV = "docs/reverse/generated/re275-re282-animation-items-epic.csv"
GATE_CSV = "docs/reverse/generated/re281-animation-items-source-patch-gates.csv"
HANDOFF_CSV = "docs/reverse/generated/re282-post-animation-items-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re275-re282-animation-items-epic.md"
STORY_INDEX = "docs/stories/RE-275-RE-282-animation-items-epic.md"

FORBIDDEN = (
    "word_le_hex", "payload_offset", "dump row", "opcode", "machine word",
    "call_address", "branch target", "call target", "0x800",
)
STALE_FRAGMENTS = (
    "camera closed", "post-camera-domain-backlog-exhausted", "calculate spotcams",
    "open re-268", "input closed", "inventory",
)
BLOCKER = "missing-animation-item-state-contract-and-non-raw-equivalence-proof"

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
CLOSED_DOMAINS = {
    "audio-effects", "collision", "inventory", "camera", "input", "lara-combat",
    "traps-switches-doors", "maths-render-support", "module-game",
    "module-spec_psxpc_n", "module-spec_psxpc", "module-spec_psx",
}
CLOSED_FILES = {"GAME/SAVEGAME.C"}


@dataclass(frozen=True)
class SelectionRow:
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
class AuditRow:
    rank: int
    domain_id: str
    subcluster: str
    function: str
    file: str
    line: int
    status: str
    mapped: str
    runtime_focus: str
    nd: str
    caller_count: int
    callee_count: int
    readiness: str
    source_patch_ready: str
    marker_ready: str
    blocker: str


@dataclass(frozen=True)
class SubclusterRow:
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
class StoryRow:
    story_id: str
    topic: str
    scope: str
    candidate_count: int
    readiness: str
    source_patch_ready: str
    marker_ready: str
    blocker: str
    artifact: str


@dataclass(frozen=True)
class GateRow:
    gate: str
    story_id: str
    scope: str
    ready_count: int
    blocked_count: int
    decision: str
    blocker: str


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
class AnimationItemsEpic:
    story_range: str
    upstream_ticket: str
    domain_id: str
    selected_pivot: str
    raw_priority_count: int
    parser_artifact_count: int
    candidate_count: int
    closed_candidate_count: int
    runtime_count: int
    nd_count: int
    code_change_ready_count: int
    marker_ready_count: int
    domain_outcome: str
    blocker: str
    selection_rows: tuple[SelectionRow, ...]
    audit_rows: tuple[AuditRow, ...]
    subcluster_rows: tuple[SubclusterRow, ...]
    story_rows: tuple[StoryRow, ...]
    gate_rows: tuple[GateRow, ...]
    handoff: HandoffRow


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_int(value: str | None) -> int:
    return int(value or 0)


def classify_domain(row: dict[str, str]) -> str:
    haystack = f"{row.get('file', '')} {row.get('repo_function', '')}".upper()
    for domain_id, terms in DOMAIN_RULES:
        if any(term in haystack for term in terms):
            return domain_id
    return "module-" + (row.get("file") or "unknown").split("/", 1)[0].lower()


def validate_upstream(repo: Path) -> None:
    handoff = read_csv(repo / UPSTREAM_HANDOFF)
    if len(handoff) != 1:
        raise ValueError("RE-274 handoff must contain exactly one row")
    expected = {
        "next_ticket": "TBD",
        "next_topic": "post-re267-domain-backlog-exhausted",
        "selected_domain": "none",
        "selected_pivot": "none",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if handoff[0].get(key) != value:
            raise ValueError(f"RE-274 handoff drift: {key}={handoff[0].get(key)!r}")


def remaining_selection_rows(repo: Path) -> tuple[SelectionRow, ...]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(repo / FUNCTION_PRIORITY):
        domain = classify_domain(row)
        if domain in CLOSED_DOMAINS or row.get("file") in CLOSED_FILES:
            continue
        grouped[domain].append(row)
    rows: list[SelectionRow] = []
    for domain, candidates in grouped.items():
        ranked = sorted(candidates, key=lambda r: (-parse_int(r.get("score")), r.get("file", ""), parse_int(r.get("line")), r.get("repo_function", "")))
        score = sum(parse_int(row.get("score")) for row in ranked[:8]) + len(ranked) * 25
        mapped_count = sum(1 for row in candidates if row.get("mapping_status") == "mapped")
        nd_count = sum(1 for row in candidates if row.get("nd") == "yes")
        runtime_count = sum(1 for row in candidates if row.get("runtime_focus") == "yes")
        rows.append(SelectionRow(
            rank=0,
            domain_id=domain,
            status="candidate",
            score=score,
            candidate_count=len(candidates),
            mapped_count=mapped_count,
            nd_count=nd_count,
            runtime_count=runtime_count,
            top_function=ranked[0].get("repo_function", ""),
            top_file=ranked[0].get("file", ""),
            next_ticket="",
            next_action="",
            code_change_readiness="blocked",
        ))
    rows.sort(key=lambda row: (-row.score, row.domain_id))
    ranked_rows = []
    for index, row in enumerate(rows, 1):
        selected = index == 1
        ranked_rows.append(SelectionRow(
            rank=index,
            domain_id=row.domain_id,
            status=row.status,
            score=row.score,
            candidate_count=row.candidate_count,
            mapped_count=row.mapped_count,
            nd_count=row.nd_count,
            runtime_count=row.runtime_count,
            top_function=row.top_function,
            top_file=row.top_file,
            next_ticket="RE-276" if selected else "TBD",
            next_action=(
                f"open RE-276 {row.domain_id} proof-first audit"
                if selected else "defer until animation-items closure"
            ),
            code_change_readiness="blocked",
        ))
    if [row.domain_id for row in ranked_rows] != ["animation-items", "module-spec_pc_n"]:
        raise ValueError(f"post-camera remaining domain drift: {[row.domain_id for row in ranked_rows]!r}")
    return tuple(ranked_rows)


def animation_priority_rows(repo: Path) -> list[dict[str, str]]:
    rows = [row for row in read_csv(repo / FUNCTION_PRIORITY) if classify_domain(row) == "animation-items"]
    if len(rows) != 31:
        raise ValueError(f"animation-items scope drifted: {len(rows)} rows")
    return rows


def subcluster_for(row: dict[str, str]) -> str:
    function = row.get("repo_function", "")
    file = row.get("file", "")
    if function in {"ReloadAnims", "DecodeAnim"}:
        return "runtime-reload"
    if function in {"CalcAnimatingItem_ASM", "CalcAllAnimatingItems_ASM", "DrawAllAnimatingItems_ASM", "AnimateLara"}:
        return "animitem-core"
    if function in {"AnimateWaterfalls", "InitialiseAnimatedTextures"}:
        return "texture-object-animation"
    if file == "SPEC_PSXPC_N/ANIMITEM.C":
        return "matrix-transform"
    raise ValueError(f"unclassified animation row: {function} {file}")


def build_epic(repo: Path) -> AnimationItemsEpic:
    repo = Path(repo)
    validate_upstream(repo)
    selection_rows = remaining_selection_rows(repo)
    rows = animation_priority_rows(repo)
    audit_rows = tuple(
        AuditRow(
            rank=i,
            domain_id="animation-items",
            subcluster=subcluster_for(row),
            function=row["repo_function"],
            file=row["file"],
            line=parse_int(row.get("line")),
            status=row.get("status", ""),
            mapped=row.get("mapping_status", ""),
            runtime_focus=row.get("runtime_focus", "no"),
            nd=row.get("nd", "no"),
            caller_count=parse_int(row.get("caller_count")),
            callee_count=parse_int(row.get("callee_count")),
            readiness="blocked",
            source_patch_ready="no",
            marker_ready="no",
            blocker=BLOCKER,
        )
        for i, row in enumerate(rows, 1)
    )
    grouped: dict[str, list[AuditRow]] = defaultdict(list)
    for row in audit_rows:
        grouped[row.subcluster].append(row)
    order = ["runtime-reload", "animitem-core", "matrix-transform", "texture-object-animation"]
    story_for = {
        "runtime-reload": "RE-277",
        "animitem-core": "RE-278",
        "matrix-transform": "RE-279",
        "texture-object-animation": "RE-279",
    }
    subcluster_rows = tuple(
        SubclusterRow(
            subcluster=name,
            rank=i,
            candidate_count=len(grouped[name]),
            mapped_count=sum(1 for row in grouped[name] if row.mapped == "mapped"),
            nd_count=sum(1 for row in grouped[name] if row.nd == "yes"),
            runtime_count=sum(1 for row in grouped[name] if row.runtime_focus == "yes"),
            top_function=grouped[name][0].function,
            outcome="blocked-no-patch",
            code_change_ready="no",
            marker_ready="no",
            blocker=BLOCKER,
            closed_by_story=story_for[name],
        )
        for i, name in enumerate(order, 1)
    )
    story_rows = (
        StoryRow("RE-275", "post-camera-domain-reprioritization", "remaining function-priority domains after RE-274", 31, "blocked", "no", "no", BLOCKER, SELECTION_CSV),
        StoryRow("RE-276", "animation-items-proof-first-audit", "animation-items domain scope from post-camera reprioritization", 31, "blocked", "no", "no", BLOCKER, AUDIT_CSV),
        StoryRow("RE-277", "animation-items-runtime-reload-chain", "ReloadAnims and DecodeAnim platform variants", 4, "blocked", "no", "no", BLOCKER, SUBCLUSTERS_CSV),
        StoryRow("RE-278", "animation-items-animitem-core-chain", "CalcAnimatingItem_ASM, CalcAllAnimatingItems_ASM, DrawAllAnimatingItems_ASM, AnimateLara", 4, "blocked", "no", "no", BLOCKER, SUBCLUSTERS_CSV),
        StoryRow("RE-279", "animation-items-matrix-transform-chain", "ANIMITEM matrix/interpolation helpers plus texture/object animation", 23, "blocked", "no", "no", BLOCKER, SUBCLUSTERS_CSV),
        StoryRow("RE-280", "animation-items-state-equivalence-gate", "animation item state/equivalence proof", 31, "blocked", "no", "no", BLOCKER, GATE_CSV),
        StoryRow("RE-281", "animation-items-source-patch-gate", "source patch and marker readiness", 31, "blocked", "no", "no", BLOCKER, GATE_CSV),
        StoryRow("RE-282", "post-animation-items-domain-handoff", "remaining domain after animation-items closure", 2, "blocked", "no", "no", BLOCKER, HANDOFF_CSV),
    )
    gate_rows = (
        GateRow("equivalence", "RE-280", "all animation-items candidates", 0, len(audit_rows), "deny", BLOCKER),
        GateRow("source-patch", "RE-281", "all animation-items candidates", 0, len(audit_rows), "deny", BLOCKER),
        GateRow("marker", "RE-281", "all animation-items candidates", 0, len(audit_rows), "deny", BLOCKER),
    )
    next_row = selection_rows[1]
    handoff = HandoffRow(
        next_ticket="TBD",
        next_topic="post-animation-items-domain-selection-needed",
        selected_domain=next_row.domain_id,
        selected_pivot=next_row.top_function,
        outcome="animation-items-closed-next-domain-unresolved-parser-artifact",
        reason="animation-items is closed; remaining domain is module-spec_pc_n, whose top row requires a parser-artifact reconciliation before opening a source patch epic",
        dependency="RE-275..RE-282 animation-items epic",
        code_change_readiness="blocked",
        stop_condition="open a post-animation-items selection/reconciliation gate before source changes",
    )
    return AnimationItemsEpic(
        story_range="RE-275..RE-282",
        upstream_ticket="RE-274",
        domain_id="animation-items",
        selected_pivot=selection_rows[0].top_function,
        raw_priority_count=len(rows),
        parser_artifact_count=0,
        candidate_count=len(rows),
        closed_candidate_count=len(rows),
        runtime_count=sum(1 for row in audit_rows if row.runtime_focus == "yes"),
        nd_count=sum(1 for row in audit_rows if row.nd == "yes"),
        code_change_ready_count=0,
        marker_ready_count=0,
        domain_outcome="documentation-only-terminal-blocker",
        blocker=BLOCKER,
        selection_rows=selection_rows,
        audit_rows=audit_rows,
        subcluster_rows=subcluster_rows,
        story_rows=story_rows,
        gate_rows=gate_rows,
        handoff=handoff,
    )


def write_rows(path: Path, rows: tuple[object, ...] | list[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    row_fields = [field.name for field in fields(rows[0])]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row_fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_markdown(path: Path, epic: AnimationItemsEpic) -> None:
    lines = [
        "# RE-275..RE-282 animation-items epic",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-274 post-camera handoff consumed.",
        "- [x] Remaining domains reprioritized from source-backed function-priority metadata.",
        "- [x] Animation-items source functions grouped into bounded proof subclusters.",
        "- [x] Equivalence/source-patch/marker gates denied with explicit blocker.",
        "",
        "## Decision",
        "",
        f"- Domain: `{epic.domain_id}`",
        f"- Pivot: `{epic.selected_pivot}`",
        f"- Raw priority rows: `{epic.raw_priority_count}`",
        f"- Runtime rows: `{epic.runtime_count}`",
        f"- ND rows: `{epic.nd_count}`",
        f"- Outcome: `{epic.domain_outcome}` — documentation-only terminal blocker",
        f"- Blocker: `{epic.blocker}`",
        f"- Recommended next ticket: `{epic.handoff.next_ticket}`",
        "",
        "No production source or marker change is authorized by this epic.",
        "",
        "## Subclusters",
        "",
    ]
    for row in epic.subcluster_rows:
        lines.append(f"- `{row.subcluster}`: {row.candidate_count} candidates; top `{row.top_function}`; readiness `blocked`.")
    lines.extend([
        "",
        "## Next handoff",
        "",
        f"- Selected domain: `{epic.handoff.selected_domain}`",
        f"- Selected pivot: `{epic.handoff.selected_pivot}`",
        f"- Stop condition: `{epic.handoff.stop_condition}`",
        "",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def story_text(row: StoryRow, epic: AnimationItemsEpic) -> str:
    return "\n".join([
        f"# {row.story_id} — {row.topic}",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        f"Advance `{row.topic}` for `{epic.domain_id}` without source or marker changes.",
        "",
        "## Progress tracker",
        "",
        "- [x] Upstream metadata consumed.",
        "- [x] Source-backed function/file/line metadata reviewed.",
        "- [x] Metadata-only artifacts emitted.",
        "- [x] Readiness and blockers recorded.",
        "",
        "## Scope",
        "",
        f"- Scope: `{row.scope}`",
        f"- Candidate count: `{row.candidate_count}`",
        f"- Artifact: `{row.artifact}`",
        "",
        "## Readiness",
        "",
        f"- Readiness: `{row.readiness}`",
        f"- Source patch ready: `{row.source_patch_ready}`",
        f"- Marker ready: `{row.marker_ready}`",
        f"- Blocker: `{row.blocker}`",
        "",
        "No production source or marker change is authorized by this story.",
        "",
    ])


def write_stories(base: Path, epic: AnimationItemsEpic) -> dict[str, Path]:
    out: dict[str, Path] = {}
    for row in epic.story_rows:
        path = base / f"docs/stories/{row.story_id}-{row.topic}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(story_text(row, epic), encoding="utf-8")
        out[row.story_id] = path
    return out


def write_story_index(path: Path, epic: AnimationItemsEpic) -> None:
    lines = [
        "# RE-275..RE-282 animation-items epic",
        "",
        "Status: Done",
        "",
        "## Progress tracker",
        "",
        "- [x] Post-camera domain reprioritization emitted.",
        "- [x] Animation item candidate scope audited.",
        "- [x] Subclusters closed as blocked documentation-only work.",
        "- [x] Next handoff emitted.",
        "",
        "## Stories",
        "",
    ]
    for row in epic.story_rows:
        lines.append(f"- `{row.story_id}` — `{row.topic}`: Readiness: `{row.readiness}`; candidates `{row.candidate_count}`.")
    lines.extend([
        "",
        "No production source or marker change is authorized by this epic.",
        "",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_all_artifacts(epic: AnimationItemsEpic, base: Path) -> dict[str, object]:
    base = Path(base)
    paths = {
        "selection_csv": base / SELECTION_CSV,
        "audit_csv": base / AUDIT_CSV,
        "subclusters_csv": base / SUBCLUSTERS_CSV,
        "epic_csv": base / EPIC_CSV,
        "gate_csv": base / GATE_CSV,
        "handoff_csv": base / HANDOFF_CSV,
        "md": base / MD_OUTPUT,
        "story_index": base / STORY_INDEX,
    }
    write_rows(paths["selection_csv"], epic.selection_rows)
    write_rows(paths["audit_csv"], epic.audit_rows)
    write_rows(paths["subclusters_csv"], epic.subcluster_rows)
    write_rows(paths["epic_csv"], epic.story_rows)
    write_rows(paths["gate_csv"], epic.gate_rows)
    write_rows(paths["handoff_csv"], (epic.handoff,))
    write_markdown(paths["md"], epic)
    write_story_index(paths["story_index"], epic)
    paths["stories"] = write_stories(base, epic)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    epic = build_epic(repo)
    write_all_artifacts(epic, repo)


if __name__ == "__main__":
    main()
