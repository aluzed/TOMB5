from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.saveleveldata_item_field_width_audit import (
    build_item_field_width_audit,
    write_csv,
    write_markdown,
)


def test_item_field_width_audit_covers_re016_mismatch_groups_and_prioritizes_width_gaps():
    audit = build_item_field_width_audit(
        repo=ROOT,
        original_dump=ROOT / "build/reverse/re007/original/SaveLevelData_80053f10.csv",
        control_flow_csv=ROOT / "docs/reverse/generated/saveleveldata-item-control-flow-audit.csv",
        write_sg_address="0x80053b04",
    )

    assert audit.mismatch_groups == (4, 5, 6, 7, 8, 9, 10, 11)
    assert audit.total_original_calls == 57
    assert audit.status == "field-width-gaps-found"
    assert audit.gap_counts["source-width-mismatch"] >= 3
    assert audit.gap_counts["source-missing-field"] >= 1
    assert audit.priority_findings[0].startswith("anim-state-byte-width")


def test_item_field_width_audit_maps_group4_anim_state_byte_mismatches():
    audit = build_item_field_width_audit(
        repo=ROOT,
        original_dump=ROOT / "build/reverse/re007/original/SaveLevelData_80053f10.csv",
        control_flow_csv=ROOT / "docs/reverse/generated/saveleveldata-item-control-flow-audit.csv",
        write_sg_address="0x80053b04",
    )
    rows = {(row.original_group, row.call_ordinal): row for row in audit.rows}

    assert rows[(4, 11)].probable_source_field == "item->current_anim_state"
    assert rows[(4, 11)].original_size == 1
    assert rows[(4, 11)].source_size == 2
    assert rows[(4, 11)].gap_status == "source-width-mismatch"
    assert rows[(4, 12)].probable_source_field == "item->goal_anim_state"
    assert rows[(4, 13)].probable_source_field == "item->required_anim_state"
    assert rows[(4, 15)].probable_source_field == "item->anim_number - obj->anim_index"
    assert rows[(4, 15)].gap_status == "exact-field-width-match"


def test_item_field_width_audit_flags_unmodeled_large_original_payloads():
    audit = build_item_field_width_audit(
        repo=ROOT,
        original_dump=ROOT / "build/reverse/re007/original/SaveLevelData_80053f10.csv",
        control_flow_csv=ROOT / "docs/reverse/generated/saveleveldata-item-control-flow-audit.csv",
        write_sg_address="0x80053b04",
    )
    rows = {(row.original_group, row.call_ordinal): row for row in audit.rows}

    assert rows[(5, 9)].original_size == 24
    assert rows[(5, 9)].gap_status == "source-missing-field"
    assert "object-specific payload" in rows[(5, 9)].probable_source_field
    assert rows[(5, 15)].original_size == 20
    assert rows[(8, 2)].original_size == 20
    assert rows[(6, 2)].original_size == 4
    assert rows[(6, 2)].gap_status in {"source-missing-field", "source-layout-mismatch"}


def test_item_field_width_outputs_are_metadata_only(tmp_path):
    audit = build_item_field_width_audit(
        repo=ROOT,
        original_dump=ROOT / "build/reverse/re007/original/SaveLevelData_80053f10.csv",
        control_flow_csv=ROOT / "docs/reverse/generated/saveleveldata-item-control-flow-audit.csv",
        write_sg_address="0x80053b04",
    )
    csv_out = tmp_path / "field-width.csv"
    md_out = tmp_path / "field-width.md"
    write_csv(audit, csv_out)
    write_markdown(audit, md_out)

    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")
    assert "## Progress tracker" in md_text
    assert "anim-state-byte-width" in md_text
    assert "source-missing-field" in csv_text
    forbidden = ("instruction", "word_le_hex", "payload_offset", "jal 0x80053b04")
    for text in (csv_text, md_text):
        for token in forbidden:
            assert token not in text
