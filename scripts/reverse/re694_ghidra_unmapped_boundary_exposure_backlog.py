#!/usr/bin/env python3
"""Emit the finite, metadata-only boundary-exposure backlog for isolated Ghidra clusters."""
from __future__ import annotations

import csv
import html
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

FORBIDDEN = ("0x", "opcode", "payload", ".bin", "disassembly", "pseudocode")
GENERATED = Path("docs/reverse/generated")
HANDOFF_FIELDS = (
    "story_id", "topic", "predecessor", "isolated_cluster_count", "identity_proof_count",
    "reconciliation_candidate_count", "raw_evidence_versioned", "code_change_readiness",
    "next_ticket", "next_topic", "stop_condition",
)
GATE_FIELDS = (
    "priority_rank", "cluster_id", "member_count", "exposure_class", "reconciliation_status",
    "identity_proof_status", "recommended_next_proof", "code_change_readiness",
)
EXPOSURE_ORDER = ("boundary-exposed", "callee-exposed", "caller-exposed", "unconnected")


@dataclass(frozen=True)
class BacklogRow:
    priority_rank: int
    exposure_class: str
    cluster_count: int
    confidence: str
    identity_proof_status: str
    recommended_next_proof: str
    code_change_readiness: str = "blocked"


@dataclass(frozen=True)
class Backlog:
    isolated_cluster_count: int
    rows: tuple[BacklogRow, ...]


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _require_one_handoff(path: Path) -> None:
    rows = _read_csv(path)
    if len(rows) != 1:
        raise ValueError("RE-693 handoff row-count drift")
    if tuple(rows[0]) != HANDOFF_FIELDS:
        raise ValueError("RE-693 handoff schema drift")
    expected = {
        "story_id": "RE-693",
        "topic": "ghidra-unmapped-isolated-cluster-proof-gate",
        "predecessor": "RE-692",
        "isolated_cluster_count": "79",
        "identity_proof_count": "0",
        "reconciliation_candidate_count": "0",
        "raw_evidence_versioned": "no",
        "code_change_readiness": "blocked",
        "next_ticket": "RE-694",
        "next_topic": "ghidra-unmapped-boundary-exposure-backlog",
        "stop_condition": "isolated graph status is not identity, semantic, ABI, or equivalence proof",
    }
    for field, value in expected.items():
        if rows[0][field] != value:
            raise ValueError(f"RE-693 handoff drift in {field}")


def build_backlog(root: Path) -> Backlog:
    generated = root / GENERATED
    _require_one_handoff(generated / "re693-ghidra-unmapped-isolated-cluster-proof-gate-handoff.csv")
    rows = _read_csv(generated / "re693-ghidra-unmapped-isolated-cluster-proof-gate.csv")
    if not rows or tuple(rows[0]) != GATE_FIELDS:
        raise ValueError("RE-693 gate schema drift")
    if len(rows) != 79:
        raise ValueError("RE-693 gate inventory drift")
    for row in rows:
        for field, value in row.items():
            if any(fragment in value.lower() for fragment in FORBIDDEN):
                raise ValueError(f"RE-693 gate forbidden content in {field}")
        if row["member_count"] != "1":
            raise ValueError("RE-693 gate drift in member_count")
        for field, value in {
            "reconciliation_status": "none",
            "identity_proof_status": "absent",
            "code_change_readiness": "blocked",
        }.items():
            if row[field] != value:
                raise ValueError(f"RE-693 gate drift in {field}")
        if row["exposure_class"] not in EXPOSURE_ORDER:
            raise ValueError("RE-693 gate drift in exposure_class")
    counts = Counter(row["exposure_class"] for row in rows)
    return Backlog(
        isolated_cluster_count=len(rows),
        rows=tuple(
            BacklogRow(
                priority_rank=index,
                exposure_class=exposure,
                cluster_count=counts[exposure],
                confidence="medium",
                identity_proof_status="absent",
                recommended_next_proof=(
                    "source-backed boundary family map" if exposure != "unconnected"
                    else "identity evidence acquisition"
                ),
            )
            for index, exposure in enumerate(EXPOSURE_ORDER, start=1)
        ),
    )


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_artifacts(backlog: Backlog, root: Path) -> dict[str, Path]:
    generated = root / GENERATED
    backlog_csv = generated / "re694-ghidra-unmapped-boundary-exposure-backlog.csv"
    summary_csv = generated / "re694-ghidra-unmapped-boundary-exposure-backlog-summary.csv"
    handoff_csv = generated / "re694-ghidra-unmapped-boundary-exposure-backlog-handoff.csv"
    dashboard_html = root / "docs/reverse/tomb5-ghidra-unmapped-boundary-exposure-backlog.html"
    story = root / "docs/stories/RE-694-ghidra-unmapped-boundary-exposure-backlog.md"
    records = [row.__dict__ for row in backlog.rows]
    _write_csv(backlog_csv, list(records[0]), records)
    summary = {
        "story_id": "RE-694", "topic": "ghidra-unmapped-boundary-exposure-backlog", "predecessor": "RE-693",
        "isolated_cluster_count": backlog.isolated_cluster_count, "backlog_lane_count": len(backlog.rows),
        "identity_proof_count": 0, "raw_evidence_versioned": "no", "code_change_readiness": "blocked",
        "next_ticket": "RE-695", "next_topic": "ghidra-unmapped-non-isolated-cluster-proof-gate",
        "stop_condition": "boundary exposure prioritizes proof acquisition only; identity, semantics, ABI, and equivalence remain unproven",
    }
    _write_csv(summary_csv, list(summary), [summary])
    _write_csv(handoff_csv, list(summary), [summary])
    dashboard_html.parent.mkdir(parents=True, exist_ok=True)
    lanes = ", ".join(f"{row.exposure_class} {row.cluster_count}" for row in backlog.rows)
    dashboard_html.write_text(
        "<!doctype html><html lang=\"fr\"><meta charset=\"utf-8\"><title>TOMB5 backlog frontière</title>"
        "<h1>TOMB5 / backlog d’exposition de frontière</h1>"
        f"<p>{backlog.isolated_cluster_count} clusters isolés répartis dans {len(backlog.rows)} voies : {html.escape(lanes)}.</p>"
        "<p>Les voies ordonnent uniquement l’acquisition de preuve. Readiness code : bloquée.</p>\n",
        encoding="utf-8",
    )
    story.parent.mkdir(parents=True, exist_ok=True)
    story.write_text(
        "# RE-694 — backlog d’exposition de frontière des clusters Ghidra isolés\n\n## Progress tracker\n\n"
        "- [x] Handoff RE-693 validé champ par champ et inventaire isolé relu fail-closed.\n"
        "- [x] Les 79 clusters isolés sont regroupés en quatre voies d’exposition déterministes.\n"
        "- [x] Le backlog reste agrégé : aucun rang fonctionnel individuel n’est créé.\n"
        "- [x] Identité, sémantique, ABI, équivalence, code et marqueurs restent bloqués.\n"
        "- [x] Dashboard et handoff synchronisés.\n\n## Décision\n\n"
        "RE-695 doit poser la porte de preuve des clusters non isolés restants, toujours sans patch source.\n",
        encoding="utf-8",
    )
    return {"backlog_csv": backlog_csv, "summary_csv": summary_csv, "handoff_csv": handoff_csv, "dashboard_html": dashboard_html, "story": story}


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    for name, path in write_artifacts(build_backlog(root), root).items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
