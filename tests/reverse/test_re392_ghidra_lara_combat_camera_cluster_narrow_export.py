from pathlib import Path
import csv

from scripts.reverse.re392_ghidra_lara_combat_camera_cluster_narrow_export import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_ghidra_lara_combat_camera_cluster_narrow_export,
    write_all_artifacts,
)


def test_re392_narrows_lara_combat_camera_cluster_to_lara_control_service():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_ghidra_lara_combat_camera_cluster_narrow_export(repo)

    assert bundle.summary.story_id == "RE-392"
    assert bundle.summary.topic == "ghidra-lara-combat-camera-cluster-narrow-export"
    assert bundle.summary.upstream_handoff == "RE-391"
    assert bundle.summary.focus_cluster == "lara-combat-camera-cluster"
    assert bundle.summary.focus_candidate_count == 2
    assert bundle.summary.narrow_subcluster_count == 2
    assert bundle.summary.selected_narrow_subcluster == "lara-control-service"
    assert bundle.summary.selected_narrow_candidate_count == 1
    assert bundle.summary.selected_candidate_ids == "4a632b41837e"
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-393"
    assert bundle.summary.next_topic == "lara-control-service-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.narrow_subcluster for row in bundle.subcluster_rows] == [
        "lara-control-service",
        "combat-camera-service",
    ]
    selected = bundle.subcluster_rows[0]
    assert selected.candidate_count == 1
    assert selected.selection_status == "selected-next"
    assert selected.gate_decision == "gate-before-proof-domain"
    assert selected.next_ticket == "RE-393"
    assert selected.next_topic == "lara-control-service-readiness-gate"

    assert [row.candidate_id for row in bundle.candidate_rows] == ["4a632b41837e", "0aaa76206517"]
    assert [row.narrow_subcluster for row in bundle.candidate_rows] == [
        "lara-control-service",
        "combat-camera-service",
    ]
    assert {row.readiness_gate for row in bundle.candidate_rows} == {"blocked-needs-candidate-level-proof"}
    assert bundle.candidate_rows[0].next_probe == "readiness-gate"
    assert bundle.candidate_rows[1].next_probe == "defer-after-re393"
    assert {row.ready_to_reopen_domain for row in bundle.candidate_rows} == {"no"}
    assert {row.source_patch_authorized for row in bundle.candidate_rows} == {"no"}


def test_re392_writes_metadata_only_narrow_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_ghidra_lara_combat_camera_cluster_narrow_export(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"subclusters_csv", "candidates_csv", "summary_csv", "handoff_csv", "md", "story"}

    subclusters = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert [row["narrow_subcluster"] for row in subclusters] == [
        "lara-control-service",
        "combat-camera-service",
    ]
    assert subclusters[0]["next_ticket"] == "RE-393"
    assert subclusters[0]["next_topic"] == "lara-control-service-readiness-gate"
    assert subclusters[1]["selection_status"] == "deferred-after-selected-subcluster"

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert [row["candidate_id"] for row in candidates] == ["4a632b41837e", "0aaa76206517"]
    assert "ghidra_entry" not in candidates[0]
    assert "ghidra_name" not in candidates[0]
    assert candidates[0]["narrow_subcluster"] == "lara-control-service"
    assert candidates[1]["narrow_subcluster"] == "combat-camera-service"

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-393"
    assert handoff["next_topic"] == "lara-control-service-readiness-gate"
    assert handoff["selected_narrow_subcluster"] == "lara-control-service"
    assert handoff["selected_candidate_ids"] == "4a632b41837e"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["metadata_work_readiness"] == "ready"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-391 lara/combat/camera cluster selection validated." in story
    assert "RE-393" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-392 Ghidra lara/combat/camera cluster narrow export" in md
    assert "Selected `lara-control-service` with `1` candidates." in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
