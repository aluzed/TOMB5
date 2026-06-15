from pathlib import Path
import csv

from scripts.reverse.re164_ui_text_rendering_callsite_map import (
    C_KEYWORD_ARTIFACTS,
    build_ui_text_rendering_callsite_map,
    write_all_artifacts,
)


def test_re164_consumes_re163_plan_and_maps_source_backed_callsites():
    repo = Path(__file__).resolve().parents[2]
    audit = build_ui_text_rendering_callsite_map(repo)

    assert audit.story_id == "RE-164"
    assert audit.upstream_ticket == "RE-163"
    assert audit.cluster == "ui-text-rendering"
    assert audit.next_ticket == "RE-165"
    assert audit.code_change_ready_count == 0
    assert audit.marker_ready_count == 0
    assert [row.function for row in audit.scope_rows] == ["PrintString", "GetStringLength"]
    assert {row.callee for row in audit.callsite_rows} == {"PrintString", "GetStringLength"}
    assert len([row for row in audit.callsite_rows if row.callee == "PrintString"]) >= 70
    assert len([row for row in audit.callsite_rows if row.callee == "GetStringLength"]) == 6
    assert any(row.caller == "DisplayFiles" and row.callee == "PrintString" and row.caller_file == "SPEC_PSXPC_N/LOADSAVE.C" for row in audit.callsite_rows)
    assert any(row.caller == "Requester" and row.callee == "PrintString" and row.caller_file == "SPEC_PSXPC_N/REQUEST.C" for row in audit.callsite_rows)
    assert any(row.caller == "PrintString" and row.callee == "GetStringLength" and row.caller_file == "SPEC_PSXPC_N/TEXT_S.C" for row in audit.callsite_rows)
    assert any(row.caller == "GetStringDimensions" and row.callee == "GetStringLength" and row.caller_file == "SPEC_PSXPC_N/TEXT_S.C" for row in audit.callsite_rows)
    assert not any(row.caller.endswith("dispatch-table") for row in audit.callsite_rows)
    assert all(row.line > 0 for row in audit.callsite_rows)
    assert all((repo / row.caller_file).read_text(encoding="utf-8", errors="ignore").splitlines()[row.line - 1].find(row.callee) >= 0 for row in audit.callsite_rows)
    assert all(row.caller not in C_KEYWORD_ARTIFACTS for row in audit.callsite_rows)
    assert all(row.callee not in C_KEYWORD_ARTIFACTS for row in audit.callsite_rows)
    assert all(row.patch_ready == "no" for row in audit.callsite_rows)

    by_location = {(row.caller_file, row.line): row for row in audit.callsite_rows}
    assert by_location[("SPEC_PSXPC_N/SPECIFIC.C", 203)].flag_source == "blink-or-composite-flags"
    assert by_location[("SPEC_PSXPC_N/SPECIFIC.C", 665)].flag_source == "blink-or-composite-flags"
    assert by_location[("SPEC_PSXPC_N/TITSEQ.C", 205)].flag_source == "blink-or-composite-flags"
    assert by_location[("SPEC_PSXPC_N/LOADSAVE.C", 419)].coordinate_source == "literal-or-expression-coordinate"
    assert by_location[("SPEC_PSXPC_N/LOADSAVE.C", 686)].coordinate_source == "literal-or-expression-coordinate"
    assert by_location[("SPEC_PSXPC_N/LOADSAVE.C", 419)].flag_source == "center-alignment-flags"
    assert by_location[("SPEC_PSXPC_N/LOADSAVE.C", 686)].flag_source == "center-alignment-flags"


def test_re164_outputs_metadata_only_artifacts_and_progress_tracker(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_ui_text_rendering_callsite_map(repo)
    written = write_all_artifacts(audit, tmp_path)

    scope_rows = list(csv.DictReader(written["scope_csv"].open(newline="", encoding="utf-8")))
    assert [row["function"] for row in scope_rows] == ["PrintString", "GetStringLength"]
    assert all(row["patch_ready"] == "no" for row in scope_rows)
    assert all("ui-text-rendering" in row["blocker"] for row in scope_rows)

    callsites = list(csv.DictReader(written["callsite_csv"].open(newline="", encoding="utf-8")))
    assert callsites
    assert all(row["caller"] not in C_KEYWORD_ARTIFACTS for row in callsites)
    assert all(row["callee"] not in C_KEYWORD_ARTIFACTS for row in callsites)
    assert any(row["caller"] == "DisplayFiles" and row["callee"] == "PrintString" for row in callsites)
    assert any(row["caller"] == "PrintString" and row["callee"] == "GetStringLength" for row in callsites)
    assert not any(row["caller"].endswith("dispatch-table") for row in callsites)
    assert not any(row["callee"] == "PrintString" and row["line"] == "196" for row in callsites)
    assert not any(row["callee"] == "GetStringLength" and row["line"] == "401" for row in callsites)

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-163 ticket plan consumed" in story_text
    assert "UI text rendering callsites mapped" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "RE-165" in story_text
    assert "test_re164_ui_text_rendering_callsite_map.py" in story_text
    assert "item-lighting" not in story_text.lower()
    assert "object-interaction" not in story_text.lower()
    assert "test_re150" not in story_text.lower()

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "raw call target" not in text
        assert "machine word" not in text
        assert "0x" not in text
