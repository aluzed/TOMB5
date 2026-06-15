from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.re053_re060_collision_chain import (
    build_collision_chain,
    write_all_artifacts,
)


def test_collision_chain_runs_re053_through_re060_to_terminal_decision():
    chain = build_collision_chain(ROOT)

    assert tuple(ticket.story_id for ticket in chain.tickets) == (
        "RE-053",
        "RE-054",
        "RE-055",
        "RE-056",
        "RE-057",
        "RE-058",
        "RE-059",
        "RE-060",
    )
    assert chain.domain_id == "collision"
    assert chain.pivot_function == "GetCollisionInfo"
    assert chain.status == "collision-chain-terminal-no-safe-marker-or-source-patch"
    assert chain.final_decision == "handoff-to-module-game-domain"
    assert chain.next_ticket == "RE-061"
    assert chain.code_change_ready_count == 0
    assert chain.marker_ready_count == 0
    assert chain.source_patch_ready_count == 0

    assert chain.summary.candidate_count >= 20
    assert chain.summary.pivot_rows == 1
    assert chain.summary.caller_count >= 15
    assert chain.summary.callee_count >= 7
    assert chain.summary.callsite_count >= 15
    assert chain.summary.callsite_shape_count >= 1
    assert chain.summary.selected_cluster in {
        "lara-movement-collision",
        "floor-height-query",
        "collision-internal",
    }
    assert {function.function for function in chain.domain_functions}.isdisjoint(
        {"if", "for", "while", "switch"}
    )

    tickets = {ticket.story_id: ticket for ticket in chain.tickets}
    assert tickets["RE-053"].topic == "collision-domain-scope"
    assert tickets["RE-054"].topic == "getcollisioninfo-caller-map"
    assert tickets["RE-055"].topic == "collision-argument-data-taxonomy"
    assert tickets["RE-056"].topic == "collision-comparison-gate"
    assert tickets["RE-057"].topic == "collision-proof-cluster"
    assert tickets["RE-058"].topic == "collision-marker-source-patch-gate"
    assert tickets["RE-059"].topic == "collision-terminal-blocker"
    assert tickets["RE-060"].topic == "collision-closure-next-domain-handoff"

    assert tickets["RE-053"].decision == "getcollisioninfo-selected-as-pivot"
    assert tickets["RE-056"].decision == "blocked-by-missing-non-raw-binary-equivalence-proof"
    assert tickets["RE-058"].decision == "no-safe-marker-or-source-patch"
    assert tickets["RE-060"].decision == "handoff-to-module-game-domain"

    for ticket in chain.tickets:
        assert ticket.status == "Done"
        assert ticket.code_change_readiness == "blocked"
        assert ticket.progress == (
            "input-artifacts-loaded",
            "metadata-only-artifact-published",
            "readiness-decision-recorded",
            "forbidden-raw-evidence-excluded",
        )


def test_collision_chain_outputs_all_stories_and_metadata_only_reports(tmp_path):
    chain = build_collision_chain(ROOT)
    written = write_all_artifacts(chain, tmp_path)

    assert written["summary_csv"].name == "re053-re060-collision-chain.csv"
    assert written["domain_csv"].name == "re053-collision-domain-scope.csv"
    assert written["caller_csv"].name == "re054-getcollisioninfo-caller-map.csv"
    assert written["taxonomy_csv"].name == "re055-collision-argument-data-taxonomy.csv"
    assert written["md"].name == "re053-re060-collision-chain.md"
    assert len(written["stories"]) == 8

    summary_csv = written["summary_csv"].read_text(encoding="utf-8")
    domain_csv = written["domain_csv"].read_text(encoding="utf-8")
    caller_csv = written["caller_csv"].read_text(encoding="utf-8")
    taxonomy_csv = written["taxonomy_csv"].read_text(encoding="utf-8")
    md_text = written["md"].read_text(encoding="utf-8")
    story_texts = [path.read_text(encoding="utf-8") for path in written["stories"]]

    assert "RE-053,collision-domain-scope" in summary_csv
    assert "RE-060,collision-closure-next-domain-handoff" in summary_csv
    assert "GetCollisionInfo" in domain_csv
    assert "cluster,function_count,caller_count" in caller_csv
    assert "shape_id,arity,site_count" in taxonomy_csv
    assert "code-change-ready tickets: `0`" in md_text
    assert "Recommended next ticket: `RE-061`" in md_text

    for story_text in story_texts:
        assert "Status: Done" in story_text
        assert "## Progress" in story_text
        assert "- [x] Input artifacts loaded." in story_text
        assert "## Readiness decision" in story_text

    forbidden = (
        "word_" + "le_hex",
        "payload_" + "offset",
        "dump" + " row",
        "jal " + "0x",
        "call_" + "address",
        "0x" + "800",
    )
    for text in (summary_csv, domain_csv, caller_csv, taxonomy_csv, md_text, *story_texts):
        for token in forbidden:
            assert token not in text
