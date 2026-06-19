from pathlib import Path
import csv

from scripts.reverse.re358_frontend_display_menu_service_next_candidate_callsite_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_frontend_display_menu_service_next_candidate_callsite_readiness_gate,
    write_all_artifacts,
)


def test_re358_gates_next_candidate_callsite_families_and_closes_frontend_display_menu_queue():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_frontend_display_menu_service_next_candidate_callsite_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-358"
    assert bundle.summary.topic == "frontend-display-menu-service-next-candidate-callsite-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-357"
    assert bundle.summary.selected_candidate_id == "4c90c6af8f9d"
    assert bundle.summary.previous_candidate_id == "de919274685f"
    assert bundle.summary.exhausted_subcluster == "frontend-display-menu-service"
    assert bundle.summary.source_context_function_count == 18
    assert bundle.summary.source_backed_callsite_count == 126
    assert bundle.summary.callsite_family_count == 5
    assert bundle.summary.implemented_callsite_family_count == 5
    assert bundle.summary.stub_only_callsite_family_count == 0
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_deferred_candidate_id == "none"
    assert bundle.summary.next_subcluster == "gpu-fmv-mainloop-service"
    assert bundle.summary.next_ticket == "RE-359"
    assert bundle.summary.next_topic == "platform-frontend-service-post-frontend-display-menu-next-subcluster-selection"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.callsite_family for row in bundle.family_rows] == [
        "text-ui-helper",
        "diagnostic-helper",
        "level-load-service-helper",
        "audio-sound-helper",
        "gpu-display-helper",
    ]
    assert [row.source_backed_callsite_count for row in bundle.family_rows] == [74, 27, 21, 2, 2]
    assert [row.implemented_callsite_count for row in bundle.family_rows] == [74, 27, 21, 2, 2]
    assert [row.stub_callsite_count for row in bundle.family_rows] == [0] * 5
    assert [row.implemented_caller_count for row in bundle.family_rows] == [5, 2, 3, 1, 1]
    assert all(row.candidate_level_proof == "no" for row in bundle.family_rows)
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.family_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.family_rows)
    assert all(row.readiness_gate == "blocked-no-candidate-level-proof" for row in bundle.family_rows)
    assert all(row.next_probe == "close-frontend-display-menu-subcluster" for row in bundle.family_rows)

    decision = bundle.decision_rows[0]
    assert decision.readiness_gate == "blocked-no-next-candidate-callsite-family-proves-candidate"
    assert decision.decision == "deny-domain-reopen-and-close-subcluster"
    assert decision.next_deferred_candidate_id == "none"
    assert decision.next_subcluster == "gpu-fmv-mainloop-service"
    assert decision.next_ticket == "RE-359"

    for row in bundle.family_rows + bundle.decision_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "source_line_text" not in row_text


def test_re358_writes_metadata_only_callsite_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_frontend_display_menu_service_next_candidate_callsite_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"families_csv", "decision_csv", "summary_csv", "handoff_csv", "md", "story"}

    families = list(csv.DictReader(written["families_csv"].open(newline="", encoding="utf-8")))
    assert len(families) == 5
    assert "source_line_text" not in families[0]
    assert families[0]["candidate_id"] == "4c90c6af8f9d"
    assert families[0]["previous_candidate_id"] == "de919274685f"
    assert families[0]["callsite_family"] == "text-ui-helper"
    assert families[0]["source_backed_callsite_count"] == "74"
    assert families[0]["implemented_callsite_count"] == "74"
    assert families[0]["readiness_gate"] == "blocked-no-candidate-level-proof"

    decision = list(csv.DictReader(written["decision_csv"].open(newline="", encoding="utf-8")))
    assert decision == [
        {
            "rank": "1",
            "candidate_id": "4c90c6af8f9d",
            "previous_candidate_id": "de919274685f",
            "callsite_family_count": "5",
            "implemented_callsite_family_count": "5",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-no-next-candidate-callsite-family-proves-candidate",
            "decision": "deny-domain-reopen-and-close-subcluster",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "selected_domain": "none",
            "selected_pivot": "none",
            "next_deferred_candidate_id": "none",
            "next_subcluster": "gpu-fmv-mainloop-service",
            "next_ticket": "RE-359",
            "next_topic": "platform-frontend-service-post-frontend-display-menu-next-subcluster-selection",
            "stop_condition": "all frontend display/menu service candidates lack candidate-level proof; close this subcluster and select the next deferred parent subcluster",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-359"
    assert handoff["selected_candidate_id"] == "4c90c6af8f9d"
    assert handoff["previous_candidate_id"] == "de919274685f"
    assert handoff["next_deferred_candidate_id"] == "none"
    assert handoff["next_subcluster"] == "gpu-fmv-mainloop-service"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-357 next-candidate callsite handoff validated." in story
    assert "- [x] Parent RE-343 deferred subcluster queue checked." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-359" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-358 frontend display/menu service next candidate callsite readiness gate" in md
    assert "No next-candidate callsite family proves candidate-level behavior" in md

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
