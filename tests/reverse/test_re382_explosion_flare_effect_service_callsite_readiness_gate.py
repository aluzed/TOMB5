from pathlib import Path
import csv

from scripts.reverse.re382_explosion_flare_effect_service_callsite_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_explosion_flare_effect_service_callsite_readiness_gate,
    write_all_artifacts,
)


def test_re382_gates_explosion_flare_callsite_families_and_closes_subcluster():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_explosion_flare_effect_service_callsite_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-382"
    assert bundle.summary.topic == "explosion-flare-effect-service-callsite-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-381"
    assert bundle.summary.selected_candidate_id == "87d9c8a62335"
    assert bundle.summary.exhausted_subcluster == "explosion-flare-effect-service"
    assert bundle.summary.source_context_function_count == 18
    assert bundle.summary.source_backed_callsite_count == 121
    assert bundle.summary.callsite_family_count == 7
    assert bundle.summary.implemented_callsite_family_count == 6
    assert bundle.summary.stub_only_callsite_family_count == 1
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_deferred_candidate_id == "none"
    assert bundle.summary.next_subcluster == "spotcam-projectile-effect-service"
    assert bundle.summary.next_ticket == "RE-383"
    assert bundle.summary.next_topic == "effects-lighting-cluster-post-explosion-flare-next-subcluster-selection"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.callsite_family for row in bundle.family_rows] == [
        "control-flow-helper",
        "explosion-flare-effect-helper",
        "joint-position-helper",
        "audio-camera-helper",
        "runtime-effect-support",
        "room-floor-helper",
        "stub-marker",
    ]
    assert [row.source_backed_callsite_count for row in bundle.family_rows] == [38, 23, 21, 17, 8, 8, 6]
    assert [row.implemented_callsite_count for row in bundle.family_rows] == [38, 23, 20, 1, 7, 7, 0]
    assert [row.stub_callsite_count for row in bundle.family_rows] == [0, 0, 1, 16, 1, 1, 6]
    assert [row.implemented_caller_count for row in bundle.family_rows] == [7, 8, 12, 1, 4, 4, 0]
    assert all(row.candidate_level_proof == "no" for row in bundle.family_rows)
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.family_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.family_rows)
    assert bundle.family_rows[-1].readiness_gate == "blocked-stub-only-family"
    assert all(row.next_probe == "close-explosion-flare-subcluster" for row in bundle.family_rows)

    decision = bundle.decision_rows[0]
    assert decision.readiness_gate == "blocked-no-callsite-family-proves-candidate"
    assert decision.decision == "deny-domain-reopen-and-close-subcluster"
    assert decision.next_deferred_candidate_id == "none"
    assert decision.next_subcluster == "spotcam-projectile-effect-service"
    assert decision.next_ticket == "RE-383"

    for row in bundle.family_rows + bundle.decision_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "source_line_text" not in row_text


def test_re382_writes_metadata_only_callsite_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_explosion_flare_effect_service_callsite_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"families_csv", "decision_csv", "summary_csv", "handoff_csv", "md", "story"}

    families = list(csv.DictReader(written["families_csv"].open(newline="", encoding="utf-8")))
    assert len(families) == 7
    assert "source_line_text" not in families[0]
    assert families[0]["candidate_id"] == "87d9c8a62335"
    assert families[0]["callsite_family"] == "control-flow-helper"
    assert families[0]["source_backed_callsite_count"] == "38"
    assert families[0]["readiness_gate"] == "blocked-no-candidate-level-proof"
    assert families[-1]["callsite_family"] == "stub-marker"
    assert families[-1]["readiness_gate"] == "blocked-stub-only-family"

    decision = list(csv.DictReader(written["decision_csv"].open(newline="", encoding="utf-8")))
    assert decision == [
        {
            "rank": "1",
            "candidate_id": "87d9c8a62335",
            "callsite_family_count": "7",
            "implemented_callsite_family_count": "6",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-no-callsite-family-proves-candidate",
            "decision": "deny-domain-reopen-and-close-subcluster",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "selected_domain": "none",
            "selected_pivot": "none",
            "next_deferred_candidate_id": "none",
            "next_subcluster": "spotcam-projectile-effect-service",
            "next_ticket": "RE-383",
            "next_topic": "effects-lighting-cluster-post-explosion-flare-next-subcluster-selection",
            "stop_condition": "the only explosion/flare service candidate lacks candidate-level proof; close this subcluster and select the next deferred parent subcluster",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-383"
    assert handoff["selected_candidate_id"] == "87d9c8a62335"
    assert handoff["next_deferred_candidate_id"] == "none"
    assert handoff["next_subcluster"] == "spotcam-projectile-effect-service"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-381 callsite-map handoff validated." in story
    assert "- [x] Parent RE-370 deferred subcluster queue checked." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-383" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-382 explosion/flare effect service callsite readiness gate" in md
    assert "No explosion/flare callsite family proves candidate-level behavior" in md

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
