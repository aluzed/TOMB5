#!/usr/bin/env python3
"""Select the next deferred collision/switch/door subcluster after switch-door-control exhaustion."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE326_HANDOFF = "docs/reverse/generated/re326-switch-door-control-helper-callsite-readiness-handoff.csv"
RE322_HANDOFF = "docs/reverse/generated/re322-collision-switch-door-next-subcluster-selection-handoff.csv"
RE322_SUBCLUSTERS = "docs/reverse/generated/re322-collision-switch-door-next-subcluster-selection-subclusters.csv"
RE311_CANDIDATES = "docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-candidates.csv"
SUBCLUSTERS_CSV = "docs/reverse/generated/re327-collision-switch-door-post-switch-door-next-subcluster-selection-subclusters.csv"
CANDIDATES_CSV = "docs/reverse/generated/re327-collision-switch-door-post-switch-door-next-subcluster-selection-candidates.csv"
SUMMARY_CSV = "docs/reverse/generated/re327-collision-switch-door-post-switch-door-next-subcluster-selection-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re327-collision-switch-door-post-switch-door-next-subcluster-selection-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re327-collision-switch-door-post-switch-door-next-subcluster-selection.md"
STORY = "docs/stories/RE-327-collision-switch-door-post-switch-door-next-subcluster-selection.md"

PARENT_SCOPE = "collision-switch-door-cluster"
CLOSED_SUBCLUSTERS = ("collision-geometry-helper", "switch-door-control-helper")
SELECTED_SUBCLUSTER = "weapon-switch-effect-helper"
SELECTED_CANDIDATE_ID = "1ddbda046e37"
NEXT_TICKET = "RE-328"
NEXT_TOPIC = "weapon-switch-effect-helper-readiness-gate"
EXPECTED_PARENT_ORDER = (
    "switch-door-control-helper",
    "weapon-switch-effect-helper",
    "door-save-runtime-helper",
    "camera-collision-helper",
)

FORBIDDEN_OUTPUT_FRAGMENTS = (
    "0x",
    "fun_",
    "word_le_hex",
    "payload_offset",
    "dump row",
    "opcode",
    "machine word",
    "call_address",
    "branch target",
    "call target",
    "hex-address-fragment",
    "raw_evidence",
    "ghidra_entry",
    "ghidra_name",
    "source_line_text",
)


@dataclass(frozen=True)
class NextSubclusterRow:
    rank: int
    source_rank: int
    narrow_subcluster: str
    candidate_count: int
    mapped_caller_total: int
    mapped_callee_total: int
    source_file_count: int
    source_module_count: int
    selection_status: str
    gate_decision: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    next_ticket: str
    next_topic: str
    stop_condition: str


@dataclass(frozen=True)
class SelectedCandidateRow:
    rank: int
    source_rank: int
    candidate_id: str
    narrow_subcluster: str
    bridge_class: str
    body_size_bucket: str
    mapped_caller_count: int
    mapped_callee_count: int
    readiness_gate: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    next_probe: str
    stop_condition: str


@dataclass(frozen=True)
class NextSubclusterSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    parent_scope: str
    closed_subclusters: str
    input_subcluster_count: int
    closed_subcluster_count: int
    deferred_subcluster_count: int
    selected_narrow_subcluster: str
    selected_narrow_candidate_count: int
    selected_candidate_ids: str
    ready_to_reopen_domain_count: int
    source_patch_authorized_count: int
    selected_domain: str
    selected_pivot: str
    next_ticket: str
    next_topic: str
    metadata_work_readiness: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class NextSubclusterBundle:
    subcluster_rows: list[NextSubclusterRow]
    candidate_rows: list[SelectedCandidateRow]
    summary: NextSubclusterSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def one_row(repo: Path, rel_path: str) -> dict[str, str]:
    rows = read_csv(repo / rel_path)
    if len(rows) != 1:
        raise ValueError(f"{rel_path} must contain exactly one row")
    return rows[0]


def validate_re326_handoff(repo: Path) -> None:
    row = one_row(repo, RE326_HANDOFF)
    expected = {
        "story_id": "RE-326",
        "next_ticket": "TBD",
        "next_topic": "switch-door-control-helper-candidate-queue-exhausted",
        "selected_candidate_id": "8d1fc6fc3cfc",
        "next_candidate_id": "none",
        "candidate_level_proof_count": "0",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-326 handoff drift: {key}={row.get(key)!r}")


def validate_re322_handoff(repo: Path) -> None:
    row = one_row(repo, RE322_HANDOFF)
    expected = {
        "story_id": "RE-322",
        "next_ticket": "RE-323",
        "next_topic": "switch-door-control-helper-readiness-gate",
        "parent_scope": PARENT_SCOPE,
        "closed_subcluster": "collision-geometry-helper",
        "selected_narrow_subcluster": "switch-door-control-helper",
        "selected_candidate_ids": "8d1fc6fc3cfc",
        "input_subcluster_count": "5",
        "closed_subcluster_count": "1",
        "deferred_subcluster_count": "4",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-322 handoff drift: {key}={row.get(key)!r}")


def validate_parent_queue(subclusters: list[dict[str, str]]) -> None:
    actual_order = [row.get("narrow_subcluster") for row in subclusters]
    if actual_order != list(EXPECTED_PARENT_ORDER):
        raise ValueError(f"RE-322 parent queue drift: {actual_order!r}")
    selected = subclusters[0]
    if selected.get("narrow_subcluster") != "switch-door-control-helper" or selected.get("selection_status") != "selected-next":
        raise ValueError("RE-322 selected subcluster baseline drift")
    if any(row.get("ready_to_reopen_domain") != "no" for row in subclusters):
        raise ValueError("RE-322 subcluster readiness drift")
    if any(row.get("source_patch_authorized") != "no" for row in subclusters):
        raise ValueError("RE-322 source patch readiness drift")


def build_collision_switch_door_post_switch_door_next_subcluster_selection(repo: Path) -> NextSubclusterBundle:
    repo = Path(repo)
    validate_re326_handoff(repo)
    validate_re322_handoff(repo)
    parent_rows = read_csv(repo / RE322_SUBCLUSTERS)
    validate_parent_queue(parent_rows)

    remaining = [row for row in parent_rows if row["narrow_subcluster"] not in CLOSED_SUBCLUSTERS]
    if [row["narrow_subcluster"] for row in remaining] != [
        "weapon-switch-effect-helper",
        "door-save-runtime-helper",
        "camera-collision-helper",
    ]:
        raise ValueError("Post-switch-door remaining subcluster order drift")
    if remaining[0]["narrow_subcluster"] != SELECTED_SUBCLUSTER:
        raise ValueError("Next deferred subcluster selection drift")

    subcluster_rows: list[NextSubclusterRow] = []
    for rank, row in enumerate(remaining, start=1):
        selected = row["narrow_subcluster"] == SELECTED_SUBCLUSTER
        subcluster_rows.append(
            NextSubclusterRow(
                rank=rank,
                source_rank=int(row["source_rank"]),
                narrow_subcluster=row["narrow_subcluster"],
                candidate_count=int(row["candidate_count"]),
                mapped_caller_total=int(row["mapped_caller_total"]),
                mapped_callee_total=int(row["mapped_callee_total"]),
                source_file_count=int(row["source_file_count"]),
                source_module_count=int(row["source_module_count"]),
                selection_status="selected-next" if selected else "deferred-after-selected-subcluster",
                gate_decision="gate-before-proof-domain" if selected else "defer-after-selected-subcluster",
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                next_ticket=NEXT_TICKET if selected else "TBD",
                next_topic=NEXT_TOPIC if selected else "defer-after-re328",
                stop_condition="candidate-level source-symbolic proof required before proof-domain selection" if selected else "wait for selected subcluster readiness gate",
            )
        )

    selected_candidates = [
        row for row in read_csv(repo / RE311_CANDIDATES) if row.get("narrow_subcluster") == SELECTED_SUBCLUSTER
    ]
    if [row["candidate_id"] for row in selected_candidates] != [SELECTED_CANDIDATE_ID]:
        raise ValueError("RE-311 weapon-switch-effect selected candidate drift")
    source_row = selected_candidates[0]
    candidate_rows = [
        SelectedCandidateRow(
            rank=1,
            source_rank=int(source_row["source_rank"]),
            candidate_id=SELECTED_CANDIDATE_ID,
            narrow_subcluster=SELECTED_SUBCLUSTER,
            bridge_class=source_row["bridge_class"],
            body_size_bucket=source_row["body_size_bucket"],
            mapped_caller_count=int(source_row["mapped_caller_count"]),
            mapped_callee_count=int(source_row["mapped_callee_count"]),
            readiness_gate="blocked-needs-candidate-level-proof",
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            next_probe="readiness-gate",
            stop_condition="candidate-level source-symbolic proof is required before domain selection",
        )
    ]

    summary = NextSubclusterSummary(
        story_id="RE-327",
        topic="collision-switch-door-post-switch-door-next-subcluster-selection",
        upstream_handoff="RE-326",
        parent_scope=PARENT_SCOPE,
        closed_subclusters=";".join(CLOSED_SUBCLUSTERS),
        input_subcluster_count=5,
        closed_subcluster_count=len(CLOSED_SUBCLUSTERS),
        deferred_subcluster_count=len(remaining),
        selected_narrow_subcluster=SELECTED_SUBCLUSTER,
        selected_narrow_candidate_count=len(candidate_rows),
        selected_candidate_ids=SELECTED_CANDIDATE_ID,
        ready_to_reopen_domain_count=0,
        source_patch_authorized_count=0,
        selected_domain="none",
        selected_pivot="none",
        next_ticket=NEXT_TICKET,
        next_topic=NEXT_TOPIC,
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="switch-door-control helper queue exhausted; select the next deferred collision/switch/door subcluster for gating",
    )
    return NextSubclusterBundle(subcluster_rows=subcluster_rows, candidate_rows=candidate_rows, summary=summary)


def write_csv(path: Path, rows: list[object], row_type: type[object]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(row_type)], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
    return path


def assert_metadata_only(paths: list[Path]) -> None:
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            if fragment in text:
                raise ValueError(f"Forbidden output fragment {fragment!r} in {path}")


def render_markdown(bundle: NextSubclusterBundle) -> str:
    rows = "\n".join(
        f"- `{row.narrow_subcluster}`: `{row.candidate_count}` candidate(s), status `{row.selection_status}`."
        for row in bundle.subcluster_rows
    )
    return f"""# RE-327 collision-switch-door post-switch-door next subcluster selection

