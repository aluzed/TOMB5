"""Actual GETSTUFF TU, synthetic roof triangles only."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--root', type=Path, required=True)
parser.add_argument('--source', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--ubsan', action='store_true')
args = parser.parse_args()
root, source, output = args.root.resolve(), args.source.resolve(), args.output.resolve()
output.mkdir(parents=True, exist_ok=False)
host = Path(__file__).with_name('roof_triangle.cpp')
flags = ['g++', '-m32', '-std=c++17', '-O0', '-Wno-narrowing',
         '-ffunction-sections', '-fdata-sections', '-fno-pie', '-no-pie',
         '-DPSX_VERSION=1', '-DPSXPC_TEST=1', '-DNTSC_VERSION=1',
         '-DUSE_32_BIT_ADDR=1', '-DDEBUG_VERSION=0', '-DDISC_VERSION=1',
         '-IGAME', '-ISPEC_PSXPC_N', '-IEMULATOR', '-I/usr/include/SDL2']
san = ['-fsanitize=undefined', '-fno-sanitize-recover=all'] if args.ubsan else []
inputs = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (host, source)}
for name, path in (('host', host), ('source', source)):
    subprocess.run(flags + san + ['-c', str(path), '-o', str(output / (name + '.o'))],
                   cwd=root, check=True, timeout=60)
exe = output / 'roof_triangle'
subprocess.run(['g++', '-m32', '-no-pie', *san, '-Wl,--gc-sections',
                str(output / 'host.o'), str(output / 'source.o'), '-o', str(exe)],
               cwd=root, check=True, timeout=60)
(output / 'inputs.json').write_text(json.dumps({
    'inputs': inputs, 'binary_sha256': hashlib.sha256(exe.read_bytes()).hexdigest(),
    'flags': flags + san}, indent=2))
raise SystemExit(subprocess.run([str(exe)], cwd=root, timeout=30).returncode)
