from pathlib import Path
import csv

from scripts.reverse.re163_module_spec_psxpc_n_audit import (
    FORBIDDEN,
    build_module_spec_psxpc_n_audit,
    write_all_artifacts,
)


ROOT = Path(__file__).resolve().parents[2]


def test_re163_builds_module_spec_psxpc_n_proof_first_audit_from_re162():
    audit = build_module_spec_psxpc_n_audit(ROOT)

    assert audit.story_id == "RE-163"
    assert audit.domain_id == "module-spec_psxpc_n"
    assert audit.pivot_function == "PrintString"
    assert audit.depends_on == ("RE-162", "RE-044")
    assert audit.status == "module-spec-psxpc-n-proof-first-audit-published"
    assert audit.decision == "module-spec-psxpc-n-domain-scoped-for-proof-chain"
    assert audit.code_change_readiness == "blocked"
    assert audit.next_ticket == "RE-164"

    assert audit.summary.candidate_count == 27
    assert audit.summary.mapped_count == 27
    assert audit.summary.nd_count == 7
    assert audit.summary.runtime_count == 5
    assert audit.summary.patch_ready_count == 0
    assert audit.summary.marker_ready_count == 0
    assert audit.summary.selected_cluster == "ui-text-rendering"

    assert audit.progress == (
        "re162-selection-loaded",
        "re044-module-spec-psxpc-n-row-consumed",
        "module-spec-psxpc-n-candidates-classified",
        "proof-first-blockers-recorded",
        "forbidden-raw-evidence-excluded",
    )

    functions = {candidate.function: candidate for candidate in audit.candidates}
    assert "PrintString" in functions
    assert functions["PrintString"].cluster == "ui-text-rendering"
    assert functions["PrintString"].role == "pivot"
    assert functions["PrintString"].readiness == "proof-first-audit-needed"
    assert functions["PrintString"].code_change_ready == "no"
    assert functions["PrintString"].marker_ready == "no"
    assert {candidate.function for candidate in audit.candidates}.isdisjoint(
        {"if", "for", "while", "switch"}
    )

    clusters = {cluster.cluster: cluster for cluster in audit.clusters}
    assert clusters["ui-text-rendering"].readiness == "best-initial-proof-cluster"
    assert clusters["ui-text-rendering"].recommended_next_ticket == "RE-164"
    assert "platform-main-lifecycle" in clusters
    assert "platform-gpu-display" in clusters
    assert "platform-memory" in clusters

    assert tuple(ticket.story_id for ticket in audit.ticket_plan) == (
        "RE-164",
        "RE-165",
        "RE-166",
        "RE-167",
        "RE-168",
        "RE-169",
        "RE-170",
    )
    assert audit.ticket_plan[0].topic == "ui-text-rendering-caller-side-effect-map"
    assert audit.ticket_plan[-1].topic == "module-spec-psxpc-n-closure-or-handoff"
    assert {ticket.code_change_readiness for ticket in audit.ticket_plan} == {"blocked-until-proof"}


def test_re163_outputs_metadata_only_story_report_and_csv(tmp_path):
    audit = build_module_spec_psxpc_n_audit(ROOT)
    written = write_all_artifacts(audit, tmp_path)

    assert written["audit_csv"].name == "re163-module-spec-psxpc-n-proof-first-audit.csv"
    assert written["cluster_csv"].name == "re163-module-spec-psxpc-n-clusters.csv"
    assert written["plan_csv"].name == "re163-module-spec-psxpc-n-ticket-plan.csv"
    assert written["md"].name == "re163-module-spec-psxpc-n-proof-first-audit.md"
    assert written["story"].name == "RE-163-module-spec-psxpc-n-proof-first-audit.md"

    rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert rows[0]["function"] == "PrintString"
    assert rows[0]["file"] == "SPEC_PSXPC_N/TEXT_S.C"
    assert rows[0]["cluster"] == "ui-text-rendering"
    assert rows[0]["role"] == "pivot"
    assert rows[0]["code_change_ready"] == "no"
    assert rows[0]["marker_ready"] == "no"

    cluster_rows = list(csv.DictReader(written["cluster_csv"].open(newline="", encoding="utf-8")))
    assert cluster_rows[0]["cluster"] == "ui-text-rendering"
    assert cluster_rows[0]["recommended_next_ticket"] == "RE-164"

    plan_text = written["plan_csv"].read_text(encoding="utf-8")
    assert "RE-164,ui-text-rendering-caller-side-effect-map" in plan_text
    assert "RE-170,module-spec-psxpc-n-closure-or-handoff" in plan_text

    md_text = written["md"].read_text(encoding="utf-8")
    assert "# RE-163 — Module SPEC_PSXPC_N proof-first audit" in md_text
    assert "Selected initial cluster: `ui-text-rendering`" in md_text
    assert "code-change-ready candidates: `0`" in md_text
    assert "marker-ready candidates: `0`" in md_text
    assert "Recommended next ticket: `RE-164`" in md_text

    story_text = written["story"].read_text(encoding="utf-8")
    assert "Status: Done" in story_text
    assert "## Progress" in story_text
    assert "- [x] RE-162 selection loaded." in story_text
    assert "## Readiness decision" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "No production source or marker change is authorized" in story_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for token in FORBIDDEN:
            assert token not in text
