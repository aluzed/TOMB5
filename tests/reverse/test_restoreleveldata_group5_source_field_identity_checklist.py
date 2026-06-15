from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.restoreleveldata_group5_source_field_identity_checklist import (
    build_restoreleveldata_group5_source_field_identity_checklist,
    write_csv,
    write_markdown,
)


PAYLOAD_CSV = ROOT / "docs/reverse/generated/restoreleveldata-group5-payload-predicate-proof.csv"
FIELD_WIDTH_CSV = ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv"
SOURCE_FILE = ROOT / "GAME/SAVEGAME.C"


def build_checklist():
    return build_restoreleveldata_group5_source_field_identity_checklist(
        repo=ROOT,
        payload_csv=PAYLOAD_CSV,
        field_width_csv=FIELD_WIDTH_CSV,
        source_file=SOURCE_FILE,
    )


def test_group5_source_field_identity_checklist_selects_high_value_blocked_family():
    checklist = build_checklist()

    assert checklist.status == "restoreleveldata-group5-source-field-identity-checklist-blocked"
    assert checklist.story_id == "RE-028"
    assert checklist.target_save_group == 5
    assert checklist.restore_group == 6
    assert checklist.source_inputs == ("RE-017", "RE-025", "GAME/SAVEGAME.C")
    assert checklist.rows_count == 5
    assert checklist.patch_ready_count == 0
    assert checklist.source_file == Path("GAME/SAVEGAME.C")

    rows = {row.payload_family: row for row in checklist.rows}
    assert set(rows) == {
        "packed-status-flags",
        "item_flags[0..3]",
        "timer",
        "trigger_flags",
        "object-extension",
    }

    assert rows["packed-status-flags"].checklist_status == "anchor-only"
    assert rows["packed-status-flags"].source_identity_state == "source-backed packed word; payload cluster anchor only"
    assert rows["packed-status-flags"].required_evidence == "restore packed-word assignment map; proof that following payload bodies are independent"

    assert rows["item_flags[0..3]"].field_width_summary == "source-missing-field=4;bytes=8"
    assert rows["item_flags[0..3]"].source_identity_state == "header predicates present; separate payload writes absent"
    assert rows["item_flags[0..3]"].required_evidence == "four source write sites; four restore assignments; body order predicate"
    assert rows["item_flags[0..3]"].safe_next_action == "do not patch; prove item_flags[0..3] payload bodies from source identity first"

    assert rows["timer"].required_evidence == "source write site; restore assignment; timer predicate identity"
    assert rows["trigger_flags"].required_evidence == "source write site; restore assignment; trigger_flags predicate identity"
    assert rows["object-extension"].field_width_summary == "source-missing-field=8;bytes=56;rare-blocks=24,20"
    assert rows["object-extension"].required_evidence == "object predicate map; named source fields for short/24-byte/20-byte payloads; restore assignment order"

    for row in checklist.rows:
        assert row.code_change_readiness == "blocked"
        assert row.recommended_next_ticket == "RE-029"


def test_group5_source_field_identity_outputs_are_metadata_only(tmp_path):
    checklist = build_checklist()
    csv_out = tmp_path / "restoreleveldata-group5-source-field-identity-checklist.csv"
    md_out = tmp_path / "restoreleveldata-group5-source-field-identity-checklist.md"

    write_csv(checklist, csv_out)
    write_markdown(checklist, md_out)

    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")

    assert "Story: `docs/stories/RE-028-restoreleveldata-group5-source-field-identity-checklist.md`" in md_text
    assert "target save group: `5`" in md_text
    assert "patch-ready checklist rows: `0`" in md_text
    assert "do not patch `GAME/SAVEGAME.C`" in md_text
    assert "Recommended next ticket: RE-029" in md_text
    assert "item_flags[0..3]" in csv_text
    assert "object predicate map" in csv_text

    forbidden = ("instruction", "word_le_hex", "payload_offset", "jal 0x", "0x800", "call_address")
    for text in (csv_text, md_text):
        for token in forbidden:
            assert token not in text
