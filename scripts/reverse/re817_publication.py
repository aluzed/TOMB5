"""RE817 metadata only, no replay/integration/activation."""
import csv,hashlib,io,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
EXPECTED={'status': 'RECOVERED_PRIVATE_NATIVE_INITIALIZER_PREREQUISITE_PASS', 'private_review': 'PRIVATE_ONLY_PASS', 'private_verdict_sha256': '292a83d4c523f0d1f9e05607f89c3800c93d6fccafad798faa28d2d72ff73141', 'private_manifest_sha256': 'eb338c1e1950dbfbd025ed65fb3856818d905d8ab3137a79a465717f4605ed76', 'candidate_sha256': '449d24af4532ee267f3ba07f8e9c2f7792cbdf0005d3d1d4f7b286ffe8b9f5dd', 'manifest_entries': 235, 'target_visits': 994, 'target_selected_bytes': 2992, 'native_selected_bytes': 2980, 'target_allocation_bytes': 92, 'native_allocation_bytes': 82, 'byte_corruptions_rejected_per_mode': 2980, 'event_corruptions_rejected_per_mode': 11, 'code_mutants_rejected': 2, 'baseline_normal_exit': 1, 'baseline_strict_exit': 1, 'candidate_normal_exit': 0, 'candidate_strict_exit': 0, 'getdoor_calls': 5, 'shut_calls': 4, 'itemnewroom_calls': 1, 'fixture_count': 1, 'domain': 'generic284 angle0 rooms0..3 portal2 sentinel255', 'allocator': 'declared double, not production allocator', 'target_origin': 'direct initializer from archived RE816 RAM; not retained caller CPU', 'abi': 'declared projection and pointer rebasing; not ABI identity', 'native_entry': 'private weak direct initializer; no registration or InitialiseItem', 'original_timeout_certified': False, 'first_reviewer_attempt_accepted': False, 'native_registration_proven': False, 'native_caller_composition_proven': False, 'general_input_domain_proven': False, 'real_allocator_proven': False, 'source_patch': False, 'activation_approved': False, 'integration_approved': False, 'production_ready': False, 'publication_review_approved': False, 'global_green': False, 'hardware_proven': False, 'startup_proven': False, 'whole_ram_oracle': False, 'next': 'RE818 actual-native conditional producer/caller composition prerequisite; not performed'}
PRECEDING='b100509e34a75f6a8590bcce38b5c9430e818c8661a32858a0a94facf8b4e071'
SECTION='<!-- start re817-native-initializer-prerequisite --><section id="re817"><h2>RE-817 — RECOVERED_PRIVATE_NATIVE_INITIALIZER_PREREQUISITE_PASS</h2><p>Récupération indépendante PRIVATE_ONLY_PASS distincte du timeout600 NON CERTIFIÉ et de attempt01 rejetée. Cible directe RAM archivée, 994 visites, 2992 octets; actual-TU privé normal/strict baseline RED1 candidat GREEN0, projection2980, corruptions2980 et événements11 rejetés par mode, deux mutants code rejetés. Allocateur double82 vs cible92; une fixture generic284 angle0 rooms0..3 portal2 sentinelle255. Pas registration/InitialiseItem ni composition caller natifs, domaine général ou allocateur réel.</p><p>Publication metadata-only pending revue finale parent; aucune production/intégration/activation ni GREEN global. Historiques RE815/816 gelés; BLOCKED-003/004/006 ouverts, 001/002 non recréés. RE818 actual-native conditional producer/caller prerequisite non effectué. <a href="../stories/RE-817-native-initializer-prerequisite.md">Story</a> · <a href="functions/re817-native-initializer-prerequisite.md">Contrat</a> · <a href="generated/re817-native-initializer-prerequisite.csv">CSV</a>.</p></section><!-- end re817-native-initializer-prerequisite -->\n'
START='<!-- start re817-native-initializer-prerequisite -->'
END='<!-- end re817-native-initializer-prerequisite -->'
FUNCTIONDOC='# RE817 — préalable initializer natif privé récupéré\n\nStatut **RECOVERED_PRIVATE_NATIVE_INITIALIZER_PREREQUISITE_PASS**; revue indépendante\n**PRIVATE_ONLY_PASS**. Acceptation du candidat privé uniquement; publication finale\nencore en attente de revue parent séparée. Aucun GO production/intégration/activation.\n\n## Preuve acceptée et provenance\n\nLe producer timeout600 original reste **NON CERTIFIÉ**, inventaire historique\n75 fichiers immuable. La première tentative du reviewer est rejetée pour erreur\ninstrumentale d’observation allocator; attempt01 reste conservée. La récupération\nindépendante corrigée est distincte et ne certifie rétroactivement aucun timeout.\nVerdict privé `292a83d4c523f0d1f9e05607f89c3800c93d6fccafad798faa28d2d72ff73141`;\nmanifest privé `eb338c1e1950dbfbd025ed65fb3856818d905d8ab3137a79a465717f4605ed76`\navec 235 entrées vérifiées. Candidat privé exact\n`449d24af4532ee267f3ba07f8e9c2f7792cbdf0005d3d1d4f7b286ffe8b9f5dd`, jamais versionné.\n\nCible fraîche directe initializer depuis RAM RE816 archivée : 994 visites hooks\n(non instructions retirées), 2992 octets sélectionnés. Registres de départ construits;\nce n’est ni la continuation CPU du caller ni une extraction nouvelle.\nActual-TU DOOR privé avec ITEMS, GETSTUFF et COLLIDE réels, normal et strict\nASan/UBSan failfast : baseline comportementale RED exit1 dans les deux modes,\ncandidat GREEN exit0 dans les deux modes. Stderr runtime vide, warnings legacy\ncompilation conservés. ShutThatDoor4, GetDoor5 et ItemNewRoom1 réels.\nProjection indépendante 2980 octets natifs, 2980 corruptions mono-octet et\n11 corruptions d’événement rejetées **dans chaque mode**; deux mutants code rejetés.\n\n## Limites et readiness\n\nUne fixture seulement : generic284, angle0, rooms0..3, portal2 et sentinelle255.\nAllocation native82 contre cible92; projection déclarée et rebasing pointeurs,\npas identité ABI. L’allocateur natif est un **double déclaré**, non allocateur réel.\nEntrée weak privée directe, **pas registration ni InitialiseItem natifs**.\nAucune preuve domaine général, composition caller native, startup, hardware,\nwholeRAM, gameplay, sécurité mémoire générale, production ou GREEN global.\nLes états pending historiques RE815/816 sont gelés, pas réécrits; cette preuve\nmet à jour seulement la frontière courante. BLOCKED-003/004/006 restent ouverts;\nBLOCKED-001/002 supprimés ne sont pas recréés. Quatre échecs historiques\nRE801/802 restent à comparer exactement, non à masquer.\n\n## Tracker et acceptance suivante\n\n- [x] Récupération indépendante privée distincte authentifiée, baseline RED/candidat GREEN.\n- [x] Oracle projeté et événements discriminants, deux mutants code rejetés.\n- [x] Publication metadata-only avec TDD, suffixe dashboard exact et CSV sûr.\n- [ ] Revue finale indépendante de cette publication par parent.\n- [ ] RE818 : préalable composition conditionnelle producer/caller **actual-native**,\n  registration/callback et retour réels, oracle indépendant borné, RED/GREEN normal/strict,\n  provenance exacte et revue séparée; travail non effectué ici.\n- [ ] Allocateur réel, élargissement du domaine et revue d’intégration distincte.\n\nAcceptance d’une preuve privée n’autorise aucune activation ou modification source.\n'
STORY=FUNCTIONDOC
OUTPUTS={'docs/reverse/functions/re817-native-initializer-prerequisite.md':'FUNCTIONDOC','docs/stories/RE-817-native-initializer-prerequisite.md':'STORY','docs/reverse/generated/re817-native-initializer-prerequisite.csv':'CSV_TEXT'}

