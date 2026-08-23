import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


@pytest.mark.parametrize(
    ('module_name', 'story_id', 'candidate_id', 'rank', 'next_ticket', 'next_topic'),
    [
        ('re468_mapped_caller_callee_bridge_readiness_gate', 'RE-468', 'c03793ac47a9', '37', 'RE-469', 'ghidra-second-window-next-candidate-selection'),
        ('re469_ghidra_second_window_next_candidate_selection', 'RE-469', '6c0aef5fd528', '38', 'RE-470', 'ghidra-second-window-rank-38-narrow-export'),
        ('re470_ghidra_second_window_rank_38_narrow_export', 'RE-470', '6c0aef5fd528', '38', 'RE-471', 'mapped-callee-bridge-readiness-gate'),
        ('re471_mapped_callee_bridge_readiness_gate', 'RE-471', '6c0aef5fd528', '38', 'RE-472', 'ghidra-second-window-next-candidate-selection'),
        ('re472_ghidra_second_window_next_candidate_selection', 'RE-472', 'c9a7379cc772', '39', 'RE-473', 'ghidra-second-window-rank-39-narrow-export'),
        ('re473_ghidra_second_window_rank_39_narrow_export', 'RE-473', 'c9a7379cc772', '39', 'RE-474', 'mapped-callee-bridge-readiness-gate'),
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
        're468_mapped_caller_callee_bridge_readiness_gate',
        're469_ghidra_second_window_next_candidate_selection',
        're470_ghidra_second_window_rank_38_narrow_export',
        're471_mapped_callee_bridge_readiness_gate',
        're472_ghidra_second_window_next_candidate_selection',
        're473_ghidra_second_window_rank_39_narrow_export',
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
        ('re468_mapped_caller_callee_bridge_readiness_gate', 'safe_context_status', 'source-backed'),
        ('re469_ghidra_second_window_next_candidate_selection', 'safe_context_status', 'source-backed'),
        ('re470_ghidra_second_window_rank_38_narrow_export', 'candidate_level_proof_count', '1'),
        ('re471_mapped_callee_bridge_readiness_gate', 'safe_context_status', 'source-backed'),
        ('re472_ghidra_second_window_next_candidate_selection', 'safe_context_status', 'source-backed'),
        ('re473_ghidra_second_window_rank_39_narrow_export', 'candidate_level_proof_count', '1'),
    ],
)
def test_metadata_handoff_rejects_safety_field_drift(module_name, field, value, tmp_path):
    module = __import__(f'scripts.reverse.{module_name}', fromlist=['build', 'write'])
    with pytest.raises(ValueError, match='output safety drift'):
        module.write(dict(module.build(REPO), **{field: value}), tmp_path)


def test_metadata_handoff_rejects_ranked_candidate_drift(monkeypatch):
    from scripts.reverse import re468_re473_metadata_handoff as batch

    monkeypatch.setattr(batch, 'ranked_candidate', lambda _repo, _rank: None)
    with pytest.raises(ValueError, match='ranked candidate drift'):
        batch.build('RE-469', REPO)
