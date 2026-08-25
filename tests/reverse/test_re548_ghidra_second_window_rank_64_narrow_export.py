import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re548_rank_64_narrow_export_is_metadata_only(tmp_path):
    from scripts.reverse import re548_ghidra_second_window_rank_64_narrow_export as m
    row = m.build(REPO)
    assert (row['story_id'], row['selected_rank'], row['selected_candidate_id'], row['source_symbol_context_count'], row['next_ticket'], row['code_change_readiness']) == ('RE-548', '64', '47d4d3877c3a', '6', 'RE-549', 'blocked')
    assert len(m.write(row, tmp_path)) == 5
