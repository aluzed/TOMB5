from pathlib import Path
import csv

from scripts.reverse.re346_cd_load_audio_service_candidate_callsite_map import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_cd_load_audio_service_candidate_callsite_map,
    write_all_artifacts,
)


def test_re346_builds_source_backed_callsite_map_without_authorizing_patch():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_cd_load_audio_service_candidate_callsite_map(repo)

    assert bundle.summary.story_id == "RE-346"
    assert bundle.summary.topic == "cd-load-audio-service-candidate-callsite-map"
    assert bundle.summary.upstream_handoff == "RE-345"
    assert bundle.summary.selected_candidate_id == "1e35f3f4fb97"
    assert bundle.summary.source_context_function_count == 34
    assert bundle.summary.source_backed_callsite_count == 266
    assert bundle.summary.implemented_context_function_count == 32
    assert bundle.summary.stub_context_function_count == 0
    assert bundle.summary.no_callsite_context_function_count == 2
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-347"
    assert bundle.summary.next_topic == "cd-load-audio-service-callsite-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.function_rows) == 34
    assert len(bundle.callsite_rows) == 266
    first_function = bundle.function_rows[0]
    assert first_function.caller_symbol == "DEL_CDFS_Read"
    assert first_function.source_file == "SPEC_PSX/CD.C"
    assert first_function.definition_line == 456
    assert first_function.end_line == 503
    assert first_function.source_backed_callsite_count == 12
    assert first_function.function_status == "source-with-calls"

    pc_cd_mode = next(row for row in bundle.function_rows if row.caller_symbol == "DEL_ChangeCDMode" and row.source_file == "SPEC_PSXPC/CD.C")
    assert pc_cd_mode.source_backed_callsite_count == 0
    assert pc_cd_mode.function_status == "source-no-callsite"

    first_callsite = bundle.callsite_rows[0]
    assert first_callsite.caller_symbol == "DEL_CDFS_Read"
    assert first_callsite.callee_symbol == "DEL_ChangeCDMode"
    assert first_callsite.source_line == 463
    assert first_callsite.callsite_family == "cd-audio-helper"
    assert first_callsite.candidate_level_proof == "no"
    assert first_callsite.ready_to_reopen_domain == "no"
    assert first_callsite.source_patch_authorized == "no"

    assert any(row.caller_symbol == "LOAD_Start" and row.callee_symbol == "DEL_CDFS_Read" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "main" and row.callee_symbol == "CDDA_SetMasterVolume" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "S_PlayFMV" and row.callee_symbol == "FMV_InitialiseVRAM" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "GPU_FlipToBuffer" and row.callee_symbol == "PutDrawEnv" for row in bundle.callsite_rows)

    for row in bundle.function_rows + bundle.callsite_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "source_line_text" not in row_text


def test_re346_writes_metadata_only_callsite_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_cd_load_audio_service_candidate_callsite_map(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"functions_csv", "callsites_csv", "gate_csv", "summary_csv", "handoff_csv", "md", "story"}

    functions = list(csv.DictReader(written["functions_csv"].open(newline="", encoding="utf-8")))
    assert len(functions) == 34
    assert "source_line_text" not in functions[0]
    assert functions[0]["caller_symbol"] == "DEL_CDFS_Read"
    assert functions[0]["definition_line"] == "456"
    assert functions[0]["function_status"] == "source-with-calls"

    callsites = list(csv.DictReader(written["callsites_csv"].open(newline="", encoding="utf-8")))
    assert len(callsites) == 266
    assert "source_line_text" not in callsites[0]
    assert callsites[0]["callee_symbol"] == "DEL_ChangeCDMode"

    gate = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert gate == [
        {
            "rank": "1",
            "candidate_id": "1e35f3f4fb97",
            "source_context_function_count": "34",
            "source_backed_callsite_count": "266",
            "implemented_context_function_count": "32",
            "stub_context_function_count": "0",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-callsite-map-needs-readiness-gate",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-347",
            "next_topic": "cd-load-audio-service-callsite-readiness-gate",
            "stop_condition": "source-backed cd/load/audio callsites exist but still need a readiness gate before domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-347"
    assert handoff["selected_candidate_id"] == "1e35f3f4fb97"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-345 proof-export handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-347" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-346 cd-load-audio service candidate callsite map" in md
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
