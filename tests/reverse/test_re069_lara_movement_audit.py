from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.re069_lara_movement_audit import (
    build_lara_movement_audit,
    write_all_artifacts,
)


def test_re069_selects_lara_movement_from_re068_handoff():
    audit = build_lara_movement_audit(ROOT)

    assert audit.story_id == "RE-069"
    assert audit.domain_id == "module-game"
    assert audit.cluster == "lara-movement-support"
    assert audit.status == "lara-movement-proof-first-audit-published"
    assert audit.depends_on == ("RE-068", "RE-061")
    assert audit.pivot_function == "TestLaraSlide"
    assert audit.decision == "lara-movement-cluster-scoped-for-proof-chain"
    assert audit.code_change_readiness == "blocked"
    assert audit.next_ticket == "RE-070"
    assert audit.summary.candidate_count >= 10
    assert audit.summary.source_backed_count >= 10
    assert audit.summary.patch_ready_count == 0
    assert audit.summary.marker_ready_count == 0

    names = {row.function: row for row in audit.candidates}
    assert "TestLaraSlide" in names
    assert "TestLaraVault" in names
    assert "CreateFlare" in names
    assert "LaraHangRightCornerTest" in names
    assert "LaraHangLeftCornerTest" in names
    assert names["TestLaraSlide"].role == "pivot"
    assert names["TestLaraSlide"].readiness == "proof-first-audit-needed"
    assert names["CreateFlare"].subcluster == "flare-movement-support"
    assert {row.function for row in audit.candidates}.isdisjoint({"if", "for", "while", "switch"})

    assert tuple(ticket.story_id for ticket in audit.ticket_plan) == (
        "RE-070",
        "RE-071",
        "RE-072",
        "RE-073",
        "RE-074",
        "RE-075",
        "RE-076",
    )
    assert audit.ticket_plan[0].topic == "lara-movement-caller-side-effect-map"
    assert audit.ticket_plan[-1].topic == "lara-movement-closure-or-handoff"
    assert {ticket.code_change_readiness for ticket in audit.ticket_plan} == {"blocked-until-proof"}


def test_re069_outputs_metadata_only_story_report_and_csv(tmp_path):
    audit = build_lara_movement_audit(ROOT)
    written = write_all_artifacts(audit, tmp_path)

    assert written["audit_csv"].name == "re069-lara-movement-proof-first-audit.csv"
    assert written["subcluster_csv"].name == "re069-lara-movement-subclusters.csv"
    assert written["plan_csv"].name == "re069-lara-movement-ticket-plan.csv"
    assert written["md"].name == "re069-lara-movement-proof-first-audit.md"
    assert written["story"].name == "RE-069-lara-movement-proof-first-audit.md"

    audit_csv = written["audit_csv"].read_text(encoding="utf-8")
    subcluster_csv = written["subcluster_csv"].read_text(encoding="utf-8")
    plan_csv = written["plan_csv"].read_text(encoding="utf-8")
    md_text = written["md"].read_text(encoding="utf-8")
    story_text = written["story"].read_text(encoding="utf-8")

    assert "function,file,line,status,markers,bucket,score" in audit_csv
    assert "TestLaraSlide,GAME/LARA.C" in audit_csv
    assert "subcluster,candidate_count" in subcluster_csv
    assert "ledge-and-vault-tests" in subcluster_csv
    assert "story_id,topic,goal,scope,code_change_readiness,exit_condition" in plan_csv
    assert "RE-070,lara-movement-caller-side-effect-map" in plan_csv
    assert "RE-076,lara-movement-closure-or-handoff" in plan_csv
    assert "# RE-069 — Lara movement proof-first audit" in md_text
    assert "## Progress tracker" in story_text
    assert "- [x] RE-068 handoff consumed." in story_text
    assert "code change readiness: `blocked`" in story_text

    forbidden_fragments = ("0x", "payload", "opcode", "machine word", "raw call target")
    for text in (audit_csv, subcluster_csv, plan_csv, md_text, story_text):
        lowered = text.lower()
        assert not any(fragment in lowered for fragment in forbidden_fragments)
