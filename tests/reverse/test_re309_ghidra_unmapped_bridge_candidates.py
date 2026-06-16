from pathlib import Path
import csv

from scripts.reverse.re309_ghidra_unmapped_bridge_candidates import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_ghidra_unmapped_bridge_candidates,
    write_all_artifacts,
)


def test_re309_builds_safe_ghidra_bridge_candidates_without_raw_targets():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_ghidra_unmapped_bridge_candidates(repo)

    assert bundle.summary.story_id == "RE-309"
    assert bundle.summary.topic == "ghidra-unmapped-bridge-candidates"
    assert bundle.summary.upstream_handoff == "RE-308"
    assert bundle.summary.ghidra_function_count == 1440
    assert bundle.summary.ghidra_only_function_count == 723
    assert bundle.summary.bridge_candidate_count == 317
    assert bundle.summary.testable_now_count == 25
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.next_ticket == "RE-310"
    assert bundle.summary.next_topic == "ghidra-bridge-candidate-readiness-gate"
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.rows) == 25
    assert bundle.rows == sorted(bundle.rows, key=lambda row: (row.rank, row.candidate_id))
    top = bundle.rows[0]
    assert top.bridge_class == "mapped-caller-heavy"
    assert top.actionability == "testable-now"
    assert top.mapped_caller_count >= 50
    assert top.safe_source_context
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.rows)

    for row in bundle.rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "0x" not in row_text


def test_re309_writes_metadata_only_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_ghidra_unmapped_bridge_candidates(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"candidates_csv", "summary_csv", "handoff_csv", "md", "story"}

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert len(candidates) == 25
    assert candidates[0]["bridge_class"] == "mapped-caller-heavy"
    assert candidates[0]["actionability"] == "testable-now"
    assert "ghidra_entry" not in candidates[0]
    assert "ghidra_name" not in candidates[0]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-310"
    assert handoff["next_topic"] == "ghidra-bridge-candidate-readiness-gate"
    assert handoff["metadata_work_readiness"] == "ready"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] Ghidra function export consumed as source-symbolic metadata." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-310" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-309 Ghidra unmapped bridge candidates" in md
    assert "No raw Ghidra function names or entry addresses are emitted" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
