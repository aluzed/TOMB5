#!/usr/bin/env python3
"""Generate RE-261..RE-267 input epic artifacts."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import asdict, dataclass, fields
from pathlib import Path

UPSTREAM_HANDOFF = "docs/reverse/generated/re260-post-inventory-handoff.csv"
UPSTREAM_SELECTION = "docs/reverse/generated/re260-post-inventory-domain-selection.csv"
FUNCTION_PRIORITY = "docs/reverse/generated/function-priority.csv"

AUDIT_CSV = "docs/reverse/generated/re261-input-proof-first-audit.csv"
SUBCLUSTERS_CSV = "docs/reverse/generated/re261-input-subclusters.csv"
EPIC_CSV = "docs/reverse/generated/re261-re267-input-epic.csv"
GATE_CSV = "docs/reverse/generated/re266-input-source-patch-gates.csv"
NEXT_SELECTION_CSV = "docs/reverse/generated/re267-post-input-domain-selection.csv"
HANDOFF_CSV = "docs/reverse/generated/re267-post-input-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re261-re267-input-epic.md"
STORY_INDEX = "docs/stories/RE-261-RE-267-input-epic.md"

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
    "inventory closed",
    "post-inventory",
    "s_callinventory2",
    "open re-261 input proof-first audit",
    "lara-combat",
)
BLOCKER = "missing-input-cross-platform-state-contract-and-non-raw-equivalence-proof"

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
CLOSED_DOMAINS = {"input"}


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
class InputEpic:
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
    audit_rows: tuple[AuditRow, ...]
    subcluster_rows: tuple[SubclusterRow, ...]
    story_rows: tuple[StoryRow, ...]
    gate_rows: tuple[GateRow, ...]
    next_domain_rows: tuple[NextDomainRow, ...]
    handoff: HandoffRow


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_int(value: str | None) -> int:
    return int(value or 0)


def classify_domain(row: dict[str, str]) -> str:
    haystack = f"{row.get('file', '')} {row.get('repo_function', '')} {row.get('top_file', '')} {row.get('top_function', '')}".upper()
    for domain_id, terms in DOMAIN_RULES:
        if any(term in haystack for term in terms):
            return domain_id
    return "module-" + (row.get("file") or row.get("top_file") or "unknown").split("/", 1)[0].lower()


def subcluster_for(row: dict[str, str]) -> str:
    file_name = row.get("file", "")
    if file_name == "SPEC_PSXPC_N/PSXINPUT.C":
        return "psxpc-n-runtime"
    if file_name == "SPEC_PSX/PSXINPUT.C":
        return "psx-runtime"
    if file_name == "SPEC_PSXPC/PSXPCINPUT.C":
        return "psxpc-service"
    raise ValueError(f"unclassified input row: {row.get('repo_function', '')} {file_name}")


def validate_upstream(repo: Path) -> None:
    handoff = read_csv(repo / UPSTREAM_HANDOFF)
    if len(handoff) != 1:
        raise ValueError("RE-260 handoff must contain exactly one row")
    expected = {
        "next_ticket": "RE-261",
        "next_topic": "input-proof-first-audit",
        "selected_domain": "input",
        "selected_pivot": "S_UpdateInput",
    }
    for key, value in expected.items():
        if handoff[0].get(key) != value:
            raise ValueError(f"RE-260 handoff drift: {key}={handoff[0].get(key)!r}")
    selection = read_csv(repo / UPSTREAM_SELECTION)
    if not selection or selection[0].get("domain_id") != "input":
        raise ValueError("RE-260 selection must rank input first")
    if selection[0].get("top_function") != "S_UpdateInput" or parse_int(selection[0].get("candidate_count")) != 3:
        raise ValueError("RE-260 selected input scope drifted")


def input_priority_rows(repo: Path) -> list[dict[str, str]]:
    rows = [row for row in read_csv(repo / FUNCTION_PRIORITY) if classify_domain(row) == "input"]
    expected = [
        ("S_UpdateInput", "SPEC_PSXPC_N/PSXINPUT.C"),
        ("S_UpdateInput", "SPEC_PSX/PSXINPUT.C"),
        ("S_UpdateInput", "SPEC_PSXPC/PSXPCINPUT.C"),
    ]
    observed = [(row["repo_function"], row["file"]) for row in rows]
    if observed != expected:
        raise ValueError(f"input scope drifted: {observed!r}")
    return rows


def build_next_domain_rows(repo: Path) -> tuple[NextDomainRow, ...]:
    source_rows = read_csv(repo / UPSTREAM_SELECTION)
    out: list[NextDomainRow] = []
    for row in source_rows:
        if row.get("domain_id") in CLOSED_DOMAINS:
            continue
        rank = len(out) + 1
        domain = row["domain_id"]
        is_next = rank == 1
        out.append(
            NextDomainRow(
                rank=rank,
                domain_id=domain,
                status=row.get("status", "candidate"),
                score=parse_int(row.get("score")),
                candidate_count=parse_int(row.get("candidate_count")),
                mapped_count=parse_int(row.get("mapped_count")),
                nd_count=parse_int(row.get("nd_count")),
                runtime_count=parse_int(row.get("runtime_count")),
                top_function=row.get("top_function", ""),
                top_file=row.get("top_file", ""),
                next_ticket="RE-268" if is_next else "TBD",
                next_action=(
                    f"open RE-268 {domain} proof-first audit"
                    if is_next
                    else "defer until higher-ranked post-input domain is selected"
                ),
                code_change_readiness="blocked",
            )
        )
    if not out or out[0].domain_id != "camera" or out[0].top_function != "CalculateSpotCams":
        raise ValueError("post-input next-domain selection drifted")
    return tuple(out)


def build_epic(repo: Path) -> InputEpic:
    validate_upstream(repo)
    rows = input_priority_rows(repo)
    audit_rows = tuple(
        AuditRow(
            rank=i,
            domain_id="input",
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
    order = ["psxpc-n-runtime", "psx-runtime", "psxpc-service"]
    story_for = {"psxpc-n-runtime": "RE-262", "psx-runtime": "RE-263", "psxpc-service": "RE-264"}
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
        StoryRow("RE-261", "input-proof-first-audit", "input domain scope from RE-260 handoff", 3, "blocked", "no", "no", BLOCKER, AUDIT_CSV),
        StoryRow("RE-262", "input-psxpc-n-runtime-chain", "SPEC_PSXPC_N S_UpdateInput runtime row", 1, "blocked", "no", "no", BLOCKER, SUBCLUSTERS_CSV),
        StoryRow("RE-263", "input-psx-runtime-chain", "SPEC_PSX S_UpdateInput runtime row", 1, "blocked", "no", "no", BLOCKER, SUBCLUSTERS_CSV),
        StoryRow("RE-264", "input-psxpc-service-chain", "SPEC_PSXPC S_UpdateInput service row", 1, "blocked", "no", "no", BLOCKER, SUBCLUSTERS_CSV),
        StoryRow("RE-265", "input-state-equivalence-gate", "cross-platform input state/equivalence proof", 3, "blocked", "no", "no", BLOCKER, GATE_CSV),
        StoryRow("RE-266", "input-source-patch-gate", "source patch and marker readiness", 3, "blocked", "no", "no", BLOCKER, GATE_CSV),
        StoryRow("RE-267", "post-input-domain-selection", "remaining ranked domains after input closure", 0, "blocked", "no", "no", BLOCKER, NEXT_SELECTION_CSV),
    )
    gate_rows = (
        GateRow("equivalence", "RE-265", "all input candidates", 0, len(audit_rows), "deny", BLOCKER),
        GateRow("source-patch", "RE-266", "all input candidates", 0, len(audit_rows), "deny", BLOCKER),
        GateRow("marker", "RE-266", "all input candidates", 0, len(audit_rows), "deny", BLOCKER),
    )
    next_rows = build_next_domain_rows(repo)
    handoff = HandoffRow(
        next_ticket="RE-268",
        next_topic="camera-proof-first-audit",
        selected_domain=next_rows[0].domain_id,
        selected_pivot=next_rows[0].top_function,
        outcome="input-closed-next-domain-selected",
        reason="input closed as a documentation-only terminal blocker after cross-platform state proof remained absent; next ranked remaining domain selected",
        dependency="RE-261..RE-267 input epic",
        code_change_readiness="blocked",
        stop_condition="camera proof-first audit emitted",
    )
    return InputEpic(
        story_range="RE-261..RE-267",
        upstream_ticket="RE-260",
        domain_id="input",
        selected_pivot="S_UpdateInput",
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
        audit_rows=audit_rows,
        subcluster_rows=subcluster_rows,
        story_rows=story_rows,
        gate_rows=gate_rows,
        next_domain_rows=next_rows,
        handoff=handoff,
    )


def write_csv(path: Path, rows: tuple[object, ...]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        if not rows:
            raise ValueError(f"no rows for {path}")
        writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(rows[0])], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
    return path


def write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def render_md(epic: InputEpic) -> str:
    lines = [
        "# RE-261..RE-267 input epic",
        "",
        "Domain: `input`",
        "Pivot: `S_UpdateInput`",
        "Outcome: `documentation-only-terminal-blocker`",
        f"Blocker: `{epic.blocker}`",
        f"Raw priority rows: `{epic.raw_priority_count}`",
        f"Runtime rows: `{epic.runtime_count}`",
        f"Candidates closed/documented: `{epic.closed_candidate_count}` / `{epic.candidate_count}`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-260 handoff consumed.",
        "- [x] Proof-first audit emitted.",
        "- [x] Cross-platform input variants scoped separately.",
        "- [x] State/equivalence and patch gates denied with zero ready rows.",
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
        "This is a documentation-only terminal blocker for input. No production source or marker change is authorized.",
        "",
        "## Next domain",
        "",
        "Next proof domain: `camera`",
        "Selected pivot: `CalculateSpotCams`",
        "Recommended next ticket: `RE-268`",
        "",
    ])
    return "\n".join(lines)


def render_story_index(epic: InputEpic) -> str:
    return "\n".join([
        "# RE-261..RE-267 input epic",
        "",
        "## Progress tracker",
        "",
        "- [x] Upstream handoff validated.",
        "- [x] Input scope generated.",
        "- [x] Cross-platform variants reconciled.",
        "- [x] Source patch gate denied.",
        "- [x] Next domain selected.",
        "",
        f"Readiness: `{epic.domain_outcome}`",
        "No production source or marker change is authorized.",
        "",
    ])


def render_story(row: StoryRow) -> str:
    return "\n".join([
        f"# {row.story_id} {row.topic}",
        "",
        "## Progress tracker",
        "",
        "- [x] Inputs consumed.",
        "- [x] Metadata-only artifact generated.",
        "- [x] Readiness recorded.",
        "",
        f"Scope: `{row.scope}`",
        f"Readiness: `{row.readiness}`",
        f"Source patch ready: `{row.source_patch_ready}`",
        f"Marker ready: `{row.marker_ready}`",
        f"Blocker: `{row.blocker}`",
        f"Artifact: `{row.artifact}`",
        "",
        "No production source or marker change is authorized.",
        "",
    ])


def assert_metadata_only(paths: list[Path]) -> None:
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN + STALE_FRAGMENTS:
            if fragment in text:
                raise ValueError(f"forbidden or stale fragment {fragment!r} in {path}")


def write_all_artifacts(epic: InputEpic, repo: Path) -> dict[str, object]:
    written: dict[str, object] = {}
    written["audit_csv"] = write_csv(repo / AUDIT_CSV, epic.audit_rows)
    written["subclusters_csv"] = write_csv(repo / SUBCLUSTERS_CSV, epic.subcluster_rows)
    written["epic_csv"] = write_csv(repo / EPIC_CSV, epic.story_rows)
    written["gate_csv"] = write_csv(repo / GATE_CSV, epic.gate_rows)
    written["next_selection_csv"] = write_csv(repo / NEXT_SELECTION_CSV, epic.next_domain_rows)
    written["handoff_csv"] = write_csv(repo / HANDOFF_CSV, (epic.handoff,))
    written["md"] = write_text(repo / MD_OUTPUT, render_md(epic))
    written["story_index"] = write_text(repo / STORY_INDEX, render_story_index(epic))
    story_paths: dict[str, Path] = {}
    for row in epic.story_rows:
        story_paths[row.story_id] = write_text(repo / f"docs/stories/{row.story_id}-{row.topic}.md", render_story(row))
    written["stories"] = story_paths
    all_paths = [p for key, value in written.items() if key != "stories" for p in [value]] + list(story_paths.values())
    assert_metadata_only(all_paths)
    return written


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    epic = build_epic(args.repo)
    write_all_artifacts(epic, args.repo)


if __name__ == "__main__":
    main()
