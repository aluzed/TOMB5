from pathlib import Path
import csv

from scripts.reverse.re117_lara_runtime_control_audit import build_lara_runtime_audit, write_all_artifacts


def test_re117_consumes_re116_handoff_and_opens_lara_runtime_control():
    repo = Path(__file__).resolve().parents[2]
    audit = build_lara_runtime_audit(repo)

    assert audit.story_id == "RE-117"
    assert audit.upstream_ticket == "RE-116"
    assert audit.cluster == "gameflow-runtime-control"
    assert audit.subcluster == "lara-runtime-control"
    assert audit.pivot == "LaraControl"
    assert [row.function for row in audit.rows] == ["LaraControl"]
    row = audit.rows[0]
    assert row.file == "GAME/LARAMISC.C"
    assert row.line == 163
    assert row.implementation_status == "implemented-source"
    assert row.object_family == "lara-runtime-state"
    assert row.code_change_ready == "no"
    assert row.marker_ready == "no"
    assert "Lara runtime state contract" in row.blocker
    assert [plan.story_id for plan in audit.ticket_plan] == ["RE-118", "RE-119", "RE-120", "RE-121", "RE-122", "RE-123", "RE-124"]


def test_re117_outputs_metadata_only_artifacts_and_progress_tracker(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_lara_runtime_audit(repo)
    written = write_all_artifacts(audit, tmp_path)

    audit_rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(audit_rows) == 1
    assert audit_rows[0]["function"] == "LaraControl"
    assert audit_rows[0]["code_change_ready"] == "no"

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-116 handoff consumed" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "test_re117_lara_runtime_audit.py" in story_text

    plan_text = written["ticket_plan_csv"].read_text(encoding="utf-8")
    assert "RE-124" in plan_text
    assert "next gameflow runtime subcluster" in plan_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "raw call target" not in text
        assert "machine word" not in text
        assert "0x" not in text
