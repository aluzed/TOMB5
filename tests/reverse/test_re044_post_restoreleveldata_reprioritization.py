from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.re044_post_restoreleveldata_reprioritization import (
    build_reprioritization,
    write_all_artifacts,
)


def test_re044_reprioritizes_domains_after_restoreleveldata_terminal_closure():
    plan = build_reprioritization(ROOT)

    assert plan.story_id == "RE-044"
    assert plan.status == "post-restoreleveldata-domain-reprioritization-ready"
    assert plan.restoreleveldata_chain_status == "closed-by-RE-043"
    assert plan.code_change_readiness == "documentation-only-selection-gate"
    assert plan.next_ticket == "RE-045"
    assert plan.excluded_closed_chain_count >= 2

    domain_ids = tuple(domain.domain_id for domain in plan.domains)
    assert "audio-effects" in domain_ids
    assert "collision" in domain_ids
    assert "inventory" in domain_ids
    assert "camera" in domain_ids
    assert "input" in domain_ids

    for domain in plan.domains:
        assert domain.status == "candidate"
        assert domain.next_action.startswith("create RE-045") or domain.next_action.startswith("defer")
        for function in domain.functions:
            assert function.file != "GAME/SAVEGAME.C"
            assert function.name not in {"RestoreLevelData", "SaveLevelData"}
            assert not function.address

    top = plan.domains[0]
    assert top.domain_id in {"audio-effects", "input", "camera", "collision", "inventory"}
    assert top.next_action.startswith("create RE-045")


def test_re044_outputs_story_generated_artifacts_and_metadata_only_content(tmp_path):
    plan = build_reprioritization(ROOT)
    written = write_all_artifacts(plan, tmp_path)

    assert written["csv"].name == "re044-domain-reprioritization.csv"
    assert written["md"].name == "re044-post-restoreleveldata-reprioritization.md"
    assert written["story"].name == "RE-044-post-restoreleveldata-domain-reprioritization.md"

    csv_text = written["csv"].read_text(encoding="utf-8")
    md_text = written["md"].read_text(encoding="utf-8")
    story_text = written["story"].read_text(encoding="utf-8")

    assert "domain_id,rank,status,score,candidate_count" in csv_text
    assert "RestoreLevelData" not in csv_text
    assert "SaveLevelData" not in csv_text
    assert "GAME/SAVEGAME.C" not in csv_text

    assert "# RE-044 — Post-RestoreLevelData domain reprioritization" in story_text
    assert "Status: Done" in story_text
    assert "## Progress" in story_text
    assert "- [x] Closed RestoreLevelData chain excluded." in story_text
    assert "## Selection decision" in story_text
    assert "Recommended next ticket: `RE-045`" in story_text

    assert "## Progress tracker" in md_text
    assert "RestoreLevelData chain: `closed-by-RE-043`" in md_text
    assert "Recommended next ticket: `RE-045`" in md_text

    forbidden = (
        "word_" + "le_hex",
        "payload_" + "offset",
        "dump" + " row",
        "jal " + "0x",
        "call_" + "address",
        "0x" + "800",
    )
    for text in (csv_text, md_text, story_text):
        for token in forbidden:
            assert token not in text
