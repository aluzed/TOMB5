from pathlib import Path
import csv

from scripts.reverse.re395_combat_camera_service_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_combat_camera_service_readiness_gate,
    write_all_artifacts,
)


def test_re395_gates_combat_camera_without_reopening_domain():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_combat_camera_service_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-395"
    assert bundle.summary.topic == "combat-camera-service-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-394"
    assert bundle.summary.selected_narrow_subcluster == "combat-camera-service"
    assert bundle.summary.input_candidate_count == 1
    assert bundle.summary.candidate_gate_count == 1
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.selected_followup_candidate_id == "0aaa76206517"
    assert bundle.summary.next_ticket == "RE-396"
    assert bundle.summary.next_topic == "combat-camera-service-candidate-proof-export"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    candidate = bundle.candidate_rows[0]
    assert candidate.candidate_id == "0aaa76206517"
    assert candidate.combat_camera_context_count == 6
    assert candidate.proof_signal_class == "caller-combat-camera-context-only"
    assert candidate.candidate_level_proof == "no"
    assert candidate.readiness_gate == "blocked-no-candidate-level-proof"
    assert candidate.next_probe == "candidate-proof-export"

    gate = bundle.gate_rows[0]
    assert gate.gate_decision == "request-still-narrower-export"
    assert gate.next_ticket == "RE-396"
    assert gate.next_topic == "combat-camera-service-candidate-proof-export"


def test_re395_writes_metadata_only_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_combat_camera_service_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)
    assert set(written) == {"candidates_csv", "gates_csv", "summary_csv", "handoff_csv", "md", "story"}

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert candidates[0]["candidate_id"] == "0aaa76206517"
    assert candidates[0]["combat_camera_context_count"] == "6"
    assert "ghidra_entry" not in candidates[0]
    assert "ghidra_name" not in candidates[0]
    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-396"
    assert handoff["selected_followup_candidate_id"] == "0aaa76206517"
    assert handoff["selected_domain"] == "none"
    assert handoff["code_change_readiness"] == "blocked"
    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-394 combat-camera handoff validated." in story
    assert "RE-396" in story
    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
