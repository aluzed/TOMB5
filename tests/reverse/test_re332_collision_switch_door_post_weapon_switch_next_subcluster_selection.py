from pathlib import Path
import csv

from scripts.reverse.re332_collision_switch_door_post_weapon_switch_next_subcluster_selection import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_collision_switch_door_post_weapon_switch_next_subcluster_selection,
    write_all_artifacts,
)


def test_re332_selects_door_save_runtime_after_weapon_switch_exhaustion():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_switch_door_post_weapon_switch_next_subcluster_selection(repo)

    assert bundle.summary.story_id == "RE-332"
    assert bundle.summary.topic == "collision-switch-door-post-weapon-switch-next-subcluster-selection"
    assert bundle.summary.upstream_handoff == "RE-331"
    assert bundle.summary.parent_scope == "collision-switch-door-cluster"
    assert bundle.summary.closed_subclusters == "collision-geometry-helper;switch-door-control-helper;weapon-switch-effect-helper"
    assert bundle.summary.input_subcluster_count == 5
    assert bundle.summary.closed_subcluster_count == 3
    assert bundle.summary.deferred_subcluster_count == 2
    assert bundle.summary.selected_narrow_subcluster == "door-save-runtime-helper"
    assert bundle.summary.selected_narrow_candidate_count == 1
    assert bundle.summary.selected_candidate_ids == "f457f2772655"
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-333"
    assert bundle.summary.next_topic == "door-save-runtime-helper-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.narrow_subcluster for row in bundle.subcluster_rows] == [
        "door-save-runtime-helper",
        "camera-collision-helper",
    ]
    assert [row.selection_status for row in bundle.subcluster_rows] == [
        "selected-next",
        "deferred-after-selected-subcluster",
    ]
    assert [row.candidate_count for row in bundle.subcluster_rows] == [1, 1]
    assert [row.mapped_caller_total for row in bundle.subcluster_rows] == [14, 11]
    assert [row.mapped_callee_total for row in bundle.subcluster_rows] == [0, 0]
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.subcluster_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.subcluster_rows)

    selected = bundle.candidate_rows[0]
    assert selected.candidate_id == "f457f2772655"
    assert selected.narrow_subcluster == "door-save-runtime-helper"
    assert selected.bridge_class == "mapped-caller-heavy"
    assert selected.body_size_bucket == "tiny"
    assert selected.mapped_caller_count == 14
    assert selected.mapped_callee_count == 0
    assert selected.next_probe == "readiness-gate"


def test_re332_writes_metadata_only_next_subcluster_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_switch_door_post_weapon_switch_next_subcluster_selection(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"subclusters_csv", "candidates_csv", "summary_csv", "handoff_csv", "md", "story"}

    subclusters = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert len(subclusters) == 2
    assert subclusters[0]["narrow_subcluster"] == "door-save-runtime-helper"
    assert subclusters[0]["selection_status"] == "selected-next"
    assert subclusters[0]["next_ticket"] == "RE-333"
    assert subclusters[0]["next_topic"] == "door-save-runtime-helper-readiness-gate"
    assert subclusters[-1]["narrow_subcluster"] == "camera-collision-helper"

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert candidates == [
        {
            "rank": "1",
            "source_rank": "19",
            "candidate_id": "f457f2772655",
            "narrow_subcluster": "door-save-runtime-helper",
            "bridge_class": "mapped-caller-heavy",
            "body_size_bucket": "tiny",
            "mapped_caller_count": "14",
            "mapped_callee_count": "0",
            "readiness_gate": "blocked-needs-candidate-level-proof",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_probe": "readiness-gate",
            "stop_condition": "candidate-level source-symbolic proof is required before domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-333"
    assert handoff["next_topic"] == "door-save-runtime-helper-readiness-gate"
    assert handoff["selected_narrow_subcluster"] == "door-save-runtime-helper"
    assert handoff["selected_candidate_ids"] == "f457f2772655"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-331 weapon-switch candidate queue exhaustion validated." in story
    assert "door-save-runtime-helper" in story
    assert "RE-333" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-332 collision-switch-door post-weapon-switch next subcluster selection" in md
    assert "Selected `door-save-runtime-helper`" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
