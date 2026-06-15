from pathlib import Path
import csv
import pytest

from scripts.reverse.re170_module_spec_psxpc_n_closure_or_handoff import (
    build_closure_or_handoff,
    validate_re169_handoff,
    validate_re169_selection,
    write_all_artifacts,
)


def test_re170_consumes_re169_and_opens_geometry_support_chain():
    repo = Path(__file__).resolve().parents[2]
    gate = build_closure_or_handoff(repo)

    assert gate.story_id == "RE-170"
    assert gate.upstream_ticket == "RE-169"
    assert gate.domain_id == "module-spec_psxpc_n"
    assert gate.selected_cluster == "geometry-support"
    assert gate.selected_pivot == "GetBoundsAccurate"
    assert gate.domain_decision == "module-spec-psxpc-n-not-closed-geometry-support-proof-chain-opened"
    assert gate.code_change_readiness == "documentation-only-handoff-gate"
    assert gate.next_ticket == "RE-171"
    assert gate.next_topic == "geometry-support-proof-first-audit"
    assert gate.source_patch_ready_count == 0
    assert gate.marker_ready_count == 0

    assert len(gate.scope_rows) == 7
    assert [row.function for row in gate.scope_rows] == [
        "GetBoundsAccurate",
        "CalcClipWindow_ONGTE",
        "InterpolateMatrix_CL",
        "GetFrames_CL",
        "GetBestFrame",
        "GetChange",
        "DecodeTrack",
    ]
    assert all(row.cluster == "geometry-support" for row in gate.scope_rows)
    assert all(row.code_change_readiness == "blocked" for row in gate.scope_rows)
    assert all(row.marker_readiness == "blocked" for row in gate.scope_rows)
    assert gate.scope_rows[0].recommended_first_proof == "geometry-support caller/state inventory"

    assert [item.story_id for item in gate.ticket_plan] == ["RE-171", "RE-172", "RE-173", "RE-174", "RE-175", "RE-176", "RE-177"]
    assert gate.ticket_plan[0].topic == "geometry-support-proof-first-audit"
    assert gate.ticket_plan[-1].topic == "module-spec-psxpc-n-post-geometry-next-cluster-selection"


def test_re170_fail_closed_on_upstream_drift():
    with pytest.raises(ValueError, match="RE-169 handoff drift"):
        validate_re169_handoff([
            {
                "next_ticket": "RE-170",
                "next_topic": "module-spec-psxpc-n-closure-or-handoff",
                "selected_cluster": "frontend-loadsave",
                "selected_pivot": "SaveGame",
                "outcome": "next-cluster-selected-source-patch-blocked",
                "dependency": "RE-169 next-cluster selection",
            }
        ])

    with pytest.raises(ValueError, match="selected cluster drifted"):
        validate_re169_selection([
            {
                "cluster": "geometry-support",
                "top_function": "GetBestFrame",
                "selection_decision": "selected",
                "code_change_readiness": "blocked",
            }
        ])


def test_re170_outputs_metadata_only_handoff_story_and_plan(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    gate = build_closure_or_handoff(repo)
    written = write_all_artifacts(gate, tmp_path)

    scope_rows = list(csv.DictReader(written["scope_csv"].open(newline="", encoding="utf-8")))
    assert len(scope_rows) == 7
    assert scope_rows[0]["function"] == "GetBoundsAccurate"
    assert scope_rows[0]["recommended_first_proof"] == "geometry-support caller/state inventory"
    assert all(row["source_patch_decision"] == "denied" for row in scope_rows)
    assert all(row["marker_change_decision"] == "denied" for row in scope_rows)

    plan_rows = list(csv.DictReader(written["ticket_plan_csv"].open(newline="", encoding="utf-8")))
    assert len(plan_rows) == 7
    assert plan_rows[0]["story_id"] == "RE-171"
    assert plan_rows[0]["scope"] == "GetBoundsAccurate plus geometry-support rows"
    assert plan_rows[-1]["story_id"] == "RE-177"

    handoff_rows = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))
    assert handoff_rows == [
        {
            "next_ticket": "RE-171",
            "next_topic": "geometry-support-proof-first-audit",
            "selected_cluster": "geometry-support",
            "selected_pivot": "GetBoundsAccurate",
            "outcome": "geometry-support-proof-chain-opened",
            "reason": "module SPEC_PSXPC_N remains open; geometry-support needs caller/state and non-raw equivalence proof before source or marker changes",
            "dependency": "RE-170 closure-or-handoff gate",
            "stop_condition": "geometry-support proof-first audit emitted",
        }
    ]

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-169 geometry-support handoff consumed" in story_text
    assert "domain closure denied" in story_text
    assert "RE-171" in story_text
    assert "No production source or marker change is authorized" in story_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "pay" + "load" not in text
        assert "op" + "code" not in text
        assert "raw" + " call target" not in text
        assert "machine" + " word" not in text
        assert "0x" not in text
