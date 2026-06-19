from pathlib import Path
import csv

from scripts.reverse.re366_runtime_callee_bridge_candidate_proof_export import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_runtime_callee_bridge_candidate_proof_export,
    write_all_artifacts,
)


def test_re366_exports_runtime_callee_bridge_candidate_context_without_reopening_domain():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_runtime_callee_bridge_candidate_proof_export(repo)

    assert bundle.summary.story_id == "RE-366"
    assert bundle.summary.topic == "runtime-callee-bridge-candidate-proof-export"
    assert bundle.summary.upstream_handoff == "RE-365"
    assert bundle.summary.selected_candidate_id == "a01f47cb95a4"
    assert bundle.summary.source_symbol_context_count == 11
    assert bundle.summary.caller_context_count == 0
    assert bundle.summary.callee_context_count == 11
    assert bundle.summary.direct_repo_symbol_count == 0
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-367"
    assert bundle.summary.next_topic == "runtime-callee-bridge-candidate-callsite-map"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.context_rows) == 11
    caller_rows = [row for row in bundle.context_rows if row.context_kind == "caller"]
    callee_rows = [row for row in bundle.context_rows if row.context_kind == "callee"]
    assert len(caller_rows) == 0
    assert len(callee_rows) == 11
    assert {row.source_symbol for row in callee_rows if row.context_family == "floor-height-query"} == {
        "GetFloor",
        "GetHeight",
    }
    assert {row.source_symbol for row in callee_rows if row.context_family == "item-room-runtime"} == {
        "ItemNewRoom",
        "KillItem",
        "RemoveActiveItem",
    }
    assert {row.source_symbol for row in callee_rows if row.context_family == "effects-spark"} == {
        "GetFreeSpark",
        "SoundEffect",
    }
    assert {row.source_symbol for row in callee_rows if row.context_family == "audio-cd-service"} == {"S_CDPlay"}
    assert {row.source_module for row in callee_rows} == {"GAME", "SPEC_PSX", "SPEC_PSXPC", "SPEC_PSXPC_N"}
    assert all(row.runtime_callee_bridge_role.endswith("callee") for row in callee_rows)
    assert all(row.candidate_level_proof == "no" for row in bundle.context_rows)
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.context_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.context_rows)

    gate = bundle.proof_rows[0]
    assert gate.proof_gate == "blocked-unmapped-candidate-identity"
    assert gate.candidate_level_proof == "no"
    assert gate.ready_to_reopen_domain == "no"
    assert gate.source_patch_authorized == "no"
    assert gate.next_ticket == "RE-367"
    assert gate.next_topic == "runtime-callee-bridge-candidate-callsite-map"

    for row in bundle.context_rows + bundle.proof_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text


def test_re366_writes_metadata_only_candidate_proof_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_runtime_callee_bridge_candidate_proof_export(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"contexts_csv", "proof_csv", "summary_csv", "handoff_csv", "md", "story"}

    contexts = list(csv.DictReader(written["contexts_csv"].open(newline="", encoding="utf-8")))
    assert len(contexts) == 11
    assert "ghidra_entry" not in contexts[0]
    assert "ghidra_name" not in contexts[0]
    assert contexts[0]["candidate_id"] == "a01f47cb95a4"
    assert contexts[0]["context_kind"] == "callee"

    proof = list(csv.DictReader(written["proof_csv"].open(newline="", encoding="utf-8")))
    assert proof == [
        {
            "rank": "1",
            "candidate_id": "a01f47cb95a4",
            "source_symbol_context_count": "11",
            "caller_context_count": "0",
            "callee_context_count": "11",
            "direct_repo_symbol_count": "0",
            "candidate_level_proof_count": "0",
            "proof_gate": "blocked-unmapped-candidate-identity",
            "candidate_level_proof": "no",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-367",
            "next_topic": "runtime-callee-bridge-candidate-callsite-map",
            "stop_condition": "runtime-callee-bridge candidate hash still lacks direct repo symbol proof; build a source-backed callsite map next",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-367"
    assert handoff["next_topic"] == "runtime-callee-bridge-candidate-callsite-map"
    assert handoff["selected_candidate_id"] == "a01f47cb95a4"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-365 candidate proof-export handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-367" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-366 runtime callee bridge candidate proof export" in md
    assert "No proof-domain is reopened by this export" in md

    raw_columns = {
        "ghidra_entry",
        "ghidra_name",
        "call_address",
        "payload_offset",
        "word_le_hex",
        "opcode",
        "raw_evidence",
        "source_line_text",
    }
    for path in (written["contexts_csv"], written["proof_csv"], written["summary_csv"], written["handoff_csv"]):
        header = path.read_text(encoding="utf-8").splitlines()[0].split(",")
        assert raw_columns.isdisjoint(header)

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
