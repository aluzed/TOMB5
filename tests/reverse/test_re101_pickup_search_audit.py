from pathlib import Path
import csv

from scripts.reverse.re101_pickup_search_control_audit import build_pickup_search_audit, write_all_artifacts


def test_re101_consumes_re100_handoff_and_opens_pickup_search_control():
    repo = Path(__file__).resolve().parents[2]
    audit = build_pickup_search_audit(repo)

    assert audit.story_id == "RE-101"
    assert audit.domain_id == "module-game"
    assert audit.cluster == "gameflow-runtime-control"
    assert audit.subcluster == "pickup-search-control"
    assert audit.pivot == "SearchObjectControl"
    assert [row.function for row in audit.rows] == ["SearchObjectControl"]
    assert audit.code_change_ready_count == 0
    assert audit.marker_ready_count == 0
    assert audit.readiness == "blocked"
    assert audit.next_ticket == "RE-102"


def test_re101_outputs_metadata_only_artifacts(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_pickup_search_audit(repo)
    written = write_all_artifacts(audit, tmp_path)

    assert written["audit_csv"].name == "re101-pickup-search-control-proof-first-audit.csv"
    assert written["subclusters_csv"].name == "re101-pickup-search-control-subclusters.csv"
    assert written["ticket_plan_csv"].name == "re101-pickup-search-control-ticket-plan.csv"
    assert written["md"].name == "re101-pickup-search-control-proof-first-audit.md"
    assert written["story"].name == "RE-101-pickup-search-control-proof-first-audit.md"

    with written["ticket_plan_csv"].open(newline="", encoding="utf-8") as f:
        plan = list(csv.DictReader(f))
    assert [row["story_id"] for row in plan] == ["RE-102", "RE-103", "RE-104", "RE-105", "RE-106", "RE-107", "RE-108"]

    with written["audit_csv"].open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["function"] == "SearchObjectControl"
    assert rows[0]["code_change_ready"] == "no"
    assert rows[0]["marker_ready"] == "no"

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "- [x]" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "test_re101_pickup_search_audit.py" in story_text
    assert "test_re093_pickup_search_audit.py" not in story_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "machine word" not in text
        assert "raw call target" not in text
        assert "0x" not in text
