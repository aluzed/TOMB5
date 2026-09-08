from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def test_re747_transaction_publication_scope():
    path = ROOT / 'docs/stories/RE-747-level-module-transaction-proof.md'
    assert path.exists()
    story = path.read_text()
    dashboard = (ROOT / 'docs/reverse/reconstruction-progress.html').read_text()
    assert path.name in dashboard
    for token in ('263', 'S_LoadLevelFile', 'LOAD_Start', 'SPEC_PSXPC_N/FILE.C',
                  '32 bits', 'Pas de preuve matérielle', '## Handoff', '- [x]', '- [ ]'):
        assert token in story
    assert 'aucun correctif de production' in story
    assert not re.search(r'0x[0-9a-fA-F]{6,}|FUN_[0-9a-fA-F]{8}', story)
