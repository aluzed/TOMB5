from pathlib import Path
import csv

from scripts.reverse.re389_ghidra_maths_render_cluster_narrow_export import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_ghidra_maths_render_cluster_narrow_export,
    write_all_artifacts,
)


def test_re389_groups_maths_render_candidates_and_selects_matrix_transform_core():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_ghidra_maths_render_cluster_narrow_export(repo)

    assert bundle.summary.story_id == "RE-389"
    assert bundle.summary.topic == "ghidra-maths-render-cluster-narrow-export"
    assert bundle.summary.upstream_handoff == "RE-388"
    assert bundle.summary.focus_cluster == "maths-render-cluster"
    assert bundle.summary.focus_candidate_count == 3
    assert bundle.summary.narrow_subcluster_count == 1
    assert bundle.summary.selected_narrow_subcluster == "matrix-transform-core"
    assert bundle.summary.selected_narrow_candidate_count == 3
    assert bundle.summary.selected_candidate_ids == "cc1a1b589426;6e9ad2da9fce;95467f3600d5"
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-390"
    assert bundle.summary.next_topic == "matrix-transform-core-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.narrow_subcluster for row in bundle.subcluster_rows] == ["matrix-transform-core"]
    selected = bundle.subcluster_rows[0]
    assert selected.selection_status == "selected-next"
    assert selected.gate_decision == "gate-before-proof-domain"
    assert selected.candidate_count == 3
    assert selected.mapped_caller_total == 5
    assert selected.mapped_callee_total == 30
    assert selected.max_source_context_count == 13
    assert selected.bridge_classes == "mapped-callee-bridge;mapped-caller-callee-bridge"
    assert selected.next_ticket == "RE-390"

    assert [row.candidate_id for row in bundle.candidate_rows] == [
        "cc1a1b589426",
        "6e9ad2da9fce",
        "95467f3600d5",
    ]
    assert all(row.narrow_subcluster == "matrix-transform-core" for row in bundle.candidate_rows)
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.candidate_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.candidate_rows)


def test_re389_writes_metadata_only_narrow_export_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_ghidra_maths_render_cluster_narrow_export(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"subclusters_csv", "candidates_csv", "summary_csv", "handoff_csv", "md", "story"}

    subclusters = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert subclusters == [
        {
            "rank": "1",
            "narrow_subcluster": "matrix-transform-core",
            "candidate_count": "3",
            "mapped_caller_total": "5",
            "mapped_callee_total": "30",
            "max_source_context_count": "13",
            "bridge_classes": "mapped-callee-bridge;mapped-caller-callee-bridge",
            "representative_source_context": "GAME:CreateEffect;GAME:FallingBlock;GAME:SmashObject;SPEC_PSXPC:mPopMatrix;SPEC_PSXPC:mPushMatrix;SPEC_PSXPC:mPushUnitMatrix",
            "selection_status": "selected-next",
            "gate_decision": "gate-before-proof-domain",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-390",
            "next_topic": "matrix-transform-core-readiness-gate",
            "stop_condition": "candidate-level source-symbolic proof required before proof-domain selection",
        }
    ]

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert [row["candidate_id"] for row in candidates] == ["cc1a1b589426", "6e9ad2da9fce", "95467f3600d5"]
    assert all(row["narrow_subcluster"] == "matrix-transform-core" for row in candidates)
    assert all(row["readiness_gate"] == "blocked-needs-candidate-level-proof" for row in candidates)
    assert all(row["ready_to_reopen_domain"] == "no" for row in candidates)
    assert all(row["source_patch_authorized"] == "no" for row in candidates)

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-390"
    assert handoff["next_topic"] == "matrix-transform-core-readiness-gate"
    assert handoff["selected_narrow_subcluster"] == "matrix-transform-core"
    assert handoff["selected_candidate_ids"] == "cc1a1b589426;6e9ad2da9fce;95467f3600d5"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-388 maths/render cluster selection validated." in story
    assert "matrix-transform-core" in story
    assert "RE-390" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-389 Ghidra maths/render cluster narrow export" in md
    assert "Selected `matrix-transform-core`" in md

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
    for path in (written["subclusters_csv"], written["candidates_csv"], written["summary_csv"], written["handoff_csv"]):
        header = path.read_text(encoding="utf-8").splitlines()[0].split(",")
        assert raw_columns.isdisjoint(header)

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
