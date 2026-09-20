"""Actual-TU i386 GetLaraJointPos preservation with real software LIBGTE.

Synthetic inputs, not game assets, PS1 hardware or full camera validation.
The independent fixed-point position oracle covers these nonsaturating cases.
"""
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
from datetime import datetime, timezone

import pytest

ROOT = Path(__file__).resolve().parents[2]
VALUES = (0, 1, 0xfff, 0x1000, 0x1fff, 0x2000, 0x4000,
          0x7fff, 0x8000, 0x9001, 0xabcd, 0xefff, 0xf000, 0xffff)
CASES = tuple(itertools.product(VALUES, range(2), range(3)))


def invoke(argv, out, label):
    start = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True, timeout=60)
    (out / (label + '.json')).write_text(json.dumps(dict(
        argv=list(map(str, argv)), start=start,
        end=datetime.now(timezone.utc).isoformat(), exit=result.returncode,
        stdout=result.stdout, stderr=result.stderr), indent=2))
    return result


@pytest.fixture(scope='module')
def joint_rows(tmp_path_factory):
    out = tmp_path_factory.mktemp('joint-matrix')
    sources = [ROOT / path for path in ('tests/porting/joint_matrix_harness.cpp',
               'SPEC_PSXPC_N/CALCLARA.C', 'EMULATOR/LIBGTE.C')]
    (out / 'sources.json').write_text(json.dumps({str(p.relative_to(ROOT)):
        hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}, indent=2))
    flags = ['-m32', '-std=c++11', '-DPSXPC_TEST=1', '-O0', '-fpermissive',
             '-fwrapv', '-ffunction-sections', '-fdata-sections',
             '-I/usr/include/SDL2', '-ISPEC_PSXPC_N', '-IGAME', '-IEMULATOR']
    objects = []
    for index, source in enumerate(sources):
        obj = out / f'{index}.o'
        result = invoke(['g++', *flags, '-MMD', '-MF', str(out / f'{index}.d'),
                         '-c', str(source), '-o', str(obj)], out, f'compile-{index}')
        assert result.returncode == 0, result.stderr
        objects.append(str(obj))
    binary = out / 'joint-matrix'
    result = invoke(['g++', '-m32', *objects, '-Wl,--gc-sections', '-o', str(binary)], out, 'link')
    assert result.returncode == 0, result.stderr
    header = binary.read_bytes()[:20]
    assert header[:6] == b'\x7fELF\x01\x01' and header[18:20] == b'\x03\x00'
    result = invoke([str(binary)], out, 'run')
    rows = [json.loads(line) for line in result.stdout.splitlines()]
    assert [(r['value'], r['variant'], r['vector']) for r in rows] == list(CASES)
    failures = sum(not (r['restored'] and r['position'] and r['joint_unchanged']) for r in rows)
    assert result.returncode == (1 if failures else 0), result.stderr
    return {key: row for key, row in zip(CASES, rows)}


@pytest.mark.parametrize('value,variant,vector', CASES)
def test_joint_restores_matrix_and_transforms_position(joint_rows, value, variant, vector):
    row = joint_rows[value, variant, vector]
    assert row['position'] == 1, row
    assert row['joint_unchanged'] == 1, row
    assert row['restored'] == 1 and row['before'] == row['after'], row
