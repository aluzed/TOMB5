from pathlib import Path
import csv

from scripts.reverse.re268_re274_camera_epic import (
    FORBIDDEN,
    STALE_FRAGMENTS,
    build_epic,
    write_all_artifacts,
)


def test_re268_re274_opens_and_closes_camera_epic():
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)

    assert epic.story_range == "RE-268..RE-274"
    assert epic.domain_id == "camera"
    assert epic.upstream_ticket == "RE-267"
    assert epic.selected_pivot == "CalculateSpotCams"
    assert epic.raw_priority_count == 4
    assert epic.parser_artifact_count == 0
    assert epic.candidate_count == 4
    assert epic.closed_candidate_count == 4
    assert epic.runtime_count == 0
    assert epic.nd_count == 0
    assert epic.code_change_ready_count == 0
    assert epic.marker_ready_count == 0
    assert epic.domain_outcome == "documentation-only-terminal-blocker"
    assert epic.blocker == "missing-camera-state-contract-and-non-raw-equivalence-proof"

    assert [row.story_id for row in epic.story_rows] == [
        "RE-268", "RE-269", "RE-270", "RE-271", "RE-272", "RE-273", "RE-274",
    ]
    assert [row.topic for row in epic.story_rows] == [
        "camera-proof-first-audit",
        "camera-spotcam-chain",
        "camera-core-chain",
        "camera-line-of-sight-chain",
        "camera-state-equivalence-gate",
        "camera-source-patch-gate",
        "post-camera-domain-exhaustion",
    ]

    subclusters = {row.subcluster: row for row in epic.subcluster_rows}
    assert subclusters["spotcam"].candidate_count == 1
    assert subclusters["spotcam"].top_function == "CalculateSpotCams"
    assert subclusters["camera-core"].candidate_count == 2
    assert subclusters["camera-core"].top_function == "CalculateCamera"
    assert subclusters["line-of-sight"].candidate_count == 1
    assert subclusters["line-of-sight"].top_function == "mgLOS"
    assert all(row.code_change_ready == "no" for row in epic.subcluster_rows)
    assert all(row.marker_ready == "no" for row in epic.subcluster_rows)

    assert epic.handoff.next_ticket == "TBD"
    assert epic.handoff.next_topic == "post-re267-domain-backlog-exhausted"
    assert epic.handoff.selected_domain == "none"
    assert epic.handoff.selected_pivot == "none"


def test_re268_re274_outputs_artifacts_stories_and_metadata_only(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)
    written = write_all_artifacts(epic, tmp_path)

    assert set(written) == {
        "audit_csv", "subclusters_csv", "epic_csv", "gate_csv", "exhaustion_csv", "handoff_csv", "md", "story_index", "stories",
    }
    assert len(written["stories"]) == 7

    audit_rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(audit_rows) == 4
    assert [row["function"] for row in audit_rows] == [
        "CalculateSpotCams", "CalculateCamera", "CombatCamera", "mgLOS",
    ]
    assert {row["domain_id"] for row in audit_rows} == {"camera"}
    assert {row["readiness"] for row in audit_rows} == {"blocked"}
    assert {row["source_patch_ready"] for row in audit_rows} == {"no"}

    subcluster_rows = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert [row["subcluster"] for row in subcluster_rows] == ["spotcam", "camera-core", "line-of-sight"]
    assert sum(int(row["candidate_count"]) for row in subcluster_rows) == 4

    epic_rows = list(csv.DictReader(written["epic_csv"].open(newline="", encoding="utf-8")))
    assert epic_rows[0]["story_id"] == "RE-268"
    assert epic_rows[-1]["story_id"] == "RE-274"
    assert {row["readiness"] for row in epic_rows} == {"blocked"}

    gates = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert [row["gate"] for row in gates] == ["equivalence", "source-patch", "marker"]
    assert {row["decision"] for row in gates} == {"deny"}

    exhaustion = list(csv.DictReader(written["exhaustion_csv"].open(newline="", encoding="utf-8")))[0]
    assert exhaustion["next_ticket"] == "TBD"
    assert exhaustion["remaining_domain_count"] == "0"
    assert exhaustion["status"] == "exhausted"

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "TBD"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"

    md_text = written["md"].read_text(encoding="utf-8")
    assert "# RE-268..RE-274 camera epic" in md_text
    assert "documentation-only terminal blocker" in md_text
    assert "Remaining domains: `0`" in md_text
    assert "Recommended next ticket: `TBD`" in md_text

    story_index = written["story_index"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_index
    assert "RE-268..RE-274" in story_index
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
