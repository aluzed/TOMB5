from pathlib import Path
import csv

from scripts.reverse.re169_module_spec_psxpc_n_next_cluster_selection import (
    build_next_cluster_selection,
    write_all_artifacts,
)


def test_re169_consumes_re168_handoff_and_selects_geometry_support_next():
    repo = Path(__file__).resolve().parents[2]
    selection = build_next_cluster_selection(repo)

    assert selection.story_id == "RE-169"
    assert selection.upstream_ticket == "RE-168"
    assert selection.current_cluster == "ui-text-rendering"
    assert selection.selected_cluster == "geometry-support"
    assert selection.selected_pivot == "GetBoundsAccurate"
    assert selection.next_ticket == "RE-170"
    assert selection.next_topic == "module-spec-psxpc-n-closure-or-handoff"
    assert selection.code_change_readiness == "documentation-only-selection-gate"
    assert selection.selection_status == "next-cluster-selected-source-patch-blocked"

    assert len(selection.rows) == 6
    assert [row.rank for row in selection.rows] == [1, 2, 3, 4, 5, 6]
    by_cluster = {row.cluster: row for row in selection.rows}
    assert by_cluster["geometry-support"].selection_decision == "selected"
    assert by_cluster["geometry-support"].next_action == "handoff-to-re170-closure-or-cluster-proof-gate"
    assert by_cluster["geometry-support"].recommended_proof == "source-level geometry state contract and non-raw equivalence gate"
    assert by_cluster["platform-gpu-display"].selection_decision == "deferred-nd-marker-audit"
    assert by_cluster["frontend-loadsave"].selection_decision == "deferred-after-selected-cluster"
    assert "ui-text-rendering" not in by_cluster


def test_re169_outputs_metadata_only_story_and_handoff(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    selection = build_next_cluster_selection(repo)
    written = write_all_artifacts(selection, tmp_path)

    rows = list(csv.DictReader(written["selection_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == 6
    assert rows[0]["cluster"] == "geometry-support"
    assert rows[0]["selection_decision"] == "selected"
    assert rows[0]["next_ticket"] == "RE-170"

    handoff_rows = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))
    assert handoff_rows == [
        {
            "next_ticket": "RE-170",
            "next_topic": "module-spec-psxpc-n-closure-or-handoff",
            "selected_cluster": "geometry-support",
            "selected_pivot": "GetBoundsAccurate",
            "outcome": "next-cluster-selected-source-patch-blocked",
            "reason": "ui-text-rendering source patch denied; geometry-support is the next non-ND proof-needed SPEC_PSXPC_N cluster",
            "dependency": "RE-169 next-cluster selection",
            "stop_condition": "module SPEC_PSXPC_N closure or handoff emitted",
        }
    ]

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-168 no-patch handoff consumed" in story_text
    assert "selected next cluster: `geometry-support`" in story_text
    assert "No production source or marker change is authorized" in story_text
    assert "RE-170" in story_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "pay" + "load" not in text
        assert "op" + "code" not in text
        assert "raw" + " call target" not in text
        assert "machine" + " word" not in text
        assert "0x" not in text
