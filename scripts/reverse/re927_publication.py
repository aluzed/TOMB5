"""RE927 portable metadata publication; no private runtime dependency."""
import argparse,copy,csv,hashlib,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PRIOR_DASHBOARD='docs/reverse/tomb5-progress-dashboard-re925-v1.html'
PRIOR_MAINTAINED='docs/reverse/tomb5-progress-dashboard-maintained-re925-v1.html'
DASHBOARD='docs/reverse/tomb5-progress-dashboard-re927-v1.html'
MAINTAINED='docs/reverse/tomb5-progress-dashboard.html'
STORY='docs/stories/RE-927-timer-proof-publication.md'
REPORT='docs/reverse/functions/re927-timer-proof-publication.md'
JSON_PATH='docs/reverse/generated/re927-timer-proof-publication-v1.json'
CSV_PATH='docs/reverse/generated/re927-timer-proof-tracker-v1.csv'
PRIOR_SHA='8e87dcfd4a2ab49ad68c4e8893926dd7d3beabce4488ae77ac950927064ac25c'
MAINTAINED_SHA='5d98ad527c74bb8679388ad1cc3ef4bbdf49bcd3dca15b422001137ccb1ccf18'
EXPECTED={'schema': 're927-timer-proof-publication-v1', 'publication_review': 'PENDING_INDEPENDENT_REVIEW', 'fresh_execution_scope': 'PUBLIC_METADATA_TESTS_ONLY', 'fresh_target': 0, 'fresh_native': 0, 'integration': False, 'production_patch': False, 'global_scope': 'FAIL', 'procedure_scope': 'FAIL', 'naturalcaller': 'BLOCKED', 'backend_boundary': 'RE926-PCSX-Redux-Timer1-local-free-running-subset', 'authentication': {'re926-timer-mmio': {'members': 153, 'manifest_sha256': '3f402188e536c1fe84ffbbf250cff8828582d99bd2e1dffe93cb88062461c2bb', 'seal_sha256': 'c37da1cbef04370433b31e4d0f8d09868e72ae131ad3432f796ef72cfe6380f7', 'exactset_all_sizes_hashes': True}, 're926-review': {'members': 107, 'manifest_sha256': '82f5f39fbf0b8beaaccb5a6ed4ca26061c55c9b4d0f3a41b08ae10263a344638', 'seal_sha256': '566c999431f06d93c51ac1382abbba9b3efa21da06ae8c76c20e5de207cc7286', 'exactset_all_sizes_hashes': True}, 're925-parent-delivery': {'members': 4, 'manifest_sha256': 'a9bddde81c12329d6dc45a1fa94df2d97c1c4215d70342bf6a4acc4c8070d67d', 'seal_sha256': '955dc9fb38343b600162b1e9b33d6364c3a29cac9edaaa0484425cc538ff1f6e', 'exactset_all_sizes_hashes': True}, 're926-parent-checkpoint': {'members': 4, 'manifest_sha256': 'e4eeb24e785949963731cc130d9d76f27a5cec298438225dde523c71684f67a6', 'seal_sha256': 'c362a853b91019f740686afae263ab53fbcca3d5dfda8e4cbc9a84fe5c4f470d', 'exactset_all_sizes_hashes': True}}, 'attribution': {'project': 'PCSX-Redux / nugget OpenBIOS', 'license': 'GPL-2.0-or-later', 'OpenBIOS_license': 'MIT', 'pcsx_commit': 'c313b116e6a55786bc127c9b3a07a90b55d97c21', 'openbios_commit': '7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30', 'sources': [{'path': 'src/core/psxcounters.cc', 'url': 'https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/psxcounters.cc', 'sha256': 'b4406898c327a8bd1f289dff2c42f85c630ab80dddc5cf489c2ace11fad45831', 'copyright': ['Copyright (C) 2010 by Blade_Arma'], 'license': 'GPL-2.0-or-later'}, {'path': 'src/core/psxcounters.h', 'url': 'https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/psxcounters.h', 'sha256': '85ef25a1a7f92f69f55030e97b0169eab9f1f8b1478d5d351136e920bac12484', 'copyright': ['Copyright (C) 2010 by Blade_Arma'], 'license': 'GPL-2.0-or-later'}, {'path': 'src/core/psxhw.cc', 'url': 'https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/psxhw.cc', 'sha256': 'db7fbff756774848150fa1acf0e7c04c3bd2c5a87e3b4aacffcacd88e21388de', 'copyright': ['Copyright (C) 2023 PCSX-Redux authors'], 'license': 'GPL-2.0-or-later'}, {'path': 'src/core/psxemulator.h', 'url': 'https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/psxemulator.h', 'sha256': 'da2a56af7f0ae6d93e38b213e65be4606527b629013b6df02cdd991691e17a0b', 'copyright': ['Copyright (C) 2022 PCSX-Redux authors'], 'license': 'GPL-2.0-or-later'}, {'path': 'src/core/psxinterpreter.cc', 'url': 'https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/psxinterpreter.cc', 'sha256': '0c9eca067b3ed23c0ea9fd84d9a3752af3c92f2281ebc05316fa1f385392f2e5', 'copyright': ['Copyright (C) 2023 PCSX-Redux authors'], 'license': 'GPL-2.0-or-later'}], 'third_party_source_redistributed': False}, 'archived_counts': {'completed': 1981087, 'visits': 1981088, 'resume_completed': 318, 'resume_visits': 319, 'whole_ram_bytes': 2097152, 'gpr': 32, 'producer_methods': 6, 'producer_source_comparisons': 28, 'producer_sensitive_mutants': 5, 'reviewer_source_comparisons': 28, 'reviewer_additional_source_comparisons': 512, 'reviewer_atomic_controls': 6, 'reviewer_methods': 6, 'reviewer_fresh_target_attempts': 6, 'reviewer_accepted_final_target_runs': 3, 'reviewer_accepted_final_CPU_runs': 2}, 'review_history': {'accepted_scope': 'finite corrected Timer1 source slice and authentic executable prefix only; NOT certification of stale archived ablation clock', 'strict_passed': True, 'strict_logic_errors': [], 'strict_concerns': [], 'stale_ablation': 'REJECTED_NON_CERTIFIED', 'archived_clock': 7912652, 'corrected_fresh_clock': 7921560, 'global_concerns': ['archived backend-noirq timer_final.clock stale 7912652 versus corrected fresh 7921560; original mismatch preserved', 'producer predecessor full authentication performed after first attempts', 'historical firstFAILs and incomplete discovery ledger retained'], 'firstFAIL': 'all historical errors and rejected attempts retained'}, 'limitations': ['constructed NTSC/settings/initial counter and ABI', 'ROM reused, not rebuilt', 'immediate loads, not hardware R3000 load delay', 'no full scheduler, CPU exceptions or hardware oracle', 'Sony/reset/GPUSTAT/CD/hardware/gameplay not proved', 'Timer IRQ/gates/deadlines/DMA transfers unsupported'], 'natural_mode_writes': 1, 'natural_counter_reads': 0, 'rom_fresh_build': False, 'frontier': 'BEFORE_SYSCALL_OpenBIOS_EnterCriticalSection', 'clock_model': 'BIAS2 per instruction plus20 BIOS next-PC region; constructed NTSC settings and local Timer1 epoch; not full scheduler', 'next_ticket': 'RE928', 'retirement': 'previous instruction completed at following hook, not hardware retirement'}
COMPATIBILITY_DELTAS={'scripts/reverse/re925_publication.py': {'before_sha256': 'bbe567db1d078cf82c03758e7f3f64d229100d73bbc76297705045bb2d11353c', 'replacements': [('\ndef preceding_maintained(data):return inverse(data,MAINTAINED_SHA)', "\ndef preceding_maintained(data):\n if b'<!-- RE927 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re927_publication.py'))['preceding_maintained'](data)\n return inverse(data,MAINTAINED_SHA)\ndef read_maintained():\n data=(ROOT/MAINTAINED).read_bytes()\n if b'<!-- RE927 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re927_publication.py'))['preceding_maintained'](data)\n return data"), ("\n  if (ROOT/p).read_bytes()!=b:raise ValueError('generated drift '+p)", "\n  if (read_maintained() if p==MAINTAINED else (ROOT/p).read_bytes())!=b:raise ValueError('generated drift '+p)")]}, 'tests/reverse/test_re925_publication.py': {'before_sha256': '2363989c01215b67fc485db5b885373d31dd947c057c16519416f789f2c39ae7', 'replacements': [('for p,b in out.items():assert (ROOT/p).read_bytes()==b;m.guard_output(p,b)', 'for p,b in out.items():assert (m.read_maintained() if p==m.MAINTAINED else (ROOT/p).read_bytes())==b;m.guard_output(p,b)')]}}
SECTION='\n<!-- RE927 PUBLICATION BEGIN -->\n<section id="re927-publication-v1" data-integration="false"><h2>CURRENT RE927 — Timer1 RE926 corrigé metadata</h2><p>Un MODE write naturel, ZERO counter read naturel. Fresh1981087 completed/1981088 visits ; reprise318/319 ; arrêt AVANT SYSCALL EnterCriticalSection. Ablation7912652 REJECTED NON CERTIFIÉE, corrected fresh7921560 distincte. ROM MIT réutilisée, modèle GPL-2.0-or-later, BIAS2/+20/NTSC construits. BLOCKED Sony/reset/GPUSTAT/CD/hardware/gameplay/integration. Global FAIL/procedure FAIL ; PENDING_INDEPENDENT_REVIEW.</p><p><a href="../stories/RE-927-timer-proof-publication.md">Story / acceptance</a> · <a href="functions/re927-timer-proof-publication.md">Evidence / blockers</a> · <a href="generated/re927-timer-proof-publication-v1.json">Status</a></p></section>\n<!-- RE927 PUBLICATION END -->\n'
DOC='# RE927 — publication metadata Timer1 RE926 corrigé\n\n## Progression\n- [x] Inventaires privés exacts153/107/4 et checkpoint4 authentifiés, schemas/seals/tailles/SHA et verdict strict lus avant tests.\n- [x] TDD RED puis GREEN canonical/public-only ; ZERO replay numérique.\n- [ ] PENDING_INDEPENDENT_REVIEW ; worktree-only, aucun stage/commit/push.\n\n## Evidence\nRE926-PCSX-Redux-Timer1-local-free-running-subset franchit un MODE write naturel, ZERO counter read naturel. Fresh1981087 instructions complétées/1981088visites, restored318/319 ; stop AVANT SYSCALL OpenBIOS EnterCriticalSection non complété. RAM entière2097152octets,32GPR, orderedPC/MMIO/serviceentries/returns comparés avec CPU indépendant reviewer. Producteur6méthodes/28comparaisons/5mutants sensibles ; reviewer28+512comparaisons/6atomiccontrols/6méthodes ; six target attempts dont trois accepted final, deux accepted final CPU runs. Publication ZERO target/native replay. ROM OpenBIOS MIT héritée authentifiée non recompilée ; sources PCSX-Redux GPL-2.0-or-later authentifiées par headers/blobs pinés. Witness extrait/adapté pas émulateur complet. Aucune source tierce redistribuée.\n\n## Reviewhistory\nStrict private PASS porte seulement sur finite corrected source/prefix ; ablation archivée clock7912652 REJECTED NON CERTIFIÉE conservée, corrected fresh7921560 distincte. firstFAIL/retries, découverte incomplète et auth prédécesseur tardive conservés ; global/procedure FAIL non rétrocertifiés. Cardinalité parent4, ancienne prose5 corrigée sans changer archives.\n\n## Blockers\nBIAS2/+20/NTSC et initialTimer/ABI/RAM construits, epoch locale, loads immédiats pas load-delay/cache ; pas fullscheduler, IRQ/gates/deadlines/DMA/exceptionCPU prouvés. Sony/reset/GPUSTAT/CD/hardware/gameplay non prouvés, integration=false, production_patch=false. BLOCKED-001/002 restent supprimés ; report/cache/assets/coldarchives/seals/firstFAIL/RE893partial préservés.\n\n## Acceptance\nSchema récursif types exacts, leaf mutants, guards raw/secret/binary/paths ; dashboard HTML versionné et maintained suffix exact inverse RE925 ; deux adapters reconstruisent HEAD sans affaiblir historique. Compatibility baseline/current/export mêmes deux FAIL RE830, pas full-suite PASS. Public-only sans build/private dependency. Revue indépendante exact-hash PENDING_INDEPENDENT_REVIEW.\n\n## Handoff\nProchaine RE928 modèle CPU exception/SYSCALL cohérent sans retour double ; aucun nouveau job/successeur ni patch production autorisé par cette publication.\n'
OUTPUT_PATHS=(STORY,REPORT,JSON_PATH,CSV_PATH,DASHBOARD,MAINTAINED)
PUBLIC_PATHS=OUTPUT_PATHS+(PRIOR_MAINTAINED,"scripts/reverse/re927_publication.py","tests/reverse/test_re927_publication.py")+tuple(COMPATIBILITY_DELTAS)
def metadata():return copy.deepcopy(EXPECTED)
def validate(data):
 def exact(a,b):
  if type(a) is not type(b):return False
  if isinstance(b,dict):return set(a)==set(b) and all(exact(a[k],b[k]) for k in b)
  if isinstance(b,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
  return a==b
 if not exact(data,EXPECTED):raise ValueError('exact RE927 recursive schema types/counts/hash/scope required')
 return data
def digest(b):return hashlib.sha256(b).hexdigest()
def inverse(data,sha):
 suffix=SECTION.encode()+b'</html>'
 if not data.endswith(suffix) or data.count(b'<!-- RE927 PUBLICATION BEGIN -->')!=1 or data.count(b'<!-- RE927 PUBLICATION END -->')!=1:raise ValueError('exact unique RE927 suffix required')
 before=data[:-len(suffix)]+b'</html>'
 if digest(before)!=sha:raise ValueError('exact predecessor bytes changed')
 return before
def preceding_dashboard(data):return inverse(data,PRIOR_SHA)
def preceding_maintained(data):
 if b'<!-- RE929 PUBLICATION' in data:
  import runpy
  data=runpy.run_path(str(ROOT/'scripts/reverse/re929_publication.py'))['preceding_maintained'](data)
 return inverse(data,MAINTAINED_SHA)
def read_maintained():
 data=(ROOT/MAINTAINED).read_bytes()
 if b'<!-- RE929 PUBLICATION' in data:
  import runpy
  data=runpy.run_path(str(ROOT/'scripts/reverse/re929_publication.py'))['preceding_maintained'](data)
 return data
def maintained_before():
 b=(ROOT/PRIOR_MAINTAINED).read_bytes()
 if digest(b)!=MAINTAINED_SHA:raise ValueError('maintained historical fixture drift')
 return b

RAW=re.compile(rb'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|raw_opcode|raw_pc|register_values|target_address|payload_offset|data:image|```(?:asm|mips|cpp|c)\b',re.I)
SECRET=re.compile(rb'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|(?:api[_-]?key|password|secret)\s*[:=]\s*[\"\x27][^\"\x27\s]{12,}',re.I)
def guard_added(path,payload):
 p=Path(path)
 if p.is_absolute() or '..' in p.parts or path not in PUBLIC_PATHS:raise ValueError('outside explicit RE927 public scope')
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
 for ticket,status in [('RE926','PRIVATE_TIMER_CORRECTED_FINITE_ACCEPTED'),('RE927','PUBLIC_METADATA_TESTS_ONLY')]:w.writerow([ticket,'archived proof' if ticket!='RE927' else 'fresh metadata',status,'false',d['publication_review']])
 out[CSV_PATH]=stream.getvalue().encode()
 for p,b in out.items():guard_output(p,b)
 return out
def original_compatibility(path,text):
 spec=COMPATIBILITY_DELTAS[path]
 for old,new in reversed(spec['replacements']):
  if text.count(new)!=1:raise ValueError('exact RE927 compatibility adapter required')
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
 print('RE927 PUBLIC_METADATA_TESTS_ONLY PASS; exact-public-hash independent review PENDING')
if __name__=='__main__':
 argparse.ArgumentParser(description=__doc__).parse_args();check()
