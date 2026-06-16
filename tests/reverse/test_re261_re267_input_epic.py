from pathlib import Path
import csv

from scripts.reverse.re261_re267_input_epic import (
    FORBIDDEN,
    STALE_FRAGMENTS,
    build_epic,
    write_all_artifacts,
)


def test_re261_re267_opens_and_closes_input_epic():
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)

    assert epic.story_range == "RE-261..RE-267"
    assert epic.domain_id == "input"
    assert epic.upstream_ticket == "RE-260"
    assert epic.selected_pivot == "S_UpdateInput"
    assert epic.raw_priority_count == 3
    assert epic.parser_artifact_count == 0
    assert epic.candidate_count == 3
    assert epic.closed_candidate_count == 3
    assert epic.runtime_count == 2
    assert epic.nd_count == 0
    assert epic.code_change_ready_count == 0
    assert epic.marker_ready_count == 0
    assert epic.domain_outcome == "documentation-only-terminal-blocker"
    assert epic.blocker == "missing-input-cross-platform-state-contract-and-non-raw-equivalence-proof"

    assert [row.story_id for row in epic.story_rows] == [
        "RE-261", "RE-262", "RE-263", "RE-264", "RE-265", "RE-266", "RE-267",
    ]
    assert [row.topic for row in epic.story_rows] == [
        "input-proof-first-audit",
        "input-psxpc-n-runtime-chain",
        "input-psx-runtime-chain",
        "input-psxpc-service-chain",
        "input-state-equivalence-gate",
        "input-source-patch-gate",
        "post-input-domain-selection",
    ]

    subclusters = {row.subcluster: row for row in epic.subcluster_rows}
    assert subclusters["psxpc-n-runtime"].candidate_count == 1
    assert subclusters["psxpc-n-runtime"].top_function == "S_UpdateInput"
    assert subclusters["psx-runtime"].candidate_count == 1
    assert subclusters["psx-runtime"].top_function == "S_UpdateInput"
    assert subclusters["psxpc-service"].candidate_count == 1
    assert subclusters["psxpc-service"].top_function == "S_UpdateInput"
    assert all(row.code_change_ready == "no" for row in epic.subcluster_rows)
    assert all(row.marker_ready == "no" for row in epic.subcluster_rows)

    assert epic.handoff.next_ticket == "RE-268"
    assert epic.handoff.next_topic == "camera-proof-first-audit"
    assert epic.handoff.selected_domain == "camera"
    assert epic.handoff.selected_pivot == "CalculateSpotCams"


def test_re261_re267_outputs_artifacts_stories_and_metadata_only(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)
    written = write_all_artifacts(epic, tmp_path)

    assert set(written) == {
        "audit_csv", "subclusters_csv", "epic_csv", "gate_csv", "next_selection_csv", "handoff_csv", "md", "story_index", "stories",
    }
    assert len(written["stories"]) == 7

    audit_rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(audit_rows) == 3
    assert [row["file"] for row in audit_rows] == [
        "SPEC_PSXPC_N/PSXINPUT.C",
        "SPEC_PSX/PSXINPUT.C",
        "SPEC_PSXPC/PSXPCINPUT.C",
    ]
    assert {row["domain_id"] for row in audit_rows} == {"input"}
    assert {row["readiness"] for row in audit_rows} == {"blocked"}
    assert {row["source_patch_ready"] for row in audit_rows} == {"no"}

    subcluster_rows = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert [row["subcluster"] for row in subcluster_rows] == [
        "psxpc-n-runtime", "psx-runtime", "psxpc-service",
    ]
    assert sum(int(row["candidate_count"]) for row in subcluster_rows) == 3

    epic_rows = list(csv.DictReader(written["epic_csv"].open(newline="", encoding="utf-8")))
    assert epic_rows[0]["story_id"] == "RE-261"
    assert epic_rows[-1]["story_id"] == "RE-267"
    assert {row["readiness"] for row in epic_rows} == {"blocked"}

    gates = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert [row["gate"] for row in gates] == ["equivalence", "source-patch", "marker"]
    assert {row["decision"] for row in gates} == {"deny"}

    next_rows = list(csv.DictReader(written["next_selection_csv"].open(newline="", encoding="utf-8")))
    assert next_rows[0]["domain_id"] == "camera"
    assert next_rows[0]["next_ticket"] == "RE-268"
    assert next_rows[0]["top_function"] == "CalculateSpotCams"
    assert "input" not in [row["domain_id"] for row in next_rows]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-268"
    assert handoff["next_topic"] == "camera-proof-first-audit"
    assert handoff["selected_domain"] == "camera"
    assert handoff["selected_pivot"] == "CalculateSpotCams"

    md_text = written["md"].read_text(encoding="utf-8")
    assert "# RE-261..RE-267 input epic" in md_text
    assert "documentation-only terminal blocker" in md_text
    assert "Runtime rows: `2`" in md_text
    assert "Next proof domain: `camera`" in md_text
    assert "Recommended next ticket: `RE-268`" in md_text

    story_index = written["story_index"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_index
    assert "RE-261..RE-267" in story_index
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
