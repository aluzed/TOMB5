from pathlib import Path
import csv

from scripts.reverse.re374_dynamic_lighting_service_callsite_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_dynamic_lighting_service_callsite_readiness_gate,
    write_all_artifacts,
)


def test_re374_gates_dynamic_lighting_callsite_families_and_selects_next_candidate():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_dynamic_lighting_service_callsite_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-374"
    assert bundle.summary.topic == "dynamic-lighting-service-callsite-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-373"
    assert bundle.summary.selected_candidate_id == "f5d0099b5511"
    assert bundle.summary.next_candidate_id == "3a208e2bf745"
    assert bundle.summary.source_context_function_count == 23
    assert bundle.summary.source_backed_callsite_count == 129
    assert bundle.summary.callsite_family_count == 7
    assert bundle.summary.implemented_callsite_family_count == 6
    assert bundle.summary.stub_only_callsite_family_count == 1
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-375"
    assert bundle.summary.next_topic == "dynamic-lighting-service-next-candidate-proof-export"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.callsite_family for row in bundle.family_rows] == [
        "control-flow-helper",
        "dynamic-light-trigger",
        "joint-position-helper",
        "effect-state-helper",
        "effects-lighting-trigger",
        "room-floor-helper",
        "stub-marker",
    ]
    assert [row.source_backed_callsite_count for row in bundle.family_rows] == [55, 32, 14, 9, 7, 5, 7]
    assert [row.implemented_callsite_count for row in bundle.family_rows] == [55, 32, 14, 9, 7, 5, 0]
    assert [row.stub_callsite_count for row in bundle.family_rows] == [0, 0, 0, 0, 0, 0, 7]
    assert [row.implemented_caller_count for row in bundle.family_rows] == [10, 16, 9, 5, 3, 3, 0]
    assert all(row.candidate_level_proof == "no" for row in bundle.family_rows)
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.family_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.family_rows)
    assert bundle.family_rows[-1].readiness_gate == "blocked-stub-only-family"
    assert all(row.readiness_gate.startswith("blocked-") for row in bundle.family_rows)

    decision = bundle.decision_rows[0]
    assert decision.readiness_gate == "blocked-no-callsite-family-proves-candidate"
    assert decision.decision == "deny-domain-reopen"
    assert decision.next_candidate_id == "3a208e2bf745"
    assert decision.next_ticket == "RE-375"

    for row in bundle.family_rows + bundle.decision_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "source_line_text" not in row_text


def test_re374_writes_metadata_only_callsite_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_dynamic_lighting_service_callsite_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"families_csv", "decision_csv", "summary_csv", "handoff_csv", "md", "story"}

    families = list(csv.DictReader(written["families_csv"].open(newline="", encoding="utf-8")))
    assert len(families) == 7
    assert "source_line_text" not in families[0]
    assert families[0]["candidate_id"] == "f5d0099b5511"
    assert families[0]["callsite_family"] == "control-flow-helper"
    assert families[0]["source_backed_callsite_count"] == "55"
    assert families[0]["implemented_callsite_count"] == "55"
    assert families[0]["readiness_gate"] == "blocked-no-candidate-level-proof"
    assert families[-1]["callsite_family"] == "stub-marker"
    assert families[-1]["readiness_gate"] == "blocked-stub-only-family"

    decision = list(csv.DictReader(written["decision_csv"].open(newline="", encoding="utf-8")))
    assert decision == [
        {
            "rank": "1",
            "candidate_id": "f5d0099b5511",
            "callsite_family_count": "7",
            "implemented_callsite_family_count": "6",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-no-callsite-family-proves-candidate",
            "decision": "deny-domain-reopen",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "selected_domain": "none",
            "selected_pivot": "none",
            "next_ticket": "RE-375",
            "next_topic": "dynamic-lighting-service-next-candidate-proof-export",
            "next_candidate_id": "3a208e2bf745",
            "stop_condition": "source-backed dynamic-lighting callsite families do not prove candidate-level behavior",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-375"
    assert handoff["selected_candidate_id"] == "f5d0099b5511"
    assert handoff["next_candidate_id"] == "3a208e2bf745"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-373 callsite handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-375" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-374 dynamic-lighting service callsite readiness gate" in md
    assert "No dynamic-lighting callsite family proves candidate-level behavior" in md

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
    for path in (written["families_csv"], written["decision_csv"], written["summary_csv"], written["handoff_csv"]):
        header = path.read_text(encoding="utf-8").splitlines()[0].split(",")
        assert raw_columns.isdisjoint(header)

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
