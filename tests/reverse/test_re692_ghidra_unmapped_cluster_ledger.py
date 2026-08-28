import csv
from pathlib import Path


def test_re692_cluster_ledger_is_complete_deterministic_and_metadata_only(tmp_path):
    from scripts.reverse.re692_ghidra_unmapped_cluster_ledger import (
        FORBIDDEN,
        build_ledger,
        write_artifacts,
    )

    repo = Path(__file__).resolve().parents[2]
    ledger = build_ledger(repo)

    assert ledger.unmapped_function_count == 723
    assert ledger.cluster_count == 112
    assert ledger.isolated_cluster_count == 79
    assert sum(row.member_count for row in ledger.rows) == 723
    assert len(ledger.rows) == len({row.cluster_id for row in ledger.rows}) == 112
    assert [row.priority_rank for row in ledger.rows] == list(range(1, 113))
    assert all(row.code_change_readiness == "blocked" for row in ledger.rows)
    assert all(row.reconciliation_status in {"none", "candidate", "ambiguous"} for row in ledger.rows)

    written = write_artifacts(ledger, tmp_path)
    assert set(written) == {"ledger_csv", "summary_csv", "handoff_csv", "dashboard_html", "story"}
    rows = list(csv.DictReader(written["ledger_csv"].open(newline="", encoding="utf-8")))
    summary = list(csv.DictReader(written["summary_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == 112
    assert sum(int(row["member_count"]) for row in rows) == 723
    assert [int(row["priority_rank"]) for row in rows] == list(range(1, 113))
    assert len(summary) == 1
    assert summary[0]["next_ticket"] == "RE-693"
    assert summary[0]["code_change_readiness"] == "blocked"

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "0x800" not in text
        for fragment in FORBIDDEN:
            assert fragment not in text


def test_re692_cluster_ledger_rejects_duplicate_ghidra_entries(tmp_path):
    from scripts.reverse.re692_ghidra_unmapped_cluster_ledger import build_ledger

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    ignored = tmp_path / "build/reverse/generated"
    generated.mkdir(parents=True)
    ignored.mkdir(parents=True)
    (generated / "re690-global-ghidra-coverage-summary.csv").write_text(
        (source / "docs/reverse/generated/re690-global-ghidra-coverage-summary.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (ignored / "ghidra-functions.csv").write_text(
        "entry,name,body_size,called_functions,callers\nentry-a,func_a,4,,\nentry-a,func_b,4,,\n",
        encoding="utf-8",
    )
    (ignored / "repo-function-map.csv").write_text(
        "mapping_status,ghidra_entry,ghidra_name,repo_function\nmapped,entry-z,func_z,repo_z\n",
        encoding="utf-8",
    )

    try:
        build_ledger(tmp_path)
    except ValueError as error:
        assert "duplicate" in str(error).lower()
    else:
        raise AssertionError("duplicate Ghidra entries must fail closed")
