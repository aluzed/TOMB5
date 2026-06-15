from pathlib import Path
import csv

from scripts.reverse.re206_re212_platform_main_lifecycle_epic import (
    EXPECTED_SCOPE,
    FORBIDDEN_FRAGMENTS,
    STALE_FRAGMENTS,
    build_platform_main_lifecycle_epic,
    write_all_artifacts,
)


def test_re206_re212_consumes_re205_handoff_and_finishes_platform_main_lifecycle():
    repo = Path(__file__).resolve().parents[2]
    epic = build_platform_main_lifecycle_epic(repo)

    assert [ticket.story_id for ticket in epic.tickets] == [
        "RE-206",
        "RE-207",
        "RE-208",
        "RE-209",
        "RE-210",
        "RE-211",
        "RE-212",
    ]
    assert epic.domain_id == "module-spec_psxpc_n"
    assert epic.cluster == "platform-main-lifecycle"
    assert epic.upstream_ticket == "RE-205"
    assert epic.pivot == "main"
    assert epic.status == "platform-main-lifecycle-epic-closed-with-proof-blocker"
    assert epic.final_decision == "documentation-only-terminal-blocker"
    assert epic.code_change_ready_count == 0
    assert epic.marker_ready_count == 0
    assert epic.source_patch_ready_count == 0
    assert [row.function for row in epic.audit_rows] == list(EXPECTED_SCOPE)
    assert {row.function for row in epic.lifecycle_rows} == set(EXPECTED_SCOPE)
    assert any(row.function == "main" and "startup-sequence" in row.state_surface for row in epic.lifecycle_rows)
    assert any(row.function == "InitNewCDSystem" and "disc-index" in row.state_surface for row in epic.lifecycle_rows)
    assert any(row.function == "VSyncFunc" and "frame-counters" in row.state_surface for row in epic.lifecycle_rows)
    assert all(row.function not in {"if", "for", "while", "switch"} for row in epic.lifecycle_rows)
    assert all(row.source_file in {"SPEC_PSXPC_N/PSXMAIN.C", "SPEC_PSXPC_N/CD.C"} for row in epic.lifecycle_rows)
    assert {row.function for row in epic.taxonomy_rows} == set(EXPECTED_SCOPE)
    assert all(row.code_change_ready == "no" for row in epic.equivalence_rows)
    assert all(row.source_patch_allowed == "no" for row in epic.source_patch_rows)
    assert epic.next_selection_rows == ()
    assert epic.handoff.next_ticket == "TBD"
    assert epic.handoff.next_topic == "module-spec-psxpc-n-exhausted"
    assert epic.handoff.selected_cluster == "module-spec_psxpc_n"
    assert epic.handoff.selected_pivot == "all-clusters-proof-blocked-or-closed"


def test_re206_re212_outputs_metadata_only_artifacts_and_story_trackers(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    epic = build_platform_main_lifecycle_epic(repo)
    written = write_all_artifacts(epic, tmp_path)

    plan = list(csv.DictReader(written["plan_csv"].open(newline="", encoding="utf-8")))
    assert [row["story_id"] for row in plan] == ["RE-207", "RE-208", "RE-209", "RE-210", "RE-211", "RE-212"]
    assert plan[-1]["topic"] == "module-spec-psxpc-n-platform-main-lifecycle-exhaustion-handoff"

    audit = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert [row["function"] for row in audit] == list(EXPECTED_SCOPE)
    assert audit[0]["role"] == "pivot"
    assert {row["marker_ready"] for row in audit} == {"no"}

    lifecycle = list(csv.DictReader(written["lifecycle_csv"].open(newline="", encoding="utf-8")))
    assert [row["function"] for row in lifecycle] == list(EXPECTED_SCOPE)
    assert all(row["source_line_range"] != "raw-source-dump" for row in lifecycle)
    assert {row["proof_status"] for row in lifecycle} == {"source-lifecycle-surface-mapped-only"}

    taxonomy = list(csv.DictReader(written["taxonomy_csv"].open(newline="", encoding="utf-8")))
    assert {row["argument_family"] for row in taxonomy} == {
        "program-entrypoint",
        "disc-system-initialization",
        "vertical-sync-callback",
    }

    equivalence = list(csv.DictReader(written["equivalence_csv"].open(newline="", encoding="utf-8")))
    assert len(equivalence) == len(EXPECTED_SCOPE)
    assert {row["equivalence_status"] for row in equivalence} == {"blocked-missing-non-raw-nd-lifecycle-equivalence-proof"}

    source_patch = list(csv.DictReader(written["source_patch_csv"].open(newline="", encoding="utf-8")))
    assert {row["source_patch_allowed"] for row in source_patch} == {"no"}
    assert {row["marker_change_allowed"] for row in source_patch} == {"no"}

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "TBD"
    assert handoff["selected_cluster"] == "module-spec_psxpc_n"
    assert handoff["selected_pivot"] == "all-clusters-proof-blocked-or-closed"
    assert handoff["code_change_readiness"] == "blocked"

    story_text = written["RE-212"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-211 source-patch gate denied source and marker changes" in story_text
    assert "next ticket: `TBD`" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "test_re206_re212_platform_main_lifecycle_epic.py" in story_text

    md_text = written["md"].read_text(encoding="utf-8")
    assert "platform-main-lifecycle-epic-closed-with-proof-blocker" in md_text
    assert "source-patch-ready rows: `0`" in md_text
    assert "module-spec_psxpc_n exhausted" in md_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_FRAGMENTS + STALE_FRAGMENTS:
            assert fragment not in text
