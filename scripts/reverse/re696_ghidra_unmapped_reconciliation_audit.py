#!/usr/bin/env python3
"""Emit a fail-closed, aggregate reconciliation audit for unmatched Ghidra coverage."""
from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path

FORBIDDEN = ("0x", "opcode", "payload", ".bin", "disassembly", "pseudocode")
GENERATED = Path("docs/reverse/generated")
BASELINE_FIELDS = (
    "story_id", "topic", "ghidra_function_count", "mapped_ghidra_function_count",
    "ghidra_only_function_count", "repo_function_count", "mapped_repo_row_count",
    "repo_only_row_count", "coverage_status", "raw_evidence_versioned",
    "code_change_readiness", "next_topic", "stop_condition",
)
LEDGER_FIELDS = (
    "priority_rank", "cluster_id", "primary_class", "member_count", "internal_edge_count",
    "mapped_inbound_count", "mapped_outbound_count", "reconciliation_status", "confidence",
    "recommended_next_proof", "code_change_readiness",
)
ISOLATED_FIELDS = (
    "priority_rank", "cluster_id", "member_count", "exposure_class", "reconciliation_status",
    "identity_proof_status", "recommended_next_proof", "code_change_readiness",
)
NONISOLATED_FIELDS = (
    "priority_rank", "category", "function_count", "cluster_count", "confidence",
    "identity_proof_status", "recommended_next_proof", "code_change_readiness",
)
HANDOFF_FIELDS = (
    "story_id", "topic", "predecessor", "unmapped_function_count",
    "aggregate_category_cluster_count", "identity_proof_count", "raw_evidence_versioned",
    "code_change_readiness", "next_ticket", "next_topic", "stop_condition",
)
AUDIT_FIELDS = (
    "story_id", "topic", "predecessor", "unmapped_function_count", "physical_cluster_count",
    "isolated_function_count", "isolated_cluster_count", "nonisolated_function_count",
    "nonisolated_physical_cluster_count", "nonisolated_category_cluster_assignment_count",
    "reconciliation_status", "reconciliation_none_cluster_count",
    "reconciliation_candidate_cluster_count", "reconciliation_ambiguous_cluster_count",
    "reconciliation_none_function_count", "reconciliation_candidate_function_count",
    "reconciliation_ambiguous_function_count", "identity_proof_count", "raw_evidence_versioned",
    "code_change_readiness", "next_ticket", "next_topic", "stop_condition",
)
INPUT_DIGESTS = {
    "re690-global-ghidra-coverage-summary.csv": "ed082af4b532be35957809831f4d439a121c397831492a369b858698413f96fb",
    "re692-ghidra-unmapped-cluster-ledger.csv": "15e09525d3c0886bed39bd96a9448bda31761ad44be6a5f11964b884b78aa5f0",
    "re693-ghidra-unmapped-isolated-cluster-proof-gate.csv": "9e76324c139906e29a8dbbf3b46a9f18e6191d07446358ac0dc18fb2639d9b6c",
    "re695-ghidra-unmapped-nonisolated-cluster-proof-gate.csv": "efb8037a9d6804e605ee32b06e5c35c052c8a299b37b690a850c8a2cdae5a4fe",
}
EXPECTED_FIRST_ROWS = {
    "re690-global-ghidra-coverage-summary.csv": {"story_id": "RE-690", "topic": "global-ghidra-coverage-baseline", "ghidra_function_count": "1440", "mapped_ghidra_function_count": "717", "ghidra_only_function_count": "723", "repo_function_count": "1250", "mapped_repo_row_count": "866", "repo_only_row_count": "384", "coverage_status": "inventory-complete-not-semantic-complete", "raw_evidence_versioned": "no", "code_change_readiness": "blocked", "next_topic": "triage-ghidra-only-function-clusters", "stop_condition": "global inventory is a prioritization baseline, not behavior or equivalence proof"},
    "re692-ghidra-unmapped-cluster-ledger.csv": {"priority_rank": "1", "cluster_id": "cluster-001", "primary_class": "isolated", "member_count": "1", "internal_edge_count": "0", "mapped_inbound_count": "0", "mapped_outbound_count": "1", "reconciliation_status": "none", "confidence": "medium", "recommended_next_proof": "metadata identity and caller/callee absence check", "code_change_readiness": "blocked"},
    "re693-ghidra-unmapped-isolated-cluster-proof-gate.csv": {"priority_rank": "1", "cluster_id": "cluster-001", "member_count": "1", "exposure_class": "caller-exposed", "reconciliation_status": "none", "identity_proof_status": "absent", "recommended_next_proof": "source-backed boundary family map", "code_change_readiness": "blocked"},
    "re695-ghidra-unmapped-nonisolated-cluster-proof-gate.csv": {"priority_rank": "1", "category": "leaf", "function_count": "265", "cluster_count": "33", "confidence": "medium", "identity_proof_status": "absent", "recommended_next_proof": "source-backed caller-family map", "code_change_readiness": "blocked"},
}


