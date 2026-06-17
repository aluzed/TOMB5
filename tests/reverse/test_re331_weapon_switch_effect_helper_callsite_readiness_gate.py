from pathlib import Path
import csv

from scripts.reverse.re331_weapon_switch_effect_helper_callsite_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_weapon_switch_effect_helper_callsite_readiness_gate,
    write_all_artifacts,
)


def test_re331_gates_weapon_switch_effect_stub_callsite_and_exhausts_candidate_queue():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_weapon_switch_effect_helper_callsite_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-331"
    assert bundle.summary.topic == "weapon-switch-effect-helper-callsite-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-330"
    assert bundle.summary.selected_candidate_id == "1ddbda046e37"
    assert bundle.summary.next_candidate_id == "none"
    assert bundle.summary.source_context_function_count == 1
    assert bundle.summary.source_backed_callsite_count == 1
    assert bundle.summary.callsite_family_count == 1
    assert bundle.summary.implemented_callsite_family_count == 0
    assert bundle.summary.stub_only_callsite_family_count == 1
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "TBD"
    assert bundle.summary.next_topic == "weapon-switch-effect-helper-candidate-queue-exhausted"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.family_rows) == 1
    family = bundle.family_rows[0]
    assert family.callsite_family == "stub-marker"
    assert family.source_backed_callsite_count == 1
    assert family.implemented_callsite_count == 0
    assert family.stub_callsite_count == 1
    assert family.caller_count == 1
    assert family.implemented_caller_count == 0
    assert family.candidate_level_proof == "no"
    assert family.readiness_gate == "blocked-stub-only-family"
    assert family.ready_to_reopen_domain == "no"
    assert family.source_patch_authorized == "no"
    assert family.next_probe == "candidate-queue-exhausted"

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


def test_re331_writes_metadata_only_callsite_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_weapon_switch_effect_helper_callsite_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"families_csv", "decision_csv", "summary_csv", "handoff_csv", "md", "story"}

    families = list(csv.DictReader(written["families_csv"].open(newline="", encoding="utf-8")))
    assert families == [
        {
            "rank": "1",
            "candidate_id": "1ddbda046e37",
            "callsite_family": "stub-marker",
            "source_backed_callsite_count": "1",
            "implemented_callsite_count": "0",
            "stub_callsite_count": "1",
            "caller_count": "1",
            "implemented_caller_count": "0",
            "candidate_level_proof": "no",
            "readiness_gate": "blocked-stub-only-family",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "blocker_class": "stub-only-callsite-family",
            "next_probe": "candidate-queue-exhausted",
        }
    ]
    assert "source_line_text" not in families[0]

    decision = list(csv.DictReader(written["decision_csv"].open(newline="", encoding="utf-8")))
    assert decision == [
        {
            "rank": "1",
            "candidate_id": "1ddbda046e37",
            "callsite_family_count": "1",
            "implemented_callsite_family_count": "0",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-single-candidate-queue-exhausted",
            "decision": "deny-domain-reopen-and-exhaust-candidate-queue",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "selected_domain": "none",
            "selected_pivot": "none",
            "next_ticket": "TBD",
            "next_topic": "weapon-switch-effect-helper-candidate-queue-exhausted",
            "next_candidate_id": "none",
            "stop_condition": "single weapon-switch-effect helper candidate has only a stub-marker callsite and no candidate-level proof; candidate queue exhausted",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "TBD"
    assert handoff["selected_candidate_id"] == "1ddbda046e37"
    assert handoff["next_candidate_id"] == "none"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-330 callsite handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "candidate queue is exhausted" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-331 weapon-switch-effect helper callsite readiness gate" in md
    assert "No weapon-switch-effect callsite family proves candidate-level behavior" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
