from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.restoreleveldata_field_control_flow_proof import (
    build_restore_field_control_flow_proof,
    write_csv,
    write_markdown,
)


def test_restore_field_control_flow_proof_covers_priority_groups_with_blocking_statuses():
    proof = build_restore_field_control_flow_proof(
        repo=ROOT,
        field_width_csv=ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv",
        restore_call_map_csv=ROOT / "docs/reverse/generated/restoreleveldata-read-call-map.csv",
    )

    assert proof.priority_groups == (4, 5, 8, 10)
    assert proof.status == "restore-field-control-flow-proof-partial"
    assert proof.patch_ready_count == 0
    rows = {row.save_original_group: row for row in proof.rows}
    assert rows[4].proof_status == "control-flow-split-candidate"
    assert rows[4].restore_group_candidates == "4;5"
    assert rows[5].proof_status == "rare-payload-anchor"
    assert rows[5].restore_group_candidates == "6"
    assert rows[8].proof_status == "rare-payload-anchor"
    assert rows[8].restore_group_candidates == "8"
    assert rows[10].proof_status == "exact-size-window"
    assert rows[10].restore_group_candidates == "9"
    assert all(row.patch_readiness == "blocked" for row in proof.rows)


def test_restore_field_control_flow_proof_records_rare_payload_and_gap_limits():
    proof = build_restore_field_control_flow_proof(
        repo=ROOT,
        field_width_csv=ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv",
        restore_call_map_csv=ROOT / "docs/reverse/generated/restoreleveldata-read-call-map.csv",
    )
    rows = {row.save_original_group: row for row in proof.rows}

    assert rows[5].rare_payload_anchors == "24,20"
    assert rows[5].gap_summary == "source-missing-field=14;exact-field-width-match=1"
    assert "object payload anchors exist on restore side" in rows[5].proof_limit
    assert rows[8].rare_payload_anchors == "20,4"
    assert rows[8].gap_summary == "source-missing-field=5;exact-field-width-match=5;source-layout-mismatch=2"
    assert rows[10].rare_payload_anchors == "none"
    assert "exact size window is not predicate proof" in rows[10].proof_limit


def test_restore_field_control_flow_outputs_are_metadata_only(tmp_path):
    proof = build_restore_field_control_flow_proof(
        repo=ROOT,
        field_width_csv=ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv",
        restore_call_map_csv=ROOT / "docs/reverse/generated/restoreleveldata-read-call-map.csv",
    )
    csv_out = tmp_path / "restore-field-proof.csv"
    md_out = tmp_path / "restore-field-proof.md"
    write_csv(proof, csv_out)
    write_markdown(proof, md_out)

    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")
    assert "Story: `docs/stories/RE-020-restoreleveldata-field-control-flow-proof.md`" in md_text
    assert "patch-ready groups: `0`" in md_text
    assert "Do not patch `GAME/SAVEGAME.C`" in md_text
    forbidden = ("instruction", "word_le_hex", "payload_offset", "jal 0x")
    for text in (csv_text, md_text):
        for token in forbidden:
            assert token not in text
