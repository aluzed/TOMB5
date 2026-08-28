#!/usr/bin/env python3
"""Generate a safe, aggregate completion matrix for Ghidra-only functions.

Detailed function identities and graph edges are consumed only from ignored inputs.
Versioned artifacts contain category and cluster aggregates, never raw evidence.
"""
from __future__ import annotations

import csv
import html
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path

FORBIDDEN = ("0x", "opcode", "payload", ".bin", "disassembly", "pseudocode")
BASELINE = Path("docs/reverse/generated/re690-global-ghidra-coverage-summary.csv")
GHIDRA_EXPORT = Path("build/reverse/generated/ghidra-functions.csv")
REPO_MAP = Path("build/reverse/generated/repo-function-map.csv")


@dataclass(frozen=True)
class CategoryRow:
    category: str
    function_count: int
    cluster_count: int
    confidence: str
    recommended_next_proof: str


@dataclass(frozen=True)
class Matrix:
    unmapped_function_count: int
    cluster_count: int
    reconciliation_candidate_count: int
    categories: tuple[CategoryRow, ...]


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _validate_baseline(root: Path) -> None:
    rows = _read_csv(root / BASELINE) if (root / BASELINE).is_file() else []
    if len(rows) != 1:
        raise ValueError("RE-690 baseline must contain exactly one summary row")
    row = rows[0]
    expected = {
        "story_id": "RE-690", "ghidra_only_function_count": "723",
        "coverage_status": "inventory-complete-not-semantic-complete",
        "raw_evidence_versioned": "no", "code_change_readiness": "blocked",
    }
    for field, value in expected.items():
        if row.get(field) != value:
            raise ValueError(f"RE-690 baseline drift in {field}")


def _components(nodes: set[str], edges: dict[str, set[str]]) -> list[set[str]]:
    remaining = set(nodes)
    groups = []
    while remaining:
        start = min(remaining)
        group = {start}
        queue = deque([start])
        remaining.remove(start)
        while queue:
            node = queue.popleft()
            for peer in edges[node]:
                if peer in remaining:
                    remaining.remove(peer)
                    group.add(peer)
                    queue.append(peer)
        groups.append(group)
    return groups


