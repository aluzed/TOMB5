"""RE765 publication contract: metadata only, no private probe execution."""
from pathlib import Path
import html
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT/'docs/stories/RE-765-getfloor-vertical-production-integration.md'
DASH = ROOT/'docs/reverse/reconstruction-progress.html'
BASE = 'be7b08c218b12a8fe57d748b197f5d3fff5cb818'


def test_re765_bounded_integration_claims():
    assert STORY.exists(), 'RE765 documentary RED: story absent'
    story = STORY.read_text()
    dashboard = DASH.read_text()
    assert dashboard.count('<h2>RE-765 ·') == 1
    section = html.unescape(dashboard.split('<h2>RE-765 ·',1)[1].split('</body>',1)[0])
    for text in (story,section):
        for token in ('SPEC_PSXPC_N/GETSTUFF.C','y < r->minfloor','y >= room->minfloor',
                      'PSX_VERSION && PSXPC_TEST','ELF32 i386','-m32 -O0',
                      'configuration, pas une architecture','648 cas','653 tests',
                      '36 divergences comportementales','54 contrôles floor négatifs',
                      '320 octets','512 octets','8 octets','GetDoor réel',
                      'frontières de fonctions','pas de trace native exhaustive',
                      're765-independent-review/rapport.md','re765-independent-review/verdict.json',
                      '442 cas','pas 884','aucun rejeu privé','gardes historiques inchangées',
                      'revue indépendante production PASS','aucun replay parent revendiqué',
                      're765-production-review/rapport.md','re765-production-review/verdict.json',
                      're765-production-review/final-verification.json','Validation finale worker : 3753',
                      'Exécution distincte du reviewer : 3753','58,55 s','58,66 s',
                      'staging et commit en attente','unité close','Prochaine recherche proposée',
                      'non effectuée dans cette unité','Aucun nouveau ticket ouvert',
                      'pas de preuve gameplay','autres architectures non validées',
                      'red-behavior.log','green.log','suite.log'):
            assert token in text, token
        assert 'revue indépendante production pending' not in text
        assert 'aucune review production déjà réussie revendiquée' not in text
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}',text)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b',text)
    assert '## Tracker' in story and '## Handoff' in story
    assert '- [x]' in story and '- [ ]' in story
    assert STORY.name in section


def test_re765_strict_append_only_dashboard():
    old = subprocess.check_output(['git','show',f'{BASE}:docs/reverse/reconstruction-progress.html'],cwd=ROOT)
    new = DASH.read_bytes()
    restored = re.sub(rb'<h2>RE-765 \xc2\xb7.*?(?=</body>)',b'',new,flags=re.S)
    assert restored == old
    for section in re.findall(rb'<h2>RE-\d+ \xc2\xb7.*?(?=<h2>|</body>)',old,re.S):
        assert section in new
