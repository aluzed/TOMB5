from pathlib import Path
import csv

from scripts.reverse.re110_re116_scripted_runtime_chain import build_scripted_runtime_chain, write_all_artifacts, C_KEYWORD_ARTIFACTS


def test_re110_re116_consumes_re109_plan_and_hands_off_to_lara_runtime_control():
    repo = Path(__file__).resolve().parents[2]
    chain = build_scripted_runtime_chain(repo)

    assert chain.domain_id == "module-game"
    assert chain.cluster == "gameflow-runtime-control"
    assert chain.subcluster == "scripted-runtime-control"
    assert [ticket.story_id for ticket in chain.tickets] == ["RE-110", "RE-111", "RE-112", "RE-113", "RE-114", "RE-115", "RE-116"]
    assert [row.function for row in chain.scope_rows] == ["andrea2_control", "special3_control"]
    assert chain.final_decision == "documentation-only-terminal-blocker"
    assert chain.code_change_ready_count == 0
    assert chain.marker_ready_count == 0
    assert chain.source_patch_ready_count == 0
    assert chain.handoff.next_ticket == "RE-117"
    assert chain.handoff.next_subcluster == "lara-runtime-control"
    assert "LaraControl" in chain.handoff.reason


def test_re110_re116_outputs_metadata_only_artifacts_and_filters_definition_calls(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    chain = build_scripted_runtime_chain(repo)
    written = write_all_artifacts(chain, tmp_path)

    assert written["chain_csv"].name == "re110-re116-scripted-runtime-chain.csv"
    assert written["scope_csv"].name == "re110-scripted-runtime-scope.csv"
    assert written["callsite_csv"].name == "re110-scripted-runtime-callsite-map.csv"
    assert written["taxonomy_csv"].name == "re111-scripted-runtime-argument-state-taxonomy.csv"
    assert written["handoff_csv"].name == "re116-scripted-runtime-handoff.csv"

    with written["chain_csv"].open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[-1]["story_id"] == "RE-116"
    assert rows[-1]["decision"] == "handoff-to-next-gameflow-subcluster"

    with written["callsite_csv"].open(newline="", encoding="utf-8") as f:
        callsites = list(csv.DictReader(f))
    assert callsites
    assert not ({row["caller"] for row in callsites} & C_KEYWORD_ARTIFACTS)
    assert not ({row["callee"] for row in callsites} & C_KEYWORD_ARTIFACTS)
    assert {int(row["line"]) for row in callsites}.isdisjoint({1891, 2606})

    story_text = written["RE-116"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-109 ticket plan consumed" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "RE-117" in story_text
    assert "test_re110_re116_scripted_runtime_chain.py" in story_text
    assert "test_re102_re108" not in story_text
    assert "Scripted-runtime metadata mapped." in story_text
    assert "Pickup-search metadata mapped." not in story_text
    assert "missing scripted runtime state contract" in written["md"].read_text(encoding="utf-8")
    assert "missing object state source body" not in written["md"].read_text(encoding="utf-8")

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "machine word" not in text
        assert "raw call target" not in text
        assert "0x" not in text
