#!/usr/bin/env python3
"""Select combat/camera after the lara-control queue closes without proof."""
from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE393_HANDOFF = "docs/reverse/generated/re393-lara-control-service-readiness-gate-handoff.csv"
RE392_HANDOFF = "docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-handoff.csv"
RE392_SUBCLUSTERS = "docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-subclusters.csv"
RE392_CANDIDATES = "docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-candidates.csv"
SUBCLUSTERS_CSV = "docs/reverse/generated/re394-lara-combat-camera-post-lara-control-next-subcluster-selection-subclusters.csv"
CANDIDATES_CSV = "docs/reverse/generated/re394-lara-combat-camera-post-lara-control-next-subcluster-selection-candidates.csv"
SUMMARY_CSV = "docs/reverse/generated/re394-lara-combat-camera-post-lara-control-next-subcluster-selection-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re394-lara-combat-camera-post-lara-control-next-subcluster-selection-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re394-lara-combat-camera-post-lara-control-next-subcluster-selection.md"
STORY = "docs/stories/RE-394-lara-combat-camera-post-lara-control-next-subcluster-selection.md"

FORBIDDEN_OUTPUT_FRAGMENTS = (
    "0x", "fun_", "word_le_hex", "payload_offset", "dump row", "opcode",
    "machine word", "call_address", "branch target", "call target",
    "hex-address-fragment", "raw_evidence", "source_line_text", "ghidra_entry",
    "ghidra_name", "unimplemented();",
)
CLOSED_SUBCLUSTERS = ("lara-control-service",)
SELECTED_SUBCLUSTER = "combat-camera-service"
SELECTED_CANDIDATE_ID = "0aaa76206517"
NEXT_TICKET = "RE-395"
NEXT_TOPIC = "combat-camera-service-readiness-gate"


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
    representative_source_context: str
    selection_status: str
    gate_decision: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    next_ticket: str
    next_topic: str
    stop_condition: str


@dataclass(frozen=True)
class NextCandidateRow:
    rank: int
    source_rank: int
    candidate_id: str
    narrow_subcluster: str
    bridge_class: str
    body_size_bucket: str
    mapped_caller_count: int
    mapped_callee_count: int
    source_context_count: int
    representative_source_context: str
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
    parent_handoff: str
    parent_scope: str
    closed_narrow_subclusters: str
    input_subcluster_count: int
    closed_subcluster_count: int
    deferred_subcluster_count: int
    selected_followup_subcluster: str
    selected_candidate_count: int
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
    candidate_rows: list[NextCandidateRow]
    summary: NextSubclusterSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def one_row(repo: Path, rel_path: str) -> dict[str, str]:
    rows = read_csv(repo / rel_path)
    if len(rows) != 1:
        raise ValueError(f"{rel_path} must contain exactly one row")
    return rows[0]


