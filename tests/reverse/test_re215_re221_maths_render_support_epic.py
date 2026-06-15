from pathlib import Path
import csv

from scripts.reverse.re215_re221_maths_render_support_epic import (
    FORBIDDEN,
    STALE_FRAGMENTS,
    build_epic,
    write_all_artifacts,
)


def test_re215_re221_consumes_re214_and_closes_maths_render_support_epic():
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)

    assert epic.story_range == "RE-215..RE-221"
    assert epic.domain_id == "maths-render-support"
    assert epic.upstream_ticket == "RE-214"
    assert epic.selected_subcluster == "matrix-transform-core"
    assert epic.selected_pivot == "mTranslateXYZ"
    assert epic.candidate_count == 92
    assert epic.closed_candidate_count == 92
    assert epic.code_change_ready_count == 0
    assert epic.marker_ready_count == 0
    assert epic.domain_outcome == "documentation-only-terminal-blocker"
    assert epic.blocker == "missing-maths-render-source-contract-and-non-raw-equivalence-proof"

    assert [row.story_id for row in epic.story_rows] == [
        "RE-215",
        "RE-216",
        "RE-217",
        "RE-218",
        "RE-219",
        "RE-220",
        "RE-221",
    ]
    assert [row.topic for row in epic.story_rows] == [
        "maths-render-support-matrix-transform-chain",
        "maths-render-support-gpu-scene-chain",
        "maths-render-support-object-draw-chain",
        "maths-render-support-draw-phase-chain",
        "maths-render-support-cross-platform-reconciliation",
        "maths-render-support-source-patch-gate",
        "post-maths-render-support-domain-selection",
    ]

    closure_by_subcluster = {row.subcluster: row for row in epic.subcluster_rows}
    assert closure_by_subcluster["matrix-transform-core"].candidate_count == 37
    assert closure_by_subcluster["gpu-scene-support"].candidate_count == 17
    assert closure_by_subcluster["object-draw-support"].candidate_count == 36
    assert closure_by_subcluster["draw-phase-support"].candidate_count == 2
    assert all(row.code_change_ready == "no" for row in epic.subcluster_rows)
    assert all(row.outcome == "blocked-no-patch" for row in epic.subcluster_rows)

    assert epic.handoff.next_ticket == "RE-222"
    assert epic.handoff.next_topic == "traps-switches-doors-proof-first-audit"
    assert epic.handoff.selected_domain == "traps-switches-doors"
    assert epic.handoff.selected_pivot == "ControlRollingBall"
    assert epic.handoff.reason == "maths-render-support closed as a documentation-only terminal blocker; next ranked remaining RE-213 domain selected"


def test_re215_re221_outputs_epic_artifacts_stories_and_metadata_only(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)
    written = write_all_artifacts(epic, tmp_path)

    expected_keys = {
        "epic_csv",
        "subclusters_csv",
        "gate_csv",
        "next_selection_csv",
        "handoff_csv",
        "md",
        "story_index",
        "stories",
    }
    assert set(written) == expected_keys
    assert len(written["stories"]) == 7

    epic_rows = list(csv.DictReader(written["epic_csv"].open(newline="", encoding="utf-8")))
    assert len(epic_rows) == 7
    assert epic_rows[0]["story_id"] == "RE-215"
    assert epic_rows[-1]["story_id"] == "RE-221"
    assert {row["readiness"] for row in epic_rows} == {"blocked"}
    assert {row["source_patch_ready"] for row in epic_rows} == {"no"}

    subclusters = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert [row["subcluster"] for row in subclusters] == [
        "matrix-transform-core",
        "gpu-scene-support",
        "object-draw-support",
        "draw-phase-support",
    ]
    assert sum(int(row["candidate_count"]) for row in subclusters) == 92

    gates = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert len(gates) == 3
    assert [row["gate"] for row in gates] == ["equivalence", "source-patch", "marker"]
    assert {row["decision"] for row in gates} == {"deny"}

    next_rows = list(csv.DictReader(written["next_selection_csv"].open(newline="", encoding="utf-8")))
    assert next_rows[0]["domain_id"] == "traps-switches-doors"
    assert next_rows[0]["next_ticket"] == "RE-222"
    assert next_rows[0]["top_function"] == "ControlRollingBall"
    assert "maths-render-support" not in [row["domain_id"] for row in next_rows]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-222"
    assert handoff["next_topic"] == "traps-switches-doors-proof-first-audit"
    assert handoff["selected_domain"] == "traps-switches-doors"
    assert handoff["selected_pivot"] == "ControlRollingBall"

    md_text = written["md"].read_text(encoding="utf-8")
    assert "# RE-215..RE-221 maths-render-support epic" in md_text
    assert "documentation-only terminal blocker" in md_text
    assert "Next proof domain: `traps-switches-doors`" in md_text
    assert "Recommended next ticket: `RE-222`" in md_text

    story_index = written["story_index"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_index
    assert "RE-215..RE-221" in story_index
    assert "No production source or marker change is authorized" in story_index

    for story_id, story_path in written["stories"].items():
        story = story_path.read_text(encoding="utf-8")
        assert f"# {story_id}" in story
        assert "## Progress tracker" in story
        assert "Readiness: `blocked`" in story
        assert "No production source or marker change is authorized" in story

    all_paths = [p for key, value in written.items() if key != "stories" for p in [value]] + list(written["stories"].values())
    for path in all_paths:
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN + STALE_FRAGMENTS:
            assert fragment not in text
