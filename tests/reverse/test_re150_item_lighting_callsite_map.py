from pathlib import Path
import csv

from scripts.reverse.re150_item_lighting_callsite_map import (
    C_KEYWORD_ARTIFACTS,
    build_item_lighting_callsite_map,
    write_all_artifacts,
)


def test_re150_consumes_re149_plan_and_maps_item_lighting_callsites():
    repo = Path(__file__).resolve().parents[2]
    audit = build_item_lighting_callsite_map(repo)

    assert audit.story_id == "RE-150"
    assert audit.upstream_ticket == "RE-149"
    assert audit.cluster == "item-lighting-interaction"
    assert audit.next_ticket == "RE-151"
    assert audit.code_change_ready_count == 0
    assert audit.marker_ready_count == 0
    assert [row.function for row in audit.scope_rows] == ["DoFlameTorch", "TriggerAlertLight"]
    assert {row.callee for row in audit.callsite_rows} == {"DoFlameTorch", "TriggerAlertLight"}
    assert any(row.caller == "LaraGun" and row.callee == "DoFlameTorch" for row in audit.callsite_rows)
    assert any(row.caller == "ControlStrobeLight" and row.callee == "TriggerAlertLight" for row in audit.callsite_rows)
    assert not any(row.caller == "item-lighting-dispatch-table" for row in audit.callsite_rows)
    assert all(row.line > 0 for row in audit.callsite_rows)
    assert all((repo / row.caller_file).read_text(encoding="utf-8", errors="ignore").splitlines()[row.line - 1].find(row.callee) >= 0 for row in audit.callsite_rows)
    assert all(row.caller not in C_KEYWORD_ARTIFACTS for row in audit.callsite_rows)
    assert all(row.callee not in C_KEYWORD_ARTIFACTS for row in audit.callsite_rows)
    assert all(row.patch_ready == "no" for row in audit.callsite_rows)


def test_re150_outputs_metadata_only_artifacts_and_progress_tracker(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_item_lighting_callsite_map(repo)
    written = write_all_artifacts(audit, tmp_path)

    scope_rows = list(csv.DictReader(written["scope_csv"].open(newline="", encoding="utf-8")))
    assert [row["function"] for row in scope_rows] == ["DoFlameTorch", "TriggerAlertLight"]
    assert all(row["patch_ready"] == "no" for row in scope_rows)
    assert all("item-lighting" in row["blocker"] for row in scope_rows)

    callsites = list(csv.DictReader(written["callsite_csv"].open(newline="", encoding="utf-8")))
    assert callsites
    assert all(row["caller"] not in C_KEYWORD_ARTIFACTS for row in callsites)
    assert all(row["callee"] not in C_KEYWORD_ARTIFACTS for row in callsites)
    assert any(row["caller"] == "LaraGun" and row["callee"] == "DoFlameTorch" and row["caller_file"] == "GAME/LARAFIRE.C" for row in callsites)
    assert any(row["caller"] == "ControlStrobeLight" and row["callee"] == "TriggerAlertLight" and row["caller_file"] == "GAME/OBJLIGHT.C" for row in callsites)
    assert not any(row["callee"] == "DoFlameTorch" and row["line"] == "54" for row in callsites)
    assert not any(row["callee"] == "TriggerAlertLight" and row["line"] == "17" for row in callsites)

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-149 ticket plan consumed" in story_text
    assert "Item-lighting callsites mapped" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "RE-151" in story_text
    assert "test_re150_item_lighting_callsite_map.py" in story_text
    assert "object-interaction" not in story_text.lower()
    assert "gameplay-mixed" not in story_text.lower()
    assert "test_re142" not in story_text.lower()

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "raw call target" not in text
        assert "machine word" not in text
        assert "0x" not in text
