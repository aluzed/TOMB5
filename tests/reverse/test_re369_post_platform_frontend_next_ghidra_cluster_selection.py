from pathlib import Path
import csv

from scripts.reverse.re369_post_platform_frontend_next_ghidra_cluster_selection import (
    SELECTED_CLUSTER,
    build_post_platform_frontend_next_ghidra_cluster_selection,
    write_all_artifacts,
)

REPO = Path(__file__).resolve().parents[2]


def read_rows(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_build_re369_selects_effects_lighting_from_parent_queue():
    bundle = build_post_platform_frontend_next_ghidra_cluster_selection(REPO)

    assert bundle.summary.story_id == "RE-369"
    assert bundle.summary.topic == "post-platform-frontend-next-ghidra-cluster-selection"
    assert bundle.summary.upstream_handoff == "RE-368"
    assert bundle.summary.parent_handoff == "RE-310"
    assert bundle.summary.parent_scope == "ghidra-bridge-candidate-clusters"
    assert bundle.summary.closed_clusters == "collision-switch-door-cluster;platform-frontend-service-cluster"
    assert bundle.summary.input_cluster_count == 7
    assert bundle.summary.closed_cluster_count == 2
    assert bundle.summary.deferred_cluster_count == 5
    assert bundle.summary.selected_followup_cluster == SELECTED_CLUSTER == "effects-lighting-cluster"
    assert bundle.summary.selected_candidate_count == 4
    assert bundle.summary.selected_candidate_ids == "b6d128932004;f5d0099b5511;3a208e2bf745;87d9c8a62335"
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-370"
    assert bundle.summary.next_topic == "ghidra-effects-lighting-cluster-narrow-export"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    selected = bundle.cluster_rows[0]
    assert selected.cluster == "effects-lighting-cluster"
    assert selected.source_rank == 3
    assert selected.candidate_count == 4
    assert selected.mapped_caller_total == 114
    assert selected.mapped_callee_total == 0
    assert selected.max_source_context_count == 52
    assert selected.selection_status == "selected-next"
    assert selected.next_ticket == "RE-370"

    deferred = [row.cluster for row in bundle.cluster_rows[1:]]
    assert deferred == [
        "maths-render-cluster",
        "lara-combat-camera-cluster",
        "gameflow-save-runtime-cluster",
        "actor-ai-cluster",
    ]
    assert all(row.next_ticket == "TBD" for row in bundle.cluster_rows[1:])
    assert [row.candidate_id for row in bundle.candidate_rows] == [
        "b6d128932004",
        "f5d0099b5511",
        "3a208e2bf745",
        "87d9c8a62335",
    ]


def test_re369_writes_metadata_only_artifacts_and_handoff():
    bundle = build_post_platform_frontend_next_ghidra_cluster_selection(REPO)
    paths = write_all_artifacts(bundle, REPO)

    expected = {"clusters_csv", "candidates_csv", "summary_csv", "handoff_csv", "md", "story"}
    assert set(paths) == expected
    for path in paths.values():
        assert path.exists()
        text = path.read_text(encoding="utf-8").lower()
        assert "payload_offset" not in text
        assert "word_le_hex" not in text
        assert "call_address" not in text
        assert "raw_evidence" not in text
        assert "source_line_text" not in text

    handoff = read_rows(paths["handoff_csv"])[0]
    assert handoff["story_id"] == "RE-369"
    assert handoff["selected_followup_cluster"] == "effects-lighting-cluster"
    assert handoff["next_ticket"] == "RE-370"
    assert handoff["next_topic"] == "ghidra-effects-lighting-cluster-narrow-export"
    assert handoff["selected_domain"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = paths["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-368 platform/frontend service exhaustion validated." in story
    assert "effects-lighting-cluster" in story

    md = paths["md"].read_text(encoding="utf-8")
    assert "# RE-369 post platform-frontend next Ghidra cluster selection" in md
    assert "Code readiness remains `blocked`" in md
