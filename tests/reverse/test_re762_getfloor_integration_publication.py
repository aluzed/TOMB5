"""RE762 metadata-only publication contract; no private probe execution."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT/'docs/stories/RE-762-getfloor-clamp-production-integration.md'
DASHBOARD = ROOT/'docs/reverse/reconstruction-progress.html'
BASE = '32efbfca360e2729d81ea5d99932dc506a6c3a19'


def test_integration_scope_and_evidence():
    assert STORY.exists(), 'RE762 story missing: documentary RED'
    story = STORY.read_text()
    dashboard = DASHBOARD.read_text()
    assert dashboard.count('<h2>RE-762 ·') == 1
    section = dashboard.split('<h2>RE-762 ·',1)[1].split('<h2>',1)[0].split('</body>',1)[0]
    for text in (story,section):
        for token in ('SPEC_PSXPC_N/GETSTUFF.C', 'dx = 1', 'PSX_VERSION', 'PSXPC_TEST',
                      'i386', '-m32', 'configuration, pas une architecture',
                      '1728 cas', '96 échecs comportementaux', '72 divergences finales',
                      '96 divergences intermédiaires', '1733 tests',
                      'GetDoor réel', 'unsigned char', '255', 'domain proof',
                      '240 octets', '1536 octets', '8 octets', 'symbole ELF',
                      'masquants', 'asymétriques', 'gardes historiques inchangées',
                      'aucun rejeu privé', 'revue indépendante de RE-762',
                      'autres backends non validés', 'chaînes verticales',
                      'pas de sanitizers', 'pas de preuve gameplay',
                      'red.log', 'green.log', 'suite.log', 'commands.json'):
            assert token.casefold() in text.casefold(), token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}',text)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b',text)
        assert not re.search(r'(?:\\x[0-9a-fA-F]{2}){2,}|(?:\b[0-9A-Fa-f]{2} ){12,}',text)
    for token in ('## Tracker','## Handoff','- [x]','- [ ]'):
        assert token in story
    assert STORY.name in section
    assert 'Suivi au 9 septembre 2026, intégration RE-762' in dashboard
    handoff=dashboard.split('<h2>Suite de la recherche</h2>',1)[1].split('<h2>',1)[0]
    assert 'Après RE-762' in handoff and 'Après RE-761' in handoff


def test_preserved_historical_dashboard():
    old=subprocess.check_output(['git','show',f'{BASE}:docs/reverse/reconstruction-progress.html'],cwd=ROOT)
    new=DASHBOARD.read_bytes()
    def normalize(data):
        data=re.sub(rb'<h2>RE-762 \xc2\xb7.*?(?=</body>)',b'',data,flags=re.S)
        data=re.sub(rb'(?<=<h1>TOMB5 \xe2\x80\x94 Reconstruction fond\xc3\xa9e sur le binaire</h1>\n).*?(?=<h2>)',b'OVERVIEW\n',data,count=1,flags=re.S)
        return re.sub(rb'(?<=<h2>Suite de la recherche</h2>\n)<p>.*?</p>',b'HANDOFF',data,count=1,flags=re.S)
    assert normalize(new)==normalize(old),'historical dashboard bytes changed'
    for section in re.findall(rb'<h2>RE-\d+ \xc2\xb7.*?(?=<h2>|</body>)',old,re.S):
        assert section in new
