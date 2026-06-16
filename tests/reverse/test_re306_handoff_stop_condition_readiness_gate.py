from pathlib import Path
import csv

from scripts.reverse.re306_handoff_stop_condition_readiness_gate import (
    FORBIDDEN,
    build_handoff_stop_condition_readiness_gate,
    write_all_artifacts,
)


def test_re306_gates_handoff_stop_condition_taxonomy_without_reopening_domain_selection():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_handoff_stop_condition_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-306"
    assert bundle.summary.upstream_handoff == "RE-305"
    assert bundle.summary.handoff_stop_condition_class_count == 5
    assert bundle.summary.gate_row_count == 5
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.needs_new_evidence_count == 5
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.raw_or_asset_source_count == 0
    assert bundle.summary.next_ticket == "RE-307"
    assert bundle.summary.next_topic == "blocker-reduction-source-exhaustion-audit"
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"
    assert bundle.summary.stop_condition == "audit blocker-reduction metadata source exhaustion before selecting another proof domain"

    rows_by_class = {row.normalized_class: row for row in bundle.rows}
    assert set(rows_by_class) == {
        "proof-blocked-or-no-marker-patch",
        "metadata-reduction-before-domain-selection",
        "generic-handoff-stop-condition",
        "upstream-input-refresh-or-change-needed",
        "readiness-gate-before-domain-selection",
    }
    assert rows_by_class["proof-blocked-or-no-marker-patch"].evidence_count == 27
    assert rows_by_class["proof-blocked-or-no-marker-patch"].gate_decision == "needs-new-non-raw-proof-evidence"
    assert rows_by_class["upstream-input-refresh-or-change-needed"].gate_decision == "needs-upstream-input-change"
    assert rows_by_class["metadata-reduction-before-domain-selection"].readiness_reason.startswith("handoff stop conditions request more metadata reduction")
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.rows)
    assert all(row.next_metadata_source == "blocker-reduction-source-exhaustion-audit" for row in bundle.rows)
    assert all(row.next_ticket == "RE-307" for row in bundle.rows)
    assert bundle.rows == sorted(bundle.rows, key=lambda row: (-row.evidence_count, row.normalized_class))


def test_re306_writes_gate_outputs_and_metadata_only_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_handoff_stop_condition_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"gate_csv", "summary_csv", "handoff_csv", "md", "story"}

    gate_rows = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert len(gate_rows) == 5
    assert gate_rows[0]["normalized_class"] == "proof-blocked-or-no-marker-patch"
    assert gate_rows[0]["gate_decision"] == "needs-new-non-raw-proof-evidence"
    assert gate_rows[0]["ready_to_reopen_domain"] == "no"
    assert "stop_condition_text" not in gate_rows[0]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-307"
    assert handoff["next_topic"] == "blocker-reduction-source-exhaustion-audit"
    assert handoff["selected_domain"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-305 handoff stop-condition reduction handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-307" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-306 handoff stop-condition readiness gate" in md
    assert "Handoff stop-condition classes do not reopen proof-domain selection" in md
    assert "No production source or marker change is authorized" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
