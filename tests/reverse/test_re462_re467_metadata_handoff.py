import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
FORBIDDEN = ('raw binary', 'copyrighted asset', 'secret')


@pytest.mark.parametrize(
    ('module_name', 'story_id', 'candidate_id', 'rank', 'next_ticket', 'next_topic'),
    [
        ('re462_mapped_caller_bridge_readiness_gate', 'RE-462', 'ede72eed0265', '35', 'RE-463', 'ghidra-second-window-next-candidate-selection'),
        ('re463_ghidra_second_window_next_candidate_selection', 'RE-463', '86fb195b0e34', '36', 'RE-464', 'ghidra-second-window-rank-36-narrow-export'),
        ('re464_ghidra_second_window_rank_36_narrow_export', 'RE-464', '86fb195b0e34', '36', 'RE-465', 'mapped-callee-bridge-readiness-gate'),
        ('re465_mapped_callee_bridge_readiness_gate', 'RE-465', '86fb195b0e34', '36', 'RE-466', 'ghidra-second-window-next-candidate-selection'),
        ('re466_ghidra_second_window_next_candidate_selection', 'RE-466', 'c03793ac47a9', '37', 'RE-467', 'ghidra-second-window-rank-37-narrow-export'),
        ('re467_ghidra_second_window_rank_37_narrow_export', 'RE-467', 'c03793ac47a9', '37', 'RE-468', 'mapped-caller-callee-bridge-readiness-gate'),
    ],
)
def test_metadata_handoff_is_fail_closed(module_name, story_id, candidate_id, rank, next_ticket, next_topic, tmp_path):
    module = __import__(f'scripts.reverse.{module_name}', fromlist=['build', 'write'])
    result = module.build(REPO)
    assert result['story_id'] == story_id
    assert result['selected_candidate_id'] == candidate_id
    assert result['selected_rank'] == rank
    assert result['next_ticket'] == next_ticket
    assert result['next_topic'] == next_topic
    assert result['code_change_readiness'] == 'blocked'
    assert result['source_patch_authorized_count'] == '0'
    for output in module.write(result, tmp_path):
        content = output.read_text(encoding='utf-8').lower()
        assert not any(fragment in content for fragment in module.FORBIDDEN_OUTPUT_FRAGMENTS)


@pytest.mark.parametrize(
    'module_name',
    [
        're462_mapped_caller_bridge_readiness_gate',
        're463_ghidra_second_window_next_candidate_selection',
        're464_ghidra_second_window_rank_36_narrow_export',
        're465_mapped_callee_bridge_readiness_gate',
        're466_ghidra_second_window_next_candidate_selection',
        're467_ghidra_second_window_rank_37_narrow_export',
    ],
)
@pytest.mark.parametrize('forbidden_text', ('raw binary', 'raw evidence', 'private key material', 'source patch applied'))
def test_metadata_handoff_rejects_forbidden_output(module_name, forbidden_text, tmp_path):
    module = __import__(f'scripts.reverse.{module_name}', fromlist=['build', 'write'])
    with pytest.raises(ValueError, match='forbidden output fragment'):
        module.write(dict(module.build(REPO), stop_condition=forbidden_text), tmp_path)


@pytest.mark.parametrize(
    ('module_name', 'field', 'value'),
    [
        ('re462_mapped_caller_bridge_readiness_gate', 'safe_context_status', 'source-backed'),
        ('re463_ghidra_second_window_next_candidate_selection', 'safe_context_status', 'source-backed'),
        ('re464_ghidra_second_window_rank_36_narrow_export', 'candidate_level_proof_count', '1'),
        ('re465_mapped_callee_bridge_readiness_gate', 'safe_context_status', 'source-backed'),
        ('re466_ghidra_second_window_next_candidate_selection', 'safe_context_status', 'source-backed'),
        ('re467_ghidra_second_window_rank_37_narrow_export', 'candidate_level_proof_count', '1'),
    ],
)
def test_metadata_handoff_rejects_safety_field_drift(module_name, field, value, tmp_path):
    module = __import__(f'scripts.reverse.{module_name}', fromlist=['build', 'write'])
    with pytest.raises(ValueError, match='output safety drift'):
        module.write(dict(module.build(REPO), **{field: value}), tmp_path)
