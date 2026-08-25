import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re545_rank_63_narrow_export_is_metadata_only(tmp_path):
    from scripts.reverse import re545_ghidra_second_window_rank_63_narrow_export as m
    row = m.build(REPO)
    assert (row['story_id'], row['selected_rank'], row['selected_candidate_id'], row['source_symbol_context_count'], row['next_ticket'], row['code_change_readiness']) == ('RE-545', '63', '0887abf727ec', '6', 'RE-546', 'blocked')
    assert len(m.write(row, tmp_path)) == 5
