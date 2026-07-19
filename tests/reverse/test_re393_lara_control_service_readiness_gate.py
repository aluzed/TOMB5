from pathlib import Path
import csv

from scripts.reverse.re393_lara_control_service_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_lara_control_service_readiness_gate,
    write_all_artifacts,
)


def test_re393_gates_lara_control_service_without_reopening_domain():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_lara_control_service_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-393"
    assert bundle.summary.topic == "lara-control-service-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-392"
    assert bundle.summary.selected_narrow_subcluster == "lara-control-service"
    assert bundle.summary.input_candidate_count == 1
    assert bundle.summary.candidate_gate_count == 1
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.selected_followup_candidate_id == "none"
    assert bundle.summary.next_ticket == "RE-394"
    assert bundle.summary.next_topic == "lara-combat-camera-post-lara-control-next-subcluster-selection"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.candidate_id for row in bundle.candidate_rows] == ["4a632b41837e"]
    candidate = bundle.candidate_rows[0]
    assert candidate.lara_control_context_count == 6
    assert candidate.proof_signal_class == "caller-callee-lara-control-context-only"
    assert candidate.candidate_level_proof == "no"
    assert candidate.readiness_gate == "blocked-no-candidate-level-proof"
    assert candidate.ready_to_reopen_domain == "no"
    assert candidate.source_patch_authorized == "no"
    assert candidate.next_probe == "close-lara-control-service-select-next-subcluster"

    gate = bundle.gate_rows[0]
    assert gate.gate_class == "candidate-level-source-symbolic-proof-missing"
    assert gate.candidate_count == 1
    assert gate.representative_candidates == "4a632b41837e"
    assert gate.gate_decision == "close-subcluster-select-next-deferred-subcluster"
    assert gate.ready_to_reopen_domain == "no"
    assert gate.source_patch_authorized == "no"
    assert gate.next_ticket == "RE-394"
    assert gate.next_topic == "lara-combat-camera-post-lara-control-next-subcluster-selection"

    for row in bundle.candidate_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text


def test_re393_writes_metadata_only_readiness_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_lara_control_service_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"candidates_csv", "gates_csv", "summary_csv", "handoff_csv", "md", "story"}

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert len(candidates) == 1
    assert "ghidra_entry" not in candidates[0]
    assert "ghidra_name" not in candidates[0]
    assert candidates[0]["candidate_id"] == "4a632b41837e"
    assert candidates[0]["lara_control_context_count"] == "6"
    assert candidates[0]["readiness_gate"] == "blocked-no-candidate-level-proof"
    assert candidates[0]["next_probe"] == "close-lara-control-service-select-next-subcluster"

    gates = list(csv.DictReader(written["gates_csv"].open(newline="", encoding="utf-8")))
    assert gates == [
        {
            "rank": "1",
            "gate_class": "candidate-level-source-symbolic-proof-missing",
            "candidate_count": "1",
            "representative_candidates": "4a632b41837e",
            "candidate_level_proof_count": "0",
            "gate_decision": "close-subcluster-select-next-deferred-subcluster",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-394",
            "next_topic": "lara-combat-camera-post-lara-control-next-subcluster-selection",
            "stop_condition": "lara control service candidate queue exhausted without candidate-level proof",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-394"
    assert handoff["next_topic"] == "lara-combat-camera-post-lara-control-next-subcluster-selection"
    assert handoff["selected_followup_candidate_id"] == "none"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["metadata_work_readiness"] == "ready"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-392 lara-control-service handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-394" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-393 lara control service readiness gate" in md
    assert "No proof-domain is reopened by this gate" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
