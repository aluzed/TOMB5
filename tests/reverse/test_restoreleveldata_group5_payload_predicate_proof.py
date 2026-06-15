from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.restoreleveldata_group5_payload_predicate_proof import (
    build_restoreleveldata_group5_payload_predicate_proof,
    write_csv,
    write_markdown,
)


PLAN_CSV = ROOT / "docs/reverse/generated/restoreleveldata-implementation-plan.csv"
RECONCILIATION_CSV = ROOT / "docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv"
FIELD_WIDTH_CSV = ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv"
CONTROL_FLOW_CSV = ROOT / "docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv"
BRANCH_CSV = ROOT / "docs/reverse/generated/restoreleveldata-branch-predicate-map.csv"


def build_proof():
    return build_restoreleveldata_group5_payload_predicate_proof(
        repo=ROOT,
        implementation_plan_csv=PLAN_CSV,
        reconciliation_csv=RECONCILIATION_CSV,
        field_width_csv=FIELD_WIDTH_CSV,
        control_flow_csv=CONTROL_FLOW_CSV,
        branch_predicate_csv=BRANCH_CSV,
    )


def test_group5_payload_predicate_proof_keeps_restoreleveldata_code_blocked():
    proof = build_proof()

    assert proof.target_save_group == 5
    assert proof.restore_group == "6"
    assert proof.status == "restoreleveldata-group5-payload-proof-blocked"
    assert proof.code_change_ready_count == 0
    assert proof.payload_rows == 5
    rows = {row.payload_family: row for row in proof.rows}

    assert rows["packed-status-flags"].save_payload_profile == "exact-field-width-match=1;bytes=4"
    assert rows["packed-status-flags"].source_predicate_profile == "obj->save_flags guarded packed status word"
    assert rows["packed-status-flags"].proof_verdict == "source-backed-anchor-only"

    assert rows["item_flags[0..3]"].save_payload_profile == "source-missing-field=4;bytes=8"
    assert rows["item_flags[0..3]"].source_predicate_profile == "header-bit predicates visible; separate payload writes absent"
    assert rows["item_flags[0..3]"].proof_verdict == "payload-body-predicate-unproven"
    assert "four item flag payload words" in rows["item_flags[0..3]"].next_action

    assert rows["timer"].save_payload_profile == "source-missing-field=1;bytes=2"
    assert rows["timer"].proof_verdict == "payload-body-predicate-unproven"
    assert rows["trigger_flags"].save_payload_profile == "source-missing-field=1;bytes=2"
    assert rows["trigger_flags"].proof_verdict == "payload-body-predicate-unproven"

    assert rows["object-extension"].save_payload_profile == "source-missing-field=8;bytes=56;rare-blocks=24,20"
    assert rows["object-extension"].restore_payload_profile == "rare-payload-anchor;restore-size-sequence=24,2,2,2,2,2,20,1"
    assert rows["object-extension"].proof_verdict == "object-extension-predicate-unproven"
    assert rows["object-extension"].recommended_next_ticket == "RE-026"

    for row in proof.rows:
        assert row.code_change_readiness == "blocked"


def test_group5_payload_predicate_outputs_are_metadata_only(tmp_path):
    proof = build_proof()
    csv_out = tmp_path / "restoreleveldata-group5-payload-predicate-proof.csv"
    md_out = tmp_path / "restoreleveldata-group5-payload-predicate-proof.md"

    write_csv(proof, csv_out)
    write_markdown(proof, md_out)

    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")
    assert "Story: `docs/stories/RE-025-restoreleveldata-group5-payload-predicate-proof.md`" in md_text
    assert "target save group: `5`" in md_text
    assert "payload rows: `5`" in md_text
    assert "code-change-ready payload families: `0`" in md_text
    assert "Do not patch `GAME/SAVEGAME.C`" in md_text
    assert "Recommended next ticket: RE-026" in md_text

    forbidden = ("instruction", "word_le_hex", "payload_offset", "jal 0x", "0x800")
    for text in (csv_text, md_text):
        for token in forbidden:
            assert token not in text
