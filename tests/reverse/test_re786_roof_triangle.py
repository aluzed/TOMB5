"""RE-786: distinguish the two roof triangle families on the real GETSTUFF TU."""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / 'tests/reverse/fixtures/re786/run_test.py'
OUT = ROOT / 'build/reverse/re786-public-tests'
BASELINE = 'fd74fbb9'
COORDS = [(100, 200), (200, 100), (512, 512), (900, 200), (200, 900), (824, 200), (825, 200), (823, 200)]


def oracle(typ, offset, x, z):
    reverse = typ in (9, 15, 16)
    first = x + z > 1024 if reverse else z < x
    dz = -6 if first else -2
    dx = (1 if reverse else -3) if first else (-3 if reverse else 1)
    value = 3072 + (offset if offset < 16 else offset - 32) * 256
    value += z * dz // 4
    value += ((1023 - x) * dx // 4) if dx < 0 else -(x * dx // 4)
    return (value + 32768) % 65536 - 32768


@pytest.mark.parametrize('ubsan', [False, True])
@pytest.mark.parametrize('baseline', [False, True])
def test_roof_triangle_actual_tu(ubsan, baseline):
    OUT.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix='roof-', dir=OUT))
    source = ROOT / 'SPEC_PSXPC_N/GETSTUFF.C'
    if baseline:
        source = work / 'GETSTUFF.C'
        source.write_bytes(subprocess.check_output(['git', 'show', f'{BASELINE}:SPEC_PSXPC_N/GETSTUFF.C'], cwd=ROOT))
    argv = [sys.executable, '-B', str(RUN), '--root', str(ROOT), '--source', str(source), '--output', str(work / 'run')]
    if ubsan:
        argv.append('--ubsan')
    result = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, timeout=120)
    assert result.returncode == (1 if baseline else 0), result.stdout + result.stderr
    rows = re.findall(r'^ROW type=(\d+) offset=(\d+) x=(\d+) z=(\d+) result=(-?\d+) expected=(-?\d+) state=(\d) unchanged=(\d)$', result.stdout, re.M)
    expected_order = [(t, o, x, z) for t in (9, 10, 15, 16, 17, 18) for o in range(32) for x, z in COORDS]
    assert len(rows) == len(expected_order) == 1536
    failures = 0
    for row, key in zip(rows, expected_order):
        typ, offset, x, z, got, expected, state, unchanged = map(int, row)
        assert (typ, offset, x, z) == key
        assert expected == oracle(*key)
        assert state == unchanged == 1
        if baseline and typ == 10:
            assert got == oracle(9, offset, x, z)
        else:
            assert got == expected
        failures += got != expected
    assert failures == (256 if baseline else 0)
    assert f'SUMMARY cases=1536 failures={failures}' in result.stdout
    assert 'runtime error' not in result.stdout + result.stderr
