from pathlib import Path
import csv

from scripts.reverse.re335_door_save_runtime_helper_candidate_callsite_map import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_door_save_runtime_helper_candidate_callsite_map,
    write_all_artifacts,
)


def test_re335_builds_source_backed_callsite_map_without_authorizing_patch():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_door_save_runtime_helper_candidate_callsite_map(repo)

    assert bundle.summary.story_id == "RE-335"
    assert bundle.summary.topic == "door-save-runtime-helper-candidate-callsite-map"
    assert bundle.summary.upstream_handoff == "RE-334"
    assert bundle.summary.selected_candidate_id == "f457f2772655"
    assert bundle.summary.source_context_function_count == 14
    assert bundle.summary.source_backed_callsite_count == 185
    assert bundle.summary.implemented_context_function_count == 13
    assert bundle.summary.stub_context_function_count == 1
    assert bundle.summary.no_callsite_context_function_count == 0
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-336"
    assert bundle.summary.next_topic == "door-save-runtime-helper-callsite-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.function_rows) == 14
    assert len(bundle.callsite_rows) == 185
    first_function = bundle.function_rows[0]
    assert first_function.caller_symbol == "OpenThatDoor"
    assert first_function.source_file == "GAME/DOOR.C"
    assert first_function.definition_line == 236
    assert first_function.end_line == 239
    assert first_function.source_backed_callsite_count == 1
    assert first_function.function_status == "stub-unimplemented"

    spotcam = next(row for row in bundle.function_rows if row.caller_symbol == "CalculateSpotCams")
    assert spotcam.source_file == "GAME/SPOTCAM.C"
    assert spotcam.definition_line == 429
    assert spotcam.end_line == 1089
    assert spotcam.source_backed_callsite_count == 42
    assert spotcam.function_status == "source-with-calls"

    first_callsite = bundle.callsite_rows[0]
    assert first_callsite.caller_symbol == "OpenThatDoor"
    assert first_callsite.source_line == 238
    assert first_callsite.callee_symbol == "UNIMPLEMENTED"
    assert first_callsite.callsite_family == "stub-marker"
    assert first_callsite.candidate_level_proof == "no"
    assert first_callsite.ready_to_reopen_domain == "no"
    assert first_callsite.source_patch_authorized == "no"

    assert any(row.caller_symbol == "sgSaveGame" and row.callee_symbol == "SaveLaraData" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "DoLevel" and row.callee_symbol == "sgRestoreGame" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "CalculateSpotCams" and row.callee_symbol == "CalculateCamera" for row in bundle.callsite_rows)

    for row in bundle.function_rows + bundle.callsite_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "unimplemented();" not in row_text


def test_re335_writes_metadata_only_callsite_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_door_save_runtime_helper_candidate_callsite_map(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"functions_csv", "callsites_csv", "gate_csv", "summary_csv", "handoff_csv", "md", "story"}

    functions = list(csv.DictReader(written["functions_csv"].open(newline="", encoding="utf-8")))
    assert len(functions) == 14
    assert "source_line_text" not in functions[0]
    assert functions[0]["caller_symbol"] == "OpenThatDoor"
    assert functions[0]["definition_line"] == "236"
    assert functions[0]["function_status"] == "stub-unimplemented"

    callsites = list(csv.DictReader(written["callsites_csv"].open(newline="", encoding="utf-8")))
    assert len(callsites) == 185
    assert "source_line_text" not in callsites[0]
    assert callsites[0]["source_line"] == "238"
    assert callsites[0]["callee_symbol"] == "UNIMPLEMENTED"

    gate = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert gate == [
        {
            "rank": "1",
            "candidate_id": "f457f2772655",
            "source_context_function_count": "14",
            "source_backed_callsite_count": "185",
            "implemented_context_function_count": "13",
            "stub_context_function_count": "1",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-callsite-map-needs-readiness-gate",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-336",
            "next_topic": "door-save-runtime-helper-callsite-readiness-gate",
            "stop_condition": "source-backed callsites exist but still need a readiness gate before domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-336"
    assert handoff["selected_candidate_id"] == "f457f2772655"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-334 proof-export handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-336" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-335 door-save-runtime helper candidate callsite map" in md
    assert "Source-backed callsite rows are not source-patch authorization" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
