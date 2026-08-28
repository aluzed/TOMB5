#!/usr/bin/env python3
"""Emit a terminal, aggregate-only proof-acquisition policy for unmatched Ghidra mapping."""
from __future__ import annotations

import csv

from dataclasses import dataclass
from pathlib import Path

FORBIDDEN = ("0x", "opcode", "payload", ".bin", "disassembly", "pseudocode")
GENERATED = Path("docs/reverse/generated")

HANDOFF_FIELDS = (
    "story_id", "topic", "predecessor", "unmapped_function_count", "physical_cluster_count",
    "isolated_function_count", "isolated_cluster_count", "nonisolated_function_count",
    "nonisolated_physical_cluster_count", "nonisolated_category_cluster_assignment_count",
    "reconciliation_status", "reconciliation_none_cluster_count",
    "reconciliation_candidate_cluster_count", "reconciliation_ambiguous_cluster_count",
    "reconciliation_none_function_count", "reconciliation_candidate_function_count",
    "reconciliation_ambiguous_function_count", "identity_proof_count", "raw_evidence_versioned",
    "code_change_readiness", "next_ticket", "next_topic", "stop_condition",
)
POLICY_FIELDS = (
    "priority_rank", "lane", "scope", "function_count", "cluster_assignment_count", "confidence",
    "identity_proof_status", "recommended_next_proof", "code_change_readiness",
)


@dataclass(frozen=True)
class PolicyRow:
    priority_rank: int
    lane: str
    scope: str
    function_count: int
    cluster_assignment_count: int
    confidence: str
    identity_proof_status: str = "absent"
    recommended_next_proof: str = "aggregate proof acquisition only"
    code_change_readiness: str = "blocked"


@dataclass(frozen=True)
class Policy:
    unmapped_function_count: int
    physical_cluster_count: int
    rows: tuple[PolicyRow, ...]


def _read_rows(path: Path) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return tuple(reader.fieldnames or ()), list(reader)


def _validate_handoff(path: Path) -> None:
    fields, rows = _read_rows(path)
    if fields != HANDOFF_FIELDS or len(rows) != 1:
        raise ValueError("RE-696 handoff schema or row-count drift")
    expected = {
        "story_id": "RE-696", "topic": "ghidra-unmapped-reconciliation-audit", "predecessor": "RE-695",
        "unmapped_function_count": "723", "physical_cluster_count": "112", "isolated_function_count": "79",
        "isolated_cluster_count": "79", "nonisolated_function_count": "644",
        "nonisolated_physical_cluster_count": "33", "nonisolated_category_cluster_assignment_count": "72",
        "reconciliation_status": "no-metadata-detectable-reconciliation-discrepancy",
        "reconciliation_none_cluster_count": "112", "reconciliation_candidate_cluster_count": "0",
        "reconciliation_ambiguous_cluster_count": "0", "reconciliation_none_function_count": "723",
        "reconciliation_candidate_function_count": "0", "reconciliation_ambiguous_function_count": "0",
        "identity_proof_count": "0", "raw_evidence_versioned": "no", "code_change_readiness": "blocked",
        "next_ticket": "RE-697", "next_topic": "ghidra-unmapped-proof-acquisition-policy",
        "stop_condition": "reconciliation status is metadata-only; identity, semantics, ABI, behavior, equivalence, raw evidence, and code-change authorization remain absent",
    }
    for field, value in expected.items():
        if rows[0][field] != value:
            raise ValueError(f"RE-696 handoff drift in {field}")
    for value in rows[0].values():
        if any(fragment in value.lower() for fragment in FORBIDDEN):
            raise ValueError("RE-696 handoff forbidden content")


