from pathlib import Path
import csv

from scripts.reverse.re222_re228_traps_switches_doors_epic import (
    FORBIDDEN,
    STALE_FRAGMENTS,
    build_epic,
    write_all_artifacts,
)


def test_re222_re228_opens_and_closes_traps_switches_doors_epic():
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)

    assert epic.story_range == "RE-222..RE-228"
    assert epic.domain_id == "traps-switches-doors"
    assert epic.upstream_ticket == "RE-221"
    assert epic.selected_pivot == "ControlRollingBall"
    assert epic.candidate_count == 20
    assert epic.closed_candidate_count == 20
    assert epic.code_change_ready_count == 0
    assert epic.marker_ready_count == 0
    assert epic.domain_outcome == "documentation-only-terminal-blocker"
    assert epic.blocker == "missing-traps-switches-doors-source-contract-and-non-raw-equivalence-proof"

    assert [row.story_id for row in epic.story_rows] == [
        "RE-222",
        "RE-223",
        "RE-224",
        "RE-225",
        "RE-226",
        "RE-227",
        "RE-228",
    ]
    assert [row.topic for row in epic.story_rows] == [
        "traps-switches-doors-proof-first-audit",
        "traps-switches-doors-trap-hazard-chain",
        "traps-switches-doors-door-control-chain",
        "traps-switches-doors-switch-control-chain",
        "traps-switches-doors-trigger-state-reconciliation",
        "traps-switches-doors-source-patch-gate",
        "post-traps-switches-doors-domain-selection",
    ]

    subclusters = {row.subcluster: row for row in epic.subcluster_rows}
    assert subclusters["trap-hazard-control"].candidate_count == 11
    assert subclusters["trap-hazard-control"].top_function == "ControlRollingBall"
    assert subclusters["door-control"].candidate_count == 4
    assert subclusters["door-control"].top_function == "DoorControl"
    assert subclusters["switch-control"].candidate_count == 5
    assert subclusters["switch-control"].top_function == "TurnSwitchControl"
    assert all(row.code_change_ready == "no" for row in epic.subcluster_rows)
    assert all(row.marker_ready == "no" for row in epic.subcluster_rows)

    assert epic.handoff.next_ticket == "RE-229"
    assert epic.handoff.next_topic == "module-spec-psxpc-proof-first-audit"
    assert epic.handoff.selected_domain == "module-spec_psxpc"
    assert epic.handoff.selected_pivot == "PrintString"


def test_re222_re228_outputs_artifacts_stories_and_metadata_only(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)
    written = write_all_artifacts(epic, tmp_path)

    expected_keys = {
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
    assert set(written) == expected_keys
    assert len(written["stories"]) == 7

    audit_rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(audit_rows) == 20
    assert audit_rows[0]["function"] == "ControlRollingBall"
    assert {row["domain_id"] for row in audit_rows} == {"traps-switches-doors"}
    assert {row["readiness"] for row in audit_rows} == {"blocked"}
    assert {row["source_patch_ready"] for row in audit_rows} == {"no"}

    subcluster_rows = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert [row["subcluster"] for row in subcluster_rows] == [
        "trap-hazard-control",
        "door-control",
        "switch-control",
    ]
    assert sum(int(row["candidate_count"]) for row in subcluster_rows) == 20

    epic_rows = list(csv.DictReader(written["epic_csv"].open(newline="", encoding="utf-8")))
    assert epic_rows[0]["story_id"] == "RE-222"
    assert epic_rows[-1]["story_id"] == "RE-228"
    assert {row["readiness"] for row in epic_rows} == {"blocked"}

    gates = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert [row["gate"] for row in gates] == ["equivalence", "source-patch", "marker"]
    assert {row["decision"] for row in gates} == {"deny"}

    next_rows = list(csv.DictReader(written["next_selection_csv"].open(newline="", encoding="utf-8")))
    assert next_rows[0]["domain_id"] == "module-spec_psxpc"
    assert next_rows[0]["next_ticket"] == "RE-229"
    assert next_rows[0]["top_function"] == "PrintString"
    assert "traps-switches-doors" not in [row["domain_id"] for row in next_rows]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-229"
    assert handoff["next_topic"] == "module-spec-psxpc-proof-first-audit"
    assert handoff["selected_domain"] == "module-spec_psxpc"
    assert handoff["selected_pivot"] == "PrintString"

    md_text = written["md"].read_text(encoding="utf-8")
    assert "# RE-222..RE-228 traps-switches-doors epic" in md_text
    assert "documentation-only terminal blocker" in md_text
    assert "Next proof domain: `module-spec_psxpc`" in md_text
    assert "Recommended next ticket: `RE-229`" in md_text

    story_index = written["story_index"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_index
    assert "RE-222..RE-228" in story_index
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
