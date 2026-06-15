from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.re070_re076_lara_movement_chain import (
    build_lara_movement_chain,
    write_all_artifacts,
)


def test_re070_re076_builds_lara_movement_chain_with_handoff():
    chain = build_lara_movement_chain(ROOT)

    assert chain.domain_id == "module-game"
    assert chain.cluster == "lara-movement-support"
    assert chain.subcluster == "ledge-and-vault-tests"
    assert chain.status == "lara-movement-chain-closed-with-proof-blocker"
    assert chain.final_decision == "documentation-only-terminal-blocker"
    assert chain.code_change_ready_count == 0
    assert chain.marker_ready_count == 0
    assert chain.source_patch_ready_count == 0
    assert chain.next_ticket == "RE-077"

    assert tuple(ticket.story_id for ticket in chain.tickets) == (
        "RE-070",
        "RE-071",
        "RE-072",
        "RE-073",
        "RE-074",
        "RE-075",
        "RE-076",
    )
    assert chain.tickets[0].status == "done"
    assert chain.tickets[-1].decision == "handoff-to-next-module-game-cluster"
    assert all(ticket.code_change_readiness == "blocked" for ticket in chain.tickets)
    assert all(ticket.progress for ticket in chain.tickets)

    functions = {row.function: row for row in chain.scope_rows}
    assert functions["TestLaraSlide"].role == "pivot"
    assert functions["TestLaraSlide"].implementation_status == "implemented-source"
    assert functions["TestLaraVault"].role == "ledge-vault-predicate"
    assert functions["LaraHangRightCornerTest"].role == "corner-predicate"
    assert functions["LaraHangLeftCornerTest"].role == "corner-predicate"
    assert {row.function for row in chain.scope_rows}.isdisjoint({"if", "for", "while", "switch"})

    assert len(chain.callsites) >= 10
    assert {row.caller for row in chain.callsites}.isdisjoint({"if", "for", "while", "switch"})
    assert any(row.callee == "TestLaraSlide" and row.shape_id == "shape-item-coll-predicate" for row in chain.callsites)
    assert any(row.callee == "TestLaraVault" and row.shape_id == "shape-item-coll-predicate" for row in chain.callsites)
    assert any(row.callee == "LaraHangRightCornerTest" for row in chain.callsites)

    shapes = {shape.shape_id: shape for shape in chain.argument_shapes}
    assert "shape-item-coll-predicate" in shapes
    assert shapes["shape-item-coll-predicate"].source_backed == "yes"
    assert shapes["shape-item-coll-predicate"].patch_ready == "no"
    assert "missing-non-raw-binary-equivalence" in shapes["shape-item-coll-predicate"].blocker

    assert chain.handoff.next_ticket == "RE-077"
    assert chain.handoff.next_cluster != "lara-movement-support"
    assert chain.handoff.reason == "initial-subcluster-terminal-blocker"


def test_re070_re076_outputs_metadata_only_artifacts(tmp_path):
    chain = build_lara_movement_chain(ROOT)
    written = write_all_artifacts(chain, tmp_path)

    expected_keys = {
        "chain_csv",
        "scope_csv",
        "callsite_csv",
        "taxonomy_csv",
        "handoff_csv",
        "md",
        "RE-070",
        "RE-071",
        "RE-072",
        "RE-073",
        "RE-074",
        "RE-075",
        "RE-076",
    }
    assert expected_keys <= set(written)

    chain_csv = written["chain_csv"].read_text(encoding="utf-8")
    scope_csv = written["scope_csv"].read_text(encoding="utf-8")
    callsite_csv = written["callsite_csv"].read_text(encoding="utf-8")
    taxonomy_csv = written["taxonomy_csv"].read_text(encoding="utf-8")
    handoff_csv = written["handoff_csv"].read_text(encoding="utf-8")
    md_text = written["md"].read_text(encoding="utf-8")
    story_text = written["RE-076"].read_text(encoding="utf-8")

    assert "story_id,title,status,decision,next_ticket,code_change_readiness" in chain_csv
    assert "RE-070,Lara movement caller side-effect map,done" in chain_csv
    assert "function,file,role,implementation_status" in scope_csv
    assert "TestLaraSlide,GAME/LARA.C,pivot,implemented-source" in scope_csv
    assert "caller,callee,caller_file,callee_file,line,shape_id" in callsite_csv
    assert "TestLaraSlide" in callsite_csv
    assert "shape_id,site_count,arg1_kind,arg2_kind,state_fields" in taxonomy_csv
    assert "shape-item-coll-predicate" in taxonomy_csv
    assert "next_ticket,next_cluster,reason" in handoff_csv
    assert "RE-077" in handoff_csv
    assert "# RE-070..RE-076 — Lara movement chain" in md_text
    assert "## Progress tracker" in story_text
    assert "- [x] Closure/handoff recorded." in story_text

    forbidden_fragments = ("0x", "payload", "opcode", "machine word", "raw call target")
    for text in (chain_csv, scope_csv, callsite_csv, taxonomy_csv, handoff_csv, md_text, story_text):
        lowered = text.lower()
        assert not any(fragment in lowered for fragment in forbidden_fragments)
