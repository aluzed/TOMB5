import csv
import shutil
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


@pytest.mark.parametrize(
    ('module_name', 'story_id', 'candidate_id', 'rank', 'next_ticket', 'next_topic'),
    [
        ('re474_mapped_callee_bridge_readiness_gate', 'RE-474', 'c9a7379cc772', '39', 'RE-475', 'ghidra-second-window-next-candidate-selection'),
        ('re475_ghidra_second_window_next_candidate_selection', 'RE-475', 'd9f849d5d0c1', '40', 'RE-476', 'ghidra-second-window-rank-40-narrow-export'),
        ('re476_ghidra_second_window_rank_40_narrow_export', 'RE-476', 'd9f849d5d0c1', '40', 'RE-477', 'mapped-callee-bridge-readiness-gate'),
        ('re477_mapped_callee_bridge_readiness_gate', 'RE-477', 'd9f849d5d0c1', '40', 'RE-478', 'ghidra-second-window-next-candidate-selection'),
        ('re478_ghidra_second_window_next_candidate_selection', 'RE-478', '85322d1b32c0', '41', 'RE-479', 'ghidra-second-window-rank-41-narrow-export'),
        ('re479_ghidra_second_window_rank_41_narrow_export', 'RE-479', '85322d1b32c0', '41', 'RE-480', 'mapped-caller-callee-bridge-readiness-gate'),
        ('re480_mapped_caller_callee_bridge_readiness_gate', 'RE-480', '85322d1b32c0', '41', 'RE-481', 'ghidra-second-window-next-candidate-selection'),
        ('re481_ghidra_second_window_next_candidate_selection', 'RE-481', 'b2bc06730403', '42', 'RE-482', 'ghidra-second-window-rank-42-narrow-export'),
        ('re482_ghidra_second_window_rank_42_narrow_export', 'RE-482', 'b2bc06730403', '42', 'RE-483', 'mapped-callee-bridge-readiness-gate'),
        ('re483_mapped_callee_bridge_readiness_gate', 'RE-483', 'b2bc06730403', '42', 'RE-484', 'ghidra-second-window-next-candidate-selection'),
        ('re484_ghidra_second_window_next_candidate_selection', 'RE-484', 'bc923a17e1b0', '43', 'RE-485', 'ghidra-second-window-rank-43-narrow-export'),
        ('re485_ghidra_second_window_rank_43_narrow_export', 'RE-485', 'bc923a17e1b0', '43', 'RE-486', 'mapped-callee-bridge-readiness-gate'),
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
        're474_mapped_callee_bridge_readiness_gate',
        're475_ghidra_second_window_next_candidate_selection',
        're476_ghidra_second_window_rank_40_narrow_export',
        're477_mapped_callee_bridge_readiness_gate',
        're478_ghidra_second_window_next_candidate_selection',
        're479_ghidra_second_window_rank_41_narrow_export',
        're480_mapped_caller_callee_bridge_readiness_gate',
        're481_ghidra_second_window_next_candidate_selection',
        're482_ghidra_second_window_rank_42_narrow_export',
        're483_mapped_callee_bridge_readiness_gate',
        're484_ghidra_second_window_next_candidate_selection',
        're485_ghidra_second_window_rank_43_narrow_export',
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
        ('re474_mapped_callee_bridge_readiness_gate', 'safe_context_status', 'source-backed'),
        ('re475_ghidra_second_window_next_candidate_selection', 'safe_context_status', 'source-backed'),
        ('re476_ghidra_second_window_rank_40_narrow_export', 'candidate_level_proof_count', '1'),
        ('re477_mapped_callee_bridge_readiness_gate', 'safe_context_status', 'source-backed'),
        ('re478_ghidra_second_window_next_candidate_selection', 'safe_context_status', 'source-backed'),
        ('re479_ghidra_second_window_rank_41_narrow_export', 'candidate_level_proof_count', '1'),
        ('re480_mapped_caller_callee_bridge_readiness_gate', 'safe_context_status', 'source-backed'),
        ('re481_ghidra_second_window_next_candidate_selection', 'safe_context_status', 'source-backed'),
        ('re482_ghidra_second_window_rank_42_narrow_export', 'candidate_level_proof_count', '1'),
        ('re483_mapped_callee_bridge_readiness_gate', 'safe_context_status', 'source-backed'),
        ('re484_ghidra_second_window_next_candidate_selection', 'safe_context_status', 'source-backed'),
        ('re485_ghidra_second_window_rank_43_narrow_export', 'candidate_level_proof_count', '1'),
    ],
)
def test_metadata_handoff_rejects_safety_field_drift(module_name, field, value, tmp_path):
    module = __import__(f'scripts.reverse.{module_name}', fromlist=['build', 'write'])
    with pytest.raises(ValueError, match='output safety drift'):
        module.write(dict(module.build(REPO), **{field: value}), tmp_path)


