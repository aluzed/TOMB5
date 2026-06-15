from pathlib import Path
import csv

from scripts.reverse.re149_item_lighting_interaction_audit import (
    build_item_lighting_interaction_audit,
    write_all_artifacts,
)


def test_re149_consumes_re148_handoff_and_opens_item_lighting_interaction():
    repo = Path(__file__).resolve().parents[2]
    audit = build_item_lighting_interaction_audit(repo)

    assert audit.story_id == "RE-149"
    assert audit.upstream_ticket == "RE-148"
    assert audit.domain_id == "module-game"
    assert audit.cluster == "item-lighting-interaction"
    assert audit.pivot == "DoFlameTorch"
    assert audit.next_ticket == "RE-150"
    assert audit.code_change_ready_count == 0
    assert audit.marker_ready_count == 0
    assert [row.function for row in audit.rows] == ["DoFlameTorch", "TriggerAlertLight"]
    assert [row.implementation_status for row in audit.rows] == ["unimplemented-stub", "unimplemented-stub"]
    assert audit.rows[0].interaction_family == "torch-item-state"
    assert audit.rows[1].interaction_family == "alert-light-state"
    assert all(row.code_change_ready == "no" and row.marker_ready == "no" for row in audit.rows)
    assert [plan.story_id for plan in audit.ticket_plan] == [
        "RE-150",
        "RE-151",
        "RE-152",
        "RE-153",
        "RE-154",
        "RE-155",
        "RE-156",
    ]


def test_re149_outputs_metadata_only_artifacts_and_progress_tracker(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_item_lighting_interaction_audit(repo)
    written = write_all_artifacts(audit, tmp_path)

    audit_rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(audit_rows) == 2
    assert audit_rows[0]["function"] == "DoFlameTorch"
    assert audit_rows[0]["cluster"] == "item-lighting-interaction"
    assert audit_rows[0]["role"] == "pivot-item-lighting-interaction"
    assert audit_rows[0]["next_probe"].startswith("RE-150")

    cluster_rows = list(csv.DictReader(written["clusters_csv"].open(newline="", encoding="utf-8")))
    assert cluster_rows == [{
        "cluster": "item-lighting-interaction",
        "candidate_count": "2",
        "top_function": "DoFlameTorch",
        "representative_functions": "DoFlameTorch;TriggerAlertLight",
        "interaction_family": "item-lighting-state",
        "readiness": "best-next-module-game-cluster",
        "blocker": "Item lighting interaction state contract and symbolic equivalence proof missing",
        "recommended_next_ticket": "RE-150",
    }]

    plan_rows = list(csv.DictReader(written["ticket_plan_csv"].open(newline="", encoding="utf-8")))
    assert [row["story_id"] for row in plan_rows] == ["RE-150", "RE-151", "RE-152", "RE-153", "RE-154", "RE-155", "RE-156"]
    assert "caller" in plan_rows[0]["topic"]
    assert "closure" in plan_rows[-1]["topic"]

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-148 object-interaction handoff consumed" in story_text
    assert "RE-061 item-lighting-interaction rows selected" in story_text
    assert "DoFlameTorch item-lighting pivot selected" in story_text
    assert "RE-150..RE-156 ticket plan emitted" in story_text
    assert "test_re149_item_lighting_interaction_audit.py" in story_text
    assert "object-interaction" not in story_text.lower().replace("re-148 object-interaction handoff consumed", "")
    assert "gameplay-mixed" not in story_text.lower()
    assert "re142" not in story_text.lower()

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "raw call target" not in text
        assert "machine word" not in text
        assert "0x" not in text
