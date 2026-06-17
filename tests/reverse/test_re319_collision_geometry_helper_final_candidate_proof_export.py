from pathlib import Path
import csv

from scripts.reverse.re319_collision_geometry_helper_final_candidate_proof_export import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_collision_geometry_helper_final_candidate_proof_export,
    write_all_artifacts,
)


def test_re319_exports_final_candidate_context_without_reopening_domain():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_geometry_helper_final_candidate_proof_export(repo)

    assert bundle.summary.story_id == "RE-319"
    assert bundle.summary.topic == "collision-geometry-helper-final-candidate-proof-export"
    assert bundle.summary.upstream_handoff == "RE-318"
    assert bundle.summary.selected_candidate_id == "61d55bb1809b"
    assert bundle.summary.previous_candidate_id == "d96359c1d9f3"
    assert bundle.summary.source_symbol_context_count == 21
    assert bundle.summary.caller_context_count == 20
    assert bundle.summary.callee_context_count == 1
    assert bundle.summary.direct_repo_symbol_count == 0
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-320"
    assert bundle.summary.next_topic == "collision-geometry-helper-final-candidate-callsite-map"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.context_rows) == 21
    caller_rows = [row for row in bundle.context_rows if row.context_kind == "caller"]
    callee_rows = [row for row in bundle.context_rows if row.context_kind == "callee"]
    assert len(caller_rows) == 20
    assert len(callee_rows) == 1
    assert caller_rows[0].source_symbol == "TrapCollision"
    assert any(row.source_symbol == "SwitchCollision" for row in caller_rows)
    assert any(row.source_symbol == "RollingBallCollision" for row in caller_rows)
    assert {row.source_symbol for row in callee_rows} == {"TestCollision"}
    assert {row.geometry_role for row in callee_rows} == {"geometry-callee"}
    assert all(row.candidate_level_proof == "no" for row in bundle.context_rows)
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.context_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.context_rows)

    gate = bundle.proof_rows[0]
    assert gate.proof_gate == "blocked-unmapped-candidate-identity"
    assert gate.candidate_level_proof == "no"
    assert gate.ready_to_reopen_domain == "no"
    assert gate.source_patch_authorized == "no"
    assert gate.next_ticket == "RE-320"

    for row in bundle.context_rows + bundle.proof_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text


def test_re319_writes_metadata_only_final_candidate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_geometry_helper_final_candidate_proof_export(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"contexts_csv", "proof_csv", "summary_csv", "handoff_csv", "md", "story"}

    contexts = list(csv.DictReader(written["contexts_csv"].open(newline="", encoding="utf-8")))
    assert len(contexts) == 21
    assert "ghidra_entry" not in contexts[0]
    assert "ghidra_name" not in contexts[0]
    assert contexts[0]["candidate_id"] == "61d55bb1809b"
    assert contexts[0]["context_kind"] == "caller"

    proof = list(csv.DictReader(written["proof_csv"].open(newline="", encoding="utf-8")))
    assert proof == [
        {
            "rank": "1",
            "candidate_id": "61d55bb1809b",
            "previous_candidate_id": "d96359c1d9f3",
            "source_symbol_context_count": "21",
            "caller_context_count": "20",
            "callee_context_count": "1",
            "direct_repo_symbol_count": "0",
            "candidate_level_proof_count": "0",
            "proof_gate": "blocked-unmapped-candidate-identity",
            "candidate_level_proof": "no",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-320",
            "next_topic": "collision-geometry-helper-final-candidate-callsite-map",
            "stop_condition": "final candidate still lacks direct repo symbol proof; build a source-backed callsite map next",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-320"
    assert handoff["next_topic"] == "collision-geometry-helper-final-candidate-callsite-map"
    assert handoff["selected_candidate_id"] == "61d55bb1809b"
    assert handoff["previous_candidate_id"] == "d96359c1d9f3"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-318 final-candidate handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-320" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-319 collision geometry helper final candidate proof export" in md
    assert "No proof-domain is reopened by this export" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
