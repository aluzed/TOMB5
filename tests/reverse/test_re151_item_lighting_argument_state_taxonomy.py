from pathlib import Path
import csv

from scripts.reverse.re151_item_lighting_argument_state_taxonomy import (
    build_item_lighting_argument_state_taxonomy,
    write_all_artifacts,
)


def test_re151_consumes_re150_callsites_and_classifies_argument_state_shapes():
    repo = Path(__file__).resolve().parents[2]
    taxonomy = build_item_lighting_argument_state_taxonomy(repo)

    assert taxonomy.story_id == "RE-151"
    assert taxonomy.upstream_ticket == "RE-150"
    assert taxonomy.cluster == "item-lighting-interaction"
    assert taxonomy.next_ticket == "RE-152"
    assert taxonomy.code_change_ready_count == 0
    assert taxonomy.marker_ready_count == 0
    assert [row.shape_id for row in taxonomy.rows] == [
        "shape-item-lighting-alert-light-parameters",
        "shape-item-lighting-void-torch-update",
    ]
    alert = taxonomy.rows[0]
    torch = taxonomy.rows[1]
    assert alert.site_count == 1
    assert alert.argument_kinds == "position-color-room-arguments"
    assert "alert-light-state" in alert.state_fields
    assert "dynamic-light-state" in alert.state_fields
    assert "room-light-state" in alert.state_fields
    assert torch.site_count == 1
    assert torch.argument_kinds == "void"
    assert "torch-item-state" in torch.state_fields
    assert all(row.patch_ready == "no" for row in taxonomy.rows)


def test_re151_outputs_metadata_only_artifacts_and_progress_tracker(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    taxonomy = build_item_lighting_argument_state_taxonomy(repo)
    written = write_all_artifacts(taxonomy, tmp_path)

    rows = list(csv.DictReader(written["taxonomy_csv"].open(newline="", encoding="utf-8")))
    assert [row["shape_id"] for row in rows] == [
        "shape-item-lighting-alert-light-parameters",
        "shape-item-lighting-void-torch-update",
    ]
    assert all(row["patch_ready"] == "no" for row in rows)
    assert all(row["source_backed"] == "source-callsite-only" for row in rows)
    assert any("position-color-room-arguments" in row["argument_kinds"] for row in rows)
    assert any("void" == row["argument_kinds"] for row in rows)

    story_text = written["story"].read_text(encoding="utf-8")
    assert "## Progress tracker" in story_text
    assert "RE-150 callsite map consumed" in story_text
    assert "Argument and state taxonomy emitted" in story_text
    assert "code change readiness: `blocked`" in story_text
    assert "RE-152" in story_text
    assert "test_re151_item_lighting_argument_state_taxonomy.py" in story_text
    assert "object-interaction" not in story_text.lower()
    assert "gameplay-mixed" not in story_text.lower()
    assert "test_re142" not in story_text.lower()

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "payload" not in text
        assert "opcode" not in text
        assert "raw call target" not in text
        assert "machine word" not in text
        assert "0x" not in text
