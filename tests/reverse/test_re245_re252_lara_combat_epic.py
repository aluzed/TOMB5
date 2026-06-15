from pathlib import Path
import csv

from scripts.reverse.re245_re252_lara_combat_epic import (
    FORBIDDEN,
    STALE_FRAGMENTS,
    PARSER_ARTIFACTS,
    build_epic,
    write_all_artifacts,
)


def test_re245_re252_opens_and_closes_lara_combat_epic():
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)

    assert epic.story_range == "RE-245..RE-252"
    assert epic.domain_id == "lara-combat"
    assert epic.upstream_ticket == "RE-244"
    assert epic.selected_pivot == "DoProperDetection"
    assert epic.raw_priority_count == 10
    assert epic.parser_artifact_count == 3
    assert epic.candidate_count == 7
    assert epic.closed_candidate_count == 7
    assert epic.runtime_count == 0
    assert epic.nd_count == 0
    assert epic.code_change_ready_count == 0
    assert epic.marker_ready_count == 0
    assert epic.domain_outcome == "documentation-only-terminal-blocker"
    assert epic.blocker == "missing-lara-combat-source-contract-and-non-raw-equivalence-proof"

    assert [row.story_id for row in epic.story_rows] == [
        "RE-245", "RE-246", "RE-247", "RE-248", "RE-249", "RE-250", "RE-251", "RE-252",
    ]
    assert [row.topic for row in epic.story_rows] == [
        "lara-combat-proof-first-audit",
        "lara-combat-target-detection-chain",
        "lara-combat-target-acquisition-chain",
        "lara-combat-weapon-fire-control-chain",
        "lara-combat-parser-artifact-reconciliation",
        "lara-combat-state-equivalence-gate",
        "lara-combat-source-patch-gate",
        "post-lara-combat-domain-selection",
    ]

    subclusters = {row.subcluster: row for row in epic.subcluster_rows}
    assert subclusters["target-detection"].candidate_count == 2
    assert subclusters["target-detection"].top_function == "DoProperDetection"
    assert subclusters["target-acquisition"].candidate_count == 3
    assert subclusters["target-acquisition"].top_function == "LaraGetNewTarget"
    assert subclusters["weapon-fire-control"].candidate_count == 2
    assert subclusters["weapon-fire-control"].top_function == "FireWeapon"
    assert all(row.code_change_ready == "no" for row in epic.subcluster_rows)
    assert all(row.marker_ready == "no" for row in epic.subcluster_rows)

    assert [row.function for row in epic.parser_artifact_rows] == ["if", "if", "if"]
    assert epic.handoff.next_ticket == "RE-253"
    assert epic.handoff.next_topic == "inventory-proof-first-audit"
    assert epic.handoff.selected_domain == "inventory"
    assert epic.handoff.selected_pivot == "S_CallInventory2"


def test_re245_re252_outputs_artifacts_stories_and_metadata_only(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)
    written = write_all_artifacts(epic, tmp_path)

    assert set(written) == {
        "audit_csv", "subclusters_csv", "parser_artifacts_csv", "epic_csv", "gate_csv", "next_selection_csv", "handoff_csv", "md", "story_index", "stories",
    }
    assert len(written["stories"]) == 8

    audit_rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(audit_rows) == 7
    assert audit_rows[0]["function"] == "DoProperDetection"
    assert {row["domain_id"] for row in audit_rows} == {"lara-combat"}
    assert {row["readiness"] for row in audit_rows} == {"blocked"}
    assert {row["source_patch_ready"] for row in audit_rows} == {"no"}
    assert not any(row["function"] in PARSER_ARTIFACTS for row in audit_rows)

    parser_rows = list(csv.DictReader(written["parser_artifacts_csv"].open(newline="", encoding="utf-8")))
    assert len(parser_rows) == 3
    assert {row["function"] for row in parser_rows} == {"if"}
    assert {row["action"] for row in parser_rows} == {"excluded-from-function-scope"}

    subcluster_rows = list(csv.DictReader(written["subclusters_csv"].open(newline="", encoding="utf-8")))
    assert [row["subcluster"] for row in subcluster_rows] == [
        "target-detection", "target-acquisition", "weapon-fire-control",
    ]
    assert sum(int(row["candidate_count"]) for row in subcluster_rows) == 7

    epic_rows = list(csv.DictReader(written["epic_csv"].open(newline="", encoding="utf-8")))
    assert epic_rows[0]["story_id"] == "RE-245"
    assert epic_rows[-1]["story_id"] == "RE-252"
    assert {row["readiness"] for row in epic_rows} == {"blocked"}

    gates = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert [row["gate"] for row in gates] == ["equivalence", "source-patch", "marker"]
    assert {row["decision"] for row in gates} == {"deny"}

    next_rows = list(csv.DictReader(written["next_selection_csv"].open(newline="", encoding="utf-8")))
    assert next_rows[0]["domain_id"] == "inventory"
    assert next_rows[0]["next_ticket"] == "RE-253"
    assert next_rows[0]["top_function"] == "S_CallInventory2"
    assert "lara-combat" not in [row["domain_id"] for row in next_rows]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-253"
    assert handoff["next_topic"] == "inventory-proof-first-audit"
    assert handoff["selected_domain"] == "inventory"
    assert handoff["selected_pivot"] == "S_CallInventory2"

    md_text = written["md"].read_text(encoding="utf-8")
    assert "# RE-245..RE-252 lara-combat epic" in md_text
    assert "documentation-only terminal blocker" in md_text
    assert "Parser artifacts excluded: `3`" in md_text
    assert "Next proof domain: `inventory`" in md_text
    assert "Recommended next ticket: `RE-253`" in md_text

    story_index = written["story_index"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_index
    assert "RE-245..RE-252" in story_index
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
