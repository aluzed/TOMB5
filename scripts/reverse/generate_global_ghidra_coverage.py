#!/usr/bin/env python3
"""Build a reproducible, metadata-only global TOMB5 Ghidra coverage snapshot.

The detailed Ghidra export stays under ignored build/reverse/.  Versioned outputs
contain only aggregate counts and readiness metadata, never addresses, bytes,
raw calls, or decompiler text.
"""
from __future__ import annotations

import csv
import html
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

FORBIDDEN = ("0x", "opcode", "payload", ".bin", "disassembly", "pseudocode")
GHIDRA_EXPORT = Path("build/reverse/generated/ghidra-functions.csv")
REPO_MAP = Path("build/reverse/generated/repo-function-map.csv")


@dataclass(frozen=True)
class CoverageRow:
    coverage_state: str
    size_bucket: str
    function_count: int


@dataclass(frozen=True)
class Snapshot:
    ghidra_function_count: int
    repo_function_count: int
    mapped_repo_row_count: int
    repo_only_row_count: int
    mapped_ghidra_function_count: int
    ghidra_only_function_count: int
    coverage: tuple[CoverageRow, ...]


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _size_bucket(raw_size: str) -> str:
    size = int(raw_size)
    if size <= 64:
        return "tiny-1-64"
    if size <= 256:
        return "small-65-256"
    if size <= 1024:
        return "medium-257-1024"
    return "large-1025-plus"


def build_snapshot(repo: Path) -> Snapshot:
    export_path = repo / GHIDRA_EXPORT
    map_path = repo / REPO_MAP
    if not export_path.is_file() or not map_path.is_file():
        raise ValueError("Missing ignored Ghidra function export or repository mapping snapshot")

    ghidra_rows = _read_csv(export_path)
    repo_rows = _read_csv(map_path)
    if not ghidra_rows or not repo_rows:
        raise ValueError("Ghidra function export and repository mapping must be non-empty")

    normalized_entries = [row.get("entry", "").lower() for row in ghidra_rows]
    if not all(normalized_entries) or len(set(normalized_entries)) != len(normalized_entries):
        raise ValueError("Ghidra entries must be unique non-empty values")
    mapping_statuses = {row.get("mapping_status", "") for row in repo_rows}
    unexpected_statuses = mapping_statuses - {"mapped", "repo_only"}
    if unexpected_statuses:
        raise ValueError(f"Repository mapping has unexpected mapping statuses: {sorted(unexpected_statuses)}")

    mapped_entries = {
        row["ghidra_entry"].lower()
        for row in repo_rows
        if row.get("mapping_status") == "mapped" and row.get("ghidra_entry")
    }
    entries = {row["entry"].lower() for row in ghidra_rows}
    if not mapped_entries <= entries:
        raise ValueError("Repository mapping references entries absent from ignored Ghidra snapshot")

    counts: Counter[tuple[str, str]] = Counter()
    for row in ghidra_rows:
        state = "mapped-to-repo" if row["entry"].lower() in mapped_entries else "ghidra-only"
        counts[(state, _size_bucket(row["body_size"]))] += 1
    coverage = tuple(
        CoverageRow(state, bucket, count)
        for (state, bucket), count in sorted(counts.items())
    )
    mapped_repo_rows = sum(row.get("mapping_status") == "mapped" for row in repo_rows)
    repo_only_rows = sum(row.get("mapping_status") == "repo_only" for row in repo_rows)
    return Snapshot(
        ghidra_function_count=len(ghidra_rows),
        repo_function_count=len(repo_rows),
        mapped_repo_row_count=mapped_repo_rows,
        repo_only_row_count=repo_only_rows,
        mapped_ghidra_function_count=len(mapped_entries),
        ghidra_only_function_count=len(ghidra_rows) - len(mapped_entries),
        coverage=coverage,
    )


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _summary(snapshot: Snapshot) -> dict[str, object]:
    return {
        "story_id": "RE-690",
        "topic": "global-ghidra-coverage-baseline",
        "ghidra_function_count": snapshot.ghidra_function_count,
        "mapped_ghidra_function_count": snapshot.mapped_ghidra_function_count,
        "ghidra_only_function_count": snapshot.ghidra_only_function_count,
        "repo_function_count": snapshot.repo_function_count,
        "mapped_repo_row_count": snapshot.mapped_repo_row_count,
        "repo_only_row_count": snapshot.repo_only_row_count,
        "coverage_status": "inventory-complete-not-semantic-complete",
        "raw_evidence_versioned": "no",
        "code_change_readiness": "blocked",
        "next_topic": "triage-ghidra-only-function-clusters",
        "stop_condition": "global inventory is a prioritization baseline, not behavior or equivalence proof",
    }


