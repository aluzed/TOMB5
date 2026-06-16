from pathlib import Path
import csv

from scripts.reverse.re291_function_priority_refresh_audit import (
    FORBIDDEN,
    build_audit,
    write_all_artifacts,
)


def test_re291_refresh_audit_regenerates_priority_without_opening_fake_epic():
    repo = Path(__file__).resolve().parents[2]
    audit = build_audit(repo)

    assert audit.story_id == "RE-291"
    assert audit.topic == "function-priority-upstream-refresh-audit"
    assert audit.upstream_handoff == "RE-290"
    assert audit.source_map_rows > audit.regenerated_priority_rows
    assert audit.regenerated_priority_rows == 348
    assert audit.current_priority_rows == 348
    assert audit.priority_delta_rows == 0
    assert audit.priority_changed == "no"
    assert audit.next_ticket == "TBD"
    assert audit.next_topic == "function-priority-inputs-unchanged"
    assert audit.selected_domain == "none"
    assert audit.selected_pivot == "none"
    assert audit.code_change_readiness == "blocked"
    assert audit.stop_condition == "provide changed repo-function-map.csv or new non-raw proof evidence before opening another epic"


def test_re291_refresh_outputs_metadata_only_story_and_handoff(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_audit(repo)
    written = write_all_artifacts(audit, tmp_path)

    assert set(written) == {"audit_csv", "handoff_csv", "md", "story"}

    rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == 1
    assert rows[0]["regenerated_priority_rows"] == "348"
    assert rows[0]["priority_delta_rows"] == "0"
    assert rows[0]["priority_changed"] == "no"

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "TBD"
    assert handoff["selected_domain"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-291 function-priority upstream refresh audit" in md
    assert "Regenerated priority rows: `348`" in md
    assert "Priority delta rows: `0`" in md
    assert "No production source or marker change is authorized" in md

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] Current repo-function-map.csv consumed." in story
    assert "Readiness: `blocked`" in story
    assert "Next topic: `function-priority-inputs-unchanged`" in story

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