@dataclass(frozen=True)
class Audit:
    unmapped_function_count: int
    physical_cluster_count: int
    isolated_function_count: int
    isolated_cluster_count: int
    nonisolated_function_count: int
    nonisolated_physical_cluster_count: int
    nonisolated_category_cluster_assignment_count: int
    reconciliation_status: str
    reconciliation_none_cluster_count: int
    reconciliation_candidate_cluster_count: int
    reconciliation_ambiguous_cluster_count: int
    reconciliation_none_function_count: int
    reconciliation_candidate_function_count: int
    reconciliation_ambiguous_function_count: int
    identity_proof_count: int = 0
    raw_evidence_versioned: str = "no"
    code_change_readiness: str = "blocked"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _validate_values(rows: list[dict[str, str]], label: str) -> None:
    for row in rows:
        for field, value in row.items():
            if any(fragment in value.lower() for fragment in FORBIDDEN):
                raise ValueError(f"{label} forbidden content in {field}")


def _one_row(path: Path, fields: tuple[str, ...], expected: dict[str, str]) -> dict[str, str]:
    rows = _rows(path)
    if len(rows) != 1:
        raise ValueError(f"{path.name} row-count drift")
    if tuple(rows[0]) != fields:
        raise ValueError(f"{path.name} schema drift")
    _validate_values(rows, path.name)
    for field, value in expected.items():
        if rows[0][field] != value:
            raise ValueError(f"{path.name} drift in {field}")
    return rows[0]


def _integer(row: dict[str, str], field: str, label: str) -> int:
    try:
        value = int(row[field])
    except (KeyError, ValueError) as error:
        raise ValueError(f"{label} drift in {field}") from error
    if value < 0:
        raise ValueError(f"{label} drift in {field}")
    return value


def _validate_first_row(path: Path) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        row = next(reader, None)
    if row is None:
        raise ValueError(f"{path.name} row-count drift")
    for field, expected in EXPECTED_FIRST_ROWS[path.name].items():
        if row.get(field) != expected:
            raise ValueError(f"{path.name} drift in {field}")


def _validate_snapshot(path: Path) -> None:
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != INPUT_DIGESTS[path.name]:
        raise ValueError(f"{path.name} drift in snapshot")


