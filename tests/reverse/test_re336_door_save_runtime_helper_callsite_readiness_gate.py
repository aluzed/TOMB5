from pathlib import Path
import csv

from scripts.reverse.re336_door_save_runtime_helper_callsite_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_door_save_runtime_helper_callsite_readiness_gate,
    write_all_artifacts,
)


def test_re336_gates_door_save_runtime_callsite_families_and_exhausts_candidate_queue():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_door_save_runtime_helper_callsite_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-336"
    assert bundle.summary.topic == "door-save-runtime-helper-callsite-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-335"
    assert bundle.summary.selected_candidate_id == "f457f2772655"
    assert bundle.summary.next_candidate_id == "none"
    assert bundle.summary.source_context_function_count == 14
    assert bundle.summary.source_backed_callsite_count == 185
    assert bundle.summary.callsite_family_count == 13
    assert bundle.summary.implemented_callsite_family_count == 12
    assert bundle.summary.stub_only_callsite_family_count == 1
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "TBD"
    assert bundle.summary.next_topic == "door-save-runtime-helper-candidate-queue-exhausted"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.family_rows) == 13
    expected_families = [
        "platform-cd-helper",
        "camera-runtime-helper",
        "savegame-memory-helper",
        "platform-file-helper",
        "lara-state-helper",
        "collision-trigger-helper",
        "level-runtime-helper",
        "frontend-runtime-helper",
        "gameflow-load-helper",
        "audio-helper",
        "address-derived-symbol-omitted",
        "stub-marker",
        "other",
    ]
    assert [row.callsite_family for row in bundle.family_rows] == expected_families

    platform_cd = bundle.family_rows[0]
    assert platform_cd.source_backed_callsite_count == 46
    assert platform_cd.implemented_callsite_count == 46
    assert platform_cd.stub_callsite_count == 0
    assert platform_cd.caller_count == 3
    assert platform_cd.readiness_gate == "blocked-no-candidate-level-proof"
    assert platform_cd.next_probe == "candidate-queue-exhausted"

    stub = next(row for row in bundle.family_rows if row.callsite_family == "stub-marker")
    assert stub.source_backed_callsite_count == 1
    assert stub.implemented_callsite_count == 0
    assert stub.stub_callsite_count == 1
    assert stub.caller_count == 1
    assert stub.readiness_gate == "blocked-stub-only-family"

    decision = bundle.decision_rows[0]
    assert decision.readiness_gate == "blocked-single-candidate-queue-exhausted"
    assert decision.decision == "deny-domain-reopen-and-exhaust-candidate-queue"
    assert decision.next_candidate_id == "none"
    assert decision.next_ticket == "TBD"

    for row in bundle.family_rows + bundle.decision_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "unimplemented();" not in row_text


def test_re336_writes_metadata_only_callsite_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_door_save_runtime_helper_callsite_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"families_csv", "decision_csv", "summary_csv", "handoff_csv", "md", "story"}

    families = list(csv.DictReader(written["families_csv"].open(newline="", encoding="utf-8")))
    assert len(families) == 13
    assert families[0] == {
        "rank": "1",
        "candidate_id": "f457f2772655",
        "callsite_family": "platform-cd-helper",
        "source_backed_callsite_count": "46",
        "implemented_callsite_count": "46",
        "stub_callsite_count": "0",
        "caller_count": "3",
        "implemented_caller_count": "3",
        "candidate_level_proof": "no",
        "readiness_gate": "blocked-no-candidate-level-proof",
        "ready_to_reopen_domain": "no",
        "source_patch_authorized": "no",
        "blocker_class": "implemented-family-lacks-candidate-level-proof",
        "next_probe": "candidate-queue-exhausted",
    }
    assert "source_line_text" not in families[0]
    assert any(row["callsite_family"] == "address-derived-symbol-omitted" for row in families)

    decision = list(csv.DictReader(written["decision_csv"].open(newline="", encoding="utf-8")))
    assert decision == [
        {
            "rank": "1",
            "candidate_id": "f457f2772655",
            "callsite_family_count": "13",
            "implemented_callsite_family_count": "12",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-single-candidate-queue-exhausted",
            "decision": "deny-domain-reopen-and-exhaust-candidate-queue",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "selected_domain": "none",
            "selected_pivot": "none",
            "next_ticket": "TBD",
            "next_topic": "door-save-runtime-helper-candidate-queue-exhausted",
            "next_candidate_id": "none",
            "stop_condition": "single door-save-runtime helper candidate has source-backed callsites but no candidate-level proof; candidate queue exhausted",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "TBD"
    assert handoff["selected_candidate_id"] == "f457f2772655"
    assert handoff["next_candidate_id"] == "none"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-335 callsite handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "candidate queue is exhausted" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-336 door-save-runtime helper callsite readiness gate" in md
    assert "No door-save-runtime callsite family proves candidate-level behavior" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
