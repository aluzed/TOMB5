from pathlib import Path
import csv

from scripts.reverse.re126_re132_runtime_support_chain import build_runtime_support_chain, write_all_artifacts, C_KEYWORD_ARTIFACTS


def test_re126_re132_consumes_re125_plan_and_exhausts_gameflow_runtime():
    repo = Path(__file__).resolve().parents[2]
    chain = build_runtime_support_chain(repo)

    assert [ticket.story_id for ticket in chain.tickets] == ["RE-126", "RE-127", "RE-128", "RE-129", "RE-130", "RE-131", "RE-132"]
    assert chain.scope == "runtime-support-mixed"
    assert [row.function for row in chain.scope_rows] == ["ResetGuards"]
    assert chain.code_change_ready_count == 0
    assert chain.marker_ready_count == 0
    assert chain.source_patch_ready_count == 0
    assert chain.handoff.next_ticket == "TBD"
    assert chain.handoff.next_subcluster == "gameflow-runtime-control-exhausted"
    assert "all RE-077 gameflow runtime subclusters are closed" in chain.handoff.reason
    assert any(ticket.story_id == "RE-132" and ticket.next_ticket == "TBD" for ticket in chain.tickets)


def test_re126_re132_outputs_metadata_only_artifacts_and_filters_definition_calls(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    chain = build_runtime_support_chain(repo)
    written = write_all_artifacts(chain, tmp_path)

    callsites = list(csv.DictReader(written["callsite_csv"].open(newline="", encoding="utf-8")))
    assert callsites
    assert all(row["callee"] == "ResetGuards" for row in callsites)
    assert all(row["caller"] not in C_KEYWORD_ARTIFACTS for row in callsites)
    assert all(row["callee"] not in C_KEYWORD_ARTIFACTS for row in callsites)
    assert all(row["patch_ready"] == "no" for row in callsites)

    taxonomy = list(csv.DictReader(written["taxonomy_csv"].open(newline="", encoding="utf-8")))
    assert taxonomy
    assert all(row["patch_ready"] == "no" for row in taxonomy)
    assert any("active-item-state" in row["state_fields"] for row in taxonomy)
    assert any("guard-ai-state" in row["write_surfaces"] for row in taxonomy)

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "TBD"
    assert handoff["next_subcluster"] == "gameflow-runtime-control-exhausted"

    story_text = written["RE-132"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-125 ticket plan consumed" in story_text
    assert "Runtime-support metadata mapped." in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "gameflow-runtime-control-exhausted" in story_text
    assert "test_re126_re132_runtime_support_chain.py" in story_text
    assert "test_re118_re124" not in story_text

    md_text = written["md"].read_text(encoding="utf-8")
    assert "missing runtime support state contract" in md_text
    assert "lara runtime" not in md_text.lower()
    assert "Lara-runtime" not in md_text

    for key, path in written.items():
        paths = [path]
        for one_path in paths:
            text = one_path.read_text(encoding="utf-8").lower()
            assert "payload" not in text
            assert "opcode" not in text
            assert "raw call target" not in text
            assert "machine word" not in text
            assert "0x" not in text
