from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.restoreleveldata_reconstruction_backlog import (
    build_restoreleveldata_reconstruction_backlog,
    write_all_artifacts,
)


def test_reconstruction_backlog_covers_re031_through_re037_with_explicit_readiness():
    backlog = build_restoreleveldata_reconstruction_backlog(ROOT)

    assert tuple(ticket.story_id for ticket in backlog.tickets) == (
        "RE-031",
        "RE-032",
        "RE-033",
        "RE-034",
        "RE-035",
        "RE-036",
        "RE-037",
    )
    assert backlog.status == "restoreleveldata-reconstruction-backlog-blocked"
    assert backlog.code_change_ready_count == 0
    assert backlog.patch_scope_decision == "documentation-only-no-source-patch"

    tickets = {ticket.story_id: ticket for ticket in backlog.tickets}
    assert tickets["RE-031"].topic == "limited-restoreleveldata-reconstruction-scope"
    assert tickets["RE-031"].decision == "exclude-blocked-groups-from-source-scope"
    assert tickets["RE-031"].depends_on == ("RE-027", "RE-030")
    assert tickets["RE-031"].next_ticket == "RE-032"

    assert tickets["RE-032"].topic == "group10-room-byte-order-layout-predicate"
    assert tickets["RE-032"].target_save_groups == (10,)
    assert tickets["RE-032"].blockers == ("room byte order/layout predicate",)

    assert tickets["RE-033"].topic == "group4-active-item-split-restore-predicates"
    assert tickets["RE-033"].target_save_groups == (4,)
    assert tickets["RE-033"].blockers == (
        "anim-state byte-vs-word restore predicate",
        "split restore groups 4+5",
    )

    assert tickets["RE-034"].topic == "non-raw-restore-assignment-identity-method"
    assert tickets["RE-034"].decision == "method-defined-but-no-identities-recovered"
    assert "no raw opcodes" in tickets["RE-034"].safety_contract

    assert tickets["RE-035"].topic == "group5-safe-assignment-identity-retry"
    assert tickets["RE-035"].target_save_groups == (5,)
    assert tickets["RE-035"].blockers == (
        "packed-status-flags assignment identity",
        "item_flags[0..3] assignment identity and body order",
        "timer assignment identity",
        "trigger_flags assignment identity",
        "object-extension target fields and assignment order",
    )

    assert tickets["RE-036"].topic == "group8-subtype-layout-fanout-readiness"
    assert tickets["RE-036"].target_save_groups == (8,)
    assert "group5 item flag payload dependency" in tickets["RE-036"].blockers

    assert tickets["RE-037"].topic == "partial-patch-readiness-matrix"
    assert tickets["RE-037"].decision == "no-partial-patch-ready"
    assert tickets["RE-037"].next_ticket == "RE-038"

    for ticket in backlog.tickets:
        assert ticket.status == "Done"
        assert ticket.progress == (
            "input-artifacts-loaded",
            "metadata-only-decision-published",
            "source-patch-readiness-evaluated",
            "forbidden-raw-evidence-excluded",
        )
        assert ticket.code_change_readiness == "blocked"


def test_reconstruction_backlog_outputs_are_metadata_only_and_write_expected_files(tmp_path):
    backlog = build_restoreleveldata_reconstruction_backlog(ROOT)
    written = write_all_artifacts(backlog, tmp_path)

    assert written["csv"].name == "restoreleveldata-reconstruction-backlog-re031-re037.csv"
    assert written["md"].name == "restoreleveldata-reconstruction-backlog-re031-re037.md"
    assert len(written["stories"]) == 7

    csv_text = written["csv"].read_text(encoding="utf-8")
    md_text = written["md"].read_text(encoding="utf-8")
    story_texts = [path.read_text(encoding="utf-8") for path in written["stories"]]

    assert "RE-031,limited-restoreleveldata-reconstruction-scope" in csv_text
    assert "RE-037,partial-patch-readiness-matrix" in csv_text
    assert "## Progress tracker" in md_text
    assert "code-change-ready tickets: `0`" in md_text
    assert "Do not patch `GAME/SAVEGAME.C`" in md_text
    assert "Recommended next ticket: RE-038" in md_text

    for text in story_texts:
        assert "Status: Done" in text
        assert "## Progress" in text
        assert "- [x] Input artifacts loaded." in text
        assert "## Readiness decision" in text

    forbidden = (
        "word_" + "le_hex",
        "payload_" + "offset",
        "dump" + " row",
        "jal " + "0x",
        "call_" + "address",
        "0x" + "800",
    )
    for text in (csv_text, md_text, *story_texts):
        for token in forbidden:
            assert token not in text
