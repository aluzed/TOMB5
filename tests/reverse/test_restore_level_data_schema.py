from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.restore_level_data_schema import parse_restore_level_data_reads


def test_parse_restore_level_data_read_order_has_core_fields():
    rows = parse_restore_level_data_reads(ROOT / "GAME" / "SAVEGAME.C")

    assert rows[0].expression == "(char*)&FmvSceneTriggered"
    assert rows[0].size == "4"
    assert rows[1].expression == "(char*)&GLOBAL_lastinvitem"
    assert rows[1].size == "4"
    assert any(row.expression == "cd_flags" and row.size == "136" for row in rows)
    assert any(row.expression == "(char*)&CurrentSequence" and row.size == "1" for row in rows)


def test_parse_restore_level_data_read_order_captures_item_fields():
    rows = parse_restore_level_data_reads(ROOT / "GAME" / "SAVEGAME.C")
    expressions = [row.expression for row in rows]

    assert any("y_rot" in e for e in expressions)
    assert any("current_anim_state" in e for e in expressions)
    assert any("hit_points" in e for e in expressions)
    assert any(row.expression == "(char*)&byte" and row.size == "1" for row in rows)
    assert len(rows) >= 30
