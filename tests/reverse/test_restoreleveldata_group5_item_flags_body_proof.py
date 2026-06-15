from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.restoreleveldata_group5_item_flags_body_proof import (
    build_restoreleveldata_group5_item_flags_body_proof,
    write_csv,
    write_markdown,
)


CHECKLIST_CSV = ROOT / "docs/reverse/generated/restoreleveldata-group5-source-field-identity-checklist.csv"
FIELD_WIDTH_CSV = ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv"
READ_MAP_CSV = ROOT / "docs/reverse/generated/restoreleveldata-read-call-map.csv"
BRANCH_MAP_CSV = ROOT / "docs/reverse/generated/restoreleveldata-branch-predicate-map.csv"
SOURCE_FILE = ROOT / "GAME/SAVEGAME.C"


def build_proof():
    return build_restoreleveldata_group5_item_flags_body_proof(
        repo=ROOT,
        checklist_csv=CHECKLIST_CSV,
        field_width_csv=FIELD_WIDTH_CSV,
        read_map_csv=READ_MAP_CSV,
        branch_map_csv=BRANCH_MAP_CSV,
        source_file=SOURCE_FILE,
    )


def test_item_flags_body_proof_tracks_each_flag_and_keeps_patch_blocked():
    proof = build_proof()

    assert proof.story_id == "RE-029"
    assert proof.target_save_group == 5
    assert proof.restore_group == 6
    assert proof.payload_family == "item_flags[0..3]"
    assert proof.source_inputs == ("RE-017", "RE-021", "RE-028", "GAME/SAVEGAME.C")
    assert proof.rows_count == 4
    assert proof.patch_ready_count == 0
    assert proof.status == "restoreleveldata-group5-item-flags-body-proof-blocked"

    rows = {row.flag_index: row for row in proof.rows}
    assert set(rows) == {0, 1, 2, 3}

    expected_masks = {0: "0x80", 1: "0x100", 2: "0x200", 3: "0x400"}
    for index, mask in expected_masks.items():
        row = rows[index]
        assert row.payload_field == f"item->item_flags[{index}] payload"
        assert row.header_predicate == f"item->item_flags[{index}] -> word bit {mask}"
        assert row.source_body_evidence == "no separate Write site in current source"
        assert row.save_payload_width == 2
        assert row.restore_candidate_width == 2
        assert row.restore_candidate_context == "restore group 6 compact branch payload cluster"
        assert row.body_order_status == "candidate-width-only"
        assert row.proof_status == "payload-body-identity-missing"
        assert row.code_change_readiness == "blocked"
        assert row.safe_next_action == "do not patch; recover source/restore assignment identity before serializer edit"
        assert row.recommended_next_ticket == "RE-030"


def test_item_flags_body_outputs_are_metadata_only(tmp_path):
    proof = build_proof()
    csv_out = tmp_path / "restoreleveldata-group5-item-flags-body-proof.csv"
    md_out = tmp_path / "restoreleveldata-group5-item-flags-body-proof.md"

    write_csv(proof, csv_out)
    write_markdown(proof, md_out)

    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")

    assert "Story: `docs/stories/RE-029-restoreleveldata-group5-item-flags-body-proof.md`" in md_text
    assert "payload family: `item_flags[0..3]`" in md_text
    assert "patch-ready rows: `0`" in md_text
    assert "do not patch `GAME/SAVEGAME.C`" in md_text
    assert "Recommended next ticket: RE-030" in md_text
    assert "item_flags[3]" in csv_text
    assert "candidate-width-only" in csv_text

    forbidden = ("instruction", "word_le_hex", "payload_offset", "jal 0x", "0x800", "call_address")
    for text in (csv_text, md_text):
        for token in forbidden:
            assert token not in text
