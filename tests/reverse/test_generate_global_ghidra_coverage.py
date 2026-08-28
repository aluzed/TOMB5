import csv
from pathlib import Path

import pytest


def test_global_coverage_snapshot_is_safe_complete_and_reconciled(tmp_path):
    from scripts.reverse.generate_global_ghidra_coverage import (
        FORBIDDEN,
        build_snapshot,
        write_artifacts,
    )

    repo = Path(__file__).resolve().parents[2]
    snapshot = build_snapshot(repo)

    assert snapshot.ghidra_function_count > 0
    assert snapshot.repo_function_count > 0
    assert snapshot.mapped_repo_row_count + snapshot.repo_only_row_count == snapshot.repo_function_count
    assert sum(row.function_count for row in snapshot.coverage) == snapshot.ghidra_function_count
    assert {row.coverage_state for row in snapshot.coverage} <= {
        "mapped-to-repo",
        "ghidra-only",
    }

    written = write_artifacts(snapshot, tmp_path)
    assert set(written) == {"coverage_csv", "summary_csv", "dashboard_html", "story"}

    rows = list(csv.DictReader(written["coverage_csv"].open(newline="", encoding="utf-8")))
    assert rows
    assert [row["coverage_state"] for row in rows] == sorted(row["coverage_state"] for row in rows)
    assert "entry_address" not in rows[0]
    assert "function_name" not in rows[0]

    summary = list(csv.DictReader(written["summary_csv"].open(newline="", encoding="utf-8")))
    assert len(summary) == 1
    assert summary[0]["code_change_readiness"] == "blocked"
    assert summary[0]["raw_evidence_versioned"] == "no"

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert b"\r" not in path.read_bytes()
        assert "0x800" not in text
        for fragment in FORBIDDEN:
            assert fragment not in text


def test_global_coverage_rejects_missing_ignored_ghidra_snapshot(tmp_path):
    from scripts.reverse.generate_global_ghidra_coverage import build_snapshot

    with pytest.raises(ValueError, match="Missing ignored Ghidra function export"):
        build_snapshot(tmp_path)


def _write_snapshot_inputs(tmp_path, ghidra_rows, repo_rows):
    generated = tmp_path / "build/reverse/generated"
    generated.mkdir(parents=True)
    with (generated / "ghidra-functions.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["entry", "name", "body_size"])
        writer.writeheader()
        writer.writerows(ghidra_rows)
    with (generated / "repo-function-map.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["ghidra_entry", "mapping_status"])
        writer.writeheader()
        writer.writerows(repo_rows)


def test_global_coverage_rejects_duplicate_or_empty_ghidra_entries(tmp_path):
    from scripts.reverse.generate_global_ghidra_coverage import build_snapshot

    _write_snapshot_inputs(
        tmp_path,
        [{"entry": "entry-a", "name": "a", "body_size": "1"}, {"entry": "entry-a", "name": "b", "body_size": "2"}],
        [{"ghidra_entry": "entry-a", "mapping_status": "mapped"}],
    )
    with pytest.raises(ValueError, match="unique non-empty"):
        build_snapshot(tmp_path)


def test_global_coverage_rejects_unknown_mapping_status(tmp_path):
    from scripts.reverse.generate_global_ghidra_coverage import build_snapshot

    _write_snapshot_inputs(
        tmp_path,
        [{"entry": "entry-a", "name": "a", "body_size": "1"}],
        [{"ghidra_entry": "entry-a", "mapping_status": "uncertain"}],
    )
    with pytest.raises(ValueError, match="unexpected mapping statuses"):
        build_snapshot(tmp_path)
