from pathlib import Path
import csv

from scripts.reverse.re359_platform_frontend_service_post_frontend_display_menu_next_subcluster_selection import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_platform_frontend_service_post_frontend_display_menu_next_subcluster_selection,
    write_all_artifacts,
)


def test_re359_selects_gpu_fmv_mainloop_after_frontend_display_menu_exhaustion():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_platform_frontend_service_post_frontend_display_menu_next_subcluster_selection(repo)

    assert bundle.summary.story_id == "RE-359"
    assert bundle.summary.topic == "platform-frontend-service-post-frontend-display-menu-next-subcluster-selection"
    assert bundle.summary.upstream_handoff == "RE-358"
    assert bundle.summary.parent_scope == "platform-frontend-service-cluster"
    assert bundle.summary.closed_subclusters == "cd-load-audio-service;frontend-display-menu-service"
    assert bundle.summary.input_subcluster_count == 4
    assert bundle.summary.closed_subcluster_count == 2
    assert bundle.summary.deferred_subcluster_count == 2
    assert bundle.summary.selected_narrow_subcluster == "gpu-fmv-mainloop-service"
    assert bundle.summary.selected_narrow_candidate_count == 1
    assert bundle.summary.selected_candidate_ids == "1b3534d34062"
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-360"
    assert bundle.summary.next_topic == "gpu-fmv-mainloop-service-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.narrow_subcluster for row in bundle.subcluster_rows] == ["gpu-fmv-mainloop-service"]
    selected_subcluster = bundle.subcluster_rows[0]
    assert selected_subcluster.source_rank == 3
    assert selected_subcluster.candidate_count == 1
    assert selected_subcluster.mapped_caller_total == 14
    assert selected_subcluster.mapped_callee_total == 0
    assert selected_subcluster.max_source_context_count == 14
    assert selected_subcluster.selection_status == "selected-next"
    assert selected_subcluster.gate_decision == "gate-before-proof-domain"
    assert selected_subcluster.ready_to_reopen_domain == "no"
    assert selected_subcluster.source_patch_authorized == "no"

    assert [row.candidate_id for row in bundle.candidate_rows] == ["1b3534d34062"]
    candidate = bundle.candidate_rows[0]
    assert candidate.source_rank == 18
    assert candidate.bridge_class == "mapped-caller-heavy"
    assert candidate.body_size_bucket == "medium"
    assert candidate.mapped_caller_count == 14
    assert candidate.mapped_callee_count == 0
    assert candidate.source_context_count == 14
    assert candidate.next_probe == "candidate-proof-export"
    assert candidate.ready_to_reopen_domain == "no"
    assert candidate.source_patch_authorized == "no"


def test_re359_writes_metadata_only_next_subcluster_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_platform_frontend_service_post_frontend_display_menu_next_subcluster_selection(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"subclusters_csv", "candidates_csv", "summary_csv", "handoff_csv", "md", "story"}

    subclusters = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert subclusters == [
        {
            "rank": "1",
            "source_rank": "3",
            "narrow_subcluster": "gpu-fmv-mainloop-service",
            "candidate_count": "1",
            "mapped_caller_total": "14",
            "mapped_callee_total": "0",
            "max_source_context_count": "14",
            "bridge_classes": "mapped-caller-heavy",
            "selection_status": "selected-next",
            "gate_decision": "gate-before-proof-domain",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-360",
            "next_topic": "gpu-fmv-mainloop-service-readiness-gate",
            "stop_condition": "candidate-level source-symbolic proof required before proof-domain selection",
        }
    ]

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert candidates == [
        {
            "rank": "1",
            "source_rank": "18",
            "candidate_id": "1b3534d34062",
            "narrow_subcluster": "gpu-fmv-mainloop-service",
            "bridge_class": "mapped-caller-heavy",
            "body_size_bucket": "medium",
            "mapped_caller_count": "14",
            "mapped_callee_count": "0",
            "source_context_count": "14",
            "readiness_gate": "blocked-needs-candidate-level-proof",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_probe": "candidate-proof-export",
            "stop_condition": "candidate-level source-symbolic proof is required before domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-360"
    assert handoff["next_topic"] == "gpu-fmv-mainloop-service-readiness-gate"
    assert handoff["selected_narrow_subcluster"] == "gpu-fmv-mainloop-service"
    assert handoff["selected_candidate_ids"] == "1b3534d34062"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-358 frontend display/menu queue exhaustion validated." in story
    assert "gpu-fmv-mainloop-service" in story
    assert "RE-360" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-359 platform/frontend service post frontend display/menu next subcluster selection" in md
    assert "Selected `gpu-fmv-mainloop-service`" in md

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
    for path in (written["subclusters_csv"], written["candidates_csv"], written["summary_csv"], written["handoff_csv"]):
        header = path.read_text(encoding="utf-8").splitlines()[0].split(",")
        assert raw_columns.isdisjoint(header)

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
