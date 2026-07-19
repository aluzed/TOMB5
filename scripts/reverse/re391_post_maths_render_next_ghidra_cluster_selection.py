#!/usr/bin/env python3
"""Select the next Ghidra bridge cluster after maths/render exhaustion."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE390_HANDOFF = "docs/reverse/generated/re390-matrix-transform-core-readiness-gate-handoff.csv"
RE388_CLUSTERS = "docs/reverse/generated/re388-post-effects-lighting-next-ghidra-cluster-selection-clusters.csv"
RE310_CANDIDATES = "docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-candidates.csv"

CLUSTERS_CSV = "docs/reverse/generated/re391-post-maths-render-next-ghidra-cluster-selection-clusters.csv"
CANDIDATES_CSV = "docs/reverse/generated/re391-post-maths-render-next-ghidra-cluster-selection-candidates.csv"
SUMMARY_CSV = "docs/reverse/generated/re391-post-maths-render-next-ghidra-cluster-selection-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re391-post-maths-render-next-ghidra-cluster-selection-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re391-post-maths-render-next-ghidra-cluster-selection.md"
STORY = "docs/stories/RE-391-post-maths-render-next-ghidra-cluster-selection.md"

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
    "source_line_text",
    "ghidra_entry",
    "ghidra_name",
)

CLOSED_CLUSTERS = (
    "collision-switch-door-cluster",
    "platform-frontend-service-cluster",
    "effects-lighting-cluster",
    "maths-render-cluster",
)
SELECTED_CLUSTER = "lara-combat-camera-cluster"
SELECTED_CANDIDATE_IDS = ("4a632b41837e", "0aaa76206517")
NEXT_TICKET = "RE-392"
NEXT_TOPIC = "ghidra-lara-combat-camera-cluster-narrow-export"


@dataclass(frozen=True)
class NextClusterRow:
    rank: int
    source_rank: int
    cluster: str
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
    source_cluster: str
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
class NextClusterSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    parent_handoff: str
    parent_scope: str
    closed_clusters: str
    input_cluster_count: int
    closed_cluster_count: int
    deferred_cluster_count: int
    selected_followup_cluster: str
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
class NextClusterBundle:
    cluster_rows: list[NextClusterRow]
    candidate_rows: list[NextCandidateRow]
    summary: NextClusterSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def one_row(repo: Path, rel_path: str) -> dict[str, str]:
    rows = read_csv(repo / rel_path)
    if len(rows) != 1:
        raise ValueError(f"{rel_path} must contain exactly one row")
    return rows[0]


def validate_re390_exhaustion(repo: Path) -> None:
    row = one_row(repo, RE390_HANDOFF)
    expected = {
        "story_id": "RE-390",
        "next_ticket": "RE-391",
        "next_topic": "post-maths-render-next-ghidra-cluster-selection",
        "selected_narrow_subcluster": "matrix-transform-core",
        "input_candidate_count": "3",
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
            raise ValueError(f"RE-390 exhaustion drift: {key}={row.get(key)!r}")


def validate_re388_parent_queue(rows: list[dict[str, str]]) -> None:
    expected_order = [
        "maths-render-cluster",
        "lara-combat-camera-cluster",
        "gameflow-save-runtime-cluster",
        "actor-ai-cluster",
    ]
    actual_order = [row.get("cluster") for row in rows]
    if actual_order != expected_order:
        raise ValueError(f"RE-388 parent cluster queue drift: {actual_order!r}")
    if rows[0].get("selection_status") != "selected-next" or rows[0].get("cluster") != "maths-render-cluster":
        raise ValueError("RE-388 selected maths/render baseline drift")
    for row in rows:
        if row.get("ready_to_reopen_domain") != "no" or row.get("source_patch_authorized") != "no":
            raise ValueError(f"RE-388 cluster readiness drift: {row.get('cluster')}")


def require_metadata_only(text: str) -> None:
    lowered = text.lower()
    for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
        if fragment in lowered:
            raise ValueError(f"Forbidden raw-evidence fragment in generated output: {fragment}")


def build_post_maths_render_next_ghidra_cluster_selection(repo: Path) -> NextClusterBundle:
    repo = Path(repo)
    validate_re390_exhaustion(repo)
    source_clusters = read_csv(repo / RE388_CLUSTERS)
    validate_re388_parent_queue(source_clusters)

    deferred_clusters = [row for row in source_clusters if row["cluster"] not in CLOSED_CLUSTERS]
    if not deferred_clusters or deferred_clusters[0]["cluster"] != SELECTED_CLUSTER:
        raise ValueError("RE-388 deferred cluster ordering drift; cannot select lara/combat/camera cluster")

    cluster_rows: list[NextClusterRow] = []
    for rank, row in enumerate(deferred_clusters, start=1):
        selected = row["cluster"] == SELECTED_CLUSTER
        cluster_rows.append(
            NextClusterRow(
                rank=rank,
                source_rank=int(row["source_rank"]),
                cluster=row["cluster"],
                candidate_count=int(row["candidate_count"]),
                mapped_caller_total=int(row["mapped_caller_total"]),
                mapped_callee_total=int(row["mapped_callee_total"]),
                max_source_context_count=int(row["max_source_context_count"]),
                bridge_classes=row["bridge_classes"],
                representative_source_context=row["representative_source_context"],
                selection_status="selected-next" if selected else "deferred-after-selected-cluster",
                gate_decision="needs-narrow-source-symbolic-export" if selected else "defer-after-re392",
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                next_ticket=NEXT_TICKET if selected else "TBD",
                next_topic=NEXT_TOPIC if selected else "defer-after-re392",
                stop_condition=(
                    "narrow source-symbolic export required before proof-domain selection"
                    if selected
                    else "wait for selected cluster narrow export and gate result"
                ),
            )
        )

    source_candidates = read_csv(repo / RE310_CANDIDATES)
    selected_sources = [row for row in source_candidates if row["source_cluster"] == SELECTED_CLUSTER]
    selected_sources.sort(key=lambda row: int(row["rank"]))
    if tuple(row["candidate_id"] for row in selected_sources) != SELECTED_CANDIDATE_IDS:
        raise ValueError("RE-310 lara/combat/camera selected candidate drift")

    candidate_rows = [
        NextCandidateRow(
            rank=rank,
            source_rank=int(row["rank"]),
            candidate_id=row["candidate_id"],
            source_cluster=row["source_cluster"],
            bridge_class=row["bridge_class"],
            body_size_bucket=row["body_size_bucket"],
            mapped_caller_count=int(row["mapped_caller_count"]),
            mapped_callee_count=int(row["mapped_callee_count"]),
            source_context_count=int(row["source_context_count"]),
            representative_source_context=row["representative_source_context"],
            readiness_gate="blocked-needs-narrow-source-symbolic-export",
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            next_probe="narrow-source-symbolic-export",
            stop_condition="candidate remains source-symbolic until narrowed export is generated",
        )
        for rank, row in enumerate(selected_sources, start=1)
    ]

    summary = NextClusterSummary(
        story_id="RE-391",
        topic="post-maths-render-next-ghidra-cluster-selection",
        upstream_handoff="RE-390",
        parent_handoff="RE-388",
        parent_scope="ghidra-bridge-candidate-clusters",
        closed_clusters=";".join(CLOSED_CLUSTERS),
        input_cluster_count=len(source_clusters),
        closed_cluster_count=len(CLOSED_CLUSTERS),
        deferred_cluster_count=len(deferred_clusters),
        selected_followup_cluster=SELECTED_CLUSTER,
        selected_candidate_count=len(candidate_rows),
        selected_candidate_ids=";".join(row.candidate_id for row in candidate_rows),
        ready_to_reopen_domain_count=0,
        source_patch_authorized_count=0,
        selected_domain="none",
        selected_pivot="none",
        next_ticket=NEXT_TICKET,
        next_topic=NEXT_TOPIC,
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="maths/render cluster exhausted; select next deferred Ghidra bridge cluster for a narrow export",
    )
    return NextClusterBundle(cluster_rows=cluster_rows, candidate_rows=candidate_rows, summary=summary)


def write_csv(path: Path, rows: list[object], row_type: type[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(row_type)], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def render_md(bundle: NextClusterBundle) -> str:
    s = bundle.summary
    selected = bundle.cluster_rows[0]
    text = f"""# RE-391 post maths-render next Ghidra cluster selection

