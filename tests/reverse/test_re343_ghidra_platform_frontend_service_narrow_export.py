from pathlib import Path
import csv

from scripts.reverse.re343_ghidra_platform_frontend_service_narrow_export import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_ghidra_platform_frontend_service_narrow_export,
    write_all_artifacts,
)


def test_re343_groups_platform_frontend_candidates_and_selects_cd_load_audio_service():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_ghidra_platform_frontend_service_narrow_export(repo)

    assert bundle.summary.story_id == "RE-343"
    assert bundle.summary.topic == "ghidra-platform-frontend-service-cluster-narrow-export"
    assert bundle.summary.upstream_handoff == "RE-342"
    assert bundle.summary.focus_cluster == "platform-frontend-service-cluster"
    assert bundle.summary.focus_candidate_count == 6
    assert bundle.summary.narrow_subcluster_count == 4
    assert bundle.summary.selected_narrow_subcluster == "cd-load-audio-service"
    assert bundle.summary.selected_narrow_candidate_count == 2
    assert bundle.summary.selected_candidate_ids == "1e35f3f4fb97;653df7c5909b"
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-344"
    assert bundle.summary.next_topic == "cd-load-audio-service-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.narrow_subcluster for row in bundle.subcluster_rows] == [
        "cd-load-audio-service",
        "frontend-display-menu-service",
        "gpu-fmv-mainloop-service",
        "runtime-callee-bridge",
    ]
    selected = bundle.subcluster_rows[0]
    assert selected.selection_status == "selected-next"
    assert selected.gate_decision == "gate-before-proof-domain"
    assert selected.candidate_count == 2
    assert selected.mapped_caller_total == 52
    assert selected.mapped_callee_total == 0
    assert selected.next_ticket == "RE-344"


def test_re343_writes_metadata_only_narrow_export_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_ghidra_platform_frontend_service_narrow_export(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"subclusters_csv", "candidates_csv", "summary_csv", "handoff_csv", "md", "story"}

    subclusters = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert subclusters[0]["narrow_subcluster"] == "cd-load-audio-service"
    assert subclusters[0]["selection_status"] == "selected-next"
    assert subclusters[0]["next_ticket"] == "RE-344"
    assert all(row["ready_to_reopen_domain"] == "no" for row in subclusters)
    assert all(row["source_patch_authorized"] == "no" for row in subclusters)

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert [row["candidate_id"] for row in candidates[:2]] == ["1e35f3f4fb97", "653df7c5909b"]
    assert all(row["ready_to_reopen_domain"] == "no" for row in candidates)
    assert all(row["source_patch_authorized"] == "no" for row in candidates)

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-344"
    assert handoff["next_topic"] == "cd-load-audio-service-readiness-gate"
    assert handoff["selected_narrow_subcluster"] == "cd-load-audio-service"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-342 platform/frontend cluster selection validated." in story
    assert "cd-load-audio-service" in story
    assert "RE-344" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-343 Ghidra platform/frontend service narrow export" in md
    assert "Selected `cd-load-audio-service`" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
