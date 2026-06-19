from pathlib import Path
import csv

from scripts.reverse.re351_platform_frontend_service_post_cd_load_audio_next_subcluster_selection import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_platform_frontend_service_post_cd_load_audio_next_subcluster_selection,
    write_all_artifacts,
)


def test_re351_selects_frontend_display_menu_after_cd_load_audio_exhaustion():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_platform_frontend_service_post_cd_load_audio_next_subcluster_selection(repo)

    assert bundle.summary.story_id == "RE-351"
    assert bundle.summary.topic == "platform-frontend-service-post-cd-load-audio-next-subcluster-selection"
    assert bundle.summary.upstream_handoff == "RE-350"
    assert bundle.summary.parent_scope == "platform-frontend-service-cluster"
    assert bundle.summary.closed_subclusters == "cd-load-audio-service"
    assert bundle.summary.input_subcluster_count == 4
    assert bundle.summary.closed_subcluster_count == 1
    assert bundle.summary.deferred_subcluster_count == 3
    assert bundle.summary.selected_narrow_subcluster == "frontend-display-menu-service"
    assert bundle.summary.selected_narrow_candidate_count == 2
    assert bundle.summary.selected_candidate_ids == "de919274685f;4c90c6af8f9d"
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-352"
    assert bundle.summary.next_topic == "frontend-display-menu-service-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.narrow_subcluster for row in bundle.subcluster_rows] == ["frontend-display-menu-service"]
    selected_subcluster = bundle.subcluster_rows[0]
    assert selected_subcluster.source_rank == 2
    assert selected_subcluster.candidate_count == 2
    assert selected_subcluster.mapped_caller_total == 43
    assert selected_subcluster.mapped_callee_total == 0
    assert selected_subcluster.max_source_context_count == 25
    assert selected_subcluster.selection_status == "selected-next"
    assert selected_subcluster.gate_decision == "gate-before-proof-domain"
    assert selected_subcluster.ready_to_reopen_domain == "no"
    assert selected_subcluster.source_patch_authorized == "no"

    assert [row.candidate_id for row in bundle.candidate_rows] == ["de919274685f", "4c90c6af8f9d"]
    first, second = bundle.candidate_rows
    assert first.source_rank == 8
    assert first.bridge_class == "mapped-caller-heavy"
    assert first.body_size_bucket == "tiny"
    assert first.mapped_caller_count == 25
    assert first.mapped_callee_count == 0
    assert first.source_context_count == 25
    assert first.next_probe == "candidate-proof-export"
    assert second.source_rank == 14
    assert second.body_size_bucket == "medium"
    assert second.mapped_caller_count == 18
    assert second.next_probe == "defer-after-re352"
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.candidate_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.candidate_rows)


def test_re351_writes_metadata_only_next_subcluster_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_platform_frontend_service_post_cd_load_audio_next_subcluster_selection(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"subclusters_csv", "candidates_csv", "summary_csv", "handoff_csv", "md", "story"}

    subclusters = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert subclusters == [
        {
            "rank": "1",
            "source_rank": "2",
            "narrow_subcluster": "frontend-display-menu-service",
            "candidate_count": "2",
            "mapped_caller_total": "43",
            "mapped_callee_total": "0",
            "max_source_context_count": "25",
            "bridge_classes": "mapped-caller-heavy",
            "selection_status": "selected-next",
            "gate_decision": "gate-before-proof-domain",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-352",
            "next_topic": "frontend-display-menu-service-readiness-gate",
            "stop_condition": "candidate-level source-symbolic proof required before proof-domain selection",
        }
    ]

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert candidates == [
        {
            "rank": "1",
            "source_rank": "8",
            "candidate_id": "de919274685f",
            "narrow_subcluster": "frontend-display-menu-service",
            "bridge_class": "mapped-caller-heavy",
            "body_size_bucket": "tiny",
            "mapped_caller_count": "25",
            "mapped_callee_count": "0",
            "source_context_count": "25",
            "readiness_gate": "blocked-needs-candidate-level-proof",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_probe": "candidate-proof-export",
            "stop_condition": "candidate-level source-symbolic proof is required before domain selection",
        },
        {
            "rank": "2",
            "source_rank": "14",
            "candidate_id": "4c90c6af8f9d",
            "narrow_subcluster": "frontend-display-menu-service",
            "bridge_class": "mapped-caller-heavy",
            "body_size_bucket": "medium",
            "mapped_caller_count": "18",
            "mapped_callee_count": "0",
            "source_context_count": "18",
            "readiness_gate": "blocked-needs-candidate-level-proof",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_probe": "defer-after-re352",
            "stop_condition": "candidate-level source-symbolic proof is required before domain selection",
        },
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-352"
    assert handoff["next_topic"] == "frontend-display-menu-service-readiness-gate"
    assert handoff["selected_narrow_subcluster"] == "frontend-display-menu-service"
    assert handoff["selected_candidate_ids"] == "de919274685f;4c90c6af8f9d"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-350 cd/load/audio queue exhaustion validated." in story
    assert "frontend-display-menu-service" in story
    assert "RE-352" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-351 platform/frontend service post cd/load/audio next subcluster selection" in md
    assert "Selected `frontend-display-menu-service`" in md

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
