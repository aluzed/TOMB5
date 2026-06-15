from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.restoreleveldata_group8_layout_fanout_proof import (
    build_restoreleveldata_group8_layout_fanout_proof,
    write_csv,
    write_markdown,
)


PLAN_CSV = ROOT / "docs/reverse/generated/restoreleveldata-implementation-plan.csv"
RECONCILIATION_CSV = ROOT / "docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv"
FIELD_WIDTH_CSV = ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv"
CONTROL_FLOW_CSV = ROOT / "docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv"
BRANCH_CSV = ROOT / "docs/reverse/generated/restoreleveldata-branch-predicate-map.csv"
GROUP5_CSV = ROOT / "docs/reverse/generated/restoreleveldata-group5-payload-predicate-proof.csv"


def build_proof():
    return build_restoreleveldata_group8_layout_fanout_proof(
        repo=ROOT,
        implementation_plan_csv=PLAN_CSV,
        reconciliation_csv=RECONCILIATION_CSV,
        field_width_csv=FIELD_WIDTH_CSV,
        control_flow_csv=CONTROL_FLOW_CSV,
        branch_predicate_csv=BRANCH_CSV,
        group5_payload_csv=GROUP5_CSV,
    )


def test_group8_layout_fanout_proof_keeps_restoreleveldata_code_blocked():
    proof = build_proof()

    assert proof.target_save_group == 8
    assert proof.restore_group == "8"
    assert proof.status == "restoreleveldata-group8-layout-fanout-proof-blocked"
    assert proof.code_change_ready_count == 0
    assert proof.fanout_rows == 7
    rows = {row.fanout_family: row for row in proof.rows}

    assert rows["subtype-extra-byte"].save_payload_profile == "source-missing-field=1;bytes=1"
    assert rows["subtype-extra-byte"].restore_layout_profile == "rare-payload-anchor;restore-size-sequence=1,1,20,2,2,2,2,4,2,2,2,2,2;extra-restore-byte-candidate=1"
    assert rows["subtype-extra-byte"].proof_verdict == "subtype-and-extra-byte-predicate-unproven"

    assert rows["position-layout-block"].save_payload_profile == "source-layout-mismatch=1;bytes=20"
    assert rows["position-layout-block"].source_predicate_profile == "current source uses split position writes, not a proved twenty-byte block"
    assert rows["position-layout-block"].proof_verdict == "layout-block-predicate-unproven"

    assert rows["room-rotation-ordering"].save_payload_profile == "source-layout-mismatch=1;bytes=2"
    assert rows["room-rotation-ordering"].proof_verdict == "room-rotation-ordering-unproven"

    assert rows["speed-fallspeed"].save_payload_profile == "exact-field-width-match=2;bytes=4"
    assert rows["speed-fallspeed"].proof_verdict == "field-width-match-fanout-still-blocked"

    assert rows["item-data-word"].save_payload_profile == "source-missing-field=1;bytes=4"
    assert rows["item-data-word"].proof_verdict == "item-data-pointer-predicate-unproven"

    assert rows["item_flags[3,0,1]"].save_payload_profile == "source-missing-field=3;bytes=6"
    assert rows["item_flags[3,0,1]"].prior_group5_dependency == "group5-item-flag-payloads-blocked"
    assert rows["item_flags[3,0,1]"].proof_verdict == "item-flag-payload-predicate-unproven"

    assert rows["anim-state-payload"].save_payload_profile == "exact-field-width-match=3;bytes=6"
    assert rows["anim-state-payload"].proof_verdict == "field-width-match-fanout-still-blocked"

    for row in proof.rows:
        assert row.code_change_readiness == "blocked"
        assert row.recommended_next_ticket == "RE-027"


def test_group8_layout_fanout_outputs_are_metadata_only(tmp_path):
    proof = build_proof()
    csv_out = tmp_path / "restoreleveldata-group8-layout-fanout-proof.csv"
    md_out = tmp_path / "restoreleveldata-group8-layout-fanout-proof.md"

    write_csv(proof, csv_out)
    write_markdown(proof, md_out)

    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")
    assert "Story: `docs/stories/RE-026-restoreleveldata-group8-layout-fanout-proof.md`" in md_text
    assert "target save group: `8`" in md_text
    assert "fanout rows: `7`" in md_text
    assert "code-change-ready fanout families: `0`" in md_text
    assert "Do not patch `GAME/SAVEGAME.C`" in md_text
    assert "Recommended next ticket: RE-027" in md_text

    forbidden = ("instruction", "word_le_hex", "payload_offset", "jal 0x", "0x800")
    for text in (csv_text, md_text):
        for token in forbidden:
            assert token not in text
