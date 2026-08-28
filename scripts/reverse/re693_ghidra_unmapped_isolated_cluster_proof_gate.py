#!/usr/bin/env python3
"""Emit a metadata-only proof gate for isolated unmatched Ghidra clusters."""
from __future__ import annotations

import csv
import html
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

FORBIDDEN = ("0x", "opcode", "payload", ".bin", "disassembly", "pseudocode")
GENERATED = Path("docs/reverse/generated")


@dataclass(frozen=True)
class GateRow:
    priority_rank: int
    cluster_id: str
    member_count: int
    exposure_class: str
    reconciliation_status: str
    identity_proof_status: str
    recommended_next_proof: str
    code_change_readiness: str = "blocked"


@dataclass(frozen=True)
class Gate:
    isolated_cluster_count: int
    rows: tuple[GateRow, ...]


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _one_row(path: Path, expected: dict[str, str]) -> dict[str, str]:
    rows = _read_csv(path)
    if len(rows) != 1:
        raise ValueError(f"{path.name} must contain exactly one row")
    for field, value in expected.items():
        if rows[0].get(field) != value:
            raise ValueError(f"{path.name} drift in {field}")
    return rows[0]


def build_gate(root: Path) -> Gate:
    _one_row(root / GENERATED / "re690-global-ghidra-coverage-summary.csv", {
        "story_id": "RE-690", "ghidra_only_function_count": "723",
        "raw_evidence_versioned": "no", "code_change_readiness": "blocked",
    })
    _one_row(root / GENERATED / "re692-ghidra-unmapped-cluster-ledger-handoff.csv", {
        "story_id": "RE-692", "topic": "ghidra-unmapped-cluster-ledger", "predecessor": "RE-691",
        "unmapped_function_count": "723", "cluster_count": "112", "isolated_cluster_count": "79",
        "reconciliation_candidate_count": "0", "reconciliation_ambiguous_count": "0",
        "raw_evidence_versioned": "no", "code_change_readiness": "blocked",
        "next_ticket": "RE-693", "next_topic": "ghidra-unmapped-isolated-cluster-proof-gate",
    })
    rows = _read_csv(root / GENERATED / "re692-ghidra-unmapped-cluster-ledger.csv")
    expected_fields = {
        "priority_rank", "cluster_id", "primary_class", "member_count", "internal_edge_count",
        "mapped_inbound_count", "mapped_outbound_count", "reconciliation_status", "confidence",
        "recommended_next_proof", "code_change_readiness",
    }
    if not rows or set(rows[0]) != expected_fields:
        raise ValueError("RE-692 ledger schema drift")
    for row in rows:
        for field, value in row.items():
            if any(fragment in value.lower() for fragment in FORBIDDEN):
                raise ValueError(f"RE-692 ledger has forbidden content in {field}")
    isolated = [row for row in rows if row["primary_class"] == "isolated"]
    if len(rows) != 112 or len(isolated) != 79:
        raise ValueError("RE-692 isolated cluster inventory drift")
    gate_rows = []
    for row in isolated:
        inbound, outbound = int(row["mapped_inbound_count"]), int(row["mapped_outbound_count"])
        if row["member_count"] != "1" or row["internal_edge_count"] != "0":
            raise ValueError("RE-692 isolated row drift")
        if row["reconciliation_status"] != "none" or row["code_change_readiness"] != "blocked":
            raise ValueError("RE-692 isolated safety drift")
        exposure = "boundary-exposed" if inbound and outbound else "callee-exposed" if inbound else "caller-exposed" if outbound else "unconnected"
        proof = "source-backed boundary family map" if exposure != "unconnected" else "identity evidence acquisition"
        gate_rows.append(GateRow(int(row["priority_rank"]), row["cluster_id"], 1, exposure, "none", "absent", proof))
    gate_rows.sort(key=lambda row: row.priority_rank)
    return Gate(len(gate_rows), tuple(gate_rows))


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_artifacts(gate: Gate, root: Path) -> dict[str, Path]:
    generated = root / GENERATED
    gate_csv = generated / "re693-ghidra-unmapped-isolated-cluster-proof-gate.csv"
    summary_csv = generated / "re693-ghidra-unmapped-isolated-cluster-proof-gate-summary.csv"
    handoff_csv = generated / "re693-ghidra-unmapped-isolated-cluster-proof-gate-handoff.csv"
    dashboard_html = root / "docs/reverse/tomb5-ghidra-unmapped-isolated-cluster-proof-gate.html"
    story = root / "docs/stories/RE-693-ghidra-unmapped-isolated-cluster-proof-gate.md"
    records = [row.__dict__ for row in gate.rows]
    _write_csv(gate_csv, list(records[0]), records)
    classes = Counter(row.exposure_class for row in gate.rows)
    summary = {
        "story_id": "RE-693", "topic": "ghidra-unmapped-isolated-cluster-proof-gate", "predecessor": "RE-692",
        "isolated_cluster_count": gate.isolated_cluster_count, "identity_proof_count": 0,
        "reconciliation_candidate_count": 0, "raw_evidence_versioned": "no", "code_change_readiness": "blocked",
        "next_ticket": "RE-694", "next_topic": "ghidra-unmapped-boundary-exposure-backlog",
        "stop_condition": "isolated graph status is not identity, semantic, ABI, or equivalence proof",
    }
    _write_csv(summary_csv, list(summary), [summary])
    _write_csv(handoff_csv, list(summary), [summary])
    dashboard_html.parent.mkdir(parents=True, exist_ok=True)
    dashboard_html.write_text(
        "<!doctype html><html lang=\"fr\"><meta charset=\"utf-8\"><title>TOMB5 porte isolée</title>"
        "<h1>TOMB5 / porte de preuve des clusters isolés</h1>"
        f"<p>{gate.isolated_cluster_count} clusters isolés, preuve d’identité absente : {gate.isolated_cluster_count}.</p>"
        f"<p>Exposition agrégée : {html.escape(', '.join(f'{key} {classes[key]}' for key in sorted(classes)))}.</p>"
        "<p>Readiness code : bloquée. Prochain axe : backlog d’exposition de frontière.</p></html>\n", encoding="utf-8")
    story.parent.mkdir(parents=True, exist_ok=True)
    story.write_text(
        "# RE-693 — porte de preuve des clusters Ghidra isolés\n\n## Progress tracker\n\n"
        "- [x] Handoff RE-692 et baseline RE-690 validés fail-closed.\n"
        "- [x] Les 79 clusters isolés sont exhaustivement classés par exposition agrégée.\n"
        "- [x] Aucune identité, sémantique, ABI ou équivalence n’est inférée.\n"
        "- [x] Dashboard et handoff synchronisés ; code et marqueurs restent bloqués.\n\n## Décision\n\n"
        "RE-694 doit produire un backlog agrégé d’exposition de frontière, sans reprendre des tickets individuels.\n", encoding="utf-8")
    return {"gate_csv": gate_csv, "summary_csv": summary_csv, "handoff_csv": handoff_csv, "dashboard_html": dashboard_html, "story": story}


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    for name, path in write_artifacts(build_gate(root), root).items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
