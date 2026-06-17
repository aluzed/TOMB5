from pathlib import Path
import csv

from scripts.reverse.re322_collision_switch_door_next_subcluster_selection import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_collision_switch_door_next_subcluster_selection,
    write_all_artifacts,
)


def test_re322_selects_next_deferred_subcluster_after_collision_geometry_exhaustion():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_switch_door_next_subcluster_selection(repo)

    assert bundle.summary.story_id == "RE-322"
    assert bundle.summary.topic == "collision-switch-door-next-subcluster-selection"
    assert bundle.summary.upstream_handoff == "RE-321"
    assert bundle.summary.parent_scope == "collision-switch-door-cluster"
    assert bundle.summary.closed_subcluster == "collision-geometry-helper"
    assert bundle.summary.input_subcluster_count == 5
    assert bundle.summary.closed_subcluster_count == 1
    assert bundle.summary.deferred_subcluster_count == 4
    assert bundle.summary.selected_narrow_subcluster == "switch-door-control-helper"
    assert bundle.summary.selected_narrow_candidate_count == 1
    assert bundle.summary.selected_candidate_ids == "8d1fc6fc3cfc"
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-323"
    assert bundle.summary.next_topic == "switch-door-control-helper-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.narrow_subcluster for row in bundle.subcluster_rows] == [
        "switch-door-control-helper",
        "weapon-switch-effect-helper",
        "door-save-runtime-helper",
        "camera-collision-helper",
    ]
    assert [row.selection_status for row in bundle.subcluster_rows] == [
        "selected-next",
        "deferred-after-selected-subcluster",
        "deferred-after-selected-subcluster",
        "deferred-after-selected-subcluster",
    ]
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.subcluster_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.subcluster_rows)

    selected = bundle.candidate_rows[0]
    assert selected.candidate_id == "8d1fc6fc3cfc"
    assert selected.narrow_subcluster == "switch-door-control-helper"
    assert selected.next_probe == "readiness-gate"


def test_re322_writes_metadata_only_next_subcluster_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_switch_door_next_subcluster_selection(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"subclusters_csv", "candidates_csv", "summary_csv", "handoff_csv", "md", "story"}

    subclusters = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert len(subclusters) == 4
    assert subclusters[0]["narrow_subcluster"] == "switch-door-control-helper"
    assert subclusters[0]["selection_status"] == "selected-next"
    assert subclusters[0]["next_ticket"] == "RE-323"
    assert subclusters[0]["next_topic"] == "switch-door-control-helper-readiness-gate"
    assert subclusters[-1]["narrow_subcluster"] == "camera-collision-helper"

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert candidates == [
        {
            "rank": "1",
            "source_rank": "6",
            "candidate_id": "8d1fc6fc3cfc",
            "narrow_subcluster": "switch-door-control-helper",
            "bridge_class": "mapped-caller-heavy",
            "body_size_bucket": "medium",
            "mapped_caller_count": "22",
            "mapped_callee_count": "3",
            "readiness_gate": "blocked-needs-candidate-level-proof",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_probe": "readiness-gate",
            "stop_condition": "candidate-level source-symbolic proof is required before domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-323"
    assert handoff["next_topic"] == "switch-door-control-helper-readiness-gate"
    assert handoff["selected_narrow_subcluster"] == "switch-door-control-helper"
    assert handoff["selected_candidate_ids"] == "8d1fc6fc3cfc"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-321 collision-geometry queue exhaustion validated." in story
    assert "switch-door-control-helper" in story
    assert "RE-323" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-322 collision-switch-door next subcluster selection" in md
    assert "Selected `switch-door-control-helper`" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
