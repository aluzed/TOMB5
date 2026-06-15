from pathlib import Path
import csv

from scripts.reverse.re078_re084_gameflow_runtime_chain import (
    build_gameflow_runtime_chain,
    write_all_artifacts,
    C_KEYWORD_ARTIFACTS,
)


def test_re078_re084_consumes_re077_plan_and_closes_title_control_phase():
    repo = Path(__file__).resolve().parents[2]
    chain = build_gameflow_runtime_chain(repo)

    assert chain.domain_id == "module-game"
    assert chain.cluster == "gameflow-runtime-control"
    assert chain.subcluster == "title-and-control-phase"
    assert [ticket.story_id for ticket in chain.tickets] == [
        "RE-078",
        "RE-079",
        "RE-080",
        "RE-081",
        "RE-082",
        "RE-083",
        "RE-084",
    ]
    assert chain.final_decision == "documentation-only-terminal-blocker"
    assert chain.code_change_ready_count == 0
    assert chain.marker_ready_count == 0
    assert chain.source_patch_ready_count == 0
    assert [row.function for row in chain.scope_rows] == ["DoTitle", "QuickControlPhase", "DoGameflow"]
    assert chain.handoff.next_ticket == "RE-085"
    assert chain.handoff.next_cluster == "object-runtime-control"


def test_re078_re084_outputs_metadata_only_artifacts_and_filters_keywords(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    chain = build_gameflow_runtime_chain(repo)
    written = write_all_artifacts(chain, tmp_path)

    assert written["chain_csv"].name == "re078-re084-gameflow-runtime-chain.csv"
    assert written["scope_csv"].name == "re078-gameflow-runtime-scope.csv"
    assert written["callsite_csv"].name == "re078-gameflow-runtime-callsite-map.csv"
    assert written["taxonomy_csv"].name == "re079-gameflow-runtime-argument-state-taxonomy.csv"
    assert written["handoff_csv"].name == "re084-gameflow-runtime-handoff.csv"
    assert written["md"].name == "re078-re084-gameflow-runtime-chain.md"

    with written["chain_csv"].open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[-1]["story_id"] == "RE-084"
    assert rows[-1]["decision"] == "handoff-to-next-gameflow-runtime-subcluster"
    assert rows[-1]["next_ticket"] == "RE-085"

    with written["callsite_csv"].open(newline="", encoding="utf-8") as f:
        callsites = list(csv.DictReader(f))
    assert callsites, "expected symbolic caller/callee rows for title/control phase"
    assert not ({row["caller"] for row in callsites} & C_KEYWORD_ARTIFACTS)
    assert not ({row["callee"] for row in callsites} & C_KEYWORD_ARTIFACTS)
    assert {int(row["line"]) for row in callsites}.isdisjoint({155, 783, 931})

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "machine word" not in text
        assert "raw call target" not in text
        assert "0x" not in text

    for story_id in ("RE-078", "RE-079", "RE-080", "RE-081", "RE-082", "RE-083", "RE-084"):
        story = written[story_id]
        text = story.read_text(encoding="utf-8")
        assert "## Progress tracker" in text
        assert "- [x]" in text
        assert "code change readiness: `blocked`" in text
