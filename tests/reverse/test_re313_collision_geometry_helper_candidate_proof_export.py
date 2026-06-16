from pathlib import Path
import csv

from scripts.reverse.re313_collision_geometry_helper_candidate_proof_export import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_collision_geometry_helper_candidate_proof_export,
    write_all_artifacts,
)


def test_re313_exports_candidate_scoped_proof_metadata_without_reopening_domain():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_geometry_helper_candidate_proof_export(repo)

    assert bundle.summary.story_id == "RE-313"
    assert bundle.summary.topic == "collision-geometry-helper-candidate-proof-export"
    assert bundle.summary.upstream_handoff == "RE-312"
    assert bundle.summary.selected_candidate_id == "5e99f39fd8ef"
    assert bundle.summary.source_symbol_context_count == 27
    assert bundle.summary.caller_context_count == 20
    assert bundle.summary.callee_context_count == 7
    assert bundle.summary.direct_repo_symbol_count == 0
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-314"
    assert bundle.summary.next_topic == "collision-geometry-helper-candidate-callsite-map"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.context_rows) == 27
    assert len(bundle.proof_rows) == 1
    assert bundle.proof_rows[0].proof_gate == "blocked-unmapped-candidate-identity"
    assert bundle.proof_rows[0].candidate_level_proof == "no"
    assert bundle.proof_rows[0].ready_to_reopen_domain == "no"
    assert bundle.proof_rows[0].source_patch_authorized == "no"
    assert bundle.proof_rows[0].next_ticket == "RE-314"

    caller_rows = [row for row in bundle.context_rows if row.context_kind == "caller"]
    callee_rows = [row for row in bundle.context_rows if row.context_kind == "callee"]
    assert len(caller_rows) == 20
    assert len(callee_rows) == 7
    assert {row.geometry_role for row in callee_rows} == {"geometry-callee"}
    assert all(row.candidate_level_proof == "no" for row in bundle.context_rows)
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.context_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.context_rows)

    for row in bundle.context_rows + bundle.proof_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text


def test_re313_writes_metadata_only_candidate_proof_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_geometry_helper_candidate_proof_export(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"contexts_csv", "proof_csv", "summary_csv", "handoff_csv", "md", "story"}

    contexts = list(csv.DictReader(written["contexts_csv"].open(newline="", encoding="utf-8")))
    assert len(contexts) == 27
    assert "ghidra_entry" not in contexts[0]
    assert "ghidra_name" not in contexts[0]
    assert contexts[0]["candidate_id"] == "5e99f39fd8ef"
    assert contexts[0]["context_kind"] == "caller"

    proof = list(csv.DictReader(written["proof_csv"].open(newline="", encoding="utf-8")))
    assert proof == [
        {
            "rank": "1",
            "candidate_id": "5e99f39fd8ef",
            "source_symbol_context_count": "27",
            "caller_context_count": "20",
            "callee_context_count": "7",
            "direct_repo_symbol_count": "0",
            "candidate_level_proof_count": "0",
            "proof_gate": "blocked-unmapped-candidate-identity",
            "candidate_level_proof": "no",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-314",
            "next_topic": "collision-geometry-helper-candidate-callsite-map",
            "stop_condition": "candidate hash still lacks direct repo symbol proof; build a source-backed callsite map next",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-314"
    assert handoff["next_topic"] == "collision-geometry-helper-candidate-callsite-map"
    assert handoff["selected_candidate_id"] == "5e99f39fd8ef"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-312 candidate proof-export handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-314" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-313 collision geometry helper candidate proof export" in md
    assert "No proof-domain is reopened by this export" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
