from pathlib import Path
import csv

from scripts.reverse.re388_post_effects_lighting_next_ghidra_cluster_selection import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_post_effects_lighting_next_ghidra_cluster_selection,
    write_all_artifacts,
)


def test_re388_selects_maths_render_after_effects_lighting_exhaustion():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_post_effects_lighting_next_ghidra_cluster_selection(repo)

    assert bundle.summary.story_id == "RE-388"
    assert bundle.summary.topic == "post-effects-lighting-next-ghidra-cluster-selection"
    assert bundle.summary.upstream_handoff == "RE-387"
    assert bundle.summary.parent_handoff == "RE-369"
    assert bundle.summary.parent_scope == "ghidra-bridge-candidate-clusters"
    assert bundle.summary.closed_clusters == "collision-switch-door-cluster;platform-frontend-service-cluster;effects-lighting-cluster"
    assert bundle.summary.input_cluster_count == 5
    assert bundle.summary.closed_cluster_count == 3
    assert bundle.summary.deferred_cluster_count == 4
    assert bundle.summary.selected_followup_cluster == "maths-render-cluster"
    assert bundle.summary.selected_candidate_count == 3
    assert bundle.summary.selected_candidate_ids == "cc1a1b589426;6e9ad2da9fce;95467f3600d5"
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-389"
    assert bundle.summary.next_topic == "ghidra-maths-render-cluster-narrow-export"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.cluster for row in bundle.cluster_rows] == [
        "maths-render-cluster",
        "lara-combat-camera-cluster",
        "gameflow-save-runtime-cluster",
        "actor-ai-cluster",
    ]
    selected = bundle.cluster_rows[0]
    assert selected.source_rank == 4
    assert selected.candidate_count == 3
    assert selected.mapped_caller_total == 5
    assert selected.mapped_callee_total == 30
    assert selected.max_source_context_count == 13
    assert selected.bridge_classes == "mapped-callee-bridge;mapped-caller-callee-bridge"
    assert selected.selection_status == "selected-next"
    assert selected.gate_decision == "needs-narrow-source-symbolic-export"
    assert selected.ready_to_reopen_domain == "no"
    assert selected.source_patch_authorized == "no"

    assert [row.candidate_id for row in bundle.candidate_rows] == [
        "cc1a1b589426",
        "6e9ad2da9fce",
        "95467f3600d5",
    ]
    first = bundle.candidate_rows[0]
    assert first.source_rank == 21
    assert first.source_cluster == "maths-render-cluster"
    assert first.bridge_class == "mapped-caller-callee-bridge"
    assert first.body_size_bucket == "medium"
    assert first.mapped_caller_count == 2
    assert first.mapped_callee_count == 11
    assert first.source_context_count == 13
    assert first.next_probe == "narrow-source-symbolic-export"


def test_re388_writes_metadata_only_next_cluster_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_post_effects_lighting_next_ghidra_cluster_selection(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"clusters_csv", "candidates_csv", "summary_csv", "handoff_csv", "md", "story"}

    clusters = list(csv.DictReader(written["clusters_csv"].open(newline="", encoding="utf-8")))
    assert clusters[0] == {
        "rank": "1",
        "source_rank": "4",
        "cluster": "maths-render-cluster",
        "candidate_count": "3",
        "mapped_caller_total": "5",
        "mapped_callee_total": "30",
        "max_source_context_count": "13",
        "bridge_classes": "mapped-callee-bridge;mapped-caller-callee-bridge",
        "representative_source_context": "GAME:CreateEffect;GAME:FallingBlock;GAME:SmashObject;SPEC_PSXPC:mPopMatrix;SPEC_PSXPC:mPushMatrix;SPEC_PSXPC:mPushUnitMatrix",
        "selection_status": "selected-next",
        "gate_decision": "needs-narrow-source-symbolic-export",
        "ready_to_reopen_domain": "no",
        "source_patch_authorized": "no",
        "next_ticket": "RE-389",
        "next_topic": "ghidra-maths-render-cluster-narrow-export",
        "stop_condition": "narrow source-symbolic export required before proof-domain selection",
    }
    assert [row["cluster"] for row in clusters] == [
        "maths-render-cluster",
        "lara-combat-camera-cluster",
        "gameflow-save-runtime-cluster",
        "actor-ai-cluster",
    ]

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert [row["candidate_id"] for row in candidates] == ["cc1a1b589426", "6e9ad2da9fce", "95467f3600d5"]
    assert candidates[0]["source_rank"] == "21"
    assert candidates[0]["source_cluster"] == "maths-render-cluster"
    assert candidates[0]["readiness_gate"] == "blocked-needs-narrow-source-symbolic-export"
    assert candidates[0]["ready_to_reopen_domain"] == "no"
    assert candidates[0]["source_patch_authorized"] == "no"

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-389"
    assert handoff["next_topic"] == "ghidra-maths-render-cluster-narrow-export"
    assert handoff["selected_followup_cluster"] == "maths-render-cluster"
    assert handoff["selected_candidate_ids"] == "cc1a1b589426;6e9ad2da9fce;95467f3600d5"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-387 effects/lighting cluster exhaustion validated." in story
    assert "maths-render-cluster" in story
    assert "RE-389" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-388 post effects-lighting next Ghidra cluster selection" in md
    assert "Selected `maths-render-cluster`" in md

    raw_columns = {
        "ghidra_entry",
        "ghidra_name",
        "call_address",
        "payload_offset",
        "word_le_hex",
        "opcode",
        "raw_evidence",
        "source_line_text",
    }
    for path in (written["clusters_csv"], written["candidates_csv"], written["summary_csv"], written["handoff_csv"]):
        header = path.read_text(encoding="utf-8").splitlines()[0].split(",")
        assert raw_columns.isdisjoint(header)

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
