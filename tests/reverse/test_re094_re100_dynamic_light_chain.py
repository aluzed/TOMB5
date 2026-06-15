from pathlib import Path
import csv

from scripts.reverse.re094_re100_dynamic_light_chain import build_dynamic_light_chain, write_all_artifacts, C_KEYWORD_ARTIFACTS


def test_re094_re100_consumes_re093_plan_and_closes_dynamic_light_control():
    repo = Path(__file__).resolve().parents[2]
    chain = build_dynamic_light_chain(repo)

    assert chain.domain_id == "module-game"
    assert chain.cluster == "gameflow-runtime-control"
    assert chain.subcluster == "dynamic-light-control"
    assert [ticket.story_id for ticket in chain.tickets] == ["RE-094", "RE-095", "RE-096", "RE-097", "RE-098", "RE-099", "RE-100"]
    assert [row.function for row in chain.scope_rows] == ["ControlElectricalLight", "ControlStrobeLight"]
    assert chain.final_decision == "documentation-only-terminal-blocker"
    assert chain.code_change_ready_count == 0
    assert chain.marker_ready_count == 0
    assert chain.source_patch_ready_count == 0
    assert chain.handoff.next_ticket == "RE-101"
    assert chain.handoff.next_subcluster == "pickup-search-control"
    assert "SearchObjectControl" in chain.handoff.reason


def test_re094_re100_outputs_metadata_only_artifacts_and_filters_definition_calls(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    chain = build_dynamic_light_chain(repo)
    written = write_all_artifacts(chain, tmp_path)

    assert written["chain_csv"].name == "re094-re100-dynamic-light-chain.csv"
    assert written["scope_csv"].name == "re094-dynamic-light-scope.csv"
    assert written["callsite_csv"].name == "re094-dynamic-light-callsite-map.csv"
    assert written["taxonomy_csv"].name == "re095-dynamic-light-argument-state-taxonomy.csv"
    assert written["handoff_csv"].name == "re100-dynamic-light-handoff.csv"

    with written["chain_csv"].open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[-1]["story_id"] == "RE-100"
    assert rows[-1]["decision"] == "handoff-to-next-object-runtime-subcluster"

    with written["callsite_csv"].open(newline="", encoding="utf-8") as f:
        callsites = list(csv.DictReader(f))
    assert callsites
    assert not ({row["caller"] for row in callsites} & C_KEYWORD_ARTIFACTS)
    assert not ({row["callee"] for row in callsites} & C_KEYWORD_ARTIFACTS)
    assert {int(row["line"]) for row in callsites}.isdisjoint({22, 104})

    story_text = written["RE-100"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-093 ticket plan consumed" in story_text
    assert "RE-085 ticket plan consumed" not in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "RE-101" in story_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "machine word" not in text
        assert "raw call target" not in text
        assert "0x" not in text
