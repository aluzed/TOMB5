from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.saveleveldata_item_flag_audit import (
    build_item_flag_audit,
    write_csv,
    write_markdown,
)


def test_item_flag_audit_models_current_source_write_count_cases():
    audit = build_item_flag_audit(
        repo=ROOT,
        call_map_csv=ROOT / "docs/reverse/generated/saveleveldata-write-call-map.csv",
        source=ROOT / "GAME" / "SAVEGAME.C",
    )

    assert audit.total_item_groups == 9
    assert audit.total_item_group_calls == 64
    assert audit.active_control_word_written is False
    assert audit.save_flags_write_sites == 0
    assert audit.possible_active_branch_counts == (0, 1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
    assert audit.unrepresented_original_groups == (4, 6)
    assert audit.status == "source-gaps-found"


def test_item_group_rows_mark_unrepresented_counts_and_keep_coordinates_only():
    audit = build_item_flag_audit(
        repo=ROOT,
        call_map_csv=ROOT / "docs/reverse/generated/saveleveldata-write-call-map.csv",
        source=ROOT / "GAME" / "SAVEGAME.C",
    )
    rows = {row.original_group: row for row in audit.rows}

    assert rows[4].original_call_count == 17
    assert rows[4].count_status == "not-representable-by-current-source-count-model"
    assert "active control word" in rows[4].notes
    assert rows[6].original_call_count == 3
    assert rows[6].count_status == "not-representable-by-current-source-count-model"
    assert rows[8].original_call_count == 12
    assert rows[8].count_status == "representable-count-needs-control-flow-proof"
    assert all("jal" not in line and "word_le_hex" not in line for row in audit.rows for line in row.versionable_lines())


def test_item_flag_audit_outputs_progress_tracker_and_no_original_instructions(tmp_path):
    audit = build_item_flag_audit(
        repo=ROOT,
        call_map_csv=ROOT / "docs/reverse/generated/saveleveldata-write-call-map.csv",
        source=ROOT / "GAME" / "SAVEGAME.C",
    )
    csv_out = tmp_path / "item-audit.csv"
    md_out = tmp_path / "item-audit.md"

    write_csv(audit, csv_out)
    write_markdown(audit, md_out)
    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")

    assert "## Progress tracker" in md_text
    assert "- [x] Model source item serialization write-count cases" in md_text
    assert "unrepresented original item groups: `4, 6`" in md_text
    assert "active control word written: `no`" in md_text
    assert "save_flags write sites: `0`" in md_text
    assert "jal 0x80053b04" not in md_text
    assert "word_le_hex" not in csv_text
    assert "payload_offset" not in csv_text
