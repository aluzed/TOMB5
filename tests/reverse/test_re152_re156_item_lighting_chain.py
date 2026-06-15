from pathlib import Path
import csv

from scripts.reverse.re152_re156_item_lighting_chain import (
    build_item_lighting_chain,
    write_all_artifacts,
    FORBIDDEN_FRAGMENTS,
)


def test_re152_re156_consumes_re149_plan_and_closes_item_lighting_to_ui_text():
    repo = Path(__file__).resolve().parents[2]
    chain = build_item_lighting_chain(repo)

    assert [ticket.story_id for ticket in chain.tickets] == ["RE-152", "RE-153", "RE-154", "RE-155", "RE-156"]
    assert chain.cluster == "item-lighting-interaction"
    assert chain.upstream_ticket == "RE-151"
    assert [row.function for row in chain.comparison_rows] == ["DoFlameTorch", "TriggerAlertLight"]
    assert [row.shape_id for row in chain.comparison_rows] == [
        "shape-item-lighting-void-torch-update",
        "shape-item-lighting-alert-light-parameters",
    ]
    assert chain.code_change_ready_count == 0
    assert chain.marker_ready_count == 0
    assert chain.source_patch_ready_count == 0
    assert chain.status == "item-lighting-interaction-chain-closed-with-proof-blocker"
    assert chain.handoff.next_ticket == "RE-157"
    assert chain.handoff.next_cluster == "ui-text-support"
    assert chain.handoff.next_subcluster == "ui-text-support"
    assert "item-lighting-interaction closed" in chain.handoff.reason
    assert "InitFont" in chain.handoff.reason


def test_re152_re156_outputs_metadata_only_artifacts_and_progress_trackers(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    chain = build_item_lighting_chain(repo)
    written = write_all_artifacts(chain, tmp_path)

    comparison = list(csv.DictReader(written["comparison_csv"].open(newline="", encoding="utf-8")))
    assert [row["function"] for row in comparison] == ["DoFlameTorch", "TriggerAlertLight"]
    assert all(row["equivalence_status"] == "blocked-missing-symbolic-equivalence-proof" for row in comparison)
    assert all(row["code_change_ready"] == "no" for row in comparison)
    assert all(row["marker_ready"] == "no" for row in comparison)

    plan = list(csv.DictReader(written["plan_csv"].open(newline="", encoding="utf-8")))
    assert [row["ticket"] for row in plan] == ["RE-157", "RE-158", "RE-159", "RE-160", "RE-161"]
    assert plan[0]["cluster"] == "ui-text-support"
    assert "InitFont" in plan[0]["goal"]

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-157"
    assert handoff["next_cluster"] == "ui-text-support"
    assert handoff["code_change_readiness"] == "blocked"

    story_text = written["RE-156"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-151 taxonomy consumed" in story_text
    assert "Item-lighting metadata closed with blocker" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "RE-157" in story_text
    assert "test_re152_re156_item_lighting_chain.py" in story_text
    assert "object-interaction" not in story_text.lower()
    assert "gameplay-mixed" not in story_text.lower()
    assert "test_re142" not in story_text.lower()

    md_text = written["md"].read_text(encoding="utf-8")
    assert "missing item lighting state contract" in md_text
    assert "ui-text-support" in md_text
    assert "source-patch-ready rows: `0`" in md_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_FRAGMENTS:
            assert fragment not in text
