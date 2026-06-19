#!/usr/bin/env python3
"""Select the next platform/frontend service subcluster after gpu/fmv mainloop exhaustion."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE363_HANDOFF = "docs/reverse/generated/re363-gpu-fmv-mainloop-service-callsite-readiness-handoff.csv"
RE343_HANDOFF = "docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-handoff.csv"
RE343_SUBCLUSTERS = "docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-subclusters.csv"
RE343_CANDIDATES = "docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-candidates.csv"
SUBCLUSTERS_CSV = "docs/reverse/generated/re364-platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection-subclusters.csv"
CANDIDATES_CSV = "docs/reverse/generated/re364-platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection-candidates.csv"
SUMMARY_CSV = "docs/reverse/generated/re364-platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re364-platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re364-platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection.md"
STORY = "docs/stories/RE-364-platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection.md"

PARENT_SCOPE = "platform-frontend-service-cluster"
CLOSED_SUBCLUSTERS = ("cd-load-audio-service", "frontend-display-menu-service", "gpu-fmv-mainloop-service")
SELECTED_SUBCLUSTER = "runtime-callee-bridge"
SELECTED_CANDIDATE_IDS = ("a01f47cb95a4",)
NEXT_TICKET = "RE-365"
NEXT_TOPIC = "runtime-callee-bridge-readiness-gate"

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
    "unimplemented();",
)


@dataclass(frozen=True)
class NextSubclusterRow:
    rank: int
    source_rank: int
    narrow_subcluster: str
    candidate_count: int
    mapped_caller_total: int
    mapped_callee_total: int
    max_source_context_count: int
    bridge_classes: str
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
    source_context_count: int
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


def validate_re363_handoff(repo: Path) -> None:
    row = one_row(repo, RE363_HANDOFF)
    expected = {
        "story_id": "RE-363",
        "next_ticket": "RE-364",
        "next_topic": "platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection",
        "selected_candidate_id": "1b3534d34062",
        "exhausted_subcluster": "gpu-fmv-mainloop-service",
        "candidate_level_proof_count": "0",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "selected_domain": "none",
        "selected_pivot": "none",
        "next_deferred_candidate_id": "none",
        "next_subcluster": SELECTED_SUBCLUSTER,
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-363 handoff drift: {key}={row.get(key)!r}")


def validate_re343_handoff(repo: Path) -> None:
    row = one_row(repo, RE343_HANDOFF)
    expected = {
        "story_id": "RE-343",
        "next_ticket": "RE-344",
        "next_topic": "cd-load-audio-service-readiness-gate",
        "focus_cluster": PARENT_SCOPE,
        "selected_narrow_subcluster": "cd-load-audio-service",
        "selected_narrow_candidate_count": "2",
        "selected_candidate_ids": "1e35f3f4fb97;653df7c5909b",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-343 handoff drift: {key}={row.get(key)!r}")


def validate_parent_queue(subclusters: list[dict[str, str]]) -> None:
    actual_order = [row.get("narrow_subcluster") for row in subclusters]
    expected_order = [
        "cd-load-audio-service",
        "frontend-display-menu-service",
        "gpu-fmv-mainloop-service",
        SELECTED_SUBCLUSTER,
    ]
    if actual_order != expected_order:
        raise ValueError(f"RE-343 parent queue drift: {actual_order!r}")
    if subclusters[0].get("selection_status") != "selected-next":
        raise ValueError("RE-343 selected subcluster baseline drift")
    for row in subclusters[1:]:
        if row.get("selection_status") != "deferred-after-selected-subcluster" or row.get("gate_decision") != "defer-after-re344":
            raise ValueError(f"RE-343 deferred subcluster baseline drift: {row.get('narrow_subcluster')}")
    if any(row.get("ready_to_reopen_domain") != "no" for row in subclusters):
        raise ValueError("RE-343 subcluster readiness drift")
    if any(row.get("source_patch_authorized") != "no" for row in subclusters):
        raise ValueError("RE-343 source patch readiness drift")


def build_platform_frontend_service_post_gpu_fmv_mainloop_next_subcluster_selection(repo: Path) -> NextSubclusterBundle:
    repo = Path(repo)
    validate_re363_handoff(repo)
    validate_re343_handoff(repo)
    parent_rows = read_csv(repo / RE343_SUBCLUSTERS)
    validate_parent_queue(parent_rows)

    remaining = [row for row in parent_rows if row["narrow_subcluster"] not in CLOSED_SUBCLUSTERS]
    if [row["narrow_subcluster"] for row in remaining] != [SELECTED_SUBCLUSTER]:
        raise ValueError("Post-gpu-fmv-mainloop remaining subcluster order drift")

    source_subcluster = remaining[0]
    subcluster_rows = [
        NextSubclusterRow(
            rank=1,
            source_rank=int(source_subcluster["rank"]),
            narrow_subcluster=SELECTED_SUBCLUSTER,
            candidate_count=int(source_subcluster["candidate_count"]),
            mapped_caller_total=int(source_subcluster["mapped_caller_total"]),
            mapped_callee_total=int(source_subcluster["mapped_callee_total"]),
            max_source_context_count=int(source_subcluster["max_source_context_count"]),
            bridge_classes=source_subcluster["bridge_classes"],
            selection_status="selected-next",
            gate_decision="gate-before-proof-domain",
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            next_ticket=NEXT_TICKET,
            next_topic=NEXT_TOPIC,
            stop_condition="candidate-level source-symbolic proof required before proof-domain selection",
        )
    ]

    candidate_source_rows = [
        row for row in read_csv(repo / RE343_CANDIDATES) if row.get("narrow_subcluster") == SELECTED_SUBCLUSTER
    ]
    if [row["candidate_id"] for row in candidate_source_rows] != list(SELECTED_CANDIDATE_IDS):
        raise ValueError("RE-343 runtime callee bridge selected candidate drift")

    candidate_rows: list[SelectedCandidateRow] = []
    for rank, row in enumerate(candidate_source_rows, start=1):
        candidate_rows.append(
            SelectedCandidateRow(
                rank=rank,
                source_rank=int(row["source_rank"]),
                candidate_id=row["candidate_id"],
                narrow_subcluster=SELECTED_SUBCLUSTER,
                bridge_class=row["bridge_class"],
                body_size_bucket=row["body_size_bucket"],
                mapped_caller_count=int(row["mapped_caller_count"]),
                mapped_callee_count=int(row["mapped_callee_count"]),
                source_context_count=int(row["source_context_count"]),
                readiness_gate="blocked-needs-candidate-level-proof",
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                next_probe="readiness-gate",
                stop_condition="candidate-level source-symbolic proof is required before domain selection",
            )
        )

    summary = NextSubclusterSummary(
        story_id="RE-364",
        topic="platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection",
        upstream_handoff="RE-363",
        parent_scope=PARENT_SCOPE,
        closed_subclusters=";".join(CLOSED_SUBCLUSTERS),
        input_subcluster_count=len(parent_rows),
        closed_subcluster_count=len(CLOSED_SUBCLUSTERS),
        deferred_subcluster_count=len(remaining),
        selected_narrow_subcluster=SELECTED_SUBCLUSTER,
        selected_narrow_candidate_count=len(candidate_rows),
        selected_candidate_ids=";".join(SELECTED_CANDIDATE_IDS),
        ready_to_reopen_domain_count=0,
        source_patch_authorized_count=0,
        selected_domain="none",
        selected_pivot="none",
        next_ticket=NEXT_TICKET,
        next_topic=NEXT_TOPIC,
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="gpu/fmv mainloop service queue exhausted; select runtime callee bridge for gating",
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
    return f"""# RE-364 platform/frontend service post gpu/fmv mainloop next subcluster selection

