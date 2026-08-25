import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re554_rank_66_narrow_export_is_metadata_only(tmp_path):
    from scripts.reverse import re554_ghidra_second_window_rank_66_narrow_export as module

    row = module.build(REPO)
    assert (row['story_id'], row['selected_rank'], row['selected_candidate_id'], row['source_symbol_context_count'], row['next_ticket'], row['code_change_readiness']) == ('RE-554', '66', '87acb47f89b8', '6', 'RE-555', 'blocked')
    assert len(module.write(row, tmp_path)) == 5
