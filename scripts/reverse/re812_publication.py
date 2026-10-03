"""Safe pinned RE812 metadata only; no protected target inputs or source writes."""
import csv, hashlib, io
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SOURCE='4e4374916bf454fd577fb92d89e7160a1b818e5a744e9244ad89c44fbb0ef84f'
PRECEDING='7629485a524ee5cf87041374b6e50acedbbe42b10dd18325b9ff088471b690ac'
START='<!-- start re812-addactiveitem-characterization -->'
END='<!-- end re812-addactiveitem-characterization -->'
EXPECTED={'status': 'PRIVATECHARACTERIZATIONPASS', 'source_sha256': '4e4374916bf454fd577fb92d89e7160a1b818e5a744e9244ad89c44fbb0ef84f', 'verdict_sha256': '43d1beb61e28a71ed2611421d3bc069923cdeb69e2f4cd1ddcaa1c8ab09f202b', 'sequences': 48, 'returns': 192, 'hook_visits': 4860, 'native_bytes_per_return': 642, 'whole_ram_bytes_per_return': 2097152, 'normal_failures': 0, 'strict_ASan_UBSan_failures': 0, 'normal_stderr_bytes': 0, 'strict_stderr_bytes': 0, 'production_patch': False, 'production_ready': False, 'runtime_performed': False, 'gameplay_performed': False, 'fullbuild_performed': False, 'global_green': False, 'historical_lock_compliance': False, 'control_callbacks_invoked': False, 'interior_removal_tested': False, 'natural_reachability_proven': False, 'hardware_validated': False, 'independent_publication_review': 'pending', 'frontier': 'RE813 caller/registration control provenance then real composition; BLOCKED006 remains'}
FUNCTIONDOC="# RE812 — AddActiveItem / composition : caractérisation privée\n\nStatut : **PRIVATECHARACTERIZATIONPASS**, distinct de production-ready.\nSource inchangée : `4e4374916bf454fd577fb92d89e7160a1b818e5a744e9244ad89c44fbb0ef84f`.\nVerdict privé indépendant : `43d1beb61e28a71ed2611421d3bc069923cdeb69e2f4cd1ddcaa1c8ab09f202b`.\n\n## Preuve et domaine\n\nRevue privée fraîche passée : 48 séquences continues Add/Add/Remove/Add,\n192 retours cible et 192 comparaisons par mode natif normal/strict ASan+UBSan,\n4860 visites hooks cible. Zéro échec, exit 0 et stderr vide dans les deux modes.\nContrôles : présence control NULL/nonNULL × active 0/1 × status 0/1/2/3 ×\nlongueur initiale 0/1/2. Cible item 3, toujours en tête lorsqu'actif.\nBuffers natifs complets de 642 octets (arène incluant guards + head);\noracle indépendant de RAM complète de 2 MiB à chaque retour cible.\nCPU/RAM conservés entre appels. Pointeurs natifs non comparés aux adresses cible.\nSi active=1/control=NULL, active et chaîne conservés, status remis à zéro.\nControl est seulement une présence de pointeur, callbacks jamais invoqués.\n\n## Décision NO PATCH et limites\n\nPas de régression production démontrée sur ce domaine, donc aucun candidat ni\npatch justifié et aucun behavioral RED. Le RED de publication vérifie seulement\nl'absence de métadonnées, pas un bug du jeu. Retrait intérieur/queue non couvert\n(RE811 séparé); listes synthétiques finies acycliques seulement. Comparaison aux\nretours, pas trace des stores transitoires. Oracle logiciel Unicorn/MIPS, pas\nhardware ni certification des autres configurations. Compilation privée de\nGAME/ITEMS.C i386 sous PSXPC_TEST/PSX_VERSION/USE_32_BIT_ADDR; aucun fullbuild\nRE812, runtime jeu, gameplay, accessibilité naturelle ni GREEN global.\nAnimateItem et DoorControl ne sont pas activés.\n\nIncident historique : première écriture du run.py producteur hors mutation lock,\nconservée; historical_lock_compliance=false, aucune certification rétroactive.\nPremier child bloqué après lectures non utilisé comme preuve. PASS limité au\ncontenu/replay privé, pas approbation d'intégration ou de publication publique.\nLa revue indépendante finale de ces fichiers de publication reste pending.\n\n## Frontier\n\nRE813 planned-not-proven : nouvelle preuve caller/registration et provenance de\ncontrol, puis composition réelle. Pas de répétition de matrice ni activation\nglobale AnimateItem/DoorControl. BLOCKED-006 existant couvre toujours la\nnatural reachability; aucun nouveau blocker nécessaire.\n"
STORY="# RE812 — AddActiveItem / composition : caractérisation privée\n\nStatut : **PRIVATECHARACTERIZATIONPASS**, distinct de production-ready.\nSource inchangée : `4e4374916bf454fd577fb92d89e7160a1b818e5a744e9244ad89c44fbb0ef84f`.\nVerdict privé indépendant : `43d1beb61e28a71ed2611421d3bc069923cdeb69e2f4cd1ddcaa1c8ab09f202b`.\n\n## Preuve et domaine\n\nRevue privée fraîche passée : 48 séquences continues Add/Add/Remove/Add,\n192 retours cible et 192 comparaisons par mode natif normal/strict ASan+UBSan,\n4860 visites hooks cible. Zéro échec, exit 0 et stderr vide dans les deux modes.\nContrôles : présence control NULL/nonNULL × active 0/1 × status 0/1/2/3 ×\nlongueur initiale 0/1/2. Cible item 3, toujours en tête lorsqu'actif.\nBuffers natifs complets de 642 octets (arène incluant guards + head);\noracle indépendant de RAM complète de 2 MiB à chaque retour cible.\nCPU/RAM conservés entre appels. Pointeurs natifs non comparés aux adresses cible.\nSi active=1/control=NULL, active et chaîne conservés, status remis à zéro.\nControl est seulement une présence de pointeur, callbacks jamais invoqués.\n\n## Décision NO PATCH et limites\n\nPas de régression production démontrée sur ce domaine, donc aucun candidat ni\npatch justifié et aucun behavioral RED. Le RED de publication vérifie seulement\nl'absence de métadonnées, pas un bug du jeu. Retrait intérieur/queue non couvert\n(RE811 séparé); listes synthétiques finies acycliques seulement. Comparaison aux\nretours, pas trace des stores transitoires. Oracle logiciel Unicorn/MIPS, pas\nhardware ni certification des autres configurations. Compilation privée de\nGAME/ITEMS.C i386 sous PSXPC_TEST/PSX_VERSION/USE_32_BIT_ADDR; aucun fullbuild\nRE812, runtime jeu, gameplay, accessibilité naturelle ni GREEN global.\nAnimateItem et DoorControl ne sont pas activés.\n\nIncident historique : première écriture du run.py producteur hors mutation lock,\nconservée; historical_lock_compliance=false, aucune certification rétroactive.\nPremier child bloqué après lectures non utilisé comme preuve. PASS limité au\ncontenu/replay privé, pas approbation d'intégration ou de publication publique.\nLa revue indépendante finale de ces fichiers de publication reste pending.\n\n## Frontier\n\nRE813 planned-not-proven : nouvelle preuve caller/registration et provenance de\ncontrol, puis composition réelle. Pas de répétition de matrice ni activation\nglobale AnimateItem/DoorControl. BLOCKED-006 existant couvre toujours la\nnatural reachability; aucun nouveau blocker nécessaire.\n\n## Tracker\n\n- [x] Contenu privé et replay frais revus indépendamment.\n- [x] Décision NO PATCH; production GAME/ITEMS.C inchangée.\n- [x] RED publication métadonnées absentes observé avant générateur.\n- [x] Métadonnées sûres, CSV, functiondoc et section dashboard ajoutés.\n- [ ] Revue indépendante finale des hashes de publication.\n- [ ] RE813 preuve caller/registration/control puis composition réelle.\n- [ ] Accessibilité naturelle / runtime / gameplay / production-ready.\n"
SECTION='<!-- start re812-addactiveitem-characterization --><section id="re812"><h2>RE-812 — AddActiveItem / composition : PRIVATECHARACTERIZATIONPASS</h2><p>48 séquences Add/Add/Remove/Add, 192 retours, 4860 visites hooks; buffers complets 642 octets et RAM 2 MiB à chaque retour. Revue privée fraîche PASS, normal/strict ASan+UBSan zéro échec et stderr vide. Cible active toujours en tête; control présence seulement, callbacks non invoqués. Retrait intérieur exclu.</p><p>NO PATCH : aucune régression démontrée sur ce domaine; RED publication seulement, pas behavioral RED. Incident initial run.py hors mutation lock conservé : historical_lock_compliance=false. Aucun runtime jeu, gameplay, hardware, fullbuild RE812 ou GREEN global; pas production-ready. Revue finale publication pending. RE813 caller/registration/control provenance puis composition réelle planned-not-proven; BLOCKED-006 reste applicable. <a href="../stories/RE-812-addactiveitem-characterization.md">Tracker RE812</a> · <a href="functions/re812-addactiveitem-composition.md">Functiondoc</a> · <a href="generated/re812-addactiveitem-characterization.csv">CSV sûr</a>.</p></section><!-- end re812-addactiveitem-characterization -->\n'