## Summary

Selected `{bundle.summary.selected_narrow_subcluster}` after RE-326 exhausted the switch-door-control helper candidate queue.
The selected candidate is `{bundle.summary.selected_candidate_ids}` and must pass a readiness gate before any proof domain can reopen.

## Remaining subclusters

{rows}

## Readiness decision

- ready-to-reopen rows: `{bundle.summary.ready_to_reopen_domain_count}`
- source-patch authorized rows: `{bundle.summary.source_patch_authorized_count}`
- selected domain: `{bundle.summary.selected_domain}`
- selected pivot: `{bundle.summary.selected_pivot}`
- next ticket: `{bundle.summary.next_ticket}` / `{bundle.summary.next_topic}`

Code readiness remains `blocked`.
"""


def render_story(bundle: NextSubclusterBundle) -> str:
    return f"""# RE-327 collision-switch-door post-switch-door next subcluster selection

## Goal

Consume the RE-326 switch-door-control candidate queue exhaustion and select the next deferred collision/switch/door subcluster from the parent queue.

## Inputs

- Exhausted selected-subcluster handoff: `{RE326_HANDOFF}`
- Parent subcluster queue: `{RE322_SUBCLUSTERS}`
- Candidate metadata: `{RE311_CANDIDATES}`

## Progress tracker

