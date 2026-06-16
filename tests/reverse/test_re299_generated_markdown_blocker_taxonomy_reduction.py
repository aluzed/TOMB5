from pathlib import Path
import csv

from scripts.reverse.re299_generated_markdown_blocker_taxonomy_reduction import (
    FORBIDDEN,
    build_generated_markdown_reduction,
    write_all_artifacts,
)


def test_re299_reduces_generated_markdown_blockers_without_reopening_domain_selection():
    repo = Path(__file__).resolve().parents[2]
    reduction = build_generated_markdown_reduction(repo)

    assert reduction.summary.story_id == "RE-299"
    assert reduction.summary.upstream_handoff == "RE-298"
    assert reduction.summary.generated_markdown_file_count >= 80
    assert reduction.summary.evidence_line_count >= 300
    assert reduction.summary.normalized_class_count >= 6
    assert reduction.summary.metadata_reduction_ready_count == reduction.summary.normalized_class_count
    assert reduction.summary.domain_selection_ready_count == 0
    assert reduction.summary.raw_or_asset_source_count == 0
    assert reduction.summary.next_ticket == "RE-300"
    assert reduction.summary.next_topic == "generated-markdown-blocker-taxonomy-readiness-gate"
    assert reduction.summary.selected_domain == "none"
    assert reduction.summary.selected_pivot == "none"
    assert reduction.summary.code_change_readiness == "blocked"

    rows_by_class = {row.normalized_class: row for row in reduction.rows}
    for required in {
        "source-or-code-readiness-blocked",
        "no-production-source-authorization",
        "proof-or-marker-change-blocked",
        "domain-selection-still-blocked",
        "metadata-work-readiness-only",
        "generic-blocker-reference",
    }:
        assert required in rows_by_class

    assert all(row.metadata_reduction_ready == "yes" for row in reduction.rows)
    assert all(row.domain_selection_ready == "no" for row in reduction.rows)
    assert all(row.source_patch_authorized == "no" for row in reduction.rows)
    assert all(row.story_tracker_correlated in {"yes", "partial", "no"} for row in reduction.rows)
    assert rows_by_class["source-or-code-readiness-blocked"].story_tracker_correlated == "yes"
    assert reduction.rows == sorted(reduction.rows, key=lambda row: (-row.evidence_count, row.normalized_class))


def test_re299_outputs_metadata_only_evidence_story_and_handoff(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    reduction = build_generated_markdown_reduction(repo)
    written = write_all_artifacts(reduction, tmp_path)

    assert set(written) == {"taxonomy_csv", "evidence_csv", "summary_csv", "handoff_csv", "md", "story"}

    rows = list(csv.DictReader(written["taxonomy_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == reduction.summary.normalized_class_count
    assert all(row["metadata_reduction_ready"] == "yes" for row in rows)
    assert all(row["domain_selection_ready"] == "no" for row in rows)
    assert all(row["source_patch_authorized"] == "no" for row in rows)

    evidence = list(csv.DictReader(written["evidence_csv"].open(newline="", encoding="utf-8")))
    assert len(evidence) == reduction.summary.evidence_line_count
    assert set(evidence[0]) == {"markdown_file", "line_number", "normalized_class", "line_fingerprint"}
    assert "line_text" not in evidence[0]

    summary = list(csv.DictReader(written["summary_csv"].open(newline="", encoding="utf-8")))[0]
    assert summary["next_ticket"] == "RE-300"
    assert summary["next_topic"] == "generated-markdown-blocker-taxonomy-readiness-gate"
    assert summary["domain_selection_ready_count"] == "0"
    assert summary["code_change_readiness"] == "blocked"

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["stop_condition"] == "gate generated-markdown taxonomy before proof-domain selection can reopen"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-299 generated-Markdown blocker taxonomy reduction" in md
    assert "## Story-tracker correlation" in md
    assert "No production source or marker change is authorized" in md

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-298 readiness-gate handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-300" in story

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
