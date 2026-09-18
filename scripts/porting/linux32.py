#!/usr/bin/env python3
"""Build and launch the provisional Linux32/PSXPC_N target, with private ledgers.

No game data is downloaded. See docs/porting/linux32.md. Outputs must be in an
ignored directory inside this checkout; existing output directories are refused.
"""
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import struct
import subprocess
import sys
import tarfile
import time

ROOT = Path(__file__).resolve().parents[2]
GLEW_SHA256 = 'd4fc82893cfb00109578d0a1a2337fb8ca335b3ceccf97b97e5cc7f08e4353e1'


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def now():
    return datetime.now().astimezone().isoformat()


def record(out, label, argv, cwd, timeout=300):
    """Record real child status; kill its entire session on a bounded timeout."""
    meta = {'argv': list(map(str, argv)), 'cwd': str(cwd), 'start': now(),
            'timeout_seconds': timeout, 'timed_out': False}
    ledger = Path(out) / (label + '.json')
    # Reserve both names before starting the child. Never overwrite evidence.
    with ledger.open('x') as f:
        json.dump(meta, f, indent=2)
    started = time.monotonic()
    with (Path(out) / (label + '.log')).open('xb') as log:
        try:
            p = subprocess.Popen(meta['argv'], cwd=cwd, stdout=log,
                                 stderr=subprocess.STDOUT, start_new_session=True)
            try:
                meta['exit'] = p.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                meta['timed_out'] = True
                os.killpg(p.pid, signal.SIGKILL)
                meta['exit'] = p.wait()
                raise
        except OSError as exc:
            meta['error'] = str(exc)
            raise
        finally:
            meta.update(end=now(), elapsed_seconds=time.monotonic() - started)
            ledger.write_text(json.dumps(meta, indent=2) + '\n')
    if meta['exit']:
        raise subprocess.CalledProcessError(meta['exit'], meta['argv'])
    return meta


def require_elf32(path):
    with Path(path).open('rb') as f:
        header = f.read(20)
    if (len(header) < 20 or header[:6] != b'\x7fELF\x01\x01'
            or struct.unpack_from('<H', header, 18)[0] != 3):
        raise ValueError(f'Expected ELF32 little-endian i386: {path}')


def check_data(directory):
    """Fail before the native parser's unchecked fopen; narrow supported CUE."""
    directory = Path(directory).resolve()
    cue = directory / 'TOMB5.CUE'
    if not cue.is_file():
        raise ValueError(f'Missing {cue}; supply your legally obtained CUE/BIN with --data-dir')
    text = cue.read_text(encoding='ascii')
    match = re.fullmatch(r'FILE "([^"\s/\\]+)" BINARY\s+TRACK 01 MODE[12]/2352\s+INDEX 01 00:00:00\s*', text)
    if not match or match[1] in ('.', '..'):
        raise ValueError('Unsupported CUE: need one quoted filename without spaces, TRACK 01 MODE1/2352 or MODE2/2352, INDEX 01 00:00:00')
    if len(match[1].encode('ascii')) > 125:
        raise ValueError('Unsupported CUE: BIN filename exceeds 125 ASCII bytes (native signed-char parser limit)')
    binary = directory / match[1]
    if not binary.is_file():
        raise ValueError(f'Missing {binary}; place the BIN named in TOMB5.CUE beside it')
    if not binary.stat().st_size or binary.stat().st_size % 2352:
        raise ValueError('BIN must contain complete 2352-byte sectors')
    return binary


def claim_output(path):
    path = Path(path).resolve()
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        raise ValueError('Output must be inside this checkout in a Git-ignored directory')
    probe = subprocess.run(['git', 'check-ignore', '-q', str(relative) + '/'], cwd=ROOT)
    if probe.returncode != 0:
        raise ValueError('Output must be Git-ignored (use build/porting/...)')
    path.mkdir(parents=True, exist_ok=False, mode=0o700)
    return path


def unpack_glew(archive, destination):
    if sha256(archive) != GLEW_SHA256:
        raise ValueError('GLEW archive SHA256 mismatch; obtain official glew-2.2.0.tgz')
    destination = Path(destination)
    # Pinned source archive; additionally refuse links and path traversal.
    with tarfile.open(archive) as tar:
        for item in tar.getmembers():
            parts = Path(item.name).parts
            if not parts or parts[0] != 'glew-2.2.0' or '..' in parts or not (item.isfile() or item.isdir()):
                raise ValueError('Unsafe GLEW archive member')
        destination.mkdir(exist_ok=False)
        tar.extractall(destination, filter='data')
    return destination / 'glew-2.2.0'


