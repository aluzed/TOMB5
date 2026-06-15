from pathlib import Path
import csv

from scripts.reverse.re141_object_interaction_audit import build_object_interaction_audit, write_all_artifacts


def test_re141_consumes_re140_handoff_and_opens_object_interaction():
    repo = Path(__file__).resolve().parents[2]
    audit = build_object_interaction_audit(repo)

    assert audit.story_id == "RE-141"
    assert audit.upstream_ticket == "RE-140"
    assert audit.domain_id == "module-game"
    assert audit.cluster == "object-interaction"
    assert audit.pivot == "FindPlinth"
    assert audit.next_ticket == "RE-142"
    assert audit.code_change_ready_count == 0
    assert audit.marker_ready_count == 0
    assert [row.function for row in audit.rows] == [
        "FindPlinth",
        "CollectCarriedItems",
        "BaddyObjects",
        "InitialiseObjects",
        "TrapObjects",
        "ObjectObjects",
    ]
    assert audit.rows[0].implementation_status == "unimplemented-stub"
    assert audit.rows[2].object_family == "object-setup-state"
    assert audit.ticket_plan[0].story_id == "RE-142"
    assert audit.ticket_plan[-1].story_id == "RE-148"
    assert all(row.code_change_ready == "no" and row.marker_ready == "no" for row in audit.rows)


def test_re141_outputs_metadata_only_artifacts_and_progress_tracker(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_object_interaction_audit(repo)
    written = write_all_artifacts(audit, tmp_path)

    audit_rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(audit_rows) == 6
    assert audit_rows[0]["function"] == "FindPlinth"
    assert audit_rows[0]["cluster"] == "object-interaction"
    assert audit_rows[0]["object_family"] == "object-interaction-state"
    assert audit_rows[0]["next_probe"].startswith("RE-142")

    cluster_rows = list(csv.DictReader(written["clusters_csv"].open(newline="", encoding="utf-8")))
    assert cluster_rows == [{
        "cluster": "object-interaction",
        "candidate_count": "6",
        "top_function": "FindPlinth",
        "representative_functions": "FindPlinth;CollectCarriedItems;BaddyObjects;InitialiseObjects;TrapObjects;ObjectObjects",
        "object_family": "object-interaction-state",
        "readiness": "best-next-module-game-cluster",
        "blocker": "Object interaction state contract and symbolic equivalence proof missing",
        "recommended_next_ticket": "RE-142",
    }]

    plan_rows = list(csv.DictReader(written["ticket_plan_csv"].open(newline="", encoding="utf-8")))
    assert [row["story_id"] for row in plan_rows] == ["RE-142", "RE-143", "RE-144", "RE-145", "RE-146", "RE-147", "RE-148"]
    assert "item-lighting-interaction" in plan_rows[-1]["goal"]

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-140 gameplay-mixed handoff consumed" in story_text
    assert "RE-061 object-interaction rows selected" in story_text
    assert "RE-142..RE-148 ticket plan emitted" in story_text
    assert "test_re141_object_interaction_audit.py" in story_text
    assert "gameplay-mixed" not in story_text.lower().replace("re-140 gameplay-mixed handoff consumed", "")

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "raw call target" not in text
        assert "machine word" not in text
        assert "0x" not in text
