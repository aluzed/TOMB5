from pathlib import Path
import csv

from scripts.reverse.re325_switch_door_control_helper_candidate_callsite_map import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_switch_door_control_helper_candidate_callsite_map,
    write_all_artifacts,
)


def test_re325_builds_source_backed_callsite_map_without_authorizing_patch():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_switch_door_control_helper_candidate_callsite_map(repo)

    assert bundle.summary.story_id == "RE-325"
    assert bundle.summary.topic == "switch-door-control-helper-candidate-callsite-map"
    assert bundle.summary.upstream_handoff == "RE-324"
    assert bundle.summary.selected_candidate_id == "8d1fc6fc3cfc"
    assert bundle.summary.source_context_function_count == 22
    assert bundle.summary.source_backed_callsite_count == 39
    assert bundle.summary.implemented_context_function_count == 7
    assert bundle.summary.stub_context_function_count == 13
    assert bundle.summary.no_callsite_context_function_count == 2
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-326"
    assert bundle.summary.next_topic == "switch-door-control-helper-callsite-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.function_rows) == 22
    assert len(bundle.callsite_rows) == 39
    assert {row.function_status for row in bundle.function_rows} == {
        "source-with-calls",
        "stub-unimplemented",
        "source-no-callsite",
    }
    assert sum(row.function_status == "source-with-calls" for row in bundle.function_rows) == 7
    assert sum(row.function_status == "stub-unimplemented" for row in bundle.function_rows) == 13
    assert sum(row.function_status == "source-no-callsite" for row in bundle.function_rows) == 2

    first = bundle.callsite_rows[0]
    assert first.caller_symbol == "DoorControl"
    assert first.source_file == "GAME/DOOR.C"
    assert first.source_line == 233
    assert first.callee_symbol == "UNIMPLEMENTED"
    assert first.callsite_family == "stub-marker"
    assert first.candidate_level_proof == "no"
    assert first.ready_to_reopen_domain == "no"
    assert first.source_patch_authorized == "no"

    sequence_open_rows = [row for row in bundle.callsite_rows if row.caller_symbol == "SequenceDoorControl" and row.callee_symbol == "OpenThatDoor"]
    assert [row.source_line for row in sequence_open_rows] == [86, 87, 88, 89]
    trapdoor_rows = [row for row in bundle.callsite_rows if row.caller_symbol == "TrapDoorControl"]
    assert [row.callee_symbol for row in trapdoor_rows] == ["TriggerActive", "AnimateItem", "OpenTrapDoor", "CloseTrapDoor"]

    for row in bundle.function_rows + bundle.callsite_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "unimplemented();" not in row_text


def test_re325_writes_metadata_only_callsite_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_switch_door_control_helper_candidate_callsite_map(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"functions_csv", "callsites_csv", "gate_csv", "summary_csv", "handoff_csv", "md", "story"}

    functions = list(csv.DictReader(written["functions_csv"].open(newline="", encoding="utf-8")))
    assert len(functions) == 22
    assert "source_line_text" not in functions[0]
    assert functions[0]["caller_symbol"] == "DoorControl"
    assert functions[0]["definition_line"] == "231"
    assert functions[0]["function_status"] == "stub-unimplemented"

    callsites = list(csv.DictReader(written["callsites_csv"].open(newline="", encoding="utf-8")))
    assert len(callsites) == 39
    assert "source_line_text" not in callsites[0]
    assert callsites[0]["source_line"] == "233"
    assert callsites[0]["callee_symbol"] == "UNIMPLEMENTED"

    gate = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert gate == [
        {
            "rank": "1",
            "candidate_id": "8d1fc6fc3cfc",
            "source_context_function_count": "22",
            "source_backed_callsite_count": "39",
            "implemented_context_function_count": "7",
            "stub_context_function_count": "13",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-callsite-map-needs-readiness-gate",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-326",
            "next_topic": "switch-door-control-helper-callsite-readiness-gate",
            "stop_condition": "source-backed callsites exist but still need a readiness gate before domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-326"
    assert handoff["selected_candidate_id"] == "8d1fc6fc3cfc"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-324 callsite-map handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-326" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-325 switch-door-control helper candidate callsite map" in md
    assert "Source-backed callsite rows are not source-patch authorization" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
