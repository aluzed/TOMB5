from pathlib import Path
import csv

from scripts.reverse.re288_re290_global_exhaustion_epic import (
    FORBIDDEN,
    STALE_FRAGMENTS,
    build_epic,
    write_all_artifacts,
)


def test_re288_re290_proves_function_priority_backlog_exhausted():
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)

    assert epic.story_range == "RE-288..RE-290"
    assert epic.upstream_ticket == "RE-287"
    assert epic.total_priority_rows == 348
    assert epic.closed_domain_count == 15
    assert epic.remaining_domain_count == 0
    assert epic.remaining_candidate_count == 0
    assert epic.parser_artifact_count == 16
    assert epic.code_change_ready_count == 0
    assert epic.marker_ready_count == 0
    assert epic.outcome == "function-priority-backlog-exhausted"

    assert [row.domain_id for row in epic.domain_rows] == [
        "maths-render-support",
        "module-game",
        "collision",
        "animation-items",
        "module-spec_psxpc",
        "module-spec_psxpc_n",
        "traps-switches-doors",
        "audio-effects",
        "module-spec_psx",
        "inventory",
        "lara-combat",
        "camera",
        "savegame",
        "input",
        "module-spec_pc_n",
    ]
    assert {row.domain_id: row.priority_count for row in epic.domain_rows} == {
        "maths-render-support": 92,
        "module-game": 54,
        "collision": 32,
        "animation-items": 31,
        "module-spec_psxpc": 28,
        "module-spec_psxpc_n": 27,
        "traps-switches-doors": 20,
        "audio-effects": 19,
        "module-spec_psx": 12,
        "inventory": 11,
        "lara-combat": 10,
        "camera": 4,
        "savegame": 3,
        "input": 3,
        "module-spec_pc_n": 2,
    }
    assert {row.domain_id: row.parser_artifact_count for row in epic.domain_rows} == {
        "maths-render-support": 0,
        "module-game": 2,
        "collision": 1,
        "animation-items": 0,
        "module-spec_psxpc": 0,
        "module-spec_psxpc_n": 3,
        "traps-switches-doors": 0,
        "audio-effects": 0,
        "module-spec_psx": 0,
        "inventory": 6,
        "lara-combat": 3,
        "camera": 0,
        "savegame": 0,
        "input": 0,
        "module-spec_pc_n": 1,
    }
    assert sum(row.priority_count for row in epic.domain_rows) == 348
    assert {row.status for row in epic.domain_rows} == {"closed-or-proof-blocked"}

    assert [row.story_id for row in epic.story_rows] == ["RE-288", "RE-289", "RE-290"]
    assert [row.topic for row in epic.story_rows] == [
        "global-function-priority-exhaustion-audit",
        "global-parser-artifact-reconciliation",
        "final-function-priority-handoff",
    ]

    assert epic.handoff.next_ticket == "TBD"
    assert epic.handoff.next_topic == "function-priority-backlog-exhausted"
    assert epic.handoff.selected_domain == "none"
    assert epic.handoff.selected_pivot == "none"


def test_re288_re290_outputs_artifacts_stories_and_metadata_only(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)
    written = write_all_artifacts(epic, tmp_path)

    assert set(written) == {"domains_csv", "parser_csv", "epic_csv", "handoff_csv", "md", "story_index", "stories"}
    assert len(written["stories"]) == 3

    domain_rows = list(csv.DictReader(written["domains_csv"].open(newline="", encoding="utf-8")))
    assert len(domain_rows) == 15
    assert domain_rows[0]["domain_id"] == "maths-render-support"
    assert domain_rows[-1]["domain_id"] == "module-spec_pc_n"
    assert sum(int(row["priority_count"]) for row in domain_rows) == 348
    assert {row["remaining_candidates"] for row in domain_rows} == {"0"}
    assert {row["domain_id"]: int(row["parser_artifact_count"]) for row in domain_rows} == {
        row.domain_id: row.parser_artifact_count for row in epic.domain_rows
    }

    parser_rows = list(csv.DictReader(written["parser_csv"].open(newline="", encoding="utf-8")))
    assert len(parser_rows) == 16
    assert {row["classification"] for row in parser_rows} == {"parser-artifact"}

    epic_rows = list(csv.DictReader(written["epic_csv"].open(newline="", encoding="utf-8")))
    assert epic_rows[0]["story_id"] == "RE-288"
    assert epic_rows[-1]["story_id"] == "RE-290"
    assert {row["readiness"] for row in epic_rows} == {"blocked"}

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "TBD"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"

    md_text = written["md"].read_text(encoding="utf-8")
    assert "# RE-288..RE-290 global function-priority exhaustion epic" in md_text
    assert "Total priority rows: `348`" in md_text
    assert "Remaining candidate rows: `0`" in md_text
    assert "Recommended next ticket: `TBD`" in md_text

    story_index = written["story_index"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_index
    assert "RE-288..RE-290" in story_index
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
