from pathlib import Path
import csv

from scripts.reverse.re307_blocker_reduction_source_exhaustion_audit import (
    FORBIDDEN,
    build_blocker_reduction_source_exhaustion_audit,
    write_all_artifacts,
)


def test_re307_audits_all_blocker_reduction_sources_as_exhausted_without_reopening_domain():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_blocker_reduction_source_exhaustion_audit(repo)

    assert bundle.summary.story_id == "RE-307"
    assert bundle.summary.upstream_handoff == "RE-306"
    assert bundle.summary.candidate_source_count == 5
    assert bundle.summary.reduction_complete_count == 5
    assert bundle.summary.readiness_gate_complete_count == 5
    assert bundle.summary.remaining_metadata_source_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.raw_or_asset_source_count == 0
    assert bundle.summary.next_ticket == "TBD"
    assert bundle.summary.next_topic == "blocker-reduction-sources-exhausted"
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.metadata_work_readiness == "blocked"
    assert bundle.summary.code_change_readiness == "blocked"
    assert bundle.summary.stop_condition == "provide changed upstream mapping or new non-raw proof evidence before selecting another proof domain"

    rows_by_source = {row.source_id: row for row in bundle.rows}
    assert set(rows_by_source) == {"story-tracker", "generated-markdown", "proof-audits", "source-patch-gates", "handoff-csvs"}
    assert rows_by_source["story-tracker"].reduction_story == "RE-297"
    assert rows_by_source["story-tracker"].gate_story == "RE-298"
    assert rows_by_source["generated-markdown"].reduction_story == "RE-299"
    assert rows_by_source["generated-markdown"].gate_story == "RE-300"
    assert rows_by_source["proof-audits"].reduction_story == "RE-301"
    assert rows_by_source["proof-audits"].gate_story == "RE-302"
    assert rows_by_source["source-patch-gates"].reduction_story == "RE-303"
    assert rows_by_source["source-patch-gates"].gate_story == "RE-304"
    assert rows_by_source["handoff-csvs"].reduction_story == "RE-305"
    assert rows_by_source["handoff-csvs"].gate_story == "RE-306"
    assert all(row.exhaustion_status == "exhausted-blocked" for row in bundle.rows)
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.rows)
    assert bundle.rows == sorted(bundle.rows, key=lambda row: row.selection_rank)


def test_re307_writes_exhaustion_outputs_and_metadata_only_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_blocker_reduction_source_exhaustion_audit(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"audit_csv", "summary_csv", "handoff_csv", "md", "story"}

    audit_rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(audit_rows) == 5
    assert audit_rows[0]["source_id"] == "story-tracker"
    assert audit_rows[0]["exhaustion_status"] == "exhausted-blocked"
    assert audit_rows[-1]["source_id"] == "handoff-csvs"
    assert "raw_evidence" not in audit_rows[0]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "TBD"
    assert handoff["next_topic"] == "blocker-reduction-sources-exhausted"
    assert handoff["selected_domain"] == "none"
    assert handoff["metadata_work_readiness"] == "blocked"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-306 handoff stop-condition readiness gate validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "changed upstream mapping" in story
    assert "new non-raw proof evidence" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-307 blocker-reduction source exhaustion audit" in md
    assert "All blocker-reduction metadata sources are exhausted or gated blocked" in md
    assert "No production source or marker change is authorized" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
