from pathlib import Path
import csv

from scripts.reverse.re109_scripted_runtime_control_audit import build_scripted_runtime_audit, write_all_artifacts


def test_re109_opens_scripted_runtime_control_from_re077_after_object_runtime_exhaustion():
    repo = Path(__file__).resolve().parents[2]
    audit = build_scripted_runtime_audit(repo)

    assert audit.story_id == "RE-109"
    assert audit.domain_id == "module-game"
    assert audit.cluster == "gameflow-runtime-control"
    assert audit.subcluster == "scripted-runtime-control"
    assert audit.pivot == "andrea2_control"
    assert [row.function for row in audit.rows] == ["andrea2_control", "special3_control"]
    assert audit.code_change_ready_count == 0
    assert audit.marker_ready_count == 0
    assert audit.readiness == "blocked"
    assert audit.next_ticket == "RE-110"


def test_re109_outputs_metadata_only_artifacts(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_scripted_runtime_audit(repo)
    written = write_all_artifacts(audit, tmp_path)

    assert written["audit_csv"].name == "re109-scripted-runtime-control-proof-first-audit.csv"
    assert written["subclusters_csv"].name == "re109-scripted-runtime-control-subclusters.csv"
    assert written["ticket_plan_csv"].name == "re109-scripted-runtime-control-ticket-plan.csv"
    assert written["md"].name == "re109-scripted-runtime-control-proof-first-audit.md"
    assert written["story"].name == "RE-109-scripted-runtime-control-proof-first-audit.md"

    with written["ticket_plan_csv"].open(newline="", encoding="utf-8") as f:
        plan = list(csv.DictReader(f))
    assert [row["story_id"] for row in plan] == ["RE-110", "RE-111", "RE-112", "RE-113", "RE-114", "RE-115", "RE-116"]

    with written["audit_csv"].open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert [row["function"] for row in rows] == ["andrea2_control", "special3_control"]
    assert {row["code_change_ready"] for row in rows} == {"no"}
    assert {row["marker_ready"] for row in rows} == {"no"}

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "test_re109_scripted_runtime_audit.py" in story_text
    assert "next gameflow runtime subcluster" in written["ticket_plan_csv"].read_text(encoding="utf-8")
    assert "next object runtime subcluster" not in written["ticket_plan_csv"].read_text(encoding="utf-8")

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "machine word" not in text
        assert "raw call target" not in text
        assert "0x" not in text