## Purpose

Close the exhausted maths/render bridge-cluster path from RE-390 and select the next deferred Ghidra bridge cluster without authorizing a proof domain or source patch.

## Inputs

- Exhaustion handoff: `{RE390_HANDOFF}`
- Parent cluster queue: `{RE388_CLUSTERS}`
- Parent candidates: `{RE310_CANDIDATES}`

## Selection

Selected `{s.selected_followup_cluster}` with `{s.selected_candidate_count}` source-symbolic candidates.

## Counts

- Input clusters: `{s.input_cluster_count}`
- Closed clusters: `{s.closed_cluster_count}`
- Deferred clusters: `{s.deferred_cluster_count}`
- Selected mapped caller total: `{selected.mapped_caller_total}`
- Selected mapped callee total: `{selected.mapped_callee_total}`
- Ready to reopen domain: `{s.ready_to_reopen_domain_count}`
- Source patch authorized: `{s.source_patch_authorized_count}`

## Readiness

Domain and pivot remain `{s.selected_domain}` / `{s.selected_pivot}`. Code readiness remains `{s.code_change_readiness}` because the selected cluster still needs a narrow source-symbolic export before any proof-domain selection.

## Handoff

- Next ticket: `{s.next_ticket}`
- Next topic: `{s.next_topic}`
- Stop condition: `{s.stop_condition}`

