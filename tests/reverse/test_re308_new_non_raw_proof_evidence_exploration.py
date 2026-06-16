from pathlib import Path
import csv

import pytest

from scripts.reverse.re308_new_non_raw_proof_evidence_exploration import (
    FORBIDDEN,
    build_new_non_raw_proof_evidence_exploration,
    validate_re307_handoff,
    write_all_artifacts,
)


def test_re308_explores_safe_evidence_inputs_without_reopening_domain():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_new_non_raw_proof_evidence_exploration(repo)

    assert bundle.summary.story_id == "RE-308"
    assert bundle.summary.topic == "new-non-raw-proof-evidence-exploration"
    assert bundle.summary.upstream_handoff == "RE-307"
    assert bundle.summary.exploration_vector_count == 6
    assert bundle.summary.testable_now_count == 0
    assert bundle.summary.needs_new_export_count == 2
    assert bundle.summary.exhausted_metadata_count == 2
    assert bundle.summary.unsafe_raw_only_count == 1
    assert bundle.summary.missing_user_input_count == 1
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.metadata_work_readiness == "blocked"
    assert bundle.summary.code_change_readiness == "blocked"
    assert bundle.summary.next_ticket == "TBD"
    assert bundle.summary.next_topic == "await-new-safe-evidence-input"

    rows_by_id = {row.vector_id: row for row in bundle.rows}
    assert list(rows_by_id) == [
        "changed-upstream-mapping",
        "new-user-supplied-proof-artifact",
        "safe-source-symbolic-export",
        "existing-generated-metadata",
        "existing-story-and-markdown-taxonomies",
        "raw-binary-or-asset-evidence",
    ]
    assert rows_by_id["changed-upstream-mapping"].actionability == "needs-new-export"
    assert rows_by_id["new-user-supplied-proof-artifact"].actionability == "missing-input"
    assert rows_by_id["safe-source-symbolic-export"].actionability == "needs-new-export"
    assert rows_by_id["existing-generated-metadata"].actionability == "exhausted-metadata"
    assert rows_by_id["existing-story-and-markdown-taxonomies"].actionability == "exhausted-metadata"
    assert rows_by_id["raw-binary-or-asset-evidence"].actionability == "unsafe-raw-only"
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.rows)


def test_re308_rejects_handoff_drift(tmp_path):
    handoff_dir = tmp_path / "docs/reverse/generated"
    handoff_dir.mkdir(parents=True)
    source = Path(__file__).resolve().parents[2] / "docs/reverse/generated/re307-blocker-reduction-source-exhaustion-audit-handoff.csv"
    rows = list(csv.DictReader(source.open(newline="", encoding="utf-8")))
    rows[0]["ready_to_reopen_domain_count"] = "1"
    with (handoff_dir / "re307-blocker-reduction-source-exhaustion-audit-handoff.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    with pytest.raises(ValueError, match="RE-307 handoff drift"):
        validate_re307_handoff(tmp_path)


def test_re308_writes_metadata_only_exploration_outputs(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_new_non_raw_proof_evidence_exploration(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"exploration_csv", "summary_csv", "handoff_csv", "md", "story"}

    exploration_rows = list(csv.DictReader(written["exploration_csv"].open(newline="", encoding="utf-8")))
    assert len(exploration_rows) == 6
    assert exploration_rows[0]["vector_id"] == "changed-upstream-mapping"
    assert exploration_rows[-1]["vector_id"] == "raw-binary-or-asset-evidence"
    assert "raw_evidence" not in exploration_rows[0]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "TBD"
    assert handoff["next_topic"] == "await-new-safe-evidence-input"
    assert handoff["selected_domain"] == "none"
    assert handoff["metadata_work_readiness"] == "blocked"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-307 exhaustion handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "changed-upstream-mapping-refresh" in story
    assert "new-safe-proof-evidence-intake" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-308 new non-raw proof evidence exploration" in md
    assert "No current vector is testable now" in md
    assert "No production source or marker change is authorized" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
