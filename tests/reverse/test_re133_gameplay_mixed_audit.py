from pathlib import Path
import csv

from scripts.reverse.re133_gameplay_mixed_audit import build_gameplay_mixed_audit, write_all_artifacts


def test_re133_consumes_re132_exhaustion_and_opens_gameplay_mixed():
    repo = Path(__file__).resolve().parents[2]
    audit = build_gameplay_mixed_audit(repo)

    assert audit.story_id == "RE-133"
    assert audit.upstream_ticket == "RE-132"
    assert audit.domain_id == "module-game"
    assert audit.cluster == "gameplay-mixed"
    assert audit.pivot == "Load_and_Init_Cutseq"
    assert audit.next_ticket == "RE-134"
    assert audit.code_change_ready_count == 0
    assert audit.marker_ready_count == 0
    assert [row.function for row in audit.rows][:5] == [
        "Load_and_Init_Cutseq",
        "CreateZone",
        "special4_init",
        "init_water_table",
        "InitialiseSqrtTable",
    ]
    assert len(audit.rows) == 11
    assert audit.rows[0].implementation_status in {"implemented-source", "unimplemented-stub", "platform-gated-source"}
    assert audit.ticket_plan[0].story_id == "RE-134"
    assert audit.ticket_plan[-1].story_id == "RE-140"
    assert all(row.code_change_ready == "no" and row.marker_ready == "no" for row in audit.rows)


def test_re133_outputs_metadata_only_artifacts_and_progress_tracker(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_gameplay_mixed_audit(repo)
    written = write_all_artifacts(audit, tmp_path)

    audit_rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(audit_rows) == 11
    assert audit_rows[0]["function"] == "Load_and_Init_Cutseq"
    assert audit_rows[0]["cluster"] == "gameplay-mixed"
    assert audit_rows[0]["object_family"] == "gameplay-state"
    assert audit_rows[0]["next_probe"].startswith("RE-134")

    cluster_rows = list(csv.DictReader(written["clusters_csv"].open(newline="", encoding="utf-8")))
    assert cluster_rows == [{
        "cluster": "gameplay-mixed",
        "candidate_count": "11",
        "top_function": "Load_and_Init_Cutseq",
        "representative_functions": "Load_and_Init_Cutseq;CreateZone;special4_init;init_water_table;InitialiseSqrtTable;InitTarget;InitBinoculars;InitialiseFootPrints;LoadLevel;EscapeBox;InitPackNodes",
        "object_family": "gameplay-state",
        "readiness": "best-next-module-game-cluster",
        "blocker": "Gameplay mixed state contract and symbolic equivalence proof missing",
        "recommended_next_ticket": "RE-134",
    }]

    plan_rows = list(csv.DictReader(written["ticket_plan_csv"].open(newline="", encoding="utf-8")))
    assert [row["story_id"] for row in plan_rows] == ["RE-134", "RE-135", "RE-136", "RE-137", "RE-138", "RE-139", "RE-140"]
    assert "object-interaction" in plan_rows[-1]["goal"]

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-132 gameflow-runtime-control exhaustion consumed" in story_text
    assert "RE-061 gameplay-mixed rows selected" in story_text
    assert "RE-134..RE-140 ticket plan emitted" in story_text
    assert "test_re133_gameplay_mixed_audit.py" in story_text
    assert "runtime-support" not in story_text.lower()

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "raw call target" not in text
        assert "machine word" not in text
        assert "0x" not in text
