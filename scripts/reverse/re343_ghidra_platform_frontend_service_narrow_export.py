#!/usr/bin/env python3
"""Generate RE-343 narrowed metadata export for the platform/frontend Ghidra bridge cluster."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE342_HANDOFF = "docs/reverse/generated/re342-post-collision-switch-door-next-ghidra-cluster-selection-handoff.csv"
RE342_CANDIDATES = "docs/reverse/generated/re342-post-collision-switch-door-next-ghidra-cluster-selection-candidates.csv"
SUBCLUSTERS_CSV = "docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-subclusters.csv"
CANDIDATES_CSV = "docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-candidates.csv"
SUMMARY_CSV = "docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re343-ghidra-platform-frontend-service-narrow-export.md"
STORY = "docs/stories/RE-343-ghidra-platform-frontend-service-narrow-export.md"

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
)

SUBCLUSTER_PRIORITY = {
    "cd-load-audio-service": 0,
    "frontend-display-menu-service": 1,
    "gpu-fmv-mainloop-service": 2,
    "runtime-callee-bridge": 3,
}
SELECTED_SUBCLUSTER = "cd-load-audio-service"


@dataclass(frozen=True)
class NarrowCandidateRow:
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
class NarrowSubclusterRow:
    rank: int
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
class NarrowSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    focus_cluster: str
    focus_candidate_count: int
    narrow_subcluster_count: int
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
class NarrowBundle:
    subcluster_rows: list[NarrowSubclusterRow]
    candidate_rows: list[NarrowCandidateRow]
    summary: NarrowSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def one_row(repo: Path, rel_path: str) -> dict[str, str]:
    rows = read_csv(repo / rel_path)
    if len(rows) != 1:
        raise ValueError(f"{rel_path} must contain exactly one row")
    return rows[0]


def validate_re342_handoff(repo: Path) -> None:
    row = one_row(repo, RE342_HANDOFF)
    expected = {
        "story_id": "RE-342",
        "next_ticket": "RE-343",
        "next_topic": "ghidra-platform-frontend-service-cluster-narrow-export",
        "selected_followup_cluster": "platform-frontend-service-cluster",
        "selected_domain": "none",
        "selected_pivot": "none",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-342 handoff drift: {key}={row.get(key)!r}")


def classify_subcluster(context: str, bridge_class: str) -> str:
    lowered = context.lower()
    if "getfloor" in lowered or "getheight" in lowered or bridge_class == "mapped-callee-bridge":
        return "runtime-callee-bridge"
    if any(token in lowered for token in ["drawgameinfo", "displayconfig", "displayfiles", "s_callinventory", "ammo_selector", "object_list"]):
        return "frontend-display-menu-service"
    if any(token in lowered for token in ["del_cdfs", "change_cd", "s_cdplay", "s_cdstop"]):
        return "cd-load-audio-service"
    if any(token in lowered for token in ["gpu_flip", "s_playfmv", "main", "load_start"]):
        return "gpu-fmv-mainloop-service"
    return "frontend-display-menu-service"


def require_metadata_only(text: str) -> None:
    lowered = text.lower()
    for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
        if fragment in lowered:
            raise ValueError(f"Forbidden raw-evidence fragment in generated output: {fragment}")


def build_ghidra_platform_frontend_service_narrow_export(repo: Path) -> NarrowBundle:
    repo = Path(repo)
    validate_re342_handoff(repo)
    rows = read_csv(repo / RE342_CANDIDATES)
    if len(rows) != 6:
        raise ValueError(f"Expected 6 RE-342 platform/frontend candidates, got {len(rows)}")
    for row in rows:
        if row.get("source_cluster") != "platform-frontend-service-cluster":
            raise ValueError(f"Unexpected source cluster: {row.get('source_cluster')}")
        if row.get("ready_to_reopen_domain") != "no" or row.get("source_patch_authorized") != "no":
            raise ValueError(f"RE-342 candidate readiness drift: {row.get('candidate_id')}")

    candidate_rows: list[NarrowCandidateRow] = []
    buckets: dict[str, list[NarrowCandidateRow]] = defaultdict(list)
    for source in rows:
        subcluster = classify_subcluster(source["representative_source_context"], source["bridge_class"])
        row = NarrowCandidateRow(
            rank=0,
            source_rank=int(source["source_rank"]),
            candidate_id=source["candidate_id"],
            narrow_subcluster=subcluster,
            bridge_class=source["bridge_class"],
            body_size_bucket=source["body_size_bucket"],
            mapped_caller_count=int(source["mapped_caller_count"]),
            mapped_callee_count=int(source["mapped_callee_count"]),
            source_context_count=int(source["source_context_count"]),
            representative_source_context=source["representative_source_context"],
            readiness_gate="blocked-needs-candidate-level-proof",
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            next_probe="readiness-gate" if subcluster == SELECTED_SUBCLUSTER else "defer-after-re344",
            stop_condition="candidate-level source-symbolic proof required before domain selection",
        )
        buckets[subcluster].append(row)

    def bucket_sort(item: tuple[str, list[NarrowCandidateRow]]) -> tuple[int, int, int, str]:
        name, bucket = item
        return (
            SUBCLUSTER_PRIORITY.get(name, 99),
            -len(bucket),
            -sum(row.mapped_caller_count + row.mapped_callee_count for row in bucket),
            name,
        )

    subcluster_rows: list[NarrowSubclusterRow] = []
    for rank, (subcluster, bucket) in enumerate(sorted(buckets.items(), key=bucket_sort), start=1):
        bucket_sorted = sorted(bucket, key=lambda row: row.source_rank)
        selected = subcluster == SELECTED_SUBCLUSTER
        subcluster_rows.append(
            NarrowSubclusterRow(
                rank=rank,
                narrow_subcluster=subcluster,
                candidate_count=len(bucket_sorted),
                mapped_caller_total=sum(row.mapped_caller_count for row in bucket_sorted),
                mapped_callee_total=sum(row.mapped_callee_count for row in bucket_sorted),
                max_source_context_count=max(row.source_context_count for row in bucket_sorted),
                bridge_classes=";".join(sorted({row.bridge_class for row in bucket_sorted})),
                representative_source_context=bucket_sorted[0].representative_source_context,
                selection_status="selected-next" if selected else "deferred-after-selected-subcluster",
                gate_decision="gate-before-proof-domain" if selected else "defer-after-re344",
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                next_ticket="RE-344" if selected else "TBD",
                next_topic="cd-load-audio-service-readiness-gate" if selected else "defer-after-re344",
                stop_condition=(
                    "candidate-level source-symbolic proof required before proof-domain selection"
                    if selected
                    else "wait for selected subcluster readiness gate"
                ),
            )
        )
        for row in bucket_sorted:
            candidate_rows.append(
                NarrowCandidateRow(
                    rank=len(candidate_rows) + 1,
                    source_rank=row.source_rank,
                    candidate_id=row.candidate_id,
                    narrow_subcluster=row.narrow_subcluster,
                    bridge_class=row.bridge_class,
                    body_size_bucket=row.body_size_bucket,
                    mapped_caller_count=row.mapped_caller_count,
                    mapped_callee_count=row.mapped_callee_count,
                    source_context_count=row.source_context_count,
                    representative_source_context=row.representative_source_context,
                    readiness_gate=row.readiness_gate,
                    ready_to_reopen_domain=row.ready_to_reopen_domain,
                    source_patch_authorized=row.source_patch_authorized,
                    next_probe=row.next_probe,
                    stop_condition=row.stop_condition,
                )
            )

    selected_candidates = [row for row in candidate_rows if row.narrow_subcluster == SELECTED_SUBCLUSTER]
    summary = NarrowSummary(
        story_id="RE-343",
        topic="ghidra-platform-frontend-service-cluster-narrow-export",
        upstream_handoff="RE-342",
        focus_cluster="platform-frontend-service-cluster",
        focus_candidate_count=len(rows),
        narrow_subcluster_count=len(subcluster_rows),
        selected_narrow_subcluster=SELECTED_SUBCLUSTER,
        selected_narrow_candidate_count=len(selected_candidates),
        selected_candidate_ids=";".join(row.candidate_id for row in selected_candidates),
        ready_to_reopen_domain_count=0,
        source_patch_authorized_count=0,
        selected_domain="none",
        selected_pivot="none",
        next_ticket="RE-344",
        next_topic="cd-load-audio-service-readiness-gate",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="platform/frontend cluster narrowed; gate selected cd/load/audio service before proof-domain selection",
    )
    return NarrowBundle(subcluster_rows=subcluster_rows, candidate_rows=candidate_rows, summary=summary)


def write_csv(path: Path, rows: list[object], row_type: type) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(row_type)], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def render_md(bundle: NarrowBundle) -> str:
    s = bundle.summary
    text = f"""# RE-343 Ghidra platform/frontend service narrow export

