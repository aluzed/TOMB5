from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.restoreleveldata_read_call_map import (
    build_restore_read_call_map,
    write_csv,
    write_markdown,
)


def test_restore_read_call_map_extracts_readsg_groups_and_size_sequences():
    mapping = build_restore_read_call_map(
        repo=ROOT,
        original_dump=ROOT / "build/reverse/re007/original/RestoreLevelData_80054f6c.csv",
        field_width_csv=ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv",
        read_sg_address="0x80053b44",
    )

    assert mapping.total_read_sg_calls == 79
    assert len(mapping.restore_groups) == 10
    assert mapping.status == "restore-size-proof-partial"
    first = mapping.restore_groups[0]
    assert first.group_id == 1
    assert first.call_count == 9
    assert first.size_sequence == "4,4,2,2,4,4,4,136,1"
    assert mapping.restore_groups[5].size_sequence == "24,2,2,2,2,2,20,1"


def test_restore_read_call_map_compares_re017_item_sequences_to_restore_metadata():
    mapping = build_restore_read_call_map(
        repo=ROOT,
        original_dump=ROOT / "build/reverse/re007/original/RestoreLevelData_80054f6c.csv",
        field_width_csv=ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv",
        read_sg_address="0x80053b44",
    )
    rows = {row.save_original_group: row for row in mapping.comparison_rows}

    assert set(rows) == {4, 5, 6, 7, 8, 9, 10, 11}
    assert rows[4].restore_match_status == "no-exact-restore-size-sequence"
    assert rows[4].restore_match_locations == "none"
    assert rows[5].restore_match_status == "no-exact-restore-size-sequence"
    assert rows[7].restore_match_status == "ambiguous-single-byte-restore-matches"
    assert rows[10].restore_match_status == "exact-restore-size-subsequence-match"
    assert rows[10].restore_match_locations == "restore_group=9:call_ordinal=2"
    assert mapping.patch_ready_count == 0


def test_restore_read_call_map_outputs_are_metadata_only_and_keep_marker_limits(tmp_path):
    mapping = build_restore_read_call_map(
        repo=ROOT,
        original_dump=ROOT / "build/reverse/re007/original/RestoreLevelData_80054f6c.csv",
        field_width_csv=ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv",
        read_sg_address="0x80053b44",
    )
    csv_out = tmp_path / "restore-read-map.csv"
    md_out = tmp_path / "restore-read-map.md"
    write_csv(mapping, csv_out)
    write_markdown(mapping, md_out)

    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")
    assert "## Progress tracker" in md_text
    assert "restore-size-proof-partial" in md_text
    assert "Do not add `(F)`, `(D)`, or `(**)`" in md_text
    forbidden = ("instruction", "word_le_hex", "payload_offset", "jal 0x")
    for text in (csv_text, md_text):
        for token in forbidden:
            assert token not in text
