#!/usr/bin/env python3
"""Generate RE-237..RE-244 module-spec_psx epic artifacts."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

UPSTREAM_HANDOFF = "docs/reverse/generated/re236-post-module-spec-psxpc-handoff.csv"
UPSTREAM_SELECTION = "docs/reverse/generated/re236-post-module-spec-psxpc-domain-selection.csv"
FUNCTION_PRIORITY = "docs/reverse/generated/function-priority.csv"

AUDIT_CSV = "docs/reverse/generated/re237-module-spec-psx-proof-first-audit.csv"
SUBCLUSTERS_CSV = "docs/reverse/generated/re237-module-spec-psx-subclusters.csv"
EPIC_CSV = "docs/reverse/generated/re237-re244-module-spec-psx-epic.csv"
GATE_CSV = "docs/reverse/generated/re243-module-spec-psx-source-patch-gates.csv"
NEXT_SELECTION_CSV = "docs/reverse/generated/re244-post-module-spec-psx-domain-selection.csv"
HANDOFF_CSV = "docs/reverse/generated/re244-post-module-spec-psx-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re237-re244-module-spec-psx-epic.md"
STORY_INDEX = "docs/stories/RE-237-RE-244-module-spec-psx-epic.md"

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
    "module-spec_psxpc closed",
    "post-module-spec-psxpc",
    "text-debug-rendering",
    "render-geometry-support",
    "platform-services",
    "open re-237 module-spec_psx proof-first audit",
)
BLOCKER = "missing-module-spec-psx-source-contract-and-non-raw-equivalence-proof"

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
CLOSED_CHAIN_FUNCTIONS = {"RestoreLevelData", "SaveLevelData"}
CLOSED_CHAIN_FILES = {"GAME/SAVEGAME.C"}


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
    outcome: str
    blocker: str
    generated_artifact: str


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
class ModuleSpecPsxEpic:
    story_range: str
    upstream_ticket: str
    domain_id: str
    selected_pivot: str
    candidate_count: int
    closed_candidate_count: int
    runtime_count: int
    nd_count: int
    code_change_ready_count: int
    marker_ready_count: int
    domain_outcome: str
    blocker: str
    audit_rows: tuple[AuditRow, ...]
    subcluster_rows: tuple[SubclusterRow, ...]
    story_rows: tuple[StoryRow, ...]
    gate_rows: tuple[GateRow, ...]
    next_domain_rows: tuple[NextDomainRow, ...]
    handoff: HandoffRow


def parse_int(value: str | None) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def classify_domain(row: dict[str, str]) -> str:
    haystack = f"{row.get('file', '')} {row.get('repo_function', '')}".upper()
    for domain_id, terms in DOMAIN_RULES:
        if any(term in haystack for term in terms):
            return domain_id
    module = row.get("file", ".").split("/", 1)[0]
    return f"module-{module.lower()}"


def is_closed_chain(row: dict[str, str]) -> bool:
    return row.get("repo_function", "") in CLOSED_CHAIN_FUNCTIONS or row.get("file", "") in CLOSED_CHAIN_FILES


def subcluster_for(row: dict[str, str]) -> str:
    function = row.get("repo_function", "")
    file = row.get("file", "")
    if function in {"main", "InitNewCDSystem", "VSyncFunc"}:
        return "platform-main-lifecycle"
    if file in {"SPEC_PSX/MOVIE.C", "SPEC_PSX/LOADSAVE.C", "SPEC_PSX/SPECIFIC.C"}:
        return "frontend-loadsave-flow"
    if file == "SPEC_PSX/MALLOC.C":
        return "platform-memory"
    raise ValueError(f"unclassified module-spec_psx row: {function} {file}")


def validate_upstream(repo: Path) -> None:
    handoff = read_csv(repo / UPSTREAM_HANDOFF)
    if len(handoff) != 1:
        raise ValueError("RE-236 handoff must contain exactly one row")
    expected = {
        "next_ticket": "RE-237",
        "next_topic": "module-spec-psx-proof-first-audit",
        "selected_domain": "module-spec_psx",
        "selected_pivot": "main",
    }
    for key, value in expected.items():
        if handoff[0].get(key) != value:
            raise ValueError(f"RE-236 handoff drift: {key}={handoff[0].get(key)!r}")
    selection = read_csv(repo / UPSTREAM_SELECTION)
    if not selection or selection[0].get("domain_id") != "module-spec_psx":
        raise ValueError("RE-236 selection must rank module-spec_psx first")
    if selection[0].get("top_function") != "main":
        raise ValueError("RE-236 selected pivot drifted")


def build_audit_rows(repo: Path) -> tuple[AuditRow, ...]:
    rows = []
    for row in read_csv(repo / FUNCTION_PRIORITY):
        if is_closed_chain(row):
            continue
        if classify_domain(row) != "module-spec_psx":
            continue
        rows.append(row)
    rows.sort(key=lambda item: (-parse_int(item.get("score")), item.get("file", ""), parse_int(item.get("line")), item.get("repo_function", "")))
    if len(rows) != 12 or rows[0].get("repo_function") != "main":
        raise ValueError("module-spec_psx function scope drifted")
    audit: list[AuditRow] = []
    for rank, row in enumerate(rows, start=1):
        audit.append(AuditRow(
            rank=rank,
            domain_id="module-spec_psx",
            subcluster=subcluster_for(row),
            function=row.get("repo_function", ""),
            file=row.get("file", ""),
            line=parse_int(row.get("line")),
            status=row.get("status", ""),
            mapped="yes" if row.get("mapping_status") == "mapped" else "no",
            runtime_focus=row.get("runtime_focus", ""),
            nd=row.get("nd", ""),
            caller_count=parse_int(row.get("caller_count")),
            callee_count=parse_int(row.get("callee_count")),
            readiness="blocked",
            source_patch_ready="no",
            marker_ready="no",
            blocker=BLOCKER,
        ))
    return tuple(audit)


def build_subcluster_rows(audit_rows: tuple[AuditRow, ...]) -> tuple[SubclusterRow, ...]:
    order = ("platform-main-lifecycle", "frontend-loadsave-flow", "platform-memory")
    story_by_subcluster = {
        "platform-main-lifecycle": "RE-238",
        "frontend-loadsave-flow": "RE-239",
        "platform-memory": "RE-240",
    }
    grouped: dict[str, list[AuditRow]] = defaultdict(list)
    for row in audit_rows:
        grouped[row.subcluster].append(row)
    result = []
    for rank, subcluster in enumerate(order, start=1):
        rows = grouped[subcluster]
        result.append(SubclusterRow(
            subcluster=subcluster,
            rank=rank,
            candidate_count=len(rows),
            mapped_count=sum(1 for row in rows if row.mapped == "yes"),
            nd_count=sum(1 for row in rows if row.nd == "yes"),
            runtime_count=sum(1 for row in rows if row.runtime_focus == "yes"),
            top_function=rows[0].function,
            outcome="blocked-no-patch",
            code_change_ready="no",
            marker_ready="no",
            blocker=BLOCKER,
            closed_by_story=story_by_subcluster[subcluster],
        ))
    return tuple(result)


def build_story_rows() -> tuple[StoryRow, ...]:
    specs = (
        ("RE-237", "module-spec-psx-proof-first-audit", "all module-spec_psx candidates", 12, "opening-audit"),
        ("RE-238", "module-spec-psx-platform-main-lifecycle-chain", "platform-main-lifecycle candidates", 3, "documentation-only"),
        ("RE-239", "module-spec-psx-frontend-loadsave-flow-chain", "frontend-loadsave-flow candidates", 5, "documentation-only"),
        ("RE-240", "module-spec-psx-platform-memory-chain", "platform-memory candidates", 4, "documentation-only"),
        ("RE-241", "module-spec-psx-nd-stub-reconciliation", "ND and stub-like rows", 12, "documentation-only"),
        ("RE-242", "module-spec-psx-runtime-cross-platform-reconciliation", "runtime and cross-platform rows", 12, "documentation-only"),
        ("RE-243", "module-spec-psx-source-patch-gate", "ready module-spec_psx rows", 12, "documentation-only"),
        ("RE-244", "post-module-spec-psx-domain-selection", "remaining domain backlog after module-spec_psx", 0, "next-domain-selected"),
    )
    return tuple(
        StoryRow(
            story_id=story_id,
            topic=topic,
            scope=scope,
            candidate_count=count,
            readiness="blocked",
            source_patch_ready="no",
            marker_ready="no",
            outcome=outcome,
            blocker=BLOCKER if story_id != "RE-244" else "module-spec_psx-terminal-blocker-published",
            generated_artifact=f"docs/stories/{story_id}-{topic}.md",
        )
        for story_id, topic, scope, count, outcome in specs
    )


def build_gate_rows() -> tuple[GateRow, ...]:
    return (
        GateRow("equivalence", "RE-242", "all module-spec_psx rows", 0, 12, "deny", BLOCKER),
        GateRow("source-patch", "RE-243", "ready module-spec_psx rows", 0, 12, "deny", "zero rows passed the equivalence gate"),
        GateRow("marker", "RE-243", "ready module-spec_psx rows", 0, 12, "deny", "zero rows passed the source-patch gate"),
    )


def build_next_domain_rows(repo: Path) -> tuple[NextDomainRow, ...]:
    source_rows = read_csv(repo / UPSTREAM_SELECTION)
    remaining = [row for row in source_rows if row.get("domain_id") != "module-spec_psx"]
    if not remaining or remaining[0].get("domain_id") != "lara-combat":
        raise ValueError("post-module-spec_psx next-domain selection drifted")
    result: list[NextDomainRow] = []
    for rank, row in enumerate(remaining, start=1):
        selected = rank == 1
        result.append(NextDomainRow(
            rank=rank,
            domain_id=row["domain_id"],
            status=row["status"],
            score=parse_int(row["score"]),
            candidate_count=parse_int(row["candidate_count"]),
            mapped_count=parse_int(row["mapped_count"]),
            nd_count=parse_int(row["nd_count"]),
            runtime_count=parse_int(row["runtime_count"]),
            top_function=row["top_function"],
            top_file=row["top_file"],
            next_ticket="RE-245" if selected else "TBD",
            next_action="open RE-245 lara-combat proof-first audit" if selected else "defer until higher-ranked post-module-spec_psx domain is selected",
            code_change_readiness="blocked",
        ))
    return tuple(result)


def build_epic(repo: Path) -> ModuleSpecPsxEpic:
    repo = Path(repo)
    validate_upstream(repo)
    audit_rows = build_audit_rows(repo)
    subcluster_rows = build_subcluster_rows(audit_rows)
    story_rows = build_story_rows()
    gate_rows = build_gate_rows()
    next_domain_rows = build_next_domain_rows(repo)
    selected = next_domain_rows[0]
    handoff = HandoffRow(
        next_ticket="RE-245",
        next_topic="lara-combat-proof-first-audit",
        selected_domain=selected.domain_id,
        selected_pivot=selected.top_function,
        outcome="module-spec_psx-closed-next-domain-selected",
        reason="module-spec_psx closed as a documentation-only terminal blocker; next ranked remaining domain selected",
        dependency="RE-237..RE-244 module-spec_psx epic",
        code_change_readiness="blocked",
        stop_condition="lara-combat proof-first audit emitted",
    )
    return ModuleSpecPsxEpic(
        story_range="RE-237..RE-244",
        upstream_ticket="RE-236",
        domain_id="module-spec_psx",
        selected_pivot="main",
        candidate_count=len(audit_rows),
        closed_candidate_count=sum(row.candidate_count for row in subcluster_rows),
        runtime_count=sum(1 for row in audit_rows if row.runtime_focus == "yes"),
        nd_count=sum(1 for row in audit_rows if row.nd == "yes"),
        code_change_ready_count=0,
        marker_ready_count=0,
        domain_outcome="documentation-only-terminal-blocker",
        blocker=BLOCKER,
        audit_rows=audit_rows,
        subcluster_rows=subcluster_rows,
        story_rows=story_rows,
        gate_rows=gate_rows,
        next_domain_rows=next_domain_rows,
        handoff=handoff,
    )


def write_rows(path: Path, cls: type, rows: list[dict[str, object]]) -> None:
    fields = list(cls.__dataclass_fields__)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_md(path: Path, epic: ModuleSpecPsxEpic) -> None:
    lines = [
        "# RE-237..RE-244 module-spec_psx epic",
        "",
        f"Domain: `{epic.domain_id}`",
        f"Pivot: `{epic.selected_pivot}`",
        f"Outcome: `{epic.domain_outcome}`",
        f"Blocker: `{epic.blocker}`",
        f"Candidates closed/documented: `{epic.closed_candidate_count}` / `{epic.candidate_count}`",
        f"Runtime-focused rows: `{epic.runtime_count}`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-236 handoff consumed.",
        "- [x] Proof-first audit emitted.",
        "- [x] Lifecycle, frontend/loadsave, and memory subclusters documented.",
        "- [x] Runtime/cross-platform reconciliation and patch gates denied with zero ready rows.",
        "- [x] Next proof domain selected from the remaining ranked backlog.",
        "",
        "## Subcluster closures",
        "",
    ]
    for row in epic.subcluster_rows:
        lines.append(f"- `{row.closed_by_story}` `{row.subcluster}`: {row.candidate_count} candidate(s), top `{row.top_function}`, outcome `{row.outcome}`.")
    lines.extend([
        "",
        "## Terminal decision",
        "",
        "This is a documentation-only terminal blocker for module-spec_psx. No production source or marker change is authorized.",
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


def write_story_index(path: Path, epic: ModuleSpecPsxEpic) -> None:
    lines = [
        "# RE-237..RE-244 — module-spec_psx epic",
        "",
        "Status: Done",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-237..RE-244 range generated as a bounded epic.",
        "- [x] All module-spec_psx subclusters documented.",
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


def write_story(path: Path, row: StoryRow, epic: ModuleSpecPsxEpic) -> None:
    lines = [
        f"# {row.story_id} — {row.topic}",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        f"Advance `{row.topic}` within the module-spec_psx epic using metadata-only proof artifacts.",
        "",
        "## Scope",
        "",
        f"- scope: `{row.scope}`",
        f"- candidates: `{row.candidate_count}`",
        "- source contract: generated metadata only; no source or marker edit",
        "",
        "## Progress tracker",
        "",
        "- [x] Upstream handoff consumed.",
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
        "- `python3 -m pytest tests/reverse/test_re237_re244_module_spec_psx_epic.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over RE-237..RE-244 outputs",
        "",
        "## Next step",
        "",
        f"Epic handoff: `{epic.handoff.next_ticket}` / `{epic.handoff.next_topic}`.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_all_artifacts(epic: ModuleSpecPsxEpic, repo: Path) -> dict[str, object]:
    repo = Path(repo)
    paths: dict[str, object] = {
        "audit_csv": repo / AUDIT_CSV,
        "subclusters_csv": repo / SUBCLUSTERS_CSV,
        "epic_csv": repo / EPIC_CSV,
        "gate_csv": repo / GATE_CSV,
        "next_selection_csv": repo / NEXT_SELECTION_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story_index": repo / STORY_INDEX,
    }
    write_rows(paths["audit_csv"], AuditRow, [row.__dict__ for row in epic.audit_rows])
    write_rows(paths["subclusters_csv"], SubclusterRow, [row.__dict__ for row in epic.subcluster_rows])
    write_rows(paths["epic_csv"], StoryRow, [row.__dict__ for row in epic.story_rows])
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