def write_artifacts(snapshot: Snapshot, root: Path) -> dict[str, Path]:
    generated = root / "docs/reverse/generated"
    coverage_csv = generated / "re690-global-ghidra-coverage.csv"
    summary_csv = generated / "re690-global-ghidra-coverage-summary.csv"
    dashboard_html = root / "docs/reverse/tomb5-global-coverage.html"
    story = root / "docs/stories/RE-690-global-ghidra-coverage-baseline.md"

    _write_csv(coverage_csv, ["coverage_state", "size_bucket", "function_count"], [row.__dict__ for row in snapshot.coverage])
    summary = _summary(snapshot)
    _write_csv(summary_csv, list(summary), [summary])
    rows = "".join(
        f"<tr><td>{html.escape(row.coverage_state)}</td><td>{html.escape(row.size_bucket)}</td><td>{row.function_count}</td></tr>"
        for row in snapshot.coverage
    )
    dashboard_html.parent.mkdir(parents=True, exist_ok=True)
    dashboard_html.write_text(
        "<!doctype html><html lang=\"fr\"><meta charset=\"utf-8\"><title>TOMB5 couverture globale</title>"
        "<style>body{font:16px system-ui;background:#101514;color:#edf4ee;margin:auto;max-width:960px;padding:32px}"
        "table{border-collapse:collapse;width:100%}td,th{padding:9px;border-bottom:1px solid #30433e;text-align:left}.n{font-size:30px;color:#b7f36a}</style>"
        f"<h1>TOMB5 / couverture Ghidra</h1><p class=\"n\">{snapshot.ghidra_function_count} fonctions inventoriées</p>"
        f"<p>Mappées au dépôt : {snapshot.mapped_ghidra_function_count} · Sans correspondance exacte : {snapshot.ghidra_only_function_count}</p>"
        "<p>Ce tableau est une couverture d’inventaire, pas une preuve de comportement ou d’équivalence binaire.</p>"
        "<table><tr><th>Couverture</th><th>Taille</th><th>Fonctions</th></tr>"
        f"{rows}</table><p>Readiness code : bloquée. Prochaine étape : triage par clusters des fonctions sans correspondance.</p></html>\n",
        encoding="utf-8",
    )
    story.parent.mkdir(parents=True, exist_ok=True)
    story.write_text(
        "# RE-690 — baseline de couverture Ghidra globale\n\n"
        "## Progress tracker\n\n"
        "- [x] Export Ghidra complet régénéré dans le répertoire ignoré.\n"
        "- [x] Mapping exact dépôt ↔ Ghidra réconcilié.\n"
        "- [x] Matrice de couverture agrégée, sans adresses ni dump, générée.\n"
        "- [x] Dashboard global reproductible généré.\n"
        "- [x] Aucune modification de source ou de marqueur autorisée.\n\n"
        "## Décision\n\n"
        "La couverture d’inventaire est complète pour ce snapshot ; elle ne prouve ni le comportement ni l’équivalence binaire. "
        "Le prochain travail sûr est le triage par clusters des fonctions sans correspondance exacte.\n",
        encoding="utf-8",
    )
    return {"coverage_csv": coverage_csv, "summary_csv": summary_csv, "dashboard_html": dashboard_html, "story": story}


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    snapshot = build_snapshot(repo)
    written = write_artifacts(snapshot, repo)
    print(f"Ghidra functions: {snapshot.ghidra_function_count}")
    print(f"Mapped Ghidra functions: {snapshot.mapped_ghidra_function_count}")
    print(f"Ghidra-only functions: {snapshot.ghidra_only_function_count}")
    for name, path in written.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
