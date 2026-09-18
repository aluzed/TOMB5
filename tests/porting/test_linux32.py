"""Source-only tests for the reproducible Linux32 driver, not game acceptance."""
import importlib.util
from pathlib import Path
import struct
import subprocess
import sys
import tarfile
import io

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'scripts/porting/linux32.py'


def driver():
    spec = importlib.util.spec_from_file_location('linux32', SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def elf(path, bits=1, machine=3):
    data = bytearray(52)
    data[:6] = b'\x7fELF' + bytes([bits, 1])
    struct.pack_into('<H', data, 18, machine)
    path.write_bytes(data)
    return path


def test_elf32(tmp_path):
    driver().require_elf32(elf(tmp_path / 'app'))


@pytest.mark.parametrize('bits,machine', [(2, 62), (1, 40), (0, 3)])
def test_wrong_abi(tmp_path, bits, machine):
    with pytest.raises(ValueError, match='ELF32.*i386'):
        driver().require_elf32(elf(tmp_path / 'app', bits, machine))


def test_missing_cue(tmp_path):
    with pytest.raises(ValueError, match='TOMB5.CUE'):
        driver().check_data(tmp_path)


def cue(tmp_path, name='TOMB5.BIN', mode='MODE2/2352'):
    (tmp_path / 'TOMB5.CUE').write_text(f'FILE "{name}" BINARY\n  TRACK 01 {mode}\n    INDEX 01 00:00:00\n')


def test_missing_bin(tmp_path):
    cue(tmp_path)
    with pytest.raises(ValueError, match='TOMB5.BIN'):
        driver().check_data(tmp_path)


def test_valid_data(tmp_path):
    cue(tmp_path)
    (tmp_path / 'TOMB5.BIN').write_bytes(bytes(2352))
    assert driver().check_data(tmp_path).name == 'TOMB5.BIN'


@pytest.mark.parametrize('name,mode', [('a b.bin', 'MODE2/2352'), ('../outside.bin', 'MODE2/2352'), ('TOMB5.BIN', 'MODE1/2048')])
def test_unsupported_cue(tmp_path, name, mode):
    cue(tmp_path, name, mode)
    with pytest.raises(ValueError, match='Unsupported CUE'):
        driver().check_data(tmp_path)


def test_truncated_bin(tmp_path):
    cue(tmp_path)
    (tmp_path / 'TOMB5.BIN').write_bytes(b'x')
    with pytest.raises(ValueError, match='2352'):
        driver().check_data(tmp_path)


def test_cue_filename_boundary(tmp_path):
    name = 'a' * 125
    cue(tmp_path, name)
    (tmp_path / name).write_bytes(bytes(2352))
    assert driver().check_data(tmp_path).name == name
    name += 'b'
    cue(tmp_path, name)
    (tmp_path / name).write_bytes(bytes(2352))
    with pytest.raises(ValueError, match='125'):
        driver().check_data(tmp_path)
    binary = elf(tmp_path / 'app')
    out = subprocess.run([sys.executable, str(SCRIPT), 'launch', '--binary', str(binary), '--data-dir', str(tmp_path), '--output', str(tmp_path / 'out')], capture_output=True, text=True)
    assert out.returncode == 2 and '125' in out.stderr


def test_build_flags(tmp_path):
    argv = driver().configure_command(ROOT, tmp_path / 'build', tmp_path / 'glew')
    assert '-DCMAKE_C_FLAGS=-m32' in argv
    assert '-DCMAKE_CXX_FLAGS=-m32' in argv
    assert '-DCMAKE_EXE_LINKER_FLAGS=-m32' in argv
    assert '-DDISC_VERSION=ON' in argv
    assert '-DDEBUG_VERSION=OFF' in argv
    assert any(a.startswith('-DGLEW_LIBRARY=') for a in argv)
    assert not any('runtime-1058' in a for a in argv)


def test_wrong_archive_hash(tmp_path):
    archive = tmp_path / 'bad.tgz'
    archive.write_bytes(b'not the official archive')
    with pytest.raises(ValueError, match='SHA256'):
        driver().unpack_glew(archive, tmp_path / 'dest')
    assert not (tmp_path / 'dest').exists()


def test_command_failure_is_recorded(tmp_path):
    with pytest.raises(subprocess.CalledProcessError):
        driver().record(tmp_path, 'fail', [sys.executable, '-c', 'raise SystemExit(7)'], ROOT)
    import json
    assert json.loads((tmp_path / 'fail.json').read_text())['exit'] == 7
    with pytest.raises(FileExistsError):
        driver().record(tmp_path, 'fail', [sys.executable, '-c', 'pass'], ROOT)


def test_command_timeout_is_distinct(tmp_path):
    import json
    with pytest.raises(subprocess.TimeoutExpired):
        driver().record(tmp_path, 'timeout', [sys.executable, '-c', 'import time; time.sleep(5)'], ROOT, timeout=0.05)
    result = json.loads((tmp_path / 'timeout.json').read_text())
    assert result['timed_out'] is True
    assert result['exit'] != 0


def test_cli_missing_data(tmp_path):
    binary = elf(tmp_path / 'app')
    out = subprocess.run([sys.executable, str(SCRIPT), 'launch', '--binary', str(binary), '--data-dir', str(tmp_path), '--output', str(tmp_path / 'out')], capture_output=True, text=True)
    assert out.returncode == 2
    assert 'TOMB5.CUE' in out.stderr
    assert 'Traceback' not in out.stderr
