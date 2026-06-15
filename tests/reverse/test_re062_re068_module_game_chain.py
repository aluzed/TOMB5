from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.re062_re068_module_game_chain import (
    build_module_game_chain,
    write_all_artifacts,
)


def test_re062_re068_builds_debris_chain_with_terminal_blocker():
    chain = build_module_game_chain(ROOT)

    assert chain.domain_id == "module-game"
    assert chain.cluster == "debris-object-breakage"
    assert chain.status == "module-game-debris-chain-closed-with-proof-blocker"
    assert chain.final_decision == "documentation-only-terminal-blocker"
    assert chain.code_change_ready_count == 0
    assert chain.marker_ready_count == 0
    assert chain.source_patch_ready_count == 0
    assert chain.next_ticket == "RE-069"

    assert tuple(ticket.story_id for ticket in chain.tickets) == (
        "RE-062",
        "RE-063",
        "RE-064",
        "RE-065",
        "RE-066",
        "RE-067",
        "RE-068",
    )
    assert chain.tickets[0].status == "done"
    assert chain.tickets[-1].decision == "handoff-to-next-module-game-cluster"
    assert all(ticket.code_change_readiness == "blocked" for ticket in chain.tickets)
    assert all(ticket.progress for ticket in chain.tickets)

    functions = {row.function: row for row in chain.scope_rows}
    assert functions["ShatterObject"].implementation_status == "unimplemented-stub"
    assert functions["TriggerDebris"].implementation_status == "unimplemented-stub"
    assert functions["GetFreeDebris"].implementation_status == "implemented-source"
    assert functions["ExplodeItemNode"].caller_or_callee_role == "caller"
    assert functions["ExplodeFX"].caller_or_callee_role == "caller"
    assert functions["UpdateDebris"].implementation_status == "unimplemented-stub"

    assert {row.caller for row in chain.callsites}.isdisjoint({"if", "for", "while", "switch"})
    callsites = {(row.caller, row.callee): row for row in chain.callsites}
    assert ("ExplodeFX", "ShatterObject") in callsites
    assert ("ExplodeItemNode", "ShatterObject") in callsites
    assert callsites[("ExplodeItemNode", "ShatterObject")].shape_id == "shape-item-derived-room-and-bits"
    assert ("InitialiseLevel", "UpdateDebris") not in callsites

    shapes = {shape.shape_id: shape for shape in chain.argument_shapes}
    assert "shape-item-derived-room-and-bits" in shapes
    assert shapes["shape-item-derived-room-and-bits"].source_backed == "yes"
    assert shapes["shape-item-derived-room-and-bits"].patch_ready == "no"
    assert "missing-non-raw-binary-equivalence" in shapes["shape-item-derived-room-and-bits"].blocker

    assert chain.handoff.next_cluster != "debris-object-breakage"
    assert chain.handoff.next_ticket == "RE-069"
    assert chain.handoff.reason == "initial-cluster-terminal-blocker"


def test_re062_re068_outputs_metadata_only_artifacts(tmp_path):
    chain = build_module_game_chain(ROOT)
    written = write_all_artifacts(chain, tmp_path)

    expected_keys = {
        "chain_csv",
        "scope_csv",
        "callsite_csv",
        "taxonomy_csv",
        "handoff_csv",
        "md",
        "RE-062",
        "RE-063",
        "RE-064",
        "RE-065",
        "RE-066",
        "RE-067",
        "RE-068",
    }
    assert expected_keys <= set(written)

    chain_csv = written["chain_csv"].read_text(encoding="utf-8")
    scope_csv = written["scope_csv"].read_text(encoding="utf-8")
    callsite_csv = written["callsite_csv"].read_text(encoding="utf-8")
    taxonomy_csv = written["taxonomy_csv"].read_text(encoding="utf-8")
    handoff_csv = written["handoff_csv"].read_text(encoding="utf-8")
    md_text = written["md"].read_text(encoding="utf-8")
    story_text = written["RE-068"].read_text(encoding="utf-8")

    assert "story_id,title,status,decision,next_ticket,code_change_readiness" in chain_csv
    assert "RE-062,Debris object breakage caller side-effect map,done" in chain_csv
    assert "function,file,caller_or_callee_role,implementation_status" in scope_csv
    assert "ShatterObject,GAME/DEBRIS.C,pivot,unimplemented-stub" in scope_csv
    assert "caller,callee,caller_file,callee_file,line,shape_id" in callsite_csv
    assert "ExplodeItemNode,ShatterObject,GAME/CONTROL.C,GAME/DEBRIS.C" in callsite_csv
    assert "shape_id,site_count,arg1_kind,arg2_kind,arg3_kind,arg4_kind,arg5_kind" in taxonomy_csv
    assert "shape-item-derived-room-and-bits" in taxonomy_csv
    assert "next_ticket,next_cluster,reason" in handoff_csv
    assert "RE-069" in handoff_csv
    assert "# RE-062..RE-068 — Module-game debris/object-breakage chain" in md_text
    assert "## Progress tracker" in story_text
    assert "- [x] Closure/handoff recorded." in story_text

    forbidden_fragments = (
        "0x",
        "36A3C",
        "36F3C",
        "3675C",
        "36C5C",
        "366B0",
        "36BB0",
        "207DC",
        "209F0",
    )
    for text in (chain_csv, scope_csv, callsite_csv, taxonomy_csv, handoff_csv, md_text, story_text):
        assert not any(fragment in text for fragment in forbidden_fragments)
