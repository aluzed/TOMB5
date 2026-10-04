"""Portable RE821 documentary contract: metadata only, no private probe/import."""
import hashlib
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
BEFORE = '3b65e79f42936ce9a49c9e16aa15d7f6b01a5daf7dd2191856d5b2e79b81af22'
SECTION = '''\n<!-- RE821 PUBLICATION BEGIN -->
<section id="re821-publication" data-private-review="PASS_SCOPED" data-publication-review="PENDING_FINAL_REVIEW" data-integration-approved="false">
<h2>RE821 — composition caller nonzero, revue privée bornée</h2>
<p><a href="../stories/RE-821-nonzero-orientation-caller-composition.md">Story RE821 / progression</a> — publication metadata-only; private-reviewed; pending final review. Aucun GREEN d’intégration, aucune nouvelle source intégrée.</p>
<p>Quatre fixtures construites objet284: -32768, 16384, -16384, 1; sans portail ni flip. InitialiseItem vers initializer privé après registration partielle; dispatch cible externe conditionnel après préfixe suspendu, pas startup naturel.</p>
<p>Producteur: huit cas natifs i386 et quatre cibles; reviewer: huit natifs frais, quatre replays cible et quatre observations indépendantes. Buffer natif1088324 octets, entrée464, projection cible2980; deux mutants bypass rejetés exit1, 34 octets différents. Ces résultats privés archivés ne sont pas relancés par cette publication.</p>
<p>Limites: snapshots exit PRE-EPILOGUE, pas post-RET; ShutThatDoor DOOR privé; ITEMS/GETSTUFF/MALLOC réels, COLLIDE lié mais non invoqué; 137 dépendances épinglées après compilation, pas certification historique précompile. Champs/validité/mathématiques dans le domaine construit, pas gameplay ni provenance naturelle.</p>
<p>Frontière suivante: corpus authentique d’angles OU domaine portail/flip distinct avant activation partagée; pas de nouveau caller construit répétitif. BLOCKED-006 reste ouvert. Incident provider résolu, pas de blocage provider actuel.</p>
</section>
<!-- RE821 PUBLICATION END -->
'''


def preceding_dashboard(data):
    suffix = SECTION.encode() + b'</html>'
    assert data.endswith(suffix), 'RE821 suffix absent or altered'
    assert data.count(b'<!-- RE821 PUBLICATION BEGIN -->') == 1
    assert data.count(b'<!-- RE821 PUBLICATION END -->') == 1
    before = data[:-len(suffix)] + b'</html>'
    assert hashlib.sha256(before).hexdigest() == BEFORE
    return before


def test_re821_documentary_publication_and_exact_historical_inverse():
    story = ROOT / 'docs/stories/RE-821-nonzero-orientation-caller-composition.md'
    assert story.exists(), 'RED: RE821 story absent'
    text = story.read_text()
    required = [
        'private-reviewed', 'PENDING_FINAL_REVIEW', 'integration_approved=false',
        'publication_review_approved=false', 'production_patch=false',
        'natural_startup_proven=false', 'gameplay_proven=false',
        '-32768, 16384, -16384, 1', '13, 7, 17, 17',
        '1088324', '464', '2980', '34 octets', 'PRE-EPILOGUE', 'post-RET',
        'DOOR privé', 'COLLIDE lié mais non invoqué', '137 dépendances',
        'après compilation', 'précompile', 'dispatch externe conditionnel',
        'corpus authentique d’angles OU domaine portail/flip distinct',
        'pas de nouveau caller construit répétitif', 'Incident provider résolu',
        '690dafaf7487cc1b453e883fe3db3ab949e9a2ac7ffae3e65cdf968510258fe8',
        '- [x]', '- [ ]', 'BLOCKED-006',
    ]
    for phrase in required:
        assert phrase in text, phrase
    assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|data:image|```(?:asm|mips|cpp|c)\b', text)
    data = (ROOT / 'docs/reverse/tomb5-progress-dashboard.html').read_bytes()
    old = preceding_dashboard(data)
    assert old.endswith(b'</html>')
    # Check only the new active section, never borrow predecessor qualifications.
    section = data[len(old)-len(b'</html>'):-len(b'</html>')].decode()
    assert section == SECTION
    for fragment in ['PENDING_FINAL_REVIEW', 'data-integration-approved="false"',
                     'PRE-EPILOGUE', 'pas post-RET', '137 dépendances',
                     'COLLIDE lié mais non invoqué', 'corpus authentique']:
        assert fragment in section
    for mutant in [data+b'foreign', data.replace(b'PRE-EPILOGUE', b'POST-RET'),
                   data.replace(b'<!-- RE821 PUBLICATION END -->', b''),
                   data.replace(b'<!-- RE821 PUBLICATION BEGIN -->', b''),
                   data[:-7]+SECTION.encode()+b'</html>',
                   data.replace(b'TOMB5 suivi', b'TOMB5 modif', 1),
                   data.replace(SECTION.encode(), SECTION.encode()[::-1])]:
        with pytest.raises(AssertionError):
            preceding_dashboard(mutant)
