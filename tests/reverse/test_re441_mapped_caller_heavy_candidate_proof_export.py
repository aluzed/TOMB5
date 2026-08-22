import csv
import shutil
from pathlib import Path

import pytest

from scripts.reverse.re441_mapped_caller_heavy_candidate_proof_export import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    UPSTREAM,
    build,
    write,
)

REPO = Path(__file__).resolve().parents[2]


def test_re441_emits_fail_closed_metadata_only_candidate_proof_export(tmp_path):
    result = build(REPO)
    assert result == {
        'story_id': 'RE-441',
        'topic': 'mapped-caller-heavy-candidate-proof-export',
        'upstream_handoff': 'RE-440',
        'selected_candidate_id': '0947c90b8674',
        'selected_rank': '30',
        'selected_subcluster': 'mapped-caller-heavy-readiness-gate',
        'source_symbol_context_count': '8',
        'bridge_class': 'mapped-caller-heavy',
        'safe_context_status': 'filtered-metadata-only',
        'candidate_level_proof_count': '0',
        'repository_symbol_direct_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-442',
        'next_topic': 'mapped-caller-heavy-candidate-callsite-map',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'mapped caller-heavy context has no direct candidate proof',
    }
    outputs = write(result, tmp_path)
    assert {path.name for path in outputs} == {
        're441-mapped-caller-heavy-candidate-proof-contexts.csv',
        're441-mapped-caller-heavy-candidate-proof-summary.csv',
        're441-mapped-caller-heavy-candidate-proof-handoff.csv',
        're441-mapped-caller-heavy-candidate-proof-export.md',
        'RE-441-mapped-caller-heavy-candidate-proof-export.md',
    }
    for path in outputs:
        text = path.read_text(encoding='utf-8').lower()
        assert not any(fragment in text for fragment in FORBIDDEN_OUTPUT_FRAGMENTS)
        assert 'code.wad' not in text
        assert 'gamewad.obj' not in text
        assert 'secret' not in text


def test_re441_rejects_upstream_and_output_safety_drift(tmp_path):
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

    with (REPO / UPSTREAM).open(encoding='utf-8', newline='') as handle:
        safe_row = next(csv.DictReader(handle))
        safe_fields = tuple(safe_row)
    tainted_fields = (*safe_fields, 'ghidra_entry')
    safe_row['ghidra_entry'] = 'metadata'
    with upstream.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=tainted_fields, lineterminator='\n')
        writer.writeheader()
        writer.writerow(safe_row)
    with pytest.raises(ValueError, match='handoff schema drift'):
        build(tmp_path)

    result = build(REPO)
    with pytest.raises(ValueError, match='forbidden output fragment'):
        write(dict(result, stop_condition='unsafe 0x value'), tmp_path)
    with pytest.raises(ValueError, match='output safety drift'):
        write(dict(result, code_change_readiness='ready'), tmp_path)
    with pytest.raises(ValueError, match='output schema drift'):
        write(dict(result, call_address='metadata-only'), tmp_path)
    with pytest.raises(ValueError, match='output identity drift'):
        write(dict(result, next_ticket='RE-999'), tmp_path)
