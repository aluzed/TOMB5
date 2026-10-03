"""RE816 safe metadata publication only; no target replay/source patch."""
import csv, hashlib, io, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
EXPECTED={'status': 'CONDITIONAL_INITIALIZER_COMPOSITION_PASS_NATIVE_REQUIREMENT_RED', 'private_review': 'PASS_scoped', 'private_verdict_sha256': '808046ae20f2f7df911cebdedbceb00fdbf34e44f311eee8a6c50cfe24957014', 'private_manifest_sha256': '6115bc3346b89bb941bd4ddb804fba82587f60a90f0dfc8357f5a130d4945563', 'manifest_entries': 49, 'prefix_visits': 601, 'caller_visits': 1147, 'selected_bytes': 2992, 'corruptions_rejected': 2992, 'immutable_events': 35, 'allocation_bytes': 92, 'copy_calls': 4, 'getdoor_calls': 5, 'shut_calls': 4, 'native_requirement_exit': 1, 'strict_requirement_exit': 1, 'native_characterization_exit': 0, 'strict_characterization_exit': 0, 'same_cpu_ram': True, 'initializer_target_return': True, 'caller_target_return': True, 'native_runtime_stderr_empty': True, 'dispatch': 'conditional external A0 RA; retained prefix SP', 'native_door': 'compiled then dead-stripped; initializer absent', 'source_patch': False, 'integration_approved': False, 'publication_review_approved': False, 'production_ready': False, 'global_green': False, 'startup_proven': False, 'objectobjects_full_return': False, 'native_initializer_invoked': False, 'controller_invoked': False, 'whole_ram_oracle': False, 'hardware_proven': False, 'activation_approved': False, 'floor_mutation_equivalent': False, 're817_approved': False, 'next': 'RE817 private concurrent; independent review pending; not approved; no result claimed'}
PRECEDING='a714b8ad5482e776c416b785919efba2a1d99bad56045e4f48d7c986c21cd427'
START='<!-- start re816-initializer-composition -->'
END='<!-- end re816-initializer-composition -->'
SECTION='<!-- start re816-initializer-composition --><section id="re816"><h2>RE-816 — CONDITIONAL_INITIALIZER_COMPOSITION_PASS_NATIVE_REQUIREMENT_RED</h2><p>Revue privée indépendante PASS_scoped : préfixe registration naturel 601 visites, dispatch conditionnel externe sur même CPU/RAM, initializer et caller retournent, 1147 visites. Allocation réelle 92 octets, copy4, GetDoor5, shut4, navigation et ItemNewRoom exécutés. Oracle indépendant sélectionné 2992 octets, 2992 corruptions rejetées; ledger immuable 35 événements.</p><p>SETUP/ITEMS natifs réels normal/strict : requirement RED exit1, characterization PASS exit0. DOOR compilé puis dead-stripped, initializer natif absent. Checker cell9 non discriminant, aucune équivalence floor-mutation. Pas retour ObjectObjects/startup, wholeRAM, hardware, activation, production ou intégration. RE815 historique pending conservé; RE816 privé désormais approuvé scoped, publication union RE815+RE816 pending revue finale séparée. BLOCKED-003/004/006 restent; RE817 privé concurrent non approuvé, aucun résultat revendiqué. <a href="../stories/RE-816-initializer-composition.md">Story</a> · <a href="functions/re816-initializer-composition.md">Contrat</a> · <a href="generated/re816-initializer-composition.csv">CSV</a>.</p></section><!-- end re816-initializer-composition -->\n'
FUNCTIONDOC="# RE816 — registration naturelle puis composition conditionnelle initializer\n\nStatut **CONDITIONAL_INITIALIZER_COMPOSITION_PASS_NATIVE_REQUIREMENT_RED**.\nRevue privée indépendante **PASS_scoped**, non approbation de publication,\nd'intégration, production ou activation. Publication union RE815+RE816 en attente\nd'une revue finale distincte; les mentions pending RE815 restent historiques.\nVerdict privé : `808046ae20f2f7df911cebdedbceb00fdbf34e44f311eee8a6c50cfe24957014`.\nManifest privé : `6115bc3346b89bb941bd4ddb804fba82587f60a90f0dfc8357f5a130d4945563`,\n49 entrées authentifiées individuellement avant génération.\n\n## Preuve bornée et frontières\n\nUne fixture synthétique, binaires hérités authentifiés, aucune extraction fraîche.\nPréfixe ObjectObjects naturel : 14 slots, 601 visites hooks, pas instructions retirées;\nGP/SP/RA construits initialement, t7/t8/t9 produits sans injection.\nObjectObjects suspendu avant la famille suivante : **ni retour complet ni startup**.\nDispatch conditionnel extérieur InitialiseItem : A0/RA construits, même CPU/RAM\net SP du préfixe suspendu conservés. Callback lu naturellement depuis la table\net initializer cible complet, retour au caller puis retour caller : 1147 visites.\nCe n'est pas une preuve d'appel naturel depuis le startup.\nAllocateur réel : allocation complète 92 octets; copy4, GetDoor5, shut4,\nnavigation et ItemNewRoom réellement exécutés, sans hooks de remplacement.\nOracle indépendant : sélection 2992 octets, 2992 corruptions mono-octet rejetées,\nledger immuable 35 événements et ordre vérifiés. Régions sélectionnées seulement,\npas wholeRAM/memory safety/hardware. Entrée initializer authentique; état\npréinitializer caller non reconstruit intégralement par un oracle indépendant.\n\n## Natif, readiness et écarts conservés\n\nVrais SETUP/ITEMS inchangés, i386 normal et strict ASan/UBSan failfast.\n**Requirement RED exit1** dans chacun des deux modes; **characterization PASS\nexit0** dans chacun. Stderr des runtimes vide, warnings de compilation distincts.\nDOOR compilé puis dead-stripped au link : **initializer natif absent**, pas exécuté.\nSETUP ObjectObjects natif signale Unimplemented sur stdout; aucun enregistrement\nnatif de porte prouvé. Characterization d'absence n'est pas GREEN comportemental.\nChecker natif cell9 non discriminant; caller cell12, porte cell11, floor uniforme :\naucune équivalence floor-mutation/initializer/native revendiquée.\nDeux incidents privés conservés : hypothèse SP corrigée vers SP sauvegardé;\ncoordonnée fixture/oracle porte corrigée avant natif. Pas de modification d'opcodes,\nni certification rétroactive des échecs RE813/RE814 originaux.\nPas controller, gameplay, activation, fullbuild, intégration ou GREEN global.\n\n## Progression et critères\n\n- [x] Preuve privée distincte approuvée scoped, 49 entrées vérifiées.\n- [x] Publication metadata-only préparée sous contrat TDD; sources inchangées.\n- [ ] Revue finale exacte du manifest PUBLIC UNION RE815+RE816.\n- [ ] Implémentation/équivalence initializer native avant activation (BLOCKED-006).\n- [ ] Startup, hardware, fullbuild/intégration : non prouvés; BLOCKED-003/004 restent.\n\nRE817 privé concurrent, revue indépendante pending, non approuvé; aucun résultat\nRE817 revendiqué et aucune recherche supplémentaire exécutée par cette publication.\nBLOCKED-001/002 restent absents; report utilisateur non suivi préservé.\n"
STORY=FUNCTIONDOC
OUTPUTS={'docs/reverse/generated/re816-initializer-composition.csv':'CSV_TEXT','docs/reverse/functions/re816-initializer-composition.md':'FUNCTIONDOC','docs/stories/RE-816-initializer-composition.md':'STORY'}
def metadata():return dict(EXPECTED)
def validate(d):
 if not isinstance(d,dict) or set(d)!=set(EXPECTED) or any(type(d[k]) is not type(v) or d[k]!=v for k,v in EXPECTED.items()):raise ValueError('RE816 exact schema, values and types required')
 return d
