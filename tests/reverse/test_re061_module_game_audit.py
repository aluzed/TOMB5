from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.re061_module_game_audit import (
    build_module_game_audit,
    write_all_artifacts,
)


def test_re061_builds_module_game_proof_first_audit_from_re044_handoff():
    audit = build_module_game_audit(ROOT)

    assert audit.story_id == "RE-061"
    assert audit.domain_id == "module-game"
    assert audit.pivot_function == "ShatterObject"
    assert audit.depends_on == ("RE-060", "RE-044")
    assert audit.status == "module-game-proof-first-audit-published"
    assert audit.decision == "module-game-domain-scoped-for-proof-chain"
    assert audit.code_change_readiness == "blocked"
    assert audit.next_ticket == "RE-062"
    assert tuple(ticket.story_id for ticket in audit.ticket_plan) == (
        "RE-062",
        "RE-063",
        "RE-064",
        "RE-065",
        "RE-066",
        "RE-067",
        "RE-068",
    )
    assert audit.ticket_plan[0].topic == "debris-object-breakage-caller-side-effect-map"
    assert audit.ticket_plan[-1].topic == "module-game-closure-or-next-cluster-handoff"
    assert {ticket.code_change_readiness for ticket in audit.ticket_plan} == {"blocked-until-proof"}

    assert audit.summary.candidate_count >= 50
    assert audit.summary.mapped_count >= 50
    assert audit.summary.nd_count == 3
    assert audit.summary.runtime_count >= 10
    assert audit.summary.patch_ready_count == 0
    assert audit.summary.marker_ready_count == 0
    assert audit.summary.selected_cluster == "debris-object-breakage"

    assert audit.progress == (
        "re060-handoff-loaded",
        "re044-module-game-row-consumed",
        "module-game-candidates-classified",
        "proof-first-blockers-recorded",
        "forbidden-raw-evidence-excluded",
    )

    functions = {candidate.function: candidate for candidate in audit.candidates}
    assert "ShatterObject" in functions
    assert functions["ShatterObject"].cluster == "debris-object-breakage"
    assert functions["ShatterObject"].readiness == "proof-first-audit-needed"
    assert functions["ShatterObject"].code_change_ready == "no"
    assert {candidate.function for candidate in audit.candidates}.isdisjoint(
        {"if", "for", "while", "switch"}
    )

    clusters = {cluster.cluster: cluster for cluster in audit.clusters}
    assert "debris-object-breakage" in clusters
    assert clusters["debris-object-breakage"].candidate_count >= 1
    assert clusters["debris-object-breakage"].readiness == "best-initial-proof-cluster"


def test_re061_outputs_metadata_only_story_report_and_csv(tmp_path):
    audit = build_module_game_audit(ROOT)
    written = write_all_artifacts(audit, tmp_path)

    assert written["audit_csv"].name == "re061-module-game-proof-first-audit.csv"
    assert written["cluster_csv"].name == "re061-module-game-clusters.csv"
    assert written["plan_csv"].name == "re061-module-game-ticket-plan.csv"
    assert written["md"].name == "re061-module-game-proof-first-audit.md"
    assert written["story"].name == "RE-061-module-game-proof-first-audit.md"

    audit_csv = written["audit_csv"].read_text(encoding="utf-8")
    cluster_csv = written["cluster_csv"].read_text(encoding="utf-8")
    plan_csv = written["plan_csv"].read_text(encoding="utf-8")
    md_text = written["md"].read_text(encoding="utf-8")
    story_text = written["story"].read_text(encoding="utf-8")

    assert "function,file,line,status,markers,bucket,score" in audit_csv
    assert "ShatterObject,GAME/DEBRIS.C" in audit_csv
    assert "cluster,candidate_count,mapped_count" in cluster_csv
    assert "debris-object-breakage" in cluster_csv
    assert "story_id,topic,goal,scope,code_change_readiness,exit_condition" in plan_csv
    assert "RE-062,debris-object-breakage-caller-side-effect-map" in plan_csv
    assert "RE-068,module-game-closure-or-next-cluster-handoff" in plan_csv
    assert "# RE-061 — Module-game proof-first audit" in md_text
    assert "## Multi-ticket plan" in md_text
    for story_id in ("RE-062", "RE-063", "RE-064", "RE-065", "RE-066", "RE-067", "RE-068"):
        assert f"`{story_id}`" in md_text
        assert f"`{story_id}`" in story_text
    assert "Selected initial cluster: `debris-object-breakage`" in md_text
    assert "code-change-ready candidates: `0`" in md_text
    assert "marker-ready candidates: `0`" in md_text
    assert "Recommended next ticket: `RE-062`" in md_text

    assert "Status: Done" in story_text
    assert "## Progress" in story_text
    assert "- [x] RE-060 handoff loaded." in story_text
    assert "## Readiness decision" in story_text
    assert "code change readiness: `blocked`" in story_text

    forbidden = (
        "word_" + "le_hex",
        "payload_" + "offset",
        "dump" + " row",
        "jal " + "0x",
        "call_" + "address",
        "0x" + "800",
    )
    for text in (audit_csv, cluster_csv, plan_csv, md_text, story_text):
        for token in forbidden:
            assert token not in text
