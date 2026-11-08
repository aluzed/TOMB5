from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.saveleveldata_restore_side_audit import (
    build_restore_side_audit,
    write_csv,
    write_markdown,
)


def _audit():
    return build_restore_side_audit(
        repo=ROOT,
        source=ROOT / "GAME/SAVEGAME.C",
        field_width_csv=ROOT / "docs/reverse/generated/saveleveldata-item-field-width-audit.csv",
        restore_read_map_csv=ROOT / "docs/reverse/generated/restoreleveldata-read-call-map.csv",
    )


def test_restore_side_audit_detects_current_restore_state_and_blocks_patch_readiness():
    audit = _audit()

    assert audit.restore_function_status == "source-has-read-sites"
    assert audit.total_hypotheses == 57
    assert audit.priority_hypotheses == 34
    assert audit.patch_ready_count == 0
    assert audit.status == "restore-side-proof-missing"
    # implemented evidence is now present for many hypotheses, but original proof is still missing
    assert sum(audit.restore_status_counts.values()) == 57
    assert not any(status in {"ready", "patch-ready"} for status in audit.restore_status_counts)


def test_restore_side_audit_prioritizes_re017_findings_with_implemented_evidence():
    audit = _audit()
    rows = {(row.original_group, row.call_ordinal): row for row in audit.rows}

    # group 4 anim states: RE-017 original hypothesis is 1 byte, implemented restore/save read/write 2 bytes
    assert rows[(4, 11)].probable_source_field == "item->current_anim_state"
    assert rows[(4, 11)].restore_side_status == "implemented-restore-width-differs-from-original-hypothesis"
    assert "2 bytes" in rows[(4, 11)].implemented_evidence
    assert rows[(4, 11)].patch_readiness == "blocked"

    # group 5 item_flags payloads: implemented save/restore now have payload sites, but original proof is still missing
    assert rows[(5, 2)].probable_source_field == "item->item_flags[0] payload"
    assert rows[(5, 2)].restore_side_status == "implemented-restore-payload-present-needs-original-proof"
    assert "PortSave_LevelFormat" in rows[(5, 2)].implemented_evidence or "payload" in rows[(5, 2)].implemented_evidence

    # group 5 object-specific block: no implemented payload read in active item loop
    assert rows[(5, 9)].restore_side_status == "needs-original-restore-proof"
    assert "24" in (rows[(5, 9)].implemented_evidence or "") or "object-specific" in rows[(5, 9)].implemented_evidence.lower() or "block" in rows[(5, 9)].implemented_evidence.lower()

    # group 10 has RE-019 exact size subsequence match context, but layout/order remains unproven
    assert rows[(10, 7)].probable_source_field == "item->room_number"
    assert rows[(10, 7)].save_gap_status == "source-layout-mismatch"
    assert rows[(10, 7)].restore_side_status == "implemented-restore-layout-differs-from-original-hypothesis"
    assert rows[(10, 7)].re019_restore_match_status == "exact-restore-size-subsequence-match"

    # group 8 large layout block remains unproven
    assert rows[(8, 2)].restore_side_status == "needs-original-restore-proof"


def test_restore_side_outputs_are_metadata_only_and_state_no_markers(tmp_path):
    audit = _audit()
    csv_out = tmp_path / "restore-side.csv"
    md_out = tmp_path / "restore-side.md"
    write_csv(audit, csv_out)
    write_markdown(audit, md_out)

    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")
    assert "## Progress tracker" in md_text
    assert "restore-side-proof-missing" in md_text
    assert "source-has-read-sites" in md_text
    assert "Do not add `(F)`, `(D)`, or `(**)`" in md_text
    assert "RE-019" in md_text
    forbidden = ("instruction", "word_le_hex", "payload_offset", "jal 0x")
    for text in (csv_text, md_text):
        for token in forbidden:
            assert token not in text