def build_audit(root: Path) -> Audit:
    generated = root / GENERATED
    for name in INPUT_DIGESTS:
        path = generated / name
        _validate_first_row(path)
        _validate_snapshot(path)
    _one_row(generated / "re690-global-ghidra-coverage-summary.csv", BASELINE_FIELDS, {
        "story_id": "RE-690", "topic": "global-ghidra-coverage-baseline",
        "ghidra_only_function_count": "723", "raw_evidence_versioned": "no",
        "code_change_readiness": "blocked",
    })
    _one_row(generated / "re695-ghidra-unmapped-nonisolated-cluster-proof-gate-handoff.csv", HANDOFF_FIELDS, {
        "story_id": "RE-695", "topic": "ghidra-unmapped-nonisolated-cluster-proof-gate",
        "predecessor": "RE-694", "unmapped_function_count": "644",
        "aggregate_category_cluster_count": "72", "identity_proof_count": "0",
        "raw_evidence_versioned": "no", "code_change_readiness": "blocked",
        "next_ticket": "RE-696", "next_topic": "ghidra-unmapped-reconciliation-audit",
        "stop_condition": "category and graph metadata do not prove identity, semantics, ABI, or equivalence",
    })

    ledger = _rows(generated / "re692-ghidra-unmapped-cluster-ledger.csv")
    if len(ledger) != 112 or not ledger or tuple(ledger[0]) != LEDGER_FIELDS:
        raise ValueError("RE-692 ledger schema or row-count drift")
    _validate_values(ledger, "RE-692 ledger")
    ranks = [_integer(row, "priority_rank", "RE-692 ledger") for row in ledger]
    if sorted(ranks) != list(range(1, 113)) or len({row["cluster_id"] for row in ledger}) != 112:
        raise ValueError("RE-692 ledger identity drift")
    if any(row["code_change_readiness"] != "blocked" for row in ledger):
        raise ValueError("RE-692 ledger drift in code_change_readiness")
    allowed_statuses = {"none", "candidate", "ambiguous"}
    if any(row["reconciliation_status"] not in allowed_statuses for row in ledger):
        raise ValueError("RE-692 ledger drift in reconciliation_status")
    members = {id(row): _integer(row, "member_count", "RE-692 ledger") for row in ledger}
    if any(value < 1 for value in members.values()) or sum(members.values()) != 723:
        raise ValueError("RE-692 ledger member-count drift")
    isolated = [row for row in ledger if row["primary_class"] == "isolated"]
    if len(isolated) != 79 or any(members[id(row)] != 1 or row["internal_edge_count"] != "0" for row in isolated):
        raise ValueError("RE-692 ledger isolated partition drift")
    nonisolated = [row for row in ledger if row["primary_class"] != "isolated"]
    if len(nonisolated) != 33 or sum(members[id(row)] for row in nonisolated) != 644:
        raise ValueError("RE-692 ledger nonisolated partition drift")

    isolated_gate = _rows(generated / "re693-ghidra-unmapped-isolated-cluster-proof-gate.csv")
    if len(isolated_gate) != 79 or not isolated_gate or tuple(isolated_gate[0]) != ISOLATED_FIELDS:
        raise ValueError("RE-693 gate schema or row-count drift")
    _validate_values(isolated_gate, "RE-693 gate")
    if any(row["member_count"] != "1" or row["reconciliation_status"] != "none" or row["identity_proof_status"] != "absent" or row["code_change_readiness"] != "blocked" for row in isolated_gate):
        raise ValueError("RE-693 gate safety drift")

    nonisolated_gate = _rows(generated / "re695-ghidra-unmapped-nonisolated-cluster-proof-gate.csv")
    if len(nonisolated_gate) != 4 or not nonisolated_gate or tuple(nonisolated_gate[0]) != NONISOLATED_FIELDS:
        raise ValueError("RE-695 gate schema or row-count drift")
    _validate_values(nonisolated_gate, "RE-695 gate")
    expected_categories = {"leaf": (265, 33), "helper": (54, 29), "large-block": (292, 8), "hub": (33, 2)}
    by_category = {row["category"]: row for row in nonisolated_gate}
    if set(by_category) != set(expected_categories):
        raise ValueError("RE-695 gate category drift")
    for category, (functions, clusters) in expected_categories.items():
        row = by_category[category]
        if (_integer(row, "function_count", "RE-695 gate"), _integer(row, "cluster_count", "RE-695 gate")) != (functions, clusters):
            raise ValueError(f"RE-695 gate drift in {category}")
        if row["identity_proof_status"] != "absent" or row["code_change_readiness"] != "blocked":
            raise ValueError(f"RE-695 gate safety drift in {category}")

    status_cluster_counts = {status: sum(row["reconciliation_status"] == status for row in ledger) for status in allowed_statuses}
    status_function_counts = {status: sum(members[id(row)] for row in ledger if row["reconciliation_status"] == status) for status in allowed_statuses}
    if sum(status_cluster_counts.values()) != 112 or sum(status_function_counts.values()) != 723:
        raise ValueError("RE-692 ledger reconciliation conservation drift")
    if status_cluster_counts["candidate"] or status_cluster_counts["ambiguous"]:
        reconciliation_status = "metadata-reconciliation-candidate-present" if status_cluster_counts["candidate"] else "metadata-reconciliation-ambiguous"
    else:
        reconciliation_status = "no-metadata-detectable-reconciliation-discrepancy"
    return Audit(723, 112, 79, 79, 644, 33, 72, reconciliation_status,
                 status_cluster_counts["none"], status_cluster_counts["candidate"], status_cluster_counts["ambiguous"],
                 status_function_counts["none"], status_function_counts["candidate"], status_function_counts["ambiguous"])


