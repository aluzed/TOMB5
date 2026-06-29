from pathlib import Path
import csv

from scripts.reverse.re386_spotcam_projectile_effect_service_candidate_callsite_map import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_spotcam_projectile_effect_service_candidate_callsite_map,
    write_all_artifacts,
)


def test_re386_maps_spotcam_projectile_callsite_metadata_without_authorizing_patch():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_spotcam_projectile_effect_service_candidate_callsite_map(repo)

    assert bundle.summary.story_id == "RE-386"
    assert bundle.summary.topic == "spotcam-projectile-effect-service-candidate-callsite-map"
    assert bundle.summary.upstream_handoff == "RE-385"
    assert bundle.summary.selected_candidate_id == "b6d128932004"
    assert bundle.summary.source_context_function_count == 52
    assert bundle.summary.source_backed_callsite_count == 296
    assert bundle.summary.implemented_context_function_count == 33
    assert bundle.summary.stub_context_function_count == 19
    assert bundle.summary.no_callsite_context_function_count == 0
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-387"
    assert bundle.summary.next_topic == "spotcam-projectile-effect-service-callsite-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.function_rows) == 52
    assert len(bundle.callsite_rows) == 296
    assert len([row for row in bundle.function_rows if row.function_status == "source-with-calls"]) == 33
    assert len([row for row in bundle.function_rows if row.function_status == "stub-unimplemented"]) == 19
    assert {row.caller_symbol for row in bundle.function_rows if row.function_status == "source-no-callsite"} == set()

    spotcam = [row for row in bundle.function_rows if row.caller_symbol == "CalculateSpotCams"]
    assert len(spotcam) == 1
    assert spotcam[0].source_file == "GAME/SPOTCAM.C"
    assert spotcam[0].source_backed_callsite_count == 5

    projectile_callers = {row.caller_symbol for row in bundle.callsite_rows if row.callsite_family == "spotcam-projectile-helper"}
    assert {"ControlBodyPart", "CalculateSpotCams"}.issubset(projectile_callers)
    assert {row.callee_symbol for row in bundle.callsite_rows if row.callsite_family == "spotcam-projectile-helper"} >= {
        "GetRandomControl",
        "GetLaraJointPos",
    }
    assert {row.callee_symbol for row in bundle.callsite_rows if row.callsite_family == "stub-marker"} == {"UNIMPLEMENTED"}

    gate = bundle.gate_rows[0]
    assert gate.readiness_gate == "blocked-callsite-map-needs-readiness-gate"
    assert gate.ready_to_reopen_domain == "no"
    assert gate.source_patch_authorized == "no"
    assert gate.next_ticket == "RE-387"

    for row in bundle.function_rows + bundle.callsite_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text


def test_re386_writes_metadata_only_callsite_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_spotcam_projectile_effect_service_candidate_callsite_map(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"functions_csv", "callsites_csv", "gate_csv", "summary_csv", "handoff_csv", "md", "story"}

    functions = list(csv.DictReader(written["functions_csv"].open(newline="", encoding="utf-8")))
    assert len(functions) == 52
    assert "source_line_text" not in functions[0]
    assert functions[0]["candidate_id"] == "b6d128932004"
    assert functions[0]["caller_symbol"] == "MoveCamera"

    callsites = list(csv.DictReader(written["callsites_csv"].open(newline="", encoding="utf-8")))
    assert len(callsites) == 296
    assert "source_line_text" not in callsites[0]
    assert {row["callsite_family"] for row in callsites} >= {
        "spotcam-projectile-helper",
        "trap-effect-helper",
        "room-floor-helper",
        "runtime-effect-support",
        "stub-marker",
    }

    gate = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert gate == [
        {
            "rank": "1",
            "candidate_id": "b6d128932004",
            "source_context_function_count": "52",
            "source_backed_callsite_count": "296",
            "implemented_context_function_count": "33",
            "stub_context_function_count": "19",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-callsite-map-needs-readiness-gate",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-387",
            "next_topic": "spotcam-projectile-effect-service-callsite-readiness-gate",
            "stop_condition": "source-backed spotcam/projectile callsites exist but still need a readiness gate before domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-387"
    assert handoff["next_topic"] == "spotcam-projectile-effect-service-callsite-readiness-gate"
    assert handoff["selected_candidate_id"] == "b6d128932004"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-385 proof-export handoff validated." in story
    assert "RE-387" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-386 spotcam/projectile effect service candidate callsite map" in md
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
