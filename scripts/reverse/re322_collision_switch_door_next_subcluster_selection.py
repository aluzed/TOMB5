#!/usr/bin/env python3
"""Select the next deferred collision/switch/door subcluster after collision-geometry exhaustion."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE321_HANDOFF = "docs/reverse/generated/re321-collision-geometry-helper-final-candidate-callsite-readiness-handoff.csv"
RE311_SUBCLUSTERS = "docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-subclusters.csv"
RE311_CANDIDATES = "docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-candidates.csv"
SUBCLUSTERS_CSV = "docs/reverse/generated/re322-collision-switch-door-next-subcluster-selection-subclusters.csv"
CANDIDATES_CSV = "docs/reverse/generated/re322-collision-switch-door-next-subcluster-selection-candidates.csv"
SUMMARY_CSV = "docs/reverse/generated/re322-collision-switch-door-next-subcluster-selection-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re322-collision-switch-door-next-subcluster-selection-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re322-collision-switch-door-next-subcluster-selection.md"
STORY = "docs/stories/RE-322-collision-switch-door-next-subcluster-selection.md"

CLOSED_SUBCLUSTER = "collision-geometry-helper"
SELECTED_SUBCLUSTER = "switch-door-control-helper"
SELECTED_CANDIDATE_ID = "8d1fc6fc3cfc"
PARENT_SCOPE = "collision-switch-door-cluster"

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
    closed_subcluster: str
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


def validate_re321_handoff(repo: Path) -> None:
    row = one_row(repo, RE321_HANDOFF)
    expected = {
        "story_id": "RE-321",
        "next_ticket": "TBD",
        "next_topic": "collision-geometry-helper-candidate-queue-exhausted",
        "next_candidate_id": "none",
        "selected_candidate_id": "61d55bb1809b",
        "previous_candidate_id": "d96359c1d9f3",
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
            raise ValueError(f"RE-321 handoff drift: {key}={row.get(key)!r}")


def validate_re311_scope(subclusters: list[dict[str, str]]) -> None:
    expected_order = [
        CLOSED_SUBCLUSTER,
        SELECTED_SUBCLUSTER,
        "weapon-switch-effect-helper",
        "door-save-runtime-helper",
        "camera-collision-helper",
    ]
    actual_order = [row.get("narrow_subcluster") for row in subclusters]
    if actual_order != expected_order:
        raise ValueError(f"RE-311 subcluster order drift: {actual_order!r}")
    closed = subclusters[0]
    if closed.get("next_ticket") != "RE-312" or closed.get("gate_decision") != "gate-before-proof-domain":
        raise ValueError("RE-311 closed subcluster baseline drift")
    if any(row.get("ready_to_reopen_domain") != "no" for row in subclusters):
        raise ValueError("RE-311 subcluster readiness drift")
    if any(row.get("source_patch_authorized") != "no" for row in subclusters):
        raise ValueError("RE-311 source patch readiness drift")


def build_collision_switch_door_next_subcluster_selection(repo: Path) -> NextSubclusterBundle:
    repo = Path(repo)
    validate_re321_handoff(repo)
    subclusters = read_csv(repo / RE311_SUBCLUSTERS)
    validate_re311_scope(subclusters)
    deferred = [row for row in subclusters if row["narrow_subcluster"] != CLOSED_SUBCLUSTER]
    if deferred[0]["narrow_subcluster"] != SELECTED_SUBCLUSTER:
        raise ValueError("Next deferred subcluster selection drift")

    subcluster_rows: list[NextSubclusterRow] = []
    for rank, row in enumerate(deferred, start=1):
        selected = row["narrow_subcluster"] == SELECTED_SUBCLUSTER
        subcluster_rows.append(
            NextSubclusterRow(
                rank=rank,
                source_rank=int(row["rank"]),
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
                next_ticket="RE-323" if selected else "TBD",
                next_topic="switch-door-control-helper-readiness-gate" if selected else "defer-after-re323",
                stop_condition="candidate-level source-symbolic proof required before proof-domain selection" if selected else "wait for selected subcluster readiness gate",
            )
        )

    selected_candidates = [
        row for row in read_csv(repo / RE311_CANDIDATES) if row.get("narrow_subcluster") == SELECTED_SUBCLUSTER
    ]
    if [row["candidate_id"] for row in selected_candidates] != [SELECTED_CANDIDATE_ID]:
        raise ValueError("RE-311 selected candidate drift")
    candidate_rows = [
        SelectedCandidateRow(
            rank=1,
            source_rank=int(selected_candidates[0]["source_rank"]),
            candidate_id=SELECTED_CANDIDATE_ID,
            narrow_subcluster=SELECTED_SUBCLUSTER,
            bridge_class=selected_candidates[0]["bridge_class"],
            body_size_bucket=selected_candidates[0]["body_size_bucket"],
            mapped_caller_count=int(selected_candidates[0]["mapped_caller_count"]),
            mapped_callee_count=int(selected_candidates[0]["mapped_callee_count"]),
            readiness_gate="blocked-needs-candidate-level-proof",
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            next_probe="readiness-gate",
            stop_condition="candidate-level source-symbolic proof is required before domain selection",
        )
    ]

    summary = NextSubclusterSummary(
        story_id="RE-322",
        topic="collision-switch-door-next-subcluster-selection",
        upstream_handoff="RE-321",
        parent_scope=PARENT_SCOPE,
        closed_subcluster=CLOSED_SUBCLUSTER,
        input_subcluster_count=len(subclusters),
        closed_subcluster_count=1,
        deferred_subcluster_count=len(deferred),
        selected_narrow_subcluster=SELECTED_SUBCLUSTER,
        selected_narrow_candidate_count=len(candidate_rows),
        selected_candidate_ids=SELECTED_CANDIDATE_ID,
        ready_to_reopen_domain_count=0,
        source_patch_authorized_count=0,
        selected_domain="none",
        selected_pivot="none",
        next_ticket="RE-323",
        next_topic="switch-door-control-helper-readiness-gate",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="collision-geometry helper queue exhausted; select the next deferred collision/switch/door subcluster for gating",
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


def render_markdown(bundle: NextSubclusterBundle) -> str:
    rows = "\n".join(
        f"- `{row.narrow_subcluster}`: `{row.candidate_count}` candidate(s), status `{row.selection_status}`."
        for row in bundle.subcluster_rows
    )
    return f"""# RE-322 collision-switch-door next subcluster selection

