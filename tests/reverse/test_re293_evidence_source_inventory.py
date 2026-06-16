from pathlib import Path
import csv

from scripts.reverse.re293_evidence_source_inventory import (
    FORBIDDEN,
    build_inventory,
    write_all_artifacts,
)


def test_re293_inventory_consumes_re292_and_classifies_evidence_sources():
    repo = Path(__file__).resolve().parents[2]
    inventory = build_inventory(repo)

    assert inventory.summary.story_id == "RE-293"
    assert inventory.summary.upstream_handoff == "RE-292"
    assert inventory.summary.source_count >= 12
    assert inventory.summary.metadata_only_sources >= 10
    assert inventory.summary.raw_or_asset_sources == 0
    assert inventory.summary.selected_domain == "none"
    assert inventory.summary.selected_pivot == "none"
    assert inventory.summary.code_change_readiness == "blocked"
    assert inventory.summary.next_ticket == "RE-294"
    assert inventory.summary.next_topic == "evidence-source-gap-ranking"

    by_id = {row.source_id: row for row in inventory.sources}
    assert by_id["repo-function-map"].row_or_file_count == 1250
    assert by_id["function-priority"].row_or_file_count == 348
    assert by_id["proof-audits"].row_or_file_count >= 34
    assert by_id["callsite-maps"].row_or_file_count >= 13
    assert by_id["equivalence-gates"].row_or_file_count >= 7
    assert by_id["source-corpus"].row_or_file_count >= 300
    assert by_id["story-tracker"].progression_status == "available"
    assert all(row.safety_class != "raw-or-asset" for row in inventory.sources)


def test_re293_outputs_metadata_only_inventory_story_and_handoff(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    inventory = build_inventory(repo)
    written = write_all_artifacts(inventory, tmp_path)

    assert set(written) == {"inventory_csv", "summary_csv", "handoff_csv", "md", "story"}

    rows = list(csv.DictReader(written["inventory_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == inventory.summary.source_count
    assert [row["source_id"] for row in rows] == sorted(row["source_id"] for row in rows)
    assert all(row["safety_class"] in {"metadata-only", "source-symbolic"} for row in rows)

    summary = list(csv.DictReader(written["summary_csv"].open(newline="", encoding="utf-8")))[0]
    assert summary["next_ticket"] == "RE-294"
    assert summary["next_topic"] == "evidence-source-gap-ranking"
    assert summary["code_change_readiness"] == "blocked"

    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))[0]
    assert handoff["selected_domain"] == "none"
    assert handoff["stop_condition"] == "rank existing safe evidence sources before opening a new proof domain"

    md = written["md"].read_text(encoding="utf-8")
    assert "# RE-293 evidence source inventory" in md
    assert "## Evidence source inventory" in md
    assert "Raw/asset sources admitted: `0`" in md
    assert "No production source or marker change is authorized" in md

    story = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story
    assert "- [x] RE-292 blocked handoff validated." in story
    assert "## Next objective" in story
    assert "RE-294" in story

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
