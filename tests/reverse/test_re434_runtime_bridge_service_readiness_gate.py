import csv
import shutil
from pathlib import Path

import pytest

from scripts.reverse.re434_runtime_bridge_service_readiness_gate import UPSTREAM, build, write


REPO = Path(__file__).resolve().parents[2]


def test_re434_preserves_fail_closed_runtime_bridge_gate(tmp_path):
    result = build(REPO)
    assert result['story_id'] == 'RE-434'
    assert result['selected_candidate_id'] == '763c9cd0e3f7'
    assert result['selected_subcluster'] == 'runtime-bridge-service'
    assert result['candidate_level_proof_count'] == '0'
    assert result['ready_to_reopen_domain_count'] == '0'
    assert result['source_patch_authorized_count'] == '0'
    assert result['code_change_readiness'] == 'blocked'
    assert result['next_ticket'] == 'RE-435'
    outputs = write(result, tmp_path)
    assert all(path.exists() for path in outputs)
    generated = (tmp_path / 'docs/reverse/generated/re434-runtime-bridge-service-readiness-gate-handoff.csv').read_text()
    assert '0x' not in generated
    assert 'FUN_' not in generated


def test_re434_rejects_unsafe_upstream_drift(tmp_path):
    upstream = tmp_path / UPSTREAM
    upstream.parent.mkdir(parents=True)
    shutil.copy2(REPO / UPSTREAM, upstream)
    with upstream.open(encoding='utf-8', newline='') as handle:
        row = next(csv.DictReader(handle))
        fields = tuple(row)
    row['source_patch_authorized_count'] = '1'
    with upstream.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerow(row)
    with pytest.raises(ValueError, match='safety-count drift'):
        build(tmp_path)
