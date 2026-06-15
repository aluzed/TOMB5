from pathlib import Path
import csv

from scripts.reverse.re237_re244_module_spec_psx_epic import (
    FORBIDDEN,
    STALE_FRAGMENTS,
    build_epic,
    write_all_artifacts,
)


def test_re237_re244_opens_and_closes_module_spec_psx_epic():
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)

    assert epic.story_range == "RE-237..RE-244"
    assert epic.domain_id == "module-spec_psx"
    assert epic.upstream_ticket == "RE-236"
    assert epic.selected_pivot == "main"
    assert epic.candidate_count == 12
    assert epic.closed_candidate_count == 12
    assert epic.runtime_count == 4
    assert epic.nd_count == 7
    assert epic.code_change_ready_count == 0
    assert epic.marker_ready_count == 0
    assert epic.domain_outcome == "documentation-only-terminal-blocker"
    assert epic.blocker == "missing-module-spec-psx-source-contract-and-non-raw-equivalence-proof"

    assert [row.story_id for row in epic.story_rows] == [
        "RE-237", "RE-238", "RE-239", "RE-240", "RE-241", "RE-242", "RE-243", "RE-244",
    ]
    assert [row.topic for row in epic.story_rows] == [
        "module-spec-psx-proof-first-audit",
        "module-spec-psx-platform-main-lifecycle-chain",
        "module-spec-psx-frontend-loadsave-flow-chain",
        "module-spec-psx-platform-memory-chain",
        "module-spec-psx-nd-stub-reconciliation",
        "module-spec-psx-runtime-cross-platform-reconciliation",
        "module-spec-psx-source-patch-gate",
        "post-module-spec-psx-domain-selection",
    ]

    subclusters = {row.subcluster: row for row in epic.subcluster_rows}
    assert subclusters["platform-main-lifecycle"].candidate_count == 3
    assert subclusters["platform-main-lifecycle"].top_function == "main"
    assert subclusters["frontend-loadsave-flow"].candidate_count == 5
    assert subclusters["frontend-loadsave-flow"].top_function == "S_PlayFMV"
    assert subclusters["platform-memory"].candidate_count == 4
    assert subclusters["platform-memory"].top_function == "game_malloc"
    assert all(row.code_change_ready == "no" for row in epic.subcluster_rows)
    assert all(row.marker_ready == "no" for row in epic.subcluster_rows)

    assert epic.handoff.next_ticket == "RE-245"
    assert epic.handoff.next_topic == "lara-combat-proof-first-audit"
    assert epic.handoff.selected_domain == "lara-combat"
    assert epic.handoff.selected_pivot == "DoProperDetection"


def test_re237_re244_outputs_artifacts_stories_and_metadata_only(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)
    written = write_all_artifacts(epic, tmp_path)

    assert set(written) == {
        "audit_csv", "subclusters_csv", "epic_csv", "gate_csv", "next_selection_csv", "handoff_csv", "md", "story_index", "stories",
    }
    assert len(written["stories"]) == 8

    audit_rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(audit_rows) == 12
    assert audit_rows[0]["function"] == "main"
    assert {row["domain_id"] for row in audit_rows} == {"module-spec_psx"}
    assert {row["readiness"] for row in audit_rows} == {"blocked"}
    assert {row["source_patch_ready"] for row in audit_rows} == {"no"}
    assert sum(1 for row in audit_rows if row["runtime_focus"] == "yes") == 4
    assert sum(1 for row in audit_rows if row["nd"] == "yes") == 7

    subcluster_rows = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert [row["subcluster"] for row in subcluster_rows] == [
        "platform-main-lifecycle", "frontend-loadsave-flow", "platform-memory",
    ]
    assert sum(int(row["candidate_count"]) for row in subcluster_rows) == 12

    epic_rows = list(csv.DictReader(written["epic_csv"].open(newline="", encoding="utf-8")))
    assert epic_rows[0]["story_id"] == "RE-237"
    assert epic_rows[-1]["story_id"] == "RE-244"
    assert {row["readiness"] for row in epic_rows} == {"blocked"}

    gates = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert [row["gate"] for row in gates] == ["equivalence", "source-patch", "marker"]
    assert {row["decision"] for row in gates} == {"deny"}

    next_rows = list(csv.DictReader(written["next_selection_csv"].open(newline="", encoding="utf-8")))
    assert next_rows[0]["domain_id"] == "lara-combat"
    assert next_rows[0]["next_ticket"] == "RE-245"
    assert next_rows[0]["top_function"] == "DoProperDetection"
    assert "module-spec_psx" not in [row["domain_id"] for row in next_rows]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-245"
    assert handoff["next_topic"] == "lara-combat-proof-first-audit"
    assert handoff["selected_domain"] == "lara-combat"
    assert handoff["selected_pivot"] == "DoProperDetection"

    md_text = written["md"].read_text(encoding="utf-8")
    assert "# RE-237..RE-244 module-spec_psx epic" in md_text
    assert "documentation-only terminal blocker" in md_text
    assert "Next proof domain: `lara-combat`" in md_text
    assert "Recommended next ticket: `RE-245`" in md_text

    story_index = written["story_index"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_index
    assert "RE-237..RE-244" in story_index
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
