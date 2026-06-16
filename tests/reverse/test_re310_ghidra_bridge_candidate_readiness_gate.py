from pathlib import Path
import csv

from scripts.reverse.re310_ghidra_bridge_candidate_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_ghidra_bridge_candidate_readiness_gate,
    write_all_artifacts,
)


def test_re310_gates_re309_candidates_without_reopening_domain():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_ghidra_bridge_candidate_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-310"
    assert bundle.summary.topic == "ghidra-bridge-candidate-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-309"
    assert bundle.summary.input_candidate_count == 25
    assert bundle.summary.cluster_count == 7
    assert bundle.summary.focus_candidate_count == 7
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.selected_followup_cluster == "collision-switch-door-cluster"
    assert bundle.summary.next_ticket == "RE-311"
    assert bundle.summary.next_topic == "ghidra-collision-switch-door-cluster-narrow-export"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.cluster_rows) == 7
    assert [row.rank for row in bundle.cluster_rows] == list(range(1, 8))
    top = bundle.cluster_rows[0]
    assert top.cluster == "collision-switch-door-cluster"
    assert top.candidate_count == 7
    assert top.gate_decision == "needs-narrow-source-symbolic-export"
    assert top.ready_to_reopen_domain == "no"
    assert top.source_patch_authorized == "no"

    assert len(bundle.candidate_rows) == 25
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.candidate_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.candidate_rows)
    assert any(row.focus_cluster == "yes" for row in bundle.candidate_rows)

    for row in bundle.cluster_rows + bundle.candidate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "0x" not in row_text


def test_re310_writes_metadata_only_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_ghidra_bridge_candidate_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"clusters_csv", "candidates_csv", "summary_csv", "handoff_csv", "md", "story"}

    clusters = list(csv.DictReader(written["clusters_csv"].open(newline="", encoding="utf-8")))
    assert len(clusters) == 7
    assert clusters[0]["cluster"] == "collision-switch-door-cluster"
    assert clusters[0]["gate_decision"] == "needs-narrow-source-symbolic-export"
    assert clusters[0]["ready_to_reopen_domain"] == "no"

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-311"
    assert handoff["next_topic"] == "ghidra-collision-switch-door-cluster-narrow-export"
    assert handoff["selected_followup_cluster"] == "collision-switch-door-cluster"
    assert handoff["metadata_work_readiness"] == "ready"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-309 candidate export validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-311" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-310 Ghidra bridge candidate readiness gate" in md
    assert "No proof-domain is reopened by this gate" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
