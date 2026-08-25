import csv
import shutil
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re489_gate_is_metadata_only_and_emits_re490(tmp_path):
    from scripts.reverse import re489_mapped_caller_callee_bridge_readiness_gate as gate

    result = gate.build(REPO)
    assert result['story_id'] == 'RE-489'
    assert result['upstream_handoff'] == 'RE-488'
    assert result['selected_candidate_id'] == '967dd5c009c5'
    assert result['selected_rank'] == '44'
    assert result['bridge_class'] == 'mapped-caller-callee-bridge'
    assert result['next_ticket'] == 'RE-490'
    assert result['next_topic'] == 'ghidra-second-window-next-candidate-selection'
    assert result['source_backed_callsite_count'] == '0'
    assert result['repository_symbol_direct_proof_count'] == '0'
    assert result['code_change_readiness'] == 'blocked'
    for output in gate.write(result, tmp_path):
        assert not any(token in output.read_text(encoding='utf-8').lower() for token in gate.FORBIDDEN_OUTPUT_FRAGMENTS)


@pytest.mark.parametrize('field, replacement', [
    ('story_id', 'RE-999'), ('topic', 'wrong-topic'), ('upstream_handoff', 'RE-999'),
    ('selected_candidate_id', 'wrong-candidate'), ('selected_rank', '999'),
    ('selected_subcluster', 'wrong-subcluster'), ('source_symbol_context_count', '999'),
    ('bridge_class', 'wrong-bridge'), ('safe_context_status', 'source-backed'),
    ('candidate_level_proof_count', '1'), ('ready_to_reopen_domain_count', '1'),
    ('source_patch_authorized_count', '1'), ('selected_domain', 'reopened-domain'),
    ('selected_pivot', 'reopened-pivot'), ('next_ticket', 'RE-999'), ('next_topic', 'wrong-topic'),
    ('metadata_work_readiness', 'blocked'), ('code_change_readiness', 'ready'), ('stop_condition', 'wrong-stop'),
])
def test_re489_rejects_every_re488_handoff_drift(tmp_path, field, replacement):
    from scripts.reverse import re489_mapped_caller_callee_bridge_readiness_gate as gate

    shutil.copytree(REPO / 'docs/reverse', tmp_path / 'docs/reverse')
    upstream = tmp_path / 'docs/reverse/generated/re488-ghidra-second-window-rank-44-narrow-export-handoff.csv'
    with upstream.open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle); rows = list(reader); fields = reader.fieldnames
    assert fields and len(rows) == 1 and field in rows[0]
    rows[0][field] = replacement
    with upstream.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n'); writer.writeheader(); writer.writerows(rows)
    with pytest.raises(ValueError, match=field):
        gate.build(tmp_path)


@pytest.mark.parametrize('mutation, expected', [('schema', 'handoff schema drift'), ('rows', 'handoff row-count drift')])
def test_re489_rejects_handoff_schema_and_row_drift(tmp_path, mutation, expected):
    from scripts.reverse import re489_mapped_caller_callee_bridge_readiness_gate as gate

    shutil.copytree(REPO / 'docs/reverse', tmp_path / 'docs/reverse')
    upstream = tmp_path / 'docs/reverse/generated/re488-ghidra-second-window-rank-44-narrow-export-handoff.csv'
    with upstream.open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle); rows = list(reader); fields = reader.fieldnames
    if mutation == 'schema':
        fields = fields[:-1]; rows = [{key: value for key, value in rows[0].items() if key in fields}]
    else:
        rows.append(dict(rows[0]))
    with upstream.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n'); writer.writeheader(); writer.writerows(rows)
    with pytest.raises(ValueError, match=expected):
        gate.build(tmp_path)
