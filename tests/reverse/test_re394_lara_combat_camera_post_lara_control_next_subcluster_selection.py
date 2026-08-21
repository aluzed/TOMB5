from pathlib import Path
import csv

from scripts.reverse.re394_lara_combat_camera_post_lara_control_next_subcluster_selection import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_lara_combat_camera_post_lara_control_next_subcluster_selection,
    write_all_artifacts,
)


def test_re394_selects_combat_camera_after_lara_control_exhaustion():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_lara_combat_camera_post_lara_control_next_subcluster_selection(repo)

    assert bundle.summary.story_id == "RE-394"
    assert bundle.summary.topic == "lara-combat-camera-post-lara-control-next-subcluster-selection"
    assert bundle.summary.upstream_handoff == "RE-393"
    assert bundle.summary.parent_handoff == "RE-392"
    assert bundle.summary.parent_scope == "lara-combat-camera-cluster-narrow-subclusters"
    assert bundle.summary.closed_narrow_subclusters == "lara-control-service"
    assert bundle.summary.input_subcluster_count == 2
    assert bundle.summary.closed_subcluster_count == 1
    assert bundle.summary.deferred_subcluster_count == 1
    assert bundle.summary.selected_followup_subcluster == "combat-camera-service"
    assert bundle.summary.selected_candidate_count == 1
    assert bundle.summary.selected_candidate_ids == "0aaa76206517"
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-395"
    assert bundle.summary.next_topic == "combat-camera-service-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.narrow_subcluster for row in bundle.subcluster_rows] == ["combat-camera-service"]
    subcluster = bundle.subcluster_rows[0]
    assert subcluster.selection_status == "selected-next"
    assert subcluster.gate_decision == "gate-before-proof-domain"
    assert subcluster.next_ticket == "RE-395"
    assert subcluster.next_topic == "combat-camera-service-readiness-gate"

    assert [row.candidate_id for row in bundle.candidate_rows] == ["0aaa76206517"]
    candidate = bundle.candidate_rows[0]
    assert candidate.source_rank == 17
    assert candidate.narrow_subcluster == "combat-camera-service"
    assert candidate.readiness_gate == "blocked-needs-candidate-level-proof"
    assert candidate.ready_to_reopen_domain == "no"
    assert candidate.source_patch_authorized == "no"
    assert candidate.next_probe == "readiness-gate"


def test_re394_writes_metadata_only_transition_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_lara_combat_camera_post_lara_control_next_subcluster_selection(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"subclusters_csv", "candidates_csv", "summary_csv", "handoff_csv", "md", "story"}

    subclusters = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert len(subclusters) == 1
    assert subclusters[0]["narrow_subcluster"] == "combat-camera-service"
    assert subclusters[0]["candidate_count"] == "1"
    assert subclusters[0]["next_ticket"] == "RE-395"
    assert subclusters[0]["next_topic"] == "combat-camera-service-readiness-gate"

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert len(candidates) == 1
    assert candidates[0]["candidate_id"] == "0aaa76206517"
    assert candidates[0]["narrow_subcluster"] == "combat-camera-service"
    assert "ghidra_entry" not in candidates[0]
    assert "ghidra_name" not in candidates[0]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-395"
    assert handoff["next_topic"] == "combat-camera-service-readiness-gate"
    assert handoff["selected_followup_subcluster"] == "combat-camera-service"
    assert handoff["selected_candidate_ids"] == "0aaa76206517"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["metadata_work_readiness"] == "ready"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-393 lara-control exhaustion handoff validated." in story
    assert "RE-395" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-394 lara combat camera post lara control next subcluster selection" in md
    assert "Selected `combat-camera-service` with `1` source-symbolic candidate." in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
