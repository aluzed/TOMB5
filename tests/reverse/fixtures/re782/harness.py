"""Compile the entire selected OBJECTS.C and exercise six real bridge bodies."""
from pathlib import Path
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--root', type=Path, required=True)
parser.add_argument('--source', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--sanitize', action='store_true')
args = parser.parse_args()
root, source, output = args.root.resolve(), args.source.resolve(), args.output.resolve()
output.mkdir(parents=True, exist_ok=False)
flags = ['g++', '-m32', '-std=c++17', '-O0', '-Wno-narrowing',
         '-ffunction-sections', '-fdata-sections', '-fno-pie', '-no-pie',
         '-DPSX_VERSION=1', '-DPSXPC_TEST=1', '-DNTSC_VERSION=1',
         '-DUSE_32_BIT_ADDR=1', '-DDEBUG_VERSION=0', '-DDISC_VERSION=1',
         '-IGAME', '-ISPEC_PSXPC_N', '-IEMULATOR', '-I/usr/include/SDL2']
sanitizer = ['-fsanitize=undefined', '-fno-sanitize-recover=all'] if args.sanitize else []
for name, path in [('host', Path(__file__).with_name('bridge_contract.cpp')), ('objects', source)]:
    subprocess.run(flags + sanitizer + ['-c', str(path), '-o', str(output / (name + '.o'))],
                   cwd=root, check=True, timeout=60)
exe = output / 'bridge_contract'
subprocess.run(['g++', '-m32', '-no-pie', '-Wl,--gc-sections', *sanitizer,
                str(output / 'host.o'), str(output / 'objects.o'), '-o', str(exe)],
               cwd=root, check=True, timeout=60)
raise SystemExit(subprocess.run([str(exe)], cwd=root, timeout=30).returncode)
