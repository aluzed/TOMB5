from pathlib import Path
import csv

from scripts.reverse.re363_gpu_fmv_mainloop_service_callsite_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_gpu_fmv_mainloop_service_callsite_readiness_gate,
    write_all_artifacts,
)


def test_re363_gates_gpu_fmv_mainloop_callsite_families_and_closes_subcluster():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_gpu_fmv_mainloop_service_callsite_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-363"
    assert bundle.summary.topic == "gpu-fmv-mainloop-service-callsite-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-362"
    assert bundle.summary.selected_candidate_id == "1b3534d34062"
    assert bundle.summary.exhausted_subcluster == "gpu-fmv-mainloop-service"
    assert bundle.summary.source_context_function_count == 14
    assert bundle.summary.source_backed_callsite_count == 87
    assert bundle.summary.callsite_family_count == 8
    assert bundle.summary.implemented_callsite_family_count == 8
    assert bundle.summary.stub_only_callsite_family_count == 0
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_deferred_candidate_id == "none"
    assert bundle.summary.next_subcluster == "runtime-callee-bridge"
    assert bundle.summary.next_ticket == "RE-364"
    assert bundle.summary.next_topic == "platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.callsite_family for row in bundle.family_rows] == [
        "load-file-helper",
        "gpu-display-helper",
        "profiling-helper",
        "audio-sound-helper",
        "memory-allocation-helper",
        "platform-lifecycle-helper",
        "movie-playback-helper",
        "text-ui-helper",
    ]
    assert [row.source_backed_callsite_count for row in bundle.family_rows] == [21, 18, 15, 12, 9, 6, 3, 3]
    assert [row.implemented_callsite_count for row in bundle.family_rows] == [21, 18, 15, 12, 9, 6, 3, 3]
    assert [row.stub_callsite_count for row in bundle.family_rows] == [0] * 8
    assert [row.implemented_caller_count for row in bundle.family_rows] == [1, 2, 2, 1, 2, 1, 1, 1]
    assert all(row.candidate_level_proof == "no" for row in bundle.family_rows)
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.family_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.family_rows)
    assert all(row.readiness_gate == "blocked-no-candidate-level-proof" for row in bundle.family_rows)
    assert all(row.next_probe == "close-gpu-fmv-mainloop-subcluster" for row in bundle.family_rows)

    decision = bundle.decision_rows[0]
    assert decision.readiness_gate == "blocked-no-callsite-family-proves-candidate"
    assert decision.decision == "deny-domain-reopen-and-close-subcluster"
    assert decision.next_deferred_candidate_id == "none"
    assert decision.next_subcluster == "runtime-callee-bridge"
    assert decision.next_ticket == "RE-364"

    for row in bundle.family_rows + bundle.decision_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "source_line_text" not in row_text


def test_re363_writes_metadata_only_callsite_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_gpu_fmv_mainloop_service_callsite_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"families_csv", "decision_csv", "summary_csv", "handoff_csv", "md", "story"}

    families = list(csv.DictReader(written["families_csv"].open(newline="", encoding="utf-8")))
    assert len(families) == 8
    assert "source_line_text" not in families[0]
    assert families[0]["candidate_id"] == "1b3534d34062"
    assert families[0]["callsite_family"] == "load-file-helper"
    assert families[0]["source_backed_callsite_count"] == "21"
    assert families[0]["implemented_callsite_count"] == "21"
    assert families[0]["readiness_gate"] == "blocked-no-candidate-level-proof"

    decision = list(csv.DictReader(written["decision_csv"].open(newline="", encoding="utf-8")))
    assert decision == [
        {
            "rank": "1",
            "candidate_id": "1b3534d34062",
            "callsite_family_count": "8",
            "implemented_callsite_family_count": "8",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-no-callsite-family-proves-candidate",
            "decision": "deny-domain-reopen-and-close-subcluster",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "selected_domain": "none",
            "selected_pivot": "none",
            "next_deferred_candidate_id": "none",
            "next_subcluster": "runtime-callee-bridge",
            "next_ticket": "RE-364",
            "next_topic": "platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection",
            "stop_condition": "gpu/fmv mainloop service candidate lacks candidate-level proof; close this subcluster and select the next deferred parent subcluster",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-364"
    assert handoff["selected_candidate_id"] == "1b3534d34062"
    assert handoff["next_deferred_candidate_id"] == "none"
    assert handoff["next_subcluster"] == "runtime-callee-bridge"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-362 callsite handoff validated." in story
    assert "- [x] Parent RE-343 deferred subcluster queue checked." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-364" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-363 gpu/fmv mainloop service callsite readiness gate" in md
    assert "No gpu/fmv mainloop callsite family proves candidate-level behavior" in md

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
