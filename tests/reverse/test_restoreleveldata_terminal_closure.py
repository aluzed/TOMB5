from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.restoreleveldata_terminal_closure import (
    build_restoreleveldata_terminal_closure,
    write_all_artifacts,
)


def test_terminal_closure_covers_re038_through_re043_and_stops_the_patch_chain():
    closure = build_restoreleveldata_terminal_closure(ROOT)

    assert tuple(ticket.story_id for ticket in closure.tickets) == (
        "RE-038",
        "RE-039",
        "RE-040",
        "RE-041",
        "RE-042",
        "RE-043",
    )
    assert closure.status == "restoreleveldata-terminal-closure-no-safe-source-patch"
    assert closure.code_change_ready_count == 0
    assert closure.final_decision == "stop-restoreleveldata-source-reconstruction-chain"
    assert closure.next_ticket == "none"

    tickets = {ticket.story_id: ticket for ticket in closure.tickets}
    assert tickets["RE-038"].topic == "source-patch-gate"
    assert tickets["RE-038"].decision == "source-patch-denied-no-ready-rows"
    assert tickets["RE-038"].next_ticket == "RE-039"

    assert tickets["RE-039"].topic == "group10-terminal-blocker"
    assert tickets["RE-039"].target_save_groups == (10,)
    assert tickets["RE-039"].decision == "terminal-blocked-without-new-non-raw-evidence"

    assert tickets["RE-040"].topic == "group4-terminal-blocker"
    assert tickets["RE-040"].target_save_groups == (4,)
    assert tickets["RE-040"].decision == "terminal-blocked-without-new-non-raw-evidence"

    assert tickets["RE-041"].topic == "group5-terminal-blocker"
    assert tickets["RE-041"].target_save_groups == (5,)
    assert tickets["RE-041"].decision == "terminal-excluded-no-assignment-identities"

    assert tickets["RE-042"].topic == "group8-terminal-blocker"
    assert tickets["RE-042"].target_save_groups == (8,)
    assert tickets["RE-042"].decision == "terminal-blocked-by-layout-and-group5-dependency"

    assert tickets["RE-043"].topic == "restoreleveldata-final-stop-report"
    assert tickets["RE-043"].target_save_groups == (4, 5, 8, 10)
    assert tickets["RE-043"].decision == "no-safe-remaining-restoreleveldata-source-work"
    assert tickets["RE-043"].next_ticket == "none"

    for ticket in closure.tickets:
        assert ticket.status == "Done"
        assert ticket.code_change_readiness == "blocked"
        assert ticket.progress == (
            "input-artifacts-loaded",
            "terminal-decision-published",
            "source-patch-rejected-or-deferred",
            "forbidden-raw-evidence-excluded",
        )


def test_terminal_closure_outputs_are_metadata_only_and_mark_no_next_ticket(tmp_path):
    closure = build_restoreleveldata_terminal_closure(ROOT)
    written = write_all_artifacts(closure, tmp_path)

    assert written["csv"].name == "restoreleveldata-terminal-closure-re038-re043.csv"
    assert written["md"].name == "restoreleveldata-terminal-closure-re038-re043.md"
    assert len(written["stories"]) == 6

    csv_text = written["csv"].read_text(encoding="utf-8")
    md_text = written["md"].read_text(encoding="utf-8")
    story_texts = [path.read_text(encoding="utf-8") for path in written["stories"]]

    assert "RE-038,source-patch-gate" in csv_text
    assert "RE-043,restoreleveldata-final-stop-report" in csv_text
    assert "final decision: `stop-restoreleveldata-source-reconstruction-chain`" in md_text
    assert "next ticket: `none`" in md_text
    assert "code-change-ready tickets: `0`" in md_text
    assert "Do not patch `GAME/SAVEGAME.C`" in md_text
    assert "Recommended next ticket: none" in md_text

    for text in story_texts:
        assert "Status: Done" in text
        assert "## Progress" in text
        assert "- [x] Terminal decision published." in text
        assert "## Terminal decision" in text

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
