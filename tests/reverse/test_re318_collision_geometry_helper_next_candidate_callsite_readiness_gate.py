from pathlib import Path
import csv

from scripts.reverse.re318_collision_geometry_helper_next_candidate_callsite_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_collision_geometry_helper_next_candidate_callsite_readiness_gate,
    write_all_artifacts,
)


def test_re318_gates_next_candidate_callsite_families_without_reopening_domain():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_geometry_helper_next_candidate_callsite_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-318"
    assert bundle.summary.topic == "collision-geometry-helper-next-candidate-callsite-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-317"
    assert bundle.summary.selected_candidate_id == "d96359c1d9f3"
    assert bundle.summary.previous_candidate_id == "5e99f39fd8ef"
    assert bundle.summary.next_candidate_id == "61d55bb1809b"
    assert bundle.summary.source_context_function_count == 23
    assert bundle.summary.source_backed_callsite_count == 40
    assert bundle.summary.callsite_family_count == 4
    assert bundle.summary.implemented_callsite_family_count == 3
    assert bundle.summary.stub_only_callsite_family_count == 1
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-319"
    assert bundle.summary.next_topic == "collision-geometry-helper-final-candidate-proof-export"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.callsite_family for row in bundle.family_rows] == [
        "collision-helper",
        "position-test",
        "trigger-helper",
        "stub-marker",
    ]
    assert [row.source_backed_callsite_count for row in bundle.family_rows] == [8, 8, 5, 19]
    assert [row.implemented_caller_count for row in bundle.family_rows] == [3, 3, 2, 0]
    assert all(row.candidate_level_proof == "no" for row in bundle.family_rows)
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.family_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.family_rows)
    assert bundle.family_rows[-1].readiness_gate == "blocked-stub-only-family"
    assert bundle.family_rows[0].readiness_gate == "blocked-no-candidate-level-proof"

    decision = bundle.decision_rows[0]
    assert decision.readiness_gate == "blocked-no-callsite-family-proves-candidate"
    assert decision.decision == "deny-domain-reopen"
    assert decision.next_candidate_id == "61d55bb1809b"

    for row in bundle.family_rows + bundle.decision_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "unimplemented();" not in row_text


def test_re318_writes_metadata_only_next_candidate_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_geometry_helper_next_candidate_callsite_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"families_csv", "decision_csv", "summary_csv", "handoff_csv", "md", "story"}

    families = list(csv.DictReader(written["families_csv"].open(newline="", encoding="utf-8")))
    assert len(families) == 4
    assert "source_line_text" not in families[0]
    assert families[0]["candidate_id"] == "d96359c1d9f3"
    assert families[0]["previous_candidate_id"] == "5e99f39fd8ef"
    assert families[0]["callsite_family"] == "collision-helper"
    assert families[0]["source_backed_callsite_count"] == "8"
    assert families[0]["readiness_gate"] == "blocked-no-candidate-level-proof"
    assert families[-1]["callsite_family"] == "stub-marker"
    assert families[-1]["source_backed_callsite_count"] == "19"
    assert families[-1]["readiness_gate"] == "blocked-stub-only-family"

    decision = list(csv.DictReader(written["decision_csv"].open(newline="", encoding="utf-8")))
    assert decision == [
        {
            "rank": "1",
            "candidate_id": "d96359c1d9f3",
            "previous_candidate_id": "5e99f39fd8ef",
            "callsite_family_count": "4",
            "implemented_callsite_family_count": "3",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-no-callsite-family-proves-candidate",
            "decision": "deny-domain-reopen",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "selected_domain": "none",
            "selected_pivot": "none",
            "next_ticket": "RE-319",
            "next_topic": "collision-geometry-helper-final-candidate-proof-export",
            "next_candidate_id": "61d55bb1809b",
            "stop_condition": "next-candidate source-backed callsite families do not prove candidate-level behavior",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-319"
    assert handoff["selected_candidate_id"] == "d96359c1d9f3"
    assert handoff["previous_candidate_id"] == "5e99f39fd8ef"
    assert handoff["next_candidate_id"] == "61d55bb1809b"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-317 next-candidate callsite handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-319" in story
    assert "61d55bb1809b" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-318 collision geometry helper next candidate callsite readiness gate" in md
    assert "No next-candidate callsite family proves candidate-level behavior" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
