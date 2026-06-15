from pathlib import Path
import csv

from scripts.reverse.re125_runtime_support_mixed_audit import build_runtime_support_audit, write_all_artifacts


def test_re125_consumes_re124_handoff_and_opens_runtime_support_mixed():
    repo = Path(__file__).resolve().parents[2]
    audit = build_runtime_support_audit(repo)

    assert audit.story_id == "RE-125"
    assert audit.upstream_ticket == "RE-124"
    assert audit.subcluster == "runtime-support-mixed"
    assert audit.pivot == "ResetGuards"
    assert audit.next_ticket == "RE-126"
    assert audit.code_change_ready_count == 0
    assert audit.marker_ready_count == 0
    assert [row.function for row in audit.rows] == ["ResetGuards"]
    assert audit.rows[0].implementation_status == "unimplemented-stub"
    assert audit.ticket_plan[0].story_id == "RE-126"
    assert audit.ticket_plan[-1].story_id == "RE-132"
    assert all(row.code_change_ready == "no" and row.marker_ready == "no" for row in audit.rows)


def test_re125_outputs_metadata_only_artifacts_and_progress_tracker(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_runtime_support_audit(repo)
    written = write_all_artifacts(audit, tmp_path)

    audit_rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(audit_rows) == 1
    assert audit_rows[0]["function"] == "ResetGuards"
    assert audit_rows[0]["subcluster"] == "runtime-support-mixed"
    assert audit_rows[0]["object_family"] == "runtime-support-state"
    assert audit_rows[0]["next_probe"].startswith("RE-126")

    plan_rows = list(csv.DictReader(written["ticket_plan_csv"].open(newline="", encoding="utf-8")))
    assert [row["story_id"] for row in plan_rows] == ["RE-126", "RE-127", "RE-128", "RE-129", "RE-130", "RE-131", "RE-132"]
    assert "gameflow runtime subcluster" in plan_rows[-1]["goal"]
    assert "object runtime" not in plan_rows[-1]["goal"]

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-124 handoff consumed" in story_text
    assert "ResetGuards" in story_text
    assert "test_re125_runtime_support_audit.py" in story_text
    assert "code change readiness: `blocked`" in story_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "raw call target" not in text
        assert "machine word" not in text
        assert "0x" not in text
