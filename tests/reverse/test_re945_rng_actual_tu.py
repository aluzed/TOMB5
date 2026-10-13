"""SOURCE-only RE945: GCC i386/C++11/O0 characterization, not a target oracle.
Requires g++ multilib and SDL2 development headers; no private inputs.
Run: python3 -m pytest -p no:cacheprovider tests/reverse/test_re945_rng_actual_tu.py
CLI: python3 tests/reverse/test_re945_rng_actual_tu.py --output ABSENT_DIRECTORY
"""
import argparse
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import uuid

ROOT = Path(__file__).resolve().parents[2]
SEEDS = (0, 1, 2, 65536, 0xD371F947, 0xffffffff)
DEBT = (2, 65536, 0xD371F947)
DOCS = ('docs/stories/RE-945-rng-source-characterization.md',
        'docs/reverse/tomb5-progress-dashboard-re945-v1.html')
MARKERS = ('SOURCE-only', 'DRAFT', '3/6', 'UBSan', 'SOURCE_UNCHANGED',
           'independent public review pending', 'no target oracle')

@contextlib.contextmanager
def mutation_lock():
    canonical = ROOT / 'build/reverse/autonomy-mutation.lock'
    override = os.environ.get('RE945_MUTATION_LOCK')
    if override:
        lock = Path(override)
        if not lock.is_absolute() or not lock.is_file():
            raise ValueError('override must name an existing absolute canonical mutex')
        origin = 'explicit canonical override'
    elif canonical.is_file():
        lock, origin = canonical, 'canonical repository mutex'
    elif (ROOT / '.git').exists():
        raise RuntimeError('canonical repository mutex missing: STOP')
    else:
        lock, origin = ROOT / '.re945-export-mutation.lock', 'per-export mutex; portability only, not canonical ownership'
    with lock.open('a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        try:
            yield str(lock), origin
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)