def csv_row():return {k:str(v).lower() if type(v) is bool else str(v) for k,v in validate(metadata()).items()}
def render_csv():
 out=io.StringIO(newline='');row=csv_row();w=csv.DictWriter(out,fieldnames=list(row),lineterminator='\n');w.writeheader();w.writerow(row);return out.getvalue()
CSV_TEXT=render_csv()
def dashboard_before_re816(b):
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
 assert b.count(START.encode())==b.count(END.encode())==1
 assert b.endswith(SECTION.encode())
 before=b[:-len(SECTION.encode())]
 assert hashlib.sha256(before).hexdigest()==PRECEDING
 return before
def consume_approval():
 v=ROOT/'build/reverse/autonomy-20261003/re816-independent-review/verdict.json';proof=ROOT/'build/reverse/autonomy-20261003/re816-initializer-composition';m=proof/'manifest.json'
 assert hashlib.sha256(v.read_bytes()).hexdigest()==EXPECTED['private_verdict_sha256']
 assert hashlib.sha256(m.read_bytes()).hexdigest()==EXPECTED['private_manifest_sha256']
 d=json.loads(v.read_text());manifest=json.loads(m.read_text())
 assert d['passed'] is True and d['integration_approved'] is False and d['production_approved'] is False
 assert len(manifest)==d['checks']['manifest_entries']==49 and manifest==d['delivery_sha256']
 for name,digest in manifest.items():
  p=Path(name);assert not p.is_absolute() and '..' not in p.parts
  assert hashlib.sha256((proof/p).read_bytes()).hexdigest()==digest
 for name,digest in d['source_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
 return d
def generate():
 import fcntl
 with (ROOT/'build/reverse/autonomy-mutation.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);consume_approval()
  dash=ROOT/'docs/reverse/reconstruction-progress.html';b=dash.read_bytes()
  if START.encode() in b or END.encode() in b:dashboard_before_re816(b)
  else:
   assert hashlib.sha256(b).hexdigest()==PRECEDING
   dash.write_bytes(b+SECTION.encode())
  for p,k in OUTPUTS.items():(ROOT/p).write_text(globals()[k])
if __name__=='__main__':generate()
