from pathlib import Path
import csv

from scripts.reverse.re303_source_patch_gate_denial_reduction import (
    FORBIDDEN,
    build_source_patch_gate_denial_reduction,
    write_all_artifacts,
)


def test_re303_reduces_source_patch_gate_denials_metadata_only():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_source_patch_gate_denial_reduction(repo)

    assert bundle.summary.story_id == "RE-303"
    assert bundle.summary.upstream_handoff == "RE-302"
    assert bundle.summary.source_patch_gate_file_count == 16
    assert bundle.summary.evidence_row_count == 58
    assert bundle.summary.normalized_class_count == 5
    assert bundle.summary.metadata_reduction_ready_count == 5
    assert bundle.summary.domain_selection_ready_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.raw_or_asset_source_count == 0
    assert bundle.summary.next_ticket == "RE-304"
    assert bundle.summary.next_topic == "source-patch-gate-denial-readiness-gate"
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    rows_by_class = {row.normalized_class: row for row in bundle.rows}
    assert set(rows_by_class) == {
        "non-raw-equivalence-proof-missing",
        "upstream-gate-zero-ready",
        "symbolic-equivalence-proof-missing",
        "state-contract-and-non-raw-equivalence-missing",
        "source-contract-and-non-raw-equivalence-missing",
    }
    assert rows_by_class["non-raw-equivalence-proof-missing"].evidence_count == 22
    assert rows_by_class["upstream-gate-zero-ready"].source_patch_gate_file_count == 5
    assert rows_by_class["symbolic-equivalence-proof-missing"].unique_denial_count == 1
    assert all(row.metadata_reduction_ready == "yes" for row in bundle.rows)
    assert all(row.domain_selection_ready == "no" for row in bundle.rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.rows)
    assert bundle.rows == sorted(bundle.rows, key=lambda row: (-row.evidence_count, row.normalized_class))


def test_re303_writes_reduction_artifacts_and_handoff(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_source_patch_gate_denial_reduction(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"taxonomy_csv", "evidence_csv", "summary_csv", "handoff_csv", "md", "story"}

    taxonomy_rows = list(csv.DictReader(written["taxonomy_csv"].open(newline="", encoding="utf-8")))
    assert len(taxonomy_rows) == 5
    assert taxonomy_rows[0]["normalized_class"] == "non-raw-equivalence-proof-missing"
    assert taxonomy_rows[0]["evidence_count"] == "22"
    assert taxonomy_rows[0]["domain_selection_ready"] == "no"
    assert taxonomy_rows[0]["source_patch_authorized"] == "no"

    evidence_rows = list(csv.DictReader(written["evidence_csv"].open(newline="", encoding="utf-8")))
    assert len(evidence_rows) == 58
    assert set(evidence_rows[0]) == {
        "source_patch_gate_file",
        "row_number",
        "normalized_class",
        "denial_fingerprint",
    }
    assert "denial_text" not in evidence_rows[0]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-304"
    assert handoff["next_topic"] == "source-patch-gate-denial-readiness-gate"
    assert handoff["domain_selection_ready_count"] == "0"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-302 source-patch denial handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-304" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-303 source-patch gate denial reduction" in md
    assert "No production source or marker change is authorized" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
