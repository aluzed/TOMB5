#!/usr/bin/env python3
"""Gate RE-309 Ghidra bridge candidates into safe follow-up clusters."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE309_HANDOFF = "docs/reverse/generated/re309-ghidra-unmapped-bridge-candidates-handoff.csv"
RE309_CANDIDATES = "docs/reverse/generated/re309-ghidra-unmapped-bridge-candidates.csv"
CLUSTERS_CSV = "docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-clusters.csv"
CANDIDATES_CSV = "docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-candidates.csv"
SUMMARY_CSV = "docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re310-ghidra-bridge-candidate-readiness-gate.md"
STORY = "docs/stories/RE-310-ghidra-bridge-candidate-readiness-gate.md"

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

CLUSTER_PRIORITY = {
    "collision-switch-door-cluster": 0,
    "platform-frontend-service-cluster": 1,
    "effects-lighting-cluster": 2,
    "maths-render-cluster": 3,
    "lara-combat-camera-cluster": 4,
    "gameflow-save-runtime-cluster": 5,
    "actor-ai-cluster": 6,
    "generic-runtime-helper-cluster": 7,
}


@dataclass(frozen=True)
class GateCandidateRow:
    rank: int
    candidate_id: str
    source_cluster_rank: int
    source_cluster: str
    gate_decision: str
    focus_cluster: str
    bridge_class: str
    body_size_bucket: str
    mapped_caller_count: int
    mapped_callee_count: int
    source_context_count: int
    representative_source_context: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    next_gate: str
    stop_condition: str


@dataclass(frozen=True)
class GateClusterRow:
    rank: int
    cluster: str
    candidate_count: int
    focus_candidate_count: int
    mapped_caller_total: int
    mapped_callee_total: int
    max_source_context_count: int
    bridge_classes: str
    representative_source_context: str
    gate_decision: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    next_ticket: str
    next_topic: str
    stop_condition: str


@dataclass(frozen=True)
class GateSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    input_candidate_count: int
    cluster_count: int
    focus_candidate_count: int
    ready_to_reopen_domain_count: int
    source_patch_authorized_count: int
    selected_followup_cluster: str
    selected_domain: str
    selected_pivot: str
    next_ticket: str
    next_topic: str
    metadata_work_readiness: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class GateBundle:
    cluster_rows: list[GateClusterRow]
    candidate_rows: list[GateCandidateRow]
    summary: GateSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def one_row(repo: Path, rel_path: str) -> dict[str, str]:
    rows = read_csv(repo / rel_path)
    if len(rows) != 1:
        raise ValueError(f"{rel_path} must contain exactly one row")
    return rows[0]


def validate_re309_handoff(repo: Path) -> None:
    row = one_row(repo, RE309_HANDOFF)
    expected = {
        "story_id": "RE-309",
        "next_ticket": "RE-310",
        "next_topic": "ghidra-bridge-candidate-readiness-gate",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "selected_domain": "none",
        "selected_pivot": "none",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-309 handoff drift: {key}={row.get(key)!r}")


def classify_cluster(source_context: str) -> str:
    text = source_context.lower()
    if any(token in text for token in ["collision", "trapdoor", "switch", "doorcontrol", "fallingceiling", "fullblock"]):
        return "collision-switch-door-cluster"
    if any(token in text for token in ["gpu_", "load_start", "s_playfmv", "initnewcdsystem", "del_cdfs", "s_cdplay", "displayfiles"]):
        return "platform-frontend-service-cluster"
    if any(token in text for token in ["blink", "colouredlight", "torch", "flare", "explosion", "spark", "smoke", "light"]):
        return "effects-lighting-cluster"
    if any(token in text for token in ["mpopmatrix", "mpushmatrix", "mtranslate", "drawrooms", "matrix"]):
        return "maths-render-cluster"
    if any(token in text for token in ["lara", "fireweapon", "combatcamera", "doproperdetection"]):
        return "lara-combat-camera-cluster"
    if any(token in text for token in ["save", "restore", "gameflow", "dolevel"]):
        return "gameflow-save-runtime-cluster"
    if any(token in text for token in ["andrea", "andy", "cossack", "actorblood"]):
        return "actor-ai-cluster"
    return "generic-runtime-helper-cluster"


def safe_context_slice(source_context: str, max_items: int = 6) -> str:
    values = [part for part in source_context.split(";") if part]
    return ";".join(values[:max_items])


def write_csv(path: Path, rows: list[object], row_type: type) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(row_type)], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def build_ghidra_bridge_candidate_readiness_gate(repo: Path) -> GateBundle:
    repo = Path(repo)
    validate_re309_handoff(repo)
    candidates = read_csv(repo / RE309_CANDIDATES)
    if len(candidates) != 25:
        raise ValueError(f"Expected 25 RE-309 top candidates, got {len(candidates)}")

    buckets: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in candidates:
        if row.get("ready_to_reopen_domain") != "no" or row.get("source_patch_authorized") != "no":
            raise ValueError(f"RE-309 candidate readiness drift: {row.get('candidate_id')}")
        cluster = classify_cluster(row.get("safe_source_context", ""))
        buckets[cluster].append(row)

    def cluster_sort(item: tuple[str, list[dict[str, str]]]) -> tuple[int, int, int, str]:
        cluster, rows = item
        return (
            CLUSTER_PRIORITY.get(cluster, 99),
            -len(rows),
            -sum(int(row["mapped_caller_count"]) + int(row["mapped_callee_count"]) for row in rows),
            cluster,
        )

    cluster_rows: list[GateClusterRow] = []
    candidate_rows: list[GateCandidateRow] = []
    selected_cluster = "collision-switch-door-cluster"
    for cluster_rank, (cluster, rows) in enumerate(sorted(buckets.items(), key=cluster_sort), start=1):
        rows_sorted = sorted(rows, key=lambda row: int(row["rank"]))
        mapped_caller_total = sum(int(row["mapped_caller_count"]) for row in rows_sorted)
        mapped_callee_total = sum(int(row["mapped_callee_count"]) for row in rows_sorted)
        max_context = max(int(row["source_context_count"]) for row in rows_sorted)
        bridge_classes = ";".join(sorted({row["bridge_class"] for row in rows_sorted}))
        representative_context = safe_context_slice(rows_sorted[0]["safe_source_context"])
        focus = cluster == selected_cluster
        decision = "needs-narrow-source-symbolic-export" if focus else "defer-after-focus-cluster"
        next_ticket = "RE-311" if focus else "TBD"
        next_topic = "ghidra-collision-switch-door-cluster-narrow-export" if focus else "defer-after-re311"
        cluster_rows.append(
            GateClusterRow(
                rank=cluster_rank,
                cluster=cluster,
                candidate_count=len(rows_sorted),
                focus_candidate_count=len(rows_sorted) if focus else 0,
                mapped_caller_total=mapped_caller_total,
                mapped_callee_total=mapped_callee_total,
                max_source_context_count=max_context,
                bridge_classes=bridge_classes,
                representative_source_context=representative_context,
                gate_decision=decision,
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                next_ticket=next_ticket,
                next_topic=next_topic,
                stop_condition="narrow source-symbolic export required before proof-domain selection" if focus else "wait for focus cluster gate result",
            )
        )
        for source_row in rows_sorted:
            candidate_rows.append(
                GateCandidateRow(
                    rank=int(source_row["rank"]),
                    candidate_id=source_row["candidate_id"],
                    source_cluster_rank=cluster_rank,
                    source_cluster=cluster,
                    gate_decision=decision,
                    focus_cluster="yes" if focus else "no",
                    bridge_class=source_row["bridge_class"],
                    body_size_bucket=source_row["body_size_bucket"],
                    mapped_caller_count=int(source_row["mapped_caller_count"]),
                    mapped_callee_count=int(source_row["mapped_callee_count"]),
                    source_context_count=int(source_row["source_context_count"]),
                    representative_source_context=safe_context_slice(source_row["safe_source_context"]),
                    ready_to_reopen_domain="no",
                    source_patch_authorized="no",
                    next_gate="ghidra-collision-switch-door-cluster-narrow-export" if focus else "defer-after-focus-cluster",
                    stop_condition="candidate remains source-symbolic until narrowed export is generated",
                )
            )
    candidate_rows.sort(key=lambda row: row.rank)
    focus_count = sum(row.focus_candidate_count for row in cluster_rows)
    summary = GateSummary(
        story_id="RE-310",
        topic="ghidra-bridge-candidate-readiness-gate",
        upstream_handoff="RE-309",
        input_candidate_count=len(candidates),
        cluster_count=len(cluster_rows),
        focus_candidate_count=focus_count,
        ready_to_reopen_domain_count=0,
        source_patch_authorized_count=0,
        selected_followup_cluster=selected_cluster,
        selected_domain="none",
        selected_pivot="none",
        next_ticket="RE-311",
        next_topic="ghidra-collision-switch-door-cluster-narrow-export",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="generate a narrower source-symbolic export for the selected cluster before reopening proof-domain selection",
    )
    return GateBundle(cluster_rows=cluster_rows, candidate_rows=candidate_rows, summary=summary)


def render_markdown(bundle: GateBundle) -> str:
    summary = bundle.summary
    lines = [
        "# RE-310 Ghidra bridge candidate readiness gate",
        "",
        "## Summary",
        "",
        f"Gated `{summary.input_candidate_count}` RE-309 bridge candidates into `{summary.cluster_count}` source-symbolic clusters.",
        "No proof-domain is reopened by this gate; the selected follow-up is a narrower metadata export for one cluster.",
        "",
        "## Cluster decisions",
        "",
    ]
    for row in bundle.cluster_rows:
        lines.append(
            f"- rank `{row.rank}` `{row.cluster}`: candidates `{row.candidate_count}`, decision `{row.gate_decision}`, next `{row.next_topic}`"
        )
    lines.extend(
        [
            "",
            "## Readiness decision",
            "",
            "All candidates remain blocked for source/marker changes and for proof-domain reopening until a narrower source-symbolic export exists.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def render_story(bundle: GateBundle) -> str:
    summary = bundle.summary
    return "\n".join(
        [
            "# RE-310 Ghidra bridge candidate readiness gate",
            "",
            "## Goal",
            "",
            "Gate the RE-309 Ghidra bridge candidates by source-symbolic context and decide whether any candidate can reopen proof-domain selection.",
            "",
            "## Inputs",
            "",
            f"- Upstream handoff: `{RE309_HANDOFF}`",
            f"- Candidate export: `{RE309_CANDIDATES}`",
            "",
            "## Progress tracker",
            "",
            "- [x] RE-309 candidate export validated.",
            "- [x] Candidates grouped by safe source-symbolic context.",
            "- [x] Cluster-level readiness gate emitted.",
            "- [x] Source/marker patch authorization denied for every row.",
            "- [x] Follow-up narrow export selected before proof-domain reopening.",
            "",
            "## Generated artifacts",
            "",
            f"- `{CLUSTERS_CSV}`",
            f"- `{CANDIDATES_CSV}`",
            f"- `{SUMMARY_CSV}`",
            f"- `{HANDOFF_CSV}`",
            f"- `{MD_OUTPUT}`",
            "",
            "## Findings",
            "",
            f"- Input candidates: `{summary.input_candidate_count}`",
            f"- Source-symbolic clusters: `{summary.cluster_count}`",
            f"- Selected follow-up cluster: `{summary.selected_followup_cluster}`",
            f"- Focus candidates: `{summary.focus_candidate_count}`",
            f"- Ready to reopen domain selection: `{summary.ready_to_reopen_domain_count}`",
            f"- Source patch authorized rows: `{summary.source_patch_authorized_count}`",
            "",
            "## Readiness decision",
            "",
            "The gate selects a narrowed metadata follow-up, not a proof domain. Domain/pivot remain `none` and code readiness remains blocked.",
            "",
            "## Follow-up ticket breakdown",
            "",
            "- `RE-311` / `ghidra-collision-switch-door-cluster-narrow-export`: produce a narrower metadata-only source-symbolic export for the selected collision/switch/door cluster.",
            "  - Inputs: RE-310 clusters/candidates plus RE-309 candidate IDs and local Ghidra/repo maps.",
            "  - Deliverables: cluster-specific candidate metadata, blocker rows, and a readiness handoff that still excludes raw Ghidra addresses/names from versioned outputs.",
            "  - Stop condition: if the narrow export still cannot separate a proof-first pivot, keep selected domain/pivot `none` and hand off to a more specific source-symbolic evidence request.",
            "",
            "## Validation commands",
            "",
            "- `python -m pytest tests/reverse/test_re310_ghidra_bridge_candidate_readiness_gate.py -q`",
            "- `python scripts/reverse/re310_ghidra_bridge_candidate_readiness_gate.py --repo .`",
            "- `python -m pytest tests/reverse -q`",
            "",
        ]
    )


def write_all_artifacts(bundle: GateBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "clusters_csv": repo / CLUSTERS_CSV,
        "candidates_csv": repo / CANDIDATES_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_csv(paths["clusters_csv"], bundle.cluster_rows, GateClusterRow)
    write_csv(paths["candidates_csv"], bundle.candidate_rows, GateCandidateRow)
    write_csv(paths["summary_csv"], [bundle.summary], GateSummary)
    write_csv(paths["handoff_csv"], [bundle.summary], GateSummary)
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text(render_markdown(bundle), encoding="utf-8")
    paths["story"].parent.mkdir(parents=True, exist_ok=True)
    paths["story"].write_text(render_story(bundle), encoding="utf-8")
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository root")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    bundle = build_ghidra_bridge_candidate_readiness_gate(repo)
    written = write_all_artifacts(bundle, repo)
    for key, path in written.items():
        print(f"{key}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
