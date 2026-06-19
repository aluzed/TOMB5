from pathlib import Path
import csv

from scripts.reverse.re352_frontend_display_menu_service_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_frontend_display_menu_service_readiness_gate,
    write_all_artifacts,
)


def test_re352_gates_frontend_display_menu_without_reopening_domain():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_frontend_display_menu_service_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-352"
    assert bundle.summary.topic == "frontend-display-menu-service-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-351"
    assert bundle.summary.selected_narrow_subcluster == "frontend-display-menu-service"
    assert bundle.summary.input_candidate_count == 2
    assert bundle.summary.candidate_gate_count == 1
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.selected_followup_candidate_id == "de919274685f"
    assert bundle.summary.next_ticket == "RE-353"
    assert bundle.summary.next_topic == "frontend-display-menu-service-candidate-proof-export"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.candidate_rows) == 2
    first, second = bundle.candidate_rows
    assert first.rank == 1
    assert first.source_rank == 8
    assert first.candidate_id == "de919274685f"
    assert first.frontend_display_menu_context_count == 6
    assert first.proof_signal_class == "caller-frontend-display-menu-context-only"
    assert first.readiness_gate == "blocked-needs-candidate-level-proof"
    assert first.ready_to_reopen_domain == "no"
    assert first.source_patch_authorized == "no"
    assert first.next_probe == "candidate-proof-export"

    assert second.rank == 2
    assert second.source_rank == 14
    assert second.candidate_id == "4c90c6af8f9d"
    assert second.frontend_display_menu_context_count == 6
    assert second.proof_signal_class == "caller-frontend-display-menu-context-only"
    assert second.next_probe == "defer-after-re353"

    gate = bundle.gate_rows[0]
    assert gate.gate_class == "candidate-level-source-symbolic-proof-missing"
    assert gate.candidate_count == 2
    assert gate.representative_candidates == "de919274685f;4c90c6af8f9d"
    assert gate.gate_decision == "request-still-narrower-export"
    assert gate.ready_to_reopen_domain == "no"
    assert gate.source_patch_authorized == "no"
    assert gate.next_ticket == "RE-353"
    assert gate.next_topic == "frontend-display-menu-service-candidate-proof-export"

    for row in bundle.candidate_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text


def test_re352_writes_metadata_only_readiness_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_frontend_display_menu_service_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"candidates_csv", "gates_csv", "summary_csv", "handoff_csv", "md", "story"}

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert len(candidates) == 2
    assert "ghidra_entry" not in candidates[0]
    assert "ghidra_name" not in candidates[0]
    assert candidates[0]["candidate_id"] == "de919274685f"
    assert candidates[0]["frontend_display_menu_context_count"] == "6"
    assert candidates[0]["readiness_gate"] == "blocked-needs-candidate-level-proof"
    assert candidates[0]["next_probe"] == "candidate-proof-export"
    assert candidates[1]["candidate_id"] == "4c90c6af8f9d"
    assert candidates[1]["next_probe"] == "defer-after-re353"

    gates = list(csv.DictReader(written["gates_csv"].open(newline="", encoding="utf-8")))
    assert gates == [
        {
            "rank": "1",
            "gate_class": "candidate-level-source-symbolic-proof-missing",
            "candidate_count": "2",
            "representative_candidates": "de919274685f;4c90c6af8f9d",
            "gate_decision": "request-still-narrower-export",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-353",
            "next_topic": "frontend-display-menu-service-candidate-proof-export",
            "stop_condition": "candidate-level source-symbolic proof is required before proof-domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-353"
    assert handoff["next_topic"] == "frontend-display-menu-service-candidate-proof-export"
    assert handoff["selected_followup_candidate_id"] == "de919274685f"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["metadata_work_readiness"] == "ready"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-351 frontend display/menu service handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-353" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-352 frontend display/menu service readiness gate" in md
    assert "No proof-domain is reopened by this gate" in md

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
    for path in (written["candidates_csv"], written["gates_csv"], written["summary_csv"], written["handoff_csv"]):
        header = path.read_text(encoding="utf-8").splitlines()[0].split(",")
        assert raw_columns.isdisjoint(header)

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
