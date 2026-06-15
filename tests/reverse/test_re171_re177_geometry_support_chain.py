from pathlib import Path
import csv

from scripts.reverse.re171_re177_geometry_support_chain import (
    FORBIDDEN_FRAGMENTS,
    EXPECTED_SCOPE,
    build_geometry_support_chain,
    write_all_artifacts,
)


def test_re171_re177_consumes_re170_plan_and_closes_geometry_support_blocked():
    repo = Path(__file__).resolve().parents[2]
    chain = build_geometry_support_chain(repo)

    assert [ticket.story_id for ticket in chain.tickets] == [
        "RE-171",
        "RE-172",
        "RE-173",
        "RE-174",
        "RE-175",
        "RE-176",
        "RE-177",
    ]
    assert chain.domain_id == "module-spec_psxpc_n"
    assert chain.cluster == "geometry-support"
    assert chain.upstream_ticket == "RE-170"
    assert chain.pivot == "GetBoundsAccurate"
    assert chain.status == "geometry-support-chain-closed-with-proof-blocker"
    assert chain.final_decision == "documentation-only-terminal-blocker"
    assert chain.code_change_ready_count == 0
    assert chain.marker_ready_count == 0
    assert chain.source_patch_ready_count == 0
    assert [row.function for row in chain.audit_rows] == list(EXPECTED_SCOPE)
    assert any(row.callee == "GetBoundsAccurate" for row in chain.callsite_rows)
    assert all(row.caller not in {"if", "for", "while", "switch"} for row in chain.callsite_rows)
    assert {row.function for row in chain.taxonomy_rows} == set(EXPECTED_SCOPE)
    assert {row.function for row in chain.contract_rows} == set(EXPECTED_SCOPE)
    assert all(row.code_change_ready == "no" for row in chain.equivalence_rows)
    assert all(row.source_patch_allowed == "no" for row in chain.source_patch_rows)
    assert chain.handoff.next_ticket == "RE-178"
    assert chain.handoff.next_topic == "frontend-sequence-proof-first-audit"


def test_re171_re177_outputs_metadata_only_artifacts_and_story_trackers(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    chain = build_geometry_support_chain(repo)
    written = write_all_artifacts(chain, tmp_path)

    audit = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    assert audit[0]["function"] == "GetBoundsAccurate"
    assert audit[0]["role"] == "pivot"
    assert audit[0]["proof_status"] == "source-scope-inventory-only"

    callsites = list(csv.DictReader(written["callsite_csv"].open(newline="", encoding="utf-8")))
    assert callsites
    assert all(row["source_line_text"] == "source-line-contains-callee-call" for row in callsites)
    assert all(int(row["line"]) > 0 for row in callsites)

    taxonomy = list(csv.DictReader(written["taxonomy_csv"].open(newline="", encoding="utf-8")))
    assert {row["argument_family"] for row in taxonomy} == {
        "bounds-item",
        "clip-window",
        "matrix-interpolation",
        "frame-pair",
        "best-frame",
        "animation-change",
        "track-decode",
    }

    equivalence = list(csv.DictReader(written["equivalence_csv"].open(newline="", encoding="utf-8")))
    assert len(equivalence) == len(EXPECTED_SCOPE)
    assert {row["equivalence_status"] for row in equivalence} == {"blocked-missing-non-raw-binary-equivalence-proof"}

    source_patch = list(csv.DictReader(written["source_patch_csv"].open(newline="", encoding="utf-8")))
    assert {row["source_patch_allowed"] for row in source_patch} == {"no"}
    assert {row["marker_change_allowed"] for row in source_patch} == {"no"}

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-178"
    assert handoff["selected_cluster"] == "frontend-sequence"
    assert handoff["code_change_readiness"] == "blocked"

    story_text = written["RE-177"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-176 source-patch gate denied source and marker changes" in story_text
    assert "next ticket: `RE-178`" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "test_re171_re177_geometry_support_chain.py" in story_text
    assert "ui-text-rendering" not in story_text.lower()
    assert "item-lighting" not in story_text.lower()

    md_text = written["md"].read_text(encoding="utf-8")
    assert "geometry-support-chain-closed-with-proof-blocker" in md_text
    assert "source-patch-ready rows: `0`" in md_text
    assert "frontend-sequence" in md_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "ui text rendering" not in text
        assert "ui-text-rendering" not in text
        assert "item-lighting" not in text
        for fragment in FORBIDDEN_FRAGMENTS:
            assert fragment not in text
