"""Contrat documentaire public RE756 : ni lecture ni replay privés."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-756-smash-object-consumer-proof.md'


def test_re756_smash_publication_scope():
    assert STORY.exists(), 'RE756 publication missing'
    story = STORY.read_text(encoding='utf-8')
    dashboard = (ROOT / 'docs/reverse/reconstruction-progress.html').read_text(encoding='utf-8')
    assert dashboard.count('<h2>RE-756 ·') == 1
    section = dashboard.split('<h2>RE-756 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0]
    assert STORY.name in section
    for text in (story, section):
        for token in (
            'PASS de caractérisation bornée', 'NON-ÉQUIVALENCE',
            '12 cas', '6 appels directs', '4 divergences', '6 wrappers',
            'B=32', 'I=432', 'F=48', '12 octets', '2 octets',
            'SmashObjectControl', 'SmashObject', 'GAME/OBJECTS.C',
            'vraie TU', 'i386', 'indice signé inchangé', 'short', 'zéro',
            'trois doubles', 'SoundEffect', 'ExplodingDeath2', 'RemoveActiveItem',
            'sans effets mémoire', '1084 visites', '32 entrées', '32 delay slots',
            'pas des instructions retirées', 'stores inférés préexécution',
            'pas une trace mémoire', '2 Mio', 'images RAM non archivées',
            'indices 0/1/2', 'inactif corrélé à l’indice 1',
            'BOX_BLOCKED initialement présent', 'BOX_LAST',
            'Ghidra', 'END_RE756', 'exit historique non retrouvé',
            'non relancé', 'snapshot', 'timeout', 'recovery',
            'revue indépendante', 'parent-replay.json', 'parent-audit.json',
            '13:46:23', '13:46:25', '13:47:17', '13:47:19',
            '314 fichiers', 'en-têtes système', 'gardes historiques inchangées',
            'aucun correctif source', 'aucun rejeu privé', 'metadata-only',
            'pas de sûreté mémoire générale', 'pas de preuve gameplay',
            '23:25 Paris', '23:45 Paris', 'unité corrective privée',
            'indices et états découplés', 'flags indépendants',
            'RED réel sur la vraie TU avant patch', 'non exécutée ici',
            '1 217 tests réussis', '51,19 s', '60 tests réussis',
            '0,56 s', 'exit 0',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', text)
        assert not re.search(r'(?:\\x[0-9a-fA-F]{2}){2,}|(?:\b[0-9A-Fa-f]{2} ){12,}', text)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b', text)
    for token in ('## Tracker', '## Handoff', '- [x]', '- [ ]',
                  'publication/red.log', 'publication/green.log',
                  'publication/suite.log', 'publication/final.log',
                  'publication/commands.json', 'test_re756_smash_publication.py'):
        assert token in story, token
    handoff = dashboard.split('<h2>Suite de la recherche</h2>', 1)[1].split('<h2>', 1)[0]
    for token in ('Après RE-755', 'Après RE-756', 'unité corrective privée',
                  'RED réel sur la vraie TU avant patch', '23:45 Paris'):
        assert token in handoff, token
    assert 'Suivi au 9 septembre 2026, publication RE-756' in dashboard
