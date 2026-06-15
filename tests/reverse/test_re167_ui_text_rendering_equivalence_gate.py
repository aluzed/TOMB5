from pathlib import Path
import csv

from scripts.reverse.re167_ui_text_rendering_equivalence_gate import (
    build_ui_text_rendering_equivalence_gate,
    write_all_artifacts,
)


def test_re167_consumes_re166_contract_and_keeps_readiness_blocked():
    repo = Path(__file__).resolve().parents[2]
    audit = build_ui_text_rendering_equivalence_gate(repo)

    assert audit.story_id == "RE-167"
    assert audit.upstream_ticket == "RE-166"
    assert audit.cluster == "ui-text-rendering"
    assert audit.next_ticket == "RE-168"
    assert audit.contract_count == 9
    assert audit.code_change_ready_count == 0
    assert audit.marker_ready_count == 0
    assert len(audit.readiness_rows) == 9
    assert all(row.source_evidence == "source-contract-only" for row in audit.readiness_rows)
    assert all(row.binary_evidence == "non-raw-symbolic-evidence-missing" for row in audit.readiness_rows)
    assert all(row.equivalence_status == "blocked-missing-ui-text-rendering-non-raw-symbolic-equivalence-proof" for row in audit.readiness_rows)
    assert all(row.code_change_ready == "no" for row in audit.readiness_rows)
    assert all(row.marker_ready == "no" for row in audit.readiness_rows)
    assert all(row.source_patch_allowed == "no" for row in audit.readiness_rows)
    assert all(row.marker_change_allowed == "no" for row in audit.readiness_rows)

    by_id = {row.contract_id: row for row in audit.readiness_rows}
    scale = by_id["ui-text-printstring-scale-flag-lifecycle"]
    assert scale.function == "PrintString"
    assert scale.state_surface == "scale-flag-state"
    assert scale.required_symbolic_proof == "scale lifetime and per-call isolation proof"

    draw = by_id["ui-text-drawchar-draw-buffer-contract"]
    assert draw.function == "DrawChar"
    assert draw.state_surface == "draw-buffer-state"
    assert draw.required_symbolic_proof == "draw-buffer side effects and ordering-table insertion proof"
    assert draw.next_action == "defer-source-and-marker-patch-to-re168-no-patch-gate"


def test_re167_outputs_metadata_only_readiness_gate_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_ui_text_rendering_equivalence_gate(repo)
    written = write_all_artifacts(audit, tmp_path)

    rows = list(csv.DictReader(written["readiness_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == 9
    assert all(row["code_change_ready"] == "no" for row in rows)
    assert all(row["marker_ready"] == "no" for row in rows)
    assert all(row["binary_evidence"] == "non-raw-symbolic-evidence-missing" for row in rows)
    assert any(row["contract_id"] == "ui-text-getstringlength-bounds-output-contract" and row["required_symbolic_proof"] == "nullable output pointer behavior proof" for row in rows)

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-166 state contract consumed" in story_text
    assert "equivalence readiness matrix emitted" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "marker readiness: `blocked`" in story_text
    assert "RE-168" in story_text
    assert "RE-169" in story_text
    assert "No production source or marker change is authorized" in story_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "pay" + "load" not in text
        assert "op" + "code" not in text
        assert "raw" + " call target" not in text
        assert "machine" + " word" not in text
        assert "0x" not in text
