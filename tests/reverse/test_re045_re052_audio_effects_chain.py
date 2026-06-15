from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.re045_re052_audio_effects_chain import (
    build_audio_effects_chain,
    write_all_artifacts,
)


def test_audio_effects_chain_runs_re045_through_re052_to_terminal_decision():
    chain = build_audio_effects_chain(ROOT)

    assert tuple(ticket.story_id for ticket in chain.tickets) == (
        "RE-045",
        "RE-046",
        "RE-047",
        "RE-048",
        "RE-049",
        "RE-050",
        "RE-051",
        "RE-052",
    )
    assert chain.domain_id == "audio-effects"
    assert chain.pivot_function == "SoundEffect"
    assert chain.status == "audio-effects-chain-terminal-no-safe-marker-or-source-patch"
    assert chain.final_decision == "handoff-to-collision-domain"
    assert chain.next_ticket == "RE-053"
    assert chain.code_change_ready_count == 0
    assert chain.marker_ready_count == 0
    assert chain.source_patch_ready_count == 0

    assert chain.summary.candidate_count >= 10
    assert chain.summary.soundeffect_rows == 3
    assert chain.summary.caller_count >= 70
    assert chain.summary.callee_count >= 7
    assert chain.summary.callsite_count > 0
    assert chain.summary.callsite_shape_count >= 1

    tickets = {ticket.story_id: ticket for ticket in chain.tickets}
    assert tickets["RE-045"].topic == "audio-effects-domain-scope"
    assert tickets["RE-046"].topic == "soundeffect-caller-map"
    assert tickets["RE-047"].topic == "soundeffect-argument-taxonomy"
    assert tickets["RE-048"].topic == "soundeffect-comparison-gate"
    assert tickets["RE-049"].topic == "audio-effects-cluster-proof"
    assert tickets["RE-050"].topic == "audio-effects-marker-source-patch-gate"
    assert tickets["RE-051"].topic == "audio-effects-terminal-blocker"
    assert tickets["RE-052"].topic == "audio-effects-closure-next-domain-handoff"

    assert tickets["RE-045"].decision == "soundeffect-selected-as-pivot"
    assert tickets["RE-048"].decision == "blocked-by-missing-non-raw-binary-equivalence-proof"
    assert tickets["RE-050"].decision == "no-safe-marker-or-source-patch"
    assert tickets["RE-052"].decision == "handoff-to-collision-domain"

    for ticket in chain.tickets:
        assert ticket.status == "Done"
        assert ticket.code_change_readiness == "blocked"
        assert ticket.progress == (
            "input-artifacts-loaded",
            "metadata-only-artifact-published",
            "readiness-decision-recorded",
            "forbidden-raw-evidence-excluded",
        )


def test_audio_effects_chain_outputs_all_stories_and_metadata_only_reports(tmp_path):
    chain = build_audio_effects_chain(ROOT)
    written = write_all_artifacts(chain, tmp_path)

    assert written["summary_csv"].name == "re045-re052-audio-effects-chain.csv"
    assert written["domain_csv"].name == "re045-audio-effects-domain-scope.csv"
    assert written["caller_csv"].name == "re046-soundeffect-caller-map.csv"
    assert written["taxonomy_csv"].name == "re047-soundeffect-argument-taxonomy.csv"
    assert written["md"].name == "re045-re052-audio-effects-chain.md"
    assert len(written["stories"]) == 8

    summary_csv = written["summary_csv"].read_text(encoding="utf-8")
    domain_csv = written["domain_csv"].read_text(encoding="utf-8")
    caller_csv = written["caller_csv"].read_text(encoding="utf-8")
    taxonomy_csv = written["taxonomy_csv"].read_text(encoding="utf-8")
    md_text = written["md"].read_text(encoding="utf-8")
    story_texts = [path.read_text(encoding="utf-8") for path in written["stories"]]

    assert "RE-045,audio-effects-domain-scope" in summary_csv
    assert "RE-052,audio-effects-closure-next-domain-handoff" in summary_csv
    assert "SoundEffect" in domain_csv
    assert "cluster,function_count,caller_count" in caller_csv
    assert "shape_id,arity,site_count" in taxonomy_csv
    assert "code-change-ready tickets: `0`" in md_text
    assert "Recommended next ticket: `RE-053`" in md_text

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
