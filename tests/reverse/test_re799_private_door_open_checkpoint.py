"""Public metadata checkpoint; no dependency on private target archives."""
import hashlib
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-799-private-door-open-proof.md'
META = ROOT / 'docs/reverse/generated/re799-door-open-proof.json'
START, END = b'<!-- start re799-private -->', b'<!-- end re799-private -->'


def test_reviewed_private_proof_exact_matrix_and_readiness():
    assert META.exists(), 'RED: private opening proof metadata absent'
    d = json.loads(META.read_text())
    assert d['cases'] == {'cartesian': 2304, 'byte_sweeps': 1024, 'total': 3328}
    assert d['baseline'] == {'build_exit': 0, 'run_exit': 1, 'failures': 2944}
    assert d['normal_exit'] == d['sanitizer_exit'] == d['target_exit'] == 0
    assert d['sanitizer_diagnostics'] == []
    assert d['target_visits'] == 401792 and d['authentic_copy_calls'] == 2176
    assert d['review_passed'] is True
    assert d['source_integrated'] is False and d['registration_activated'] is False
    assert d['runtime_performed'] is False and d['global_green'] is False
    assert d['next_story'] == 'RE-800'
    assert all(re.fullmatch('[a-f0-9]{64}', d[k]) for k in ('review_sha256', 'candidate_sha256'))


def test_story_documents_scope_and_missing_prerequisites():
    assert STORY.exists(), 'RED: scoped door opening story absent'
    text = STORY.read_text()
    for word in ('## Tracker', '- [x]', '- [ ]', '3328', '2944', 'ASan', 'UBSan',
                 'disjoints', 'i386', 'privé', 'pas de GREEN global', 'RE-800',
                 'DoorControl', 'ProcessClosedDoors', 'Critères de reprise'):
        assert word in text, word


def dashboard_before_named_re800(b):
    """Exclude only RE800, pinning the whole unchanged RE799-era dashboard."""
    start = b'<!-- start re800-integration -->'
    end = b'<!-- end re800-integration -->'
    if start in b or end in b:
        assert b.count(start) == b.count(end) == 1
        a = b.index(start)
        assert end in b[a:]
        z = b.index(end, a) + len(end)
        b = b[:a] + b[z:]
    assert hashlib.sha256(b).hexdigest() == 'ee30d8b3cfb87ca589fde3c61c5129cc9cdf5eeba738715f0d618caef18edfed'
    return b


def test_dashboard_preserves_preceding_bytes_exactly():
    b = (ROOT / 'docs/reverse/reconstruction-progress.html').read_bytes()
    assert b.count(START) == b.count(END) == 1, 'RED: opening checkpoint dashboard missing'
    b = dashboard_before_named_re800(b)
    a = b.index(START); z = b.index(END, a) + len(END)
    assert hashlib.sha256(b[:a] + b[z:]).hexdigest() == '9c7188118d7b3880ad71994e7ee8c3a39be8e00069a393568f01d3c70f035f52'
    assert b.count(b'</body>') == b.count(b'</html>') == 1


def test_new_outputs_metadata_only():
    assert STORY.exists() and META.exists(), 'RED: metadata checkpoint missing'
    b = (ROOT / 'docs/reverse/reconstruction-progress.html').read_bytes()
    assert START in b and END in b
    section = b.split(START, 1)[1].split(END, 1)[0].decode()
    for text in (STORY.read_text(), META.read_text(), section):
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|payload_offset|data:image|```(?:asm|mips)\b', text)