def _write(path: Path, fields: tuple[str, ...], row: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)


def write_artifacts(audit: Audit, root: Path) -> dict[str, Path]:
    generated = root / GENERATED
    summary_csv = generated / "re696-ghidra-unmapped-reconciliation-audit-summary.csv"
    handoff_csv = generated / "re696-ghidra-unmapped-reconciliation-audit-handoff.csv"
    dashboard_html = root / "docs/reverse/tomb5-ghidra-unmapped-reconciliation-audit.html"
    story = root / "docs/stories/RE-696-ghidra-unmapped-reconciliation-audit.md"
    row = {"story_id": "RE-696", "topic": "ghidra-unmapped-reconciliation-audit", "predecessor": "RE-695", **audit.__dict__, "next_ticket": "RE-697", "next_topic": "ghidra-unmapped-proof-acquisition-policy", "stop_condition": "reconciliation status is metadata-only; identity, semantics, ABI, behavior, equivalence, raw evidence, and code-change authorization remain absent"}
    _write(summary_csv, AUDIT_FIELDS, row)
    _write(handoff_csv, AUDIT_FIELDS, row)
    dashboard_html.parent.mkdir(parents=True, exist_ok=True)
    dashboard_html.write_text("<!doctype html><html lang=\"fr\"><meta charset=\"utf-8\"><title>TOMB5 audit réconciliation</title><h1>TOMB5 / audit de réconciliation des écarts Ghidra</h1>" + f"<p>{audit.unmapped_function_count} fonctions, {audit.physical_cluster_count} clusters physiques, signal : {audit.reconciliation_status}.</p><p>Identité et code : bloqués.</p>\n", encoding="utf-8")
    story.parent.mkdir(parents=True, exist_ok=True)
    story.write_text("# RE-696 — audit de réconciliation des écarts Ghidra\n\n## Progress tracker\n\n- [x] Handoff RE-695 et baseline RE-690 validés champ par champ fail-closed.\n- [x] Les 723 fonctions et 112 clusters physiques sont conservés par statut de réconciliation agrégé.\n- [x] Aucun signal metadata-only de candidat ou ambiguïté n’est détecté ; ce résultat ne prouve pas une correspondance.\n- [x] Aucun nom, graphe détaillé, adresse, byte ou preuve propriétaire n’est versionné.\n- [x] Dashboard et handoff synchronisés ; code et marqueurs restent bloqués.\n\n## Décision\n\nRE-697 doit définir une politique agrégée d’acquisition de preuve, sans sélection individuelle ni autorisation de patch.\n", encoding="utf-8")
    return {"summary_csv": summary_csv, "handoff_csv": handoff_csv, "dashboard_html": dashboard_html, "story": story}


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    for name, path in write_artifacts(build_audit(root), root).items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