def validate_re393_exhaustion(repo: Path) -> None:
    row = one_row(repo, RE393_HANDOFF)
    expected = {
        "story_id": "RE-393",
        "next_ticket": "RE-394",
        "next_topic": "lara-combat-camera-post-lara-control-next-subcluster-selection",
        "selected_narrow_subcluster": "lara-control-service",
        "input_candidate_count": "1",
        "candidate_level_proof_count": "0",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "selected_domain": "none",
        "selected_pivot": "none",
        "selected_followup_candidate_id": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-393 exhaustion drift: {key}={row.get(key)!r}")


def validate_re392_parent_handoff(repo: Path) -> None:
    row = one_row(repo, RE392_HANDOFF)
    expected = {
        "story_id": "RE-392",
        "focus_cluster": "lara-combat-camera-cluster",
        "narrow_subcluster_count": "2",
        "selected_narrow_subcluster": "lara-control-service",
        "selected_narrow_candidate_count": "1",
        "selected_candidate_ids": "4a632b41837e",
        "next_ticket": "RE-393",
        "next_topic": "lara-control-service-readiness-gate",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-392 parent handoff drift: {key}={row.get(key)!r}")


def validate_parent_queue(rows: list[dict[str, str]]) -> None:
    expected = ["lara-control-service", "combat-camera-service"]
    actual = [row.get("narrow_subcluster") for row in rows]
    if actual != expected:
        raise ValueError(f"RE-392 parent queue drift: {actual!r}")
    if rows[0].get("selection_status") != "selected-next":
        raise ValueError("RE-392 selected baseline drift")
    for row in rows:
        if row.get("ready_to_reopen_domain") != "no" or row.get("source_patch_authorized") != "no":
            raise ValueError(f"RE-392 parent readiness drift: {row.get('narrow_subcluster')}")


def require_metadata_only(text: str) -> None:
    lowered = text.lower()
    for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
        if fragment in lowered:
            raise ValueError(f"Forbidden raw-evidence fragment in generated output: {fragment}")


def build_lara_combat_camera_post_lara_control_next_subcluster_selection(repo: Path) -> NextSubclusterBundle:
    repo = Path(repo)
    validate_re393_exhaustion(repo)
    validate_re392_parent_handoff(repo)
    parent_rows = read_csv(repo / RE392_SUBCLUSTERS)
    validate_parent_queue(parent_rows)

    deferred = [row for row in parent_rows if row["narrow_subcluster"] not in CLOSED_SUBCLUSTERS]
    if [row["narrow_subcluster"] for row in deferred] != [SELECTED_SUBCLUSTER]:
        raise ValueError("RE-392 deferred subcluster ordering drift")
    subcluster_rows = [
        NextSubclusterRow(
            rank=rank,
            source_rank=int(row["rank"]),
            narrow_subcluster=row["narrow_subcluster"],
            candidate_count=int(row["candidate_count"]),
            mapped_caller_total=int(row["mapped_caller_total"]),
            mapped_callee_total=int(row["mapped_callee_total"]),
            max_source_context_count=int(row["max_source_context_count"]),
            bridge_classes=row["bridge_classes"],
            representative_source_context=row["representative_source_context"],
            selection_status="selected-next",
            gate_decision="gate-before-proof-domain",
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            next_ticket=NEXT_TICKET,
            next_topic=NEXT_TOPIC,
            stop_condition="candidate-level source-symbolic proof required before proof-domain selection",
        )
        for rank, row in enumerate(deferred, start=1)
    ]

    candidates = read_csv(repo / RE392_CANDIDATES)
    selected = [row for row in candidates if row.get("narrow_subcluster") == SELECTED_SUBCLUSTER]
    if [row.get("candidate_id") for row in selected] != [SELECTED_CANDIDATE_ID]:
        raise ValueError("RE-392 combat-camera candidate drift")
    for row in selected:
        expected = {"readiness_gate": "blocked-needs-candidate-level-proof", "ready_to_reopen_domain": "no", "source_patch_authorized": "no", "next_probe": "defer-after-re393"}
        for key, value in expected.items():
            if row.get(key) != value:
                raise ValueError(f"RE-392 combat-camera candidate drift: {key}={row.get(key)!r}")
    candidate_rows = [
        NextCandidateRow(
            rank=rank, source_rank=int(row["source_rank"]), candidate_id=row["candidate_id"],
            narrow_subcluster=row["narrow_subcluster"], bridge_class=row["bridge_class"],
            body_size_bucket=row["body_size_bucket"], mapped_caller_count=int(row["mapped_caller_count"]),
            mapped_callee_count=int(row["mapped_callee_count"]), source_context_count=int(row["source_context_count"]),
            representative_source_context=row["representative_source_context"],
            readiness_gate="blocked-needs-candidate-level-proof", ready_to_reopen_domain="no",
            source_patch_authorized="no", next_probe="readiness-gate",
            stop_condition="candidate-level source-symbolic proof required before domain selection",
        )
        for rank, row in enumerate(selected, start=1)
    ]
    summary = NextSubclusterSummary(
        story_id="RE-394", topic="lara-combat-camera-post-lara-control-next-subcluster-selection",
        upstream_handoff="RE-393", parent_handoff="RE-392", parent_scope="lara-combat-camera-cluster-narrow-subclusters",
        closed_narrow_subclusters=";".join(CLOSED_SUBCLUSTERS), input_subcluster_count=len(parent_rows),
        closed_subcluster_count=len(CLOSED_SUBCLUSTERS), deferred_subcluster_count=len(deferred),
        selected_followup_subcluster=SELECTED_SUBCLUSTER, selected_candidate_count=len(candidate_rows),
        selected_candidate_ids=";".join(row.candidate_id for row in candidate_rows), ready_to_reopen_domain_count=0,
        source_patch_authorized_count=0, selected_domain="none", selected_pivot="none", next_ticket=NEXT_TICKET,
        next_topic=NEXT_TOPIC, metadata_work_readiness="ready", code_change_readiness="blocked",
        stop_condition="lara control service queue exhausted; select next deferred lara/combat/camera subcluster",
    )
    return NextSubclusterBundle(subcluster_rows, candidate_rows, summary)


def write_csv(path: Path, rows: list[object], row_type: type[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[field.name for field in fields(row_type)], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def render_md(bundle: NextSubclusterBundle) -> str:
    s = bundle.summary
    text = f"""# RE-394 lara combat camera post lara control next subcluster selection

## Purpose

Close the exhausted lara-control path and select the next deferred lara/combat/camera subcluster without authorizing a proof domain or source patch.

## Inputs

- Exhaustion handoff: `{RE393_HANDOFF}`
- Parent subcluster queue: `{RE392_SUBCLUSTERS}`
- Parent candidates: `{RE392_CANDIDATES}`

## Selection

Selected `{s.selected_followup_subcluster}` with `{s.selected_candidate_count}` source-symbolic candidate.

## Readiness

Domain and pivot remain `{s.selected_domain}` / `{s.selected_pivot}`. Code readiness remains `{s.code_change_readiness}` pending candidate-level proof.

## Handoff

- Next ticket: `{s.next_ticket}`
- Next topic: `{s.next_topic}`
- Stop condition: `{s.stop_condition}`
"""
    require_metadata_only(text)
    return text


def render_story(bundle: NextSubclusterBundle) -> str:
    s = bundle.summary
    text = f"""# RE-394 lara combat camera post lara control next subcluster selection

## Goal

After RE-393 closed lara-control-service without candidate-level proof, select the remaining deferred RE-392 lara/combat/camera subcluster.

## Inputs

- Exhaustion handoff: `{RE393_HANDOFF}`
- Parent narrow handoff: `{RE392_HANDOFF}`
- Parent subcluster queue: `{RE392_SUBCLUSTERS}`
- Parent candidates: `{RE392_CANDIDATES}`

## Progress tracker

- [x] RE-393 lara-control exhaustion handoff validated.
- [x] RE-392 parent narrow handoff and deterministic queue re-opened.
- [x] lara-control-service marked closed.
- [x] Next deferred subcluster selected in parent order.
- [x] Domain, pivot, and source/code readiness kept blocked.

## Generated artifacts

- `{SUBCLUSTERS_CSV}`
- `{CANDIDATES_CSV}`
- `{SUMMARY_CSV}`
- `{HANDOFF_CSV}`
- `{MD_OUTPUT}`

## Findings

- Parent scope: `{s.parent_scope}`
- Closed subclusters: `{s.closed_narrow_subclusters}`
- Deferred subclusters: `{s.deferred_subcluster_count}`
- Selected follow-up subcluster: `{s.selected_followup_subcluster}`
- Selected candidate IDs: `{s.selected_candidate_ids}`
- Ready to reopen domain selection: `{s.ready_to_reopen_domain_count}`
- Source patch authorized rows: `{s.source_patch_authorized_count}`

## Readiness decision

The selected combat/camera queue remains source-symbolic only. Domain and pivot stay `{s.selected_domain}` / `{s.selected_pivot}`, and code readiness remains `{s.code_change_readiness}` until its readiness gate establishes candidate-level proof.

## Follow-up ticket breakdown

- `{s.next_ticket}` / `{s.next_topic}`: gate `{s.selected_followup_subcluster}` before proof-domain selection.
  - Inputs: RE-394 selected candidate and source-symbolic context.
  - Deliverables: candidate gate, summary/handoff, and story with tracker.
  - Stop condition: if candidate-level proof remains absent, keep source/code readiness blocked and select a safe follow-up.

## Validation commands

- `python -m pytest tests/reverse/test_re394_lara_combat_camera_post_lara_control_next_subcluster_selection.py -q`
- `python scripts/reverse/re394_lara_combat_camera_post_lara_control_next_subcluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
"""
    require_metadata_only(text)
    return text


def write_all_artifacts(bundle: NextSubclusterBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    outputs = {"subclusters_csv": repo / SUBCLUSTERS_CSV, "candidates_csv": repo / CANDIDATES_CSV,
               "summary_csv": repo / SUMMARY_CSV, "handoff_csv": repo / HANDOFF_CSV,
               "md": repo / MD_OUTPUT, "story": repo / STORY}
    write_csv(outputs["subclusters_csv"], bundle.subcluster_rows, NextSubclusterRow)
    write_csv(outputs["candidates_csv"], bundle.candidate_rows, NextCandidateRow)
    write_csv(outputs["summary_csv"], [bundle.summary], NextSubclusterSummary)
    write_csv(outputs["handoff_csv"], [bundle.summary], NextSubclusterSummary)
    outputs["md"].parent.mkdir(parents=True, exist_ok=True)
    outputs["md"].write_text(render_md(bundle), encoding="utf-8")
    outputs["story"].parent.mkdir(parents=True, exist_ok=True)
    outputs["story"].write_text(render_story(bundle), encoding="utf-8")
    for path in outputs.values():
        require_metadata_only(path.read_text(encoding="utf-8"))
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()
    bundle = build_lara_combat_camera_post_lara_control_next_subcluster_selection(repo)
    for label, path in write_all_artifacts(bundle, repo).items():
        print(f"{label}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
