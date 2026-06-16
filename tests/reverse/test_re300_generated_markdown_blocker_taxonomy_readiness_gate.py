from pathlib import Path
import csv

from scripts.reverse.re300_generated_markdown_blocker_taxonomy_readiness_gate import (
    FORBIDDEN,
    build_readiness_gate,
    write_all_artifacts,
)


def test_re300_gates_generated_markdown_taxonomy_without_reopening_domain_selection():
    repo = Path(__file__).resolve().parents[2]
    gate = build_readiness_gate(repo)

    assert gate.summary.story_id == "RE-300"
    assert gate.summary.upstream_handoff == "RE-299"
    assert gate.summary.generated_markdown_class_count == 7
    assert gate.summary.story_tracker_correlated_count == 7
    assert gate.summary.gate_row_count == 7
    assert gate.summary.ready_to_reopen_domain_count == 0
    assert gate.summary.needs_more_metadata_count == 7
    assert gate.summary.raw_or_asset_source_count == 0
    assert gate.summary.next_ticket == "RE-301"
    assert gate.summary.next_topic == "proof-audit-blocker-taxonomy-reduction"
    assert gate.summary.selected_domain == "none"
    assert gate.summary.selected_pivot == "none"
    assert gate.summary.metadata_work_readiness == "ready"
    assert gate.summary.code_change_readiness == "blocked"

    rows_by_class = {row.normalized_class: row for row in gate.rows}
    assert set(rows_by_class) == {
        "generic-blocker-reference",
        "domain-selection-still-blocked",
        "proof-or-marker-change-blocked",
        "source-or-code-readiness-blocked",
        "no-production-source-authorization",
        "metadata-work-readiness-only",
        "stop-condition-before-source-or-domain-work",
    }
    assert all(row.gate_decision == "needs-more-metadata" for row in gate.rows)
    assert all(row.ready_to_reopen_domain == "no" for row in gate.rows)
    assert all(row.source_patch_authorized == "no" for row in gate.rows)
    assert all(row.next_metadata_source == "proof-audits" for row in gate.rows)
    assert rows_by_class["proof-or-marker-change-blocked"].story_tracker_correlated == "partial"
    assert gate.rows == sorted(gate.rows, key=lambda row: (-row.evidence_count, row.normalized_class))


def test_re300_outputs_metadata_only_gate_story_and_handoff(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    gate = build_readiness_gate(repo)
    written = write_all_artifacts(gate, tmp_path)

    assert set(written) == {"gate_csv", "summary_csv", "handoff_csv", "md", "story"}

    rows = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == gate.summary.gate_row_count
    assert all(row["gate_decision"] == "needs-more-metadata" for row in rows)
    assert all(row["ready_to_reopen_domain"] == "no" for row in rows)
    assert all(row["source_patch_authorized"] == "no" for row in rows)
    assert all(row["next_metadata_source"] == "proof-audits" for row in rows)

    summary = list(csv.DictReader(written["summary_csv"].open(newline="", encoding="utf-8")))[0]
    assert summary["next_ticket"] == "RE-301"
    assert summary["next_topic"] == "proof-audit-blocker-taxonomy-reduction"
    assert summary["ready_to_reopen_domain_count"] == "0"
    assert summary["code_change_readiness"] == "blocked"

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["stop_condition"] == "reduce proof-audit blockers before proof-domain selection can reopen"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-300 generated-Markdown blocker taxonomy readiness gate" in md
    assert "## Gate decision" in md
    assert "proof-audit-blocker-taxonomy-reduction" in md
    assert "No production source or marker change is authorized" in md

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-299 generated-Markdown taxonomy handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-301" in story

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
