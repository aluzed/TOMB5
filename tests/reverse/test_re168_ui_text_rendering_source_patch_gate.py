from pathlib import Path
import csv

from scripts.reverse.re168_ui_text_rendering_source_patch_gate import (
    build_ui_text_rendering_source_patch_gate,
    write_all_artifacts,
)


def test_re168_consumes_re167_readiness_and_denies_all_patches():
    repo = Path(__file__).resolve().parents[2]
    gate = build_ui_text_rendering_source_patch_gate(repo)

    assert gate.story_id == "RE-168"
    assert gate.upstream_ticket == "RE-167"
    assert gate.cluster == "ui-text-rendering"
    assert gate.next_ticket == "RE-169"
    assert gate.readiness_row_count == 9
    assert gate.source_patch_allowed_count == 0
    assert gate.marker_change_allowed_count == 0
    assert gate.final_decision == "source-and-marker-patch-denied-no-ready-rows"
    assert len(gate.patch_rows) == 9
    assert all(row.source_patch_decision == "denied" for row in gate.patch_rows)
    assert all(row.marker_change_decision == "denied" for row in gate.patch_rows)
    assert all(row.production_source_modified == "no" for row in gate.patch_rows)
    assert all(row.marker_modified == "no" for row in gate.patch_rows)
    assert all(row.stop_reason == "no-re167-ready-row" for row in gate.patch_rows)
    assert all(row.next_action == "handoff-to-re169-next-cluster-selection" for row in gate.patch_rows)

    by_id = {row.contract_id: row for row in gate.patch_rows}
    assert by_id["ui-text-printstring-scale-flag-lifecycle"].function == "PrintString"
    assert by_id["ui-text-printstring-scale-flag-lifecycle"].required_symbolic_proof == "scale lifetime and per-call isolation proof"
    assert by_id["ui-text-drawchar-draw-buffer-contract"].function == "DrawChar"
    assert by_id["ui-text-drawchar-draw-buffer-contract"].patch_gate_status == "blocked-by-missing-equivalence-proof"


def test_re168_outputs_metadata_only_no_patch_story_and_handoff(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    gate = build_ui_text_rendering_source_patch_gate(repo)
    written = write_all_artifacts(gate, tmp_path)

    rows = list(csv.DictReader(written["patch_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == 9
    assert all(row["source_patch_decision"] == "denied" for row in rows)
    assert all(row["marker_change_decision"] == "denied" for row in rows)
    assert all(row["production_source_modified"] == "no" for row in rows)
    assert all(row["marker_modified"] == "no" for row in rows)
    assert all(row["stop_reason"] == "no-re167-ready-row" for row in rows)

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-167 readiness gate consumed" in story_text
    assert "No-patch source gate emitted" in story_text
    assert "source patch readiness: `blocked`" in story_text
    assert "marker change readiness: `blocked`" in story_text
    assert "RE-169" in story_text
    assert "No production source or marker change was made" in story_text

    handoff_text = written["handoff_csv"].read_text(encoding="utf-8")
    assert "RE-169" in handoff_text
    assert "module-spec-psxpc-n-next-cluster-selection" in handoff_text
    assert "ui-text-rendering-source-patch-denied" in handoff_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "pay" + "load" not in text
        assert "op" + "code" not in text
        assert "raw" + " call target" not in text
        assert "machine" + " word" not in text
        assert "0x" not in text
