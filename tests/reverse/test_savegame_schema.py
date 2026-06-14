from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.savegame_schema import parse_save_level_data_writes


def test_parse_save_level_data_pc_write_order_has_core_fields():
    rows = parse_save_level_data_writes(ROOT / "GAME" / "SAVEGAME.C")

    assert rows[0].expression == "&FmvSceneTriggered"
    assert rows[0].size == "4"
    assert rows[1].expression == "&GLOBAL_lastinvitem"
    assert rows[1].size == "4"
    assert any(row.expression == "cd_flags" and row.size == "136" for row in rows)
    assert any(row.expression == "&CurrentSequence" and row.size == "1" for row in rows)


def test_parse_save_level_data_pc_write_order_captures_late_item_fields():
    rows = parse_save_level_data_writes(ROOT / "GAME" / "SAVEGAME.C")
    expressions = [row.expression for row in rows]

    assert "&item->pos.y_rot" in expressions
    assert "&item->frame_number" in expressions
    assert "&item->hit_points" in expressions
    assert len(rows) >= 30
