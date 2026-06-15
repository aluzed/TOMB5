from pathlib import Path
import csv

from scripts.reverse.re166_ui_text_rendering_state_contract import (
    build_ui_text_rendering_state_contract,
    write_all_artifacts,
)


def test_re166_consumes_re165_taxonomy_and_emits_state_contract_rows():
    repo = Path(__file__).resolve().parents[2]
    audit = build_ui_text_rendering_state_contract(repo)

    assert audit.story_id == "RE-166"
    assert audit.upstream_ticket == "RE-165"
    assert audit.cluster == "ui-text-rendering"
    assert audit.next_ticket == "RE-167"
    assert audit.source_taxonomy_family_count == 20
    assert audit.code_change_ready_count == 0
    assert audit.marker_ready_count == 0
    assert len(audit.contract_rows) == 9
    assert all(row.source_backing == "source-contract-only" for row in audit.contract_rows)
    assert all(row.code_change_ready == "no" for row in audit.contract_rows)
    assert all(row.marker_ready == "no" for row in audit.contract_rows)
    assert all(row.blocker == "missing-ui-text-rendering-non-raw-symbolic-equivalence-proof" for row in audit.contract_rows)

    by_id = {row.contract_id: row for row in audit.contract_rows}
    assert by_id["ui-text-printstring-scale-flag-lifecycle"].function == "PrintString"
    assert by_id["ui-text-printstring-scale-flag-lifecycle"].state_surface == "scale-flag-state"
    assert by_id["ui-text-printstring-scale-flag-lifecycle"].source_tokens == "ScaleFlag;GetStringLength;DrawChar"

    assert by_id["ui-text-getstringlength-bounds-output-contract"].function == "GetStringLength"
    assert by_id["ui-text-getstringlength-bounds-output-contract"].state_surface == "optional-bounds-output"
    assert by_id["ui-text-getstringlength-bounds-output-contract"].contract_status == "contract-documented-equivalence-blocked"

    control = by_id["ui-text-getstringlength-control-character-contract"]
    assert control.proof_input == "RE-165 GetStringLength caller-string and string-wad measurement families."
    assert "inline-control-string" not in control.proof_input

    assert by_id["ui-text-drawchar-draw-buffer-contract"].function == "DrawChar"
    assert by_id["ui-text-drawchar-draw-buffer-contract"].state_surface == "draw-buffer-state"
    assert by_id["ui-text-drawchar-draw-buffer-contract"].source_tokens == "db.polyptr;db.polybuf_limit;db.ot;FontShades;ScaleFlag"


def test_re166_outputs_metadata_only_story_and_followup(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_ui_text_rendering_state_contract(repo)
    written = write_all_artifacts(audit, tmp_path)

    rows = list(csv.DictReader(written["contract_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == 9
    assert all(row["code_change_ready"] == "no" for row in rows)
    assert all(row["marker_ready"] == "no" for row in rows)
    assert any(row["contract_id"] == "ui-text-printstring-blink-frame-gate" and row["state_surface"] == "blink-frame-counter" for row in rows)
    assert any(row["contract_id"] == "ui-text-getstringlength-font-metric-contract" and row["state_surface"] == "font-metric-state" for row in rows)

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-165 taxonomy consumed" in story_text
    assert "UI text state contract emitted" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "RE-167" in story_text
    assert "test_re166_ui_text_rendering_state_contract.py" in story_text
    assert "No production source or marker change is authorized" in story_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "pay" + "load" not in text
        assert "op" + "code" not in text
        assert "raw" + " call target" not in text
        assert "machine" + " word" not in text
        assert "0x" not in text
