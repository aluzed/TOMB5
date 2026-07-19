#!/usr/bin/env python3
"""Generate RE-392 narrowed metadata export for the lara/combat/camera Ghidra bridge cluster."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE391_HANDOFF = "docs/reverse/generated/re391-post-maths-render-next-ghidra-cluster-selection-handoff.csv"
RE391_CANDIDATES = "docs/reverse/generated/re391-post-maths-render-next-ghidra-cluster-selection-candidates.csv"
SUBCLUSTERS_CSV = "docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-subclusters.csv"
CANDIDATES_CSV = "docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-candidates.csv"
SUMMARY_CSV = "docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re392-ghidra-lara-combat-camera-cluster-narrow-export.md"
STORY = "docs/stories/RE-392-ghidra-lara-combat-camera-cluster-narrow-export.md"

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

SUBCLUSTER_PRIORITY = {"lara-control-service": 0, "combat-camera-service": 1}
SELECTED_SUBCLUSTER = "lara-control-service"
SELECTED_CANDIDATE_IDS = ("4a632b41837e", "0aaa76206517")
NEXT_TICKET = "RE-393"
NEXT_TOPIC = "lara-control-service-readiness-gate"
DEFER_AFTER_NEXT = "defer-after-re393"


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


def validate_re391_handoff(repo: Path) -> None:
    row = one_row(repo, RE391_HANDOFF)
    expected = {
        "story_id": "RE-391",
        "next_ticket": "RE-392",
        "next_topic": "ghidra-lara-combat-camera-cluster-narrow-export",
        "selected_followup_cluster": "lara-combat-camera-cluster",
        "selected_candidate_count": "2",
        "selected_candidate_ids": ";".join(SELECTED_CANDIDATE_IDS),
        "selected_domain": "none",
        "selected_pivot": "none",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-391 handoff drift: {key}={row.get(key)!r}")


def classify_subcluster(context: str) -> str:
    lowered = context.lower()
    lara_tokens = ("laracontrol", "laraabove", "larasurface", "laracollide", "laradoclimb", "delalignlara")
    camera_tokens = ("camera", "target", "detection", "missile", "bodypart")
    if any(token in lowered for token in camera_tokens):
        return "combat-camera-service"
    if any(token in lowered for token in lara_tokens):
        return "lara-control-service"
    raise ValueError("Lara/combat/camera candidate lacks expected source-symbolic context")


def require_metadata_only(text: str) -> None:
    lowered = text.lower()
    for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
        if fragment in lowered:
            raise ValueError(f"Forbidden raw-evidence fragment in generated output: {fragment}")


def build_ghidra_lara_combat_camera_cluster_narrow_export(repo: Path) -> NarrowBundle:
    repo = Path(repo)
    validate_re391_handoff(repo)
    rows = read_csv(repo / RE391_CANDIDATES)
    if len(rows) != 2:
        raise ValueError(f"Expected 2 RE-391 lara/combat/camera candidates, got {len(rows)}")
    if tuple(row.get("candidate_id") for row in rows) != SELECTED_CANDIDATE_IDS:
        raise ValueError("RE-391 lara/combat/camera candidate order drift")
    for row in rows:
        if row.get("source_cluster") != "lara-combat-camera-cluster":
            raise ValueError(f"Unexpected source cluster: {row.get('source_cluster')}")
        if row.get("ready_to_reopen_domain") != "no" or row.get("source_patch_authorized") != "no":
            raise ValueError(f"RE-391 candidate readiness drift: {row.get('candidate_id')}")

    buckets: dict[str, list[NarrowCandidateRow]] = defaultdict(list)
    for source in rows:
        subcluster = classify_subcluster(source["representative_source_context"])
        buckets[subcluster].append(
            NarrowCandidateRow(
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
                next_probe="readiness-gate" if subcluster == SELECTED_SUBCLUSTER else DEFER_AFTER_NEXT,
                stop_condition="candidate-level source-symbolic proof required before domain selection",
            )
        )

    def bucket_sort(item: tuple[str, list[NarrowCandidateRow]]) -> tuple[int, int, int, str]:
        name, bucket = item
        return (
            SUBCLUSTER_PRIORITY.get(name, 99),
            -len(bucket),
            -sum(row.mapped_caller_count + row.mapped_callee_count for row in bucket),
            name,
        )

    subcluster_rows: list[NarrowSubclusterRow] = []
    candidate_rows: list[NarrowCandidateRow] = []
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
                gate_decision="gate-before-proof-domain" if selected else DEFER_AFTER_NEXT,
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                next_ticket=NEXT_TICKET if selected else "TBD",
                next_topic=NEXT_TOPIC if selected else DEFER_AFTER_NEXT,
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
        story_id="RE-392",
        topic="ghidra-lara-combat-camera-cluster-narrow-export",
        upstream_handoff="RE-391",
        focus_cluster="lara-combat-camera-cluster",
        focus_candidate_count=len(rows),
        narrow_subcluster_count=len(subcluster_rows),
        selected_narrow_subcluster=SELECTED_SUBCLUSTER,
        selected_narrow_candidate_count=len(selected_candidates),
        selected_candidate_ids=";".join(row.candidate_id for row in selected_candidates),
        ready_to_reopen_domain_count=0,
        source_patch_authorized_count=0,
        selected_domain="none",
        selected_pivot="none",
        next_ticket=NEXT_TICKET,
        next_topic=NEXT_TOPIC,
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="lara/combat/camera cluster narrowed; gate selected lara control service before proof-domain selection",
    )
    return NarrowBundle(subcluster_rows=subcluster_rows, candidate_rows=candidate_rows, summary=summary)


def write_csv(path: Path, rows: list[object], row_type: type[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(row_type)], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def render_md(bundle: NarrowBundle) -> str:
    s = bundle.summary
    text = f"""# RE-392 Ghidra lara/combat/camera cluster narrow export

## Purpose

Narrow the RE-391 selected `{s.focus_cluster}` source-symbolic cluster into deterministic subclusters without exposing raw Ghidra identity.

## Inputs

- Upstream handoff: `{RE391_HANDOFF}`
- Selected candidates: `{RE391_CANDIDATES}`

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
    text = f"""# RE-392 Ghidra lara/combat/camera cluster narrow export

## Goal

Produce a metadata-only narrow export for the RE-391 lara/combat/camera Ghidra bridge cluster and select the next readiness-gate subcluster.

## Inputs

- Upstream handoff: `{RE391_HANDOFF}`
- Selected candidates: `{RE391_CANDIDATES}`

## Progress tracker

- [x] RE-391 lara/combat/camera cluster selection validated.
- [x] Lara/combat/camera candidate rows grouped into narrow service subclusters.
- [x] Lara control service selected for the next readiness gate.
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
  - Inputs: RE-392 narrowed subcluster/candidate CSVs.
  - Deliverables: candidate-level readiness rows, summary/handoff, story.
  - Stop condition: if every row lacks candidate-level proof, keep source/code readiness blocked and continue to the next deferred bridge cluster.

## Validation commands

- `python -m pytest tests/reverse/test_re392_ghidra_lara_combat_camera_cluster_narrow_export.py -q`
- `python scripts/reverse/re392_ghidra_lara_combat_camera_cluster_narrow_export.py --repo .`
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
    bundle = build_ghidra_lara_combat_camera_cluster_narrow_export(args.repo)
    outputs = write_all_artifacts(bundle, args.repo)
    for key, path in outputs.items():
        print(f"{key}: {path.relative_to(args.repo)}")


if __name__ == "__main__":
    main()