def build_policy(root: Path) -> Policy:
    _validate_handoff(root / GENERATED / "re696-ghidra-unmapped-reconciliation-audit-handoff.csv")
    rows = (
        PolicyRow(1, "isolated-boundary", "isolated", 12, 12, "medium", recommended_next_proof="source-backed boundary-family proof"),
        PolicyRow(2, "isolated-callee", "isolated", 58, 58, "medium", recommended_next_proof="source-backed boundary-family proof"),
        PolicyRow(3, "isolated-caller", "isolated", 6, 6, "medium", recommended_next_proof="source-backed boundary-family proof"),
        PolicyRow(4, "nonisolated-leaf", "nonisolated", 265, 33, "medium", recommended_next_proof="source-backed caller-family proof"),
        PolicyRow(5, "nonisolated-helper", "nonisolated", 54, 29, "medium", recommended_next_proof="bounded signature and state-contract proof"),
        PolicyRow(6, "nonisolated-large-block", "nonisolated", 292, 8, "low", recommended_next_proof="bounded control-flow and state-contract proof"),
        PolicyRow(7, "nonisolated-hub", "nonisolated", 33, 2, "low", recommended_next_proof="partitioned callsite and ABI/state-contract proof"),
        PolicyRow(8, "isolated-unconnected", "isolated", 3, 3, "medium", recommended_next_proof="identity evidence acquisition"),
    )
    if sum(row.function_count for row in rows) != 723:
        raise ValueError("policy function conservation drift")
    return Policy(723, 112, rows)


def _write(path: Path, fields: tuple[str, ...], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_artifacts(policy: Policy, root: Path) -> dict[str, Path]:
    generated = root / GENERATED
    policy_csv = generated / "re697-ghidra-unmapped-proof-acquisition-policy.csv"
    summary_csv = generated / "re697-ghidra-unmapped-proof-acquisition-policy-summary.csv"
    handoff_csv = generated / "re697-ghidra-unmapped-proof-acquisition-policy-handoff.csv"
    dashboard_html = root / "docs/reverse/tomb5-ghidra-unmapped-proof-acquisition-policy.html"
    story = root / "docs/stories/RE-697-ghidra-unmapped-proof-acquisition-policy.md"
    _write(policy_csv, POLICY_FIELDS, [row.__dict__ for row in policy.rows])
    summary = {"story_id": "RE-697", "topic": "ghidra-unmapped-proof-acquisition-policy", "predecessor": "RE-696", "unmapped_function_count": policy.unmapped_function_count, "physical_cluster_count": policy.physical_cluster_count, "aggregate_lane_count": len(policy.rows), "identity_proof_count": 0, "raw_evidence_versioned": "no", "code_change_readiness": "blocked", "next_ticket": "TBD", "next_topic": "none", "stop_condition": "the finite mapping backlog is complete; a new source-backed identity or behavior proof input is required before reopening a lane"}
    _write(summary_csv, tuple(summary), [summary])
    _write(handoff_csv, tuple(summary), [summary])
    dashboard_html.parent.mkdir(parents=True, exist_ok=True)
    dashboard_html.write_text("<!doctype html><html lang=\"fr\"><meta charset=\"utf-8\"><title>TOMB5 politique de preuve</title><h1>TOMB5 / politique agrégée d’acquisition de preuve</h1>" + f"<p>{policy.unmapped_function_count} fonctions et {len(policy.rows)} lanes finies ; aucun patch n’est autorisé.</p><p>Handoff terminal : nouvelle preuve requise.</p>\n", encoding="utf-8")
    story.parent.mkdir(parents=True, exist_ok=True)
    story.write_text("# RE-697 — politique d’acquisition de preuve des écarts Ghidra\n\n## Progress tracker\n\n- [x] Handoff RE-696 validé fail-closed.\n- [x] Les 723 fonctions sont réparties dans huit lanes agrégées et finies.\n- [x] Les compteurs de clusters non isolés sont explicitement des affectations de catégorie, non des clusters physiques distincts.\n- [x] Les identités, sémantiques, ABI, comportements, équivalences, code et marqueurs restent bloqués.\n- [x] Dashboard et handoff terminal synchronisés.\n\n## Décision\n\nLe backlog de cartographie est complet. Toute reprise exige une nouvelle entrée de preuve source-backed, sans sélection ni patch automatique.\n", encoding="utf-8")
    return {"policy_csv": policy_csv, "summary_csv": summary_csv, "handoff_csv": handoff_csv, "dashboard_html": dashboard_html, "story": story}


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    for name, path in write_artifacts(build_policy(root), root).items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
