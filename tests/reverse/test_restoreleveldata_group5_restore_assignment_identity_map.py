from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.restoreleveldata_group5_restore_assignment_identity_map import (
    build_restoreleveldata_group5_restore_assignment_identity_map,
    write_csv,
    write_markdown,
)


CHECKLIST_CSV = ROOT / "docs/reverse/generated/restoreleveldata-group5-source-field-identity-checklist.csv"
ITEM_FLAGS_CSV = ROOT / "docs/reverse/generated/restoreleveldata-group5-item-flags-body-proof.csv"
PAYLOAD_CSV = ROOT / "docs/reverse/generated/restoreleveldata-group5-payload-predicate-proof.csv"
READ_MAP_CSV = ROOT / "docs/reverse/generated/restoreleveldata-read-call-map.csv"
RECONCILIATION_CSV = ROOT / "docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv"
SOURCE_FILE = ROOT / "GAME/SAVEGAME.C"


def build_map():
    return build_restoreleveldata_group5_restore_assignment_identity_map(
        repo=ROOT,
        checklist_csv=CHECKLIST_CSV,
        item_flags_csv=ITEM_FLAGS_CSV,
        payload_csv=PAYLOAD_CSV,
        read_map_csv=READ_MAP_CSV,
        reconciliation_csv=RECONCILIATION_CSV,
        source_file=SOURCE_FILE,
    )


def test_restore_assignment_identity_map_covers_group5_payload_families_and_defers_patch():
    identity_map = build_map()

    assert identity_map.story_id == "RE-030"
    assert identity_map.target_save_group == 5
    assert identity_map.restore_group == 6
    assert identity_map.source_inputs == ("RE-019", "RE-022", "RE-025", "RE-028", "RE-029", "GAME/SAVEGAME.C")
    assert identity_map.rows_count == 5
    assert identity_map.assignment_identity_ready_count == 0
    assert identity_map.patch_ready_count == 0
    assert identity_map.status == "restoreleveldata-group5-restore-assignment-identity-map-blocked"
    assert identity_map.restore_source_state == "RestoreLevelData source body is UNIMPLEMENTED"
    assert identity_map.group5_decision == "defer-group5-from-source-reconstruction"

    rows = {row.payload_family: row for row in identity_map.rows}
    assert set(rows) == {
        "packed-status-flags",
        "item_flags[0..3]",
        "timer",
        "trigger_flags",
        "object-extension",
    }

    assert rows["packed-status-flags"].restore_candidate_profile == "restore group 6 compact branch payload cluster; rare anchor widths present"
    assert rows["packed-status-flags"].assignment_identity_state == "missing-restore-assignment-map"
    assert rows["packed-status-flags"].required_assignment_evidence == "named restore assignment for packed status word and independence proof for following payload bodies"

    assert rows["item_flags[0..3]"].prior_body_proof == "candidate-width-only; 4 rows; patch-ready=0"
    assert rows["item_flags[0..3]"].required_assignment_evidence == "four named restore assignments; per-flag body order; source/restore field identity"
    assert rows["item_flags[0..3]"].safe_next_action == "defer group 5 or recover assignment identities before source reconstruction"

    assert rows["timer"].required_assignment_evidence == "named restore timer assignment and predicate identity"
    assert rows["trigger_flags"].required_assignment_evidence == "named restore trigger_flags assignment and predicate identity"
    assert rows["object-extension"].required_assignment_evidence == "object-specific restore target fields; object predicate map; block assignment order"

    for row in identity_map.rows:
        assert row.restore_assignment_evidence == "no versioned restore assignment identity; current source restore body absent"
        assert row.assignment_identity_readiness == "blocked"
        assert row.code_change_readiness == "blocked"
        assert row.recommended_next_ticket == "RE-031"


def test_restore_assignment_identity_outputs_are_metadata_only(tmp_path):
    identity_map = build_map()
    csv_out = tmp_path / "restoreleveldata-group5-restore-assignment-identity-map.csv"
    md_out = tmp_path / "restoreleveldata-group5-restore-assignment-identity-map.md"

    write_csv(identity_map, csv_out)
    write_markdown(identity_map, md_out)

    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")

    assert "Story: `docs/stories/RE-030-restoreleveldata-group5-restore-assignment-identity-map.md`" in md_text
    assert "assignment-identity-ready rows: `0`" in md_text
    assert "group 5 decision: `defer-group5-from-source-reconstruction`" in md_text
    assert "do not patch `GAME/SAVEGAME.C`" in md_text
    assert "Recommended next ticket: RE-031" in md_text
    assert "object-extension" in csv_text
    assert "missing-restore-assignment-map" in csv_text

    forbidden = ("instruction", "word_le_hex", "payload_offset", "jal 0x", "0x800", "call_address")
    for text in (csv_text, md_text):
        for token in forbidden:
            assert token not in text
