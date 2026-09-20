"""Full CAMERA.C i386 mgLOS against synthetic geometry contracts.

The 111 fixtures contain constructed coordinates and symbolic service events,
not game assets, target bytes, instruction traces or addresses. Expected values
were obtained from authenticated target execution with explicit geometry service
doubles and checked by an independent integer MIPS interpreter (20 Sep 2026).
This regression does not execute the target, real geometry or gameplay.
"""
import hashlib
import json
from pathlib import Path
import subprocess
from datetime import datetime, timezone

import pytest

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / 'tests/porting/mglos_synthetic.jsonl'
ROWS = [json.loads(line) for line in FIXTURE.read_text().splitlines()]


def invoke(argv, out, label, input_text=None):
    start = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(argv, cwd=ROOT, input=input_text, text=True,
                            capture_output=True, timeout=60)
    (out / (label + '.json')).write_text(json.dumps(dict(
        argv=list(map(str, argv)), start=start,
        end=datetime.now(timezone.utc).isoformat(), exit=result.returncode,
        stdout=result.stdout, stderr=result.stderr), indent=2))
    return result


@pytest.fixture(scope='module')
def native_rows(tmp_path_factory):
    assert len(ROWS) == 111
    assert len({row['case']['name'] for row in ROWS}) == 111
    out = tmp_path_factory.mktemp('mglos')
    sources = [ROOT / name for name in ('GAME/CAMERA.C', 'tests/porting/mglos_harness.cpp')]
    (out / 'sources.json').write_text(json.dumps({str(p.relative_to(ROOT)):
        hashlib.sha256(p.read_bytes()).hexdigest() for p in [*sources, FIXTURE]}, indent=2))
    flags = ['-m32', '-std=c++11', '-DPSXPC_TEST=1', '-DPSX_VERSION=1',
             '-O0', '-fpermissive', '-fwrapv', '-ffunction-sections', '-fdata-sections',
             '-I/usr/include/SDL2', '-ISPEC_PSXPC_N', '-IGAME', '-IEMULATOR']
    objects = []
    for index, source in enumerate(sources):
        obj = out / f'{index}.o'
        result = invoke(['g++', *flags, '-MMD', '-MF', str(out / f'{index}.d'),
                         '-c', str(source), '-o', str(obj)], out, f'compile-{index}')
        assert result.returncode == 0, result.stderr
        objects.append(str(obj))
    binary = out / 'mglos'
    result = invoke(['g++', '-m32', *objects, '-Wl,--gc-sections', '-o', str(binary)], out, 'link')
    assert result.returncode == 0, result.stderr
    header = binary.read_bytes()[:20]
    assert header[:6] == b'\x7fELF\x01\x01' and header[18:20] == b'\x03\x00'
    lines = []
    for row in ROWS:
        c = row['case']
        heights = [c['h'][min(i, len(c['h']) - 1)] for i in range(10)]
        ceilings = [c['c'][min(i, len(c['c']) - 1)] for i in range(10)]
        lines.append(' '.join(map(str, [*c['start'], *c['dest'], c['push'],
                                      *heights, *ceilings, *c['rooms']])))
    result = invoke([str(binary)], out, 'run', '\n'.join(lines) + '\n')
    assert result.returncode == 0, result.stderr
    outputs = [json.loads(line) for line in result.stdout.splitlines()]
    assert len(outputs) == len(ROWS)
    return outputs


@pytest.mark.parametrize('index', range(111), ids=[row['case']['name'] for row in ROWS])
def test_mglos_destination_return_and_ordered_services(native_rows, index):
    assert native_rows[index] == ROWS[index]['expected']
