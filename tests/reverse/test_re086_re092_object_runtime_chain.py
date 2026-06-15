from pathlib import Path
import csv

from scripts.reverse.re086_re092_object_runtime_chain import (
    build_object_runtime_chain,
    write_all_artifacts,
    C_KEYWORD_ARTIFACTS,
)


def test_re086_re092_consumes_re085_plan_and_closes_torch_flare_control():
    repo = Path(__file__).resolve().parents[2]
    chain = build_object_runtime_chain(repo)

    assert chain.domain_id == "module-game"
    assert chain.cluster == "gameflow-runtime-control"
    assert chain.subcluster == "torch-and-flare-control"
    assert [ticket.story_id for ticket in chain.tickets] == [
        "RE-086",
        "RE-087",
        "RE-088",
        "RE-089",
        "RE-090",
        "RE-091",
        "RE-092",
    ]
    assert chain.final_decision == "documentation-only-terminal-blocker"
    assert chain.code_change_ready_count == 0
    assert chain.marker_ready_count == 0
    assert chain.source_patch_ready_count == 0
    assert [row.function for row in chain.scope_rows] == ["FlameTorchControl", "FlareControl"]
    assert chain.handoff.next_ticket == "RE-093"
    assert chain.handoff.next_subcluster == "dynamic-light-control"


def test_re086_re092_outputs_metadata_only_artifacts_and_filters_definition_calls(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    chain = build_object_runtime_chain(repo)
    written = write_all_artifacts(chain, tmp_path)

    assert written["chain_csv"].name == "re086-re092-object-runtime-chain.csv"
    assert written["scope_csv"].name == "re086-object-runtime-scope.csv"
    assert written["callsite_csv"].name == "re086-object-runtime-callsite-map.csv"
    assert written["taxonomy_csv"].name == "re087-object-runtime-argument-state-taxonomy.csv"
    assert written["handoff_csv"].name == "re092-object-runtime-handoff.csv"
    assert written["md"].name == "re086-re092-object-runtime-chain.md"

    with written["chain_csv"].open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[-1]["story_id"] == "RE-092"
    assert rows[-1]["decision"] == "handoff-to-next-object-runtime-subcluster"
    assert rows[-1]["next_ticket"] == "RE-093"

    with written["scope_csv"].open(newline="", encoding="utf-8") as f:
        scope_rows = list(csv.DictReader(f))
    assert not ({row["function"] for row in scope_rows} & C_KEYWORD_ARTIFACTS)
    assert {row["patch_ready"] for row in scope_rows} == {"no"}

    with written["callsite_csv"].open(newline="", encoding="utf-8") as f:
        callsites = list(csv.DictReader(f))
    assert callsites, "expected symbolic dispatch/callsite rows for torch and flare control"
    assert not ({row["caller"] for row in callsites} & C_KEYWORD_ARTIFACTS)
    assert not ({row["callee"] for row in callsites} & C_KEYWORD_ARTIFACTS)
    assert {int(row["line"]) for row in callsites}.isdisjoint({25, 30})

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "machine word" not in text
        assert "raw call target" not in text
        assert "0x" not in text

    for story_id in ("RE-086", "RE-087", "RE-088", "RE-089", "RE-090", "RE-091", "RE-092"):
        story = written[story_id]
        text = story.read_text(encoding="utf-8")
        assert "## Progress tracker" in text
        assert "- [x]" in text
        assert "code change readiness: `blocked`" in text