def test_selection_rejects_ranked_candidate_drift(monkeypatch):
    from scripts.reverse import re474_re479_metadata_handoff as batch

    monkeypatch.setattr(batch, 'ranked_candidate', lambda _repo, _rank: None)
    with pytest.raises(ValueError, match='ranked candidate drift'):
        batch.build('RE-475', REPO)


@pytest.mark.parametrize('field, replacement', [
    ('safe_context_status', 'source-backed'),
    ('candidate_level_proof_count', '1'),
    ('ready_to_reopen_domain_count', '1'),
])
def test_initial_upstream_handoff_rejects_safety_drift(tmp_path, field, replacement):
    from scripts.reverse import re474_re479_metadata_handoff as batch

    upstream = tmp_path / 'docs/reverse/generated/re473-ghidra-second-window-rank-39-narrow-export-handoff.csv'
    upstream.parent.mkdir(parents=True)
    shutil.copy2(REPO / 'docs/reverse/generated/re473-ghidra-second-window-rank-39-narrow-export-handoff.csv', upstream)
    with upstream.open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = reader.fieldnames
    assert fields and len(rows) == 1
    rows[0][field] = replacement
    with upstream.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)

    with pytest.raises(ValueError, match=field):
        batch.build('RE-474', tmp_path)


def _copy_reverse_handoffs(tmp_path):
    source = REPO / 'docs/reverse'
    target = tmp_path / 'docs/reverse'
    shutil.copytree(source, target)
    return target / 'generated'


@pytest.mark.parametrize('ticket, field, replacement', [
    ('RE-480', 'safe_context_status', 'source-backed'),
    ('RE-480', 'candidate_level_proof_count', '1'),
    ('RE-480', 'ready_to_reopen_domain_count', '1'),
    ('RE-480', 'source_patch_authorized_count', '1'),
    ('RE-480', 'selected_domain', 'reopened-domain'),
    ('RE-480', 'selected_pivot', 'reopened-pivot'),
    ('RE-481', 'source_backed_callsite_count', '1'),
    ('RE-481', 'repository_symbol_direct_proof_count', '1'),
    ('RE-481', 'code_change_readiness', 'ready'),
    ('RE-482', 'safe_context_status', 'source-backed'),
    ('RE-483', 'candidate_level_proof_count', '1'),
    ('RE-484', 'source_patch_authorized_count', '1'),
    ('RE-485', 'selected_domain', 'reopened-domain'),
])
def test_batch_upstream_handoffs_reject_each_applicable_safety_drift(tmp_path, ticket, field, replacement):
    from scripts.reverse import re480_re485_metadata_handoff as batch

    _copy_reverse_handoffs(tmp_path)
    config = batch.CONFIG[ticket]
    upstream = batch.upstream_path(tmp_path, ticket, config)
    with upstream.open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = reader.fieldnames
    assert fields and len(rows) == 1 and field in rows[0]
    rows[0][field] = replacement
    with upstream.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)

    with pytest.raises(ValueError, match=field):
        batch.build(ticket, tmp_path)


@pytest.mark.parametrize('ticket, mutation, expected', [
    ('RE-480', 'schema', 'handoff schema drift'),
    ('RE-481', 'rows', 'handoff row-count drift'),
    ('RE-482', 'linkage', 'handoff drift: next_ticket'),
    ('RE-483', 'schema', 'handoff schema drift'),
    ('RE-484', 'rows', 'handoff row-count drift'),
    ('RE-485', 'linkage', 'handoff drift: next_ticket'),
])
def test_batch_upstream_handoffs_reject_schema_row_and_linkage_drift(tmp_path, ticket, mutation, expected):
    from scripts.reverse import re480_re485_metadata_handoff as batch

    _copy_reverse_handoffs(tmp_path)
    config = batch.CONFIG[ticket]
    upstream = batch.upstream_path(tmp_path, ticket, config)
    with upstream.open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = reader.fieldnames
    assert fields and len(rows) == 1
    if mutation == 'schema':
        fields = fields[:-1]
        rows = [{key: value for key, value in rows[0].items() if key in fields}]
    elif mutation == 'rows':
        rows.append(dict(rows[0]))
    else:
        rows[0]['next_ticket'] = 'RE-999'
    with upstream.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)

    with pytest.raises(ValueError, match=expected):
        batch.build(ticket, tmp_path)


@pytest.mark.parametrize('ticket', ('RE-481', 'RE-484'))
def test_batch_selections_reject_ranked_candidate_drift(monkeypatch, ticket):
    from scripts.reverse import re480_re485_metadata_handoff as batch

    monkeypatch.setattr(batch, 'ranked_candidate', lambda _repo, _rank: None)
    with pytest.raises(ValueError, match='ranked candidate drift'):
        batch.build(ticket, REPO)
