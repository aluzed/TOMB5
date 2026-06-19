from pathlib import Path
import csv

from scripts.reverse.re338_camera_collision_helper_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_camera_collision_helper_readiness_gate,
    write_all_artifacts,
)


def test_re338_gates_camera_collision_helper_without_reopening_domain():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_camera_collision_helper_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-338"
    assert bundle.summary.topic == "camera-collision-helper-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-337"
    assert bundle.summary.selected_narrow_subcluster == "camera-collision-helper"
    assert bundle.summary.input_candidate_count == 1
    assert bundle.summary.candidate_gate_count == 1
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.selected_followup_candidate_id == "95c41ac597d6"
    assert bundle.summary.next_ticket == "RE-339"
    assert bundle.summary.next_topic == "camera-collision-helper-candidate-proof-export"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.candidate_rows) == 1
    candidate = bundle.candidate_rows[0]
    assert candidate.rank == 1
    assert candidate.source_rank == 25
    assert candidate.candidate_id == "95c41ac597d6"
    assert candidate.selected_narrow_subcluster == "camera-collision-helper"
    assert candidate.mapped_caller_count == 11
    assert candidate.mapped_callee_count == 0
    assert candidate.caller_camera_collision_context_count == 3
    assert candidate.callee_camera_collision_context_count == 0
    assert candidate.proof_signal_class == "caller-camera-collision-context-only"
    assert candidate.readiness_gate == "blocked-needs-candidate-level-proof"
    assert candidate.ready_to_reopen_domain == "no"
    assert candidate.source_patch_authorized == "no"
    assert candidate.next_probe == "candidate-proof-export"

    gate = bundle.gate_rows[0]
    assert gate.gate_class == "candidate-level-source-symbolic-proof-missing"
    assert gate.candidate_count == 1
    assert gate.representative_candidates == "95c41ac597d6"
    assert gate.gate_decision == "request-still-narrower-export"
    assert gate.ready_to_reopen_domain == "no"
    assert gate.source_patch_authorized == "no"
    assert gate.next_ticket == "RE-339"
    assert gate.next_topic == "camera-collision-helper-candidate-proof-export"

    for row in bundle.candidate_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text


def test_re338_writes_metadata_only_readiness_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_camera_collision_helper_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"candidates_csv", "gates_csv", "summary_csv", "handoff_csv", "md", "story"}

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert len(candidates) == 1
    assert "ghidra_entry" not in candidates[0]
    assert "ghidra_name" not in candidates[0]
    assert candidates[0]["candidate_id"] == "95c41ac597d6"
    assert candidates[0]["caller_camera_collision_context_count"] == "3"
    assert candidates[0]["callee_camera_collision_context_count"] == "0"
    assert candidates[0]["readiness_gate"] == "blocked-needs-candidate-level-proof"
    assert candidates[0]["next_probe"] == "candidate-proof-export"

    gates = list(csv.DictReader(written["gates_csv"].open(newline="", encoding="utf-8")))
    assert gates == [
        {
            "rank": "1",
            "gate_class": "candidate-level-source-symbolic-proof-missing",
            "candidate_count": "1",
            "representative_candidates": "95c41ac597d6",
            "gate_decision": "request-still-narrower-export",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-339",
            "next_topic": "camera-collision-helper-candidate-proof-export",
            "stop_condition": "candidate-level source-symbolic proof is required before proof-domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-339"
    assert handoff["next_topic"] == "camera-collision-helper-candidate-proof-export"
    assert handoff["selected_followup_candidate_id"] == "95c41ac597d6"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["metadata_work_readiness"] == "ready"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-337 camera-collision helper handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-339" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-338 camera-collision helper readiness gate" in md
    assert "No proof-domain is reopened by this gate" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
