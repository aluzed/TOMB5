from pathlib import Path
import csv

from scripts.reverse.re326_switch_door_control_helper_callsite_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_switch_door_control_helper_callsite_readiness_gate,
    write_all_artifacts,
)


def test_re326_gates_switch_door_callsite_families_and_exhausts_candidate_queue():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_switch_door_control_helper_callsite_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-326"
    assert bundle.summary.topic == "switch-door-control-helper-callsite-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-325"
    assert bundle.summary.selected_candidate_id == "8d1fc6fc3cfc"
    assert bundle.summary.next_candidate_id == "none"
    assert bundle.summary.source_context_function_count == 22
    assert bundle.summary.source_backed_callsite_count == 39
    assert bundle.summary.callsite_family_count == 5
    assert bundle.summary.implemented_callsite_family_count == 4
    assert bundle.summary.stub_only_callsite_family_count == 1
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "TBD"
    assert bundle.summary.next_topic == "switch-door-control-helper-candidate-queue-exhausted"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.callsite_family for row in bundle.family_rows] == [
        "door-helper",
        "animation-helper",
        "trigger-helper",
        "effect-helper",
        "stub-marker",
    ]
    assert [row.source_backed_callsite_count for row in bundle.family_rows] == [14, 7, 2, 3, 13]
    assert [row.implemented_caller_count for row in bundle.family_rows] == [3, 7, 2, 1, 0]
    assert all(row.candidate_level_proof == "no" for row in bundle.family_rows)
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.family_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.family_rows)
    assert bundle.family_rows[-1].readiness_gate == "blocked-stub-only-family"
    assert bundle.family_rows[0].readiness_gate == "blocked-no-candidate-level-proof"

    decision = bundle.decision_rows[0]
    assert decision.readiness_gate == "blocked-single-candidate-queue-exhausted"
    assert decision.decision == "deny-domain-reopen-and-exhaust-candidate-queue"
    assert decision.next_candidate_id == "none"
    assert decision.next_ticket == "TBD"

    for row in bundle.family_rows + bundle.decision_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "unimplemented();" not in row_text


def test_re326_writes_metadata_only_callsite_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_switch_door_control_helper_callsite_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"families_csv", "decision_csv", "summary_csv", "handoff_csv", "md", "story"}

    families = list(csv.DictReader(written["families_csv"].open(newline="", encoding="utf-8")))
    assert len(families) == 5
    assert "source_line_text" not in families[0]
    assert families[0]["candidate_id"] == "8d1fc6fc3cfc"
    assert families[0]["callsite_family"] == "door-helper"
    assert families[0]["source_backed_callsite_count"] == "14"
    assert families[0]["readiness_gate"] == "blocked-no-candidate-level-proof"
    assert families[-1]["callsite_family"] == "stub-marker"
    assert families[-1]["source_backed_callsite_count"] == "13"
    assert families[-1]["readiness_gate"] == "blocked-stub-only-family"

    decision = list(csv.DictReader(written["decision_csv"].open(newline="", encoding="utf-8")))
    assert decision == [
        {
            "rank": "1",
            "candidate_id": "8d1fc6fc3cfc",
            "callsite_family_count": "5",
            "implemented_callsite_family_count": "4",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-single-candidate-queue-exhausted",
            "decision": "deny-domain-reopen-and-exhaust-candidate-queue",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "selected_domain": "none",
            "selected_pivot": "none",
            "next_ticket": "TBD",
            "next_topic": "switch-door-control-helper-candidate-queue-exhausted",
            "next_candidate_id": "none",
            "stop_condition": "single switch-door-control helper candidate lacks candidate-level proof; candidate queue exhausted",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "TBD"
    assert handoff["selected_candidate_id"] == "8d1fc6fc3cfc"
    assert handoff["next_candidate_id"] == "none"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-325 callsite handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "candidate queue is exhausted" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-326 switch-door-control helper callsite readiness gate" in md
    assert "No switch-door-control callsite family proves candidate-level behavior" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
