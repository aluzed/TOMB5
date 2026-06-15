from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.restoreleveldata_readiness_refresh import (
    build_restoreleveldata_readiness_refresh,
    write_csv,
    write_markdown,
)


PLAN_CSV = ROOT / "docs/reverse/generated/restoreleveldata-implementation-plan.csv"
ROOM_SPLIT_CSV = ROOT / "docs/reverse/generated/restoreleveldata-room-split-predicate-proof.csv"
GROUP5_CSV = ROOT / "docs/reverse/generated/restoreleveldata-group5-payload-predicate-proof.csv"
GROUP8_CSV = ROOT / "docs/reverse/generated/restoreleveldata-group8-layout-fanout-proof.csv"


def build_refresh():
    return build_restoreleveldata_readiness_refresh(
        repo=ROOT,
        implementation_plan_csv=PLAN_CSV,
        room_split_csv=ROOM_SPLIT_CSV,
        group5_payload_csv=GROUP5_CSV,
        group8_fanout_csv=GROUP8_CSV,
    )


def test_readiness_refresh_consolidates_re024_to_re026_and_keeps_code_blocked():
    refresh = build_refresh()

    assert refresh.status == "restoreleveldata-readiness-refresh-blocked"
    assert refresh.source_proof_inputs == ("RE-024", "RE-025", "RE-026")
    assert refresh.target_save_groups == (4, 5, 8, 10)
    assert refresh.code_change_ready_count == 0
    assert refresh.rows_count == 4
    rows = {row.save_original_group: row for row in refresh.rows}

    assert rows[4].restore_groups == "4;5"
    assert rows[4].latest_evidence == "RE-024 room/split predicate proof"
    assert rows[4].remaining_blockers == "anim-state byte-vs-word restore predicate;split restore groups 4+5"
    assert rows[4].readiness_phase == "continue-source-field-proof"
    assert rows[4].safe_next_action == "prove split active-item restore predicates before source reconstruction"

    assert rows[5].restore_groups == "6"
    assert rows[5].latest_evidence == "RE-025 group 5 payload predicate proof"
    assert rows[5].evidence_summary == "payload-families=5;blocked=5;source-backed-anchor-only=1"
    assert rows[5].remaining_blockers == "item_flags[0..3] payload bodies;timer payload body;trigger_flags payload body;object-extension field identity"
    assert rows[5].safe_next_action == "prove payload body field identities or keep group out of source patch scope"

    assert rows[8].restore_groups == "8"
    assert rows[8].latest_evidence == "RE-026 group 8 layout/fanout proof"
    assert rows[8].evidence_summary == "fanout-families=7;blocked=7;group5-dependency=group5-item-flag-payloads-blocked"
    assert rows[8].remaining_blockers == "subtype/extra byte predicate;layout block 20;room/rotation ordering;item data word;item flag payload bodies"
    assert rows[8].safe_next_action == "prove subtype/layout fanout field identities or keep group out of source patch scope"

    assert rows[10].restore_groups == "9"
    assert rows[10].latest_evidence == "RE-024 room/split predicate proof"
    assert rows[10].remaining_blockers == "room byte order/layout predicate"
    assert rows[10].safe_next_action == "prove room byte placement before source reconstruction"

    for row in refresh.rows:
        assert row.code_change_readiness == "blocked"
        assert row.recommended_next_ticket == "RE-028"


def test_readiness_refresh_outputs_are_metadata_only(tmp_path):
    refresh = build_refresh()
    csv_out = tmp_path / "restoreleveldata-readiness-refresh.csv"
    md_out = tmp_path / "restoreleveldata-readiness-refresh.md"

    write_csv(refresh, csv_out)
    write_markdown(refresh, md_out)

    csv_text = csv_out.read_text(encoding="utf-8")
    md_text = md_out.read_text(encoding="utf-8")
    assert "Story: `docs/stories/RE-027-restoreleveldata-readiness-refresh.md`" in md_text
    assert "source proof inputs: `RE-024, RE-025, RE-026`" in md_text
    assert "code-change-ready groups: `0`" in md_text
    assert "Do not patch `GAME/SAVEGAME.C`" in md_text
    assert "Recommended next ticket: RE-028" in md_text

    forbidden = ("instruction", "word_le_hex", "payload_offset", "jal 0x", "0x800")
    for text in (csv_text, md_text):
        for token in forbidden:
            assert token not in text
