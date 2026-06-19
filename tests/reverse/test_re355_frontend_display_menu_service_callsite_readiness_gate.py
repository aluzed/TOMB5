from pathlib import Path
import csv

from scripts.reverse.re355_frontend_display_menu_service_callsite_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_frontend_display_menu_service_callsite_readiness_gate,
    write_all_artifacts,
)


def test_re355_gates_frontend_display_menu_callsite_families_and_selects_next_candidate():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_frontend_display_menu_service_callsite_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-355"
    assert bundle.summary.topic == "frontend-display-menu-service-callsite-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-354"
    assert bundle.summary.selected_candidate_id == "de919274685f"
    assert bundle.summary.next_candidate_id == "4c90c6af8f9d"
    assert bundle.summary.source_context_function_count == 25
    assert bundle.summary.source_backed_callsite_count == 326
    assert bundle.summary.callsite_family_count == 9
    assert bundle.summary.implemented_callsite_family_count == 9
    assert bundle.summary.stub_only_callsite_family_count == 0
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-356"
    assert bundle.summary.next_topic == "frontend-display-menu-service-next-candidate-proof-export"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.callsite_family for row in bundle.family_rows] == [
        "gpu-display-helper",
        "level-load-service-helper",
        "inventory-menu-helper",
        "audio-sound-helper",
        "platform-lifecycle-helper",
        "text-ui-helper",
        "input-pad-helper",
        "memory-card-helper",
        "diagnostic-helper",
    ]
    assert [row.source_backed_callsite_count for row in bundle.family_rows] == [162, 80, 19, 19, 18, 12, 8, 4, 4]
    assert [row.implemented_callsite_count for row in bundle.family_rows] == [162, 80, 19, 19, 18, 12, 8, 4, 4]
    assert [row.stub_callsite_count for row in bundle.family_rows] == [0] * 9
    assert [row.implemented_caller_count for row in bundle.family_rows] == [10, 3, 1, 2, 3, 3, 2, 2, 1]
    assert all(row.candidate_level_proof == "no" for row in bundle.family_rows)
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.family_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.family_rows)
    assert all(row.readiness_gate == "blocked-no-candidate-level-proof" for row in bundle.family_rows)
    assert all(row.next_probe == "needs-non-raw-candidate-equivalence-proof" for row in bundle.family_rows)

    decision = bundle.decision_rows[0]
    assert decision.readiness_gate == "blocked-no-callsite-family-proves-candidate"
    assert decision.decision == "deny-domain-reopen"
    assert decision.next_candidate_id == "4c90c6af8f9d"
    assert decision.next_ticket == "RE-356"

    for row in bundle.family_rows + bundle.decision_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text
        assert "ghidra" not in row_text
        assert "source_line_text" not in row_text


def test_re355_writes_metadata_only_callsite_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_frontend_display_menu_service_callsite_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"families_csv", "decision_csv", "summary_csv", "handoff_csv", "md", "story"}

    families = list(csv.DictReader(written["families_csv"].open(newline="", encoding="utf-8")))
    assert len(families) == 9
    assert "source_line_text" not in families[0]
    assert families[0]["candidate_id"] == "de919274685f"
    assert families[0]["callsite_family"] == "gpu-display-helper"
    assert families[0]["source_backed_callsite_count"] == "162"
    assert families[0]["implemented_callsite_count"] == "162"
    assert families[0]["readiness_gate"] == "blocked-no-candidate-level-proof"

    decision = list(csv.DictReader(written["decision_csv"].open(newline="", encoding="utf-8")))
    assert decision == [
        {
            "rank": "1",
            "candidate_id": "de919274685f",
            "callsite_family_count": "9",
            "implemented_callsite_family_count": "9",
            "candidate_level_proof_count": "0",
            "readiness_gate": "blocked-no-callsite-family-proves-candidate",
            "decision": "deny-domain-reopen",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "selected_domain": "none",
            "selected_pivot": "none",
            "next_ticket": "RE-356",
            "next_topic": "frontend-display-menu-service-next-candidate-proof-export",
            "next_candidate_id": "4c90c6af8f9d",
            "stop_condition": "source-backed frontend display/menu callsite families do not prove candidate-level behavior",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-356"
    assert handoff["selected_candidate_id"] == "de919274685f"
    assert handoff["next_candidate_id"] == "4c90c6af8f9d"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-354 callsite handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-356" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-355 frontend display/menu service callsite readiness gate" in md
    assert "No frontend display/menu callsite family proves candidate-level behavior" in md

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
    for path in (written["families_csv"], written["decision_csv"], written["summary_csv"], written["handoff_csv"]):
        header = path.read_text(encoding="utf-8").splitlines()[0].split(",")
        assert raw_columns.isdisjoint(header)

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
