from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.re077_gameflow_runtime_audit import (
    build_gameflow_runtime_audit,
    write_all_artifacts,
)


def test_re077_selects_gameflow_runtime_from_re076_handoff():
    audit = build_gameflow_runtime_audit(ROOT)

    assert audit.story_id == "RE-077"
    assert audit.domain_id == "module-game"
    assert audit.cluster == "gameflow-runtime-control"
    assert audit.status == "gameflow-runtime-proof-first-audit-published"
    assert audit.depends_on == ("RE-076", "RE-061")
    assert audit.pivot_function == "DoTitle"
    assert audit.decision == "gameflow-runtime-cluster-scoped-for-proof-chain"
    assert audit.code_change_readiness == "blocked"
    assert audit.next_ticket == "RE-078"
    assert audit.summary.candidate_count == 12
    assert audit.summary.nd_count == 2
    assert audit.summary.runtime_count == 3
    assert audit.summary.patch_ready_count == 0
    assert audit.summary.marker_ready_count == 0

    names = {row.function: row for row in audit.candidates}
    assert names["DoTitle"].role == "pivot-nd-marker-target"
    assert names["QuickControlPhase"].subcluster == "title-and-control-phase"
    assert names["DoGameflow"].subcluster == "title-and-control-phase"
    assert names["LaraControl"].subcluster == "lara-runtime-control"
    assert names["FlameTorchControl"].subcluster == "object-runtime-control"
    assert {row.function for row in audit.candidates}.isdisjoint({"if", "for", "while", "switch"})

    assert tuple(ticket.story_id for ticket in audit.ticket_plan) == (
        "RE-078",
        "RE-079",
        "RE-080",
        "RE-081",
        "RE-082",
        "RE-083",
        "RE-084",
    )
    assert audit.ticket_plan[0].topic == "gameflow-runtime-caller-side-effect-map"
    assert audit.ticket_plan[-1].topic == "gameflow-runtime-closure-or-handoff"
    assert {ticket.code_change_readiness for ticket in audit.ticket_plan} == {"blocked-until-proof"}


def test_re077_outputs_metadata_only_story_report_and_csv(tmp_path):
    audit = build_gameflow_runtime_audit(ROOT)
    written = write_all_artifacts(audit, tmp_path)

    assert written["audit_csv"].name == "re077-gameflow-runtime-proof-first-audit.csv"
    assert written["subcluster_csv"].name == "re077-gameflow-runtime-subclusters.csv"
    assert written["plan_csv"].name == "re077-gameflow-runtime-ticket-plan.csv"
    assert written["md"].name == "re077-gameflow-runtime-proof-first-audit.md"
    assert written["story"].name == "RE-077-gameflow-runtime-proof-first-audit.md"

    audit_csv = written["audit_csv"].read_text(encoding="utf-8")
    subcluster_csv = written["subcluster_csv"].read_text(encoding="utf-8")
    plan_csv = written["plan_csv"].read_text(encoding="utf-8")
    md_text = written["md"].read_text(encoding="utf-8")
    story_text = written["story"].read_text(encoding="utf-8")

    assert "function,file,line,status,markers,bucket,score" in audit_csv
    assert "DoTitle,GAME/GAMEFLOW.C" in audit_csv
    assert "subcluster,candidate_count" in subcluster_csv
    assert "title-and-control-phase" in subcluster_csv
    assert "story_id,topic,goal,scope,code_change_readiness,exit_condition" in plan_csv
    assert "RE-078,gameflow-runtime-caller-side-effect-map" in plan_csv
    assert "RE-084,gameflow-runtime-closure-or-handoff" in plan_csv
    assert "# RE-077 — Gameflow runtime proof-first audit" in md_text
    assert "## Progress tracker" in story_text
    assert "- [x] RE-076 handoff consumed." in story_text
    assert "code change readiness: `blocked`" in story_text

    forbidden_fragments = ("0x", "payload", "opcode", "machine word", "raw call target")
    for text in (audit_csv, subcluster_csv, plan_csv, md_text, story_text):
        lowered = text.lower()
        assert not any(fragment in lowered for fragment in forbidden_fragments)
