from pathlib import Path
import csv

from scripts.reverse.re330_weapon_switch_effect_helper_candidate_callsite_map import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_weapon_switch_effect_helper_candidate_callsite_map,
    write_all_artifacts,
)


def test_re330_builds_source_backed_callsite_map_without_authorizing_patch():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_weapon_switch_effect_helper_candidate_callsite_map(repo)

    assert bundle.summary.story_id == "RE-330"
    assert bundle.summary.topic == "weapon-switch-effect-helper-candidate-callsite-map"
    assert bundle.summary.upstream_handoff == "RE-329"
    assert bundle.summary.selected_candidate_id == "1ddbda046e37"
    assert bundle.summary.source_context_function_count == 1
    assert bundle.summary.source_backed_callsite_count == 1
    assert bundle.summary.implemented_context_function_count == 0
    assert bundle.summary.stub_context_function_count == 1
    assert bundle.summary.no_callsite_context_function_count == 0
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-331"
    assert bundle.summary.next_topic == "weapon-switch-effect-helper-callsite-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.function_rows) == 1
    assert len(bundle.callsite_rows) == 1
    function = bundle.function_rows[0]
    assert function.caller_symbol == "FireWeapon"
    assert function.source_file == "GAME/LARAFIRE.C"
    assert function.definition_line == 185
    assert function.end_line == 189
    assert function.function_status == "stub-unimplemented"

    callsite = bundle.callsite_rows[0]
    assert callsite.caller_symbol == "FireWeapon"
    assert callsite.source_file == "GAME/LARAFIRE.C"
    assert callsite.source_line == 187
    assert callsite.callee_symbol == "UNIMPLEMENTED"
    assert callsite.callsite_family == "stub-marker"
    assert callsite.candidate_level_proof == "no"
    assert callsite.ready_to_reopen_domain == "no"
    assert callsite.source_patch_authorized == "no"

    for row in bundle.function_rows + bundle.callsite_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "unimplemented();" not in row_text


def test_re330_writes_metadata_only_callsite_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_weapon_switch_effect_helper_candidate_callsite_map(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"functions_csv", "callsites_csv", "gate_csv", "summary_csv", "handoff_csv", "md", "story"}

    functions = list(csv.DictReader(written["functions_csv"].open(newline="", encoding="utf-8")))
    assert len(functions) == 1
    assert "source_line_text" not in functions[0]
    assert functions[0]["caller_symbol"] == "FireWeapon"
    assert functions[0]["definition_line"] == "185"
    assert functions[0]["function_status"] == "stub-unimplemented"

    callsites = list(csv.DictReader(written["callsites_csv"].open(newline="", encoding="utf-8")))
    assert len(callsites) == 1
    assert "source_line_text" not in callsites[0]
    assert callsites[0]["source_line"] == "187"
    assert callsites[0]["callee_symbol"] == "UNIMPLEMENTED"

    gate = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert gate == [
        {
            "rank": "1",
            "candidate_id": "1ddbda046e37",
            "source_context_function_count": "1",
            "source_backed_callsite_count": "1",
            "implemented_context_function_count": "0",
            "stub_context_function_count": "1",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-callsite-map-needs-readiness-gate",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-331",
            "next_topic": "weapon-switch-effect-helper-callsite-readiness-gate",
            "stop_condition": "source-backed callsites exist but still need a readiness gate before domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-331"
    assert handoff["selected_candidate_id"] == "1ddbda046e37"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-329 callsite-map handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-331" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-330 weapon-switch-effect helper candidate callsite map" in md
    assert "Source-backed callsite rows are not source-patch authorization" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
