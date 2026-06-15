from pathlib import Path
import csv

from scripts.reverse.re102_re108_pickup_search_chain import build_pickup_search_chain, write_all_artifacts, C_KEYWORD_ARTIFACTS


def test_re102_re108_consumes_re101_plan_and_closes_pickup_search_control():
    repo = Path(__file__).resolve().parents[2]
    chain = build_pickup_search_chain(repo)

    assert chain.domain_id == "module-game"
    assert chain.cluster == "gameflow-runtime-control"
    assert chain.subcluster == "pickup-search-control"
    assert [ticket.story_id for ticket in chain.tickets] == ["RE-102", "RE-103", "RE-104", "RE-105", "RE-106", "RE-107", "RE-108"]
    assert [row.function for row in chain.scope_rows] == ["SearchObjectControl"]
    assert chain.final_decision == "documentation-only-terminal-blocker"
    assert chain.code_change_ready_count == 0
    assert chain.marker_ready_count == 0
    assert chain.source_patch_ready_count == 0
    assert chain.handoff.next_ticket == "TBD"
    assert chain.handoff.next_subcluster == "object-runtime-control-exhausted"


def test_re102_re108_outputs_metadata_only_artifacts_and_filters_definition_calls(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    chain = build_pickup_search_chain(repo)
    written = write_all_artifacts(chain, tmp_path)

    assert written["chain_csv"].name == "re102-re108-pickup-search-chain.csv"
    assert written["scope_csv"].name == "re102-pickup-search-scope.csv"
    assert written["callsite_csv"].name == "re102-pickup-search-callsite-map.csv"
    assert written["taxonomy_csv"].name == "re103-pickup-search-argument-state-taxonomy.csv"
    assert written["handoff_csv"].name == "re108-pickup-search-handoff.csv"

    with written["chain_csv"].open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[-1]["story_id"] == "RE-108"
    assert rows[-1]["decision"] == "object-runtime-control-exhausted"

    with written["callsite_csv"].open(newline="", encoding="utf-8") as f:
        callsites = list(csv.DictReader(f))
    assert callsites
    assert not ({row["caller"] for row in callsites} & C_KEYWORD_ARTIFACTS)
    assert not ({row["callee"] for row in callsites} & C_KEYWORD_ARTIFACTS)
    assert {int(row["line"]) for row in callsites}.isdisjoint({175})

    story_text = written["RE-108"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-101 ticket plan consumed" in story_text
    assert "RE-085 ticket plan consumed" not in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "object-runtime-control-exhausted" in story_text
    assert "test_re102_re108_pickup_search_chain.py" in story_text
    assert "test_re094_re100_pickup_search_chain.py" not in story_text
    assert "one unimplemented SearchObjectControl stub" in story_text
    assert "one source stub and one implemented source control" not in story_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "machine word" not in text
        assert "raw call target" not in text
        assert "0x" not in text
