import csv
import shutil
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re486_gate_is_metadata_only_and_emits_re487(tmp_path):
    from scripts.reverse import re486_mapped_callee_bridge_readiness_gate as gate

    result = gate.build(REPO)
    assert result['story_id'] == 'RE-486'
    assert result['topic'] == 'mapped-callee-bridge-readiness-gate'
    assert result['upstream_handoff'] == 'RE-485'
    assert result['selected_candidate_id'] == 'bc923a17e1b0'
    assert result['selected_rank'] == '43'
    assert result['next_ticket'] == 'RE-487'
    assert result['next_topic'] == 'ghidra-second-window-next-candidate-selection'
    assert result['safe_context_status'] == 'filtered-metadata-only'
    assert result['candidate_level_proof_count'] == '0'
    assert result['source_backed_callsite_count'] == '0'
    assert result['repository_symbol_direct_proof_count'] == '0'
    assert result['source_patch_authorized_count'] == '0'
    assert result['selected_domain'] == 'none'
    assert result['selected_pivot'] == 'none'
    assert result['code_change_readiness'] == 'blocked'
    for output in gate.write(result, tmp_path):
        text = output.read_text(encoding='utf-8').lower()
        assert not any(fragment in text for fragment in gate.FORBIDDEN_OUTPUT_FRAGMENTS)


@pytest.mark.parametrize('field, replacement', [
    ('safe_context_status', 'source-backed'),
    ('candidate_level_proof_count', '1'),
    ('ready_to_reopen_domain_count', '1'),
    ('source_patch_authorized_count', '1'),
    ('selected_domain', 'reopened-domain'),
    ('selected_pivot', 'reopened-pivot'),
    ('code_change_readiness', 'ready'),
])
def test_re486_rejects_every_applicable_upstream_safety_drift(tmp_path, field, replacement):
    from scripts.reverse import re486_mapped_callee_bridge_readiness_gate as gate

    shutil.copytree(REPO / 'docs/reverse', tmp_path / 'docs/reverse')
    upstream = tmp_path / 'docs/reverse/generated/re485-ghidra-second-window-rank-43-narrow-export-handoff.csv'
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
        gate.build(tmp_path)


@pytest.mark.parametrize('mutation, expected', [
    ('schema', 'handoff schema drift'),
    ('rows', 'handoff row-count drift'),
    ('linkage', 'handoff drift: next_ticket'),
])
def test_re486_rejects_upstream_schema_row_and_linkage_drift(tmp_path, mutation, expected):
    from scripts.reverse import re486_mapped_callee_bridge_readiness_gate as gate

    shutil.copytree(REPO / 'docs/reverse', tmp_path / 'docs/reverse')
    upstream = tmp_path / 'docs/reverse/generated/re485-ghidra-second-window-rank-43-narrow-export-handoff.csv'
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
        gate.build(tmp_path)


@pytest.mark.parametrize('field, replacement', [
    ('story_id', 'RE-999'),
    ('topic', 'wrong-topic'),
    ('selected_candidate_id', 'wrong-candidate'),
    ('selected_rank', '999'),
    ('metadata_work_readiness', 'blocked'),
    ('upstream_handoff', 'RE-999'),
    ('selected_subcluster', 'wrong-subcluster'),
    ('source_symbol_context_count', '999'),
    ('bridge_class', 'wrong-bridge'),
    ('next_topic', 'wrong-next-topic'),
    ('stop_condition', 'wrong-stop-condition'),
])
def test_re486_rejects_fixed_upstream_identity_and_context_drift(tmp_path, field, replacement):
    from scripts.reverse import re486_mapped_callee_bridge_readiness_gate as gate

    shutil.copytree(REPO / 'docs/reverse', tmp_path / 'docs/reverse')
    upstream = tmp_path / 'docs/reverse/generated/re485-ghidra-second-window-rank-43-narrow-export-handoff.csv'
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
        gate.build(tmp_path)
