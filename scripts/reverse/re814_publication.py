"""Safe RE814 metadata only; does not import private proof or execute game code."""
import csv, hashlib, io
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
EXPECTED={'status': 'BOUNDED_CONTINUATION_CHARACTERIZATION', 'corrected_review': 'PASS_scoped', 'original_review': 'FAILED/noncertifié', 'upstream_re813_original_review': 'FAILED', 'corrected_verdict_sha256': 'b4c4ded966675715a1096e98ef9571351f59703e43a16c3c2ce0fb788f7cbfd7', 'corrected_manifest_sha256': '7bcd98de7a6bb4dc9b7f7932205a84748102e571249571fc1d1e2608b686fc02', 'items_sha256': '4e4374916bf454fd577fb92d89e7160a1b818e5a744e9244ad89c44fbb0ef84f', 'setup_sha256': '4c0de40b6aa06d1206971a15041ca76e2b164e213377a02d3fb31017d6a07720', 'cases': 8, 'target_complete_returns': 4, 'target_initializer_stops': 4, 'hook_visits': 3696, 'native_returns_per_mode': 8, 'status_room_floor_equal_per_mode': 8, 'full582_equal_per_mode': 6, 'active_head_differences_per_mode': 2, 'normal_strict_scope': 'i386 O0 normal + ASan/UBSan failfast only', 'semantic_frontiers': 'generic target BEFORE initializer vs native complete; MIP target complete', 'constructed_registers': 't9 GP SP', 'status_rewrite': 'ITEM_ACTIVE after Add NULL without active/head activation', 'frontier': 'BLOCKED-006; RE815 natural ObjectObjects producer entry and generic initializer dependencies NOT executed', 'source_patch': False, 'production_ready': False, 'global_green': False, 'publication_review_approved': False, 'behavioral_red': False, 'initializer_executed': False, 'controller_invoked': False, 'whole_startup_proven': False, 'whole_ram_proven': False, 'hardware_proven': False, 'gameplay_performed': False, 'fullbuild_performed': False, 'runtime_performed': False, 'DoorControl_activated': False, 'AnimateItem_activated': False, 't7_t8_injected': False, 're815_executed': False}
PRECEDING='5c7b6d809cf6ffc00890ed0de5ee9744bc62579e10a742c67c218a13e943b081'
START="<!-- start re814-bounded-continuation -->"
END="<!-- end re814-bounded-continuation -->"
FUNCTIONDOC="# RE814 — InitialiseItem : continuation bornée\n\nStatut **BOUNDED_CONTINUATION_CHARACTERIZATION**. Revue privée indépendante fraîche\n**PASS_scoped**, pas validation de publication/intégration ni production-ready.\nVerdict : `b4c4ded966675715a1096e98ef9571351f59703e43a16c3c2ce0fb788f7cbfd7`.\nManifest corrigé : `7bcd98de7a6bb4dc9b7f7932205a84748102e571249571fc1d1e2608b686fc02`.\n\n## Preuve et limites\n\nHuit cas nouveaux construits object 284/285 × room 0/1 × activation absente/complète,\nloaded 1 fixe. Registration par producteur littéral authentique initializer/controller,\nsans injection t7/t8; seuls t9, GP et SP construits. L'entrée complète ObjectObjects\net le startup naturel ne sont pas exécutés; hashes hérités, pas extraction disc fraîche.\nQuatre retours cible complets MIP (pile restaurée), quatre stops **BEFORE initializer**\ngeneric-door; 3696 visites hooks, pas instructions retirées. Le natif termine :\n**frontières sémantiques différentes**, aucune équivalence universelle callback.\n\nVrais GAME/SETUP.C et GAME/ITEMS.C : i386 O0 normal + ASan/UBSan failfast uniquement,\nhuit retours par mode; status/room/floor concordent 8/8. Snapshot complet comparé\nitems + activehead + roomheads de 582 octets : égalité 6/8 et deux écarts attendus\nactive/head par mode car registration native absente. Insertion room, floor signé\net box précèdent callback. Après Add NULL, status réécrit ITEM_ACTIVE sans activation\nactive/head : status actif n'implique pas insertion dans la liste active.\n\nOriginal RE814 scellé **FAILED/noncertifié** : printf floor reçoit long via format\nincorrect; correction indépendante séparée, aucune certification rétroactive.\nOriginal RE813 **FAILED reste FAILED**. Aucun candidat source ni behavioral RED :\nRED/GREEN de cette publication concerne les artefacts metadata seulement.\nAucune activation AnimateItem/DoorControl, initializer/controller non exécutés;\npas startup complet, wholeRAM, hardware, fullbuild, runtime jeu, gameplay ou GREEN global.\nLa preuve privée existante n'est pas rejouée par ce générateur portable.\n\n## Frontière\n\nBLOCKED-006 existant reste applicable, pas de résurrection BLOCKED-001/002.\nRE815 : atteindre naturellement le producteur depuis l'entrée ObjectObjects/startup,\npuis composer initializer generic-door et ses dépendances allocation/floor/navigation.\n**Non exécuté**, aucune nouvelle RE/matrice; source inchangée, NO PATCH.\n"
STORY="# RE814 — InitialiseItem : continuation bornée\n\nStatut **BOUNDED_CONTINUATION_CHARACTERIZATION**. Revue privée indépendante fraîche\n**PASS_scoped**, pas validation de publication/intégration ni production-ready.\nVerdict : `b4c4ded966675715a1096e98ef9571351f59703e43a16c3c2ce0fb788f7cbfd7`.\nManifest corrigé : `7bcd98de7a6bb4dc9b7f7932205a84748102e571249571fc1d1e2608b686fc02`.\n\n## Preuve et limites\n\nHuit cas nouveaux construits object 284/285 × room 0/1 × activation absente/complète,\nloaded 1 fixe. Registration par producteur littéral authentique initializer/controller,\nsans injection t7/t8; seuls t9, GP et SP construits. L'entrée complète ObjectObjects\net le startup naturel ne sont pas exécutés; hashes hérités, pas extraction disc fraîche.\nQuatre retours cible complets MIP (pile restaurée), quatre stops **BEFORE initializer**\ngeneric-door; 3696 visites hooks, pas instructions retirées. Le natif termine :\n**frontières sémantiques différentes**, aucune équivalence universelle callback.\n\nVrais GAME/SETUP.C et GAME/ITEMS.C : i386 O0 normal + ASan/UBSan failfast uniquement,\nhuit retours par mode; status/room/floor concordent 8/8. Snapshot complet comparé\nitems + activehead + roomheads de 582 octets : égalité 6/8 et deux écarts attendus\nactive/head par mode car registration native absente. Insertion room, floor signé\net box précèdent callback. Après Add NULL, status réécrit ITEM_ACTIVE sans activation\nactive/head : status actif n'implique pas insertion dans la liste active.\n\nOriginal RE814 scellé **FAILED/noncertifié** : printf floor reçoit long via format\nincorrect; correction indépendante séparée, aucune certification rétroactive.\nOriginal RE813 **FAILED reste FAILED**. Aucun candidat source ni behavioral RED :\nRED/GREEN de cette publication concerne les artefacts metadata seulement.\nAucune activation AnimateItem/DoorControl, initializer/controller non exécutés;\npas startup complet, wholeRAM, hardware, fullbuild, runtime jeu, gameplay ou GREEN global.\nLa preuve privée existante n'est pas rejouée par ce générateur portable.\n\n## Frontière\n\nBLOCKED-006 existant reste applicable, pas de résurrection BLOCKED-001/002.\nRE815 : atteindre naturellement le producteur depuis l'entrée ObjectObjects/startup,\npuis composer initializer generic-door et ses dépendances allocation/floor/navigation.\n**Non exécuté**, aucune nouvelle RE/matrice; source inchangée, NO PATCH.\n\n## Tracker\n\n- [x] Contrat metadata testé d'abord RED puis publication minimale GREEN.\n- [x] Functiondoc, CSV et dashboard append-only; rejets historiques préservés.\n- [ ] Revue indépendante de publication et décision d'intégration.\n- [ ] RE815 naturel et dépendances initializer, non exécutés/non autorisés ici.\n"
SECTION='<!-- start re814-bounded-continuation --><section id="re814"><h2>RE-814 — BOUNDED_CONTINUATION_CHARACTERIZATION</h2><p>Private corrected independent PASS scoped; original FAILED/noncertifié unchanged. 8 cases, 4 complete target returns and 4 stops BEFORE initializer, 3696 hook visits. Native i386 O0 normal + ASan/UBSan failfast: 8 returns/mode, status/room/floor 8/8, full 582 bytes 6/8; 2 expected active/head differences: native registration absent.</p><p>Authentic literal producer without initializer/controller injection; t9 GP/SP constructed. Generic target stop and native complete have different semantic frontiers; MIP complete. ITEM_ACTIVE rewritten after Add NULL without active/head activation. No production patch, activation, behavioral RED, startup, wholeRAM, hardware, gameplay or global GREEN. Original RE813 FAILED preserved. BLOCKED-006 remains; RE815 natural ObjectObjects producer entry and generic initializer dependencies NOT executed. Publication review pending. <a href="../stories/RE-814-bounded-continuation.md">Story</a> · <a href="functions/re814-bounded-continuation.md">Contract</a> · <a href="generated/re814-bounded-continuation.csv">CSV</a>.</p></section><!-- end re814-bounded-continuation -->\n'
OUTPUTS={'docs/reverse/generated/re814-bounded-continuation.csv': 'CSV_TEXT', 'docs/reverse/functions/re814-bounded-continuation.md': 'FUNCTIONDOC', 'docs/stories/RE-814-bounded-continuation.md': 'STORY'}
def metadata():
 return dict(EXPECTED)
