from pathlib import Path
import csv

from scripts.reverse.re093_dynamic_light_control_audit import build_dynamic_light_audit, write_all_artifacts


def test_re093_consumes_re092_handoff_and_opens_dynamic_light_control():
    repo = Path(__file__).resolve().parents[2]
    audit = build_dynamic_light_audit(repo)

    assert audit.story_id == "RE-093"
    assert audit.domain_id == "module-game"
    assert audit.cluster == "gameflow-runtime-control"
    assert audit.subcluster == "dynamic-light-control"
    assert audit.pivot == "ControlElectricalLight"
    assert [row.function for row in audit.rows] == ["ControlElectricalLight", "ControlStrobeLight"]
    assert audit.code_change_ready_count == 0
    assert audit.marker_ready_count == 0
    assert audit.readiness == "blocked"
    assert audit.next_ticket == "RE-094"


def test_re093_outputs_metadata_only_artifacts(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_dynamic_light_audit(repo)
    written = write_all_artifacts(audit, tmp_path)

    assert written["audit_csv"].name == "re093-dynamic-light-control-proof-first-audit.csv"
    assert written["subclusters_csv"].name == "re093-dynamic-light-control-subclusters.csv"
    assert written["ticket_plan_csv"].name == "re093-dynamic-light-control-ticket-plan.csv"
    assert written["md"].name == "re093-dynamic-light-control-proof-first-audit.md"
    assert written["story"].name == "RE-093-dynamic-light-control-proof-first-audit.md"

    with written["ticket_plan_csv"].open(newline="", encoding="utf-8") as f:
        plan = list(csv.DictReader(f))
    assert [row["story_id"] for row in plan] == ["RE-094", "RE-095", "RE-096", "RE-097", "RE-098", "RE-099", "RE-100"]

    with written["audit_csv"].open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert {row["function"] for row in rows} == {"ControlElectricalLight", "ControlStrobeLight"}
    assert {row["code_change_ready"] for row in rows} == {"no"}
    assert {row["marker_ready"] for row in rows} == {"no"}

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "- [x]" in story_text
    assert "code change readiness: `blocked`" in story_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "machine word" not in text
        assert "raw call target" not in text
        assert "0x" not in text
