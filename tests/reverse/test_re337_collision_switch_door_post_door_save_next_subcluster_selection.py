from pathlib import Path
import csv

from scripts.reverse.re337_collision_switch_door_post_door_save_next_subcluster_selection import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_collision_switch_door_post_door_save_next_subcluster_selection,
    write_all_artifacts,
)


def test_re337_selects_camera_collision_after_door_save_exhaustion():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_switch_door_post_door_save_next_subcluster_selection(repo)

    assert bundle.summary.story_id == "RE-337"
    assert bundle.summary.topic == "collision-switch-door-post-door-save-next-subcluster-selection"
    assert bundle.summary.upstream_handoff == "RE-336"
    assert bundle.summary.parent_scope == "collision-switch-door-cluster"
    assert bundle.summary.closed_subclusters == (
        "collision-geometry-helper;switch-door-control-helper;"
        "weapon-switch-effect-helper;door-save-runtime-helper"
    )
    assert bundle.summary.input_subcluster_count == 5
    assert bundle.summary.closed_subcluster_count == 4
    assert bundle.summary.deferred_subcluster_count == 1
    assert bundle.summary.selected_narrow_subcluster == "camera-collision-helper"
    assert bundle.summary.selected_narrow_candidate_count == 1
    assert bundle.summary.selected_candidate_ids == "95c41ac597d6"
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-338"
    assert bundle.summary.next_topic == "camera-collision-helper-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.narrow_subcluster for row in bundle.subcluster_rows] == ["camera-collision-helper"]
    selected_subcluster = bundle.subcluster_rows[0]
    assert selected_subcluster.selection_status == "selected-next"
    assert selected_subcluster.gate_decision == "gate-before-proof-domain"
    assert selected_subcluster.candidate_count == 1
    assert selected_subcluster.mapped_caller_total == 11
    assert selected_subcluster.mapped_callee_total == 0
    assert selected_subcluster.source_file_count == 6
    assert selected_subcluster.source_module_count == 1
    assert selected_subcluster.ready_to_reopen_domain == "no"
    assert selected_subcluster.source_patch_authorized == "no"

    selected = bundle.candidate_rows[0]
    assert selected.candidate_id == "95c41ac597d6"
    assert selected.narrow_subcluster == "camera-collision-helper"
    assert selected.bridge_class == "mapped-caller-heavy"
    assert selected.body_size_bucket == "small"
    assert selected.mapped_caller_count == 11
    assert selected.mapped_callee_count == 0
    assert selected.next_probe == "readiness-gate"


def test_re337_writes_metadata_only_next_subcluster_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_switch_door_post_door_save_next_subcluster_selection(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"subclusters_csv", "candidates_csv", "summary_csv", "handoff_csv", "md", "story"}

    subclusters = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert subclusters == [
        {
            "rank": "1",
            "source_rank": "5",
            "narrow_subcluster": "camera-collision-helper",
            "candidate_count": "1",
            "mapped_caller_total": "11",
            "mapped_callee_total": "0",
            "source_file_count": "6",
            "source_module_count": "1",
            "selection_status": "selected-next",
            "gate_decision": "gate-before-proof-domain",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-338",
            "next_topic": "camera-collision-helper-readiness-gate",
            "stop_condition": "candidate-level source-symbolic proof required before proof-domain selection",
        }
    ]

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert candidates == [
        {
            "rank": "1",
            "source_rank": "25",
            "candidate_id": "95c41ac597d6",
            "narrow_subcluster": "camera-collision-helper",
            "bridge_class": "mapped-caller-heavy",
            "body_size_bucket": "small",
            "mapped_caller_count": "11",
            "mapped_callee_count": "0",
            "readiness_gate": "blocked-needs-candidate-level-proof",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_probe": "readiness-gate",
            "stop_condition": "candidate-level source-symbolic proof is required before domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-338"
    assert handoff["next_topic"] == "camera-collision-helper-readiness-gate"
    assert handoff["selected_narrow_subcluster"] == "camera-collision-helper"
    assert handoff["selected_candidate_ids"] == "95c41ac597d6"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-336 door-save candidate queue exhaustion validated." in story
    assert "camera-collision-helper" in story
    assert "RE-338" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-337 collision-switch-door post-door-save next subcluster selection" in md
    assert "Selected `camera-collision-helper`" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
