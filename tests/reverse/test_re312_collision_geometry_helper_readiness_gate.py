from pathlib import Path
import csv

from scripts.reverse.re312_collision_geometry_helper_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    build_collision_geometry_helper_readiness_gate,
    write_all_artifacts,
)


def test_re312_gates_collision_geometry_helper_without_reopening_domain():
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_geometry_helper_readiness_gate(repo)

    assert bundle.summary.story_id == "RE-312"
    assert bundle.summary.topic == "collision-geometry-helper-readiness-gate"
    assert bundle.summary.upstream_handoff == "RE-311"
    assert bundle.summary.selected_narrow_subcluster == "collision-geometry-helper"
    assert bundle.summary.input_candidate_count == 3
    assert bundle.summary.candidate_gate_count == 3
    assert bundle.summary.ready_to_reopen_domain_count == 0
    assert bundle.summary.source_patch_authorized_count == 0
    assert bundle.summary.selected_domain == "none"
    assert bundle.summary.selected_pivot == "none"
    assert bundle.summary.selected_followup_candidate_id == "5e99f39fd8ef"
    assert bundle.summary.next_ticket == "RE-313"
    assert bundle.summary.next_topic == "collision-geometry-helper-candidate-proof-export"
    assert bundle.summary.metadata_work_readiness == "ready"
    assert bundle.summary.code_change_readiness == "blocked"

    assert len(bundle.candidate_rows) == 3
    assert [row.rank for row in bundle.candidate_rows] == [1, 2, 3]
    assert [row.candidate_id for row in bundle.candidate_rows] == [
        "5e99f39fd8ef",
        "d96359c1d9f3",
        "61d55bb1809b",
    ]
    assert all(row.selected_narrow_subcluster == "collision-geometry-helper" for row in bundle.candidate_rows)
    assert all(row.readiness_gate == "blocked-needs-candidate-level-proof" for row in bundle.candidate_rows)
    assert all(row.ready_to_reopen_domain == "no" for row in bundle.candidate_rows)
    assert all(row.source_patch_authorized == "no" for row in bundle.candidate_rows)
    assert bundle.candidate_rows[0].next_probe == "candidate-proof-export"
    assert bundle.candidate_rows[1].next_probe == "defer-after-re313"
    assert bundle.candidate_rows[2].next_probe == "defer-after-re313"

    assert len(bundle.gate_rows) == 1
    gate = bundle.gate_rows[0]
    assert gate.gate_class == "candidate-level-source-symbolic-proof-missing"
    assert gate.candidate_count == 3
    assert gate.ready_to_reopen_domain == "no"
    assert gate.source_patch_authorized == "no"
    assert gate.next_ticket == "RE-313"
    assert gate.next_topic == "collision-geometry-helper-candidate-proof-export"

    for row in bundle.candidate_rows + bundle.gate_rows:
        row_text = ",".join(str(value) for value in row.__dict__.values()).lower()
        assert "fun_" not in row_text
        assert "0x" not in row_text


def test_re312_writes_metadata_only_readiness_gate_artifacts_and_story(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    bundle = build_collision_geometry_helper_readiness_gate(repo)
    written = write_all_artifacts(bundle, tmp_path)

    assert set(written) == {"candidates_csv", "gates_csv", "summary_csv", "handoff_csv", "md", "story"}

    candidates = list(csv.DictReader(written["candidates_csv"].open(newline="", encoding="utf-8")))
    assert len(candidates) == 3
    assert "ghidra_entry" not in candidates[0]
    assert "ghidra_name" not in candidates[0]
    assert candidates[0]["candidate_id"] == "5e99f39fd8ef"
    assert candidates[0]["readiness_gate"] == "blocked-needs-candidate-level-proof"
    assert candidates[0]["next_probe"] == "candidate-proof-export"

    gates = list(csv.DictReader(written["gates_csv"].open(newline="", encoding="utf-8")))
    assert gates == [
        {
            "rank": "1",
            "gate_class": "candidate-level-source-symbolic-proof-missing",
            "candidate_count": "3",
            "representative_candidates": "5e99f39fd8ef;d96359c1d9f3;61d55bb1809b",
            "gate_decision": "request-still-narrower-export",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_ticket": "RE-313",
            "next_topic": "collision-geometry-helper-candidate-proof-export",
            "stop_condition": "candidate-level source-symbolic proof is required before proof-domain selection",
        }
    ]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-313"
    assert handoff["next_topic"] == "collision-geometry-helper-candidate-proof-export"
    assert handoff["selected_followup_candidate_id"] == "5e99f39fd8ef"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"
    assert handoff["metadata_work_readiness"] == "ready"
    assert handoff["code_change_readiness"] == "blocked"

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-311 collision-geometry helper handoff validated." in story
    assert "## Follow-up ticket breakdown" in story
    assert "RE-313" in story

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-312 collision geometry helper readiness gate" in md
    assert "No proof-domain is reopened by this gate" in md

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            assert fragment not in text