def validate(d):
 if not isinstance(d,dict) or set(d)!=set(EXPECTED) or any(type(d[k]) is not type(v) or d[k]!=v for k,v in EXPECTED.items()):
  raise ValueError('RE814 metadata rejected: exact schema, values and types required')
 return d
def csv_row():
 return {k:str(v).lower() if type(v) is bool else str(v) for k,v in validate(metadata()).items()}
def render_csv():
 o=io.StringIO(newline='');row=csv_row();w=csv.DictWriter(o,fieldnames=list(row),lineterminator='\n');w.writeheader();w.writerow(row);return o.getvalue()
CSV_TEXT=render_csv()
def dashboard_before_re814(b):
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
 # Explicit RE815 only: exact suffix digest and inverse whole RE814 dashboard.
 start815=b'<!-- start re815-natural-registration -->';end815=b'<!-- end re815-natural-registration -->'
 if start815 in b or end815 in b:
  assert b.count(start815)==b.count(end815)==1
  a815=b.index(start815)
  assert hashlib.sha256(b[a815:]).hexdigest()=='d826a4249ebcb42fe75dddc1aec5fe5c98e2d1b4f72f1fc998cbcb7d0626d3fe'
  b=b[:a815]
  assert hashlib.sha256(b).hexdigest()=='7e48382152c975f8e876cb2f6ed573a797707013c6be8184846d623ed25614bf'
 section=SECTION.encode()
 assert b.count(START.encode())==b.count(END.encode())==1
 assert b.endswith(section)
 prior=b[:-len(section)]
 assert hashlib.sha256(prior).hexdigest()==PRECEDING
 return prior
def generate():
 import fcntl
 with (ROOT/'build/reverse/autonomy-mutation.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for p,k in [('GAME/ITEMS.C','items_sha256'),('GAME/SETUP.C','setup_sha256')]:
   assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==EXPECTED[k]
  dash=ROOT/'docs/reverse/reconstruction-progress.html';b=dash.read_bytes()
  if START.encode() in b or END.encode() in b:dashboard_before_re814(b)
  else:
   assert hashlib.sha256(b).hexdigest()==PRECEDING
   dash.write_bytes(b+SECTION.encode())
  for p,key in OUTPUTS.items():(ROOT/p).write_text(globals()[key])
if __name__=='__main__':generate()
