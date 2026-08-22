import csv
import shutil
from pathlib import Path

import pytest

from scripts.reverse.re436_runtime_bridge_service_candidate_callsite_map import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    UPSTREAM,
    build,
    write,
)

REPO = Path(__file__).resolve().parents[2]


def test_re436_emits_fail_closed_metadata_only_callsite_map(tmp_path):
    result = build(REPO)
    assert result == {
        'story_id': 'RE-436',
        'topic': 'runtime-bridge-service-candidate-callsite-map',
        'upstream_handoff': 'RE-435',
        'selected_candidate_id': '763c9cd0e3f7',
        'selected_rank': '29',
        'selected_subcluster': 'runtime-bridge-service',
        'source_context_function_count': '10',
        'source_backed_callsite_count': '0',
        'candidate_level_proof_count': '0',
        'repository_symbol_direct_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-437',
        'next_topic': 'runtime-bridge-service-callsite-readiness-gate',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'no safe source-backed candidate callsite in metadata-only map',
    }
    outputs = write(result, tmp_path)
    assert {path.name for path in outputs} == {
        're436-runtime-bridge-service-candidate-callsite-map-callsites.csv',
        're436-runtime-bridge-service-candidate-callsite-map-summary.csv',
        're436-runtime-bridge-service-candidate-callsite-map-handoff.csv',
        're436-runtime-bridge-service-candidate-callsite-map.md',
        'RE-436-runtime-bridge-service-candidate-callsite-map.md',
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


def test_re436_write_rejects_raw_or_unsafe_metadata(tmp_path):
    result = build(REPO)
    with pytest.raises(ValueError, match='forbidden output fragment'):
        write(dict(result, stop_condition='unsafe 0x value'), tmp_path)
    with pytest.raises(ValueError, match='output safety drift'):
        write(dict(result, code_change_readiness='ready'), tmp_path)
    with pytest.raises(ValueError, match='output schema drift'):
        write(dict(result, call_address='metadata-only'), tmp_path)
    with pytest.raises(ValueError, match='output identity drift'):
        write(dict(result, next_ticket='RE-999'), tmp_path)


def test_re436_rejects_upstream_safety_or_identity_drift(tmp_path):
    upstream = tmp_path / UPSTREAM
    upstream.parent.mkdir(parents=True)
    shutil.copy2(REPO / UPSTREAM, upstream)
    with upstream.open(encoding='utf-8', newline='') as handle:
        row = next(csv.DictReader(handle))
        fields = tuple(row)
    row['repository_symbol_direct_proof_count'] = '1'
    with upstream.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerow(row)
    with pytest.raises(ValueError, match='safety-count drift'):
        build(tmp_path)
