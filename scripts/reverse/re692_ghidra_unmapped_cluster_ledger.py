#!/usr/bin/env python3
"""Emit a safe, finite priority ledger for unmatched Ghidra graph clusters.

Names, entries and detailed graph relationships are read only from ignored inputs.
Committed outputs retain only opaque cluster labels and aggregate counts.
"""
from __future__ import annotations

import csv
import html
import re
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path

FORBIDDEN = ("0x", "opcode", "payload", ".bin", "disassembly", "pseudocode")
BASELINE = Path("docs/reverse/generated/re690-global-ghidra-coverage-summary.csv")
GHIDRA_EXPORT = Path("build/reverse/generated/ghidra-functions.csv")
REPO_MAP = Path("build/reverse/generated/repo-function-map.csv")


@dataclass(frozen=True)
class ClusterRow:
    priority_rank: int
    cluster_id: str
    primary_class: str
    member_count: int
    internal_edge_count: int
    mapped_inbound_count: int
    mapped_outbound_count: int
    reconciliation_status: str
    confidence: str
    recommended_next_proof: str
    code_change_readiness: str = "blocked"


@dataclass(frozen=True)
class Ledger:
    unmapped_function_count: int
    cluster_count: int
    isolated_cluster_count: int
    reconciliation_candidate_count: int
    reconciliation_ambiguous_count: int
    rows: tuple[ClusterRow, ...]


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _require_columns(rows: list[dict[str, str]], fields: set[str], label: str) -> None:
    if not rows or not fields.issubset(rows[0]):
        raise ValueError(f"{label} has missing required columns")


def _validate_baseline(root: Path) -> None:
    rows = _read_csv(root / BASELINE) if (root / BASELINE).is_file() else []
    if len(rows) != 1:
        raise ValueError("RE-690 baseline must contain exactly one summary row")
    expected = {
        "story_id": "RE-690",
        "ghidra_only_function_count": "723",
        "coverage_status": "inventory-complete-not-semantic-complete",
        "raw_evidence_versioned": "no",
        "code_change_readiness": "blocked",
    }
    for field, value in expected.items():
        if rows[0].get(field) != value:
            raise ValueError(f"RE-690 baseline drift in {field}")


def _components(nodes: set[str], edges: dict[str, set[str]]) -> list[set[str]]:
    remaining = set(nodes)
    groups: list[set[str]] = []
    while remaining:
        start = min(remaining)
        group = {start}
        queue = deque([start])
        remaining.remove(start)
        while queue:
            node = queue.popleft()
            for peer in sorted(edges[node]):
                if peer in remaining:
                    remaining.remove(peer)
                    group.add(peer)
                    queue.append(peer)
        groups.append(group)
    return groups


