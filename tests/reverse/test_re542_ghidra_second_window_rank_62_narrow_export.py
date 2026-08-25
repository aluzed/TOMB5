import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re542_rank_62_narrow_export_is_metadata_only(tmp_path):
    from scripts.reverse import re542_ghidra_second_window_rank_62_narrow_export as m
    row = m.build(REPO)
    assert (row['story_id'], row['selected_rank'], row['selected_candidate_id'], row['source_symbol_context_count'], row['next_ticket'], row['code_change_readiness']) == ('RE-542', '62', '605d53c8fbfb', '6', 'RE-543', 'blocked')
    assert len(m.write(row, tmp_path)) == 5
