from pathlib import Path
import csv

from scripts.reverse.re192_re198_platform_gpu_display_epic import (
    EXPECTED_SCOPE,
    FORBIDDEN_FRAGMENTS,
    STALE_FRAGMENTS,
    build_platform_gpu_display_epic,
    write_all_artifacts,
)


def test_re192_re198_consumes_re191_handoff_and_finishes_platform_gpu_display():
    repo = Path(__file__).resolve().parents[2]
    epic = build_platform_gpu_display_epic(repo)

    assert [ticket.story_id for ticket in epic.tickets] == [
        "RE-192",
        "RE-193",
        "RE-194",
        "RE-195",
        "RE-196",
        "RE-197",
        "RE-198",
    ]
    assert epic.domain_id == "module-spec_psxpc_n"
    assert epic.cluster == "platform-gpu-display"
    assert epic.upstream_ticket == "RE-191"
    assert epic.pivot == "clear_a_rect"
    assert epic.status == "platform-gpu-display-epic-closed-with-proof-blocker"
    assert epic.final_decision == "documentation-only-terminal-blocker"
    assert epic.code_change_ready_count == 0
    assert epic.marker_ready_count == 0
    assert epic.source_patch_ready_count == 0
    assert [row.function for row in epic.audit_rows] == list(EXPECTED_SCOPE)
    assert any(row.callee == "clear_a_rect" for row in epic.callsite_rows)
    assert any(row.callee == "S_control_screen_position" for row in epic.callsite_rows)
    assert any(row.callee == "OptimiseOTagR" for row in epic.callsite_rows)
    assert any(row.callee == "S_CalculateStaticMeshLight" for row in epic.callsite_rows)
    assert all(row.caller not in {"if", "for", "while", "switch"} for row in epic.callsite_rows)
    assert {row.function for row in epic.taxonomy_rows} == set(EXPECTED_SCOPE)
    assert all(row.code_change_ready == "no" for row in epic.equivalence_rows)
    assert all(row.source_patch_allowed == "no" for row in epic.source_patch_rows)
    assert [row.cluster for row in epic.next_selection_rows] == ["platform-memory", "platform-main-lifecycle"]
    assert [row.top_function for row in epic.next_selection_rows] == ["game_malloc", "main"]
    assert epic.handoff.next_ticket == "RE-199"
    assert epic.handoff.next_topic == "platform-memory-proof-first-audit"
    assert epic.handoff.selected_cluster == "platform-memory"
    assert epic.handoff.selected_pivot == "game_malloc"


def test_re192_re198_outputs_metadata_only_artifacts_and_story_trackers(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    epic = build_platform_gpu_display_epic(repo)
    written = write_all_artifacts(epic, tmp_path)

    plan = list(csv.DictReader(written["plan_csv"].open(newline="", encoding="utf-8")))
    assert [row["story_id"] for row in plan] == ["RE-193", "RE-194", "RE-195", "RE-196", "RE-197", "RE-198"]
    assert plan[-1]["topic"] == "module-spec-psxpc-n-post-platform-gpu-display-next-cluster-selection"

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
        "vram-rect-clear",
        "screen-position-control",
        "ordering-table-optimization",
        "static-mesh-lighting",
    }

    equivalence = list(csv.DictReader(written["equivalence_csv"].open(newline="", encoding="utf-8")))
    assert len(equivalence) == len(EXPECTED_SCOPE)
    assert {row["equivalence_status"] for row in equivalence} == {"blocked-missing-non-raw-binary-equivalence-proof"}

    source_patch = list(csv.DictReader(written["source_patch_csv"].open(newline="", encoding="utf-8")))
    assert {row["source_patch_allowed"] for row in source_patch} == {"no"}
    assert {row["marker_change_allowed"] for row in source_patch} == {"no"}

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-199"
    assert handoff["selected_cluster"] == "platform-memory"
    assert handoff["selected_pivot"] == "game_malloc"
    assert handoff["code_change_readiness"] == "blocked"

    story_text = written["RE-198"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-197 source-patch gate denied source and marker changes" in story_text
    assert "next ticket: `RE-199`" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "test_re192_re198_platform_gpu_display_epic.py" in story_text

    md_text = written["md"].read_text(encoding="utf-8")
    assert "platform-gpu-display-epic-closed-with-proof-blocker" in md_text
    assert "source-patch-ready rows: `0`" in md_text
    assert "platform-memory" in md_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_FRAGMENTS + STALE_FRAGMENTS:
            assert fragment not in text
