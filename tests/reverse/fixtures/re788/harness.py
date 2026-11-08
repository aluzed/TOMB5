"""RE788 full real TUs, normal link, fresh i386 builds; no callback substitution.
Compiler entry/exit hooks observe the actual registered adapters and bodies using
cdecl frames at -O0/-fno-omit-frame-pointer. Synthetic data; no target/gameplay claim.
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path
from zoneinfo import ZoneInfo

p = argparse.ArgumentParser()
p.add_argument('--root', type=Path, required=True)
p.add_argument('--source', choices=('current', 'baseline'), required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--ubsan', action='store_true')
a = p.parse_args()
root, out = a.root.resolve(), a.output.resolve()
out.mkdir(parents=True, exist_ok=False)
manifest = {'source': a.source, 'ubsan': a.ubsan, 'compilations': []}


def save():
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2))


def run(argv, name, timeout=25):
    now = datetime.datetime.now(ZoneInfo('Europe/Paris'))
    start = time.monotonic()
    result = subprocess.run(argv, cwd=root, capture_output=True, text=True, timeout=timeout,
                            env={**os.environ, 'UBSAN_OPTIONS': 'halt_on_error=1:print_stacktrace=1'})
    (out / f'{name}.stdout').write_text(result.stdout)
    (out / f'{name}.stderr').write_text(result.stderr)
    entry = {'argv': argv, 'exit': result.returncode, 'paris_started': now.isoformat(),
             'elapsed_seconds': time.monotonic() - start, 'timeout_seconds': timeout}
    return result, entry


source = root / 'SPEC_PSXPC_N/GETSTUFF.C'
if a.source == 'baseline':
    source = out / 'GETSTUFF.C'
    result, manifest['extraction'] = run(['git', 'show', '243c16ac:SPEC_PSXPC_N/GETSTUFF.C'], 'baseline-extraction')
    source.write_text(result.stdout)
    save()
    if result.returncode:
        raise SystemExit(result.returncode)
flags = ['g++', '-m32', '-std=c++17', '-O0', '-Wno-narrowing', '-ffunction-sections',
         '-fdata-sections', '-fno-pie', '-no-pie', '-fno-omit-frame-pointer', '-fno-optimize-sibling-calls',
         '-DPSX_VERSION=1', '-DPSXPC_TEST=1', '-DNTSC_VERSION=1', '-DUSE_32_BIT_ADDR=1',
         '-DDEBUG_VERSION=0', '-DDISC_VERSION=1', '-IGAME', '-ISPEC_PSXPC_N', '-IEMULATOR', '-I/usr/include/SDL2']
san = ['-fsanitize=undefined', '-fno-sanitize-recover=all'] if a.ubsan else []
manifest['flags'] = flags + san
srcs = [('host', Path(__file__).with_name('roof_registration.cpp')), ('getstuff', source),
        ('collide', root / 'SPEC_PSXPC_N/COLLIDE_S.C'), ('objects', root / 'GAME/OBJECTS.C'),
        ('setup', root / 'GAME/SETUP.C'), ('callbacks', root / 'GAME/BRIDGE_CALLBACKS.C')]
manifest['inputs'] = {str(s): hashlib.sha256(s.read_bytes()).hexdigest() for _, s in srcs}
# Include header hashes so a successful fresh build cannot conceal header drift.
manifest['headers'] = {str(h.relative_to(root)): hashlib.sha256(h.read_bytes()).hexdigest()
                       for directory in ('GAME', 'SPEC_PSXPC_N', 'EMULATOR')
                       for h in (root / directory).rglob('*') if h.is_file() and h.suffix.lower() == '.h'}
objects = []
for name, src in srcs:
    obj = out / (name + '.o')
    instrumentation = ['-finstrument-functions'] if name in ('objects', 'callbacks') else []
    result, entry = run(flags + san + instrumentation + ['-c', str(src), '-o', str(obj)], name)
    manifest['compilations'].append(entry)
    save()
    if result.returncode:
        print(result.stderr)
        raise SystemExit(result.returncode)
    objects.append(str(obj))
exe = out / 'roof_registration'
result, manifest['link'] = run(['g++', '-m32', '-no-pie', *san, '-Wl,--gc-sections', *objects, '-o', str(exe)], 'link')
save()
if result.returncode:
    print(result.stderr)
    raise SystemExit(result.returncode)
manifest['binary_sha256'] = hashlib.sha256(exe.read_bytes()).hexdigest()
result, manifest['run'] = run([str(exe)], 'native', timeout=20)
save()
rows, registrations, summary = [], [], None
for line in result.stdout.splitlines():
    if line.startswith('ROW '):
        rows.append([int(x) for x in line.split()[1:]])
    elif line.startswith('REG '):
        registrations.append(dict(zip(('loaded', 'records', 'neighbors', 'full_objects', 'bones', 'other_state', 'globals'),
                                      (int(x) for x in line.split()[1:]))))
    elif line.startswith('SUMMARY '):
        summary = dict(zip(('cases', 'input_differences', 'result_differences', 'state_failures'),
                           (int(x) for x in line.split()[1:])))
(out / 'evidence.json').write_text(json.dumps(dict(rows=rows, registrations=registrations, summary=summary)))
print(json.dumps({'output': str(out), 'source': a.source, 'ubsan': a.ubsan, 'exit': result.returncode,
                  'registrations': registrations, 'summary': summary}))
if result.stderr:
    print(result.stderr)
raise SystemExit(result.returncode)
