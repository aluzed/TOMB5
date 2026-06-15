from pathlib import Path
import csv

from scripts.reverse.re165_ui_text_rendering_argument_taxonomy import (
    build_ui_text_rendering_argument_taxonomy,
    write_all_artifacts,
)


def test_re165_consumes_re164_callsite_map_and_groups_argument_families():
    repo = Path(__file__).resolve().parents[2]
    audit = build_ui_text_rendering_argument_taxonomy(repo)

    assert audit.story_id == "RE-165"
    assert audit.upstream_ticket == "RE-164"
    assert audit.cluster == "ui-text-rendering"
    assert audit.next_ticket == "RE-166"
    assert audit.code_change_ready_count == 0
    assert audit.marker_ready_count == 0
    assert audit.source_callsite_count == 88
    assert len(audit.taxonomy_rows) == 20
    assert {row.callee for row in audit.taxonomy_rows} == {"PrintString", "GetStringLength"}
    assert all(row.source_backing == "source-callsite-only" for row in audit.taxonomy_rows)
    assert all(row.patch_ready == "no" for row in audit.taxonomy_rows)
    assert all(row.blocker == "missing-ui-text-rendering-state-contract-and-symbolic-equivalence-proof" for row in audit.taxonomy_rows)

    by_family = {row.family_id: row for row in audit.taxonomy_rows}
    centered = by_family["ui-text-printstring-screen-centered-literal-colour-string-wad-center"]
    assert centered.callee == "PrintString"
    assert centered.callsite_count == 36
    assert centered.coordinate_family == "screen-centered-or-absolute"
    assert centered.text_family == "string-wad-offset"
    assert centered.flag_family == "center-alignment-flags"

    blink = by_family["ui-text-printstring-screen-centered-literal-colour-string-wad-blink-composite"]
    assert blink.callsite_count == 2
    assert blink.flag_family == "blink-or-composite-flags"

    bounds = by_family["ui-text-getstringlength-caller-string-with-bounds"]
    assert bounds.callee == "GetStringLength"
    assert bounds.callsite_count == 4
    assert bounds.argument_shape == "shape-ui-text-length-with-bounds"
    assert bounds.text_family == "caller-string-or-string-wad"
    assert bounds.state_fields == "scale-flag-state;font-definition-table;accent-table"

    optional = by_family["ui-text-getstringlength-string-wad-optional-bound"]
    assert optional.callsite_count == 1
    assert optional.argument_shape == "shape-ui-text-length-with-optional-bound"


def test_re165_outputs_metadata_only_artifacts_and_story_tracker(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_ui_text_rendering_argument_taxonomy(repo)
    written = write_all_artifacts(audit, tmp_path)

    rows = list(csv.DictReader(written["taxonomy_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == 20
    assert all(row["patch_ready"] == "no" for row in rows)
    assert all(row["source_backing"] == "source-callsite-only" for row in rows)
    assert any(row["family_id"] == "ui-text-printstring-screen-centered-literal-colour-string-wad-center" and row["callsite_count"] == "36" for row in rows)
    assert any(row["family_id"] == "ui-text-getstringlength-caller-string-with-bounds" and row["callsite_count"] == "4" for row in rows)

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-164 callsite map consumed" in story_text
    assert "UI text argument taxonomy emitted" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "RE-166" in story_text
    assert "test_re165_ui_text_rendering_argument_taxonomy.py" in story_text
    assert "item-lighting" not in story_text.lower()
    assert "test_re164" not in story_text.lower()

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "pay" + "load" not in text
        assert "op" + "code" not in text
        assert "raw" + " call target" not in text
        assert "machine" + " word" not in text
        assert "0x" not in text