def build_matrix(root: Path) -> Matrix:
    _validate_baseline(root)
    ghidra_rows = _read_csv(root / GHIDRA_EXPORT)
    repo_rows = _read_csv(root / REPO_MAP)
    if not ghidra_rows or not repo_rows:
        raise ValueError("ignored mapping inputs must be non-empty")
    mapped = {row.get("ghidra_entry", "").lower() for row in repo_rows if row.get("mapping_status") == "mapped"}
    unmapped = [row for row in ghidra_rows if row.get("entry", "").lower() not in mapped]
    if len(unmapped) != 723:
        raise ValueError("RE-690 unmapped inventory drift")

    names = {row["name"] for row in unmapped}
    edges = {name: set() for name in names}
    inbound = Counter()
    outbound = Counter()
    sizes = {}
    for row in unmapped:
        name = row["name"]
        sizes[name] = int(row["body_size"])
        for called in filter(None, row.get("called_functions", "").split(";")):
            if called in names:
                edges[name].add(called)
                edges[called].add(name)
                outbound[name] += 1
                inbound[called] += 1
    groups = _components(names, edges)
    membership = {name: index for index, group in enumerate(groups) for name in group}
    component_sizes = Counter(membership.values())
    repo_names = {row.get("repo_function", "") for row in repo_rows}
    reconciliation_candidates = sum(name in repo_names for name in names)

    category_for = {}
    for name in names:
        degree = len(edges[name])
        if degree == 0:
            category = "isolated"
        elif outbound[name] == 0 and inbound[name] > 0:
            category = "leaf"
        elif degree >= 8:
            category = "hub"
        elif sizes[name] > 1024 or component_sizes[membership[name]] >= 32:
            category = "large-block"
        else:
            category = "helper"
        category_for[name] = category
    proof = {
        "isolated": ("medium", "metadata identity and caller/callee absence check"),
        "leaf": ("medium", "source-backed caller-family map"),
        "helper": ("medium", "bounded helper signature and state-contract proof"),
        "hub": ("low", "partitioned callsite and ABI/state-contract proof"),
        "large-block": ("low", "split into bounded control-flow and state-contract clusters"),
    }
    counts = Counter(category_for.values())
    clusters = {category: set() for category in proof}
    for name, category in category_for.items():
        clusters[category].add(membership[name])
    categories = tuple(CategoryRow(category, counts[category], len(clusters[category]), *proof[category]) for category in sorted(proof))
    return Matrix(len(unmapped), len(groups), reconciliation_candidates, categories)


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_artifacts(matrix: Matrix, root: Path) -> dict[str, Path]:
    generated = root / "docs/reverse/generated"
    matrix_csv = generated / "re691-ghidra-unmapped-completion-matrix.csv"
    backlog_csv = generated / "re691-ghidra-unmapped-cluster-backlog.csv"
    summary_csv = generated / "re691-ghidra-unmapped-completion-summary.csv"
    handoff_csv = generated / "re691-ghidra-unmapped-completion-handoff.csv"
    dashboard_html = root / "docs/reverse/tomb5-ghidra-unmapped-completion.html"
    story = root / "docs/stories/RE-691-ghidra-unmapped-completion-matrix.md"
    rows = [row.__dict__ for row in matrix.categories]
    _write_csv(matrix_csv, list(rows[0]), rows)
    priority = {"isolated": 1, "leaf": 2, "helper": 3, "large-block": 4, "hub": 5}
    backlog = [
        {"priority_rank": priority[row.category], "cluster_class": row.category, "function_count": row.function_count,
         "confidence": row.confidence, "recommended_next_proof": row.recommended_next_proof, "code_change_readiness": "blocked"}
        for row in sorted(matrix.categories, key=lambda row: priority[row.category])
    ]
    _write_csv(backlog_csv, list(backlog[0]), backlog)
    summary = {"story_id": "RE-691", "topic": "ghidra-unmapped-completion-matrix", "predecessor": "RE-690",
               "unmapped_function_count": matrix.unmapped_function_count, "cluster_count": matrix.cluster_count,
               "reconciliation_candidate_count": matrix.reconciliation_candidate_count, "raw_evidence_versioned": "no",
               "code_change_readiness": "blocked", "next_ticket": "RE-692", "next_topic": "ghidra-unmapped-isolated-cluster-proof-gate",
               "stop_condition": "aggregate mapping prioritizes proof only; no semantic or equivalence authorization"}
    _write_csv(summary_csv, list(summary), [summary])
    _write_csv(handoff_csv, list(summary), [summary])
    table = "".join(f"<tr><td>{html.escape(row.category)}</td><td>{row.function_count}</td><td>{row.cluster_count}</td><td>{html.escape(row.confidence)}</td></tr>" for row in matrix.categories)
    dashboard_html.parent.mkdir(parents=True, exist_ok=True)
    story.parent.mkdir(parents=True, exist_ok=True)
    dashboard_html.write_text(
        "<!doctype html><html lang=\"fr\"><meta charset=\"utf-8\"><title>TOMB5 matrice Ghidra</title>"
        "<h1>TOMB5 / matrice de complétion Ghidra</h1>"
        f"<p>Fonctions sans correspondance exacte : {matrix.unmapped_function_count} · clusters : {matrix.cluster_count}</p>"
        "<p>La cartographie est une priorisation de preuve, jamais une équivalence binaire.</p>"
        "<table><tr><th>Classe</th><th>Fonctions</th><th>Clusters</th><th>Confiance</th></tr>" + table + "</table>"
        "<p>Readiness code : bloquée. Prochain axe : clusters isolés.</p></html>\n", encoding="utf-8")
    story.write_text(
        "# RE-691 — matrice de complétion des fonctions Ghidra sans correspondance\n\n## Progress tracker\n\n"
        "- [x] Baseline RE-690 validée fail-closed.\n- [x] Les 723 fonctions sans correspondance sont classées par connectivité et taille agrégées.\n"
        "- [x] Backlog fini par classes de clusters et confiance généré.\n- [x] Réconciliation des écarts nominaux comptée sans identité versionnée.\n"
        "- [x] Dashboard de complétion synchronisé.\n- [x] Toute modification du code et des marqueurs reste bloquée.\n\n## Décision\n\n"
        "La première preuve bornée est la porte de lecture des clusters isolés (RE-692). Cette matrice ne démontre ni comportement ni équivalence binaire.\n", encoding="utf-8")
    return {"matrix_csv": matrix_csv, "backlog_csv": backlog_csv, "summary_csv": summary_csv, "dashboard_html": dashboard_html, "story": story, "handoff_csv": handoff_csv}


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    matrix = build_matrix(root)
    for name, path in write_artifacts(matrix, root).items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
