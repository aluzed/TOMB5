from pathlib import Path
import csv

from scripts.reverse.re283_re287_module_spec_pc_n_epic import (
    FORBIDDEN,
    STALE_FRAGMENTS,
    build_epic,
    write_all_artifacts,
)


def test_re283_re287_reconciles_module_spec_pc_n_parser_artifact_and_closes_domain():
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)

    assert epic.story_range == "RE-283..RE-287"
    assert epic.upstream_ticket == "RE-282"
    assert epic.domain_id == "module-spec_pc_n"
    assert epic.selected_pivot == "DecodeTrack"
    assert epic.raw_priority_count == 2
    assert epic.parser_artifact_count == 1
    assert epic.candidate_count == 1
    assert epic.closed_candidate_count == 1
    assert epic.runtime_count == 0
    assert epic.nd_count == 0
    assert epic.code_change_ready_count == 0
    assert epic.marker_ready_count == 0
    assert epic.domain_outcome == "documentation-only-terminal-blocker"
    assert epic.blocker == "missing-module-spec-pc-n-decodetrack-state-contract-and-non-raw-equivalence-proof"

    assert [row.function for row in epic.parser_artifact_rows] == ["if"]
    assert [row.function for row in epic.audit_rows] == ["DecodeTrack"]
    assert epic.audit_rows[0].file == "SPEC_PC_N/SPECIFIC.CPP"
    assert epic.audit_rows[0].line == 1934

    assert [row.story_id for row in epic.story_rows] == ["RE-283", "RE-284", "RE-285", "RE-286", "RE-287"]
    assert [row.topic for row in epic.story_rows] == [
        "module-spec-pc-n-parser-reconciliation",
        "module-spec-pc-n-decodetrack-audit",
        "module-spec-pc-n-state-equivalence-gate",
        "module-spec-pc-n-source-patch-gate",
        "post-module-spec-pc-n-exhaustion",
    ]

    assert epic.handoff.next_ticket == "TBD"
    assert epic.handoff.next_topic == "post-animation-items-domain-backlog-exhausted"
    assert epic.handoff.selected_domain == "none"
    assert epic.handoff.selected_pivot == "none"


def test_re283_re287_outputs_artifacts_stories_and_metadata_only(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    epic = build_epic(repo)
    written = write_all_artifacts(epic, tmp_path)

    assert set(written) == {
        "parser_artifacts_csv", "audit_csv", "epic_csv", "gate_csv", "handoff_csv", "md", "story_index", "stories",
    }
    assert len(written["stories"]) == 5

    parser_rows = list(csv.DictReader(written["parser_artifacts_csv"].open(newline="", encoding="utf-8")))
    assert len(parser_rows) == 1
    assert parser_rows[0]["function"] == "if"
    assert parser_rows[0]["classification"] == "parser-artifact"

    audit_rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert len(audit_rows) == 1
    assert audit_rows[0]["function"] == "DecodeTrack"
    assert audit_rows[0]["domain_id"] == "module-spec_pc_n"
    assert audit_rows[0]["readiness"] == "blocked"
    assert audit_rows[0]["source_patch_ready"] == "no"

    epic_rows = list(csv.DictReader(written["epic_csv"].open(newline="", encoding="utf-8")))
    assert epic_rows[0]["story_id"] == "RE-283"
    assert epic_rows[-1]["story_id"] == "RE-287"
    assert {row["readiness"] for row in epic_rows} == {"blocked"}

    gates = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    assert [row["gate"] for row in gates] == ["equivalence", "source-patch", "marker"]
    assert {row["decision"] for row in gates} == {"deny"}

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "TBD"
    assert handoff["selected_domain"] == "none"
    assert handoff["selected_pivot"] == "none"

    md_text = written["md"].read_text(encoding="utf-8")
    assert "# RE-283..RE-287 module-spec_pc_n epic" in md_text
    assert "Parser artifacts excluded: `1`" in md_text
    assert "Recommended next ticket: `TBD`" in md_text

    story_index = written["story_index"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_index
    assert "RE-283..RE-287" in story_index
    assert "No production source or marker change is authorized" in story_index

    for story_id, story_path in written["stories"].items():
        story = story_path.read_text(encoding="utf-8")
        assert f"# {story_id}" in story
        assert "## Progress tracker" in story
        assert "Readiness: `blocked`" in story
        assert "No production source or marker change is authorized" in story

    all_paths = [p for key, value in written.items() if key != "stories" for p in [value]] + list(written["stories"].values())
    for path in all_paths:
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN + STALE_FRAGMENTS:
            assert fragment not in text
