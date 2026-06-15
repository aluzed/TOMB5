from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.restoreleveldata_branch_predicate_map import (
    build_restore_branch_predicate_map,
    write_csv,
    write_markdown,
)


def test_restore_branch_predicate_map_covers_candidate_restore_groups():
    branch_map = build_restore_branch_predicate_map(
        repo=ROOT,
        original_dump=ROOT / "build/reverse/re007/original/RestoreLevelData_80054f6c.csv",
        restore_call_map_csv=ROOT / "docs/reverse/generated/restoreleveldata-read-call-map.csv",
        field_control_flow_csv=ROOT / "docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv",
    )

    assert branch_map.restore_groups_covered == (4, 5, 6, 8, 9)
    assert branch_map.status == "restore-branch-predicate-map-partial"
    assert branch_map.patch_ready_count == 0
    rows = {row.restore_group: row for row in branch_map.rows}
    assert rows[4].linked_save_groups == "4"
    assert rows[5].linked_save_groups == "4"
    assert rows[6].linked_save_groups == "5"
    assert rows[8].linked_save_groups == "8"
    assert rows[9].linked_save_groups == "10"
    assert all(row.patch_readiness == "blocked" for row in branch_map.rows)


def test_restore_branch_predicate_map_records_relative_branch_shapes_and_hypotheses():
    branch_map = build_restore_branch_predicate_map(
        repo=ROOT,
        original_dump=ROOT / "build/reverse/re007/original/RestoreLevelData_80054f6c.csv",
        restore_call_map_csv=ROOT / "docs/reverse/generated/restoreleveldata-read-call-map.csv",
        field_control_flow_csv=ROOT / "docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv",
    )
    rows = {row.restore_group: row for row in branch_map.rows}

    assert rows[4].branch_window == "call-range±16"
    assert rows[4].branch_summary == "before:conditional-compare=2;before:unconditional-jump=1;inside:conditional-compare=4;inside:unconditional-jump=3;after:conditional-compare=2;after:unconditional-jump=1"
    assert rows[4].predicate_hypothesis == "active-item-header-and-animation-split"
    assert rows[5].branch_summary == "before:conditional-compare=1;inside:conditional-compare=11;inside:unconditional-jump=7;after:conditional-compare=2"
    assert rows[5].predicate_hypothesis == "active-item-optional-payload-fanout"
    assert rows[6].branch_summary == "before:conditional-compare=1;before:conditional-sign=1;inside:conditional-sign=1"
    assert rows[6].predicate_hypothesis == "object-payload-anchor-compact-branch"
    assert rows[8].branch_summary == "before:conditional-compare=3;inside:conditional-compare=9;inside:unconditional-jump=5;after:conditional-compare=2;after:unconditional-jump=1"
    assert rows[8].predicate_hypothesis == "object-subtype-layout-fanout"
    assert rows[9].proof_limit == "exact read-size window still lacks field predicate identity."


def test_restore_branch_predicate_outputs_are_metadata_only(tmp_path):
    branch_map = build_restore_branch_predicate_map(
        repo=ROOT,
        original_dump=ROOT / "build/reverse/re007/original/RestoreLevelData_80054f6c.csv",
        restore_call_map_csv=ROOT / "docs/reverse/generated/restoreleveldata-read-call-map.csv",
        field_control_flow_csv=ROOT / "docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv",
    )
    csv_out = tmp_path / "branch-map.csv"
    md_out = tmp_path / "branch-map.md"
    write_csv(branch_map, csv_out)
    write_markdown(branch_map, md_out)

    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")
    assert "Story: `docs/stories/RE-021-restoreleveldata-branch-predicate-map.md`" in md_text
    assert "patch-ready groups: `0`" in md_text
    assert "Do not patch `GAME/SAVEGAME.C`" in md_text
    forbidden = ("instruction", "word_le_hex", "payload_offset", "jal 0x")
    for text in (csv_text, md_text):
        for token in forbidden:
            assert token not in text
