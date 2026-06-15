from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.restoreleveldata_field_predicate_reconciliation import (
    build_restore_field_predicate_reconciliation,
    write_csv,
    write_markdown,
)


def test_restore_field_predicate_reconciliation_covers_priority_save_groups():
    reconciliation = build_restore_field_predicate_reconciliation(
        repo=ROOT,
        field_width_csv=ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv",
        field_control_flow_csv=ROOT / "docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv",
        branch_predicate_csv=ROOT / "docs/reverse/generated/restoreleveldata-branch-predicate-map.csv",
    )

    assert reconciliation.save_groups_covered == (4, 5, 8, 10)
    assert reconciliation.status == "restore-field-predicate-reconciliation-partial"
    assert reconciliation.patch_ready_count == 0
    rows = {row.save_original_group: row for row in reconciliation.rows}
    assert rows[4].restore_groups == "4;5"
    assert rows[5].restore_groups == "6"
    assert rows[8].restore_groups == "8"
    assert rows[10].restore_groups == "9"
    assert all(row.patch_readiness == "blocked" for row in reconciliation.rows)


def test_restore_field_predicate_reconciliation_records_field_and_predicate_limits():
    reconciliation = build_restore_field_predicate_reconciliation(
        repo=ROOT,
        field_width_csv=ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv",
        field_control_flow_csv=ROOT / "docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv",
        branch_predicate_csv=ROOT / "docs/reverse/generated/restoreleveldata-branch-predicate-map.csv",
    )
    rows = {row.save_original_group: row for row in reconciliation.rows}

    assert rows[4].matched_field_count == 14
    assert rows[4].unresolved_field_count == 3
    assert rows[4].source_predicate_summary == "obj->save_position;obj->save_anim;word-bit optional x_rot/z_rot/speed/fallspeed;lara anim variant;obj->save_hitpoints"
    assert rows[4].unresolved_predicates == "anim-state byte-vs-word restore predicate;split restore groups 4+5"
    assert rows[4].proof_status == "field-identity-partial-predicate-blocked"

    assert rows[5].matched_field_count == 1
    assert rows[5].unresolved_field_count == 14
    assert rows[5].source_predicate_summary == "obj->save_flags;word-bit item_flags/timer/trigger_flags;object extension payload"
    assert rows[5].unresolved_predicates == "item_flags[0..3] payload;timer payload;trigger_flags payload;object-specific 24/20-byte payload blocks"
    assert rows[5].proof_status == "payload-predicate-missing"

    assert rows[8].matched_field_count == 5
    assert rows[8].unresolved_field_count == 7
    assert rows[8].proof_status == "layout-and-predicate-mismatch"
    assert "extra restore bytes" in rows[8].proof_limit

    assert rows[10].matched_field_count == 6
    assert rows[10].unresolved_field_count == 1
    assert rows[10].proof_status == "exact-window-field-partial"
    assert rows[10].unresolved_predicates == "room byte order/layout predicate"


def test_restore_field_predicate_reconciliation_outputs_are_metadata_only(tmp_path):
    reconciliation = build_restore_field_predicate_reconciliation(
        repo=ROOT,
        field_width_csv=ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv",
        field_control_flow_csv=ROOT / "docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv",
        branch_predicate_csv=ROOT / "docs/reverse/generated/restoreleveldata-branch-predicate-map.csv",
    )
    csv_out = tmp_path / "restore-field-predicate.csv"
    md_out = tmp_path / "restore-field-predicate.md"
    write_csv(reconciliation, csv_out)
    write_markdown(reconciliation, md_out)

    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")
    assert "Story: `docs/stories/RE-022-restoreleveldata-field-predicate-reconciliation.md`" in md_text
    assert "patch-ready groups: `0`" in md_text
    assert "Do not patch `GAME/SAVEGAME.C`" in md_text
    forbidden = ("instruction", "word_le_hex", "payload_offset", "jal 0x", "0x800")
    for text in (csv_text, md_text):
        for token in forbidden:
            assert token not in text
