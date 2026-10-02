"""RE789: approved target contract fingerprint versus freshly compiled real source."""
import hashlib
import html
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PROOF = ROOT / 'docs/reverse/generated/re789-target-composition-proof.json'
STORY = ROOT / 'docs/stories/RE-789-target-roof-registration-composition.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
START, END = '<section id="re789">', '<!-- end re789 -->'


def proof():
    assert PROOF.exists(), 'RED: approved target metadata absent'
    data = json.loads(PROOF.read_text())
    assert data['passed'] is True
    assert data['security_concerns'] == data['logic_errors'] == []
    assert data['scope'] == 'authenticated-target-synthetic-composition'
    assert data['cases'] == 13824 and data['prefix_cases'] == 2
    assert data['helper_visits'] == 4608
    assert data['baseline'] == {'entry_differences': 3456, 'callback_masks': 1152, 'short_masks': 2304, 'return_differences': 0}
    assert data['source_current_differences'] == {'normal': 0, 'ubsan': 0}
    assert len(data['contract_sha256']) == len(data['preceding_dashboard_sha256']) == 64
    assert data['limits']
    return data


def test_approved_proof_metadata():
    data = proof()
    assert data['reviewer_target_replay_exit'] == 0
    assert data['reviewer_source_fresh'] is False
    assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|data:image', PROOF.read_text())


@pytest.mark.parametrize('baseline', [False, True])
@pytest.mark.parametrize('ubsan', [False, True])
def test_actual_tu_matches_target_or_exposes_baseline(baseline, ubsan):
    data = proof()
    out = ROOT / 'build/reverse/autonomy-20261002/re789-public-tests'
    out.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=f'{"baseline" if baseline else "current"}-{ubsan}-', dir=out))
    argv = [sys.executable, '-B', str(ROOT / 'tests/reverse/fixtures/re788/run_test.py'),
            '--root', str(ROOT), '--source', 'baseline' if baseline else 'current', '--output', str(work / 'run')]
    if ubsan:
        argv.append('--ubsan')
    run = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, timeout=150)
    (work / 'invocation.json').write_text(json.dumps({'argv': argv, 'exit': run.returncode}))
    (work / 'stdout.log').write_text(run.stdout)
    (work / 'stderr.log').write_text(run.stderr)
    assert run.returncode == int(baseline), run.stdout + run.stderr
    evidence = json.loads((work / 'run/evidence.json').read_text())
    rows = evidence['rows']
    assert len(rows) == data['cases']
    canonical = []
    for row in rows:
        assert len(row) == 21 and row[17:19] == [1, 1]
        calls = int(not row[8])
        assert row[12] == row[13] == calls
        assert row[19] == (1234 if calls else 0)
        assert row[10] == row[11] and row[14] == row[15]
        canonical.append(row[:9] + [row[11] if calls else None, calls,
                                    row[15] if calls else None, row[16]])
    digest = hashlib.sha256(json.dumps(canonical, separators=(',', ':')).encode()).hexdigest()
    assert (digest == data['contract_sha256']) is (not baseline)
    assert evidence['summary'] == {'cases': 13824, 'input_differences': 3456 if baseline else 0,
                                   'result_differences': 0, 'state_failures': 0}
    manifest = json.loads((work / 'run/manifest.json').read_text())
    assert len(manifest['compilations']) == 6
    assert all(c['exit'] == 0 for c in manifest['compilations'])
    assert manifest['link']['exit'] == 0 and manifest['run']['exit'] == int(baseline)
    assert 'runtime error' not in (work / 'run/native.stderr').read_text()


def test_story_scope_and_remaining_readiness():
    data = proof()
    assert STORY.exists(), 'RED: story absent'
    text = DASH.read_text()
    assert text.count(START) == text.count(END) == 1
    section = html.unescape(text.split(START, 1)[1].split(END, 1)[0])
    for content in (STORY.read_text(), section):
        for token in ('13824', '3456', '4608', 'registration', 'GetCeiling', 'UBSan',
                      'source', 'synthétique', 'pas de runtime', 'pas de GREEN global', 'RE-790'):
            assert token in content, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|data:image|<img\b|```(?:asm|mips|c|cpp)\b', content)
    assert '## Tracker' in STORY.read_text() and '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()


def test_history_preserved_exactly():
    data = proof()
    dashboard = DASH.read_bytes()
    start, end = START.encode(), END.encode()
    assert dashboard.count(start) == dashboard.count(end) == 1
    a = dashboard.index(start)
    b = dashboard.index(end, a) + len(end)
    assert hashlib.sha256(dashboard[:a] + dashboard[b:]).hexdigest() == data['preceding_dashboard_sha256']
    assert dashboard.count(b'</html>') == dashboard.count(b'</body>') == 1
