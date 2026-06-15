from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.restoreleveldata_room_split_predicate_proof import (
    build_restoreleveldata_room_split_predicate_proof,
    write_csv,
    write_markdown,
)


PLAN_CSV = ROOT / "docs/reverse/generated/restoreleveldata-implementation-plan.csv"
RECONCILIATION_CSV = ROOT / "docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv"
FIELD_WIDTH_CSV = ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv"
CONTROL_FLOW_CSV = ROOT / "docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv"
BRANCH_CSV = ROOT / "docs/reverse/generated/restoreleveldata-branch-predicate-map.csv"


def build_proof():
    return build_restoreleveldata_room_split_predicate_proof(
        repo=ROOT,
        implementation_plan_csv=PLAN_CSV,
        reconciliation_csv=RECONCILIATION_CSV,
        field_width_csv=FIELD_WIDTH_CSV,
        control_flow_csv=CONTROL_FLOW_CSV,
        branch_predicate_csv=BRANCH_CSV,
    )


def test_room_split_predicate_proof_targets_re024_groups_and_keeps_code_blocked():
    proof = build_proof()

    assert proof.target_save_groups == (10, 4)
    assert proof.status == "restoreleveldata-room-split-proof-partial"
    assert proof.code_change_ready_count == 0
    rows = {row.save_original_group: row for row in proof.rows}

    assert rows[10].restore_groups == "9"
    assert rows[10].proof_focus == "room-layout-window"
    assert rows[10].field_width_profile == "exact-field-width-match=6;source-layout-mismatch=1"
    assert rows[10].restore_shape == "exact-size-window"
    assert rows[10].proof_verdict == "room-layout-predicate-unproven"
    assert rows[10].next_action == "model room byte placement and optional rotation predicate before source patch"
    assert rows[10].code_change_readiness == "blocked"

    assert rows[4].restore_groups == "4;5"
    assert rows[4].proof_focus == "active-item-split-predicate"
    assert rows[4].field_width_profile == "exact-field-width-match=14;source-width-mismatch=3"
    assert rows[4].restore_shape == "control-flow-split-candidate"
    assert rows[4].proof_verdict == "split-predicate-and-anim-width-unproven"
    assert "anim-state byte-vs-word restore predicate" in rows[4].blocking_predicates
    assert rows[4].code_change_readiness == "blocked"


def test_room_split_predicate_proof_outputs_are_metadata_only(tmp_path):
    proof = build_proof()
    csv_out = tmp_path / "restoreleveldata-room-split-predicate-proof.csv"
    md_out = tmp_path / "restoreleveldata-room-split-predicate-proof.md"

    write_csv(proof, csv_out)
    write_markdown(proof, md_out)

    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")
    assert "Story: `docs/stories/RE-024-restoreleveldata-room-split-predicate-proof.md`" in md_text
    assert "code-change-ready groups: `0`" in md_text
    assert "Do not patch `GAME/SAVEGAME.C`" in md_text
    assert "RE-025" in md_text

    forbidden = ("instruction", "word_le_hex", "payload_offset", "jal 0x", "0x800")
    for text in (csv_text, md_text):
        for token in forbidden:
            assert token not in text
