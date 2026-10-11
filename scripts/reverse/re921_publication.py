"""RE921 portable metadata publication; no private runtime dependency."""
import argparse,copy,csv,hashlib,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PRIOR_DASHBOARD='docs/reverse/tomb5-progress-dashboard-re919-v1.html'
PRIOR_MAINTAINED='docs/reverse/tomb5-progress-dashboard-maintained-re919-v1.html'
DASHBOARD='docs/reverse/tomb5-progress-dashboard-re921-v1.html'
MAINTAINED='docs/reverse/tomb5-progress-dashboard.html'
STORY='docs/stories/RE-921-openbios-continuation-proof-publication.md'
REPORT='docs/reverse/functions/re921-openbios-continuation-proof-publication.md'
JSON_PATH='docs/reverse/generated/re921-openbios-continuation-proof-publication-v1.json'
CSV_PATH='docs/reverse/generated/re921-openbios-continuation-proof-tracker-v1.csv'
PRIOR_SHA='ce09d86bb5c6197a5ad898ad7a3306200f0dbafb166fa8e4f2daad36712b00c7'
MAINTAINED_SHA='b2d124efa871b347d048e60914530543dfc2533b36c9acd7a465d5e570323b02'
EXPECTED={'schema': 're921-openbios-continuation-proof-publication-v1', 'publication_review': 'PENDING_INDEPENDENT_EXACT_HASH_REVIEW', 'fresh_execution_scope': 'PUBLIC_METADATA_TESTS_ONLY', 'fresh_target': 0, 'fresh_native': 0, 'integration': False, 'production_patch': False, 'global_scope': 'FAIL', 'procedure_scope': 'FAIL', 'naturalcaller': 'BLOCKED', 'backend_boundary': 'OPENBIOS_REPLACEMENT_NOT_SONY_BIOS', 'authentication_scope': 'Fresh full inventories and nested firstFAIL authenticated; no numerical replay', 'authentication': {'re920-recovery01': {'manifest_schema': 're920.recovery.inventory.v1', 'seal_schema': 're920.recovery.seal.v1', 'entries': 76, 'manifest_sha256': '3560d82679ee9f0b7a6af003a6622f2540ad0a76e7eb02b82789f570c0305c0f', 'seal_file_sha256': 'e75abaf22a27198200251c9edd3f1b1ad156b32b27249828b91f64ed6c992f61', 'verdict_sha256': '95801b85eeba70366c91d3afc1398389dfd415d5c4abec023e225b3c4ab27f9d'}, 're920-review': {'manifest_schema': 're920.review.inventory.v1', 'seal_schema': 're920.review.seal.v1', 'entries': 3174, 'manifest_sha256': '3f609ed8dff3f217ff0f37f4ea8f14a5ff33714d823958742335ad15c5a69510', 'seal_file_sha256': '3a2d500c9ffcf1654b4568f4b17374a0351d58a38e735a363e76584a68e96548', 'verdict_sha256': '053adc87274f9e6cb7380abef53e92d51fa9d2e436cfb7b7ef0d2484adce3bbc'}, 're920-review/attempt01': {'manifest_schema': 're920.review.inventory.v1', 'seal_schema': 're920.review.seal.v1', 'entries': 1573, 'manifest_sha256': '72cd4ceb41065708cf146eb81c87f3353a9231e988371a3da04d31279c622e75', 'seal_file_sha256': '50ea7d4a68b2d2263b92bcb836e5361a33e50beac1b1bc799736724ac47dc915', 'verdict_sha256': 'e15bd6f3c5acd86a69774b1b705e1f805d32ce5d6a1f2c1f0a61c24cc0854d23'}}, 'attribution': {'project': 'PCSX-Redux / nugget OpenBIOS', 'license': 'MIT', 'copyright': ['Copyright (c) 2025 PCSX-Redux authors'], 'source_url': 'https://github.com/pcsx-redux/nugget/blob/7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30/openbios/kernel/alloc.c', 'nugget_commit': '7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30', 'redux_commit': 'c313b116e6a55786bc127c9b3a07a90b55d97c21', 'redistributed_source': False, 'sources_unchanged': True, 'reference_pins': {'src/core/psxmem.h': {'sha256': '9e5658aeeef2f01af73a80f892f5e345fadee35c83d2f220daeafb40409fe6a0', 'bytes': 14765}, 'src/core/psxhw.cc': {'sha256': 'db7fbff756774848150fa1acf0e7c04c3bd2c5a87e3b4aacffcacd88e21388de', 'bytes': 35035}, 'src/mips/openbios/kernel/handlers.c': {'sha256': 'a5c97ce2e554ef07ba40e3e69c31d9fc7da328e4edcd5cc02f92a8f69bccadd3', 'bytes': 15987}, 'src/mips/openbios/kernel/alloc.c': {'sha256': '88cb79e09ab9f7a7eff8f700d496ae4c473372ac2be9b0546c47a410c710061d', 'bytes': 12356}}}, 'RE920': {'accepted_scope': 'PRIVATE_COMPILED_OPENBIOS_STARTUP_A0_39_PREFIX', 'producer': {'positive_prefixes': 1, 'actual_machine_ablations': 1, 'positive_visits': 1976489, 'ablation_visits': 1976497, 'semantic_JSON_rejections': 6, 'semantic_test_methods': 7, 'source_files_verified': 1384, 'input_pins_verified': 22}, 'reviewer': {'positive_prefixes': 1, 'actual_machine_ablations': 1, 'independent_interpreter_prefixes': 1, 'positive_visits': 1976489, 'ablation_visits': 1976497, 'whole_ram_bytes_compared': 2097152, 'gpr_compared': 32, 'ordered_pc_compared': 1976489, 'fresh_full_rom_identity': False, 'rom_identity_except_GNU_build_ID': True, 'GNU_build_ID_bytes_excluded': 20, 'all_other_ROM_bytes_identical': True, 'envelope_identical': True, 'concerns': []}, 'execution_order': ['copyDataAndInitializeBSS', 'copyA0table', 'installKernelHandlers', 'exec', 'authentic SLUS entry', 'SW RA', 'user_initheap natural return'], 'frontier': 'I_MASK 16-bit write attempted nonretired', 'BIOS_SDK_return_doubles': False, 'injected_sectors': False, 'natural_reset': False, 'natural_full_boot': False, 'CD_proof': False, 'hardware_proof': False, 'gameplay_proof': False, 'Sony_RA': 'UNKNOWN', 'CPU_model': 'immediate loads branch delay slots coherent four RAM mirrors software only', 'initial_state': 'constructed ABI and RAM; reviewer reconstructed from ISO', 'B0_fallback_return_permitted': True}, 'historical': {'original_incomplete_members': 1608, 'original_no_final_seal': True, 'first_reviewer_ROM_identity_FAIL': True, 'initial_mirror_FAIL': True, 'BFD_format_FAIL': True, 'incorrect_negative_FAIL': True, 'RE893_partial_preserved': True, 'global_procedure_FAIL_retained': True}}
COMPATIBILITY_DELTAS={'scripts/reverse/re919_publication.py': {'before_sha256': 'bf2be06f055283ffbcd960950449e9f2d39ba1880c299954ccbf862d10b94305', 'replacements': [('\ndef preceding_maintained(data):return inverse(data,MAINTAINED_SHA)', "\ndef preceding_maintained(data):\n if b'<!-- RE921 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re921_publication.py'))['preceding_maintained'](data)\n return inverse(data,MAINTAINED_SHA)\ndef read_maintained():\n data=(ROOT/MAINTAINED).read_bytes()\n if b'<!-- RE921 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re921_publication.py'))['preceding_maintained'](data)\n return data"), ("\n  if (ROOT/p).read_bytes()!=b:raise ValueError('generated drift '+p)", "\n  if (read_maintained() if p==MAINTAINED else (ROOT/p).read_bytes())!=b:raise ValueError('generated drift '+p)")]}, 'tests/reverse/test_re919_publication.py': {'before_sha256': 'a74cdfab3235c076cfe80edd9dbca2dd4f7dd61ebd741049e7748828884efc28', 'replacements': [('for p,b in out.items():assert (ROOT/p).read_bytes()==b;m.guard_output(p,b)', 'for p,b in out.items():assert (m.read_maintained() if p==m.MAINTAINED else (ROOT/p).read_bytes())==b;m.guard_output(p,b)')]}}
SECTION='\n<!-- RE921 PUBLICATION BEGIN -->\n<section id="re921-publication-v1" data-integration="false"><h2>CURRENT RE921 — continuation OpenBIOS RE920 / publication metadata</h2><p>OPENBIOS_REPLACEMENT_NOT_SONY_BIOS, MIT complet compilé inchangé. Producteur/reviewer : un positif1976489visites et une ablationmachine1976497 ; six contrôlesJSON distincts, pas sept exécutions. Initialisation puis entrée authentique et user_initheap naturellement retourné, sans double SDK/BIOS ni secteur injecté. Oracle indépendant RAM entière2097152octets32GPR et orderedPC. ROM identique sauf20octetsGNUbuildID ; enveloppe identique.</p><p>Restant : frontière I_MASK écriture16bits tentée NONretirée. BLOCKED natural reset/CD/hardware/gameplay ; ABI/RAM construits, loads immédiats. Global FAIL/procedure FAIL/integration=false ; originalINCOMPLETE1608 et firstFAIL ROMidentity conservés. ZERO fresh target/native. PENDING_INDEPENDENT_EXACT_HASH_REVIEW.</p><p><a href="../stories/RE-921-openbios-continuation-proof-publication.md">Story / acceptance</a> · <a href="functions/re921-openbios-continuation-proof-publication.md">Evidence / blockers</a> · <a href="generated/re921-openbios-continuation-proof-publication-v1.json">Status</a></p></section>\n<!-- RE921 PUBLICATION END -->\n'
DOC='# RE921 — publication metadata de la continuation OpenBIOS RE920\n\n## Progression\n- [x] Inventaires complets producteur76 / reviewer3174 / firstFAIL1573 authentifiés.\n- [x] TDD RED avant générateur ; aucune nouvelle exécution cible/native.\n- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW ; worktree-only, aucun stage/commit/push.\n\n## Evidence\nPCSX-Redux / nugget OpenBIOS complet MIT inchangé compilé GCC MIPSel. Enveloppe ABI/RAM construite : copyDataAndInitializeBSS → copyA0table → installKernelHandlers → exec → entrée SLUS authentique → SW RA → user_initheap retourné naturellement. Pas de hook retour BIOS/SDK ni secteur injecté. Un positif1976489visites et une ablation machine1976497 pour chacun producteur/reviewer ; six rejets JSON et sept méthodes sémantiques, pas sept exécutions. B0 fallback peut revenir sans sémantique A0. Oracle CPU indépendant reconstruit depuis ISO : RAM entière2097152octets,32GPR,1976489visites orderedPC. ROM identique sauf20octets GNUbuildID, tous les autres octets identiques ; enveloppe identique. Visites pas instructions retirées. Aucun source tiers redistribué.\n\n## Blockers\nOPENBIOS_REPLACEMENT_NOT_SONY_BIOS ; Sony RA UNKNOWN. Frontière I_MASK écriture16bits tentée NONretirée. Aucun modèle MMIO ou secteur succès fabriqué. Natural reset/full boot/CD/hardware/gameplay/integration=false ; contexte ABI et RAM initial construit, modèle loads immédiats et branch delay slots, pas certification R3000. Global FAIL/procedure FAIL historiques maintenus. firstFAIL ROMidentity reviewer, mirror/BFD/negative producer et original INCOMPLETE1608 sans seal final préservés ; aucune réhabilitation. BLOCKED-001/002 suppressions utilisateur, report-tech, cache, assets/cold archives/seals/firstFAIL et RE893partial intacts.\n\n## Acceptance\n- [x] Schéma exact récursif types/valeurs/counts/pins, inconnus rejetés.\n- [x] Guards raw/secret/binary avec benign même chemin.\n- [x] Story/tracker/evidence/blockers et dashboards suffixe exact ; inverse reconstitue chaque prédécesseur sans modifier ses hashes.\n- [ ] Revue indépendante exacte des hashes PENDING_INDEPENDENT_EXACT_HASH_REVIEW ; tests publication ne valent pas intégration.\n\nAucune production modifiée, aucun job/successeur lancé. Suite complète non rejouée ; compatibilité collection explicitement inventoriée. Prochaine hypothèse RE922 interrupt/MMIO depuis références libres vers startup/CD, non exécutée ici.\n'
OUTPUT_PATHS=(STORY,REPORT,JSON_PATH,CSV_PATH,DASHBOARD,MAINTAINED)
PUBLIC_PATHS=OUTPUT_PATHS+(PRIOR_MAINTAINED,"scripts/reverse/re921_publication.py","tests/reverse/test_re921_publication.py")+tuple(COMPATIBILITY_DELTAS)
def metadata():return copy.deepcopy(EXPECTED)
def validate(data):
 def exact(a,b):
  if type(a) is not type(b):return False
  if isinstance(b,dict):return set(a)==set(b) and all(exact(a[k],b[k]) for k in b)
  if isinstance(b,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
  return a==b
 if not exact(data,EXPECTED):raise ValueError('exact RE921 recursive schema types/counts/hash/scope required')
 return data
def digest(b):return hashlib.sha256(b).hexdigest()
def inverse(data,sha):
 suffix=SECTION.encode()+b'</html>'
 if not data.endswith(suffix) or data.count(b'<!-- RE921 PUBLICATION BEGIN -->')!=1 or data.count(b'<!-- RE921 PUBLICATION END -->')!=1:raise ValueError('exact unique RE921 suffix required')
 before=data[:-len(suffix)]+b'</html>'
 if digest(before)!=sha:raise ValueError('exact predecessor bytes changed')
 return before
def preceding_dashboard(data):return inverse(data,PRIOR_SHA)
def preceding_maintained(data):return inverse(data,MAINTAINED_SHA)
def maintained_before():
 b=(ROOT/PRIOR_MAINTAINED).read_bytes()
 if digest(b)!=MAINTAINED_SHA:raise ValueError('maintained historical fixture drift')
 return b

RAW=re.compile(rb'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|raw_opcode|raw_pc|register_values|target_address|payload_offset|data:image|```(?:asm|mips|cpp|c)\b',re.I)
SECRET=re.compile(rb'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|(?:api[_-]?key|password|secret)\s*[:=]\s*[\"\x27][^\"\x27\s]{12,}',re.I)
def guard_added(path,payload):
 p=Path(path)
 if p.is_absolute() or '..' in p.parts or path not in PUBLIC_PATHS:raise ValueError('outside explicit RE921 public scope')
 if len(payload)>100000 or b'\0' in payload:raise ValueError('heavy/binary payload')
 payload.decode('utf-8')
 if SECRET.search(payload):raise ValueError('secret')
 if p.suffix!='.py' and RAW.search(payload):raise ValueError('raw evidence')
def guard_output(path,payload):
 if path not in OUTPUT_PATHS:raise ValueError('not generated metadata')
 if path in (DASHBOARD,MAINTAINED):
  (preceding_dashboard if path==DASHBOARD else preceding_maintained)(payload);guard_added(path,SECTION.encode())
 else:guard_added(path,payload)
def document(report=False):
 return DOC+"\n"+json.dumps(EXPECTED,indent=2,sort_keys=True)+"\n"
def render():
 d=validate(metadata());before=(ROOT/PRIOR_DASHBOARD).read_bytes()
 if digest(before)!=PRIOR_SHA or not before.endswith(b'</html>'):raise ValueError('exact RE917 predecessor required')
 out={STORY:document().encode(),REPORT:document(True).encode(),JSON_PATH:(json.dumps(d,indent=2,sort_keys=True)+'\n').encode(),DASHBOARD:before[:-7]+SECTION.encode()+b'</html>',MAINTAINED:maintained_before()[:-7]+SECTION.encode()+b'</html>'}
 stream=io.StringIO(newline='');w=csv.writer(stream,lineterminator='\n');w.writerow(['ticket','scope','status','integration','publication_review'])
 for ticket,status in [('RE920','PRIVATE_OPENBIOS_CONTINUATION_ACCEPTED'),('RE921','PUBLIC_METADATA_TESTS_ONLY')]:w.writerow([ticket,'archived proof' if ticket!='RE921' else 'fresh metadata',status,'false',d['publication_review']])
 out[CSV_PATH]=stream.getvalue().encode()
 for p,b in out.items():guard_output(p,b)
 return out
def original_compatibility(path,text):
 spec=COMPATIBILITY_DELTAS[path]
 for old,new in reversed(spec['replacements']):
  if text.count(new)!=1:raise ValueError('exact RE921 compatibility adapter required')
  text=text.replace(new,old)
 if digest(text.encode())!=spec['before_sha256']:raise ValueError('historical compatibility code changed')
 return text
def compatibility_pins():
 for p in COMPATIBILITY_DELTAS:original_compatibility(p,(ROOT/p).read_text())
def check():
 compatibility_pins()
 for p,b in render().items():
  if (ROOT/p).read_bytes()!=b:raise ValueError('generated drift '+p)
 for p in PUBLIC_PATHS:
  if p not in (DASHBOARD,MAINTAINED,PRIOR_MAINTAINED):guard_added(p,(ROOT/p).read_bytes())
 print('RE921 PUBLIC_METADATA_TESTS_ONLY PASS; exact-public-hash independent review PENDING')
if __name__=='__main__':
 argparse.ArgumentParser(description=__doc__).parse_args();check()