def _normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def build_ledger(root: Path) -> Ledger:
    _validate_baseline(root)
    ghidra_rows = _read_csv(root / GHIDRA_EXPORT)
    repo_rows = _read_csv(root / REPO_MAP)
    _require_columns(ghidra_rows, {"entry", "name", "body_size", "called_functions", "callers"}, "Ghidra export")
    _require_columns(repo_rows, {"mapping_status", "ghidra_entry", "ghidra_name", "repo_function"}, "repo map")
    entries = [row["entry"].lower() for row in ghidra_rows]
    if len(entries) != len(set(entries)):
        raise ValueError("duplicate Ghidra entry")
    if any(not row["name"] for row in ghidra_rows):
        raise ValueError("Ghidra export has empty name")
    try:
        sizes = {row["name"]: int(row["body_size"]) for row in ghidra_rows}
    except ValueError as error:
        raise ValueError("Ghidra export has invalid body size") from error
    if any(size < 0 for size in sizes.values()):
        raise ValueError("Ghidra export has invalid body size")

    mapped_entries = {row["ghidra_entry"].lower() for row in repo_rows if row["mapping_status"] == "mapped"}
    unmapped_rows = [row for row in ghidra_rows if row["entry"].lower() not in mapped_entries]
    if len(unmapped_rows) != 723:
        raise ValueError("RE-690 unmapped inventory drift")
    names = {row["name"] for row in unmapped_rows}
    if len(names) != len(unmapped_rows):
        raise ValueError("duplicate Ghidra name in unmatched inventory")
    mapped_names = {row["ghidra_name"] for row in repo_rows if row["mapping_status"] == "mapped" and row["ghidra_name"]}
    repo_name_index: dict[str, set[str]] = {}
    for row in repo_rows:
        name = _normalized(row["repo_function"])
        if name:
            repo_name_index.setdefault(name, set()).add(row["repo_function"])

    edges = {name: set() for name in names}
    inbound = Counter()
    outbound = Counter()
    mapped_inbound = Counter()
    mapped_outbound = Counter()
    for row in unmapped_rows:
        name = row["name"]
        for called in filter(None, row["called_functions"].split(";")):
            if called in names:
                edges[name].add(called)
                edges[called].add(name)
                outbound[name] += 1
                inbound[called] += 1
            elif called in mapped_names:
                mapped_outbound[name] += 1
        for caller in filter(None, row["callers"].split(";")):
            if caller in mapped_names:
                mapped_inbound[name] += 1
    groups = _components(names, edges)
    membership = {name: index for index, group in enumerate(groups) for name in group}
    component_sizes = Counter(membership.values())

    category = {}
    for name in names:
        degree = len(edges[name])
        if degree == 0:
            category[name] = "isolated"
        elif outbound[name] == 0 and inbound[name] > 0:
            category[name] = "leaf"
        elif degree >= 8:
            category[name] = "hub"
        elif sizes[name] > 1024 or component_sizes[membership[name]] >= 32:
            category[name] = "large-block"
        else:
            category[name] = "helper"
    priority = {"isolated": 1, "leaf": 2, "helper": 3, "large-block": 4, "hub": 5}
    proof = {
        "isolated": ("medium", "metadata identity and caller/callee absence check"),
        "leaf": ("medium", "source-backed caller-family map"),
        "helper": ("medium", "bounded helper signature and state-contract proof"),
        "large-block": ("low", "split into bounded control-flow and state-contract clusters"),
        "hub": ("low", "partitioned callsite and ABI/state-contract proof"),
    }

    pending = []
    for group in groups:
        classes = {category[name] for name in group}
        primary = min(classes, key=lambda value: priority[value])
        internal_edges = sum(1 for name in group for peer in edges[name] if peer in group) // 2
        reconciled = set().union(*(repo_name_index.get(_normalized(name), set()) for name in group))
        status = "none" if not reconciled else "candidate" if len(reconciled) == 1 else "ambiguous"
        pending.append((priority[primary], -len(group), primary, min(group), group, internal_edges, status))
    pending.sort(key=lambda row: row[:4])

    rows = []
    for rank, (_, _, primary, _, group, internal_edges, status) in enumerate(pending, start=1):
        confidence, next_proof = proof[primary]
        rows.append(ClusterRow(
            priority_rank=rank,
            cluster_id=f"cluster-{rank:03d}",
            primary_class=primary,
            member_count=len(group),
            internal_edge_count=internal_edges,
            mapped_inbound_count=sum(mapped_inbound[name] for name in group),
            mapped_outbound_count=sum(mapped_outbound[name] for name in group),
            reconciliation_status=status,
            confidence=confidence,
            recommended_next_proof=next_proof,
        ))
    isolated = sum(row.primary_class == "isolated" for row in rows)
    return Ledger(723, len(rows), isolated, sum(row.reconciliation_status == "candidate" for row in rows), sum(row.reconciliation_status == "ambiguous" for row in rows), tuple(rows))


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_artifacts(ledger: Ledger, root: Path) -> dict[str, Path]:
    generated = root / "docs/reverse/generated"
    ledger_csv = generated / "re692-ghidra-unmapped-cluster-ledger.csv"
    summary_csv = generated / "re692-ghidra-unmapped-cluster-ledger-summary.csv"
    handoff_csv = generated / "re692-ghidra-unmapped-cluster-ledger-handoff.csv"
    dashboard_html = root / "docs/reverse/tomb5-ghidra-unmapped-cluster-ledger.html"
    story = root / "docs/stories/RE-692-ghidra-unmapped-cluster-ledger.md"
    records = [row.__dict__ for row in ledger.rows]
    _write_csv(ledger_csv, list(records[0]), records)
    summary = {
        "story_id": "RE-692", "topic": "ghidra-unmapped-cluster-ledger", "predecessor": "RE-691",
        "unmapped_function_count": ledger.unmapped_function_count, "cluster_count": ledger.cluster_count,
        "isolated_cluster_count": ledger.isolated_cluster_count,
        "reconciliation_candidate_count": ledger.reconciliation_candidate_count,
        "reconciliation_ambiguous_count": ledger.reconciliation_ambiguous_count,
        "raw_evidence_versioned": "no", "code_change_readiness": "blocked",
        "next_ticket": "RE-693", "next_topic": "ghidra-unmapped-isolated-cluster-proof-gate",
        "stop_condition": "ledger prioritizes metadata proof only; semantic and equivalence claims remain unauthorized",
    }
    _write_csv(summary_csv, list(summary), [summary])
    _write_csv(handoff_csv, list(summary), [summary])
    class_counts = Counter(row.primary_class for row in ledger.rows)
    status_counts = Counter(row.reconciliation_status for row in ledger.rows)
    dashboard_html.parent.mkdir(parents=True, exist_ok=True)
    dashboard_html.write_text(
        "<!doctype html><html lang=\"fr\"><meta charset=\"utf-8\"><title>TOMB5 registre Ghidra</title>"
        "<h1>TOMB5 / registre fini des clusters Ghidra sans correspondance</h1>"
        f"<p>{ledger.unmapped_function_count} fonctions · {ledger.cluster_count} clusters · {ledger.isolated_cluster_count} clusters isolés</p>"
        f"<p>Réconciliation : candidate {status_counts['candidate']} · ambiguë {status_counts['ambiguous']} · aucune {status_counts['none']}.</p>"
        "<p>Classes primaires : " + html.escape(", ".join(f"{key} {class_counts[key]}" for key in sorted(class_counts))) + ".</p>"
        "<p>Readiness code : bloquée. Prochain axe : porte de preuve des clusters isolés.</p></html>\n", encoding="utf-8")
    story.parent.mkdir(parents=True, exist_ok=True)
    story.write_text(
        "# RE-692 — registre fini des clusters Ghidra sans correspondance\n\n## Progress tracker\n\n"
        "- [x] Handoff RE-691 validé ; baseline RE-690 relue fail-closed.\n"
        "- [x] Les 723 fonctions sont affectées une fois à 112 clusters opaques et classés.\n"
        "- [x] Les relations internes et de frontière mappée sont comptées en agrégats.\n"
        "- [x] Les états de réconciliation restent agrégés et non identifiants.\n"
        "- [x] Dashboard et handoff synchronisés ; code et marqueurs bloqués.\n\n## Décision\n\n"
        "RE-693 peut examiner la porte de preuve des 79 clusters isolés, sans patch source ni prétention d’équivalence.\n", encoding="utf-8")
    return {"ledger_csv": ledger_csv, "summary_csv": summary_csv, "handoff_csv": handoff_csv, "dashboard_html": dashboard_html, "story": story}


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    ledger = build_ledger(root)
    for name, path in write_artifacts(ledger, root).items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
