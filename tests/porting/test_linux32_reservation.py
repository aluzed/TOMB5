"""Real host-only recorder reservation/start failures; no game execution."""
import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]


def driver():
    spec = importlib.util.spec_from_file_location('linux32_reservation', ROOT / 'scripts/porting/linux32.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def command(marker):
    return [sys.executable, '-c', 'from pathlib import Path; import sys; Path(sys.argv[1]).touch()', str(marker)]


@pytest.mark.parametrize('directory', [False, True])
def test_log_collision_is_finalized_without_starting_child(tmp_path, directory):
    log = tmp_path / 'collision.log'
    if directory:
        log.mkdir()
        (log / 'sentinel').write_bytes(b'original evidence')
    else:
        log.write_bytes(b'original evidence')
    marker = tmp_path / 'child-started'
    with pytest.raises(FileExistsError):
        driver().record(tmp_path, 'collision', command(marker), ROOT)
    assert not marker.exists()
    if directory:
        assert (log / 'sentinel').read_bytes() == b'original evidence'
    else:
        assert log.read_bytes() == b'original evidence'
    result = json.loads((tmp_path / 'collision.json').read_text())
    assert 'error' in result, 'log reservation failure left an unfinished ledger'
    assert result['end'] >= result['start']
    assert result['elapsed_seconds'] >= 0
    assert result['timed_out'] is False
    assert 'exit' not in result, 'no child was started; do not invent a native exit'


def test_existing_ledger_is_never_changed(tmp_path):
    ledger = tmp_path / 'collision.json'
    ledger.write_bytes(b'original ledger')
    marker = tmp_path / 'child-started'
    with pytest.raises(FileExistsError):
        driver().record(tmp_path, 'collision', command(marker), ROOT)
    assert ledger.read_bytes() == b'original ledger'
    assert not (tmp_path / 'collision.log').exists()
    assert not marker.exists()


@pytest.mark.parametrize('failure', ['executable', 'cwd'])
def test_spawn_failure_is_recorded_without_native_exit(tmp_path, failure):
    marker = tmp_path / 'child-started'
    argv = command(marker) if failure == 'cwd' else [str(tmp_path / 'missing-executable')]
    cwd = tmp_path / 'missing-cwd' if failure == 'cwd' else ROOT
    with pytest.raises(FileNotFoundError):
        driver().record(tmp_path, 'spawn', argv, cwd)
    result = json.loads((tmp_path / 'spawn.json').read_text())
    assert result['argv'] == argv
    assert result['cwd'] == str(cwd)
    assert result['error']
    assert result['end'] >= result['start']
    assert result['elapsed_seconds'] >= 0
    assert result['timed_out'] is False
    assert 'exit' not in result
    assert (tmp_path / 'spawn.log').read_bytes() == b''
    assert not marker.exists()
