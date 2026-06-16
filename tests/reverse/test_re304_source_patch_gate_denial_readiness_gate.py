from pathlib import Path
import csv

from scripts.reverse.re304_source_patch_gate_denial_readiness_gate import (
    FORBIDDEN,
    build_readiness_gate,
    write_all_artifacts,
)


def test_re304_gates_source_patch_denial_taxonomy_without_reopening_domain_selection():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-304"
    assert bundle.summary.upstream_handoff == "RE-303"
    assert bundle.summary.source_patch_denial_class_count == 5
    assert bundle.summary.gate_row_count == 5
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.needs_more_metadata_count == 5
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.raw_or_asset_source_count == 0
    assert bundle.summary.next_ticket == "RE-305"
    assert bundle.summary.next_topic == "handoff-stop-condition-reduction"
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"
    assert bundle.summary.stop_condition == "reduce handoff stop conditions before proof-domain selection can reopen"

    rows_by_class = {row.normalized_class: row for row in bundle.rows}
    assert set(rows_by_class) == {
        "non-raw-equivalence-proof-missing",
        "upstream-gate-zero-ready",
        "symbolic-equivalence-proof-missing",
        "state-contract-and-non-raw-equivalence-missing",
        "source-contract-and-non-raw-equivalence-missing",
    }
    assert rows_by_class["non-raw-equivalence-proof-missing"].evidence_count == 22
    assert rows_by_class["upstream-gate-zero-ready"].gate_decision == "needs-handoff-stop-condition-metadata"
    assert rows_by_class["symbolic-equivalence-proof-missing"].readiness_reason.startswith("source-patch denials still require symbolic")
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.rows)
    assert all(row.next_metadata_source == "handoff-csvs" for row in bundle.rows)
    assert all(row.next_ticket == "RE-305" for row in bundle.rows)
    assert bundle.rows == sorted(bundle.rows, key=lambda row: (-row.evidence_count, row.normalized_class))


def test_re304_writes_gate_outputs_and_metadata_only_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"gate_csv", "summary_csv", "handoff_csv", "md", "story"}

    gate_rows = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert len(gate_rows) == 5
    assert gate_rows[0]["normalized_class"] == "non-raw-equivalence-proof-missing"
    assert gate_rows[0]["gate_decision"] == "needs-handoff-stop-condition-metadata"
    assert gate_rows[0]["ready_to_reopen_domain"] == "no"
    assert "denial_text" not in gate_rows[0]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-305"
    assert handoff["next_topic"] == "handoff-stop-condition-reduction"
    assert handoff["selected_domain"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-303 source-patch denial taxonomy handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-305" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-304 source-patch gate denial readiness gate" in md
    assert "handoff stop conditions are the next safe metadata source" in md
    assert "No production source or marker change is authorized" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