- [x] RE-326 switch-door candidate queue exhaustion validated.
- [x] Parent collision/switch/door subcluster queue verified fail-closed.
- [x] Closed subclusters excluded: `{bundle.summary.closed_subclusters}`.
- [x] Next deferred subcluster selected: `{bundle.summary.selected_narrow_subcluster}`.
- [x] Readiness gate handoff emitted for `{bundle.summary.next_ticket}`.

## Generated artifacts

- `{SUBCLUSTERS_CSV}`
- `{CANDIDATES_CSV}`
- `{SUMMARY_CSV}`
- `{HANDOFF_CSV}`
- `{MD_OUTPUT}`

## Findings

- Parent scope: `{bundle.summary.parent_scope}`
- Closed subclusters: `{bundle.summary.closed_subclusters}`
- Input subclusters: `{bundle.summary.input_subcluster_count}`
- Remaining deferred subclusters: `{bundle.summary.deferred_subcluster_count}`
- Selected subcluster: `{bundle.summary.selected_narrow_subcluster}`
- Selected candidate: `{bundle.summary.selected_candidate_ids}`
- Ready to reopen domain selection: `{bundle.summary.ready_to_reopen_domain_count}`
- Source patch authorized rows: `{bundle.summary.source_patch_authorized_count}`

## Readiness decision

The selected weapon/switch/effect subcluster is only ready for a readiness gate. Domain and pivot stay `none`; source/code readiness remains `blocked`.

## Follow-up ticket breakdown

- `{bundle.summary.next_ticket}` / `{bundle.summary.next_topic}`: gate candidate `{bundle.summary.selected_candidate_ids}` before any proof-domain selection.
  - Inputs: RE-327 selected subcluster/candidate rows plus the parent queue metadata.
  - Deliverables: candidate readiness rows, selected/denied follow-up proof export, and handoff.
  - Stop condition: if candidate-level source-symbolic proof is still missing, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re327_collision_switch_door_post_switch_door_next_subcluster_selection.py -q`
- `python scripts/reverse/re327_collision_switch_door_post_switch_door_next_subcluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
"""


def write_all_artifacts(bundle: NextSubclusterBundle, repo: Path) -> dict[str, Path]:
    written = {
        "subclusters_csv": write_csv(repo / SUBCLUSTERS_CSV, bundle.subcluster_rows, NextSubclusterRow),
        "candidates_csv": write_csv(repo / CANDIDATES_CSV, bundle.candidate_rows, SelectedCandidateRow),
        "summary_csv": write_csv(repo / SUMMARY_CSV, [bundle.summary], NextSubclusterSummary),
        "handoff_csv": write_csv(repo / HANDOFF_CSV, [bundle.summary], NextSubclusterSummary),
    }
    md = repo / MD_OUTPUT
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text(render_markdown(bundle), encoding="utf-8")
    written["md"] = md
    story = repo / STORY
    story.parent.mkdir(parents=True, exist_ok=True)
    story.write_text(render_story(bundle), encoding="utf-8")
    written["story"] = story
    assert_metadata_only(list(written.values()))
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()
    bundle = build_collision_switch_door_post_switch_door_next_subcluster_selection(repo)
    written = write_all_artifacts(bundle, repo)
    for label, path in written.items():
        print(f"{label}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
