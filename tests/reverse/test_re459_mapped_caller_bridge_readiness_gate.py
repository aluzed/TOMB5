import csv
import shutil
from pathlib import Path
import pytest
from scripts.reverse.re459_mapped_caller_bridge_readiness_gate import FORBIDDEN_OUTPUT_FRAGMENTS, UPSTREAM, build, write
REPO = Path(__file__).resolve().parents[2]

def test_re459_fail_closed_gate(tmp_path):
    result = build(REPO)
    assert result['story_id'] == 'RE-459'
    assert result['selected_candidate_id'] == 'aaf42cb3b10b'
    assert result['selected_rank'] == '34'
    assert result['source_backed_callsite_count'] == '0'
    assert result['candidate_level_proof_count'] == '0'
    assert result['repository_symbol_direct_proof_count'] == '0'
    assert result['next_ticket'] == 'RE-460'
    assert result['next_topic'] == 'ghidra-second-window-next-candidate-selection'
    assert result['code_change_readiness'] == 'blocked'
    for path in write(result, tmp_path):
        assert not any(x in path.read_text(encoding='utf-8').lower() for x in FORBIDDEN_OUTPUT_FRAGMENTS)

def test_re459_rejects_unsafe_drift(tmp_path):
    upstream = tmp_path / UPSTREAM; upstream.parent.mkdir(parents=True)
    shutil.copy2(REPO / UPSTREAM, upstream)
    with upstream.open(encoding='utf-8', newline='') as f: row = next(csv.DictReader(f)); fields = tuple(row)
    row['source_patch_authorized_count'] = '1'
    with upstream.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n'); w.writeheader(); w.writerow(row)
    with pytest.raises(ValueError, match='safety-count drift'): build(tmp_path)
    with pytest.raises(ValueError, match='forbidden output fragment'): write(dict(build(REPO), stop_condition='raw binary evidence'), tmp_path)
