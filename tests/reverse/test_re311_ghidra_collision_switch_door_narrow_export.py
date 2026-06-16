from pathlib import Path
import csv

from scripts.reverse.re311_ghidra_collision_switch_door_narrow_export import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_collision_switch_door_narrow_export,
    write_all_artifacts,
)


def test_re311_builds_narrow_collision_switch_door_export_without_raw_identity():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_switch_door_narrow_export(repo)

    assert bundle.summary.story_id == "RE-311"
    assert bundle.summary.topic == "ghidra-collision-switch-door-cluster-narrow-export"
    assert bundle.summary.upstream_handoff == "RE-310"
    assert bundle.summary.focus_cluster == "collision-switch-door-cluster"
    assert bundle.summary.focus_candidate_count == 7
    assert bundle.summary.hidden_local_identity_resolved_count == 7
    assert bundle.summary.narrow_subcluster_count == 5
    assert bundle.summary.selected_narrow_subcluster == "collision-geometry-helper"
    assert bundle.summary.selected_narrow_candidate_count == 3
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"
    assert bundle.summary.next_ticket == "RE-312"
    assert bundle.summary.next_topic == "collision-geometry-helper-readiness-gate"

    assert len(bundle.candidate_rows) == 7
    assert len(bundle.subcluster_rows) == 5
    assert [row.rank for row in bundle.candidate_rows] == [1, 2, 3, 4, 5, 6, 7]
    top = bundle.subcluster_rows[0]
    assert top.narrow_subcluster == "collision-geometry-helper"
    assert top.candidate_count == 3
    assert top.gate_decision == "gate-before-proof-domain"
    assert top.ready_to_reopen_domain == "no"
    assert top.source_patch_authorized == "no"
    assert top.next_topic == "collision-geometry-helper-readiness-gate"

    selected = [row for row in bundle.candidate_rows if row.narrow_subcluster == "collision-geometry-helper"]
    assert len(selected) == 3
    assert all(row.hidden_local_identity_resolved == "yes" for row in bundle.candidate_rows)
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.candidate_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.candidate_rows)

    for row in bundle.candidate_rows + bundle.subcluster_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "0x" not in row_text


def test_re311_writes_metadata_only_narrow_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_switch_door_narrow_export(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"subclusters_csv", "candidates_csv", "summary_csv", "handoff_csv", "md", "story"}

    subclusters = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert len(subclusters) == 5
    assert subclusters[0]["narrow_subcluster"] == "collision-geometry-helper"
    assert subclusters[0]["candidate_count"] == "3"
    assert subclusters[0]["source_patch_authorized"] == "no"

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert len(candidates) == 7
    assert "ghidra_entry" not in candidates[0]
    assert "ghidra_name" not in candidates[0]
    assert candidates[0]["hidden_local_identity_resolved"] == "yes"

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-312"
    assert handoff["next_topic"] == "collision-geometry-helper-readiness-gate"
    assert handoff["selected_narrow_subcluster"] == "collision-geometry-helper"
    assert handoff["metadata_work_readiness"] == "ready"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-310 focus cluster validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-312" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-311 Ghidra collision/switch/door narrow export" in md
    assert "raw Ghidra identity remains local-only" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
