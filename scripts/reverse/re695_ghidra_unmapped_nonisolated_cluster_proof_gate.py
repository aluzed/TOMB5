#!/usr/bin/env python3
"""Emit a blocked, aggregate proof gate for non-isolated unmatched Ghidra categories."""
from __future__ import annotations

import csv
import html
from dataclasses import dataclass
from pathlib import Path

FORBIDDEN = ("0x", "opcode", "payload", ".bin", "disassembly", "pseudocode")
GENERATED = Path("docs/reverse/generated")
HANDOFF_FIELDS = ("story_id", "topic", "predecessor", "isolated_cluster_count", "backlog_lane_count", "identity_proof_count", "raw_evidence_versioned", "code_change_readiness", "next_ticket", "next_topic", "stop_condition")
MATRIX_FIELDS = ("category", "function_count", "cluster_count", "confidence", "recommended_next_proof")
ORDER = ("leaf", "helper", "large-block", "hub")
EXPECTED = {
    "leaf": (265, 33, "medium", "source-backed caller-family map"),
    "helper": (54, 29, "medium", "bounded helper signature and state-contract proof"),
    "large-block": (292, 8, "low", "split into bounded control-flow and state-contract clusters"),
    "hub": (33, 2, "low", "partitioned callsite and ABI/state-contract proof"),
}

@dataclass(frozen=True)
class GateRow:
    priority_rank: int
    category: str
    function_count: int
    cluster_count: int
    confidence: str
    identity_proof_status: str
    recommended_next_proof: str
    code_change_readiness: str = "blocked"

@dataclass(frozen=True)
class Gate:
    unmapped_function_count: int
    cluster_count: int
    rows: tuple[GateRow, ...]

def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def _validate_handoff(path: Path) -> None:
    rows = _rows(path)
    if len(rows) != 1:
        raise ValueError("RE-694 handoff row-count drift")
    if tuple(rows[0]) != HANDOFF_FIELDS:
        raise ValueError("RE-694 handoff schema drift")
    expected = {"story_id": "RE-694", "topic": "ghidra-unmapped-boundary-exposure-backlog", "predecessor": "RE-693", "isolated_cluster_count": "79", "backlog_lane_count": "4", "identity_proof_count": "0", "raw_evidence_versioned": "no", "code_change_readiness": "blocked", "next_ticket": "RE-695", "next_topic": "ghidra-unmapped-non-isolated-cluster-proof-gate", "stop_condition": "boundary exposure prioritizes proof acquisition only; identity, semantics, ABI, and equivalence remain unproven"}
    for field, value in expected.items():
        if rows[0][field] != value:
            raise ValueError(f"RE-694 handoff drift in {field}")

def build_gate(root: Path) -> Gate:
    generated = root / GENERATED
    _validate_handoff(generated / "re694-ghidra-unmapped-boundary-exposure-backlog-handoff.csv")
    matrix = _rows(generated / "re691-ghidra-unmapped-completion-matrix.csv")
    if len(matrix) != 5 or not matrix or tuple(matrix[0]) != MATRIX_FIELDS:
        raise ValueError("RE-691 matrix schema drift")
    by_category = {row["category"]: row for row in matrix}
    if set(by_category) != set(ORDER) | {"isolated"}:
        raise ValueError("RE-691 matrix category drift")
    rows = []
    for rank, category in enumerate(ORDER, start=1):
        row = by_category[category]
        if any(fragment in value.lower() for value in row.values() for fragment in FORBIDDEN):
            raise ValueError(f"RE-691 matrix forbidden content in {category}")
        functions, clusters, confidence, proof = EXPECTED[category]
        if (int(row["function_count"]), int(row["cluster_count"]), row["confidence"], row["recommended_next_proof"]) != (functions, clusters, confidence, proof):
            raise ValueError(f"RE-691 matrix drift in {category}")
        rows.append(GateRow(rank, category, functions, clusters, confidence, "absent", proof))
    return Gate(sum(row.function_count for row in rows), sum(row.cluster_count for row in rows), tuple(rows))

def _write(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)

def write_artifacts(gate: Gate, root: Path) -> dict[str, Path]:
    generated = root / GENERATED
    gate_csv = generated / "re695-ghidra-unmapped-nonisolated-cluster-proof-gate.csv"
    summary_csv = generated / "re695-ghidra-unmapped-nonisolated-cluster-proof-gate-summary.csv"
    handoff_csv = generated / "re695-ghidra-unmapped-nonisolated-cluster-proof-gate-handoff.csv"
    dashboard_html = root / "docs/reverse/tomb5-ghidra-unmapped-nonisolated-cluster-proof-gate.html"
    story = root / "docs/stories/RE-695-ghidra-unmapped-nonisolated-cluster-proof-gate.md"
    records = [row.__dict__ for row in gate.rows]
    _write(gate_csv, list(records[0]), records)
    summary = {"story_id": "RE-695", "topic": "ghidra-unmapped-nonisolated-cluster-proof-gate", "predecessor": "RE-694", "unmapped_function_count": gate.unmapped_function_count, "aggregate_category_cluster_count": gate.cluster_count, "identity_proof_count": 0, "raw_evidence_versioned": "no", "code_change_readiness": "blocked", "next_ticket": "RE-696", "next_topic": "ghidra-unmapped-reconciliation-audit", "stop_condition": "category and graph metadata do not prove identity, semantics, ABI, or equivalence"}
    _write(summary_csv, list(summary), [summary]); _write(handoff_csv, list(summary), [summary])
    dashboard_html.parent.mkdir(parents=True, exist_ok=True)
    story.parent.mkdir(parents=True, exist_ok=True)
    dashboard_html.write_text("<!doctype html><html lang=\"fr\"><meta charset=\"utf-8\"><title>TOMB5 porte non isolée</title><h1>TOMB5 / porte de preuve des catégories non isolées</h1>" + f"<p>{gate.unmapped_function_count} fonctions dans {gate.cluster_count} affectations de catégorie agrégées.</p><p>Identité et readiness code : bloquées.</p>\n", encoding="utf-8")
    story.write_text("# RE-695 — porte de preuve des catégories Ghidra non isolées\n\n## Progress tracker\n\n- [x] Handoff RE-694 validé champ par champ fail-closed.\n- [x] Les 644 fonctions non isolées sont réparties en quatre catégories agrégées.\n- [x] Aucun nom de fonction, détail de graphe, identité ou comportement n’est versionné.\n- [x] Code et marqueurs restent bloqués ; dashboard et handoff synchronisés.\n\n## Décision\n\nRE-696 doit auditer la réconciliation des écarts sans lever les blocages de preuve.\n", encoding="utf-8")
    return {"gate_csv": gate_csv, "summary_csv": summary_csv, "handoff_csv": handoff_csv, "dashboard_html": dashboard_html, "story": story}

def main() -> int:
    root = Path(__file__).resolve().parents[2]
    for name, path in write_artifacts(build_gate(root), root).items(): print(f"{name}: {path}")
    return 0
if __name__ == "__main__": raise SystemExit(main())
