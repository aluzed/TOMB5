from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.restoreleveldata_implementation_plan import (
    build_restoreleveldata_implementation_plan,
    write_csv,
    write_markdown,
)


RECONCILIATION_CSV = ROOT / "docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv"


def test_restoreleveldata_implementation_plan_covers_re022_blockers_without_patch_ready_claims():
    plan = build_restoreleveldata_implementation_plan(repo=ROOT, reconciliation_csv=RECONCILIATION_CSV)

    assert plan.save_groups_covered == (4, 5, 8, 10)
    assert plan.status == "restoreleveldata-implementation-plan-blocked"
    assert plan.patch_ready_count == 0
    assert plan.code_change_ready_count == 0
    rows = {row.save_original_group: row for row in plan.rows}

    assert rows[4].restore_groups == "4;5"
    assert rows[4].implementation_phase == "prove-split-active-item-layout"
    assert rows[4].recommended_next_ticket == "RE-024"
    assert "split restore groups 4+5" in rows[4].missing_proof
    assert rows[4].code_change_readiness == "blocked"

    assert rows[5].implementation_phase == "prove-object-extension-payloads"
    assert "item_flags[0..3] payload" in rows[5].missing_proof
    assert rows[5].minimal_safe_action == "derive source-level payload predicate checklist"

    assert rows[8].implementation_phase == "prove-object-subtype-layout-fanout"
    assert "extra restore bytes" in rows[8].missing_proof

    assert rows[10].implementation_phase == "prove-room-layout-window"
    assert rows[10].recommended_next_ticket == "RE-024"
    assert rows[10].risk_level == "medium"


def test_restoreleveldata_implementation_plan_outputs_are_metadata_only(tmp_path):
    plan = build_restoreleveldata_implementation_plan(repo=ROOT, reconciliation_csv=RECONCILIATION_CSV)
    csv_out = tmp_path / "restoreleveldata-implementation-plan.csv"
    md_out = tmp_path / "restoreleveldata-implementation-plan.md"

    write_csv(plan, csv_out)
    write_markdown(plan, md_out)

    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")
    assert "Story: `docs/stories/RE-023-restoreleveldata-implementation-plan.md`" in md_text
    assert "code-change-ready groups: `0`" in md_text
    assert "Do not patch `GAME/SAVEGAME.C`" in md_text
    assert "RE-024" in md_text

    forbidden = ("instruction", "word_le_hex", "payload_offset", "jal 0x", "0x800")
    for text in (csv_text, md_text):
        for token in forbidden:
            assert token not in text
