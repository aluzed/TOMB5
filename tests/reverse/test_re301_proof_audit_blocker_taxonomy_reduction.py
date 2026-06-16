from pathlib import Path
import csv

from scripts.reverse.re301_proof_audit_blocker_taxonomy_reduction import (
    FORBIDDEN,
    build_proof_audit_reduction,
    write_all_artifacts,
)


def test_re301_reduces_proof_audit_blockers_into_metadata_only_classes():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_proof_audit_reduction(repo)

    assert bundle.summary.story_id == "RE-301"
    assert bundle.summary.upstream_handoff == "RE-300"
    assert bundle.summary.proof_csv_file_count == 34
    assert bundle.summary.evidence_row_count == 384
    assert bundle.summary.normalized_class_count == 8
    assert bundle.summary.metadata_reduction_ready_count == 8
    assert bundle.summary.domain_selection_ready_count == 0
    assert bundle.summary.raw_or_asset_source_count == 0
    assert bundle.summary.next_ticket == "RE-302"
    assert bundle.summary.next_topic == "proof-audit-blocker-taxonomy-readiness-gate"
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.code_change_readiness == "blocked"

    rows_by_class = {row.normalized_class: row for row in bundle.rows}
    assert {name: row.evidence_count for name, row in rows_by_class.items()} == {
        "source-contract-and-non-raw-equivalence-missing": 164,
        "backlog-context-not-selected": 82,
        "proof-evidence-missing": 70,
        "state-contract-and-symbolic-equivalence-missing": 30,
        "generic-proof-audit-blocker": 23,
        "marker-behavior-proof-needed": 13,
        "non-raw-equivalence-proof-missing": 1,
        "symbolic-equivalence-proof-missing": 1,
    }
    assert all(row.metadata_reduction_ready == "yes" for row in bundle.rows)
    assert all(row.domain_selection_ready == "no" for row in bundle.rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.rows)
    assert bundle.rows == sorted(bundle.rows, key=lambda row: (-row.evidence_count, row.normalized_class))
    assert len(bundle.evidence_rows) == bundle.summary.evidence_row_count
    assert all(row.blocker_fingerprint and not hasattr(row, "blocker_text") for row in bundle.evidence_rows)


def test_re301_writes_metadata_only_outputs_and_handoff(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_proof_audit_reduction(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"taxonomy_csv", "evidence_csv", "summary_csv", "handoff_csv", "md", "story"}

    taxonomy = list(csv.DictReader(written["taxonomy_csv"].open(newline="", encoding="utf-8")))
    assert len(taxonomy) == 8
    assert "blocker_text" not in taxonomy[0]
    assert taxonomy[0]["normalized_class"] == "source-contract-and-non-raw-equivalence-missing"
    assert taxonomy[0]["evidence_count"] == "164"

    evidence = list(csv.DictReader(written["evidence_csv"].open(newline="", encoding="utf-8")))
    assert len(evidence) == 384
    assert set(evidence[0]) == {"proof_csv_file", "row_number", "normalized_class", "blocker_fingerprint"}

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-302"
    assert handoff["next_topic"] == "proof-audit-blocker-taxonomy-readiness-gate"
    assert handoff["stop_condition"] == "gate proof-audit taxonomy before proof-domain selection can reopen"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-300 proof-audit handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-302" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-301 proof-audit blocker taxonomy reduction" in md
    assert "source-contract-and-non-raw-equivalence-missing" in md
    assert "No production source or marker change is authorized" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
