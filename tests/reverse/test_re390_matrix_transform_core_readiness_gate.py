from pathlib import Path
import csv

from scripts.reverse.re390_matrix_transform_core_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_matrix_transform_core_readiness_gate,
    write_all_artifacts,
)


def test_re390_gates_matrix_transform_core_without_reopening_domain():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_matrix_transform_core_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-390"
    assert bundle.summary.topic == "matrix-transform-core-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-389"
    assert bundle.summary.selected_narrow_subcluster == "matrix-transform-core"
    assert bundle.summary.input_candidate_count == 3
    assert bundle.summary.candidate_gate_count == 1
    assert bundle.summary.candidate_level_proof_count == 0
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.selected_followup_candidate_id == "none"
    assert bundle.summary.next_ticket == "RE-391"
    assert bundle.summary.next_topic == "post-maths-render-next-ghidra-cluster-selection"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert [row.candidate_id for row in bundle.candidate_rows] == [
        "cc1a1b589426",
        "6e9ad2da9fce",
        "95467f3600d5",
    ]
    assert [row.matrix_context_count for row in bundle.candidate_rows] == [3, 2, 4]
    assert {row.candidate_level_proof for row in bundle.candidate_rows} == {"no"}
    assert {row.ready_to_reopen_domain for row in bundle.candidate_rows} == {"no"}
    assert {row.source_patch_authorized for row in bundle.candidate_rows} == {"no"}
    assert {row.next_probe for row in bundle.candidate_rows} == {"close-matrix-transform-core-subcluster"}

    gate = bundle.gate_rows[0]
    assert gate.gate_class == "candidate-level-source-symbolic-proof-missing"
    assert gate.candidate_count == 3
    assert gate.representative_candidates == "cc1a1b589426;6e9ad2da9fce;95467f3600d5"
    assert gate.gate_decision == "close-subcluster-select-next-deferred-cluster"
    assert gate.ready_to_reopen_domain == "no"
    assert gate.source_patch_authorized == "no"
    assert gate.next_ticket == "RE-391"
    assert gate.next_topic == "post-maths-render-next-ghidra-cluster-selection"

    for row in bundle.candidate_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "sub_" not in row_text
        assert "0x" not in row_text


def test_re390_writes_metadata_only_readiness_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_matrix_transform_core_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"candidates_csv", "gates_csv", "summary_csv", "handoff_csv", "md", "story"}

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert len(candidates) == 3
    assert "ghidra_entry" not in candidates[0]
    assert "ghidra_name" not in candidates[0]
    assert candidates[0]["candidate_id"] == "cc1a1b589426"
    assert candidates[2]["candidate_id"] == "95467f3600d5"
    assert candidates[2]["matrix_context_count"] == "4"
    assert {row["readiness_gate"] for row in candidates} == {"blocked-no-candidate-level-proof"}
    assert {row["next_probe"] for row in candidates} == {"close-matrix-transform-core-subcluster"}

    gates = list(csv.DictReader(written["gates_csv"].open(newline="", encoding="utf-8")))
    assert gates == [
        {
            "rank": "1",
            "gate_class": "candidate-level-source-symbolic-proof-missing",
            "candidate_count": "3",
            "representative_candidates": "cc1a1b589426;6e9ad2da9fce;95467f3600d5",
            "candidate_level_proof_count": "0",
            "gate_decision": "close-subcluster-select-next-deferred-cluster",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-391",
            "next_topic": "post-maths-render-next-ghidra-cluster-selection",
            "stop_condition": "matrix transform core candidate queue exhausted without candidate-level proof",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-391"
    assert handoff["next_topic"] == "post-maths-render-next-ghidra-cluster-selection"
    assert handoff["selected_followup_candidate_id"] == "none"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["metadata_work_readiness"] == "ready"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-389 matrix-transform-core handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-391" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-390 matrix transform core readiness gate" in md
    assert "No proof-domain is reopened by this gate" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
        assert "sub_" not in text
