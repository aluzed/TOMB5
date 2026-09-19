"""Fresh full-TU i386 PSXPC_N behavior, without game assets or a game run.

LaraAboveWater, LookLeftRight and ResetLook remain actual production code.
objcopy weakens only the dispatch tables and AnimateLara on a private object;
strong, exactly typed harness doubles isolate unrelated services. No undefined
symbol suppression, copied function, fake header, or source preprocessing edit.
Target attribution is static and separate; this is not a target emulator test.
Set LARA_REARM_EVIDENCE to a fresh ignored directory to retain commands/results.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
from datetime import datetime, timezone

import pytest

ROOT = Path(__file__).resolve().parents[2]


def invoke(command, out, name):
    start = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
    (out / (name + '.json')).write_text(json.dumps(dict(
        command=list(map(str, command)), cwd=str(ROOT), start=start,
        end=datetime.now(timezone.utc).isoformat(), exit=result.returncode,
        stdout=result.stdout, stderr=result.stderr), indent=2))
    return result


@pytest.fixture(scope='module')
def rearm_binary(tmp_path_factory):
    out = Path(os.environ['LARA_REARM_EVIDENCE']) if 'LARA_REARM_EVIDENCE' in os.environ else tmp_path_factory.mktemp('lara-rearm')
    out.mkdir(parents=True, exist_ok=True)
    assert not (out / 'compile.json').exists(), 'use a fresh evidence directory'
    flags = ['-m32', '-O0', '-std=c++11', '-fpermissive', '-Wno-narrowing',
             '-ffunction-sections', '-fdata-sections', '-fno-pie',
             '-DPSX_VERSION=1', '-DPSXPC_TEST=1', '-DUSE_32_BIT_ADDR=1',
             '-DDISC_VERSION=1', '-DDEBUG_VERSION=0', '-DBETA_VERSION=0',
             '-DNTSC_VERSION=1', '-DRELOC=0']
    includes = [f'-I{ROOT / p}' for p in ('SPEC_PSXPC_N', 'GAME', 'EMULATOR')]
    includes += ['-I/usr/include/SDL2']
    source = ROOT / 'GAME/LARA.C'
    (out / 'source-identity.json').write_text(json.dumps({
        'path': str(source), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'harness_sha256': hashlib.sha256((ROOT / 'tests/porting/lara_look_rearm_harness.cpp').read_bytes()).hexdigest(),
    }, indent=2))
    obj, binary = out / 'lara.o', out / 'rearm'
    result = invoke(['c++', *flags, *includes, '-MMD', '-MF', str(out / 'lara.d'),
                     '-c', str(source), '-o', str(obj)], out, 'compile')
    assert result.returncode == 0, result.stderr
    result = invoke(['objcopy', '--weaken-symbol=lara_control_routines',
                     '--weaken-symbol=lara_collision_routines',
                     '--weaken-symbol=_Z11AnimateLaraP9ITEM_INFO', str(obj)], out, 'weaken-services')
    assert result.returncode == 0, result.stderr
    result = invoke(['c++', *flags, *includes, '-no-pie',
                     str(ROOT / 'tests/porting/lara_look_rearm_harness.cpp'), str(obj),
                     '-Wl,--gc-sections', '-Wl,-Map=' + str(out / 'link.map'),
                     '-o', str(binary)], out, 'link')
    assert result.returncode == 0, result.stderr
    header = binary.read_bytes()[:20]
    assert header[:6] == b'\x7fELF\x01\x01' and header[18:20] == b'\x03\x00'
    result = invoke(['nm', '-C', str(binary)], out, 'symbols')
    assert result.returncode == 0
    for symbol in ('LaraAboveWater(ITEM_INFO*, COLL_INFO*)', 'LookLeftRight()', 'ResetLook()'):
        assert symbol in result.stdout
    return binary, out


@pytest.mark.parametrize('initial', [0, 1])
@pytest.mark.parametrize('keys', [0, 4, 8, 512, 512 | 4, 512 | 8, 512 | 4 | 8])
@pytest.mark.parametrize('inhibit', [0, 1])
@pytest.mark.parametrize('neighbors', [0, 65531, 43690, 21841])
def test_rearm_before_control_preserves_look_timing(rearm_binary, initial, keys, inhibit, neighbors):
    binary, out = rearm_binary
    result = invoke([str(binary), str(initial), str(keys), str(inhibit), str(neighbors), '0'],
                    out, f'case-{initial}-{keys}-{inhibit}-{neighbors}')
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize('neighbors', [0, 65531, 43690, 21841])
def test_inhibition_recovers_over_three_frames(rearm_binary, neighbors):
    binary, out = rearm_binary
    result = invoke([str(binary), '1', '520', '1', str(neighbors), '1'], out, f'sequence-{neighbors}')
    assert result.returncode == 0, result.stdout + result.stderr
    assert len(result.stdout.splitlines()) == 3
