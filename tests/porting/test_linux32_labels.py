"""Host-only recorder label boundary: no game inputs or execution."""
import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]


def driver():
    spec = importlib.util.spec_from_file_location('linux32_labels', ROOT / 'scripts/porting/linux32.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def command(marker):
    return [sys.executable, '-c', 'from pathlib import Path; import sys; Path(sys.argv[1]).touch()', str(marker)]


@pytest.mark.parametrize('label', ['', '.', '..', '../escape', 'nested/name', r'nested\name', '/absolute', 'with space', 'line\nfeed', 'étiquette', '-leading', 'a' * 129])
def test_invalid_label_has_no_side_effects(tmp_path, label):
    out = tmp_path / 'out'
    out.mkdir()
    (out / 'nested').mkdir()
    # Use only the test's own temporary root, including the absolute case.
    if label == '/absolute':
        label = str(tmp_path / 'absolute')
    marker = tmp_path / 'child-started'
    before = sorted(str(p.relative_to(tmp_path)) for p in tmp_path.rglob('*'))
    with pytest.raises(ValueError, match='label'):
        driver().record(out, label, command(marker), tmp_path)
    assert sorted(str(p.relative_to(tmp_path)) for p in tmp_path.rglob('*')) == before
    assert not marker.exists()


@pytest.mark.parametrize('label', ['application', 'source-status', 'A_0.test', 'a' * 128])
def test_valid_label_records_real_child(tmp_path, label):
    marker = tmp_path / 'child-started'
    result = driver().record(tmp_path, label, command(marker), tmp_path)
    assert marker.exists()
    assert result['exit'] == 0
    assert result['timed_out'] is False
    assert json.loads((tmp_path / (label + '.json')).read_text()) == result
    assert (tmp_path / (label + '.log')).read_bytes() == b''
