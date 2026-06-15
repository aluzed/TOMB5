from pathlib import Path
import csv

from scripts.reverse.re158_re161_ui_text_support_chain import (
    FORBIDDEN_FRAGMENTS,
    build_ui_text_support_chain,
    write_all_artifacts,
)


def test_re158_re161_consumes_re157_plan_and_closes_ui_text_support():
    repo = Path(__file__).resolve().parents[2]
    chain = build_ui_text_support_chain(repo)

    assert [ticket.story_id for ticket in chain.tickets] == ["RE-158", "RE-159", "RE-160", "RE-161"]
    assert chain.cluster == "ui-text-support"
    assert chain.upstream_ticket == "RE-157"
    assert chain.pivot == "InitFont"
    assert chain.status == "ui-text-support-chain-closed-with-proof-blocker"
    assert chain.final_decision == "documentation-only-terminal-blocker"
    assert chain.code_change_ready_count == 0
    assert chain.marker_ready_count == 0
    assert chain.source_patch_ready_count == 0
    assert [row.callee for row in chain.callsite_rows] == ["InitFont"]
    assert chain.callsite_rows[0].caller == "main"
    assert chain.callsite_rows[0].caller_file == "SPEC_PSX/PSXMAIN.C"
    assert chain.callsite_rows[0].arg_count == 0
    assert chain.callsite_rows[0].source_line_text == "source-line-contains-callee-call"
    assert chain.taxonomy_rows[0].shape_id == "shape-ui-text-initfont-void-font-shade-init"
    assert chain.comparison_rows[0].equivalence_status == "blocked-missing-initfont-behavior-equivalence-proof"
    assert chain.handoff.next_ticket == "TBD"
    assert chain.handoff.next_cluster == "module-game-exhausted"
    assert "all RE-061 module-game clusters" in chain.handoff.reason


def test_re158_re161_outputs_metadata_only_artifacts_and_story_trackers(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    chain = build_ui_text_support_chain(repo)
    written = write_all_artifacts(chain, tmp_path)

    callsites = list(csv.DictReader(written["callsite_csv"].open(newline="", encoding="utf-8")))
    assert len(callsites) == 1
    assert callsites[0]["callee"] == "InitFont"
    assert callsites[0]["caller"] == "main"
    assert callsites[0]["proof_status"] == "source-callsite-mapped-only"
    assert callsites[0]["patch_ready"] == "no"

    taxonomy = list(csv.DictReader(written["taxonomy_csv"].open(newline="", encoding="utf-8")))
    assert taxonomy == [{
        "function": "InitFont",
        "shape_id": "shape-ui-text-initfont-void-font-shade-init",
        "argument_kinds": "void",
        "state_fields": "font-shade-table;shade-gradient-inputs;per-channel-clamp",
        "source_contract": "initializes font shade lookup table from shade endpoints",
        "source_evidence": "source-body-and-callsite-only",
        "proof_status": "taxonomy-needs-equivalence-proof",
        "code_change_ready": "no",
        "marker_ready": "no",
        "blocker": "missing-initfont-behavior-equivalence-proof",
    }]

    comparison = list(csv.DictReader(written["comparison_csv"].open(newline="", encoding="utf-8")))
    assert comparison[0]["source_patch_allowed"] == "no"
    assert comparison[0]["marker_change_allowed"] == "no"
    assert comparison[0]["next_action"] == "close-ui-text-support-and-record-module-game-exhaustion"

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "TBD"
    assert handoff["next_cluster"] == "module-game-exhausted"
    assert handoff["code_change_readiness"] == "blocked"

    story_text = written["RE-161"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-160 comparison gate kept marker/source changes blocked" in story_text
    assert "next ticket: `TBD`" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "test_re158_re161_ui_text_support_chain.py" in story_text
    assert "item-lighting" not in story_text.lower()
    assert "object-interaction" not in story_text.lower()
    assert "test_re152" not in story_text.lower()

    md_text = written["md"].read_text(encoding="utf-8")
    assert "ui-text-support-chain-closed-with-proof-blocker" in md_text
    assert "source-patch-ready rows: `0`" in md_text
    assert "module-game-exhausted" in md_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_FRAGMENTS:
            assert fragment not in text
