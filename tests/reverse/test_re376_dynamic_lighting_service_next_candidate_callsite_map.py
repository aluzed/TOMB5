from pathlib import Path
import csv

from scripts.reverse.re376_dynamic_lighting_service_next_candidate_callsite_map import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_dynamic_lighting_service_next_candidate_callsite_map,
    write_all_artifacts,
)


def test_re376_builds_next_candidate_source_backed_callsite_map_without_authorizing_patch():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_dynamic_lighting_service_next_candidate_callsite_map(repo)

    assert bundle.summary.story_id == "RE-376"
    assert bundle.summary.topic == "dynamic-lighting-service-next-candidate-callsite-map"
    assert bundle.summary.upstream_handoff == "RE-375"
    assert bundle.summary.previous_candidate_id == "f5d0099b5511"
    assert bundle.summary.selected_candidate_id == "3a208e2bf745"
    assert bundle.summary.source_context_function_count == 21
    assert bundle.summary.source_backed_callsite_count == 40
    assert bundle.summary.implemented_context_function_count == 9
    assert bundle.summary.stub_context_function_count == 12
    assert bundle.summary.no_callsite_context_function_count == 0
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-377"
    assert bundle.summary.next_topic == "dynamic-lighting-service-next-candidate-callsite-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.function_rows) == 21
    assert len(bundle.callsite_rows) == 40

    first_function = bundle.function_rows[0]
    assert first_function.previous_candidate_id == "f5d0099b5511"
    assert first_function.candidate_id == "3a208e2bf745"
    assert first_function.caller_symbol == "GenericSphereBoxCollision"
    assert first_function.source_file == "GAME/COLLIDE.C"
    assert first_function.definition_line == 99
    assert first_function.end_line == 102
    assert first_function.source_backed_callsite_count == 1
    assert first_function.function_status == "stub-unimplemented"

    dynamic_control_symbols = {row.caller_symbol for row in bundle.function_rows if row.source_file == "GAME/OBJLIGHT.C"}
    assert dynamic_control_symbols == {
        "ControlBlinker",
        "ControlColouredLight",
        "ControlElectricalLight",
        "ControlPulseLight",
        "ControlStrobeLight",
    }

    first_callsite = bundle.callsite_rows[0]
    assert first_callsite.previous_candidate_id == "f5d0099b5511"
    assert first_callsite.candidate_id == "3a208e2bf745"
    assert first_callsite.caller_symbol == "GenericSphereBoxCollision"
    assert first_callsite.callee_symbol == "UNIMPLEMENTED"
    assert first_callsite.source_line == 101
    assert first_callsite.callsite_family == "stub-marker"
    assert first_callsite.candidate_level_proof == "no"
    assert first_callsite.ready_to_reopen_domain == "no"
    assert first_callsite.source_patch_authorized == "no"

    assert any(row.caller_symbol == "ControlBlinker" and row.callee_symbol == "TriggerDynamic" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "ControlStrobeLight" and row.callee_symbol == "TriggerAlertLight" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "FlameEmitter2Control" and row.callee_symbol == "AddFire" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "TurnSwitchCollision" and row.callee_symbol == "ItemPushLara" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "RollingBallCollision" and row.callee_symbol == "ObjectCollision" for row in bundle.callsite_rows)

    for row in bundle.function_rows + bundle.callsite_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "source_line_text" not in row_text


def test_re376_writes_metadata_only_next_candidate_callsite_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_dynamic_lighting_service_next_candidate_callsite_map(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"functions_csv", "callsites_csv", "gate_csv", "summary_csv", "handoff_csv", "md", "story"}

    functions = list(csv.DictReader(written["functions_csv"].open(newline="", encoding="utf-8")))
    assert len(functions) == 21
    assert "source_line_text" not in functions[0]
    assert functions[0]["previous_candidate_id"] == "f5d0099b5511"
    assert functions[0]["candidate_id"] == "3a208e2bf745"
    assert functions[0]["caller_symbol"] == "GenericSphereBoxCollision"
    assert functions[0]["definition_line"] == "99"
    assert functions[0]["function_status"] == "stub-unimplemented"

    callsites = list(csv.DictReader(written["callsites_csv"].open(newline="", encoding="utf-8")))
    assert len(callsites) == 40
    assert "source_line_text" not in callsites[0]
    assert callsites[0]["callee_symbol"] == "UNIMPLEMENTED"

    gate = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert gate == [
        {
            "rank": "1",
            "previous_candidate_id": "f5d0099b5511",
            "candidate_id": "3a208e2bf745",
            "source_context_function_count": "21",
            "source_backed_callsite_count": "40",
            "implemented_context_function_count": "9",
            "stub_context_function_count": "12",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-next-candidate-callsite-map-needs-readiness-gate",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-377",
            "next_topic": "dynamic-lighting-service-next-candidate-callsite-readiness-gate",
            "stop_condition": "source-backed next-candidate dynamic-lighting callsites exist but still need a readiness gate before domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-377"
    assert handoff["previous_candidate_id"] == "f5d0099b5511"
    assert handoff["selected_candidate_id"] == "3a208e2bf745"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-375 next-candidate proof-export handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-377" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-376 dynamic-lighting service next-candidate callsite map" in md
    assert "Source-backed callsite rows are not source-patch authorization" in md

    raw_columns = {
        "ghidra_entry",
        "ghidra_name",
        "call_address",
        "payload_offset",
        "word_le_hex",
        "opcode",
        "raw_evidence",
        "source_line_text",
    }
    for path in (written["functions_csv"], written["callsites_csv"], written["gate_csv"], written["summary_csv"], written["handoff_csv"]):
        header = path.read_text(encoding="utf-8").splitlines()[0].split(",")
        assert raw_columns.isdisjoint(header)

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