def metadata():return dict(EXPECTED)
def validate(d):
 if type(d) is not dict or set(d)!=set(EXPECTED) or any(type(d[k]) is not type(v) or d[k]!=v for k,v in EXPECTED.items()):raise ValueError('RE817 exact schema values types required')
 return d
def csv_row():return {k:str(v).lower() if type(v) is bool else str(v) for k,v in validate(metadata()).items()}
def render_csv():
 o=io.StringIO(newline='');d=csv_row();w=csv.DictWriter(o,fieldnames=list(d),lineterminator='\n');w.writeheader();w.writerow(d);return o.getvalue()
CSV_TEXT=render_csv()
def dashboard_before_re817(b):
 # RE819 exact named suffix; full predecessor bytes remain pinned.
 s819=b'<!-- start re819-real-allocator-prerequisite -->';e819=b'<!-- end re819-real-allocator-prerequisite -->'
 if s819 in b or e819 in b:
  assert b.count(s819)==b.count(e819)==1
  a819=b.index(s819)
  assert hashlib.sha256(b[a819:]).hexdigest()=='255c6262960783172f0f7fe39198ae9dac9ec857c1dc4c7db21f8bed55b40dd8'
  b=b[:a819]
  assert hashlib.sha256(b).hexdigest()=='301e3235d55974210f54380ad3680ba05151cef7e95f208dd9d708656895f21c'
 # RE818 exact approved metadata suffix only; inverse delta preserves old guard.
 start818=b'<!-- start re818-actual-tu-caller-prerequisite -->';end818=b'<!-- end re818-actual-tu-caller-prerequisite -->'
 if start818 in b or end818 in b:
  assert b.count(start818)==b.count(end818)==1
  a818=b.index(start818)
  assert hashlib.sha256(b[a818:]).hexdigest()=='133512b16df78502d62a52334174b04201d864b54165866985b5186b13b4ab8b'
  b=b[:a818]
  assert hashlib.sha256(b).hexdigest()=='ae791f9befe193f0370b68825cfe17d02616cc723661a8eaa07102caa2b75bc6'
 assert b.count(START.encode())==b.count(END.encode())==1 and b.endswith(SECTION.encode())
 prior=b[:-len(SECTION.encode())];assert hashlib.sha256(prior).hexdigest()==PRECEDING
 return prior
