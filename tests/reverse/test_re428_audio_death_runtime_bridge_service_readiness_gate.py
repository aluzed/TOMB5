import shutil
from pathlib import Path

import pytest

from scripts.reverse.re428_audio_death_runtime_bridge_service_readiness_gate import build, write


def test_re428_blocks_source_changes_without_candidate_proof(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    result = build(repo)

    assert result['selected_candidate_id'] == '61b63f61c1fd'
    assert result['selected_subcluster'] == 'audio-death-runtime-bridge-service'
    assert result['candidate_level_proof_count'] == '0'
    assert result['code_change_readiness'] == 'blocked'
    assert result['next_ticket'] == 'RE-429'

    outputs = write(result, tmp_path)
    forbidden = ('0x', 'fun_', 'sub_', 'word_le_hex', 'payload_offset', 'opcode')
    assert outputs
    assert all(not any(token in path.read_text(encoding='utf-8').lower() for token in forbidden) for path in outputs)


@pytest.mark.parametrize(
    ('field', 'unsafe_value'),
    (
        ('ready_to_reopen_domain_count', '1'),
        ('source_patch_authorized_count', '1'),
        ('code_change_readiness', 'ready'),
    ),
)
def test_re428_rejects_upstream_safety_gate_drift(tmp_path, field, unsafe_value):
    repo = Path(__file__).resolve().parents[2]
    source = repo / 'docs/reverse/generated/re427-ghidra-second-window-rank-28-narrow-export-handoff.csv'
    target = tmp_path / 'docs/reverse/generated/re427-ghidra-second-window-rank-28-narrow-export-handoff.csv'
    target.parent.mkdir(parents=True)
    shutil.copy2(source, target)
    text = target.read_text(encoding='utf-8')
    header, row = text.splitlines()
    columns = header.split(',')
    values = row.split(',')
    values[columns.index(field)] = unsafe_value
    target.write_text(header + '\n' + ','.join(values) + '\n', encoding='utf-8')

    with pytest.raises(ValueError, match='safety-gate drift'):
        build(tmp_path)
