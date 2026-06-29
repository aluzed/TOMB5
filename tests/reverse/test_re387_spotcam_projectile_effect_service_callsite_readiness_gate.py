from pathlib import Path
import csv

from scripts.reverse.re387_spotcam_projectile_effect_service_callsite_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_spotcam_projectile_effect_service_callsite_readiness_gate,
    write_all_artifacts,
)


def test_re387_gates_spotcam_projectile_callsite_families_and_exhausts_effects_lighting_queue():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_spotcam_projectile_effect_service_callsite_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-387"
    assert bundle.summary.topic == "spotcam-projectile-effect-service-callsite-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-386"
    assert bundle.summary.selected_candidate_id == "b6d128932004"
    assert bundle.summary.exhausted_subcluster == "spotcam-projectile-effect-service"
    assert bundle.summary.source_context_function_count == 52
    assert bundle.summary.source_backed_callsite_count == 296
    assert bundle.summary.callsite_family_count == 8
    assert bundle.summary.implemented_callsite_family_count == 7
    assert bundle.summary.stub_only_callsite_family_count == 1
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_deferred_candidate_id == "none"
    assert bundle.summary.next_subcluster == "none"
    assert bundle.summary.next_ticket == "TBD"
    assert bundle.summary.next_topic == "effects-lighting-cluster-subcluster-queue-exhausted"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.callsite_family for row in bundle.family_rows] == [
        "spotcam-projectile-helper",
        "ambient-combat-effect-helper",
        "room-floor-helper",
        "runtime-effect-support",
        "conversation-helper",
        "audio-camera-helper",
        "trap-effect-helper",
        "stub-marker",
    ]
    assert [row.source_backed_callsite_count for row in bundle.family_rows] == [204, 32, 16, 16, 6, 2, 1, 19]
    assert [row.implemented_callsite_count for row in bundle.family_rows] == [204, 32, 16, 16, 6, 2, 1, 0]
    assert [row.stub_callsite_count for row in bundle.family_rows] == [0, 0, 0, 0, 0, 0, 0, 19]
    assert [row.caller_count for row in bundle.family_rows] == [33, 15, 7, 13, 3, 1, 1, 19]
    assert [row.implemented_caller_count for row in bundle.family_rows] == [33, 15, 7, 13, 3, 1, 1, 0]
    assert all(row.candidate_level_proof == "no" for row in bundle.family_rows)
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.family_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.family_rows)
    assert bundle.family_rows[-1].readiness_gate == "blocked-stub-only-family"
    assert all(row.next_probe == "close-spotcam-projectile-subcluster" for row in bundle.family_rows)

    decision = bundle.decision_rows[0]
    assert decision.readiness_gate == "blocked-parent-subcluster-queue-exhausted"
    assert decision.decision == "deny-domain-reopen-and-exhaust-effects-lighting-queue"
    assert decision.next_deferred_candidate_id == "none"
    assert decision.next_subcluster == "none"
    assert decision.next_ticket == "TBD"

    for row in bundle.family_rows + bundle.decision_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "source_line_text" not in row_text


def test_re387_writes_metadata_only_callsite_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_spotcam_projectile_effect_service_callsite_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"families_csv", "decision_csv", "summary_csv", "handoff_csv", "md", "story"}

    families = list(csv.DictReader(written["families_csv"].open(newline="", encoding="utf-8")))
    assert len(families) == 8
    assert "source_line_text" not in families[0]
    assert families[0]["candidate_id"] == "b6d128932004"
    assert families[0]["callsite_family"] == "spotcam-projectile-helper"
    assert families[0]["source_backed_callsite_count"] == "204"
    assert families[0]["readiness_gate"] == "blocked-no-candidate-level-proof"
    assert families[-1]["callsite_family"] == "stub-marker"
    assert families[-1]["readiness_gate"] == "blocked-stub-only-family"

    decision = list(csv.DictReader(written["decision_csv"].open(newline="", encoding="utf-8")))
    assert decision == [
        {
            "rank": "1",
            "candidate_id": "b6d128932004",
            "callsite_family_count": "8",
            "implemented_callsite_family_count": "7",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-parent-subcluster-queue-exhausted",
            "decision": "deny-domain-reopen-and-exhaust-effects-lighting-queue",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "selected_domain": "none",
            "selected_pivot": "none",
            "next_deferred_candidate_id": "none",
            "next_subcluster": "none",
            "next_ticket": "TBD",
            "next_topic": "effects-lighting-cluster-subcluster-queue-exhausted",
            "stop_condition": "spotcam/projectile candidate lacks candidate-level proof; effects/lighting subcluster queue exhausted",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "TBD"
    assert handoff["selected_candidate_id"] == "b6d128932004"
    assert handoff["next_deferred_candidate_id"] == "none"
    assert handoff["next_subcluster"] == "none"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-386 callsite-map handoff validated." in story
    assert "- [x] Parent RE-370 effects/lighting subcluster queue checked." in story
    assert "## Follow-up ticket breakdown" in story
    assert "effects-lighting-cluster-subcluster-queue-exhausted" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-387 spotcam/projectile effect service callsite readiness gate" in md
    assert "No spotcam/projectile callsite family proves candidate-level behavior" in md

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
