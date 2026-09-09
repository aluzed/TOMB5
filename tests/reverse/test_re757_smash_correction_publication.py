"""RE757 public documentary contract: no private reads, imports or replay."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-757-smash-wrapper-correction-proof.md'


def test_re757_private_correction_publication():
    assert STORY.exists(), 'RE757 publication missing'
    story = STORY.read_text(encoding='utf-8')
    dashboard = (ROOT / 'docs/reverse/reconstruction-progress.html').read_text(encoding='utf-8')
    assert dashboard.count('<h2>RE-757 ·') == 1
    section = dashboard.split('<h2>RE-757 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0]
    assert STORY.name in section
    for text in (story, section):
        for token in (
            'correction privée', 'vraie TU GAME/OBJECTS.C', 'SmashObjectControl',
            'item_number', 'short', 'delay slot', 'production inchangée',
            '128 cas', 'dimensions indépendantes', 'BOX_LAST', 'BOX_BLOCKED',
            '64 appels directs', '16 wrappers', '48 divergences', 'GREEN : 128',
            'trois méthodes unittest', '128 processus natifs', '128 exécutions cible',
            'I=576', 'B=32', 'F=64', 'room=80', '576 octets', '24 octets',
            '11296 visites', '288 entrées', 'pas des instructions retirées',
            '512 images', '2 Mio', 'stores inférés', 'stack autorisée exclue',
            'écritures transitoires restaurées', 'pas de contrôle général des lectures',
            'trois doubles ABI', 'SoundEffect', 'ExplodingDeath2', 'RemoveActiveItem',
            'sans effets mémoire', 'corps authentiques non exécutés',
            'indices négatifs/extrêmes', 'états hétérogènes', 'pas de sanitizer',
            'pas de build complet', 'pas de preuve gameplay', 'non hermétique',
            'parent-replay.json', 'parent-audit.log', '14:40:50.514055', '14:41:58.778758',
            'review/review.md', 'review/review.json', 'review/verdict-clarification.json',
            '14:43:07.803942', '14:44:16.984190', '256 lignes',
            'security_concerns=[]', 'logic_errors=[]', 'clarification documentaire',
            'aucun rejeu privé', 'gardes historiques inchangées',
            'PRODUCTION', 'RED/GREEN public sur la vraie TU', 'évaluation des backends',
            'tests de régression', 'revue indépendante', 'non implémentée ici',
            '23:25 Paris', '23:45 Paris',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', text)
        assert not re.search(r'(?:\\x[0-9a-fA-F]{2}){2,}|(?:\b[0-9A-Fa-f]{2} ){12,}', text)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b', text)
        assert not re.search(r'(?i)\b(?:lui|addiu|sw|lw)\s+\$', text)
    for token in ('## Tracker', '## Handoff', '- [x]', '- [ ]',
                  'publication/red.log', 'publication/green.log', 'publication/suite.log',
                  'publication/final.log', 'publication/commands.json',
                  'test_re757_smash_correction_publication.py'):
        assert token in story, token
    handoff = dashboard.split('<h2>Suite de la recherche</h2>', 1)[1].split('<h2>', 1)[0]
    for token in ('Après RE-757', 'PRODUCTION', 'RED/GREEN public sur la vraie TU',
                  'évaluation des backends', 'non implémentée ici'):
        assert token in handoff, token
    assert 'Suivi au 9 septembre 2026, publication RE-757' in dashboard
