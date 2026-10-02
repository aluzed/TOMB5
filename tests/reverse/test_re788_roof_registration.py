"""RE788: source-only real registration/roof/bridge integration, not gameplay proof."""
import hashlib
import itertools
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / 'tests/reverse/fixtures/re788'
ARCHIVE = ROOT / 'build/reverse/autonomy-20261002/re788-source'
TYPES = (9, 10, 15, 16, 17, 18)
# Each coordinate distinguishes the two diagonal predicates; both sides per type.
COORDS = ((200, 100), (300, 900))


def roof_oracle(typ, low, high, x, z):
    reverse = typ in (9, 15, 16)
    first = x + z > 1024 if reverse else z < x
    offset = low if first else high
    signed = offset if offset < 16 else offset - 32
    dz = -6 if first else -2
    dx = (1 if reverse else -3) if first else (-3 if reverse else 1)
    roof = 3072 + signed * 256 + z * dz // 4
    roof += (1023 - x) * dx // 4 if dx < 0 else -(x * dx // 4)
    return roof, offset


def short(value):
    return (value + 32768) % 65536 - 32768


@pytest.mark.parametrize('baseline', [False, True], ids=['current', '243c16ac'])
@pytest.mark.parametrize('ubsan', [False, True], ids=['normal', 'strict-ubsan'])
def test_actual_registered_roof_bridge_chain(baseline, ubsan):
    assert (FIXTURE / 'run_test.py').is_file(), 'RE788 actual-source runner missing'
    assert (FIXTURE / 'roof_registration.cpp').is_file(), 'RE788 integration harness missing'
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=f'{"baseline" if baseline else "current"}-{ubsan}-', dir=ARCHIVE))
    argv = [sys.executable, '-B', str(FIXTURE / 'run_test.py'), '--root', str(ROOT),
            '--source', 'baseline' if baseline else 'current', '--output', str(work / 'run')]
    if ubsan:
        argv.append('--ubsan')
    result = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, timeout=150)
    (work / 'stdout.log').write_text(result.stdout)
    (work / 'stderr.log').write_text(result.stderr)
    (work / 'invocation.json').write_text(json.dumps({'argv': argv, 'exit': result.returncode}, indent=2))
    assert result.returncode == int(baseline), result.stdout[-1500:] + result.stderr[-3000:]
    evidence = json.loads((work / 'run/evidence.json').read_text())
    assert evidence['registrations'] == [dict(loaded=l, records=1, neighbors=1, full_objects=1,
                                             bones=1, other_state=1, globals=1) for l in (0, 1)]
    keys = [(loaded, typ, low, (low + 17) % 32, x, z, fam, q, inhibited)
            for loaded, typ, low, (x, z), fam, q, inhibited in
            itertools.product((0, 1), TYPES, range(32), COORDS, range(3), (-1, 0, 1), (0, 1))]
    assert len(evidence['rows']) == len(keys) == 13824
    differences = 0
    sensitive = set()
    controls = set()
    for row, key in zip(evidence['rows'], keys):
        assert tuple(row[:9]) == key
        loaded, typ, low, high, x, z, fam, q, inhibited = key
        roof, offset = roof_oracle(typ, low, high, x, z)
        level = 4096 + (0 if fam == 0 else ((-x) & 1023) // (4 if fam == 1 else 2))
        native_roof = roof + (65536 if baseline and offset >= 16 else 0)
        calls = int(not inhibited)
        output = level + 256 if q == 1 and not inhibited else native_roof
        expected_events = 1234 if calls else 0  # adapter entry, body entry/exit, adapter exit
        sentinel = 123456
        assert row[9:] == [roof, native_roof if calls else sentinel,
                          native_roof if calls else sentinel, calls, calls,
                          output if calls else sentinel, output if calls else sentinel,
                          short(output), 1, 1, expected_events, level + q]
        # Bridge ceilings overwrite solely on query threshold: signed roof debt is visible
        # at both real entries, but is masked by narrowing or an unconditional bridge write.
        assert row[16] == short(level + 256 if q == 1 and not inhibited else roof)
        diff = bool(calls and native_roof != roof)
        differences += diff
        if diff:
            sensitive.add((loaded, typ, fam, q))
        if inhibited or offset < 16:
            controls.add((loaded, typ, fam, q, inhibited))
    expected_sensitive = set(itertools.product((0, 1), TYPES, range(3), (-1, 0, 1))) if baseline else set()
    assert sensitive == expected_sensitive
    assert controls == set(itertools.product((0, 1), TYPES, range(3), (-1, 0, 1), (0, 1)))
    assert evidence['summary'] == dict(cases=len(keys), input_differences=differences,
                                      result_differences=0, state_failures=0)
    assert bool(differences) == baseline
    manifest = json.loads((work / 'run/manifest.json').read_text())
    assert len(manifest['compilations']) == 6
    sources = [FIXTURE / 'roof_registration.cpp',
               work / 'run/GETSTUFF.C' if baseline else ROOT / 'SPEC_PSXPC_N/GETSTUFF.C',
               ROOT / 'SPEC_PSXPC_N/COLLIDE_S.C', ROOT / 'GAME/OBJECTS.C',
               ROOT / 'GAME/SETUP.C', ROOT / 'GAME/BRIDGE_CALLBACKS.C']
    assert manifest['inputs'] == {str(s): hashlib.sha256(s.read_bytes()).hexdigest() for s in sources}
    for source, compilation in zip(sources, manifest['compilations']):
        assert compilation['argv'][compilation['argv'].index('-c') + 1] == str(source)
        assert ('-finstrument-functions' in compilation['argv']) == (source.name in ('OBJECTS.C', 'BRIDGE_CALLBACKS.C'))
        assert compilation['timeout_seconds'] <= 180
    assert manifest['run']['timeout_seconds'] <= 180 and manifest['link']['timeout_seconds'] <= 180
    elf = (work / 'run/roof_registration').read_bytes()
    assert elf[:5] == b'\x7fELF\x01' and int.from_bytes(elf[18:20], 'little') == 3
    assert manifest['binary_sha256'] == hashlib.sha256(elf).hexdigest()
    assert all(c['exit'] == 0 for c in manifest['compilations'])
    assert manifest['link']['exit'] == 0 and manifest['run']['exit'] == int(baseline)
    assert '-m32' in manifest['flags'] and '-DPSX_VERSION=1' in manifest['flags'] and '-DPSXPC_TEST=1' in manifest['flags']
    assert ('-fsanitize=undefined' in manifest['flags']) == ubsan
    assert not any('unresolved-symbols' in arg for arg in manifest['link']['argv'])
    assert 'runtime error' not in (work / 'run/native.stderr').read_text()
