from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def test_bridge_bodies_actual_translation_unit(tmp_path):
    run = subprocess.run([
        sys.executable, str(ROOT / 'tests/reverse/fixtures/re782/run_test.py'),
        '--root', str(ROOT), '--source', str(ROOT / 'GAME/OBJECTS.C'),
        '--output', str(tmp_path / 'build')], cwd=ROOT, text=True, capture_output=True, timeout=180)
    assert run.returncode == 0, run.stdout + run.stderr
    assert 'SUMMARY checks=1260 failures=0' in run.stdout
    assert len([line for line in run.stdout.splitlines() if line.startswith('PASS ')]) == 1260