class Recorder:
    def __init__(self, path):
        self.path = path
        path.mkdir(parents=True, exist_ok=False)
        self.ledger = path / 'operations.jsonl'
    def event(self, **data):
        with self.ledger.open('a') as stream:
            stream.write(json.dumps(data) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
    def write(self, name, data):
        if not isinstance(data, bytes):
            data = data.encode()
        ident, start = str(uuid.uuid4()), time.time()
        self.event(uuid=ident, phase='start', argv=['write', name], cwd=str(ROOT), start=start, timeout=0)
        (self.path / name).write_bytes(data)
        self.event(uuid=ident, phase='end', exit=0, end=time.time(), duration=time.time()-start,
                   sha256=hashlib.sha256(data).hexdigest())
    def record(self, name, value):
        self.write(name, json.dumps(value, indent=2) + '\n')
    def run(self, name, args, timeout=40):
        args = list(map(str, args))
        ident, start = str(uuid.uuid4()), time.time()
        self.event(uuid=ident, phase='start', name=name, argv=args, cwd=str(ROOT), start=start, timeout=timeout)
        try:
            result = subprocess.run(args, cwd=ROOT, capture_output=True, timeout=timeout)
            rc, out, err = result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired as exc:
            rc, out, err = 124, exc.stdout or b'', exc.stderr or b''
        self.write(name+'.stdout', out)
        self.write(name+'.stderr', err)
        self.event(uuid=ident, phase='end', exit=rc, end=time.time(), duration=time.time()-start)
        return rc, out, err

def signed(value):
    value &= 0xffffffff
    return value if value < 0x80000000 else value - 0x100000000

def expected(seed):
    # This modulo32 model characterizes this compiler execution, NOT C++ UB or target semantics.
    state = signed(seed * 0x41c64e6d + 0x3039)
    s = signed(seed)
    return [[s, s], [(state >> 16) & 0x7fff, state, s],
            [signed((state >> 16) * 0x7fff), state, state]]

def rows(out):
    return [[int(value) for value in line.split()[1:]] for line in out.decode().splitlines()]

def metadata_contract():
    for path in DOCS:
        text = (ROOT / path).read_text()
        for marker in MARKERS:
            assert marker in text, (path, marker)

def execute(path):
    with mutation_lock() as mutex:
        rec = Recorder(path)
        rec.record('contract.json', dict(scope='SOURCE-only', compiler='GCC i386 C++11 O0', mutex=mutex,
            seeds=SEEDS, known_UBSan_nonzero=3, source_correction=False, target_oracle=False,
            limitations='constructed one-step seeds; signed overflow UB, implementation-dependent signed conversion/shift; strict failing cases stop in Control before Draw; full TU with gc-sections, globals supplied by harness'))
        source = ROOT / 'SPEC_PSXPC_N/MISC.C'
        original = source.read_bytes()
        rec.record('pins.json', {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [source, Path(__file__), ROOT/'tests/reverse/re945_rng_actual_tu.cpp']})
        flags = ['g++', '-m32', '-std=c++11', '-O0', '-fpermissive', '-Wno-narrowing',
                 '-ffunction-sections', '-fdata-sections', '-fno-pie', '-no-pie',
                 '-DPSX_VERSION=1', '-DPSXPC_TEST=1', '-DUSE_32_BIT_ADDR=1']
        flags += ['-I'+str(ROOT/p) for p in ('SPEC_PSXPC_N', 'GAME', 'EMULATOR')]
        flags += ['-I/usr/include/SDL2']
        def build(label, src, strict=False):
            ff = flags + (['-fsanitize=undefined', '-fno-sanitize-recover=all'] if strict else [])
            obj, exe = path/(label+'.o'), path/label
            assert rec.run(label+'-compile', ff+['-x','c++','-c',src,'-o',obj])[0] == 0
            assert rec.run(label+'-link', ff+[ROOT/'tests/reverse/re945_rng_actual_tu.cpp',obj,
                '-Wl,--gc-sections,-z,defs','-o',exe])[0] == 0
            return exe
        normal = build('normal', source)
        observations = []
        for seed in SEEDS:
            rc, out, err = rec.run('normal-'+str(seed), [normal, hex(seed)])
            actual = rows(out)
            assert rc == 0 and not err and actual == expected(seed), (seed, actual)
            # After Control, Draw state untouched; after Draw, Control state untouched.
            assert actual[1][2] == signed(seed) and actual[2][1] == actual[1][1]
            observations.append(dict(seed=seed, rows=actual, state_isolation=True))
        # Distinct initial states + re-seeding verify isolation in both directions.
        rc, out, err = rec.run('isolation', [normal, '--isolation'])
        assert rc == 0 and not err and out == b'isolation PASS\n'
        for i, args in enumerate(([], ['-1'], ['4294967296'], ['1x'], [''], ['1','2'])):
            rc, _, _ = rec.run('invalid-'+str(i), [normal]+args)
            assert rc == 2
        strict = build('strict', source, True)
        diagnostics = []
        for seed in SEEDS:
            rc, out, err = rec.run('strict-'+str(seed), [strict, hex(seed)])
            if seed in DEBT:
                assert rc == 1 and b'signed integer overflow' in err and b'MISC.C:518:' in err
                assert b'control ' not in out and b'draw ' not in out
                diagnostics.append(seed)
            else:
                assert rc == 0 and not err and rows(out) == expected(seed)
        assert len(diagnostics) == 3
        text = original.decode()
        expr = 'return (rand_2 >> 16) * 0x7FFF;'
        assert text.count(expr) == 1
        mutant = path/'mutant-MISC.C'
        rec.write(mutant.name, text.replace(expr, 'return (rand_2 >> 16) & 0x7FFF;'))
        mutant_exe = build('mutant', mutant)
        killed = []
        for seed in SEEDS:
            rc, out, err = rec.run('mutant-'+str(seed), [mutant_exe, hex(seed)])
            assert rc == 0 and not err
            actual = rows(out)
            if actual != expected(seed):
                assert actual[:2] == expected(seed)[:2] and actual[2][1:] == expected(seed)[2][1:]
                killed.append(seed)
        assert killed, 'Draw multiplication-to-mask mutant insensitive'
        assert source.read_bytes() == original, 'production source changed: STOP'
        rec.record('results.json', dict(normal_cases=6, strict_cases=6, known_diagnostics=diagnostics,
            source_mutant_detected_seeds=killed, isolation='PASS', observations=observations,
            status='SOURCE_UNCHANGED', target_oracle=False, independent_public_review='pending'))
        return 0

def test_metadata_contract():
    metadata_contract()

def test_actual_tu():
    # Temp creation is also protected; execute acquires the mutex for compilation/output.
    with mutation_lock():
        path = Path(tempfile.mkdtemp(prefix='re945-')) / 'fresh'
    execute(path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(execute(args.output.resolve()))