## Summary

Selected `{bundle.summary.selected_narrow_subcluster}` after RE-363 exhausted the gpu/fmv mainloop service candidate queue.
The selected candidates are `{bundle.summary.selected_candidate_ids}` and must pass a readiness gate before any proof domain can reopen.

## Selected subcluster

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
    return f"""# RE-364 platform/frontend service post gpu/fmv mainloop next subcluster selection

## Goal

Consume the RE-363 gpu/fmv mainloop queue exhaustion and select the next deferred platform/frontend service subcluster from the parent queue.

## Inputs

- Exhausted selected-subcluster handoff: `{RE363_HANDOFF}`
- Parent selection handoff: `{RE343_HANDOFF}`
- Parent subcluster queue: `{RE343_SUBCLUSTERS}`
- Candidate metadata: `{RE343_CANDIDATES}`

## Progress tracker

- [x] RE-363 gpu/fmv mainloop queue exhaustion validated.
- [x] Parent platform/frontend service subcluster queue verified fail-closed.
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
- Selected candidates: `{bundle.summary.selected_candidate_ids}`
- Ready to reopen domain selection: `{bundle.summary.ready_to_reopen_domain_count}`
- Source patch authorized rows: `{bundle.summary.source_patch_authorized_count}`

## Readiness decision

The selected runtime callee bridge subcluster is only ready for a readiness gate. Domain and pivot stay `none`; source/code readiness remains `blocked`.

## Follow-up ticket breakdown

- `{bundle.summary.next_ticket}` / `{bundle.summary.next_topic}`: gate candidates `{bundle.summary.selected_candidate_ids}` before any proof-domain selection.
  - Inputs: RE-364 selected subcluster/candidate rows plus parent queue metadata.
  - Deliverables: candidate readiness rows, selected/denied follow-up proof export, and handoff.
  - Stop condition: if candidate-level source-symbolic proof is still missing, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re364_platform_frontend_service_post_gpu_fmv_mainloop_next_subcluster_selection.py -q`
- `python scripts/reverse/re364_platform_frontend_service_post_gpu_fmv_mainloop_next_subcluster_selection.py --repo .`
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
    bundle = build_platform_frontend_service_post_gpu_fmv_mainloop_next_subcluster_selection(repo)
    written = write_all_artifacts(bundle, repo)
    for label, path in written.items():
        print(f"{label}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