## Purpose

Narrow the RE-342 selected `{s.focus_cluster}` source-symbolic cluster into deterministic subclusters without exposing raw Ghidra identity.

## Inputs

- Upstream handoff: `{RE342_HANDOFF}`
- Selected candidates: `{RE342_CANDIDATES}`

## Selection

Selected `{s.selected_narrow_subcluster}` with `{s.selected_narrow_candidate_count}` candidates.

## Counts

- Focus candidates: `{s.focus_candidate_count}`
- Narrow subclusters: `{s.narrow_subcluster_count}`
- Ready to reopen domain: `{s.ready_to_reopen_domain_count}`
- Source patch authorized: `{s.source_patch_authorized_count}`

## Readiness

Domain and pivot remain `{s.selected_domain}` / `{s.selected_pivot}`. Code readiness remains `{s.code_change_readiness}` until `{s.selected_narrow_subcluster}` passes a candidate-level readiness gate.

## Handoff

- Next ticket: `{s.next_ticket}`
- Next topic: `{s.next_topic}`
- Stop condition: `{s.stop_condition}`
"""
    require_metadata_only(text)
    return text


def render_story(bundle: NarrowBundle) -> str:
    s = bundle.summary
    text = f"""# RE-343 Ghidra platform/frontend service narrow export

