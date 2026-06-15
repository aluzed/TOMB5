from pathlib import Path
import csv

from scripts.reverse.re142_re148_object_interaction_chain import build_object_interaction_chain, write_all_artifacts, C_KEYWORD_ARTIFACTS


def test_re142_re148_consumes_re141_plan_and_hands_to_item_lighting():
    repo = Path(__file__).resolve().parents[2]
    chain = build_object_interaction_chain(repo)

    assert [ticket.story_id for ticket in chain.tickets] == ["RE-142", "RE-143", "RE-144", "RE-145", "RE-146", "RE-147", "RE-148"]
    assert chain.scope == "object-interaction"
    assert [row.function for row in chain.scope_rows] == ["FindPlinth", "CollectCarriedItems", "BaddyObjects", "InitialiseObjects", "TrapObjects", "ObjectObjects"]
    assert chain.code_change_ready_count == 0
    assert chain.marker_ready_count == 0
    assert chain.source_patch_ready_count == 0
    assert chain.handoff.next_ticket == "RE-149"
    assert chain.handoff.next_cluster == "item-lighting-interaction"
    assert chain.handoff.next_subcluster == "item-lighting-interaction"
    assert "object-interaction closed" in chain.handoff.reason
    assert "DoFlameTorch" in chain.handoff.reason
    assert any(ticket.story_id == "RE-148" and ticket.next_ticket == "RE-149" for ticket in chain.tickets)


def test_re142_re148_outputs_metadata_only_artifacts_and_filters_definition_calls(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    chain = build_object_interaction_chain(repo)
    written = write_all_artifacts(chain, tmp_path)

    callsites = list(csv.DictReader(written["callsite_csv"].open(newline="", encoding="utf-8")))
    assert callsites
    assert all(row["caller"] not in C_KEYWORD_ARTIFACTS for row in callsites)
    assert all(row["callee"] not in C_KEYWORD_ARTIFACTS for row in callsites)
    assert all(row["patch_ready"] == "no" for row in callsites)
    assert any(row["callee"] == "FindPlinth" for row in callsites)
    assert not any(row["callee"] == "FindPlinth" and row["line"] == "319" for row in callsites)
    assert any(row["callee"] == "CollectCarriedItems" for row in callsites)
    assert any(row["callee"] == "BaddyObjects" for row in callsites)

    taxonomy = list(csv.DictReader(written["taxonomy_csv"].open(newline="", encoding="utf-8")))
    assert taxonomy
    assert all(row["patch_ready"] == "no" for row in taxonomy)
    assert any("item-state" in row["state_fields"] for row in taxonomy)
    assert any("object-setup-state" in row["state_fields"] or "trap-state" in row["state_fields"] for row in taxonomy)

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-149"
    assert handoff["next_cluster"] == "item-lighting-interaction"
    assert handoff["next_subcluster"] == "item-lighting-interaction"

    story_text = written["RE-148"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-141 ticket plan consumed" in story_text
    assert "Object-interaction metadata mapped." in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "item-lighting-interaction" in story_text
    assert "test_re142_re148_object_interaction_chain.py" in story_text
    assert "test_re134_re140" not in story_text

    md_text = written["md"].read_text(encoding="utf-8")
    assert "missing object interaction state contract" in md_text
    assert "gameplay mixed" not in md_text.lower()

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "raw call target" not in text
        assert "machine word" not in text
        assert "0x" not in text
