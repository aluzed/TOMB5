from pathlib import Path
import csv

from scripts.reverse.re367_runtime_callee_bridge_candidate_callsite_map import (
    SELECTED_CANDIDATE_ID,
    build_runtime_callee_bridge_candidate_callsite_map,
    write_all_artifacts,
)

REPO = Path(__file__).resolve().parents[2]


def read_rows(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_build_re367_runtime_callee_bridge_callsite_contract():
    bundle = build_runtime_callee_bridge_candidate_callsite_map(REPO)

    assert bundle.summary.story_id == "RE-367"
    assert bundle.summary.topic == "runtime-callee-bridge-candidate-callsite-map"
    assert bundle.summary.upstream_handoff == "RE-366"
    assert bundle.summary.selected_candidate_id == SELECTED_CANDIDATE_ID
    assert bundle.summary.source_context_function_count == 11
    assert bundle.summary.source_backed_callsite_count == 1
    assert bundle.summary.implemented_context_function_count == 1
    assert bundle.summary.stub_context_function_count == 1
    assert bundle.summary.no_callsite_context_function_count == 9
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-368"
    assert bundle.summary.next_topic == "runtime-callee-bridge-callsite-readiness-gate"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.function_rows) == 11
    assert len(bundle.callsite_rows) == 1
    assert len(bundle.gate_rows) == 1
    assert bundle.callsite_rows[0].caller_symbol == "GetFloor"
    assert bundle.callsite_rows[0].callee_symbol == "GetHeight"
    assert bundle.callsite_rows[0].callsite_family == "floor-height-query"
    assert bundle.callsite_rows[0].candidate_level_proof == "no"


def test_re367_writes_metadata_only_artifacts_and_handoff():
    bundle = build_runtime_callee_bridge_candidate_callsite_map(REPO)
    paths = write_all_artifacts(bundle, REPO)

    expected = {
        "functions_csv",
        "callsites_csv",
        "gate_csv",
        "summary_csv",
        "handoff_csv",
        "md",
        "story",
    }
    assert set(paths) == expected
    for path in paths.values():
        assert path.exists()
        text = path.read_text(encoding="utf-8").lower()
        assert "source_line_text" not in text
        assert "ghidra_name" not in text
        assert "payload_offset" not in text
        assert "word_le_hex" not in text
        assert "unimplemented();" not in text

    handoff = read_rows(paths["handoff_csv"])[0]
    assert handoff["story_id"] == "RE-367"
    assert handoff["next_ticket"] == "RE-368"
    assert handoff["next_topic"] == "runtime-callee-bridge-callsite-readiness-gate"
    assert handoff["selected_domain"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = paths["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-366 proof-export handoff validated." in story
    assert "RE-368" in story

    md = paths["md"].read_text(encoding="utf-8")
    assert "# RE-367 runtime callee bridge candidate callsite map" in md
    assert "Source-backed callsite rows are not source-patch authorization" in md
