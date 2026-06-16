from pathlib import Path
import csv

from scripts.reverse.re297_story_tracker_readiness_statement_reduction import (
    FORBIDDEN,
    build_readiness_reduction,
    write_all_artifacts,
)


def test_re297_consumes_re296_and_reduces_story_tracker_readiness_statements():
    repo = Path(__file__).resolve().parents[2]
    reduction = build_readiness_reduction(repo)

    assert reduction.summary.story_id == "RE-297"
    assert reduction.summary.upstream_handoff == "RE-296"
    assert reduction.summary.selected_candidate_id == "story-tracker-blocked-readiness-statements"
    assert reduction.summary.selected_source_id == "story-tracker"
    assert reduction.summary.normalized_class_count >= 6
    assert reduction.summary.story_file_count >= 300
    assert reduction.summary.evidence_line_count >= 650
    assert reduction.summary.raw_or_asset_source_count == 0
    assert reduction.summary.domain_selection_ready_count == 0
    assert reduction.summary.next_ticket == "RE-298"
    assert reduction.summary.next_topic == "story-tracker-blocker-taxonomy-readiness-gate"
    assert reduction.summary.selected_domain == "none"
    assert reduction.summary.selected_pivot == "none"
    assert reduction.summary.metadata_work_readiness == "ready"
    assert reduction.summary.code_change_readiness == "blocked"

    rows_by_class = {row.normalized_class: row for row in reduction.rows}
    for required in (
        "source-or-code-readiness-blocked",
        "blocked-readiness-status",
        "no-production-source-authorization",
        "domain-selection-still-blocked",
        "stop-condition-before-source-or-domain-work",
    ):
        assert required in rows_by_class
        assert rows_by_class[required].metadata_reduction_ready == "yes"
        assert rows_by_class[required].source_patch_authorized == "no"
        assert rows_by_class[required].domain_selection_ready == "no"

    top = reduction.rows[0]
    assert top.evidence_count >= rows_by_class["blocked-readiness-status"].evidence_count
    assert top.source_patch_authorized == "no"
    assert reduction.rows == sorted(reduction.rows, key=lambda row: (-row.evidence_count, row.normalized_class))


def test_re297_outputs_metadata_only_taxonomy_story_and_handoff(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    reduction = build_readiness_reduction(repo)
    written = write_all_artifacts(reduction, tmp_path)

    assert set(written) == {"taxonomy_csv", "evidence_csv", "summary_csv", "handoff_csv", "md", "story"}

    taxonomy = list(csv.DictReader(written["taxonomy_csv"].open(newline="", encoding="utf-8")))
    assert len(taxonomy) == reduction.summary.normalized_class_count
    assert all(row["source_patch_authorized"] == "no" for row in taxonomy)
    assert all(row["domain_selection_ready"] == "no" for row in taxonomy)

    evidence = list(csv.DictReader(written["evidence_csv"].open(newline="", encoding="utf-8")))
    assert len(evidence) == reduction.summary.evidence_line_count
    assert {"story_file", "line_number", "normalized_class", "line_fingerprint"}.issubset(evidence[0])
    assert "line_text" not in evidence[0]

    summary = list(csv.DictReader(written["summary_csv"].open(newline="", encoding="utf-8")))[0]
    assert summary["next_ticket"] == "RE-298"
    assert summary["next_topic"] == "story-tracker-blocker-taxonomy-readiness-gate"
    assert summary["domain_selection_ready_count"] == "0"
    assert summary["code_change_readiness"] == "blocked"

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["stop_condition"] == "run taxonomy readiness gate before reopening proof-domain selection"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-297 story-tracker readiness statement reduction" in md
    assert "## Normalized blocker taxonomy" in md
    assert "No production source or marker change is authorized" in md

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-296 candidate-selection handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-298" in story

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
