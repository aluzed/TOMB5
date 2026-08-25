import csv
import shutil
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re487_selection_is_metadata_only_and_emits_re488(tmp_path):
    from scripts.reverse import re487_ghidra_second_window_next_candidate_selection as selection

    result = selection.build(REPO)
    assert result['story_id'] == 'RE-487'
    assert result['upstream_handoff'] == 'RE-486'
    assert result['closed_candidate_id'] == 'bc923a17e1b0'
    assert result['selected_rank'] == '44'
    assert result['selected_candidate_id'] == '967dd5c009c5'
    assert result['selected_bridge_class'] == 'mapped-caller-callee-bridge'
    assert result['source_symbol_context_count'] == '8'
    assert result['next_ticket'] == 'RE-488'
    assert result['next_topic'] == 'ghidra-second-window-rank-44-narrow-export'
    assert result['code_change_readiness'] == 'blocked'
    assert result['source_patch_authorized_count'] == '0'
    for output in selection.write(result, tmp_path):
        assert not any(token in output.read_text(encoding='utf-8').lower() for token in selection.FORBIDDEN_OUTPUT_FRAGMENTS)


@pytest.mark.parametrize('field, replacement', [
    ('story_id', 'RE-999'), ('topic', 'wrong-topic'), ('upstream_handoff', 'RE-999'),
    ('selected_candidate_id', 'wrong-candidate'), ('selected_rank', '999'),
    ('selected_subcluster', 'wrong-subcluster'), ('source_symbol_context_count', '999'),
    ('bridge_class', 'wrong-bridge'), ('safe_context_status', 'source-backed'),
    ('source_backed_callsite_count', '1'), ('candidate_level_proof_count', '1'),
    ('repository_symbol_direct_proof_count', '1'), ('ready_to_reopen_domain_count', '1'),
    ('source_patch_authorized_count', '1'), ('selected_domain', 'wrong-domain'),
    ('selected_pivot', 'wrong-pivot'), ('next_ticket', 'RE-999'), ('next_topic', 'wrong-topic'),
    ('metadata_work_readiness', 'blocked'), ('code_change_readiness', 'ready'),
    ('stop_condition', 'wrong-stop'),
])
def test_re487_rejects_all_re486_upstream_drift(tmp_path, field, replacement):
    from scripts.reverse import re487_ghidra_second_window_next_candidate_selection as selection
    shutil.copytree(REPO / 'docs/reverse', tmp_path / 'docs/reverse')
    upstream = tmp_path / 'docs/reverse/generated/re486-mapped-callee-bridge-readiness-gate-handoff.csv'
    with upstream.open(encoding='utf-8', newline='') as handle:
        reader=csv.DictReader(handle); rows=list(reader); fields=reader.fieldnames
    assert fields and len(rows)==1 and field in rows[0]
    rows[0][field]=replacement
    with upstream.open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=fields,lineterminator='\n'); writer.writeheader(); writer.writerows(rows)
    with pytest.raises(ValueError, match=field):
        selection.build(tmp_path)


@pytest.mark.parametrize('mutation, expected', [('schema','handoff schema drift'), ('rows','handoff row-count drift')])
def test_re487_rejects_upstream_schema_and_row_drift(tmp_path, mutation, expected):
    from scripts.reverse import re487_ghidra_second_window_next_candidate_selection as selection
    shutil.copytree(REPO / 'docs/reverse', tmp_path / 'docs/reverse')
    upstream=tmp_path/'docs/reverse/generated/re486-mapped-callee-bridge-readiness-gate-handoff.csv'
    with upstream.open(encoding='utf-8',newline='') as handle:
        reader=csv.DictReader(handle); rows=list(reader); fields=reader.fieldnames
    if mutation=='schema':
        fields=fields[:-1]; rows=[{key:value for key,value in rows[0].items() if key in fields}]
    else: rows.append(dict(rows[0]))
    with upstream.open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=fields,lineterminator='\n'); writer.writeheader(); writer.writerows(rows)
    with pytest.raises(ValueError, match=expected): selection.build(tmp_path)


def test_re487_rejects_ranked_candidate_drift(monkeypatch):
    from scripts.reverse import re487_ghidra_second_window_next_candidate_selection as selection
    monkeypatch.setattr(selection, 'ranked_candidate', lambda _repo, _rank: None)
    with pytest.raises(ValueError, match='ranked candidate drift'):
        selection.build(REPO)
