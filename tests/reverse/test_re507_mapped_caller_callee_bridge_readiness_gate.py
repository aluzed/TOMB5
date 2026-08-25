import csv
import shutil
import sys
from pathlib import Path
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re507_metadata_only_gate(tmp_path):
    from scripts.reverse import re507_mapped_caller_callee_bridge_readiness_gate as m

    row = m.build(REPO)
    assert (
        row['story_id'], row['selected_candidate_id'], row['selected_rank'],
        row['bridge_class'], row['next_ticket'], row['code_change_readiness'],
    ) == ('RE-507', 'bdb92ce23200', '50', 'mapped-caller-callee-bridge', 'RE-508', 'blocked')
    outputs = m.write(row, tmp_path)
    assert len(outputs) == 5
    for output in outputs:
        assert not any(fragment in output.read_text(encoding='utf-8').lower() for fragment in m.BAD)


def test_re507_rejects_upstream_and_output_drift(tmp_path):
    from scripts.reverse import re507_mapped_caller_callee_bridge_readiness_gate as m

    upstream = tmp_path / 'docs/reverse/generated/re506-ghidra-second-window-rank-50-narrow-export-handoff.csv'
    upstream.parent.mkdir(parents=True)
    shutil.copy2(REPO / 'docs/reverse/generated/re506-ghidra-second-window-rank-50-narrow-export-handoff.csv', upstream)
    with upstream.open(encoding='utf-8', newline='') as handle:
        row = next(csv.DictReader(handle))
        fields = tuple(row)
    row['source_patch_authorized_count'] = '1'
    with upstream.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerow(row)
    with pytest.raises(ValueError, match='handoff drift: source_patch_authorized_count'):
        m.build(tmp_path)
    result = m.build(REPO)
    with pytest.raises(ValueError, match='forbidden output fragment'):
        m.write(dict(result, stop_condition='unsafe 0x value'), tmp_path)
    with pytest.raises(ValueError, match='output safety drift: code_change_readiness'):
        m.write(dict(result, code_change_readiness='ready'), tmp_path)
    with pytest.raises(ValueError, match='output schema drift'):
        m.write(dict(result, call_address='metadata-only'), tmp_path)
