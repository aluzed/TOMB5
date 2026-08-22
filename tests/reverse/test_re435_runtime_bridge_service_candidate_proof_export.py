import csv
import shutil
from pathlib import Path

import pytest

from scripts.reverse.re435_runtime_bridge_service_candidate_proof_export import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    UPSTREAM,
    build,
    write,
)

REPO = Path(__file__).resolve().parents[2]


def test_re435_emits_fail_closed_metadata_only_candidate_proof_export(tmp_path):
    result = build(REPO)
    assert result == {
        'story_id': 'RE-435',
        'topic': 'runtime-bridge-service-candidate-proof-export',
        'upstream_handoff': 'RE-434',
        'selected_candidate_id': '763c9cd0e3f7',
        'selected_rank': '29',
        'selected_subcluster': 'runtime-bridge-service',
        'source_symbol_context_count': '10',
        'candidate_level_proof_count': '0',
        'repository_symbol_direct_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-436',
        'next_topic': 'runtime-bridge-service-candidate-callsite-map',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'runtime bridge symbolic context has no direct candidate proof',
    }
    outputs = write(result, tmp_path)
    assert {path.name for path in outputs} == {
        're435-runtime-bridge-service-candidate-proof-contexts.csv',
        're435-runtime-bridge-service-candidate-proof-summary.csv',
        're435-runtime-bridge-service-candidate-proof-handoff.csv',
        're435-runtime-bridge-service-candidate-proof-export.md',
        'RE-435-runtime-bridge-service-candidate-proof-export.md',
    }
    for path in outputs:
        text = path.read_text(encoding='utf-8').lower()
        assert not any(fragment in text for fragment in FORBIDDEN_OUTPUT_FRAGMENTS)
        assert 'code.wad' not in text
        assert 'gamewad.obj' not in text
        assert 'secret' not in text
    for path in outputs[:3]:
        header = path.read_text(encoding='utf-8').splitlines()[0].lower()
        assert not any(fragment in header for fragment in FORBIDDEN_OUTPUT_FRAGMENTS)


def test_re435_write_rejects_untrusted_raw_or_unsafe_metadata(tmp_path):
    result = build(REPO)
    raw_result = dict(result, stop_condition='unsafe 0x value')
    with pytest.raises(ValueError, match='forbidden output fragment'):
        write(raw_result, tmp_path)
    unsafe_result = dict(result, code_change_readiness='ready')
    with pytest.raises(ValueError, match='output safety drift'):
        write(unsafe_result, tmp_path)


def test_re435_rejects_upstream_safety_or_identity_drift(tmp_path):
    upstream = tmp_path / UPSTREAM
    upstream.parent.mkdir(parents=True)
    shutil.copy2(REPO / UPSTREAM, upstream)
    with upstream.open(encoding='utf-8', newline='') as handle:
        row = next(csv.DictReader(handle))
        fields = tuple(row)
    row['candidate_level_proof_count'] = '1'
    with upstream.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerow(row)
    with pytest.raises(ValueError, match='safety-count drift'):
        build(tmp_path)
