from pathlib import Path
import csv

from scripts.reverse.re157_ui_text_support_audit import (
    FORBIDDEN,
    build_ui_text_support_audit,
    write_all_artifacts,
)


def test_re157_consumes_re156_handoff_and_opens_ui_text_support():
    repo = Path(__file__).resolve().parents[2]
    audit = build_ui_text_support_audit(repo)

    assert audit.story_id == "RE-157"
    assert audit.upstream_ticket == "RE-156"
    assert audit.domain_id == "module-game"
    assert audit.cluster == "ui-text-support"
    assert audit.pivot == "InitFont"
    assert audit.next_ticket == "RE-158"
    assert audit.code_change_ready_count == 0
    assert audit.marker_ready_count == 0
    assert [row.function for row in audit.rows] == ["InitFont"]
    row = audit.rows[0]
    assert row.file == "GAME/TEXT.C"
    assert row.implementation_status == "implemented-source"
    assert row.marker_status == "D;F;ND"
    assert row.text_family == "font-shade-initialization"
    assert row.readiness == "nd-marker-proof-needed"
    assert row.code_change_ready == "no"
    assert row.marker_ready == "no"
    assert "behavior proof" in row.blocker
    assert [plan.story_id for plan in audit.ticket_plan] == ["RE-158", "RE-159", "RE-160", "RE-161"]


def test_re157_outputs_metadata_only_artifacts_and_progress_tracker(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    audit = build_ui_text_support_audit(repo)
    written = write_all_artifacts(audit, tmp_path)

    audit_rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(audit_rows) == 1
    assert audit_rows[0]["function"] == "InitFont"
    assert audit_rows[0]["cluster"] == "ui-text-support"
    assert audit_rows[0]["role"] == "pivot-ui-text-support"
    assert audit_rows[0]["marker_status"] == "D;F;ND"
    assert audit_rows[0]["next_probe"].startswith("RE-158")

    cluster_rows = list(csv.DictReader(written["clusters_csv"].open(newline="", encoding="utf-8")))
    assert cluster_rows == [{
        "cluster": "ui-text-support",
        "candidate_count": "1",
        "top_function": "InitFont",
        "representative_functions": "InitFont",
        "text_family": "font-shade-initialization",
        "readiness": "nd-marker-proof-needed",
        "blocker": "InitFont ND marker needs behavior proof before marker or source changes",
        "recommended_next_ticket": "RE-158",
    }]

    plan_rows = list(csv.DictReader(written["ticket_plan_csv"].open(newline="", encoding="utf-8")))
    assert [row["story_id"] for row in plan_rows] == ["RE-158", "RE-159", "RE-160", "RE-161"]
    assert "callers" in plan_rows[0]["goal"]
    assert "closure" in plan_rows[-1]["topic"]

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-156 item-lighting handoff consumed" in story_text
    assert "RE-061 ui-text-support row selected" in story_text
    assert "InitFont UI text pivot selected" in story_text
    assert "RE-158..RE-161 ticket plan emitted" in story_text
    assert "test_re157_ui_text_support_audit.py" in story_text
    assert "object-interaction" not in story_text.lower()
    assert "gameplay-mixed" not in story_text.lower()
    assert "re142" not in story_text.lower()

    md_text = written["md"].read_text(encoding="utf-8")
    assert "No production source or marker change is authorized" in md_text
    assert "font-shade-initialization" in md_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