## Goal

Produce a metadata-only narrow export for the RE-342 platform/frontend Ghidra bridge cluster and select the next readiness-gate subcluster.

## Inputs

- Upstream handoff: `{RE342_HANDOFF}`
- Selected candidates: `{RE342_CANDIDATES}`

## Progress tracker

- [x] RE-342 platform/frontend cluster selection validated.
- [x] Platform/frontend candidate rows grouped into narrow service subclusters.
- [x] CD/load/audio service selected for the next readiness gate.
- [x] Domain and pivot selection kept blocked.
- [x] Source/code patch authorization denied.

## Generated artifacts

- `{SUBCLUSTERS_CSV}`
- `{CANDIDATES_CSV}`
- `{SUMMARY_CSV}`
- `{HANDOFF_CSV}`
- `{MD_OUTPUT}`

## Findings

- Focus cluster: `{s.focus_cluster}`
- Focus candidate count: `{s.focus_candidate_count}`
- Narrow subcluster count: `{s.narrow_subcluster_count}`
- Selected narrow subcluster: `{s.selected_narrow_subcluster}`
- Selected candidate count: `{s.selected_narrow_candidate_count}`
- Ready to reopen domain selection: `{s.ready_to_reopen_domain_count}`
- Source patch authorized rows: `{s.source_patch_authorized_count}`

## Readiness decision

The selected service subcluster is source-symbolic only. Domain and pivot stay `{s.selected_domain}` / `{s.selected_pivot}`, and code readiness remains `{s.code_change_readiness}` pending candidate-level proof.

## Follow-up ticket breakdown

- `{s.next_ticket}` / `{s.next_topic}`: gate `{s.selected_narrow_subcluster}` and decide whether any candidate can reopen a proof domain.
  - Inputs: RE-343 narrowed subcluster/candidate CSVs.
  - Deliverables: candidate-level readiness rows, summary/handoff, story.
  - Stop condition: if every row lacks candidate-level proof, keep source/code readiness blocked and continue to the next deferred service subcluster.

## Validation commands

- `python -m pytest tests/reverse/test_re343_ghidra_platform_frontend_service_narrow_export.py -q`
- `python scripts/reverse/re343_ghidra_platform_frontend_service_narrow_export.py --repo .`
- `python -m pytest tests/reverse -q`
"""
    require_metadata_only(text)
    return text


def write_all_artifacts(bundle: NarrowBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    outputs = {
        "subclusters_csv": repo / SUBCLUSTERS_CSV,
        "candidates_csv": repo / CANDIDATES_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_csv(outputs["subclusters_csv"], bundle.subcluster_rows, NarrowSubclusterRow)
    write_csv(outputs["candidates_csv"], bundle.candidate_rows, NarrowCandidateRow)
    write_csv(outputs["summary_csv"], [bundle.summary], NarrowSummary)
    write_csv(outputs["handoff_csv"], [bundle.summary], NarrowSummary)
    outputs["md"].parent.mkdir(parents=True, exist_ok=True)
    outputs["md"].write_text(render_md(bundle), encoding="utf-8")
    outputs["story"].parent.mkdir(parents=True, exist_ok=True)
    outputs["story"].write_text(render_story(bundle), encoding="utf-8")
    for path in outputs.values():
        require_metadata_only(path.read_text(encoding="utf-8"))
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".", type=Path)
    args = parser.parse_args()
    bundle = build_ghidra_platform_frontend_service_narrow_export(args.repo)
    outputs = write_all_artifacts(bundle, args.repo)
    for key, path in outputs.items():
        print(f"{key}: {path.relative_to(args.repo)}")


if __name__ == "__main__":
    main()
