#!/usr/bin/env python3
"""Generate RE-283..RE-287 module-spec_pc_n reconciliation artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

UPSTREAM_HANDOFF = "docs/reverse/generated/re282-post-animation-items-handoff.csv"
UPSTREAM_SELECTION = "docs/reverse/generated/re275-post-camera-domain-reprioritization.csv"
FUNCTION_PRIORITY = "docs/reverse/generated/function-priority.csv"

PARSER_ARTIFACTS_CSV = "docs/reverse/generated/re283-module-spec-pc-n-parser-artifacts.csv"
AUDIT_CSV = "docs/reverse/generated/re284-module-spec-pc-n-decodetrack-audit.csv"
EPIC_CSV = "docs/reverse/generated/re283-re287-module-spec-pc-n-epic.csv"
GATE_CSV = "docs/reverse/generated/re285-re286-module-spec-pc-n-gates.csv"
HANDOFF_CSV = "docs/reverse/generated/re287-post-module-spec-pc-n-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re283-re287-module-spec-pc-n-epic.md"
STORY_INDEX = "docs/stories/RE-283-RE-287-module-spec-pc-n-epic.md"

FORBIDDEN = (
    "word_le_hex", "payload_offset", "dump row", "opcode", "machine word",
    "call_address", "branch target", "call target", "0x800",
)
STALE_FRAGMENTS = (
    "calc animatingitem", "animation-items closed", "open re-276",
    "camera closed", "post-re267", "inventory",
)
BLOCKER = "missing-module-spec-pc-n-decodetrack-state-contract-and-non-raw-equivalence-proof"


@dataclass(frozen=True)
class ParserArtifactRow:
    rank: int
    domain_id: str
    function: str
    file: str
    line: int
    classification: str
    reason: str
    disposition: str


@dataclass(frozen=True)
class AuditRow:
    rank: int
    domain_id: str
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
class ModuleSpecPcNEpic:
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
    parser_artifact_rows: tuple[ParserArtifactRow, ...]
    audit_rows: tuple[AuditRow, ...]
    story_rows: tuple[StoryRow, ...]
    gate_rows: tuple[GateRow, ...]
    handoff: HandoffRow


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_int(value: str | None) -> int:
    return int(value or 0)


def validate_upstream(repo: Path) -> None:
    handoff = read_csv(repo / UPSTREAM_HANDOFF)
    if len(handoff) != 1:
        raise ValueError("RE-282 handoff must contain exactly one row")
    expected = {
        "next_ticket": "TBD",
        "next_topic": "post-animation-items-domain-selection-needed",
        "selected_domain": "module-spec_pc_n",
        "selected_pivot": "if",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if handoff[0].get(key) != value:
            raise ValueError(f"RE-282 handoff drift: {key}={handoff[0].get(key)!r}")
    selection = read_csv(repo / UPSTREAM_SELECTION)
    selected = [row for row in selection if row.get("domain_id") == "module-spec_pc_n"]
    if len(selected) != 1 or selected[0].get("top_function") != "if" or parse_int(selected[0].get("candidate_count")) != 2:
        raise ValueError("post-camera module-spec_pc_n selection drifted")


def module_spec_pc_n_rows(repo: Path) -> list[dict[str, str]]:
    rows = [row for row in read_csv(repo / FUNCTION_PRIORITY) if row.get("file") == "SPEC_PC_N/SPECIFIC.CPP" and row.get("repo_function") in {"if", "DecodeTrack"}]
    observed = [row.get("repo_function") for row in rows]
    if observed != ["if", "DecodeTrack"]:
        raise ValueError(f"module-spec_pc_n scope drifted: {observed!r}")
    return rows


def build_epic(repo: Path) -> ModuleSpecPcNEpic:
    repo = Path(repo)
    validate_upstream(repo)
    rows = module_spec_pc_n_rows(repo)
    parser_source = rows[0]
    candidate_source = rows[1]
    parser_rows = (
        ParserArtifactRow(
            rank=1,
            domain_id="module-spec_pc_n",
            function=parser_source["repo_function"],
            file=parser_source["file"],
            line=parse_int(parser_source.get("line")),
            classification="parser-artifact",
            reason="C keyword captured by source scanner rather than a callable function boundary",
            disposition="exclude-from-source-patch-scope",
        ),
    )
    audit_rows = (
        AuditRow(
            rank=1,
            domain_id="module-spec_pc_n",
            function=candidate_source["repo_function"],
            file=candidate_source["file"],
            line=parse_int(candidate_source.get("line")),
            status=candidate_source.get("status", ""),
            mapped=candidate_source.get("mapping_status", ""),
            runtime_focus=candidate_source.get("runtime_focus", "no"),
            nd=candidate_source.get("nd", "no"),
            caller_count=parse_int(candidate_source.get("caller_count")),
            callee_count=parse_int(candidate_source.get("callee_count")),
            readiness="blocked",
            source_patch_ready="no",
            marker_ready="no",
            blocker=BLOCKER,
        ),
    )
    story_rows = (
        StoryRow("RE-283", "module-spec-pc-n-parser-reconciliation", "exclude parser-artifact keyword row and retain DecodeTrack", 1, "blocked", "no", "no", BLOCKER, PARSER_ARTIFACTS_CSV),
        StoryRow("RE-284", "module-spec-pc-n-decodetrack-audit", "SPEC_PC_N DecodeTrack source-backed audit", 1, "blocked", "no", "no", BLOCKER, AUDIT_CSV),
        StoryRow("RE-285", "module-spec-pc-n-state-equivalence-gate", "DecodeTrack state/equivalence proof", 1, "blocked", "no", "no", BLOCKER, GATE_CSV),
        StoryRow("RE-286", "module-spec-pc-n-source-patch-gate", "source patch and marker readiness", 1, "blocked", "no", "no", BLOCKER, GATE_CSV),
        StoryRow("RE-287", "post-module-spec-pc-n-exhaustion", "remaining domains after module-spec_pc_n closure", 0, "blocked", "no", "no", BLOCKER, HANDOFF_CSV),
    )
    gate_rows = (
        GateRow("equivalence", "RE-285", "DecodeTrack", 0, 1, "deny", BLOCKER),
        GateRow("source-patch", "RE-286", "DecodeTrack", 0, 1, "deny", BLOCKER),
        GateRow("marker", "RE-286", "DecodeTrack", 0, 1, "deny", BLOCKER),
    )
    handoff = HandoffRow(
        next_ticket="TBD",
        next_topic="post-animation-items-domain-backlog-exhausted",
        selected_domain="none",
        selected_pivot="none",
        outcome="module-spec-pc-n-closed-domain-backlog-exhausted",
        reason="module-spec_pc_n parser artifact reconciled and DecodeTrack closed; no remaining ranked domains after the post-animation-items backlog",
        dependency="RE-283..RE-287 module-spec_pc_n epic",
        code_change_readiness="blocked",
        stop_condition="no ranked remaining domain in post-animation-items selection",
    )
    return ModuleSpecPcNEpic(
        story_range="RE-283..RE-287",
        upstream_ticket="RE-282",
        domain_id="module-spec_pc_n",
        selected_pivot="DecodeTrack",
        raw_priority_count=len(rows),
        parser_artifact_count=len(parser_rows),
        candidate_count=len(audit_rows),
        closed_candidate_count=len(audit_rows),
        runtime_count=sum(1 for row in audit_rows if row.runtime_focus == "yes"),
        nd_count=sum(1 for row in audit_rows if row.nd == "yes"),
        code_change_ready_count=0,
        marker_ready_count=0,
        domain_outcome="documentation-only-terminal-blocker",
        blocker=BLOCKER,
        parser_artifact_rows=parser_rows,
        audit_rows=audit_rows,
        story_rows=story_rows,
        gate_rows=gate_rows,
        handoff=handoff,
    )


def write_rows(path: Path, rows: tuple[object, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    row_fields = [field.name for field in fields(rows[0])]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row_fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_markdown(path: Path, epic: ModuleSpecPcNEpic) -> None:
    lines = [
        "# RE-283..RE-287 module-spec_pc_n epic",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-282 post-animation-items handoff consumed.",
        "- [x] Parser-artifact row reconciled before source scope selection.",
        "- [x] DecodeTrack source-backed metadata audited.",
        "- [x] Equivalence/source-patch/marker gates denied with explicit blocker.",
        "",
        "## Decision",
        "",
        f"- Domain: `{epic.domain_id}`",
        f"- Pivot after reconciliation: `{epic.selected_pivot}`",
        f"- Raw priority rows: `{epic.raw_priority_count}`",
        f"- Parser artifacts excluded: `{epic.parser_artifact_count}`",
        f"- Real candidates: `{epic.candidate_count}`",
        f"- Outcome: `{epic.domain_outcome}` — documentation-only terminal blocker",
        f"- Blocker: `{epic.blocker}`",
        f"- Recommended next ticket: `{epic.handoff.next_ticket}`",
        "",
        "No production source or marker change is authorized by this epic.",
        "",
        "## Handoff",
        "",
        f"- Next topic: `{epic.handoff.next_topic}`",
        f"- Selected domain: `{epic.handoff.selected_domain}`",
        f"- Stop condition: `{epic.handoff.stop_condition}`",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def story_text(row: StoryRow, epic: ModuleSpecPcNEpic) -> str:
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


def write_stories(base: Path, epic: ModuleSpecPcNEpic) -> dict[str, Path]:
    out: dict[str, Path] = {}
    for row in epic.story_rows:
        path = base / f"docs/stories/{row.story_id}-{row.topic}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(story_text(row, epic), encoding="utf-8")
        out[row.story_id] = path
    return out


def write_story_index(path: Path, epic: ModuleSpecPcNEpic) -> None:
    lines = [
        "# RE-283..RE-287 module-spec_pc_n epic",
        "",
        "Status: Done",
        "",
        "## Progress tracker",
        "",
        "- [x] Parser-artifact keyword row excluded.",
        "- [x] DecodeTrack retained as the only real source-backed candidate.",
        "- [x] Gates denied with explicit non-raw proof blocker.",
        "- [x] Backlog exhaustion handoff emitted.",
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


def write_all_artifacts(epic: ModuleSpecPcNEpic, base: Path) -> dict[str, object]:
    base = Path(base)
    paths = {
        "parser_artifacts_csv": base / PARSER_ARTIFACTS_CSV,
        "audit_csv": base / AUDIT_CSV,
        "epic_csv": base / EPIC_CSV,
        "gate_csv": base / GATE_CSV,
        "handoff_csv": base / HANDOFF_CSV,
        "md": base / MD_OUTPUT,
        "story_index": base / STORY_INDEX,
    }
    write_rows(paths["parser_artifacts_csv"], epic.parser_artifact_rows)
    write_rows(paths["audit_csv"], epic.audit_rows)
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
