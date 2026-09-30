"""RE-784: actual TU signed base heights, both char modes and strict UBSan."""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / 'tests/reverse/fixtures/re784/run_test.py'
OUT = ROOT / 'build/reverse/re784-public-tests'
BASELINE = '73f994f0'


def run_case(source, family, unsigned_char, ubsan):
    OUT.mkdir(parents=True, exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix='signed-height-', dir=OUT)) / 'run'
    argv = [sys.executable, '-B', str(RUN), '--root', str(ROOT), '--source', str(source),
            '--output', str(output), '--family', family]
    if unsigned_char:
        argv.append('--unsigned-char')
    if ubsan:
        argv.append('--ubsan')
    return subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, timeout=120)


@pytest.mark.parametrize('family', ['floor', 'ceiling'])
@pytest.mark.parametrize('unsigned_char', [False, True])
@pytest.mark.parametrize('ubsan', [False, True])
def test_signed_height_actual_tu(family, unsigned_char, ubsan):
    result = run_case(ROOT / 'SPEC_PSXPC_N/GETSTUFF.C', family, unsigned_char, ubsan)
    assert result.returncode == 0, result.stdout + result.stderr
    rows = re.findall(r'^ROW family=(\w+) value=(-?\d+) result=(-?\d+) state=(\d) unchanged=(\d)$',
                      result.stdout, re.M)
    assert rows == [(family, str(v), str(v * 256), '1', '1') for v in range(-128, 128)]
    assert 'SUMMARY cases=256 failures=0' in result.stdout
    assert 'runtime error' not in result.stdout + result.stderr


@pytest.mark.parametrize('family', ['floor', 'ceiling'])
def test_signed_height_baseline_ubsan_red(family):
    OUT.mkdir(parents=True, exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix='baseline-', dir=OUT))
    source = directory / 'GETSTUFF.C'
    source.write_bytes(subprocess.check_output(
        ['git', 'show', f'{BASELINE}:SPEC_PSXPC_N/GETSTUFF.C'], cwd=ROOT))
    result = run_case(source, family, False, True)
    assert result.returncode == 1, result.stdout + result.stderr
    assert 'runtime error: left shift of negative value -128' in result.stderr
    assert 'SUMMARY' not in result.stdout  # fail-fast sanitizer, not a completed matrix
