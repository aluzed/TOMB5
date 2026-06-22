from pathlib import Path
import csv

from scripts.reverse.re381_explosion_flare_effect_service_candidate_callsite_map import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_explosion_flare_effect_service_candidate_callsite_map,
    write_all_artifacts,
)


def test_re381_builds_explosion_flare_source_backed_callsite_map_without_authorizing_patch():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_explosion_flare_effect_service_candidate_callsite_map(repo)

    assert bundle.summary.story_id == "RE-381"
    assert bundle.summary.topic == "explosion-flare-effect-service-candidate-callsite-map"
    assert bundle.summary.upstream_handoff == "RE-380"
    assert bundle.summary.selected_candidate_id == "87d9c8a62335"
    assert bundle.summary.source_context_function_count == 18
    assert bundle.summary.source_backed_callsite_count == 121
    assert bundle.summary.implemented_context_function_count == 12
    assert bundle.summary.stub_context_function_count == 6
    assert bundle.summary.no_callsite_context_function_count == 0
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-382"
    assert bundle.summary.next_topic == "explosion-flare-effect-service-callsite-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.function_rows) == 18
    assert len(bundle.callsite_rows) == 121

    first_function = bundle.function_rows[0]
    assert first_function.caller_symbol == "CalculateCamera"
    assert first_function.source_file == "GAME/CAMERA.C"
    assert first_function.definition_line == 1167
    assert first_function.end_line == 1594
    assert first_function.source_backed_callsite_count == 20
    assert first_function.function_status == "stub-unimplemented"

    flare_symbols = {row.caller_symbol for row in bundle.function_rows if row.source_file == "GAME/LARAFLAR.C"}
    assert flare_symbols == {"CreateFlare", "DoFlareInHand"}

    first_callsite = bundle.callsite_rows[0]
    assert first_callsite.caller_symbol == "CalculateCamera"
    assert first_callsite.callee_symbol == "BinocularCamera"
    assert first_callsite.source_line == 1196
    assert first_callsite.callsite_family == "audio-camera-helper"
    assert first_callsite.candidate_level_proof == "no"
    assert first_callsite.ready_to_reopen_domain == "no"
    assert first_callsite.source_patch_authorized == "no"

    assert any(row.caller_symbol == "CreateFlare" and row.callee_symbol == "UNIMPLEMENTED" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "DoFlareInHand" and row.callee_symbol == "DoFlareLight" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "CutLaraBubbles" and row.callee_symbol == "CreateBubble" for row in bundle.callsite_rows)
    assert any(row.caller_symbol == "FlameControl" and row.callee_symbol == "TriggerFireFlame" for row in bundle.callsite_rows)

    for row in bundle.function_rows + bundle.callsite_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "source_line_text" not in row_text


def test_re381_writes_metadata_only_callsite_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_explosion_flare_effect_service_candidate_callsite_map(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"functions_csv", "callsites_csv", "gate_csv", "summary_csv", "handoff_csv", "md", "story"}

    functions = list(csv.DictReader(written["functions_csv"].open(newline="", encoding="utf-8")))
    assert len(functions) == 18
    assert "source_line_text" not in functions[0]
    assert functions[0]["caller_symbol"] == "CalculateCamera"
    assert functions[0]["definition_line"] == "1167"
    assert functions[0]["function_status"] == "stub-unimplemented"

    callsites = list(csv.DictReader(written["callsites_csv"].open(newline="", encoding="utf-8")))
    assert len(callsites) == 121
    assert "source_line_text" not in callsites[0]
    assert callsites[0]["callee_symbol"] == "BinocularCamera"

    gate = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert gate == [
        {
            "rank": "1",
            "candidate_id": "87d9c8a62335",
            "source_context_function_count": "18",
            "source_backed_callsite_count": "121",
            "implemented_context_function_count": "12",
            "stub_context_function_count": "6",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-callsite-map-needs-readiness-gate",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-382",
            "next_topic": "explosion-flare-effect-service-callsite-readiness-gate",
            "stop_condition": "source-backed explosion/flare callsites exist but still need a readiness gate before domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-382"
    assert handoff["selected_candidate_id"] == "87d9c8a62335"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-380 proof-export handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-382" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-381 explosion/flare effect service candidate callsite map" in md
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