Code readiness remains `blocked`.
"""
    require_metadata_only(text)
    return text


def render_story(bundle: NextClusterBundle) -> str:
    s = bundle.summary
    text = f"""# RE-391 post maths-render next Ghidra cluster selection

## Goal

After RE-390 exhausted the maths/render matrix-transform-core queue, select the next deferred parent Ghidra bridge cluster autonomously instead of stopping at an exhausted topic.

## Inputs

- Exhaustion handoff: `{RE390_HANDOFF}`
- Parent Ghidra bridge cluster queue: `{RE388_CLUSTERS}`
- Parent Ghidra bridge candidate gate: `{RE310_CANDIDATES}`

## Progress tracker

- [x] RE-390 maths/render exhaustion validated.
- [x] RE-388 parent Ghidra bridge cluster queue re-opened.
- [x] Prior collision/switch/door, platform/frontend, effects/lighting, and maths/render clusters marked closed.
- [x] Next deferred cluster selected in parent order.
- [x] Source/domain readiness kept blocked pending a narrow export.

## Generated artifacts

- `{CLUSTERS_CSV}`
- `{CANDIDATES_CSV}`
- `{SUMMARY_CSV}`
- `{HANDOFF_CSV}`
- `{MD_OUTPUT}`

## Findings

- Parent scope: `{s.parent_scope}`
- Closed clusters: `{s.closed_clusters}`
- Deferred clusters: `{s.deferred_cluster_count}`
- Selected follow-up cluster: `{s.selected_followup_cluster}`
- Selected candidate count: `{s.selected_candidate_count}`
- Ready to reopen domain selection: `{s.ready_to_reopen_domain_count}`
- Source patch authorized rows: `{s.source_patch_authorized_count}`

## Readiness decision

The next safe hypothesis is `{s.selected_followup_cluster}`, but it remains source-symbolic. Domain and pivot stay `{s.selected_domain}` / `{s.selected_pivot}`, and code readiness remains `{s.code_change_readiness}` until a narrow export and gate establish candidate-level proof.

## Follow-up ticket breakdown

- `{s.next_ticket}` / `{s.next_topic}`: generate a metadata-only narrow source-symbolic export for `{s.selected_followup_cluster}`.
  - Inputs: RE-391 selected candidates and the local repo maps.
  - Deliverables: cluster-specific narrowed candidates, summary/handoff, and readiness-preserving story.
  - Stop condition: if the export still lacks candidate-level proof, keep source/code readiness blocked and hand off to a readiness gate.

## Validation commands

- `python -m pytest tests/reverse/test_re391_post_maths_render_next_ghidra_cluster_selection.py -q`
- `python scripts/reverse/re391_post_maths_render_next_ghidra_cluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
"""
    require_metadata_only(text)
    return text


def write_all_artifacts(bundle: NextClusterBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    written = {
        "clusters_csv": repo / CLUSTERS_CSV,
        "candidates_csv": repo / CANDIDATES_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
    }
    write_csv(written["clusters_csv"], bundle.cluster_rows, NextClusterRow)
    write_csv(written["candidates_csv"], bundle.candidate_rows, NextCandidateRow)
    write_csv(written["summary_csv"], [bundle.summary], NextClusterSummary)
    write_csv(written["handoff_csv"], [bundle.summary], NextClusterSummary)

    md = repo / MD_OUTPUT
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text(render_md(bundle), encoding="utf-8")
    written["md"] = md

    story = repo / STORY
    story.parent.mkdir(parents=True, exist_ok=True)
    story.write_text(render_story(bundle), encoding="utf-8")
    written["story"] = story

    for path in written.values():
        require_metadata_only(path.read_text(encoding="utf-8"))
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()
    bundle = build_post_maths_render_next_ghidra_cluster_selection(repo)
    written = write_all_artifacts(bundle, repo)
    for label, path in written.items():
        print(f"{label}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