def consume_approval():
 p=ROOT/'build/reverse/autonomy-20261003/re817-recovery-independent-review'
 for n,k in [('verdict.json','private_verdict_sha256'),('manifest.json','private_manifest_sha256')]:assert hashlib.sha256((p/n).read_bytes()).hexdigest()==EXPECTED[k]
 v=json.loads((p/'verdict.json').read_text());m=json.loads((p/'manifest.json').read_text())
 assert v['passed'] is True and v['private_accepted'] is True and v['status']=='PRIVATE_ONLY_PASS'
 assert not v['integration_approved'] and not v['production_approved'] and not v['public_edit_approved'] and not v['security_concerns'] and not v['logic_errors']
 assert len(m['sha256'])==235 and v['candidate_sha256']==EXPECTED['candidate_sha256']
 for n,d in m['sha256'].items():
  q=Path(n);assert not q.is_absolute() and '..' not in q.parts
  assert hashlib.sha256((p/q).read_bytes()).hexdigest()==d
 return v
def generate():
 import fcntl
 with (ROOT/'build/reverse/autonomy-mutation.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);consume_approval()
  p=ROOT/'docs/reverse/reconstruction-progress.html';b=p.read_bytes()
  if START.encode() in b or END.encode() in b:dashboard_before_re817(b)
  else:
   assert hashlib.sha256(b).hexdigest()==PRECEDING;p.write_bytes(b+SECTION.encode())
  for p,k in OUTPUTS.items():(ROOT/p).write_text(globals()[k])
if __name__=='__main__':generate()
