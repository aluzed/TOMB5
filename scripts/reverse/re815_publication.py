"""RE815 publication safe metadata. Private approval read only; no execution."""
import csv, hashlib, io, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
EXPECTED={'status': 'REGISTRATION_PREFIX_PASS_NATIVE_REQUIREMENT_RED', 'private_review': 'PASS_scoped', 'private_verdict_sha256': '91a64b4efe5c16fbe416806feb46073a5bccd63404c43f2c341f428ef9dc5460', 'private_manifest_sha256': '0784525f0d9eb2cd020554acf15bf23d0b79a745b5032574ebf3d4d8ffb173e8', 'slots': 14, 'hook_visits': 601, 'oracle_bytes': 896, 'corruptions_rejected': 896, 'independent_stores': 70, 'native_requirement_exit': 1, 'strict_requirement_exit': 1, 'native_characterization_exit': 0, 'strict_characterization_exit': 0, 'constructed_registers': 'GP SP RA', 'native_runtime_stderr_empty': True, 'items_sha256': '4e4374916bf454fd577fb92d89e7160a1b818e5a744e9244ad89c44fbb0ef84f', 'setup_sha256': '4c0de40b6aa06d1206971a15041ca76e2b164e213377a02d3fb31017d6a07720', 'door_sha256': 'a538fca3ca3bd0426570d60b7a1c8b3a44d4d96c66b59990a04e716ef4e295ff', 'next': 'RE816 private composition executed; independent review pending; NO publication', 'source_patch': False, 'integration_approved': False, 'publication_review_approved': False, 'production_ready': False, 'global_green': False, 'startup_proven': False, 'full_target_return': False, 'initializer_invoked': False, 'controller_invoked': False, 'whole_ram_oracle': False, 'hardware_proven': False, 't7_t8_t9_injected': False, 're816_publication_approved': False}
PRECEDING='7e48382152c975f8e876cb2f6ed573a797707013c6be8184846d623ed25614bf'
START='<!-- start re815-natural-registration -->'
END='<!-- end re815-natural-registration -->'
FUNCTIONDOC="# RE815 — ObjectObjects : entrée authentique, registration bornée\n\nStatut **REGISTRATION_PREFIX_PASS_NATIVE_REQUIREMENT_RED**. Revue privée indépendante\n**PASS_scoped**, aucune approbation de publication/intégration ou production.\nVerdict privé : `91a64b4efe5c16fbe416806feb46073a5bccd63404c43f2c341f428ef9dc5460`.\nManifest privé : `0784525f0d9eb2cd020554acf15bf23d0b79a745b5032574ebf3d4d8ffb173e8`,\n33 entrées vérifiées individuellement avant émission.\n\n## Preuve et limites\n\nEntrée binaire authentique ObjectObjects attribuée par le caller InitialiseObjects\net son ordre Baddy/Object/Trap/Hair/Effects; ce caller entier n'est pas exécuté.\nUne fixture synthétique RAM 2MiB, placement authentifié hérité, sans extraction disc fraîche.\nLe préfixe produit lui-même t7/t8/t9, **aucune injection**; seuls GP/SP/RA sont construits.\nLe producteur réel choisit une base différente du framework construit RE814 :\nla comparaison historique n'est pas une certification rétroactive de celui-ci.\n14 slots génériques enregistrés, 601 visites hooks (pas instructions retirées),\nstop avant la famille suivante; **pas de retour ObjectObjects cible complet ni startup**.\nOracle indépendant des 14 records, 896 octets; 896 corruptions mono-octet rejetées,\n70 stores génériques reconstruits. Égalité RAM entre replays ≠ oracle indépendant wholeRAM,\nni couverture des stores transitoires ou preuve hardware.\n\nVrai GAME/SETUP.C inchangé, i386 normal et ASan/UBSan failfast :\n14 slots poison restent inchangés après retour natif. **Requirement RED exit1**\ndans les deux modes; **characterization PASS exit0** dans les deux modes.\nCes assertions sont différentes : aucun GREEN comportemental natif, aucune correction.\nStderr des quatre runtimes vide; warnings legacy de compilation conservés.\nCible loaded=1/autres flags zéro versus natif bytes poison et pointeurs typés :\nentrées sensibles différentes, frontières préfixe cible/retour natif différentes;\naucune équivalence universelle. InitialiseGenericDoor et DoorControl seulement enregistrés,\njamais invoqués. Aucune composition item/allocation/floor/navigation dans RE815.\n\n## Progression et frontière\n\nRE813 original FAILED et RE814 original FAILED/noncertifié restent inchangés.\nRE814 demeure un checkpoint historique; RE815 avance son objectif d'entrée productrice,\npas l'objectif startup. BLOCKED-006 existant reste applicable; BLOCKED-001/002 supprimés\nrestent supprimés. Aucun patch production/source, activation, fullbuild, runtime jeu,\ngameplay, startup ou GREEN global. Le générateur ne rejoue pas les preuves privées :\nRED/GREEN de publication metadata est distinct du requirement natif RED.\n\nProchain objectif : **RE816 composition privée déjà exécutée, revue indépendante pending**.\nCe n'est ni une preuve approuvée ni une publication RE816; ne pas inventer de RE817.\n\n## Tracker\n\n- [x] Contrat publication testé RED avant générateur, log archivé.\n- [x] Approval privé exact hashes et 33 pièces vérifiés; publication metadata seulement.\n- [x] Functiondoc/CSV/story et dashboard versionné append-only avec inverse exact.\n- [ ] Revue indépendante distincte des hashes de cette publication par le parent.\n- [ ] Revue indépendante RE816; aucune intégration ou startup autorisés.\n"
STORY=FUNCTIONDOC
SECTION='<!-- start re815-natural-registration --><section id="re815"><h2>RE-815 — REGISTRATION_PREFIX_PASS_NATIVE_REQUIREMENT_RED</h2><p>PASS privé scoped : entrée authentique ObjectObjects, 14 slots, 601 visites hooks; sans injection t7/t8/t9. GP/SP/RA construits. Oracle indépendant 896 octets, 896 mutations rejetées, 70 stores. Préfixe cible PASS, pas retour complet/startup. Natif réel normal/strict : requirement RED exit1, characterization PASS exit0, runtime stderr vide; slots poison inchangés, aucune correction.</p><p>Fixtures et frontières différentes; pas équivalence globale, oracle wholeRAM, initializer/controller invoqués, production ou intégration. Rejets RE813/814 historiques conservés. BLOCKED-006 reste. RE816 composition privée exécutée, revue indépendante pending : aucune publication RE816. Revue de cette publication pending. <a href="../stories/RE-815-natural-registration.md">Story</a> · <a href="functions/re815-natural-registration.md">Contrat</a> · <a href="generated/re815-natural-registration.csv">CSV</a>.</p></section><!-- end re815-natural-registration -->\n'
OUTPUTS={'docs/reverse/generated/re815-natural-registration.csv':'CSV_TEXT','docs/reverse/functions/re815-natural-registration.md':'FUNCTIONDOC','docs/stories/RE-815-natural-registration.md':'STORY'}
def metadata():return dict(EXPECTED)
def validate(d):
 if not isinstance(d,dict) or set(d)!=set(EXPECTED) or any(type(d[k]) is not type(v) or d[k]!=v for k,v in EXPECTED.items()):
  raise ValueError('RE815 exact schema, values and types required')
 return d
