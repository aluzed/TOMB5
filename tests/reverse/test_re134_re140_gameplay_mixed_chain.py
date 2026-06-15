from pathlib import Path
import csv

from scripts.reverse.re134_re140_gameplay_mixed_chain import build_gameplay_mixed_chain, write_all_artifacts, C_KEYWORD_ARTIFACTS


def test_re134_re140_consumes_re133_plan_and_hands_to_object_interaction():
    repo = Path(__file__).resolve().parents[2]
    chain = build_gameplay_mixed_chain(repo)

    assert [ticket.story_id for ticket in chain.tickets] == ["RE-134", "RE-135", "RE-136", "RE-137", "RE-138", "RE-139", "RE-140"]
    assert chain.scope == "gameplay-mixed"
    assert [row.function for row in chain.scope_rows][:5] == ["Load_and_Init_Cutseq", "CreateZone", "special4_init", "init_water_table", "InitialiseSqrtTable"]
    assert len(chain.scope_rows) == 11
    assert chain.code_change_ready_count == 0
    assert chain.marker_ready_count == 0
    assert chain.source_patch_ready_count == 0
    assert chain.handoff.next_ticket == "RE-141"
    assert chain.handoff.next_cluster == "object-interaction"
    assert chain.handoff.next_subcluster == "object-interaction"
    assert "gameplay-mixed closed" in chain.handoff.reason
    assert "FindPlinth" in chain.handoff.reason
    assert any(ticket.story_id == "RE-140" and ticket.next_ticket == "RE-141" for ticket in chain.tickets)


def test_re134_re140_outputs_metadata_only_artifacts_and_filters_definition_calls(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    chain = build_gameplay_mixed_chain(repo)
    written = write_all_artifacts(chain, tmp_path)

    callsites = list(csv.DictReader(written["callsite_csv"].open(newline="", encoding="utf-8")))
    assert callsites
    assert all(row["caller"] not in C_KEYWORD_ARTIFACTS for row in callsites)
    assert all(row["callee"] not in C_KEYWORD_ARTIFACTS for row in callsites)
    assert all(row["patch_ready"] == "no" for row in callsites)
    assert any(row["callee"] == "Load_and_Init_Cutseq" for row in callsites)
    assert any(row["callee"] == "CreateZone" for row in callsites)

    taxonomy = list(csv.DictReader(written["taxonomy_csv"].open(newline="", encoding="utf-8")))
    assert taxonomy
    assert all(row["patch_ready"] == "no" for row in taxonomy)
    assert any("cutscene-state" in row["state_fields"] for row in taxonomy)
    assert any("zone-state" in row["state_fields"] or "setup-table-state" in row["state_fields"] for row in taxonomy)

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-141"
    assert handoff["next_cluster"] == "object-interaction"
    assert handoff["next_subcluster"] == "object-interaction"

    story_text = written["RE-140"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-133 ticket plan consumed" in story_text
    assert "Gameplay-mixed metadata mapped." in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "object-interaction" in story_text
    assert "test_re134_re140_gameplay_mixed_chain.py" in story_text
    assert "test_re126_re132" not in story_text

    md_text = written["md"].read_text(encoding="utf-8")
    assert "missing gameplay mixed state contract" in md_text
    assert "runtime support" not in md_text.lower()

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "raw call target" not in text
        assert "machine word" not in text
        assert "0x" not in text
