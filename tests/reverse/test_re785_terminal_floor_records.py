"""RE-785: terminal floor records must exclude a following allocated roof suffix."""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / 'tests/reverse/fixtures/re785/run_test.py'
OUT = ROOT / 'build/reverse/re785-public-tests'
BASELINE = '73f994f0'


def run_case(source, ubsan):
    OUT.mkdir(parents=True, exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix='terminal-floor-', dir=OUT)) / 'run'
    argv = [sys.executable, '-B', str(RUN), '--root', str(ROOT), '--source', str(source), '--output', str(output)]
    if ubsan:
        argv.append('--ubsan')
    return subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, timeout=120)


@pytest.mark.parametrize('ubsan', [False, True])
@pytest.mark.parametrize('baseline', [False, True])
def test_terminal_floor_record_actual_tu(ubsan, baseline):
    source = ROOT / 'SPEC_PSXPC_N/GETSTUFF.C'
    if baseline:
        OUT.mkdir(parents=True, exist_ok=True)
        source = Path(tempfile.mkdtemp(prefix='baseline-', dir=OUT)) / 'GETSTUFF.C'
        source.write_bytes(subprocess.check_output(['git', 'show', f'{BASELINE}:SPEC_PSXPC_N/GETSTUFF.C'], cwd=ROOT))
    result = run_case(source, ubsan)
    assert result.returncode == (1 if baseline else 0), result.stdout + result.stderr
    rows = re.findall(r'^ROW type=(\d+) terminal=(\d) slope=(\d+) result=(-?\d+) expected=(-?\d+) state=(\d) unchanged=(\d)$', result.stdout, re.M)
    assert len(rows) == 56
    expected_order = [(str(t), str(end), str(s)) for t in (2, 7, 8, 11, 12, 13, 14) for end in (0, 1) for s in (0, 1, 256, 65027)]
    assert [r[:3] for r in rows] == expected_order
    failures = 0
    for typ, terminal, slope, got, expected, state, unchanged in rows:
        oracle = 3072 if terminal == '1' else {0: 3072, 1: 3046, 256: 3000, 65027: 2625}[int(slope)]
        assert int(expected) == oracle
        assert state == unchanged == '1'
        if baseline and terminal == '1' and int(slope) != 0:
            assert int(got) == {1: 3046, 256: 3000, 65027: 2625}[int(slope)]
            failures += 1
        else:
            assert int(got) == oracle
    assert failures == (21 if baseline else 0)
    assert f'SUMMARY cases=56 failures={failures}' in result.stdout
    assert 'runtime error' not in result.stdout + result.stderr
