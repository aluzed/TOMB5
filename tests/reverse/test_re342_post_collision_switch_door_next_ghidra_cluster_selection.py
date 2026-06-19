from pathlib import Path
import csv

from scripts.reverse.re342_post_collision_switch_door_next_ghidra_cluster_selection import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_post_collision_switch_door_next_ghidra_cluster_selection,
    write_all_artifacts,
)


def test_re342_selects_platform_frontend_after_collision_switch_door_exhaustion():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_post_collision_switch_door_next_ghidra_cluster_selection(repo)

    assert bundle.summary.story_id == "RE-342"
    assert bundle.summary.topic == "post-collision-switch-door-next-ghidra-cluster-selection"
    assert bundle.summary.upstream_handoff == "RE-341"
    assert bundle.summary.parent_handoff == "RE-310"
    assert bundle.summary.parent_scope == "ghidra-bridge-candidate-clusters"
    assert bundle.summary.closed_clusters == "collision-switch-door-cluster"
    assert bundle.summary.input_cluster_count == 7
    assert bundle.summary.closed_cluster_count == 1
    assert bundle.summary.deferred_cluster_count == 6
    assert bundle.summary.selected_followup_cluster == "platform-frontend-service-cluster"
    assert bundle.summary.selected_candidate_count == 6
    assert bundle.summary.selected_candidate_ids == "1e35f3f4fb97;de919274685f;4c90c6af8f9d;653df7c5909b;1b3534d34062;a01f47cb95a4"
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-343"
    assert bundle.summary.next_topic == "ghidra-platform-frontend-service-cluster-narrow-export"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.cluster for row in bundle.cluster_rows] == [
        "platform-frontend-service-cluster",
        "effects-lighting-cluster",
        "maths-render-cluster",
        "lara-combat-camera-cluster",
        "gameflow-save-runtime-cluster",
        "actor-ai-cluster",
    ]
    selected_cluster = bundle.cluster_rows[0]
    assert selected_cluster.selection_status == "selected-next"
    assert selected_cluster.gate_decision == "needs-narrow-source-symbolic-export"
    assert selected_cluster.candidate_count == 6
    assert selected_cluster.mapped_caller_total == 109
    assert selected_cluster.mapped_callee_total == 13
    assert selected_cluster.next_ticket == "RE-343"


def test_re342_writes_metadata_only_cluster_selection_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_post_collision_switch_door_next_ghidra_cluster_selection(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"clusters_csv", "candidates_csv", "summary_csv", "handoff_csv", "md", "story"}

    clusters = list(csv.DictReader(written["clusters_csv"].open(newline="", encoding="utf-8")))
    assert clusters[0]["cluster"] == "platform-frontend-service-cluster"
    assert clusters[0]["selection_status"] == "selected-next"
    assert clusters[0]["next_ticket"] == "RE-343"
    assert clusters[0]["next_topic"] == "ghidra-platform-frontend-service-cluster-narrow-export"
    assert all(row["ready_to_reopen_domain"] == "no" for row in clusters)
    assert all(row["source_patch_authorized"] == "no" for row in clusters)

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert [row["candidate_id"] for row in candidates[:2]] == ["1e35f3f4fb97", "de919274685f"]
    assert all(row["source_cluster"] == "platform-frontend-service-cluster" for row in candidates[:6])
    assert all(row["ready_to_reopen_domain"] == "no" for row in candidates)
    assert all(row["source_patch_authorized"] == "no" for row in candidates)

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-343"
    assert handoff["next_topic"] == "ghidra-platform-frontend-service-cluster-narrow-export"
    assert handoff["selected_followup_cluster"] == "platform-frontend-service-cluster"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-341 camera-collision exhaustion validated." in story
    assert "platform-frontend-service-cluster" in story
    assert "RE-343" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-342 post collision-switch-door next Ghidra cluster selection" in md
    assert "Selected `platform-frontend-service-cluster`" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
