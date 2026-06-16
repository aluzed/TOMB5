from pathlib import Path
import csv

from scripts.reverse.re305_handoff_stop_condition_reduction import (
    FORBIDDEN,
    build_handoff_stop_condition_reduction,
    write_all_artifacts,
)


def test_re305_reduces_handoff_stop_conditions_without_reopening_domain_selection():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_handoff_stop_condition_reduction(repo)

    assert bundle.summary.story_id == "RE-305"
    assert bundle.summary.upstream_handoff == "RE-304"
    assert bundle.summary.handoff_file_count == 50
    assert bundle.summary.evidence_row_count == 50
    assert bundle.summary.normalized_class_count == 5
    assert bundle.summary.metadata_reduction_ready_count == 5
    assert bundle.summary.domain_selection_ready_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.raw_or_asset_source_count == 0
    assert bundle.summary.next_ticket == "RE-306"
    assert bundle.summary.next_topic == "handoff-stop-condition-readiness-gate"
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"
    assert bundle.summary.stop_condition == "gate handoff stop-condition taxonomy before proof-domain selection can reopen"

    rows_by_class = {row.normalized_class: row for row in bundle.rows}
    assert set(rows_by_class) == {
        "proof-blocked-or-no-marker-patch",
        "metadata-reduction-before-domain-selection",
        "generic-handoff-stop-condition",
        "upstream-input-refresh-or-change-needed",
        "readiness-gate-before-domain-selection",
    }
    assert rows_by_class["proof-blocked-or-no-marker-patch"].evidence_count == 27
    assert rows_by_class["metadata-reduction-before-domain-selection"].evidence_count == 12
    assert rows_by_class["generic-handoff-stop-condition"].evidence_count == 7
    assert rows_by_class["upstream-input-refresh-or-change-needed"].evidence_count == 3
    assert rows_by_class["readiness-gate-before-domain-selection"].evidence_count == 1
    assert all(row.metadata_reduction_ready == "yes" for row in bundle.rows)
    assert all(row.domain_selection_ready == "no" for row in bundle.rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.rows)
    assert bundle.rows == sorted(bundle.rows, key=lambda row: (-row.evidence_count, row.normalized_class))


def test_re305_writes_stop_condition_outputs_and_metadata_only_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_handoff_stop_condition_reduction(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"taxonomy_csv", "evidence_csv", "summary_csv", "handoff_csv", "md", "story"}

    taxonomy_rows = list(csv.DictReader(written["taxonomy_csv"].open(newline="", encoding="utf-8")))
    assert len(taxonomy_rows) == 5
    assert taxonomy_rows[0]["normalized_class"] == "proof-blocked-or-no-marker-patch"
    assert taxonomy_rows[0]["domain_selection_ready"] == "no"
    assert "stop_condition_text" not in taxonomy_rows[0]

    evidence_rows = list(csv.DictReader(written["evidence_csv"].open(newline="", encoding="utf-8")))
    assert len(evidence_rows) == 50
    assert set(evidence_rows[0]) == {"handoff_file", "row_number", "source_field", "normalized_class", "stop_condition_fingerprint"}
    assert "stop_condition_text" not in evidence_rows[0]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-306"
    assert handoff["next_topic"] == "handoff-stop-condition-readiness-gate"
    assert handoff["selected_domain"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-304 source-patch denial readiness gate handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-306" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-305 handoff stop-condition reduction" in md
    assert "Handoff stop conditions remain metadata-only blockers" in md
    assert "No production source or marker change is authorized" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