def metadata():
    return dict(EXPECTED)
def validate(d):
    assert set(d)==set(EXPECTED)
    assert all(type(d[k]) is type(v) and d[k]==v for k,v in EXPECTED.items())
    return d
def csv_row():
    return {k:str(v).lower() if type(v) is bool else str(v) for k,v in validate(metadata()).items()}
def render_csv():
    o=io.StringIO(newline=''); row=csv_row()
    w=csv.DictWriter(o,fieldnames=list(row),lineterminator='\n');w.writeheader();w.writerow(row)
    return o.getvalue()
def dashboard_before_re812(b):
    # RE814 only: exact named suffix + inverse whole predecessor digest.
    start814=b'<!-- start re814-bounded-continuation -->';end814=b'<!-- end re814-bounded-continuation -->'
    if start814 in b or end814 in b:
     assert b.count(start814)==b.count(end814)==1
     a814=b.index(start814)
     assert hashlib.sha256(b[a814:]).hexdigest()=='6f173a0ece3975d02b65e2a6b60ede0d85c6a7652874be7137a5b86d535c21ef'
     b=b[:a814]
     assert hashlib.sha256(b).hexdigest()=='5c7b6d809cf6ffc00890ed0de5ee9744bc62579e10a742c67c218a13e943b081'
    # Only explicitly named RE813: exact suffix digest + inverse baseline.
    start813=b'<!-- start re813-conditional-producer-gap -->';end813=b'<!-- end re813-conditional-producer-gap -->'
    if start813 in b or end813 in b:
        assert b.count(start813)==b.count(end813)==1
        a813=b.index(start813)
        assert hashlib.sha256(b[a813:]).hexdigest()=='1b17a1f1e76b2da1b5546202fd247559fbb52817c3f222895dada65ab652c3f6'
        b=b[:a813]
        assert hashlib.sha256(b).hexdigest()=='dd5ea56cc15c10cbe319154b2def1209b0e54d4ca017294ace0df5242097096d'
    start=START.encode();end=END.encode();section=SECTION.encode()
    assert b.count(start)==b.count(end)==1
    assert b.endswith(section)
    prior=b[:-len(section)]
    assert hashlib.sha256(prior).hexdigest()==PRECEDING
    return prior
def generate():
    import fcntl
    with (ROOT/'build/reverse/autonomy-mutation.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        assert hashlib.sha256((ROOT/'GAME/ITEMS.C').read_bytes()).hexdigest()==SOURCE
        dash=ROOT/'docs/reverse/reconstruction-progress.html';b=dash.read_bytes()
        if START.encode() in b: dashboard_before_re812(b)
        else:
            assert hashlib.sha256(b).hexdigest()==PRECEDING
            dash.write_bytes(b+SECTION.encode())
        for p,text in [('docs/reverse/generated/re812-addactiveitem-characterization.csv',render_csv()),('docs/reverse/functions/re812-addactiveitem-composition.md',FUNCTIONDOC),('docs/stories/RE-812-addactiveitem-characterization.md',STORY)]:
            (ROOT/p).write_text(text)
if __name__=='__main__':generate()
