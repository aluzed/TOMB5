"""Compile the actual production TU, never a tmp_path source replica."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'build/reverse/autonomy-20260925-publication-0928'


def test_re780_public_runner_compiles_actual_production_tu():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    run = Path(tempfile.mkdtemp(prefix='pytest-actual-tu-', dir=OUTPUT))
    assert subprocess.run(['git', 'check-ignore', '-q', str(run)], cwd=ROOT).returncode == 0
    source = ROOT / 'SPEC_PSXPC_N/GETSTUFF.C'
    runner = ROOT / 'tests/reverse/fixtures/re780/run_test.py'
    fixture = runner.with_name('trigger_filter_test.cpp')
    before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in (source, runner, fixture)}
    argv = [sys.executable, '-B', str(runner), '--root', str(ROOT),
            '--source', str(source), '--output', str(run / 'compiled')]
    start = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True, timeout=210)
    (run / 'stdout.log').write_text(result.stdout)
    (run / 'stderr.log').write_text(result.stderr)
    after = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in (source, runner, fixture)}
    (run / 'invocation.json').write_text(json.dumps({
        'argv': argv, 'cwd': str(ROOT), 'start': start,
        'end': datetime.now(timezone.utc).isoformat(), 'exit': result.returncode,
        'environment': {key: os.environ.get(key) for key in
                        ('PYTHONDONTWRITEBYTECODE', 'PYTEST_DISABLE_PLUGIN_AUTOLOAD')},
        'input_hashes_before': before, 'input_hashes_after': after,
        'attribution': 'publication pytest: synthetic cases, actual source TU, not full game'
    }, indent=2))
    assert before == after
    assert result.returncode == 0, result.stdout + result.stderr
    assert 'SUMMARY checks=153 failures=0' in result.stdout
    assert (run / 'compiled/source.o').is_file()
    assert (run / 'compiled/trigger_filter_test').is_file()
