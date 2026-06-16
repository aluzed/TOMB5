from pathlib import Path
import csv

from scripts.reverse.re294_evidence_source_gap_ranking import (
    FORBIDDEN,
    build_gap_ranking,
    write_all_artifacts,
)


def test_re294_consumes_re293_inventory_and_ranks_safe_sources():
    repo = Path(__file__).resolve().parents[2]
    ranking = build_gap_ranking(repo)

    assert ranking.summary.story_id == "RE-294"
    assert ranking.summary.upstream_handoff == "RE-293"
    assert ranking.summary.ranked_source_count == 15
    assert ranking.summary.testable_now_count >= 5
    assert ranking.summary.testable_with_existing_metadata_count == 2
    assert ranking.summary.supporting_only_count == 6
    assert ranking.summary.raw_or_asset_source_count == 0
    assert ranking.summary.top_source_id == "generated-markdown"
    assert ranking.summary.next_ticket == "RE-295"
    assert ranking.summary.next_topic == "metadata-blocker-extraction"
    assert ranking.summary.selected_domain == "none"
    assert ranking.summary.selected_pivot == "none"
    assert ranking.summary.code_change_readiness == "blocked"
    assert ranking.summary.metadata_work_readiness == "ready"

    rows_by_source = {row.source_id: row for row in ranking.rows}
    assert rows_by_source["generated-markdown"].actionability == "testable-now"
    assert rows_by_source["story-tracker"].actionability == "testable-now"
    assert rows_by_source["handoff-csvs"].actionability == "testable-now"
    assert rows_by_source["source-corpus"].actionability == "supporting-only"
    assert rows_by_source["function-priority"].actionability == "blocked-no-candidate"
    assert all(row.safety_class != "raw-or-asset" for row in ranking.rows)
    assert ranking.rows == sorted(ranking.rows, key=lambda row: (-row.priority_score, row.source_id))


def test_re294_outputs_metadata_only_gap_ranking_story_and_handoff(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    ranking = build_gap_ranking(repo)
    written = write_all_artifacts(ranking, tmp_path)

    assert set(written) == {"ranking_csv", "summary_csv", "handoff_csv", "md", "story"}

    rows = list(csv.DictReader(written["ranking_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == ranking.summary.ranked_source_count
    assert rows[0]["source_id"] == "generated-markdown"
    assert rows[0]["actionability"] == "testable-now"
    assert all(row["safety_class"] in {"metadata-only", "source-symbolic"} for row in rows)

    summary = list(csv.DictReader(written["summary_csv"].open(newline="", encoding="utf-8")))[0]
    assert summary["next_ticket"] == "RE-295"
    assert summary["next_topic"] == "metadata-blocker-extraction"
    assert summary["metadata_work_readiness"] == "ready"
    assert summary["code_change_readiness"] == "blocked"
    assert summary["testable_now_count"] == "5"
    assert summary["testable_with_existing_metadata_count"] == "2"
    assert summary["supporting_only_count"] == "6"

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["selected_domain"] == "none"
    assert handoff["stop_condition"] == "extract machine-readable blockers from top-ranked metadata sources before selecting a proof domain"

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-294 evidence source gap ranking" in md
    assert "## Ranked evidence sources" in md
    assert "Raw/asset sources admitted: `0`" in md
    assert "No production source or marker change is authorized" in md

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-293 source inventory handoff validated." in story
    assert "## Next objective" in story
    assert "RE-295" in story

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
