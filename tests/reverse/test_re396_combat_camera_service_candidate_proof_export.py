from pathlib import Path
import csv

from scripts.reverse.re396_combat_camera_service_candidate_proof_export import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_combat_camera_service_candidate_proof_export,
    write_all_artifacts,
)


def test_re396_exports_candidate_scoped_combat_camera_context_without_proof():
    bundle = build_combat_camera_service_candidate_proof_export(Path(__file__).resolve().parents[2])
    assert bundle.summary.story_id == "RE-396"
    assert bundle.summary.upstream_handoff == "RE-395"
    assert bundle.summary.selected_candidate_id == "0aaa76206517"
    assert bundle.summary.source_symbol_context_count > 0
    assert bundle.summary.caller_context_count > 0
    assert bundle.summary.direct_repo_symbol_count == 0
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.next_ticket == "RE-397"
    assert bundle.summary.next_topic == "combat-camera-service-candidate-callsite-map"
    assert bundle.summary.code_change_readiness == "blocked"
    assert {row.candidate_level_proof for row in bundle.context_rows} == {"no"}


def test_re396_writes_metadata_only_artifacts_and_story(tmp_path):
    bundle = build_combat_camera_service_candidate_proof_export(Path(__file__).resolve().parents[2])
    written = write_all_artifacts(bundle, tmp_path)
    assert set(written) == {"contexts_csv", "proof_csv", "summary_csv", "handoff_csv", "md", "story"}
    contexts = list(csv.DictReader(written["contexts_csv"].open(newline="", encoding="utf-8")))
    assert contexts and {row["candidate_id"] for row in contexts} == {"0aaa76206517"}
    assert "ghidra_entry" not in contexts[0]
    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-397"
    assert handoff["code_change_readiness"] == "blocked"
    assert "## Progress tracker" in written["story"].read_text(encoding="utf-8")
    for path in written.values():
        text=path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS: assert fragment not in text
        assert "sub_" not in text
