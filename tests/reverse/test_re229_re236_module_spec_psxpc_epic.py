from pathlib import Path
import csv

from scripts.reverse.re229_re236_module_spec_psxpc_epic import (
    FORBIDDEN,
    STALE_FRAGMENTS,
    build_epic,
    write_all_artifacts,
)


def test_re229_re236_opens_and_closes_module_spec_psxpc_epic():
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)

    assert epic.story_range == "RE-229..RE-236"
    assert epic.domain_id == "module-spec_psxpc"
    assert epic.upstream_ticket == "RE-228"
    assert epic.selected_pivot == "PrintString"
    assert epic.candidate_count == 28
    assert epic.closed_candidate_count == 28
    assert epic.runtime_count == 4
    assert epic.nd_count == 0
    assert epic.code_change_ready_count == 0
    assert epic.marker_ready_count == 0
    assert epic.domain_outcome == "documentation-only-terminal-blocker"
    assert epic.blocker == "missing-module-spec-psxpc-source-contract-and-non-raw-equivalence-proof"

    assert [row.story_id for row in epic.story_rows] == [
        "RE-229",
        "RE-230",
        "RE-231",
        "RE-232",
        "RE-233",
        "RE-234",
        "RE-235",
        "RE-236",
    ]
    assert [row.topic for row in epic.story_rows] == [
        "module-spec-psxpc-proof-first-audit",
        "module-spec-psxpc-text-debug-rendering-chain",
        "module-spec-psxpc-render-geometry-support-chain",
        "module-spec-psxpc-frontend-flow-chain",
        "module-spec-psxpc-platform-services-chain",
        "module-spec-psxpc-runtime-cross-platform-reconciliation",
        "module-spec-psxpc-source-patch-gate",
        "post-module-spec-psxpc-domain-selection",
    ]

    subclusters = {row.subcluster: row for row in epic.subcluster_rows}
    assert subclusters["text-debug-rendering"].candidate_count == 2
    assert subclusters["text-debug-rendering"].top_function == "PrintString"
    assert subclusters["render-geometry-support"].candidate_count == 4
    assert subclusters["render-geometry-support"].top_function == "GetBoundsAccurate"
    assert subclusters["frontend-flow"].candidate_count == 9
    assert subclusters["frontend-flow"].top_function == "S_PlayFMV"
    assert subclusters["platform-services"].candidate_count == 13
    assert subclusters["platform-services"].top_function == "CDDA_SetVolume"
    assert all(row.code_change_ready == "no" for row in epic.subcluster_rows)
    assert all(row.marker_ready == "no" for row in epic.subcluster_rows)

    assert epic.handoff.next_ticket == "RE-237"
    assert epic.handoff.next_topic == "module-spec-psx-proof-first-audit"
    assert epic.handoff.selected_domain == "module-spec_psx"
    assert epic.handoff.selected_pivot == "main"


def test_re229_re236_outputs_artifacts_stories_and_metadata_only(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)
    written = write_all_artifacts(epic, tmp_path)

    assert set(written) == {
        "audit_csv",
        "subclusters_csv",
        "epic_csv",
        "gate_csv",
        "next_selection_csv",
        "handoff_csv",
        "md",
        "story_index",
        "stories",
    }
    assert len(written["stories"]) == 8

    audit_rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(audit_rows) == 28
    assert audit_rows[0]["function"] == "PrintString"
    assert {row["domain_id"] for row in audit_rows} == {"module-spec_psxpc"}
    assert {row["readiness"] for row in audit_rows} == {"blocked"}
    assert {row["source_patch_ready"] for row in audit_rows} == {"no"}
    assert sum(1 for row in audit_rows if row["runtime_focus"] == "yes") == 4

    subcluster_rows = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert [row["subcluster"] for row in subcluster_rows] == [
        "text-debug-rendering",
        "render-geometry-support",
        "frontend-flow",
        "platform-services",
    ]
    assert sum(int(row["candidate_count"]) for row in subcluster_rows) == 28

    epic_rows = list(csv.DictReader(written["epic_csv"].open(newline="", encoding="utf-8")))
    assert epic_rows[0]["story_id"] == "RE-229"
    assert epic_rows[-1]["story_id"] == "RE-236"
    assert {row["readiness"] for row in epic_rows} == {"blocked"}

    gates = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert [row["gate"] for row in gates] == ["equivalence", "source-patch", "marker"]
    assert {row["decision"] for row in gates} == {"deny"}

    next_rows = list(csv.DictReader(written["next_selection_csv"].open(newline="", encoding="utf-8")))
    assert next_rows[0]["domain_id"] == "module-spec_psx"
    assert next_rows[0]["next_ticket"] == "RE-237"
    assert next_rows[0]["top_function"] == "main"
    assert "module-spec_psxpc" not in [row["domain_id"] for row in next_rows]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-237"
    assert handoff["next_topic"] == "module-spec-psx-proof-first-audit"
    assert handoff["selected_domain"] == "module-spec_psx"
    assert handoff["selected_pivot"] == "main"

    md_text = written["md"].read_text(encoding="utf-8")
    assert "# RE-229..RE-236 module-spec_psxpc epic" in md_text
    assert "documentation-only terminal blocker" in md_text
    assert "Next proof domain: `module-spec_psx`" in md_text
    assert "Recommended next ticket: `RE-237`" in md_text

    story_index = written["story_index"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_index
    assert "RE-229..RE-236" in story_index
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
