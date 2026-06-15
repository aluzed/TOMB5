#!/usr/bin/env python3
"""Generate RE-169 SPEC_PSXPC_N next-cluster selection artifacts.

This metadata-only gate consumes the RE-168 no-patch handoff, excludes the
blocked ui-text-rendering cluster, and selects the next smallest SPEC_PSXPC_N
proof target without authorizing source or marker changes.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

UPSTREAM_HANDOFF = "docs/reverse/generated/re168-ui-text-rendering-source-patch-handoff.csv"
SOURCE_CLUSTERS = "docs/reverse/generated/re163-module-spec-psxpc-n-clusters.csv"
SOURCE_TICKET_PLAN = "docs/reverse/generated/re163-module-spec-psxpc-n-ticket-plan.csv"
SELECTION_CSV = "docs/reverse/generated/re169-module-spec-psxpc-n-next-cluster-selection.csv"
HANDOFF_CSV = "docs/reverse/generated/re169-module-spec-psxpc-n-next-cluster-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re169-module-spec-psxpc-n-next-cluster-selection.md"
STORY_OUTPUT = "docs/stories/RE-169-module-spec-psxpc-n-next-cluster-selection.md"

FORBIDDEN = (
    "word_le_hex",
    "payload_offset",
    "dump row",
    "opcode",
    "machine word",
    "call_address",
    "branch target",
    "call target",
    "0x",
)

PROOF_RECOMMENDATIONS = {
    "geometry-support": "source-level geometry state contract and non-raw equivalence gate",
    "frontend-loadsave": "frontend save/load state contract and non-raw equivalence gate",
    "frontend-sequence": "frontend sequencing caller/state proof before marker changes",
    "platform-gpu-display": "ND marker behavior audit and display-side state proof",
    "platform-main-lifecycle": "ND marker lifecycle audit with startup/shutdown state proof",
    "platform-memory": "ND marker allocation contract audit with source-level callers",
}


@dataclass(frozen=True)
class ClusterSelectionRow:
    rank: int
    cluster: str
    candidate_count: int
    mapped_count: int
    nd_count: int
    runtime_count: int
    top_function: str
    representative_functions: str
    prior_readiness: str
    selection_decision: str
    recommended_proof: str
    blocker: str
    next_action: str
    next_ticket: str
    code_change_readiness: str


@dataclass(frozen=True)
class NextClusterSelection:
    story_id: str
    upstream_ticket: str
    current_cluster: str
    upstream_outcome: str
    selected_cluster: str
    selected_pivot: str
    selection_status: str
    next_ticket: str
    next_topic: str
    code_change_readiness: str
    rows: tuple[ClusterSelectionRow, ...]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_int(value: str | None) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def validate_upstream_handoff(rows: list[dict[str, str]]) -> dict[str, str]:
    if len(rows) != 1:
        raise ValueError("RE-168 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "next_ticket": "RE-169",
        "next_topic": "module-spec-psxpc-n-next-cluster-selection",
        "current_cluster": "ui-text-rendering",
        "outcome": "ui-text-rendering-source-patch-denied",
        "dependency": "RE-168 no-patch gate",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-168 handoff drift: expected {key}={value!r}, got {row.get(key)!r}")
    return row


def validate_ticket_plan(rows: list[dict[str, str]]) -> None:
    by_id = {row.get("story_id"): row for row in rows}
    row = by_id.get("RE-169")
    if not row:
        raise ValueError("RE-163 ticket plan does not name RE-169")
    expected = {
        "topic": "module-spec-psxpc-n-next-cluster-selection",
        "scope": "remaining SPEC_PSXPC_N clusters",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-169 ticket-plan drift: expected {key}={value!r}, got {row.get(key)!r}")


def cluster_priority(row: dict[str, str]) -> tuple[int, int, int, int]:
    readiness = row.get("readiness", "")
    nd_count = parse_int(row.get("nd_count"))
    runtime_count = parse_int(row.get("runtime_count"))
    candidate_count = parse_int(row.get("candidate_count"))
    if readiness == "proof-needed" and nd_count == 0 and runtime_count == 0:
        tier = 0
    elif readiness == "proof-needed":
        tier = 1
    elif readiness == "nd-marker-audit-later":
        tier = 2
    else:
        tier = 3
    return (tier, nd_count, runtime_count, candidate_count)


def decision_for(row: dict[str, str], selected_cluster: str) -> tuple[str, str, str]:
    cluster = row.get("cluster", "")
    if cluster == selected_cluster:
        return (
            "selected",
            "handoff-to-re170-closure-or-cluster-proof-gate",
            "RE-170",
        )
    if row.get("readiness") == "nd-marker-audit-later":
        return ("deferred-nd-marker-audit", "defer until non-ND proof clusters are handled", "TBD")
    return ("deferred-after-selected-cluster", "defer until selected cluster is closed or handed off", "TBD")


def build_next_cluster_selection(repo: Path) -> NextClusterSelection:
    repo = Path(repo)
    upstream = validate_upstream_handoff(read_csv(repo / UPSTREAM_HANDOFF))
    validate_ticket_plan(read_csv(repo / SOURCE_TICKET_PLAN))
    clusters = read_csv(repo / SOURCE_CLUSTERS)

    remaining = [row for row in clusters if row.get("cluster") != upstream["current_cluster"]]
    if not remaining:
        raise ValueError("No remaining SPEC_PSXPC_N clusters after ui-text-rendering")

    selected_source = sorted(remaining, key=cluster_priority)[0]
    selected_cluster = selected_source.get("cluster", "")
    selected_pivot = selected_source.get("top_function", "")

    ranked = sorted(remaining, key=cluster_priority)
    rows: list[ClusterSelectionRow] = []
    for rank, row in enumerate(ranked, start=1):
        decision, action, next_ticket = decision_for(row, selected_cluster)
        cluster = row.get("cluster", "")
        rows.append(
            ClusterSelectionRow(
                rank=rank,
                cluster=cluster,
                candidate_count=parse_int(row.get("candidate_count")),
                mapped_count=parse_int(row.get("mapped_count")),
                nd_count=parse_int(row.get("nd_count")),
                runtime_count=parse_int(row.get("runtime_count")),
                top_function=row.get("top_function", ""),
                representative_functions=row.get("representative_functions", ""),
                prior_readiness=row.get("readiness", ""),
                selection_decision=decision,
                recommended_proof=PROOF_RECOMMENDATIONS.get(cluster, "source-level state contract and non-raw equivalence gate"),
                blocker=row.get("blocker", ""),
                next_action=action,
                next_ticket=next_ticket,
                code_change_readiness="blocked",
            )
        )

    return NextClusterSelection(
        story_id="RE-169",
        upstream_ticket="RE-168",
        current_cluster=upstream["current_cluster"],
        upstream_outcome=upstream["outcome"],
        selected_cluster=selected_cluster,
        selected_pivot=selected_pivot,
        selection_status="next-cluster-selected-source-patch-blocked",
        next_ticket="RE-170",
        next_topic="module-spec-psxpc-n-closure-or-handoff",
        code_change_readiness="documentation-only-selection-gate",
        rows=tuple(rows),
    )


def write_selection_csv(path: Path, selection: NextClusterSelection) -> None:
    fields = [
        "rank",
        "cluster",
        "candidate_count",
        "mapped_count",
        "nd_count",
        "runtime_count",
        "top_function",
        "representative_functions",
        "prior_readiness",
        "selection_decision",
        "recommended_proof",
        "blocker",
        "next_action",
        "next_ticket",
        "code_change_readiness",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in selection.rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def write_handoff_csv(path: Path, selection: NextClusterSelection) -> None:
    fields = [
        "next_ticket",
        "next_topic",
        "selected_cluster",
        "selected_pivot",
        "outcome",
        "reason",
        "dependency",
        "stop_condition",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerow(
            {
                "next_ticket": selection.next_ticket,
                "next_topic": selection.next_topic,
                "selected_cluster": selection.selected_cluster,
                "selected_pivot": selection.selected_pivot,
                "outcome": selection.selection_status,
                "reason": f"ui-text-rendering source patch denied; {selection.selected_cluster} is the next non-ND proof-needed SPEC_PSXPC_N cluster",
                "dependency": "RE-169 next-cluster selection",
                "stop_condition": "module SPEC_PSXPC_N closure or handoff emitted",
            }
        )


def write_markdown(path: Path, selection: NextClusterSelection) -> None:
    lines = [
        "# RE-169 module SPEC_PSXPC_N next-cluster selection",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-168 no-patch handoff consumed.",
        "- [x] UI text rendering cluster excluded from the remaining cluster shortlist.",
        "- [x] Remaining SPEC_PSXPC_N clusters ranked with metadata-only criteria.",
        "- [x] Next cluster and RE-170 handoff emitted without source or marker changes.",
        "",
        "## Decision",
        "",
        f"- upstream outcome: `{selection.upstream_outcome}`",
        f"- selected next cluster: `{selection.selected_cluster}`",
        f"- selected pivot: `{selection.selected_pivot}`",
        f"- next ticket: `{selection.next_ticket}` `{selection.next_topic}`",
        f"- code-change readiness: `{selection.code_change_readiness}`",
        "",
        "No production source or marker change is authorized by this selection gate.",
        "",
        "## Ranked remaining clusters",
        "",
    ]
    for row in selection.rows:
        lines.append(
            f"- #{row.rank} `{row.cluster}` / `{row.top_function}`: `{row.selection_decision}`; "
            f"readiness `{row.code_change_readiness}`; next `{row.next_ticket}`."
        )
    lines.extend(
        [
            "",
            "## Next proof",
            "",
            f"`{selection.next_ticket}` should use `{selection.selected_cluster}` / `{selection.selected_pivot}` to either emit a bounded proof handoff or close the module SPEC_PSXPC_N domain.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story(path: Path, selection: NextClusterSelection) -> None:
    lines = [
        "# RE-169 — Module SPEC_PSXPC_N next-cluster selection",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Select the next SPEC_PSXPC_N cluster after the UI text rendering no-patch gate.",
        "",
        "## Scope",
        "",
        "- depends on: `RE-168`, `RE-163`",
        "- safety contract: metadata-only cluster ranking; no production source or marker updates",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-168 no-patch handoff consumed.",
        "- [x] Remaining SPEC_PSXPC_N clusters loaded from RE-163.",
        "- [x] Next-cluster ranking emitted.",
        "- [x] RE-170 handoff emitted.",
        "- [x] Forbidden raw evidence excluded from generated artifacts.",
        "",
        "## Generated artifacts",
        "",
        f"- `{SELECTION_CSV}`",
        f"- `{HANDOFF_CSV}`",
        f"- `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- upstream cluster: `{selection.current_cluster}`",
        f"- upstream outcome: `{selection.upstream_outcome}`",
        f"- selected next cluster: `{selection.selected_cluster}`",
        f"- selected pivot: `{selection.selected_pivot}`",
        "- readiness: source and marker changes remain blocked pending cluster-specific proof",
        "",
        "## Follow-up breakdown",
        "",
        f"- `{selection.next_ticket}` `{selection.next_topic}`: consume this selection, decide whether `{selection.selected_cluster}` can open a bounded proof chain, or emit module closure/handoff.",
        "- Stop condition: closure or handoff artifact names the next objective without touching source unless an explicit readiness gate marks rows ready.",
        "",
        "## Validation",
        "",
        "- `python3 -m pytest tests/reverse/test_re169_module_spec_psxpc_n_next_cluster_selection.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over RE-169 outputs",
        "",
        "## Decision",
        "",
        f"Recommended next ticket: `{selection.next_ticket}`",
        f"Code-change readiness: `{selection.code_change_readiness}`",
        "No production source or marker change is authorized by this selection gate.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_all_artifacts(selection: NextClusterSelection, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "selection_csv": repo / SELECTION_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY_OUTPUT,
    }
    write_selection_csv(paths["selection_csv"], selection)
    write_handoff_csv(paths["handoff_csv"], selection)
    write_markdown(paths["md"], selection)
    write_story(paths["story"], selection)
    assert_metadata_only(paths)
    return paths


def assert_metadata_only(paths: dict[str, Path]) -> None:
    for path in paths.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            if fragment in text:
                raise ValueError(f"forbidden metadata fragment {fragment!r} in {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="repository root")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    selection = build_next_cluster_selection(repo)
    write_all_artifacts(selection, repo)
    print(f"selected_cluster={selection.selected_cluster}")
    print(f"selected_pivot={selection.selected_pivot}")
    print(f"next_ticket={selection.next_ticket}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
