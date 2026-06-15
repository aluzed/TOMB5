from pathlib import Path
import csv

from scripts.reverse.re199_re205_platform_memory_epic import (
    EXPECTED_SCOPE,
    FORBIDDEN_FRAGMENTS,
    STALE_FRAGMENTS,
    build_platform_memory_epic,
    write_all_artifacts,
)


def test_re199_re205_consumes_re198_handoff_and_finishes_platform_memory():
    repo = Path(__file__).resolve().parents[2]
    epic = build_platform_memory_epic(repo)

    assert [ticket.story_id for ticket in epic.tickets] == [
        "RE-199",
        "RE-200",
        "RE-201",
        "RE-202",
        "RE-203",
        "RE-204",
        "RE-205",
    ]
    assert epic.domain_id == "module-spec_psxpc_n"
    assert epic.cluster == "platform-memory"
    assert epic.upstream_ticket == "RE-198"
    assert epic.pivot == "game_malloc"
    assert epic.status == "platform-memory-epic-closed-with-proof-blocker"
    assert epic.final_decision == "documentation-only-terminal-blocker"
    assert epic.code_change_ready_count == 0
    assert epic.marker_ready_count == 0
    assert epic.source_patch_ready_count == 0
    assert [row.function for row in epic.audit_rows] == list(EXPECTED_SCOPE)
    assert any(row.callee == "game_malloc" for row in epic.callsite_rows)
    assert any(row.callee == "init_game_malloc" for row in epic.callsite_rows)
    assert any(row.callee == "game_free" for row in epic.callsite_rows)
    assert all(row.caller not in {"if", "for", "while", "switch"} for row in epic.callsite_rows)
    assert all(row.caller_file != "SPEC_PSXPC_N/MALLOC.C" for row in epic.callsite_rows)
    assert all(row.line not in {44, 64} for row in epic.callsite_rows if row.callee == "game_malloc")
    assert any(
        row.caller == "ReadResidentData" and row.callee == "game_malloc" and row.caller_file == "GAME/SETUP.C" and row.line == 4851
        for row in epic.callsite_rows
    )
    assert {row.function for row in epic.taxonomy_rows} == set(EXPECTED_SCOPE)
    assert all(row.code_change_ready == "no" for row in epic.equivalence_rows)
    assert all(row.source_patch_allowed == "no" for row in epic.source_patch_rows)
    assert [row.cluster for row in epic.next_selection_rows] == ["platform-main-lifecycle"]
    assert [row.top_function for row in epic.next_selection_rows] == ["main"]
    assert epic.handoff.next_ticket == "RE-206"
    assert epic.handoff.next_topic == "platform-main-lifecycle-proof-first-audit"
    assert epic.handoff.selected_cluster == "platform-main-lifecycle"
    assert epic.handoff.selected_pivot == "main"


def test_re199_re205_outputs_metadata_only_artifacts_and_story_trackers(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    epic = build_platform_memory_epic(repo)
    written = write_all_artifacts(epic, tmp_path)

    plan = list(csv.DictReader(written["plan_csv"].open(newline="", encoding="utf-8")))
    assert [row["story_id"] for row in plan] == ["RE-200", "RE-201", "RE-202", "RE-203", "RE-204", "RE-205"]
    assert plan[-1]["topic"] == "module-spec-psxpc-n-post-platform-memory-next-cluster-selection"

    audit = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert [row["function"] for row in audit] == list(EXPECTED_SCOPE)
    assert audit[0]["role"] == "pivot"
    assert {row["marker_ready"] for row in audit} == {"no"}

    callsites = list(csv.DictReader(written["callsite_csv"].open(newline="", encoding="utf-8")))
    assert callsites
    assert all(row["source_line_text"] == "source-line-contains-callee-call" for row in callsites)
    assert all(int(row["line"]) > 0 for row in callsites)

    taxonomy = list(csv.DictReader(written["taxonomy_csv"].open(newline="", encoding="utf-8")))
    assert {row["argument_family"] for row in taxonomy} == {
        "arena-initialization",
        "arena-allocation",
        "arena-rewind-free",
    }

    equivalence = list(csv.DictReader(written["equivalence_csv"].open(newline="", encoding="utf-8")))
    assert len(equivalence) == len(EXPECTED_SCOPE)
    assert {row["equivalence_status"] for row in equivalence} == {"blocked-missing-non-raw-binary-equivalence-proof"}

    source_patch = list(csv.DictReader(written["source_patch_csv"].open(newline="", encoding="utf-8")))
    assert {row["source_patch_allowed"] for row in source_patch} == {"no"}
    assert {row["marker_change_allowed"] for row in source_patch} == {"no"}

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-206"
    assert handoff["selected_cluster"] == "platform-main-lifecycle"
    assert handoff["selected_pivot"] == "main"
    assert handoff["code_change_readiness"] == "blocked"

    story_text = written["RE-205"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-204 source-patch gate denied source and marker changes" in story_text
    assert "next ticket: `RE-206`" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "test_re199_re205_platform_memory_epic.py" in story_text

    md_text = written["md"].read_text(encoding="utf-8")
    assert "platform-memory-epic-closed-with-proof-blocker" in md_text
    assert "source-patch-ready rows: `0`" in md_text
    assert "platform-main-lifecycle" in md_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_FRAGMENTS + STALE_FRAGMENTS:
            assert fragment not in text
