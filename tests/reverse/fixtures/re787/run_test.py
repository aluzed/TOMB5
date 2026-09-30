"""Compile entire GETSTUFF/TRAPS TUs; exactly typed callback adapter, i386."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--root', type=Path, required=True)
p.add_argument('--source', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--ubsan', action='store_true')
a = p.parse_args()
r, s, o = a.root.resolve(), a.source.resolve(), a.output.resolve()
o.mkdir(parents=True, exist_ok=False)
h = Path(__file__).with_name('roof_callback.cpp')
t = r / 'GAME/TRAPS.C'
flags = ['g++', '-m32', '-std=c++17', '-O0', '-Wno-narrowing', '-ffunction-sections', '-fdata-sections', '-fno-pie', '-no-pie', '-DPSX_VERSION=1', '-DPSXPC_TEST=1', '-DNTSC_VERSION=1', '-DUSE_32_BIT_ADDR=1', '-DDEBUG_VERSION=0', '-DDISC_VERSION=1', '-IGAME', '-ISPEC_PSXPC_N', '-IEMULATOR', '-I/usr/include/SDL2']
san = ['-fsanitize=undefined', '-fno-sanitize-recover=all'] if a.ubsan else []
inputs = {str(x): hashlib.sha256(x.read_bytes()).hexdigest() for x in (h, s, t)}
objects = []
for name, src in [('host', h), ('source', s), ('traps', t)]:
    obj = o / (name + '.o')
    subprocess.run(flags + san + ['-c', str(src), '-o', str(obj)], cwd=r, check=True, timeout=40)
    objects.append(str(obj))
exe = o / 'roof_callback'
subprocess.run(['g++', '-m32', '-no-pie', *san, '-Wl,--gc-sections', *objects, '-o', str(exe)], cwd=r, check=True, timeout=40)
(o / 'inputs.json').write_text(json.dumps({'inputs': inputs, 'binary_sha256': hashlib.sha256(exe.read_bytes()).hexdigest(), 'flags': flags + san}, indent=2))
raise SystemExit(subprocess.run([str(exe)], cwd=r, timeout=20).returncode)
