from pathlib import Path
import csv

from scripts.reverse.re357_frontend_display_menu_service_next_candidate_callsite_map import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_frontend_display_menu_service_next_candidate_callsite_map,
    write_all_artifacts,
)


def test_re357_builds_next_candidate_source_backed_callsite_map_without_authorizing_patch():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_frontend_display_menu_service_next_candidate_callsite_map(repo)

    assert bundle.summary.story_id == "RE-357"
    assert bundle.summary.topic == "frontend-display-menu-service-next-candidate-callsite-map"
    assert bundle.summary.upstream_handoff == "RE-356"
    assert bundle.summary.selected_candidate_id == "4c90c6af8f9d"
    assert bundle.summary.previous_candidate_id == "de919274685f"
    assert bundle.summary.source_context_function_count == 18
    assert bundle.summary.source_backed_callsite_count == 126
    assert bundle.summary.implemented_context_function_count == 17
    assert bundle.summary.stub_context_function_count == 0
    assert bundle.summary.no_callsite_context_function_count == 1
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-358"
    assert bundle.summary.next_topic == "frontend-display-menu-service-next-candidate-callsite-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.function_rows) == 18
    assert len(bundle.callsite_rows) == 126

    first_function = bundle.function_rows[0]
    assert first_function.caller_symbol == "DrawGameInfo"
    assert first_function.source_file == "GAME/HEALTH.C"
    assert first_function.definition_line == 203
    assert first_function.end_line == 283
    assert first_function.source_backed_callsite_count == 6
    assert first_function.function_status == "source-with-calls"

    no_callsite_symbols = {(row.caller_symbol, row.source_file) for row in bundle.function_rows if row.function_status == "source-no-callsite"}
    assert no_callsite_symbols == {("DisplayConfig", "SPEC_PSXPC/SPECIFIC.C")}

    first_callsite = bundle.callsite_rows[0]
    assert first_callsite.caller_symbol == "DrawGameInfo"
    assert first_callsite.callee_symbol == "PrintString"
    assert first_callsite.source_line == 238
    assert first_callsite.callsite_family == "text-ui-helper"
    assert first_callsite.candidate_level_proof == "no"
    assert first_callsite.ready_to_reopen_domain == "no"
    assert first_callsite.source_patch_authorized == "no"

    assert any(row.caller_symbol == "draw_current_object_list" and row.callee_symbol == "SoundEffect" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "FILE_Load" and row.callee_symbol == "DEL_CDFS_Read" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "DisplayFiles" and row.callee_symbol == "strcpy" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "InitNewCDSystem" and row.callee_symbol == "VSync" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "DisplayConfig" and row.callee_symbol == "PrintString" for row in bundle.callsite_rows)

    for row in bundle.function_rows + bundle.callsite_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "source_line_text" not in row_text


def test_re357_writes_metadata_only_callsite_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_frontend_display_menu_service_next_candidate_callsite_map(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"functions_csv", "callsites_csv", "gate_csv", "summary_csv", "handoff_csv", "md", "story"}

    functions = list(csv.DictReader(written["functions_csv"].open(newline="", encoding="utf-8")))
    assert len(functions) == 18
    assert "source_line_text" not in functions[0]
    assert functions[0]["candidate_id"] == "4c90c6af8f9d"
    assert functions[0]["caller_symbol"] == "DrawGameInfo"
    assert functions[0]["definition_line"] == "203"
    assert functions[0]["function_status"] == "source-with-calls"

    callsites = list(csv.DictReader(written["callsites_csv"].open(newline="", encoding="utf-8")))
    assert len(callsites) == 126
    assert "source_line_text" not in callsites[0]
    assert callsites[0]["callee_symbol"] == "PrintString"

    gate = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert gate == [
        {
            "rank": "1",
            "candidate_id": "4c90c6af8f9d",
            "previous_candidate_id": "de919274685f",
            "source_context_function_count": "18",
            "source_backed_callsite_count": "126",
            "implemented_context_function_count": "17",
            "stub_context_function_count": "0",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-next-candidate-callsite-map-needs-readiness-gate",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-358",
            "next_topic": "frontend-display-menu-service-next-candidate-callsite-readiness-gate",
            "stop_condition": "next frontend display/menu candidate has source-backed callsites but still needs a readiness gate before domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-358"
    assert handoff["next_topic"] == "frontend-display-menu-service-next-candidate-callsite-readiness-gate"
    assert handoff["selected_candidate_id"] == "4c90c6af8f9d"
    assert handoff["previous_candidate_id"] == "de919274685f"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-356 next-candidate proof-export handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-358" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-357 frontend display/menu service next candidate callsite map" in md
    assert "Source-backed callsite rows are still not source-patch authorization" in md

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
