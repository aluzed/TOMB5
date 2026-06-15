from pathlib import Path
import csv

from scripts.reverse.re185_re191_frontend_loadsave_epic import (
    EXPECTED_SCOPE,
    FORBIDDEN_FRAGMENTS,
    STALE_FRAGMENTS,
    build_frontend_loadsave_epic,
    write_all_artifacts,
)


def test_re185_re191_consumes_re184_handoff_and_finishes_frontend_loadsave():
    repo = Path(__file__).resolve().parents[2]
    epic = build_frontend_loadsave_epic(repo)

    assert [ticket.story_id for ticket in epic.tickets] == [
        "RE-185",
        "RE-186",
        "RE-187",
        "RE-188",
        "RE-189",
        "RE-190",
        "RE-191",
    ]
    assert epic.domain_id == "module-spec_psxpc_n"
    assert epic.cluster == "frontend-loadsave"
    assert epic.upstream_ticket == "RE-184"
    assert epic.pivot == "SaveGame"
    assert epic.status == "frontend-loadsave-epic-closed-with-proof-blocker"
    assert epic.final_decision == "documentation-only-terminal-blocker"
    assert epic.code_change_ready_count == 0
    assert epic.marker_ready_count == 0
    assert epic.source_patch_ready_count == 0
    assert [row.function for row in epic.audit_rows] == list(EXPECTED_SCOPE)
    assert any(row.callee == "SaveGame" for row in epic.callsite_rows)
    assert any(row.callee == "DisplayFiles" for row in epic.callsite_rows)
    assert any(row.callee == "LoadGame" for row in epic.callsite_rows)
    assert all(row.caller not in {"if", "for", "while", "switch"} for row in epic.callsite_rows)
    assert {row.function for row in epic.taxonomy_rows} == set(EXPECTED_SCOPE)
    assert all(row.code_change_ready == "no" for row in epic.equivalence_rows)
    assert all(row.source_patch_allowed == "no" for row in epic.source_patch_rows)
    assert epic.handoff.next_ticket == "RE-192"
    assert epic.handoff.next_topic == "platform-gpu-display-proof-first-audit"
    assert epic.handoff.selected_cluster == "platform-gpu-display"
    assert epic.handoff.selected_pivot == "clear_a_rect"


def test_re185_re191_outputs_metadata_only_artifacts_and_story_trackers(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    epic = build_frontend_loadsave_epic(repo)
    written = write_all_artifacts(epic, tmp_path)

    plan = list(csv.DictReader(written["plan_csv"].open(newline="", encoding="utf-8")))
    assert [row["story_id"] for row in plan] == ["RE-186", "RE-187", "RE-188", "RE-189", "RE-190", "RE-191"]
    assert plan[-1]["topic"] == "module-spec-psxpc-n-post-frontend-loadsave-next-cluster-selection"

    audit = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert audit[0]["function"] == "SaveGame"
    assert audit[0]["role"] == "pivot"
    assert audit[1]["function"] == "DisplayFiles"
    assert audit[2]["function"] == "LoadGame"

    callsites = list(csv.DictReader(written["callsite_csv"].open(newline="", encoding="utf-8")))
    assert callsites
    assert all(row["source_line_text"] == "source-line-contains-callee-call" for row in callsites)
    assert all(int(row["line"]) > 0 for row in callsites)

    taxonomy = list(csv.DictReader(written["taxonomy_csv"].open(newline="", encoding="utf-8")))
    assert {row["argument_family"] for row in taxonomy} == {"savegame-menu-write", "savegame-file-list", "savegame-menu-read"}

    equivalence = list(csv.DictReader(written["equivalence_csv"].open(newline="", encoding="utf-8")))
    assert len(equivalence) == len(EXPECTED_SCOPE)
    assert {row["equivalence_status"] for row in equivalence} == {"blocked-missing-non-raw-binary-equivalence-proof"}

    source_patch = list(csv.DictReader(written["source_patch_csv"].open(newline="", encoding="utf-8")))
    assert {row["source_patch_allowed"] for row in source_patch} == {"no"}
    assert {row["marker_change_allowed"] for row in source_patch} == {"no"}

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-192"
    assert handoff["selected_cluster"] == "platform-gpu-display"
    assert handoff["selected_pivot"] == "clear_a_rect"
    assert handoff["code_change_readiness"] == "blocked"

    story_text = written["RE-191"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-190 source-patch gate denied source and marker changes" in story_text
    assert "next ticket: `RE-192`" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "test_re185_re191_frontend_loadsave_epic.py" in story_text

    md_text = written["md"].read_text(encoding="utf-8")
    assert "frontend-loadsave-epic-closed-with-proof-blocker" in md_text
    assert "source-patch-ready rows: `0`" in md_text
    assert "platform-gpu-display" in md_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_FRAGMENTS + STALE_FRAGMENTS:
            assert fragment not in text
