"""RE909 portable safe metadata only; no private dependencies."""
import argparse,copy,csv,hashlib,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PRIOR_DASHBOARD='docs/reverse/tomb5-progress-dashboard-re906-v1.html'
PRIOR_MAINTAINED='docs/reverse/tomb5-progress-dashboard-maintained-re906-v1.html'
DASHBOARD='docs/reverse/tomb5-progress-dashboard-re909-v1.html'
MAINTAINED='docs/reverse/tomb5-progress-dashboard.html'
STORY='docs/stories/RE-909-relocation-cd-context-publication.md'
REPORT='docs/reverse/functions/re909-relocation-cd-context-publication.md'
JSON_PATH='docs/reverse/generated/re909-relocation-cd-context-publication-v1.json'
CSV_PATH='docs/reverse/generated/re909-relocation-cd-context-tracker-v1.csv'
PRIOR_SHA='a255798fd70dbb99510280e63533f11d811245863047809971868673dbcc6b78'
MAINTAINED_SHA='e80bf1fcb2143563168fcb904f3dd7f8a024a1d5500082a7a6f8dbb8425a253d'
EXPECTED={'schema': 're909-relocation-cd-context-publication-v1', 'publication_review': 'PENDING_INDEPENDENT_EXACT_HASH_REVIEW', 'fresh_execution_scope': 'PUBLIC_METADATA_TESTS_ONLY', 'fresh_target': 0, 'fresh_native': 0, 'integration': False, 'production_patch': False, 'global_scope': 'FAIL', 'procedure_scope': 'FAIL', 'naturalcaller': 'BLOCKED', 'authentication_scope': 'selected seal/manifest membership/verdict/HANDOFF; full inventories audited by parent and reviewers, not publisher', 'authentication': {'re907-registration-prefix': {'seal_sha256': '0a7f7fd0a9f39c4e8b1b898219f7ec0c84be32583790211f27297f60a9a51e55', 'manifest_sha256': '432b5de3ead7586a62b0820fbb35ed77a5c19e1e28958b198b3c2ce34f47db08', 'entries': 34, 'verdict_sha256': '456f07d4d0bb9d158cdc8a730cea25d00354220dc61d650aa624bb5f99e427c0', 'handoff_sha256': 'e9e82131fc5de78378e4a9e028387dcff1db4e1a5c00737a2f2938816de2b8df'}, 're907-review': {'seal_sha256': '98ce16b67a6c14201191d7db06356c54652791eec2ece506ab04afe973842196', 'manifest_sha256': 'f4723b03730641e728e5ef06502e1ac236718c45550fd94ef5b2483654108d37', 'entries': 31, 'verdict_sha256': '5f3d8d7c5be2c9aa237649acd16b5c4e9f8915b7bb575011d3a5aa497a647712', 'handoff_sha256': 'b88dc329c968472061d89d3d64959b987a0247834fb9dd83a4ecdefaeedb440d'}, 're908-ai-loader': {'seal_sha256': '4813d796d5dbf82fa0af3c9f4bc9b568037127e3ceac70b8061077c7e6d1184d', 'manifest_sha256': '6751dab13ae80be31fea0b3f35f686df03622dfe37f0f916bf493bdc29c9efe2', 'entries': 31, 'verdict_sha256': '2b73b7cee52faf3fed5324b2c81b9391b53ed92fe0cddf22fee3a9b514494cae', 'handoff_sha256': '6a5016cee8a36a21133ad70da66cdeb3fe4c4e444536912ba778cbe883027617'}, 're908-review': {'seal_sha256': '1c41b4a345bc79ce81a5f9d80711db249236f062f6c1002f1e0e6fea10a03345', 'manifest_sha256': 'dec93138ddc75416b82068cb9a041b5679bb528f1399df5bae1e15aea48ca2ee', 'entries': 36, 'verdict_sha256': '96feb7aa35e02390ff51a1f7c3acece3a7f05c18c73c9e604e332d009a8c2c8e', 'handoff_sha256': '28c05e3ea63a741b6a66b7b236101768b00662c84d37f4709dc7eb2890245980'}}, 'RE907': {'review_passed': True, 'security_concerns': [], 'logic_errors': [], 'relocated_objects': 460, 'relocation_bytes': 29440, 'whole_RAM_bytes': 4194304, 'GPR_count': 32, 'producer_target_prefixes': 1, 'producer_interpreter_prefixes': 1, 'reviewer_target_prefixes': 1, 'reviewer_interpreter_prefixes': 1, 'visits_each': 13578, 'interpreted_stores_each': 6942, 'returns_each': 0, 'first_dependency_object': 41, 'slot': 22, 'slot_state': 'NULL', 'registration284': 'BLOCKED_BEFORE_OBJECTOBJECTS', 'loader_fresh': 0}, 'RE908': {'producer_passed': False, 'review_diagnostic_passed': True, 'review_security_concerns': [], 'review_logic_errors': [], 'functional_passed': False, 'functional': 'BLOCKED_CD_CONTEXT_NOT_PRODUCED', 'producer_functional_FAIL': 1, 'reviewer_functional_FAIL': 1, 'functional_GREEN': 0, 'producer_prefix_recoveries': 1, 'reviewer_prefix_recoveries': 1, 'prefix_visits_each': 87017, 'historical_CD_doubles_each': 3, 'real_prefix_allocations_each': 2, 'producer_target_suffixes': 1, 'reviewer_target_suffixes': 1, 'producer_oracle_suffixes': 1, 'reviewer_oracle_suffixes': 1, 'suffix_visits_each': 39, 'interpreted_stores_each': 10, 'suffix_returns_each': 0, 'whole_RAM_bytes': 4194304, 'GPR_count': 32, 'stop': 'before CdControl; SDK unexecuted', 'cd_current_sector': 0, 'cd_base_sector': 0, 'ISO_catalogue_sector': 18040, 'catalogue_scope': 'STATIC_ISO_NOT_TARGET_READ', 'descriptor': 30, 'slot': 22, 'slot_state': 'NULL_NOT_ABSENT_ON_DISC', 'catalogue_target_reads': 0, 'AI_allocations': 0, 'AI_relocations': 0, 'AI_installs': 0, 'registration': 0, 'InitialiseItem': 0, 'native': 0, 'runtime': 0}, 'next_objective': 'PROPOSE_ONLY real upstream CD context provenance; research CLOSED, no execution authorized'}
COMPATIBILITY_DELTAS={'scripts/reverse/re906_publication.py': {'before_sha256': 'ad014b728f1aa77be34633891e7fddee916179555757cff2d5bb4600ac83d7ab', 'replacements': [('\ndef preceding_maintained(data):return inverse(data,MAINTAINED_SHA)', "\ndef preceding_maintained(data):\n if b'<!-- RE909 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re909_publication.py'))['preceding_maintained'](data)\n return inverse(data,MAINTAINED_SHA)\ndef read_maintained():\n data=(ROOT/MAINTAINED).read_bytes()\n if b'<!-- RE909 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re909_publication.py'))['preceding_maintained'](data)\n return data"), ('\ndef original_compatibility(path,text):\n', "\ndef original_compatibility(path,text):\n if '# RE909 exact authenticated successor' in text or path=='scripts/reverse/re904_publication.py':\n  import runpy\n  text=runpy.run_path(str(ROOT/'scripts/reverse/re909_publication.py'))['original_compatibility'](path,text)\n"), ("\n  if (ROOT/p).read_bytes()!=b:raise ValueError('generated drift '+p)", "\n  if (read_maintained() if p==MAINTAINED else (ROOT/p).read_bytes())!=b:raise ValueError('generated drift '+p)")]}, 'tests/reverse/test_re906_publication.py': {'before_sha256': 'fe4aa2292c16f4f9dc79a815bc7dd13eba235d0511c6f764616a958aae6bd1a3', 'replacements': [('for p,b in out.items():assert (ROOT/p).read_bytes()==b;m.guard_output(p,b)', 'for p,b in out.items():assert (m.read_maintained() if p==m.MAINTAINED else (ROOT/p).read_bytes())==b;m.guard_output(p,b)')]}, 'scripts/reverse/re904_publication.py': {'before_sha256': '60413d7d7cfafffb0519b481fefe54999dce5ef321af3daaf6ed3b2b98cb98db', 'replacements': [('\n spec=COMPATIBILITY_DELTAS[path]', "\n if '# RE909 exact authenticated successor' in text:\n  import runpy\n  text=runpy.run_path(str(ROOT/'scripts/reverse/re909_publication.py'))['original_compatibility'](path,text)\n spec=COMPATIBILITY_DELTAS[path]")]}, 'tests/reverse/test_re830_table_provenance_publication.py': {'before_sha256': '303593664659037bb6eba4bfba0517a2ae2a1e36aad07af390d1be6df4d6c17c', 'replacements': [('    # RE906 exact authenticated successor; preserve contiguous older adapters.\n', "    # RE909 exact authenticated successor; preserve contiguous older adapters.\n    if b'<!-- RE909 PUBLICATION' in data:\n        import runpy\n        try:\n            data = runpy.run_path(str(ROOT/'scripts/reverse/re909_publication.py'))['preceding_maintained'](data)\n        except ValueError as exc:\n            raise AssertionError('malformed RE909 successor') from exc\n    # RE906 exact authenticated successor; preserve contiguous older adapters.\n")]}}
OUTPUT_PATHS=(STORY,REPORT,JSON_PATH,CSV_PATH,DASHBOARD,MAINTAINED)
PUBLIC_PATHS=OUTPUT_PATHS+(PRIOR_MAINTAINED,'scripts/reverse/re909_publication.py','tests/reverse/test_re909_publication.py')+tuple(COMPATIBILITY_DELTAS)
SECTION='\n<!-- RE909 PUBLICATION BEGIN -->\n<section id="re909-publication-v1" data-integration="false"><h2>CURRENT RE909 — reviewed RE907 / RE908 diagnostic metadata</h2><p>RE907 relocation460 records29440 bytes,13578 visits6942 interpreted stores; object41 dependency slot22 NULL; registration284 BLOCKED. RE908 conditional recovery87017 visits3 historical CD doubles2 real allocations; retained CPU/RAM suffix39 visits10 interpreted stores stops before CdControl. CD current/base0; ISO catalogue18040 STATIC NOT TARGET READ, descriptor30 maps slot22 present on disc. Producer functional FAIL1 and reviewer FAIL1, functional GREEN0. No AI allocation/relocation/install, registration, InitialiseItem or native/runtime.</p><p>Global FAIL / procedure FAIL / integration=false / naturalcaller BLOCKED. PENDING_INDEPENDENT_EXACT_HASH_REVIEW. Publication adds ZERO numerical replays. Research CLOSED.</p><p><a href="../stories/RE-909-relocation-cd-context-publication.md">Story / acceptance</a> · <a href="functions/re909-relocation-cd-context-publication.md">Evidence / limitations</a> · <a href="generated/re909-relocation-cd-context-publication-v1.json">Metadata</a> · <a href="generated/re909-relocation-cd-context-tracker-v1.csv">Tracker</a></p></section>\n<!-- RE909 PUBLICATION END -->\n'
def metadata():return copy.deepcopy(EXPECTED)
def validate(data):
 def exact(a,b):
  if type(a) is not type(b):return False
  if isinstance(b,dict):return set(a)==set(b) and all(exact(a[k],b[k]) for k in b)
  if isinstance(b,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
  return a==b
 if not exact(data,EXPECTED):raise ValueError('exact RE909 recursive schema types/counts/hash/scope required')
 return data
def digest(b):return hashlib.sha256(b).hexdigest()
def inverse(data,sha):
 suffix=SECTION.encode()+b'</html>'
 if not data.endswith(suffix) or data.count(b'<!-- RE909 PUBLICATION BEGIN -->')!=1 or data.count(b'<!-- RE909 PUBLICATION END -->')!=1:raise ValueError('exact unique RE909 suffix required')
 before=data[:-len(suffix)]+b'</html>'
 if digest(before)!=sha:raise ValueError('exact predecessor bytes changed')
 return before
def preceding_dashboard(data):return inverse(data,PRIOR_SHA)
def preceding_maintained(data):
 if b'<!-- RE911 PUBLICATION' in data:
  import runpy
  data=runpy.run_path(str(ROOT/'scripts/reverse/re911_publication.py'))['preceding_maintained'](data)
 return inverse(data,MAINTAINED_SHA)
def read_maintained():
 data=(ROOT/MAINTAINED).read_bytes()
 if b'<!-- RE911 PUBLICATION' in data:
  import runpy
  data=runpy.run_path(str(ROOT/'scripts/reverse/re911_publication.py'))['preceding_maintained'](data)
 return data
def maintained_before():
 b=(ROOT/PRIOR_MAINTAINED).read_bytes()
 if digest(b)!=MAINTAINED_SHA:raise ValueError('maintained historical fixture drift')
 return b

RAW=re.compile(rb'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|raw_opcode|raw_pc|register_values|target_address|payload_offset|data:image|```(?:asm|mips|cpp|c)\b',re.I)
SECRET=re.compile(rb'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|(?:api[_-]?key|password|secret)\s*[:=]\s*[\"\x27][^\"\x27\s]{12,}',re.I)
def guard_added(path,payload):
 p=Path(path)
 if p.is_absolute() or '..' in p.parts or path not in PUBLIC_PATHS:raise ValueError('outside explicit RE909 public scope')
 if len(payload)>100000 or b'\0' in payload:raise ValueError('heavy/binary payload')
 payload.decode('utf-8')
 if SECRET.search(payload):raise ValueError('secret')
 if p.suffix!='.py' and RAW.search(payload):raise ValueError('raw evidence')
def guard_output(path,payload):
 if path not in OUTPUT_PATHS:raise ValueError('not generated metadata')
 if path in (DASHBOARD,MAINTAINED):
  (preceding_dashboard if path==DASHBOARD else preceding_maintained)(payload);guard_added(path,SECTION.encode())
 else:guard_added(path,payload)
DOC='# RE909 — publication metadata-only RE907 / RE908\n\n## Progression\n- [x] RED discriminant puis GREEN publication metadata seulement.\n- [x] Verdicts et HANDOFF sélectionnés authentifiés dans manifests scellés.\n- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW; worktree-only, aucun stage/commit/push.\n\n## Evidence\nRE907: diagnostic strict accepté, relocation460 records29440 octets; première dépendance objet41 / slot22 NULL. Registration284 non atteinte. RE908: diagnostic strict accepté mais verdict fonctionnel producteur passed=false conservé. Récupérations conditionnelles et suffixes producteur/reviewer archivés ici, pas replays frais de publication.\n\n## Limitations\nRAM4194304 et32 GPR comparés dans preuves archivées, oracle logiciel non hardware. Visites non instructions retirées; stores interprétés non trace transitoire exhaustive. RE907 CPU entrée construit depuis RAM archivée RE855; RE908 CPU/RAM retenus après récupération conditionnelle. Trois doubles CD historiques seulement dans préfixe, aucun SDK/double suffixe. Catalogue ISO secteur18040 STATIC NOT TARGET READ; current/base CD0. Descripteur30 -> slot22 présent sur disque: NULL RAM ne signifie pas absence sur disque. Aucun AI load/allocation/relocation/install, registration, InitialiseItem, native/runtime frais.\n\n## Blockers\nglobal FAIL / procédure FAIL / integration=false / naturalcaller BLOCKED. firstFAIL historiques, RE893 partial FAIL, lancement reviewer absent et gaps discovery/transport non rétrocertifiés. BLOCKED-001/002 supprimés par utilisateur; report-tech untracked intact. Source privée XYZ non intégrée. Recherche CLOSED, aucune nouvelle RE ou compilation native/runtime.\n\n## Acceptance\n- [x] Schéma récursif exact types bool/int, compteurs et pins; mutants de chaque feuille.\n- [x] Dashboard versionné et maintenu: inverse exact prédécesseur RE906, suffixe unique strict.\n- [x] Tests metadata frais et export public-only sans build/proofs; gardes baseline-aware avec nodeids exacts.\n- [ ] Revue publique indépendante exact allowlist/hashmanifest.\n- [ ] Provenance CD naturelle, registration, startup/gameplay et équivalence globale restent bloqués.\n\n## Handoff\nPROPOSE_ONLY provenance CD amont réelle, sans exécution autorisée.\n'
def document(report=False):
 return DOC+"\n"+json.dumps(EXPECTED,indent=2,sort_keys=True)+"\n"
def render():
 d=validate(metadata());before=(ROOT/PRIOR_DASHBOARD).read_bytes()
 if digest(before)!=PRIOR_SHA or not before.endswith(b'</html>'):raise ValueError('exact RE906 predecessor required')
 out={STORY:document().encode(),REPORT:document(True).encode(),JSON_PATH:(json.dumps(d,indent=2,sort_keys=True)+'\n').encode(),DASHBOARD:before[:-7]+SECTION.encode()+b'</html>',MAINTAINED:maintained_before()[:-7]+SECTION.encode()+b'</html>'}
 stream=io.StringIO(newline='');w=csv.writer(stream,lineterminator='\n');w.writerow(['ticket','scope','status','integration','publication_review'])
 for ticket,status in [('RE907','SCOPED_DIAGNOSTIC_PASS_REGISTRATION_BLOCKED'),('RE908','DIAGNOSTIC_PASS_FUNCTIONAL_BLOCKED_CD_CONTEXT'),('RE909','PUBLIC_METADATA_TESTS_ONLY')]:w.writerow([ticket,'archived proof' if ticket!='RE909' else 'fresh metadata',status,'false',d['publication_review']])
 out[CSV_PATH]=stream.getvalue().encode()
 for p,b in out.items():guard_output(p,b)
 return out
def original_compatibility(path,text):
 spec=COMPATIBILITY_DELTAS[path]
 for old,new in reversed(spec['replacements']):
  if text.count(new)!=1:raise ValueError('exact RE909 compatibility adapter required')
  text=text.replace(new,old)
 if digest(text.encode())!=spec['before_sha256']:raise ValueError('historical compatibility code changed')
 return text
def compatibility_pins():
 for p in COMPATIBILITY_DELTAS:original_compatibility(p,(ROOT/p).read_text())
def check():
 compatibility_pins()
 for p,b in render().items():
  if (read_maintained() if p==MAINTAINED else (ROOT/p).read_bytes())!=b:raise ValueError('generated drift '+p)
 for p in PUBLIC_PATHS:
  if p not in (DASHBOARD,MAINTAINED,PRIOR_MAINTAINED):guard_added(p,(ROOT/p).read_bytes())
 print('RE909 PUBLIC_METADATA_TESTS_ONLY PASS; exact-public-hash independent review PENDING')
if __name__=='__main__':
 argparse.ArgumentParser(description=__doc__).parse_args();check()
