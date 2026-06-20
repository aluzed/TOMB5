from pathlib import Path
import csv

from scripts.reverse.re368_runtime_callee_bridge_callsite_readiness_gate import (
    SELECTED_CANDIDATE_ID,
    build_runtime_callee_bridge_callsite_readiness_gate,
    write_all_artifacts,
)

REPO = Path(__file__).resolve().parents[2]


def read_rows(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_build_re368_runtime_callee_bridge_readiness_contract():
    bundle = build_runtime_callee_bridge_callsite_readiness_gate(REPO)

    assert bundle.summary.story_id == "RE-368"
    assert bundle.summary.topic == "runtime-callee-bridge-callsite-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-367"
    assert bundle.summary.selected_candidate_id == SELECTED_CANDIDATE_ID
    assert bundle.summary.exhausted_subcluster == "runtime-callee-bridge"
    assert bundle.summary.source_context_function_count == 11
    assert bundle.summary.source_backed_callsite_count == 1
    assert bundle.summary.callsite_family_count == 1
    assert bundle.summary.implemented_callsite_family_count == 1
    assert bundle.summary.stub_only_callsite_family_count == 0
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_deferred_candidate_id == "none"
    assert bundle.summary.next_subcluster == "none"
    assert bundle.summary.next_ticket == "TBD"
    assert bundle.summary.next_topic == "platform-frontend-service-subcluster-queue-exhausted"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.family_rows) == 1
    family = bundle.family_rows[0]
    assert family.callsite_family == "floor-height-query"
    assert family.source_backed_callsite_count == 1
    assert family.implemented_callsite_count == 1
    assert family.stub_callsite_count == 0
    assert family.candidate_level_proof == "no"
    assert family.ready_to_reopen_domain == "no"
    assert family.source_patch_authorized == "no"
    assert family.next_probe == "close-runtime-callee-bridge-subcluster"

    assert len(bundle.decision_rows) == 1
    decision = bundle.decision_rows[0]
    assert decision.decision == "deny-domain-reopen-and-exhaust-parent-subcluster-queue"
    assert decision.next_ticket == "TBD"
    assert decision.next_topic == "platform-frontend-service-subcluster-queue-exhausted"


def test_re368_writes_metadata_only_artifacts_and_handoff():
    bundle = build_runtime_callee_bridge_callsite_readiness_gate(REPO)
    paths = write_all_artifacts(bundle, REPO)

    expected = {"families_csv", "decision_csv", "summary_csv", "handoff_csv", "md", "story"}
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
    assert handoff["story_id"] == "RE-368"
    assert handoff["next_ticket"] == "TBD"
    assert handoff["next_subcluster"] == "none"
    assert handoff["selected_domain"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = paths["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-367 callsite handoff validated." in story
    assert "platform/frontend service subcluster queue is exhausted" in story

    md = paths["md"].read_text(encoding="utf-8")
    assert "# RE-368 runtime callee bridge callsite readiness gate" in md
    assert "Code readiness remains `blocked`" in md
