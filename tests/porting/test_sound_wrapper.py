"""Actual Linux32 SFX TU wrapper contract; explicit PlaySample boundary double.

No game data, target bytes, or audio hardware. objcopy weakens only the callee
symbol on a private object, letting a strongly defined recording double replace
it without copying the wrapper or editing the production translation unit.
"""
import json
from pathlib import Path
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[2]
HARNESS = r'''
#include "SFX.H"
#include <stdio.h>
#include <stdlib.h>
int GtSFXEnabled;
static int calls, result, captured[7];
int PlaySample(int a, int b, int c, int d, int e, int f, int g) {
    int values[7] = {a,b,c,d,e,f,g};
    for (int i=0;i<7;++i) captured[i]=values[i];
    ++calls;
    printf("CALL [%d,%d,%d,%d,%d,%d,%d]\n",a,b,c,d,e,f,g);
    fflush(stdout);
    return result;
}
int main(int argc, char **argv) {
    if (argc != 9) return 2;
    int a[5];
    GtSFXEnabled=atoi(argv[1]); result=atoi(argv[2]);
    for (int i=0;i<5;++i) a[i]=atoi(argv[i+4]);
    int r=atoi(argv[3]) ? S_SoundPlaySampleLooped(a[0],a[1],a[2],a[3],a[4])
                       : S_SoundPlaySample(a[0],a[1],a[2],a[3],a[4]);
    printf("RESULT %d %d\n",r,calls);
    return 0;
}
'''


@pytest.fixture(scope='module')
def wrapper_binary(tmp_path_factory):
    out = tmp_path_factory.mktemp('sound-wrapper')
    harness = out / 'harness.cpp'
    harness.write_text(HARNESS)
    obj = out / 'sfx.o'
    binary = out / 'wrapper'
    flags = ['-m32', '-O0', '-std=c++11', '-fpermissive', '-Wno-narrowing',
             '-ffunction-sections', '-fdata-sections', '-DPSX_VERSION=1',
             '-DPSXPC_TEST=1', '-DUSE_32_BIT_ADDR=1', '-DDISC_VERSION=1',
             '-DDEBUG_VERSION=0', '-DBETA_VERSION=0', '-DNTSC_VERSION=1', '-DRELOC=0']
    includes = [f'-I{ROOT / name}' for name in ('SPEC_PSXPC_N', 'GAME', 'EMULATOR')]
    subprocess.run(['c++', *flags, *includes, '-c', str(ROOT / 'SPEC_PSXPC_N/SFX.C'),
                    '-o', str(obj)], check=True, capture_output=True, text=True, timeout=30)
    subprocess.run(['objcopy', '--weaken-symbol=_Z10PlaySampleiiiiiii', str(obj)],
                   check=True, capture_output=True, timeout=10)
    subprocess.run(['c++', *flags, *includes, str(harness), str(obj),
                    '-Wl,--gc-sections', '-o', str(binary)], check=True,
                   capture_output=True, text=True, timeout=30)
    # This is a real i386 executable, not the source's unsafe LP64 layout.
    assert binary.read_bytes()[:6] == b'\x7fELF\x01\x01'
    return binary


@pytest.mark.parametrize('looped', [0, 1])
@pytest.mark.parametrize('enabled', [0, 1, -1])
@pytest.mark.parametrize('args', [(0, 7296, 9728, 0, 0),
                                  (7, 1234, 15360, -21, 77),
                                  (1, 0, -64, 9, 13)])
@pytest.mark.parametrize('result', [-3, -2, -1, 0, 7])
def test_actual_wrapper_forwards_and_returns(wrapper_binary, looped, enabled, args, result):
    run = subprocess.run([str(wrapper_binary), str(enabled), str(result), str(looped),
                          *map(str, args)], capture_output=True, text=True, timeout=3)
    # A captured CALL does not constitute successful return from the wrapper.
    assert run.returncode == 0, (run.returncode, run.stdout, run.stderr)
    lines = run.stdout.splitlines()
    calls = [json.loads(line.removeprefix('CALL ')) for line in lines if line.startswith('CALL ')]
    expected = [args[4], args[1], args[2], args[3], 2 if looped else 1, args[0], args[2]]
    assert calls == ([expected] if enabled else [])
    assert lines[-1] == f'RESULT {result if enabled else -3} {1 if enabled else 0}'
