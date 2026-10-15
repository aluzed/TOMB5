"""Real-process interruption regressions for the build recorder; no game data."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'scripts/porting/linux32.py'


def running(pid):
    try:
        # A zombie cannot execute or retain the log descriptor.
        return Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()[0] != 'Z'
    except FileNotFoundError:
        return False


@pytest.mark.parametrize('exception', ['KeyboardInterrupt', 'SystemExit'])
def test_interruption_reaps_session_and_records_status(tmp_path, exception):
    marker = tmp_path / 'pids.json'
    child_code = ("import subprocess,sys,os,json,time; "
                  "p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)']); "
                  "open(sys.argv[1],'w').write(json.dumps([os.getpid(),p.pid])); "
                  "time.sleep(30)")
    parent_code = ("import importlib.util,sys,signal; "
                   "spec=importlib.util.spec_from_file_location('driver',sys.argv[1]); "
                   "mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); "
                   "signal.signal(signal.SIGTERM,lambda *_:sys.exit(17)); "
                   "mod.record(sys.argv[2],'interrupted',[sys.executable,'-c',sys.argv[3],sys.argv[4]],sys.argv[2],timeout=20)")
    pids = []
    with (tmp_path / 'parent.log').open('wb') as log:
        parent = subprocess.Popen([sys.executable, '-B', '-c', parent_code, str(SCRIPT),
                                   str(tmp_path), child_code, str(marker)],
                                  stdout=log, stderr=subprocess.STDOUT)
        try:
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                if marker.exists():
                    try:
                        pids = json.loads(marker.read_text())
                        break
                    except json.JSONDecodeError:
                        pass
                assert parent.poll() is None, 'recorder exited before child readiness'
                time.sleep(0.01)
            assert len(pids) == 2, 'child readiness deadline exceeded'
            assert all(running(pid) for pid in pids)
            parent.send_signal(signal.SIGINT if exception == 'KeyboardInterrupt' else signal.SIGTERM)
            parent.wait(timeout=5)
            deadline = time.monotonic() + 2
            while any(running(pid) for pid in pids) and time.monotonic() < deadline:
                time.sleep(0.01)
            assert not any(running(pid) for pid in pids), 'interruption left child/session descendant running'
            meta = json.loads((tmp_path / 'interrupted.json').read_text())
            assert meta['interrupted'] == exception
            assert meta['exit'] == -signal.SIGKILL
            assert meta['timed_out'] is False
            assert meta['elapsed_seconds'] > 0
            assert meta['end'] >= meta['start']
            assert parent.returncode != 0
            if exception == 'SystemExit':
                assert parent.returncode == 17
        finally:
            # Test cleanup is independent of the recorder under test, also on RED.
            if pids:
                try:
                    os.killpg(pids[0], signal.SIGKILL)
                except ProcessLookupError:
                    pass
            if parent.poll() is None:
                parent.kill()
            parent.wait(timeout=5)
