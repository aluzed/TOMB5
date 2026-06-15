from pathlib import Path
import csv

from scripts.reverse.re214_maths_render_support_audit import (
    EXPECTED_SCOPE,
    FORBIDDEN,
    STALE_FRAGMENTS,
    build_audit,
    write_all_artifacts,
)


def test_re214_consumes_re213_handoff_and_opens_maths_render_support_audit():
    repo = Path(__file__).resolve().parents[2]
    audit = build_audit(repo)

    assert audit.story_id == "RE-214"
    assert audit.upstream_ticket == "RE-213"
    assert audit.domain_id == "maths-render-support"
    assert audit.pivot == "mTranslateXYZ"
    assert audit.status == "maths-render-support-proof-first-audit-ready"
    assert audit.code_change_readiness == "blocked"
    assert audit.marker_readiness == "blocked"
    assert audit.next_ticket == "RE-215"
    assert audit.next_topic == "maths-render-support-matrix-transform-chain"

    assert audit.candidate_count == 92
    assert audit.mapped_count == 92
    assert audit.nd_count == 4
    assert audit.runtime_count == 0
    assert [row.function for row in audit.scope_rows[:5]] == list(EXPECTED_SCOPE)
    assert audit.scope_rows[0].function == "mTranslateXYZ"
    assert audit.scope_rows[0].file == "SPEC_PSXPC_N/MATHS.C"
    assert audit.scope_rows[0].subcluster == "matrix-transform-core"
    assert {row.subcluster for row in audit.cluster_rows} == {
        "matrix-transform-core",
        "gpu-scene-support",
        "object-draw-support",
        "draw-phase-support",
    }
    matrix = next(row for row in audit.cluster_rows if row.subcluster == "matrix-transform-core")
    assert matrix.candidate_count == 37
    assert matrix.top_function == "mTranslateXYZ"
    assert matrix.next_ticket == "RE-215"
    assert all(row.code_change_ready == "no" for row in audit.scope_rows)
    assert all(row.marker_ready == "no" for row in audit.scope_rows)


def test_re214_outputs_metadata_only_artifacts_plan_and_progress_tracker(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_audit(repo)
    written = write_all_artifacts(audit, tmp_path)

    assert written["audit_csv"].name == "re214-maths-render-support-proof-first-audit.csv"
    assert written["clusters_csv"].name == "re214-maths-render-support-clusters.csv"
    assert written["plan_csv"].name == "re214-maths-render-support-ticket-plan.csv"
    assert written["handoff_csv"].name == "re214-maths-render-support-handoff.csv"

    rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == 92
    assert rows[0]["function"] == "mTranslateXYZ"
    assert rows[0]["file"] == "SPEC_PSXPC_N/MATHS.C"
    assert rows[0]["proof_status"] == "source-priority-metadata-only"
    assert {row["code_change_ready"] for row in rows} == {"no"}

    clusters = list(csv.DictReader(written["clusters_csv"].open(newline="", encoding="utf-8")))
    assert [row["subcluster"] for row in clusters] == [
        "matrix-transform-core",
        "gpu-scene-support",
        "object-draw-support",
        "draw-phase-support",
    ]
    assert clusters[0]["next_ticket"] == "RE-215"

    plan = list(csv.DictReader(written["plan_csv"].open(newline="", encoding="utf-8")))
    assert [row["story_id"] for row in plan] == ["RE-215", "RE-216", "RE-217", "RE-218", "RE-219", "RE-220", "RE-221"]
    assert plan[0]["topic"] == "maths-render-support-matrix-transform-chain"
    assert plan[-1]["topic"] == "post-maths-render-support-domain-selection"

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-215"
    assert handoff["next_topic"] == "maths-render-support-matrix-transform-chain"
    assert handoff["selected_subcluster"] == "matrix-transform-core"
    assert handoff["selected_pivot"] == "mTranslateXYZ"

    story_text = written["story"].read_text(encoding="utf-8")
    assert "# RE-214 — maths-render-support proof-first audit" in story_text
    assert "## Progress tracker" in story_text
    assert "RE-213 handoff consumed" in story_text
    assert "Recommended next ticket: `RE-215`" in story_text
    assert "No production source or marker change is authorized" in story_text

    md_text = written["md"].read_text(encoding="utf-8")
    assert "Selected subcluster: `matrix-transform-core`" in md_text
    assert "Selected pivot: `mTranslateXYZ`" in md_text
    assert "candidate count: `92`" in md_text
    assert "RE-215" in md_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN + STALE_FRAGMENTS:
            assert fragment not in text
