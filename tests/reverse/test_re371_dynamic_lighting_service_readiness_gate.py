from pathlib import Path
import csv

from scripts.reverse.re371_dynamic_lighting_service_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_dynamic_lighting_service_readiness_gate,
    write_all_artifacts,
)


def test_re371_gates_dynamic_lighting_service_without_reopening_domain():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_dynamic_lighting_service_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-371"
    assert bundle.summary.topic == "dynamic-lighting-service-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-370"
    assert bundle.summary.selected_narrow_subcluster == "dynamic-lighting-service"
    assert bundle.summary.input_candidate_count == 2
    assert bundle.summary.candidate_gate_count == 1
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.selected_followup_candidate_id == "f5d0099b5511"
    assert bundle.summary.next_ticket == "RE-372"
    assert bundle.summary.next_topic == "dynamic-lighting-service-candidate-proof-export"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.candidate_rows) == 2
    first, second = bundle.candidate_rows
    assert first.rank == 1
    assert first.source_rank == 9
    assert first.candidate_id == "f5d0099b5511"
    assert first.dynamic_lighting_context_count == 5
    assert first.proof_signal_class == "caller-dynamic-lighting-context-only"
    assert first.readiness_gate == "blocked-needs-candidate-level-proof"
    assert first.ready_to_reopen_domain == "no"
    assert first.source_patch_authorized == "no"
    assert first.next_probe == "candidate-proof-export"

    assert second.rank == 2
    assert second.source_rank == 11
    assert second.candidate_id == "3a208e2bf745"
    assert second.dynamic_lighting_context_count == 4
    assert second.proof_signal_class == "caller-dynamic-lighting-context-only"
    assert second.next_probe == "defer-after-re372"

    gate = bundle.gate_rows[0]
    assert gate.gate_class == "candidate-level-source-symbolic-proof-missing"
    assert gate.candidate_count == 2
    assert gate.representative_candidates == "f5d0099b5511;3a208e2bf745"
    assert gate.gate_decision == "request-still-narrower-export"
    assert gate.ready_to_reopen_domain == "no"
    assert gate.source_patch_authorized == "no"
    assert gate.next_ticket == "RE-372"
    assert gate.next_topic == "dynamic-lighting-service-candidate-proof-export"

    for row in bundle.candidate_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text


def test_re371_writes_metadata_only_readiness_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_dynamic_lighting_service_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"candidates_csv", "gates_csv", "summary_csv", "handoff_csv", "md", "story"}

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert len(candidates) == 2
    assert "ghidra_entry" not in candidates[0]
    assert "ghidra_name" not in candidates[0]
    assert candidates[0]["candidate_id"] == "f5d0099b5511"
    assert candidates[0]["dynamic_lighting_context_count"] == "5"
    assert candidates[0]["readiness_gate"] == "blocked-needs-candidate-level-proof"
    assert candidates[0]["next_probe"] == "candidate-proof-export"
    assert candidates[1]["candidate_id"] == "3a208e2bf745"
    assert candidates[1]["next_probe"] == "defer-after-re372"

    gates = list(csv.DictReader(written["gates_csv"].open(newline="", encoding="utf-8")))
    assert gates == [
        {
            "rank": "1",
            "gate_class": "candidate-level-source-symbolic-proof-missing",
            "candidate_count": "2",
            "representative_candidates": "f5d0099b5511;3a208e2bf745",
            "gate_decision": "request-still-narrower-export",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-372",
            "next_topic": "dynamic-lighting-service-candidate-proof-export",
            "stop_condition": "candidate-level source-symbolic proof is required before proof-domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-372"
    assert handoff["next_topic"] == "dynamic-lighting-service-candidate-proof-export"
    assert handoff["selected_followup_candidate_id"] == "f5d0099b5511"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["metadata_work_readiness"] == "ready"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-370 dynamic-lighting service handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-372" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-371 dynamic-lighting service readiness gate" in md
    assert "No proof-domain is reopened by this gate" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
