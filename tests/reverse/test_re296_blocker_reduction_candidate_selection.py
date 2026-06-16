from pathlib import Path
import csv

from scripts.reverse.re296_blocker_reduction_candidate_selection import (
    FORBIDDEN,
    build_candidate_selection,
    write_all_artifacts,
)


def test_re296_consumes_re295_and_selects_metadata_reduction_candidate():
    repo = Path(__file__).resolve().parents[2]
    selection = build_candidate_selection(repo)

    assert selection.summary.story_id == "RE-296"
    assert selection.summary.upstream_handoff == "RE-295"
    assert selection.summary.source_count == 5
    assert selection.summary.candidate_row_count == 5
    assert selection.summary.selected_candidate_id == "story-tracker-blocked-readiness-statements"
    assert selection.summary.selected_source_id == "story-tracker"
    assert selection.summary.selected_blocker == "blocked-readiness-statements"
    assert selection.summary.metadata_candidate_ready_count == 5
    assert selection.summary.domain_selection_ready_count == 0
    assert selection.summary.raw_or_asset_source_count == 0
    assert selection.summary.next_ticket == "RE-297"
    assert selection.summary.next_topic == "story-tracker-readiness-statement-reduction"
    assert selection.summary.selected_domain == "none"
    assert selection.summary.selected_pivot == "none"
    assert selection.summary.metadata_work_readiness == "ready"
    assert selection.summary.code_change_readiness == "blocked"

    rows_by_id = {row.candidate_id: row for row in selection.rows}
    selected = rows_by_id[selection.summary.selected_candidate_id]
    assert selected.selection_status == "selected"
    assert selected.source_id == "story-tracker"
    assert selected.blocker_class == "progression-blockers"
    assert selected.safety_class == "metadata-only"
    assert selected.domain_scope == "none"
    assert selected.pivot_scope == "none"
    assert selected.reduction_action == "normalize story readiness blocker statements before any proof-domain selection"
    assert selected.next_ticket == "RE-297"
    assert all(row.raw_or_asset_dependency == "no" for row in selection.rows)
    assert all(row.source_patch_authorized == "no" for row in selection.rows)
    assert all(row.domain_selection_ready == "no" for row in selection.rows)
    assert selection.rows == sorted(selection.rows, key=lambda row: (-row.selection_score, row.candidate_id))


def test_re296_outputs_metadata_only_candidate_story_and_handoff(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    selection = build_candidate_selection(repo)
    written = write_all_artifacts(selection, tmp_path)

    assert set(written) == {"candidate_csv", "summary_csv", "handoff_csv", "md", "story"}

    rows = list(csv.DictReader(written["candidate_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == selection.summary.candidate_row_count
    assert rows[0]["candidate_id"] == selection.summary.selected_candidate_id
    assert rows[0]["selection_status"] == "selected"
    assert all(row["domain_scope"] == "none" for row in rows)
    assert all(row["source_patch_authorized"] == "no" for row in rows)
    assert all(row["domain_selection_ready"] == "no" for row in rows)

    summary = list(csv.DictReader(written["summary_csv"].open(newline="", encoding="utf-8")))[0]
    assert summary["next_ticket"] == "RE-297"
    assert summary["next_topic"] == "story-tracker-readiness-statement-reduction"
    assert summary["selected_candidate_id"] == "story-tracker-blocked-readiness-statements"
    assert summary["code_change_readiness"] == "blocked"

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["stop_condition"] == "reduce selected metadata blocker candidate before reopening any proof domain"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-296 blocker reduction candidate selection" in md
    assert "## Selected candidate" in md
    assert "story-tracker-blocked-readiness-statements" in md
    assert "No production source or marker change is authorized" in md

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-295 blocker extraction handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-297" in story

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
