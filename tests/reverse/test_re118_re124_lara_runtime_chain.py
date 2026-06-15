from pathlib import Path
import csv

from scripts.reverse.re118_re124_lara_runtime_chain import build_lara_runtime_chain, write_all_artifacts, C_KEYWORD_ARTIFACTS


def test_re118_re124_consumes_re117_plan_and_hands_off_to_runtime_support_mixed():
    repo = Path(__file__).resolve().parents[2]
    chain = build_lara_runtime_chain(repo)

    assert [ticket.story_id for ticket in chain.tickets] == ["RE-118", "RE-119", "RE-120", "RE-121", "RE-122", "RE-123", "RE-124"]
    assert chain.scope == "lara-runtime-control"
    assert [row.function for row in chain.scope_rows] == ["LaraControl"]
    assert chain.code_change_ready_count == 0
    assert chain.marker_ready_count == 0
    assert chain.source_patch_ready_count == 0
    assert chain.handoff.next_ticket == "RE-125"
    assert chain.handoff.next_subcluster == "runtime-support-mixed"
    assert "ResetGuards" in chain.handoff.reason
    assert any(ticket.story_id == "RE-124" and ticket.next_ticket == "RE-125" for ticket in chain.tickets)


def test_re118_re124_outputs_metadata_only_artifacts_and_filters_definition_calls(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    chain = build_lara_runtime_chain(repo)
    written = write_all_artifacts(chain, tmp_path)

    callsites = list(csv.DictReader(written["callsite_csv"].open(newline="", encoding="utf-8")))
    assert callsites
    assert all(row["callee"] == "LaraControl" for row in callsites)
    assert all(row["caller"] not in C_KEYWORD_ARTIFACTS for row in callsites)
    assert all(row["callee"] not in C_KEYWORD_ARTIFACTS for row in callsites)
    assert all(row["patch_ready"] == "no" for row in callsites)

    taxonomy = list(csv.DictReader(written["taxonomy_csv"].open(newline="", encoding="utf-8")))
    assert taxonomy
    assert all(row["patch_ready"] == "no" for row in taxonomy)
    assert any("lara-state" in row["state_fields"] for row in taxonomy)

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-125"
    assert handoff["next_subcluster"] == "runtime-support-mixed"

    story_text = written["RE-124"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-117 ticket plan consumed" in story_text
    assert "Lara-runtime metadata mapped." in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "RE-125" in story_text
    assert "test_re118_re124_lara_runtime_chain.py" in story_text
    assert "test_re110_re116" not in story_text

    md_text = written["md"].read_text(encoding="utf-8")
    assert "missing Lara runtime state contract" in md_text
    assert "scripted runtime" not in md_text.lower()

    for key, path in written.items():
        if key == "stories":
            paths = path.values()
        else:
            paths = [path]
        for one_path in paths:
            text = one_path.read_text(encoding="utf-8").lower()
            assert "payload" not in text
            assert "opcode" not in text
            assert "raw call target" not in text
            assert "machine word" not in text
            assert "0x" not in text
