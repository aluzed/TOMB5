import csv
from pathlib import Path


def test_unmapped_completion_matrix_is_deterministic_safe_and_actionable(tmp_path):
    from scripts.reverse.generate_ghidra_unmapped_completion_matrix import (
        FORBIDDEN,
        build_matrix,
        write_artifacts,
    )

    repo = Path(__file__).resolve().parents[2]
    matrix = build_matrix(repo)

    assert matrix.unmapped_function_count == 723
    assert sum(row.function_count for row in matrix.categories) == 723
    assert {row.category for row in matrix.categories} == {
        "helper",
        "hub",
        "isolated",
        "large-block",
        "leaf",
    }
    assert matrix.cluster_count > 0
    assert matrix.reconciliation_candidate_count >= 0

    written = write_artifacts(matrix, tmp_path)
    assert set(written) == {"matrix_csv", "backlog_csv", "summary_csv", "dashboard_html", "story", "handoff_csv"}

    matrix_rows = list(csv.DictReader(written["matrix_csv"].open(newline="", encoding="utf-8")))
    backlog_rows = list(csv.DictReader(written["backlog_csv"].open(newline="", encoding="utf-8")))
    summary_rows = list(csv.DictReader(written["summary_csv"].open(newline="", encoding="utf-8")))
    handoff_rows = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))
    assert len(matrix_rows) == 5
    assert [row["category"] for row in matrix_rows] == sorted(row["category"] for row in matrix_rows)
    assert backlog_rows
    assert [int(row["priority_rank"]) for row in backlog_rows] == list(range(1, len(backlog_rows) + 1))
    assert set(backlog_rows[0]) == {"priority_rank", "cluster_class", "function_count", "confidence", "recommended_next_proof", "code_change_readiness"}
    assert len(summary_rows) == len(handoff_rows) == 1
    assert summary_rows[0]["code_change_readiness"] == "blocked"
    assert handoff_rows[0]["next_ticket"] == "RE-692"

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "0x800" not in text
        for fragment in FORBIDDEN:
            assert fragment not in text


def test_unmapped_completion_matrix_rejects_bad_coverage_baseline(tmp_path):
    from scripts.reverse.generate_ghidra_unmapped_completion_matrix import build_matrix

    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    (generated / "re690-global-ghidra-coverage-summary.csv").write_text(
        "ghidra_only_function_count,code_change_readiness\n723,ready\n", encoding="utf-8"
    )
    try:
        build_matrix(tmp_path)
    except ValueError as error:
        assert "baseline" in str(error).lower()
    else:
        raise AssertionError("unsafe baseline must be rejected")
