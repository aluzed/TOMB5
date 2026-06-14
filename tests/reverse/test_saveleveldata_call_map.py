from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.saveleveldata_call_map import (
    build_call_group_map,
    extract_write_sg_call_groups,
    write_csv,
    write_markdown,
)


def _write_dump(path: Path, call_indices: list[int]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["index", "ram_address", "payload_offset", "word_le_hex", "instruction"],
            lineterminator="\n",
        )
        writer.writeheader()
        for index in range(max(call_indices) + 1):
            is_call = index in call_indices
            writer.writerow({
                "index": index,
                "ram_address": f"0x800540{index:02x}",
                "payload_offset": f"0x0440{index:02x}",
                "word_le_hex": f"0x{index + 0x100:08x}",
                "instruction": "jal 0x80053b04" if is_call else "nop",
            })


def test_extract_write_sg_call_groups_uses_index_gaps_without_instruction_payload(tmp_path):
    dump = tmp_path / "SaveLevelData_80053f10.csv"
    _write_dump(dump, [1, 4, 8, 40, 44])

    groups = extract_write_sg_call_groups(dump, "0x80053b04", max_gap=12)

    assert [(group.group_id, group.call_count, group.first_call_index, group.last_call_index) for group in groups] == [
        (1, 3, 1, 8),
        (2, 2, 40, 44),
    ]
    assert groups[0].first_call_address == "0x80054001"
    assert groups[1].last_call_address == "0x8005402c"
    assert all("jal" not in line and "word_le_hex" not in line for group in groups for line in group.versionable_lines())


def test_build_call_group_map_preserves_total_counts_and_candidate_source_rows():
    mapping = build_call_group_map(
        repo=ROOT,
        original_dump=ROOT / "build/reverse/re007/original/SaveLevelData_80053f10.csv",
        source=ROOT / "GAME" / "SAVEGAME.C",
        write_sg_address="0x80053b04",
        max_gap=24,
    )

    assert mapping.total_original_calls == 81
    assert mapping.total_source_sites == 34
    assert mapping.status == "candidate-map-needs-manual-audit"
    assert len(mapping.rows) >= 8
    assert any(row.candidate_source_rows == "1-9" for row in mapping.rows)
    assert any("item" in row.candidate_context.lower() for row in mapping.rows)
    assert sum(row.original_call_count for row in mapping.rows) == 81


def test_call_map_outputs_are_versionable_and_have_progress_tracker(tmp_path):
    mapping = build_call_group_map(
        repo=ROOT,
        original_dump=ROOT / "build/reverse/re007/original/SaveLevelData_80053f10.csv",
        source=ROOT / "GAME" / "SAVEGAME.C",
        write_sg_address="0x80053b04",
        max_gap=24,
    )
    csv_out = tmp_path / "map.csv"
    md_out = tmp_path / "map.md"

    write_csv(mapping, csv_out)
    write_markdown(mapping, md_out)

    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")

    assert "instruction" not in csv_text
    assert "word_le_hex" not in csv_text
    assert "jal 0x80053b04" not in md_text
    assert "## Progress tracker" in md_text
    assert "- [x] Group original `WriteSG` calls" in md_text
    assert "original `WriteSG` calls: `81`" in md_text
    assert "source `Write(...)` sites: `34`" in md_text
