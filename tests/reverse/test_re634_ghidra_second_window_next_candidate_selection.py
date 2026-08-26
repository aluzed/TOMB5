import csv
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re634_selects_rank_93_metadata_only_candidate(tmp_path):
    from scripts.reverse import re634_ghidra_second_window_next_candidate_selection as module

    row = module.build(REPO)
    assert (
        row['story_id'], row['closed_candidate_id'], row['selected_rank'],
        row['selected_candidate_id'], row['selected_bridge_class'], row['next_ticket'],
        row['code_change_readiness'],
    ) == ('RE-634', 'fdae952cff84', '93', 'd0bf1556870a', 'mapped-caller-bridge', 'RE-635', 'blocked')
    assert len(module.write(row, tmp_path)) == 5


@pytest.mark.parametrize('field', (
    'story_id', 'topic', 'upstream_handoff', 'selected_candidate_id', 'selected_rank',
    'selected_subcluster', 'source_symbol_context_count', 'bridge_class',
    'safe_context_status', 'source_backed_callsite_count', 'candidate_level_proof_count',
    'repository_symbol_direct_proof_count', 'ready_to_reopen_domain_count',
    'source_patch_authorized_count', 'selected_domain', 'selected_pivot', 'next_ticket',
    'next_topic', 'metadata_work_readiness', 'code_change_readiness', 'stop_condition',
))
def test_re634_rejects_each_upstream_handoff_field_drift(tmp_path, field):
    from scripts.reverse import re634_ghidra_second_window_next_candidate_selection as module

    with (REPO / module.UPSTREAM).open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        rows, fields = list(reader), tuple(reader.fieldnames or ())
    rows[0][field] = 'drift'
    target = tmp_path / module.UPSTREAM
    target.parent.mkdir(parents=True)
    with target.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match=rf'handoff drift: {field}'):
        module.build(tmp_path)


def test_re634_rejects_ranked_candidate_drift(monkeypatch):
    from scripts.reverse import re634_ghidra_second_window_next_candidate_selection as module

    monkeypatch.setattr(module.candidate_source.candidates, 'build_bridge_candidates', lambda repo: ([], None))
    with pytest.raises(ValueError, match='ranked candidate drift'):
        module.build(REPO)


def test_re634_rejects_upstream_schema_and_row_count_drift(tmp_path):
    from scripts.reverse import re634_ghidra_second_window_next_candidate_selection as module

    target = tmp_path / module.UPSTREAM
    target.parent.mkdir(parents=True)
    target.write_text('bad_schema\nvalue\n', encoding='utf-8')
    with pytest.raises(ValueError, match='handoff schema drift'):
        module.build(tmp_path)
    valid = (REPO / module.UPSTREAM).read_text(encoding='utf-8')
    target.write_text(valid + valid.splitlines()[1] + '\n', encoding='utf-8')
    with pytest.raises(ValueError, match='handoff row-count drift'):
        module.build(tmp_path)