## Summary

Validated RE-321 collision-geometry queue exhaustion and re-entered the RE-311 deferred subcluster queue.
Selected `{bundle.summary.selected_narrow_subcluster}` with candidate `{bundle.summary.selected_candidate_ids}` for the next readiness gate.

## Deferred subclusters

{rows}

## Readiness decision

No proof domain or source patch is reopened by this selection. Domain and pivot remain `none`; code readiness remains `blocked`.

## Next

- `{bundle.summary.next_ticket}` / `{bundle.summary.next_topic}`
"""


def render_story(bundle: NextSubclusterBundle) -> str:
    return f"""# RE-322 collision-switch-door next subcluster selection

## Goal

After RE-321 exhausted the collision-geometry helper candidate queue, select the next deferred RE-311 collision/switch/door subcluster without reopening a proof domain or authorizing source changes.

## Inputs

- Upstream handoff: `{RE321_HANDOFF}`
- Parent subcluster queue: `{RE311_SUBCLUSTERS}`
- Parent candidate rows: `{RE311_CANDIDATES}`

## Progress tracker

- [x] RE-321 collision-geometry queue exhaustion validated.
- [x] RE-311 parent subcluster queue checked fail-closed.
- [x] Closed `collision-geometry-helper` excluded from next selection.
- [x] Next deferred subcluster selected in source order.
- [x] Domain/pivot/source-patch readiness kept blocked.

## Generated artifacts

- `{SUBCLUSTERS_CSV}`
- `{CANDIDATES_CSV}`
- `{SUMMARY_CSV}`
- `{HANDOFF_CSV}`
- `{MD_OUTPUT}`

## Findings

- Parent scope: `{bundle.summary.parent_scope}`
- Closed subcluster: `{bundle.summary.closed_subcluster}`
- Deferred subclusters remaining: `{bundle.summary.deferred_subcluster_count}`
- Selected subcluster: `{bundle.summary.selected_narrow_subcluster}`
- Selected candidates: `{bundle.summary.selected_candidate_ids}`
- Ready to reopen domain selection: `{bundle.summary.ready_to_reopen_domain_count}`
- Source patch authorized rows: `{bundle.summary.source_patch_authorized_count}`

## Readiness decision

The next subcluster is selected only for a readiness gate. It does not prove a domain or authorize source changes.

## Follow-up ticket breakdown

- `{bundle.summary.next_ticket}` / `{bundle.summary.next_topic}`: gate candidate `{bundle.summary.selected_candidate_ids}` in `{bundle.summary.selected_narrow_subcluster}` before any proof-domain selection.
  - Inputs: RE-322 handoff plus RE-311 source-symbolic candidate metadata.
  - Deliverables: candidate readiness rows, gate decision, and handoff to either a still-narrower candidate export or the next deferred subcluster.
  - Stop condition: if candidate-level proof remains absent, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re322_collision_switch_door_next_subcluster_selection.py -q`
- `python scripts/reverse/re322_collision_switch_door_next_subcluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
"""


def assert_metadata_only(paths: list[Path]) -> None:
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            if fragment in text:
                raise ValueError(f"Forbidden output fragment {fragment!r} in {path}")


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
    bundle = build_collision_switch_door_next_subcluster_selection(repo)
    written = write_all_artifacts(bundle, repo)
    for label, path in written.items():
        print(f"{label}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
