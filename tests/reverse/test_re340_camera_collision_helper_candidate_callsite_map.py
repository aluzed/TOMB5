from pathlib import Path
import csv

from scripts.reverse.re340_camera_collision_helper_candidate_callsite_map import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_camera_collision_helper_candidate_callsite_map,
    write_all_artifacts,
)


def test_re340_builds_source_backed_callsite_map_without_authorizing_patch():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_camera_collision_helper_candidate_callsite_map(repo)

    assert bundle.summary.story_id == "RE-340"
    assert bundle.summary.topic == "camera-collision-helper-candidate-callsite-map"
    assert bundle.summary.upstream_handoff == "RE-339"
    assert bundle.summary.selected_candidate_id == "95c41ac597d6"
    assert bundle.summary.source_context_function_count == 9
    assert bundle.summary.source_backed_callsite_count == 60
    assert bundle.summary.implemented_context_function_count == 2
    assert bundle.summary.stub_context_function_count == 7
    assert bundle.summary.no_callsite_context_function_count == 0
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-341"
    assert bundle.summary.next_topic == "camera-collision-helper-callsite-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.function_rows) == 9
    assert len(bundle.callsite_rows) == 60
    first_function = bundle.function_rows[0]
    assert first_function.caller_symbol == "CalculateCamera"
    assert first_function.source_file == "GAME/CAMERA.C"
    assert first_function.definition_line == 1167
    assert first_function.end_line == 1594
    assert first_function.source_backed_callsite_count == 26
    assert first_function.function_status == "stub-unimplemented"

    move_camera = next(row for row in bundle.function_rows if row.caller_symbol == "MoveCamera")
    assert move_camera.source_file == "GAME/CAMERA.C"
    assert move_camera.definition_line == 2244
    assert move_camera.end_line == 2478
    assert move_camera.source_backed_callsite_count == 22
    assert move_camera.function_status == "source-with-calls"

    first_callsite = bundle.callsite_rows[0]
    assert first_callsite.caller_symbol == "CalculateCamera"
    assert first_callsite.callee_symbol == "BinocularCamera"
    assert first_callsite.callsite_family == "camera-runtime-helper"
    assert first_callsite.candidate_level_proof == "no"
    assert first_callsite.ready_to_reopen_domain == "no"
    assert first_callsite.source_patch_authorized == "no"

    assert any(row.caller_symbol == "CalculateCamera" and row.callee_symbol == "SoundEffect" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "MoveCamera" and row.callee_symbol == "GetFloor" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "CreatureCollision" and row.callee_symbol == "UNIMPLEMENTED" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "LaraWaterCurrent" and row.callee_symbol == "UNIMPLEMENTED" for row in bundle.callsite_rows)

    for row in bundle.function_rows + bundle.callsite_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "unimplemented();" not in row_text


def test_re340_writes_metadata_only_callsite_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_camera_collision_helper_candidate_callsite_map(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"functions_csv", "callsites_csv", "gate_csv", "summary_csv", "handoff_csv", "md", "story"}

    functions = list(csv.DictReader(written["functions_csv"].open(newline="", encoding="utf-8")))
    assert len(functions) == 9
    assert "source_line_text" not in functions[0]
    assert functions[0]["caller_symbol"] == "CalculateCamera"
    assert functions[0]["definition_line"] == "1167"
    assert functions[0]["function_status"] == "stub-unimplemented"

    callsites = list(csv.DictReader(written["callsites_csv"].open(newline="", encoding="utf-8")))
    assert len(callsites) == 60
    assert "source_line_text" not in callsites[0]
    assert callsites[0]["callee_symbol"] == "BinocularCamera"

    gate = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert gate == [
        {
            "rank": "1",
            "candidate_id": "95c41ac597d6",
            "source_context_function_count": "9",
            "source_backed_callsite_count": "60",
            "implemented_context_function_count": "2",
            "stub_context_function_count": "7",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-callsite-map-needs-readiness-gate",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-341",
            "next_topic": "camera-collision-helper-callsite-readiness-gate",
            "stop_condition": "source-backed camera/collision callsites exist but still need a readiness gate before domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-341"
    assert handoff["selected_candidate_id"] == "95c41ac597d6"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-339 proof-export handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-341" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-340 camera-collision helper candidate callsite map" in md
    assert "Source-backed callsite rows are not source-patch authorization" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
