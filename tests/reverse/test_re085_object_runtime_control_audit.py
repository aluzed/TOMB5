from pathlib import Path
import csv

from scripts.reverse.re085_object_runtime_control_audit import (
    build_object_runtime_control_audit,
    write_all_artifacts,
    C_KEYWORD_ARTIFACTS,
)


def test_re085_consumes_re084_handoff_and_selects_object_runtime_control():
    repo = Path(__file__).resolve().parents[2]
    audit = build_object_runtime_control_audit(repo)

    assert audit.story_id == "RE-085"
    assert audit.domain_id == "module-game"
    assert audit.cluster == "gameflow-runtime-control"
    assert audit.subcluster == "object-runtime-control"
    assert audit.pivot_function == "FlameTorchControl"
    assert audit.depends_on == ("RE-077", "RE-078..RE-084")
    assert audit.summary.candidate_count == 5
    assert audit.summary.nd_count == 0
    assert audit.summary.patch_ready_count == 0
    assert audit.summary.marker_ready_count == 0
    assert audit.code_change_readiness == "blocked"
    assert audit.next_ticket == "RE-086"
    assert [row.function for row in audit.candidates] == [
        "FlameTorchControl",
        "SearchObjectControl",
        "ControlElectricalLight",
        "FlareControl",
        "ControlStrobeLight",
    ]
    assert {row.subcluster for row in audit.candidates} == {
        "torch-and-flare-control",
        "pickup-search-control",
        "dynamic-light-control",
    }
    assert not ({row.function for row in audit.candidates} & C_KEYWORD_ARTIFACTS)


def test_re085_outputs_metadata_only_story_report_and_plan(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_object_runtime_control_audit(repo)
    written = write_all_artifacts(audit, tmp_path)

    assert written["audit_csv"].name == "re085-object-runtime-control-proof-first-audit.csv"
    assert written["subcluster_csv"].name == "re085-object-runtime-control-subclusters.csv"
    assert written["plan_csv"].name == "re085-object-runtime-control-ticket-plan.csv"
    assert written["md"].name == "re085-object-runtime-control-proof-first-audit.md"
    assert written["story"].name == "RE-085-object-runtime-control-proof-first-audit.md"

    with written["plan_csv"].open(newline="", encoding="utf-8") as f:
        plan_rows = list(csv.DictReader(f))
    assert [row["story_id"] for row in plan_rows] == [
        "RE-086",
        "RE-087",
        "RE-088",
        "RE-089",
        "RE-090",
        "RE-091",
        "RE-092",
    ]
    assert all(row["code_change_readiness"] == "blocked-until-proof" for row in plan_rows)

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "- [x] RE-084 handoff consumed." in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "next ticket: `RE-086`" in story_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "machine word" not in text
        assert "raw call target" not in text
        assert "0x" not in text
