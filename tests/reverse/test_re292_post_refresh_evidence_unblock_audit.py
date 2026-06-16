from pathlib import Path
import csv

from scripts.reverse.re292_post_refresh_evidence_unblock_audit import (
    FORBIDDEN,
    build_audit,
    write_all_artifacts,
)


def test_re292_evidence_unblock_consumes_re291_and_does_not_select_fake_domain():
    repo = Path(__file__).resolve().parents[2]
    audit = build_audit(repo)

    assert audit.story_id == "RE-292"
    assert audit.topic == "post-refresh-evidence-unblock-audit"
    assert audit.upstream_handoff == "RE-291"
    assert audit.priority_changed == "no"
    assert audit.source_map_rows == 1250
    assert audit.priority_rows == 348
    assert audit.generated_artifact_count == 295
    assert audit.proof_audit_count >= 34
    assert audit.callsite_map_count >= 13
    assert audit.equivalence_gate_count >= 7
    assert audit.new_priority_candidate_count == 0
    assert audit.new_non_raw_proof_evidence == "no"
    assert audit.next_ticket == "TBD"
    assert audit.next_topic == "await-new-non-raw-proof-evidence"
    assert audit.selected_domain == "none"
    assert audit.selected_pivot == "none"
    assert audit.code_change_readiness == "blocked"


def test_re292_outputs_metadata_only_blocked_handoff_and_followup_plan(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_audit(repo)
    written = write_all_artifacts(audit, tmp_path)

    assert set(written) == {"audit_csv", "handoff_csv", "followup_csv", "md", "story"}

    rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == 1
    assert rows[0]["new_priority_candidate_count"] == "0"
    assert rows[0]["new_non_raw_proof_evidence"] == "no"

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "TBD"
    assert handoff["next_topic"] == "await-new-non-raw-proof-evidence"
    assert handoff["selected_domain"] == "none"
    assert handoff["code_change_readiness"] == "blocked"

    followups = list(csv.DictReader(written["followup_csv"].open(newline="", encoding="utf-8")))
    assert [row["ticket_id"] for row in followups] == ["UNBLOCK-1", "UNBLOCK-2", "UNBLOCK-3"]
    assert all(row["status"] == "blocked-pending-input" for row in followups)

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-292 post-refresh evidence unblock audit" in md
    assert "New priority candidates: `0`" in md
    assert "New non-raw proof evidence: `no`" in md
    assert "No production source or marker change is authorized" in md

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-291 refresh handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "Readiness: `blocked`" in story

    for key in ("audit_csv", "handoff_csv", "followup_csv", "md", "story"):
        text = written[key].read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
