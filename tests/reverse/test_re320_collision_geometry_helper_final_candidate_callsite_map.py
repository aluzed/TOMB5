from pathlib import Path
import csv

from scripts.reverse.re320_collision_geometry_helper_final_candidate_callsite_map import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_collision_geometry_helper_final_candidate_callsite_map,
    write_all_artifacts,
)


def test_re320_builds_final_candidate_source_backed_callsite_map_without_authorizing_patch():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_geometry_helper_final_candidate_callsite_map(repo)

    assert bundle.summary.story_id == "RE-320"
    assert bundle.summary.topic == "collision-geometry-helper-final-candidate-callsite-map"
    assert bundle.summary.upstream_handoff == "RE-319"
    assert bundle.summary.selected_candidate_id == "61d55bb1809b"
    assert bundle.summary.previous_candidate_id == "d96359c1d9f3"
    assert bundle.summary.source_context_function_count == 20
    assert bundle.summary.source_backed_callsite_count == 28
    assert bundle.summary.implemented_context_function_count == 4
    assert bundle.summary.stub_context_function_count == 15
    assert bundle.summary.no_callsite_context_function_count == 1
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-321"
    assert bundle.summary.next_topic == "collision-geometry-helper-final-candidate-callsite-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.function_rows) == 20
    assert len(bundle.callsite_rows) == 28
    assert {row.function_status for row in bundle.function_rows} == {
        "source-with-calls",
        "stub-unimplemented",
        "source-no-callsite",
    }
    assert sum(row.function_status == "source-with-calls" for row in bundle.function_rows) == 4
    assert sum(row.function_status == "stub-unimplemented" for row in bundle.function_rows) == 15
    assert sum(row.function_status == "source-no-callsite" for row in bundle.function_rows) == 1

    first = bundle.callsite_rows[0]
    assert first.caller_symbol == "TrapCollision"
    assert first.source_file == "GAME/COLLIDE.C"
    assert first.source_line == 364
    assert first.callee_symbol == "TestBoundsCollide"
    assert first.callsite_family == "collision-helper"
    assert first.candidate_level_proof == "no"
    assert first.ready_to_reopen_domain == "no"
    assert first.source_patch_authorized == "no"

    rolling_rows = [row for row in bundle.callsite_rows if row.caller_symbol == "RollingBallCollision"]
    assert [row.callee_symbol for row in rolling_rows] == [
        "TestBoundsCollide",
        "TestCollision",
        "TriggerActive",
        "ObjectCollision",
    ]

    for row in bundle.function_rows + bundle.callsite_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "unimplemented();" not in row_text


def test_re320_writes_metadata_only_final_candidate_callsite_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_geometry_helper_final_candidate_callsite_map(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"functions_csv", "callsites_csv", "gate_csv", "summary_csv", "handoff_csv", "md", "story"}

    functions = list(csv.DictReader(written["functions_csv"].open(newline="", encoding="utf-8")))
    assert len(functions) == 20
    assert "source_line_text" not in functions[0]
    assert functions[0]["candidate_id"] == "61d55bb1809b"
    assert functions[0]["caller_symbol"] == "TrapCollision"
    assert functions[0]["definition_line"] == "358"
    assert functions[0]["function_status"] == "source-with-calls"

    callsites = list(csv.DictReader(written["callsites_csv"].open(newline="", encoding="utf-8")))
    assert len(callsites) == 28
    assert "source_line_text" not in callsites[0]
    assert callsites[0]["candidate_id"] == "61d55bb1809b"
    assert callsites[0]["source_line"] == "364"
    assert callsites[0]["callee_symbol"] == "TestBoundsCollide"

    gate = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert gate == [
        {
            "rank": "1",
            "candidate_id": "61d55bb1809b",
            "previous_candidate_id": "d96359c1d9f3",
            "source_context_function_count": "20",
            "source_backed_callsite_count": "28",
            "implemented_context_function_count": "4",
            "stub_context_function_count": "15",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-final-candidate-callsite-map-needs-readiness-gate",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-321",
            "next_topic": "collision-geometry-helper-final-candidate-callsite-readiness-gate",
            "stop_condition": "final-candidate source-backed callsites exist but still need a readiness gate before domain selection or queue exhaustion",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-321"
    assert handoff["selected_candidate_id"] == "61d55bb1809b"
    assert handoff["previous_candidate_id"] == "d96359c1d9f3"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-319 final-candidate callsite-map handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-321" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-320 collision geometry helper final candidate callsite map" in md
    assert "Final-candidate source-backed callsite rows are not source-patch authorization" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