def configure_command(root, build, glew):
    return ['cmake', '-S', str(root), '-B', str(build), '-DDISC_VERSION=ON',
            '-DDEBUG_VERSION=OFF', '-DCMAKE_BUILD_TYPE=Debug',
            '-DCMAKE_C_FLAGS=-m32', '-DCMAKE_CXX_FLAGS=-m32',
            '-DCMAKE_EXE_LINKER_FLAGS=-m32', '-DCMAKE_EXPORT_COMPILE_COMMANDS=ON',
            f'-DGLEW_INCLUDE_DIR={glew}/include', f'-DGLEW_LIBRARY={glew}/lib/libGLEW.so']


def build(args):
    archive = args.glew_archive.resolve()
    if sha256(archive) != GLEW_SHA256:
        raise ValueError('GLEW archive SHA256 mismatch')
    out = claim_output(args.output)
    record(out, 'source', ['git', 'rev-parse', 'HEAD'], ROOT)
    record(out, 'source-status', ['git', 'status', '--short'], ROOT)
    record(out, 'toolchain', ['c++', '--version'], ROOT)
    record(out, 'cmake-version', ['cmake', '--version'], ROOT)
    glew = unpack_glew(archive, out / 'dependency')
    record(out, 'glew-build', ['make', '-C', str(glew), '-j' + str(args.jobs),
           'glew.lib', 'SYSTEM=linux', 'M_ARCH=i386', 'CC=gcc -m32', 'LD=gcc -m32',
           f'DIST_DIR={out}/glew-dist', 'STRIP='], ROOT)
    require_elf32(glew / 'lib/libGLEW.so')
    tree = out / 'build'
    record(out, 'configure', configure_command(ROOT, tree, glew), ROOT)
    record(out, 'build', ['cmake', '--build', str(tree), '--target',
           'TombRaiderChronicles_PSXPC_N', '-j', str(args.jobs)], ROOT)
    binary = tree / 'SPEC_PSXPC_N/MAIN'
    require_elf32(binary)
    record(out, 'libraries', ['ldd', str(binary)], ROOT)
    if 'not found' in (out / 'libraries.log').read_text():
        raise ValueError('Unresolved runtime library; inspect libraries.log and install i386 dependencies')
    for line in (out / 'libraries.log').read_text().splitlines():
        match = re.search(r'=> (/\S+)', line)
        if match:
            require_elf32(match[1])
    result = {'binary': str(binary), 'sha256': sha256(binary), 'elf': 'ELF32 i386',
              'glew_archive_sha256': sha256(archive), 'completed': now(),
              'readiness': 'build only; no runtime acceptance'}
    (out / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


def launch(args):
    binary = args.binary.resolve()
    require_elf32(binary)
    image = check_data(args.data_dir)
    out = claim_output(args.output)
    meta = {'binary': str(binary), 'binary_sha256': sha256(binary),
            'data_dir': str(args.data_dir.resolve()), 'cue_sha256': sha256(image.parent / 'TOMB5.CUE'),
            'image_sha256': sha256(image), 'DISPLAY': os.environ.get('DISPLAY'),
            'readiness': 'exit status is not menu/gameplay validation'}
    (out / 'provenance.json').write_text(json.dumps(meta, indent=2) + '\n')
    # Native exit and GNU timeout status are separately visible in application.json.
    record(out, 'application', ['timeout', '--kill-after=2s', str(args.seconds) + 's', str(binary)],
           args.data_dir.resolve(), timeout=args.seconds + 5)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    b = sub.add_parser('build')
    b.add_argument('--glew-archive', type=Path, required=True)
    b.add_argument('--output', type=Path, required=True)
    b.add_argument('--jobs', type=int, default=4)
    l = sub.add_parser('launch')
    l.add_argument('--binary', type=Path, required=True)
    l.add_argument('--data-dir', type=Path, required=True)
    l.add_argument('--output', type=Path, required=True)
    l.add_argument('--seconds', type=int, default=30)
    args = parser.parse_args()
    try:
        if args.action == 'build':
            if not 1 <= args.jobs <= 64:
                raise ValueError('--jobs must be between 1 and 64')
            build(args)
        else:
            if not 1 <= args.seconds <= 300:
                raise ValueError('--seconds must be between 1 and 300')
            launch(args)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f'linux32: {exc}', file=sys.stderr)
        if isinstance(exc, subprocess.CalledProcessError):
            return exc.returncode if 0 < exc.returncode < 256 else 1
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
