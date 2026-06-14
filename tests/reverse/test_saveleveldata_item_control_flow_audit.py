from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.saveleveldata_item_control_flow_audit import (
    build_item_control_flow_audit,
    write_csv,
    write_markdown,
)


def test_item_control_flow_audit_compares_original_size_sequences_to_source_cases():
    audit = build_item_control_flow_audit(
        repo=ROOT,
        original_dump=ROOT / "build/reverse/re007/original/SaveLevelData_80053f10.csv",
        item_flag_csv=ROOT / "docs/reverse/generated/saveleveldata-item-flag-audit.csv",
        write_sg_address="0x80053b04",
    )

    assert audit.total_item_groups == 9
    assert audit.exact_match_groups == (12,)
    assert audit.mismatch_groups == (4, 5, 6, 7, 8, 9, 10, 11)
    assert audit.status == "control-flow-gaps-found"


def test_item_control_flow_rows_keep_metadata_only_and_show_mismatch_reasons():
    audit = build_item_control_flow_audit(
        repo=ROOT,
        original_dump=ROOT / "build/reverse/re007/original/SaveLevelData_80053f10.csv",
        item_flag_csv=ROOT / "docs/reverse/generated/saveleveldata-item-flag-audit.csv",
        write_sg_address="0x80053b04",
    )
    rows = {row.original_group: row for row in audit.rows}

    assert rows[4].original_call_count == 17
    assert rows[4].control_flow_status == "size-sequence-mismatch"
    assert rows[4].original_size_sequence.startswith("2,2,2,2,1")
    assert "no exact source size sequence" in rows[4].notes
    assert rows[12].control_flow_status == "exact-size-sequence-match"
    assert "save_anim=lara" in rows[12].matching_source_cases
    assert all("instruction" not in line for row in audit.rows for line in row.versionable_lines())
    assert all("word_le_hex" not in line for row in audit.rows for line in row.versionable_lines())
    assert all("payload_offset" not in line for row in audit.rows for line in row.versionable_lines())


def test_item_control_flow_outputs_progress_tracker_and_no_original_instructions(tmp_path):
    audit = build_item_control_flow_audit(
        repo=ROOT,
        original_dump=ROOT / "build/reverse/re007/original/SaveLevelData_80053f10.csv",
        item_flag_csv=ROOT / "docs/reverse/generated/saveleveldata-item-flag-audit.csv",
        write_sg_address="0x80053b04",
    )
    csv_out = tmp_path / "item-control-flow.csv"
    md_out = tmp_path / "item-control-flow.md"

    write_csv(audit, csv_out)
    write_markdown(audit, md_out)
    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")

    assert "## Progress tracker" in md_text
    assert "exact-match groups: `12`" in md_text
    assert "mismatch groups: `4, 5, 6, 7, 8, 9, 10, 11`" in md_text
    assert "status: `control-flow-gaps-found`" in md_text
    assert "jal 0x80053b04" not in md_text
    assert "instruction" not in csv_text
    assert "word_le_hex" not in csv_text
    assert "payload_offset" not in csv_text
