from pathlib import Path
import csv

from scripts.reverse.re295_metadata_blocker_extraction import (
    FORBIDDEN,
    build_blocker_extraction,
    write_all_artifacts,
)


def test_re295_consumes_re294_and_extracts_top_metadata_blockers():
    repo = Path(__file__).resolve().parents[2]
    extraction = build_blocker_extraction(repo)

    assert extraction.summary.story_id == "RE-295"
    assert extraction.summary.upstream_handoff == "RE-294"
    assert extraction.summary.source_count == 5
    assert extraction.summary.extraction_row_count == 5
    assert extraction.summary.raw_or_asset_source_count == 0
    assert extraction.summary.metadata_reduction_ready_count >= 3
    assert extraction.summary.domain_selection_ready_count == 0
    assert extraction.summary.top_source_id == "story-tracker"
    assert extraction.summary.next_ticket == "RE-296"
    assert extraction.summary.next_topic == "blocker-reduction-candidate-selection"
    assert extraction.summary.selected_domain == "none"
    assert extraction.summary.selected_pivot == "none"
    assert extraction.summary.metadata_work_readiness == "ready"
    assert extraction.summary.code_change_readiness == "blocked"

    rows_by_source = {row.source_id: row for row in extraction.rows}
    assert rows_by_source["story-tracker"].evidence_count >= 600
    assert rows_by_source["generated-markdown"].evidence_count >= 400
    assert rows_by_source["handoff-csvs"].evidence_count >= 38
    assert rows_by_source["handoff-csvs"].evidence_count == 40
    assert rows_by_source["source-patch-gates"].evidence_count >= 58
    assert rows_by_source["proof-audits"].evidence_count >= 300
    assert rows_by_source["source-patch-gates"].dominant_blocker == "missing-non-raw-binary-equivalence-proof"
    assert rows_by_source["proof-audits"].dominant_blocker == "missing-maths-render-source-contract-and-non-raw-equivalence-proof"
    assert all(row.safety_class == "metadata-only" for row in extraction.rows)
    assert all(row.domain_selection_ready == "no" for row in extraction.rows)
    assert extraction.rows == sorted(extraction.rows, key=lambda row: (-row.reduction_score, row.source_id))

    rebuilt = build_blocker_extraction(repo)
    assert {row.source_id: row for row in rebuilt.rows}["handoff-csvs"].evidence_count == 40


def test_re295_outputs_metadata_only_extraction_story_and_handoff(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    extraction = build_blocker_extraction(repo)
    written = write_all_artifacts(extraction, tmp_path)

    assert set(written) == {"extraction_csv", "summary_csv", "handoff_csv", "md", "story"}

    rows = list(csv.DictReader(written["extraction_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == extraction.summary.extraction_row_count
    assert rows[0]["source_id"] == "story-tracker"
    assert all(row["safety_class"] == "metadata-only" for row in rows)
    assert all(row["domain_selection_ready"] == "no" for row in rows)

    summary = list(csv.DictReader(written["summary_csv"].open(newline="", encoding="utf-8")))[0]
    assert summary["next_ticket"] == "RE-296"
    assert summary["next_topic"] == "blocker-reduction-candidate-selection"
    assert summary["metadata_work_readiness"] == "ready"
    assert summary["code_change_readiness"] == "blocked"
    assert summary["domain_selection_ready_count"] == "0"

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["selected_domain"] == "none"
    assert handoff["stop_condition"] == "select a metadata blocker-reduction candidate before reopening any proof domain"

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-295 metadata blocker extraction" in md
    assert "## Extracted blocker sources" in md
    assert "Domain selection ready rows: `0`" in md
    assert "No production source or marker change is authorized" in md

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-294 ranking handoff validated." in story
    assert "## Next objective" in story
    assert "RE-296" in story

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
