from pathlib import Path
import csv

from scripts.reverse.re275_re282_animation_items_epic import (
    FORBIDDEN,
    STALE_FRAGMENTS,
    build_epic,
    write_all_artifacts,
)


def test_re275_re282_selects_and_closes_animation_items_epic():
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)

    assert epic.story_range == "RE-275..RE-282"
    assert epic.upstream_ticket == "RE-274"
    assert epic.domain_id == "animation-items"
    assert epic.selected_pivot == "CalcAnimatingItem_ASM"
    assert epic.raw_priority_count == 31
    assert epic.parser_artifact_count == 0
    assert epic.candidate_count == 31
    assert epic.closed_candidate_count == 31
    assert epic.runtime_count == 3
    assert epic.nd_count == 1
    assert epic.code_change_ready_count == 0
    assert epic.marker_ready_count == 0
    assert epic.domain_outcome == "documentation-only-terminal-blocker"
    assert epic.blocker == "missing-animation-item-state-contract-and-non-raw-equivalence-proof"

    assert [row.story_id for row in epic.story_rows] == [
        "RE-275", "RE-276", "RE-277", "RE-278", "RE-279", "RE-280", "RE-281", "RE-282",
    ]
    assert [row.topic for row in epic.story_rows] == [
        "post-camera-domain-reprioritization",
        "animation-items-proof-first-audit",
        "animation-items-runtime-reload-chain",
        "animation-items-animitem-core-chain",
        "animation-items-matrix-transform-chain",
        "animation-items-state-equivalence-gate",
        "animation-items-source-patch-gate",
        "post-animation-items-domain-handoff",
    ]

    selection = {row.domain_id: row for row in epic.selection_rows}
    assert list(selection)[:2] == ["animation-items", "module-spec_pc_n"]
    assert selection["animation-items"].next_ticket == "RE-276"
    assert selection["animation-items"].top_function == "CalcAnimatingItem_ASM"
    assert selection["module-spec_pc_n"].next_ticket == "TBD"

    subclusters = {row.subcluster: row for row in epic.subcluster_rows}
    assert subclusters["runtime-reload"].candidate_count == 4
    assert subclusters["runtime-reload"].top_function == "ReloadAnims"
    assert subclusters["animitem-core"].candidate_count == 4
    assert subclusters["animitem-core"].top_function == "CalcAnimatingItem_ASM"
    assert subclusters["matrix-transform"].candidate_count == 21
    assert subclusters["matrix-transform"].top_function == "GetBounds_AI"
    assert subclusters["texture-object-animation"].candidate_count == 2
    assert subclusters["texture-object-animation"].top_function == "AnimateWaterfalls"
    assert all(row.code_change_ready == "no" for row in epic.subcluster_rows)
    assert all(row.marker_ready == "no" for row in epic.subcluster_rows)

    assert epic.handoff.next_ticket == "TBD"
    assert epic.handoff.next_topic == "post-animation-items-domain-selection-needed"
    assert epic.handoff.selected_domain == "module-spec_pc_n"
    assert epic.handoff.selected_pivot == "if"


def test_re275_re282_outputs_artifacts_stories_and_metadata_only(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)
    written = write_all_artifacts(epic, tmp_path)

    assert set(written) == {
        "selection_csv", "audit_csv", "subclusters_csv", "epic_csv", "gate_csv", "handoff_csv", "md", "story_index", "stories",
    }
    assert len(written["stories"]) == 8

    selection_rows = list(csv.DictReader(written["selection_csv"].open(newline="", encoding="utf-8")))
    assert [row["domain_id"] for row in selection_rows] == ["animation-items", "module-spec_pc_n"]
    assert selection_rows[0]["next_ticket"] == "RE-276"

    audit_rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(audit_rows) == 31
    assert audit_rows[0]["function"] == "ReloadAnims"
    assert {row["domain_id"] for row in audit_rows} == {"animation-items"}
    assert {row["readiness"] for row in audit_rows} == {"blocked"}
    assert {row["source_patch_ready"] for row in audit_rows} == {"no"}
    assert all(row["file"] for row in audit_rows)
    assert all(int(row["line"]) > 0 for row in audit_rows)

    subcluster_rows = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert [row["subcluster"] for row in subcluster_rows] == [
        "runtime-reload", "animitem-core", "matrix-transform", "texture-object-animation",
    ]
    assert sum(int(row["candidate_count"]) for row in subcluster_rows) == 31

    epic_rows = list(csv.DictReader(written["epic_csv"].open(newline="", encoding="utf-8")))
    assert epic_rows[0]["story_id"] == "RE-275"
    assert epic_rows[-1]["story_id"] == "RE-282"
    assert {row["readiness"] for row in epic_rows} == {"blocked"}

    gates = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert [row["gate"] for row in gates] == ["equivalence", "source-patch", "marker"]
    assert {row["decision"] for row in gates} == {"deny"}

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "TBD"
    assert handoff["selected_domain"] == "module-spec_pc_n"
    assert handoff["selected_pivot"] == "if"

    md_text = written["md"].read_text(encoding="utf-8")
    assert "# RE-275..RE-282 animation-items epic" in md_text
    assert "documentation-only terminal blocker" in md_text
    assert "Recommended next ticket: `TBD`" in md_text

    story_index = written["story_index"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_index
    assert "RE-275..RE-282" in story_index
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
