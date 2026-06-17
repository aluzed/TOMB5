from pathlib import Path
import csv

from scripts.reverse.re317_collision_geometry_helper_next_candidate_callsite_map import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_collision_geometry_helper_next_candidate_callsite_map,
    write_all_artifacts,
)


def test_re317_builds_next_candidate_source_backed_callsite_map_without_authorizing_patch():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_geometry_helper_next_candidate_callsite_map(repo)

    assert bundle.summary.story_id == "RE-317"
    assert bundle.summary.topic == "collision-geometry-helper-next-candidate-callsite-map"
    assert bundle.summary.upstream_handoff == "RE-316"
    assert bundle.summary.selected_candidate_id == "d96359c1d9f3"
    assert bundle.summary.previous_candidate_id == "5e99f39fd8ef"
    assert bundle.summary.source_context_function_count == 23
    assert bundle.summary.source_backed_callsite_count == 40
    assert bundle.summary.implemented_context_function_count == 3
    assert bundle.summary.stub_context_function_count == 19
    assert bundle.summary.no_callsite_context_function_count == 1
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-318"
    assert bundle.summary.next_topic == "collision-geometry-helper-next-candidate-callsite-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.function_rows) == 23
    assert len(bundle.callsite_rows) == 40
    assert {row.function_status for row in bundle.function_rows} == {
        "source-with-calls",
        "stub-unimplemented",
        "source-no-callsite",
    }
    assert sum(row.function_status == "source-with-calls" for row in bundle.function_rows) == 3
    assert sum(row.function_status == "stub-unimplemented" for row in bundle.function_rows) == 19
    assert sum(row.function_status == "source-no-callsite" for row in bundle.function_rows) == 1

    first = bundle.callsite_rows[0]
    assert first.caller_symbol == "DoorCollision"
    assert first.source_file == "GAME/DOOR.C"
    assert first.source_line == 161
    assert first.callee_symbol == "TestLaraPosition"
    assert first.callsite_family == "position-test"
    assert first.candidate_level_proof == "no"
    assert first.ready_to_reopen_domain == "no"
    assert first.source_patch_authorized == "no"

    monitor_rows = [row for row in bundle.callsite_rows if row.caller_symbol == "MonitorScreenCollision"]
    assert [row.callee_symbol for row in monitor_rows] == [
        "TestTriggersAtXYZ",
        "ObjectCollision",
        "GetBoundsAccurate",
        "TestLaraPosition",
        "MoveLaraPosition",
    ]

    for row in bundle.function_rows + bundle.callsite_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "unimplemented();" not in row_text


def test_re317_writes_metadata_only_next_candidate_callsite_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_geometry_helper_next_candidate_callsite_map(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"functions_csv", "callsites_csv", "gate_csv", "summary_csv", "handoff_csv", "md", "story"}

    functions = list(csv.DictReader(written["functions_csv"].open(newline="", encoding="utf-8")))
    assert len(functions) == 23
    assert "source_line_text" not in functions[0]
    assert functions[0]["candidate_id"] == "d96359c1d9f3"
    assert functions[0]["caller_symbol"] == "DoorCollision"
    assert functions[0]["definition_line"] == "147"
    assert functions[0]["function_status"] == "source-with-calls"

    callsites = list(csv.DictReader(written["callsites_csv"].open(newline="", encoding="utf-8")))
    assert len(callsites) == 40
    assert "source_line_text" not in callsites[0]
    assert callsites[0]["candidate_id"] == "d96359c1d9f3"
    assert callsites[0]["source_line"] == "161"
    assert callsites[0]["callee_symbol"] == "TestLaraPosition"

    gate = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert gate == [
        {
            "rank": "1",
            "candidate_id": "d96359c1d9f3",
            "previous_candidate_id": "5e99f39fd8ef",
            "source_context_function_count": "23",
            "source_backed_callsite_count": "40",
            "implemented_context_function_count": "3",
            "stub_context_function_count": "19",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-next-candidate-callsite-map-needs-readiness-gate",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-318",
            "next_topic": "collision-geometry-helper-next-candidate-callsite-readiness-gate",
            "stop_condition": "next-candidate source-backed callsites exist but still need a readiness gate before domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-318"
    assert handoff["selected_candidate_id"] == "d96359c1d9f3"
    assert handoff["previous_candidate_id"] == "5e99f39fd8ef"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-316 next-candidate callsite-map handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-318" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-317 collision geometry helper next candidate callsite map" in md
    assert "Next-candidate source-backed callsite rows are not source-patch authorization" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
