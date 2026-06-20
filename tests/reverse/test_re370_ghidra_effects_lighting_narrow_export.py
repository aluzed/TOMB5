from pathlib import Path
import csv

from scripts.reverse.re370_ghidra_effects_lighting_narrow_export import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_ghidra_effects_lighting_narrow_export,
    write_all_artifacts,
)


def test_re370_groups_effects_lighting_candidates_and_selects_dynamic_lighting_service():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_ghidra_effects_lighting_narrow_export(repo)

    assert bundle.summary.story_id == "RE-370"
    assert bundle.summary.topic == "ghidra-effects-lighting-cluster-narrow-export"
    assert bundle.summary.upstream_handoff == "RE-369"
    assert bundle.summary.focus_cluster == "effects-lighting-cluster"
    assert bundle.summary.focus_candidate_count == 4
    assert bundle.summary.narrow_subcluster_count == 3
    assert bundle.summary.selected_narrow_subcluster == "dynamic-lighting-service"
    assert bundle.summary.selected_narrow_candidate_count == 2
    assert bundle.summary.selected_candidate_ids == "f5d0099b5511;3a208e2bf745"
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-371"
    assert bundle.summary.next_topic == "dynamic-lighting-service-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.narrow_subcluster for row in bundle.subcluster_rows] == [
        "dynamic-lighting-service",
        "explosion-flare-effect-service",
        "spotcam-projectile-effect-service",
    ]
    selected = bundle.subcluster_rows[0]
    assert selected.selection_status == "selected-next"
    assert selected.gate_decision == "gate-before-proof-domain"
    assert selected.candidate_count == 2
    assert selected.mapped_caller_total == 44
    assert selected.mapped_callee_total == 0
    assert selected.next_ticket == "RE-371"


def test_re370_writes_metadata_only_narrow_export_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_ghidra_effects_lighting_narrow_export(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"subclusters_csv", "candidates_csv", "summary_csv", "handoff_csv", "md", "story"}

    subclusters = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert subclusters[0]["narrow_subcluster"] == "dynamic-lighting-service"
    assert subclusters[0]["selection_status"] == "selected-next"
    assert subclusters[0]["next_ticket"] == "RE-371"
    assert all(row["ready_to_reopen_domain"] == "no" for row in subclusters)
    assert all(row["source_patch_authorized"] == "no" for row in subclusters)

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert [row["candidate_id"] for row in candidates[:2]] == ["f5d0099b5511", "3a208e2bf745"]
    assert candidates[0]["narrow_subcluster"] == "dynamic-lighting-service"
    assert all(row["ready_to_reopen_domain"] == "no" for row in candidates)
    assert all(row["source_patch_authorized"] == "no" for row in candidates)

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-371"
    assert handoff["next_topic"] == "dynamic-lighting-service-readiness-gate"
    assert handoff["selected_narrow_subcluster"] == "dynamic-lighting-service"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-369 effects/lighting cluster selection validated." in story
    assert "dynamic-lighting-service" in story
    assert "RE-371" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-370 Ghidra effects/lighting narrow export" in md
    assert "Selected `dynamic-lighting-service`" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
