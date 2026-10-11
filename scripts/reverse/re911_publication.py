"""RE911 metadata only portable publication; no private dependency."""
import argparse,copy,csv,hashlib,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PRIOR_DASHBOARD='docs/reverse/tomb5-progress-dashboard-re909-v1.html'
PRIOR_MAINTAINED='docs/reverse/tomb5-progress-dashboard-maintained-re909-v1.html'
DASHBOARD='docs/reverse/tomb5-progress-dashboard-re911-v1.html'
MAINTAINED='docs/reverse/tomb5-progress-dashboard.html'
STORY='docs/stories/RE-911-cd-upstream-diagnostic-publication.md'
REPORT='docs/reverse/functions/re911-cd-upstream-diagnostic-publication.md'
JSON_PATH='docs/reverse/generated/re911-cd-upstream-diagnostic-publication-v1.json'
CSV_PATH='docs/reverse/generated/re911-cd-upstream-diagnostic-tracker-v1.csv'
PRIOR_SHA='e51942bad9efed0f616fce521006e6dfcb5238c315fd4995b7b8965f3b6eb66c'
MAINTAINED_SHA='4c4528ecd04d627f2bc2cbd258623aa40c63383d0315a3e2f5bceab7b98b0df9'
EXPECTED={'schema': 're911-cd-upstream-diagnostic-publication-v1', 'publication_review': 'PENDING_INDEPENDENT_EXACT_HASH_REVIEW', 'fresh_execution_scope': 'PUBLIC_METADATA_TESTS_ONLY', 'fresh_target': 0, 'fresh_native': 0, 'integration': False, 'production_patch': False, 'global_scope': 'FAIL', 'procedure_scope': 'FAIL', 'naturalcaller': 'BLOCKED', 'authentication_scope': 'full two RE910 inventories size/hash verified; historical111 members reviewed by RE910 not freshly replayed', 'authentication': {'re910-cd-upstream': {'entries': 56, 'manifest_sha256': '7ef9f8ad67aeb5bf6beb57d4c717c14ed68e10ce4430121b50042c95fe4aac9a', 'seal_sha256': '8148b137634d74a4cf4aa30fcf2983934fdcdda2489003df07baba71ebaecb7c', 'verdict_sha256': 'de40cc48984f023b8c49db6f667e4eec70cfb87c02e9667ce9c9fedb8120f987', 'handoff_sha256': 'daa9ee5388b62eae1fbcffa9f3bc142d23f8d9373309b3c72613a6ed022550fb', 'verification_sha256': '9071f6997bac9392ac638301cabfe22dea23657e891230e1cb41c453e629ae20'}, 're910-review': {'entries': 52, 'manifest_sha256': 'da0ac0b393081ee892f8052e0332046c39418537aa6a3d869905b8f117d67e85', 'seal_sha256': '4d6172d155db2234fd41bd586a53423a61d70342b7c58138be5b8a256e253c72', 'verdict_sha256': '61434fd898e98df40a81d7d9168834f308c952bdbd02a72b501a5fe1bffb6e17', 'handoff_sha256': '232a7683cba809c2cb16c2ad7329d2a32b588b1ff41494d50a9dc0a09312b71d', 'verification_sha256': '99353a611c1cef27875d9c035feb5bb3cef0017daa8a91007e8ca09cedeefb4a'}}, 'RE910': {'diagnostic': 'PASS_ONLY', 'functional_passed': False, 'functional_GREEN': 0, 'entry': 'constructed earlier InitNewCDSystem entry on archival loader RAM, not natural startup', 'stop': 'BEFORE GPUSTAT VSync MMIO SDK', 'current_start_gwLba': 0, 'producer': {'target_setup_attempts': 2, 'first_setup_failures': 1, 'accepted_target_runs': 1, 'authenticated_target_visits': 124, 'stopping_instruction_visits_excluded': 1, 'producer_returns': 0, 'stdlib_interpreter_runs': 3, 'accepted_oracle_comparisons': 1, 'model_ablation_runs': 2, 'oracle_visits': 124, 'interpreted_stores': 45, 'whole_RAM_bytes': 4194304, 'GPR_compared': 32, 'sensitivity_controls_rejected': 5, 'required_archive_unique_members': 111, 'archive_member_checks_across_attempts': 222, 'CD_current_start_lba_stores': 0, 'CD_sector_deliveries': 0, 'CD_service_doubles': 0, 'DEL_CDFS_OpenFile_calls': 0, 'DEL_CDFS_Seek_calls': 0, 'DEL_CDFS_Read_calls': 0, 'AI_reads': 0, 'AI_allocations': 0, 'AI_relocations': 0, 'AI_installs': 0, 'registration_calls': 0, 'InitialiseItem_calls': 0, 'native_compilations': 0, 'native_executions': 0, 'functional_contract_FAIL': 1, 'functional_contract_GREEN': 0, 'diagnostic_contract_PASS': 1, 'runtime_game': 0}, 'reviewer': {'fresh_target_runs': 1, 'accepted_oracle_comparisons': 1, 'independent_interpreter_runs': 3, 'model_ablation_runs': 2, 'sensitivity_controls': 5, 'RAM_bytes': 4194304, 'GPR': 32, 'ordered_PC': 124, 'stop_visit_excluded': 1, 'ordered_stores': 45, 'ordered_accesses_including_stop': 54, 'CD_sector_deliveries': 0, 'CD_service_doubles': 0, 'producer_returns': 0, 'OpenFile_Seek_Read_calls': 0, 'AI_reads_installs_registration': 0, 'native_compilations_executions': 0, 'game_runtime': 0, 'fresh_functional_contract_FAIL': 1, 'functional_GREEN': 0, 'fresh_diagnostic_contract_PASS': 1, 'producer_manifest_entries': 56, 'unique_historical_members_reviewed': 111, 'producer_historical_member_checks_two_attempts': 222}, 'producer_transport_task_seconds': 544.58, 'producer_transport_outer_seconds': 544.65, 'producer_anchor_seconds': 533.003, 'review_transport_task_seconds': 289.4, 'review_transport_outer_seconds': 289.44, 'review_anchor_seconds': 279.72, 'first_setup_FAIL_preserved': True, 'accepted_retry': 'retry01', 'software_oracle_not_hardware': True, 'stores': 'interpreted not exhaustive transient hooks'}, 'successor': 'RE912 GPUSTAT video timing and SDK preconditions BEFORE natural CD search seek read; no fabricated returns or positive sectors'}
COMPATIBILITY_DELTAS={'scripts/reverse/re909_publication.py': {'before_sha256': '503f7c7eda275e50e47b67133c7bbe24ff6107b171decfee15804861a587846e', 'replacements': [('\ndef preceding_maintained(data):return inverse(data,MAINTAINED_SHA)', "\ndef preceding_maintained(data):\n if b'<!-- RE911 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re911_publication.py'))['preceding_maintained'](data)\n return inverse(data,MAINTAINED_SHA)\ndef read_maintained():\n data=(ROOT/MAINTAINED).read_bytes()\n if b'<!-- RE911 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re911_publication.py'))['preceding_maintained'](data)\n return data"), ("\n  if (ROOT/p).read_bytes()!=b:raise ValueError('generated drift '+p)", "\n  if (read_maintained() if p==MAINTAINED else (ROOT/p).read_bytes())!=b:raise ValueError('generated drift '+p)")]}, 'tests/reverse/test_re909_publication.py': {'before_sha256': '2253454fb2918d76950db4946eb35d10f4c0a8de8237c9e2d6576c6ddfb554c4', 'replacements': [('for p,b in out.items():assert (ROOT/p).read_bytes()==b;m.guard_output(p,b)', 'for p,b in out.items():assert (m.read_maintained() if p==m.MAINTAINED else (ROOT/p).read_bytes())==b;m.guard_output(p,b)')]}}
SECTION='\n<!-- RE911 PUBLICATION BEGIN -->\n<section id="re911-publication-v1" data-integration="false"><h2>CURRENT RE911 — RE910 diagnostic only</h2><p>InitNewCDSystem authentic conditional124 visits stops BEFORE GPUSTAT/VSync MMIO SDK. Producer1target3oracle2model controls; independent reviewer1fresh target3oracle5sensitivity checks,45interpreted stores54accesses fullRAM4194304/GPR32. current/start/gwLba0; no CD doubles, sector delivery, OpenFile/Seek/Read, AI, registration or InitialiseItem. Archival RAM/constructed entry NOT natural startup. Functional FAIL1/GREEN0 per executor, diagnostic PASS ONLY; firstsetupFAIL immutable/retry01 distinct.</p><p>Global FAIL / procedure FAIL / integration=false / naturalcaller BLOCKED. PENDING_INDEPENDENT_EXACT_HASH_REVIEW. Publication adds ZERO numerical replays. RE912 GPUSTAT/video timing/SDK preconditions BEFORE natural CD search seek read; no fabricated returns or positive sectors.</p><p><a href="../stories/RE-911-cd-upstream-diagnostic-publication.md">Story / acceptance</a> · <a href="functions/re911-cd-upstream-diagnostic-publication.md">Evidence / blockers</a> · <a href="generated/re911-cd-upstream-diagnostic-publication-v1.json">Metadata / status</a></p></section>\n<!-- RE911 PUBLICATION END -->\n'
DOC="# RE911 — publication sûre du diagnostic RE910\n\n## Progression\n- [x] RED puis GREEN publication metadata uniquement, sans replay numérique.\n- [x] Deux inventories RE910 authentifiés tailles/SHA et verdict strict indépendant diagnostic seul.\n- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW; worktree-only, aucun stage/commit/push.\n\n## Evidence\nInitNewCDSystem construit depuis RAM loader archivée, CPU/RAM conservés jusqu'arrêt AVANT GPUSTAT/VSync MMIO SDK. Producteur1target124visits/3oracle dont2contrôles modèle; reviewer1fresh124PC45stores54accesses/3oracle indépendant/5sensitivitychecks. FullRAM4194304/GPR32, stop exclu des124visites. Stores interprétés, pas instrumentation transitoire exhaustive. Oracle logiciel non hardware. Archive111unique/222checksproducer2attempts/111reviewchecks, zéro loader frais ici.\n\n## Blockers\nDiagnostic PASS ONLY, functional FAIL1/GREEN0 pour chaque exécuteur, global FAIL / procédure FAIL / integration=false / naturalcaller BLOCKED. current/start/gwLba0, aucun CDdouble/secteur livré/OpenFile/Seek/Read/AI/Registration/InitialiseItem, natif ou runtime. Entrée construite archival RAM ≠ natural startup. firstFAIL setup immuable/retry01 distinct, errors/checker historiques non effacés. Budget producer500 dépassé544.58task/544.65outer, ancre533.003distincte; reviewer289.40task/289.44outer ancre279.72distincte. BLOCKED-001/002 supprimés par utilisateur et report-tech conservés. Aucun source patch/intégration.\n\n## Acceptance\n- [x] Types récursifs exacts et chaque feuille discriminée; gardes raw/secret/binaires public-only.\n- [x] Dashboard versionné/maintenu suffixe unique inverse exact RE909; pins historiques inchangés.\n- [x] Tests ciblés et même collection compatibilitybaseline contexte authentique préservant userdeletes.\n- [ ] Revue indépendante des hashes publics exacts par parent requise; aucun claim publication acceptée indépendamment.\n\n## Next — RE912\nGPUSTAT/video timing et préconditions SDK (interruptions/callback/timer requis) authentifiés et discriminés AVANT natural CD search/seek/read. Retenir CPU/RAM; pas de faux retour SDK ni catalogue/secteur positif injecté. Ensuite seulement vrais producteurs gwHeader/gwLba et vrai caller OpenFile/Seek/Read, puis AI/RelocPtr22/registration284/InitialiseItem. Nouvelle unité NON exécutée ici.\n"
OUTPUT_PATHS=(STORY,REPORT,JSON_PATH,CSV_PATH,DASHBOARD,MAINTAINED)
PUBLIC_PATHS=OUTPUT_PATHS+(PRIOR_MAINTAINED,"scripts/reverse/re911_publication.py","tests/reverse/test_re911_publication.py")+tuple(COMPATIBILITY_DELTAS)
def metadata():return copy.deepcopy(EXPECTED)
def validate(data):
 def exact(a,b):
  if type(a) is not type(b):return False
  if isinstance(b,dict):return set(a)==set(b) and all(exact(a[k],b[k]) for k in b)
  if isinstance(b,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
  return a==b
 if not exact(data,EXPECTED):raise ValueError('exact RE911 recursive schema types/counts/hash/scope required')
 return data
def digest(b):return hashlib.sha256(b).hexdigest()
def inverse(data,sha):
 suffix=SECTION.encode()+b'</html>'
 if not data.endswith(suffix) or data.count(b'<!-- RE911 PUBLICATION BEGIN -->')!=1 or data.count(b'<!-- RE911 PUBLICATION END -->')!=1:raise ValueError('exact unique RE911 suffix required')
 before=data[:-len(suffix)]+b'</html>'
 if digest(before)!=sha:raise ValueError('exact predecessor bytes changed')
 return before
def preceding_dashboard(data):return inverse(data,PRIOR_SHA)
def preceding_maintained(data):
 if b'<!-- RE913 PUBLICATION' in data:
  import runpy
  data=runpy.run_path(str(ROOT/'scripts/reverse/re913_publication.py'))['preceding_maintained'](data)
 return inverse(data,MAINTAINED_SHA)
def read_maintained():
 data=(ROOT/MAINTAINED).read_bytes()
 if b'<!-- RE913 PUBLICATION' in data:
  import runpy
  data=runpy.run_path(str(ROOT/'scripts/reverse/re913_publication.py'))['preceding_maintained'](data)
 return data
def maintained_before():
 b=(ROOT/PRIOR_MAINTAINED).read_bytes()
 if digest(b)!=MAINTAINED_SHA:raise ValueError('maintained historical fixture drift')
 return b

RAW=re.compile(rb'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|raw_opcode|raw_pc|register_values|target_address|payload_offset|data:image|```(?:asm|mips|cpp|c)\b',re.I)
SECRET=re.compile(rb'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|(?:api[_-]?key|password|secret)\s*[:=]\s*[\"\x27][^\"\x27\s]{12,}',re.I)
def guard_added(path,payload):
 p=Path(path)
 if p.is_absolute() or '..' in p.parts or path not in PUBLIC_PATHS:raise ValueError('outside explicit RE911 public scope')
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
 if digest(before)!=PRIOR_SHA or not before.endswith(b'</html>'):raise ValueError('exact RE909 predecessor required')
 out={STORY:document().encode(),REPORT:document(True).encode(),JSON_PATH:(json.dumps(d,indent=2,sort_keys=True)+'\n').encode(),DASHBOARD:before[:-7]+SECTION.encode()+b'</html>',MAINTAINED:maintained_before()[:-7]+SECTION.encode()+b'</html>'}
 stream=io.StringIO(newline='');w=csv.writer(stream,lineterminator='\n');w.writerow(['ticket','scope','status','integration','publication_review'])
 for ticket,status in [('RE910','DIAGNOSTIC_PASS_FUNCTIONAL_BLOCKED_SDK'),('RE911','PUBLIC_METADATA_TESTS_ONLY')]:w.writerow([ticket,'archived proof' if ticket!='RE911' else 'fresh metadata',status,'false',d['publication_review']])
 out[CSV_PATH]=stream.getvalue().encode()
 for p,b in out.items():guard_output(p,b)
 return out
def original_compatibility(path,text):
 spec=COMPATIBILITY_DELTAS[path]
 for old,new in reversed(spec['replacements']):
  if text.count(new)!=1:raise ValueError('exact RE911 compatibility adapter required')
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
 print('RE911 PUBLIC_METADATA_TESTS_ONLY PASS; exact-public-hash independent review PENDING')
if __name__=='__main__':
 argparse.ArgumentParser(description=__doc__).parse_args();check()
