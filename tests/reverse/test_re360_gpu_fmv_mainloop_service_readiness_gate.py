from pathlib import Path
import csv

from scripts.reverse.re360_gpu_fmv_mainloop_service_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_gpu_fmv_mainloop_service_readiness_gate,
    write_all_artifacts,
)


def test_re360_gates_gpu_fmv_mainloop_without_reopening_domain():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_gpu_fmv_mainloop_service_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-360"
    assert bundle.summary.topic == "gpu-fmv-mainloop-service-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-359"
    assert bundle.summary.selected_narrow_subcluster == "gpu-fmv-mainloop-service"
    assert bundle.summary.input_candidate_count == 1
    assert bundle.summary.candidate_gate_count == 1
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.selected_followup_candidate_id == "1b3534d34062"
    assert bundle.summary.next_ticket == "RE-361"
    assert bundle.summary.next_topic == "gpu-fmv-mainloop-service-candidate-proof-export"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.candidate_rows) == 1
    candidate = bundle.candidate_rows[0]
    assert candidate.rank == 1
    assert candidate.source_rank == 18
    assert candidate.candidate_id == "1b3534d34062"
    assert candidate.gpu_fmv_mainloop_context_count == 5
    assert candidate.proof_signal_class == "caller-gpu-fmv-mainloop-context-only"
    assert candidate.readiness_gate == "blocked-needs-candidate-level-proof"
    assert candidate.ready_to_reopen_domain == "no"
    assert candidate.source_patch_authorized == "no"
    assert candidate.next_probe == "candidate-proof-export"

    gate = bundle.gate_rows[0]
    assert gate.gate_class == "candidate-level-source-symbolic-proof-missing"
    assert gate.candidate_count == 1
    assert gate.representative_candidates == "1b3534d34062"
    assert gate.gate_decision == "request-still-narrower-export"
    assert gate.ready_to_reopen_domain == "no"
    assert gate.source_patch_authorized == "no"
    assert gate.next_ticket == "RE-361"
    assert gate.next_topic == "gpu-fmv-mainloop-service-candidate-proof-export"

    for row in bundle.candidate_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text


def test_re360_writes_metadata_only_readiness_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_gpu_fmv_mainloop_service_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"candidates_csv", "gates_csv", "summary_csv", "handoff_csv", "md", "story"}

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert len(candidates) == 1
    assert "ghidra_entry" not in candidates[0]
    assert "ghidra_name" not in candidates[0]
    assert candidates[0]["candidate_id"] == "1b3534d34062"
    assert candidates[0]["gpu_fmv_mainloop_context_count"] == "5"
    assert candidates[0]["readiness_gate"] == "blocked-needs-candidate-level-proof"
    assert candidates[0]["next_probe"] == "candidate-proof-export"

    gates = list(csv.DictReader(written["gates_csv"].open(newline="", encoding="utf-8")))
    assert gates == [
        {
            "rank": "1",
            "gate_class": "candidate-level-source-symbolic-proof-missing",
            "candidate_count": "1",
            "representative_candidates": "1b3534d34062",
            "gate_decision": "request-still-narrower-export",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-361",
            "next_topic": "gpu-fmv-mainloop-service-candidate-proof-export",
            "stop_condition": "candidate-level source-symbolic proof is required before proof-domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-361"
    assert handoff["next_topic"] == "gpu-fmv-mainloop-service-candidate-proof-export"
    assert handoff["selected_followup_candidate_id"] == "1b3534d34062"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["metadata_work_readiness"] == "ready"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-359 gpu/fmv mainloop service handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-361" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-360 gpu/fmv mainloop service readiness gate" in md
    assert "No proof-domain is reopened by this gate" in md

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
    for path in (written["candidates_csv"], written["gates_csv"], written["summary_csv"], written["handoff_csv"]):
        header = path.read_text(encoding="utf-8").splitlines()[0].split(",")
        assert raw_columns.isdisjoint(header)

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