def csv_row():return {k:str(v).lower() if type(v) is bool else str(v) for k,v in validate(metadata()).items()}
def render_csv():
 out=io.StringIO(newline='');row=csv_row();w=csv.DictWriter(out,fieldnames=list(row),lineterminator='\n');w.writeheader();w.writerow(row);return out.getvalue()
CSV_TEXT=render_csv()
def dashboard_before_re815(b):
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
 # Explicit RE817 only: exact suffix and entire preceding dashboard pinned.
 start817=b'<!-- start re817-native-initializer-prerequisite -->';end817=b'<!-- end re817-native-initializer-prerequisite -->'
 if start817 in b or end817 in b:
  assert b.count(start817)==b.count(end817)==1
  a817=b.index(start817)
  assert hashlib.sha256(b[a817:]).hexdigest()=='8e6e79b7750bab3ef10b63ddab3a5a2330794ae35f3eb49ad46e9549be5a124a'
  b=b[:a817]
  assert hashlib.sha256(b).hexdigest()=='b100509e34a75f6a8590bcce38b5c9430e818c8661a32858a0a94facf8b4e071'
 # Explicit RE816 only: authenticate exact suffix AND complete RE815 inverse.
 start816=b'<!-- start re816-initializer-composition -->';end816=b'<!-- end re816-initializer-composition -->'
 if start816 in b or end816 in b:
  assert b.count(start816)==b.count(end816)==1
  a816=b.index(start816)
  assert hashlib.sha256(b[a816:]).hexdigest()=='a1496dc4941eabba8228a5d0be95971a1b61e45e7848890999e77c87c7358343'
  b=b[:a816]
  assert hashlib.sha256(b).hexdigest()=='a714b8ad5482e776c416b785919efba2a1d99bad56045e4f48d7c986c21cd427'
 assert b.count(START.encode())==b.count(END.encode())==1
 assert b.endswith(SECTION.encode())
 before=b[:-len(SECTION.encode())]
 assert hashlib.sha256(before).hexdigest()==PRECEDING
 return before
def consume_approval():
 review=ROOT/'build/reverse/autonomy-20261003/re815-independent-review/verdict.json'
 proof=ROOT/'build/reverse/autonomy-20261003/re815-natural-proof'
 assert hashlib.sha256(review.read_bytes()).hexdigest()==EXPECTED['private_verdict_sha256']
 assert hashlib.sha256((proof/'manifest.json').read_bytes()).hexdigest()==EXPECTED['private_manifest_sha256']
 verdict=json.loads(review.read_text());manifest=json.loads((proof/'manifest.json').read_text())
 assert verdict['passed'] is True and verdict['integration_approved'] is False and verdict['production_approved'] is False
 assert len(manifest)==verdict['manifest_entries']==33 and manifest==verdict['producer_hashes']
 for name,digest in manifest.items():
  p=Path(name);assert not p.is_absolute() and '..' not in p.parts
  assert hashlib.sha256((proof/p).read_bytes()).hexdigest()==digest
 return verdict
def generate():
 import fcntl
 with (ROOT/'build/reverse/autonomy-mutation.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  consume_approval()
  for p,k in [('GAME/ITEMS.C','items_sha256'),('GAME/SETUP.C','setup_sha256'),('GAME/DOOR.C','door_sha256')]:
   assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==EXPECTED[k]
  dash=ROOT/'docs/reverse/reconstruction-progress.html';b=dash.read_bytes()
  if START.encode() in b or END.encode() in b:dashboard_before_re815(b)
  else:
   assert hashlib.sha256(b).hexdigest()==PRECEDING
   dash.write_bytes(b+SECTION.encode())
  for p,k in OUTPUTS.items():(ROOT/p).write_text(globals()[k])
if __name__=='__main__':generate()
