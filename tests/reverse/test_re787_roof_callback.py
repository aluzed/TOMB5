"""RE787 signed roof offsets: actual GETSTUFF/TRAPS translation units, i386."""
import re
import subprocess
import sys
import tempfile
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / 'tests/reverse/fixtures/re787/run_test.py'
OUT = ROOT / 'build/reverse/re787-public-tests'
COORDS = [(100,200),(200,100),(512,512),(900,200),(200,900),(824,200),(825,200),(823,200)]


def oracle(typ, low, high, x, z):
    reverse = typ in (9,15,16)
    first = x + z > 1024 if reverse else z < x
    offset = low if first else high
    dz = -6 if first else -2
    dx = (1 if reverse else -3) if first else (-3 if reverse else 1)
    return 3072 + (offset if offset < 16 else offset - 32)*256 + z*dz//4 + (((1023-x)*dx//4) if dx < 0 else -(x*dx//4))


@pytest.mark.parametrize('baseline', [False, True])
@pytest.mark.parametrize('ubsan', [False, True])
def test_roof_offset_callback_actual_tu(baseline, ubsan):
    OUT.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix='callback-', dir=OUT))
    source = ROOT / 'SPEC_PSXPC_N/GETSTUFF.C'
    if baseline:
        source = work / 'GETSTUFF.C'
        source.write_bytes(subprocess.check_output(['git','show','243c16ac:SPEC_PSXPC_N/GETSTUFF.C'],cwd=ROOT))
    argv = [sys.executable,'-B',str(RUN),'--root',str(ROOT),'--source',str(source),'--output',str(work/'run')]
    if ubsan:
        argv.append('--ubsan')
    result = subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=110)
    (work/'stdout.log').write_text(result.stdout)
    (work/'stderr.log').write_text(result.stderr)
    assert result.returncode == (1 if baseline else 0), result.stdout[-500:] + result.stderr
    rows = re.findall(r'^ROW type=(\d+) low=(\d+) high=(\d+) x=(\d+) z=(\d+) mode=(\d+) seen=(-?\d+) input=(-?\d+) calls=(\d+) result=(-?\d+) expected=(-?\d+) state=(\d) unchanged=(\d)$', result.stdout,re.M)
    order = [(t,l,(l+17)%32,x,z,m) for t in (9,10,15,16,17,18) for l in range(32) for x,z in COORDS for m in range(5)]
    assert len(rows) == len(order) == 7680
    input_diffs = result_diffs = failures = 0
    for row,key in zip(rows,order):
        t,l,h,x,z,m,seen,incoming,calls,got,expected,state,unchanged = map(int,row)
        assert (t,l,h,x,z,m) == key
        target = oracle(t,l,h,x,z)
        expected_calls = int(m not in (0,4))
        final = 256 if m == 2 and target < 0 else target
        final = (final+32768)%65536-32768
        assert incoming == target and expected == final
        assert calls == expected_calls and state == unchanged == 1
        reverse=t in (9,15,16)
        first=x+z>1024 if reverse else z<x
        offset=l if first else h
        native_input=target+(65536 if baseline and offset>=16 else 0)
        if expected_calls:
            assert seen == native_input
        native_final=256 if m==2 and native_input<0 else native_input
        native_final=(native_final+32768)%65536-32768
        assert got==native_final
        bad_input=bool(expected_calls and seen!=target)
        bad_result=got!=final
        input_diffs+=bad_input;result_diffs+=bad_result;failures+=bad_input or bad_result
    assert input_diffs == (2304 if baseline else 0)
    assert result_diffs == (309 if baseline else 0)
    assert failures == (2304 if baseline else 0)
    assert f'SUMMARY cases=7680 failures={failures} input_diffs={input_diffs} result_diffs={result_diffs}' in result.stdout
    assert 'runtime error' not in result.stdout+result.stderr
