from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.saveleveldata_restore_side_audit import (
    build_restore_side_audit,
    write_csv,
    write_markdown,
)


def test_restore_side_audit_detects_unimplemented_restore_and_blocks_patch_readiness():
    audit = build_restore_side_audit(
        repo=ROOT,
        source=ROOT / "GAME/SAVEGAME.C",
        field_width_csv=ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv",
    )

    assert audit.restore_function_status == "source-unimplemented"
    assert audit.total_hypotheses == 57
    assert audit.priority_hypotheses == 34
    assert audit.patch_ready_count == 0
    assert audit.status == "restore-side-proof-missing"
    assert audit.restore_status_counts["needs-original-restore-proof"] >= 1
    assert audit.restore_status_counts["restore-source-absent"] >= 1


def test_restore_side_audit_prioritizes_re017_findings_with_explicit_statuses():
    audit = build_restore_side_audit(
        repo=ROOT,
        source=ROOT / "GAME/SAVEGAME.C",
        field_width_csv=ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv",
    )
    rows = {(row.original_group, row.call_ordinal): row for row in audit.rows}

    assert rows[(4, 11)].probable_source_field == "item->current_anim_state"
    assert rows[(4, 11)].restore_side_status == "restore-width-unverifiable"
    assert rows[(4, 11)].next_action == "derive original RestoreLevelData read width before changing source"
    assert rows[(5, 2)].restore_side_status == "restore-source-absent"
    assert rows[(5, 9)].restore_side_status == "needs-original-restore-proof"
    assert rows[(8, 2)].restore_side_status == "needs-original-restore-proof"
    assert rows[(10, 7)].restore_side_status == "restore-layout-unverifiable"


def test_restore_side_outputs_are_metadata_only_and_state_no_markers(tmp_path):
    audit = build_restore_side_audit(
        repo=ROOT,
        source=ROOT / "GAME/SAVEGAME.C",
        field_width_csv=ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv",
    )
    csv_out = tmp_path / "restore-side.csv"
    md_out = tmp_path / "restore-side.md"
    write_csv(audit, csv_out)
    write_markdown(audit, md_out)

    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")
    assert "## Progress tracker" in md_text
    assert "restore-side-proof-missing" in md_text
    assert "Do not add `(F)`, `(D)`, or `(**)`" in md_text
    forbidden = ("instruction", "word_le_hex", "payload_offset", "jal 0x")
    for text in (csv_text, md_text):
        for token in forbidden:
            assert token not in text
