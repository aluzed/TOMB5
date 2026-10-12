"""RE929 portable metadata publication; no private runtime dependency."""
import argparse,copy,csv,hashlib,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PRIOR_DASHBOARD='docs/reverse/tomb5-progress-dashboard-re927-v1.html'
PRIOR_MAINTAINED='docs/reverse/tomb5-progress-dashboard-maintained-re927-v1.html'
DASHBOARD='docs/reverse/tomb5-progress-dashboard-re929-v1.html'
MAINTAINED='docs/reverse/tomb5-progress-dashboard.html'
STORY='docs/stories/RE-929-cpu-exception-proof-publication.md'
REPORT='docs/reverse/functions/re929-cpu-exception-proof-publication.md'
JSON_PATH='docs/reverse/generated/re929-cpu-exception-proof-publication-v1.json'
CSV_PATH='docs/reverse/generated/re929-cpu-exception-proof-tracker-v1.csv'
PRIOR_SHA='108128135889eff7f44f0670c9ffd131863c0d24ac65d2fc16f03e2a70d6e4de'
MAINTAINED_SHA='c843903d95bdbb8f675e83eb3a950341739f18c4f2dd0f38c771651a8ee97fb2'
EXPECTED={'schema': 're929-cpu-exception-proof-publication-v1', 'publication_review': 'PENDING_INDEPENDENT_REVIEW', 'fresh_execution_scope': 'PUBLIC_METADATA_TESTS_ONLY', 'fresh_target': 0, 'fresh_native': 0, 'integration': False, 'production_patch': False, 'global_scope': 'FAIL', 'procedure_scope': 'FAIL', 'naturalcaller': 'BLOCKED', 'backend_boundary': 'RE928-PCSX-Redux-CPU-exception-subset', 'authentication': {'re928-cpu-exception': {'members': 131, 'manifest_sha256': '3c7015a8ca058a435dcdbb31fd3562b1906a8876b567339d1917daebdc228e86', 'seal_sha256': 'ad90a3adbcd9df24ad2613c87954d0bf13795586b0344a3a9ba6edbf41c3967b', 'exactset_all_sizes_hashes': True}, 're926-timer-mmio': {'members': 153, 'manifest_sha256': '3f402188e536c1fe84ffbbf250cff8828582d99bd2e1dffe93cb88062461c2bb', 'seal_sha256': 'c37da1cbef04370433b31e4d0f8d09868e72ae131ad3432f796ef72cfe6380f7', 'exactset_all_sizes_hashes': True}, 're924-dma-mmio': {'members': 85, 'manifest_sha256': 'c425623ea296d3700c125d8cbe0adc104f7694ae13f04c0ed6c9f1417fcc464a', 'seal_sha256': 'fab8b8b58f8312cc1578701ab1803a79610a1398846b083b822896e74f516a56', 'exactset_all_sizes_hashes': True}, 're922-interrupt-mmio': {'members': 112, 'manifest_sha256': '3a7465def56d0074975152e05edd4d7807a23a84c0775d2503046156d72cc1c1', 'seal_sha256': '5d2b37d4687bf165ebeed2ee2c6605f059a05a8a9727ab9045193d13447707cf', 'exactset_all_sizes_hashes': True}, 're920-recovery01': {'members': 76, 'manifest_sha256': '3560d82679ee9f0b7a6af003a6622f2540ad0a76e7eb02b82789f570c0305c0f', 'seal_sha256': 'e75abaf22a27198200251c9edd3f1b1ad156b32b27249828b91f64ed6c992f61', 'exactset_all_sizes_hashes': True}, 're918-openbios': {'members': 92, 'manifest_sha256': '093dc01dadd97038aef080264f77aac05e1607d2ca3bbb07330a4f78e912142a', 'seal_sha256': 'a47cb98851a0e28b9da66f8a097158f82bd26fed03ddb936856985e0e38ba591', 'exactset_all_sizes_hashes': True}, 're924-review': {'members': 70, 'manifest_sha256': '555c64baa95f28115235e5b5a9b73a0a65e8998531b39b00f45293f28769d823', 'seal_sha256': 'a99abe186b996e5cad9acd8e09c96b4b878f985aecdc9e2800c8c61ffd79bd77', 'exactset_all_sizes_hashes': True}, 're924-review-scope-clarification01': {'members': 7, 'manifest_sha256': '8ef0f29125e4306d196d1e664576df7610b1f85c04a9afa3de8851dfcabb4e11', 'seal_sha256': '39e44a8df73d8d757f1a9ffc3dfdff2ef6cbe4cc12a256606b450973b4e28b45', 'exactset_all_sizes_hashes': True}, 're926-review': {'members': 107, 'manifest_sha256': '82f5f39fbf0b8beaaccb5a6ed4ca26061c55c9b4d0f3a41b08ae10263a344638', 'seal_sha256': '566c999431f06d93c51ac1382abbba9b3efa21da06ae8c76c20e5de207cc7286', 'exactset_all_sizes_hashes': True}, 're928-review-closure01': {'members': 73, 'manifest_sha256': 'cc08412bff27e459273629e3d977df52a67db150e2db849d6a58253fc734004c', 'seal_sha256': 'cd7cdc19036866f4398c453b74b3d2cb7736cf71c0ce75ccd2eb59e91f454e9a', 'exactset_all_sizes_hashes': True}, 're928-review-closure03': {'members': 82, 'manifest_sha256': '217a9ad86857927a31520923fe30088b396f297da94ca7df9858d53b480e8dea', 'seal_sha256': 'c94198919ab3348494ba57142157a229e00800c8bbe68e01e791370b6be781cf', 'exactset_all_sizes_hashes': True}, 're927-parent-delivery': {'members': 5, 'manifest_sha256': '89ad4758378bee74b7d6983ce562e8a22e3edd39af2d7c517b8be703d1b17c10', 'seal_sha256': '951817953f629796f17a7835ec41323b6e11baf6acaffd35f1c836c8de18cb87', 'exactset_all_sizes_hashes': True}, 're928-parent-checkpoint': {'members': 6, 'manifest_sha256': '5283e2de479b15ba285750bdad71c9b3af2d20e0ed7d2222d938b7ffd3beca5b', 'seal_sha256': '8fa6281f7da7b2650fb1f55d8822f8ac0e154fd8fbfae99d4ec4f3d731d7a006', 'exactset_all_sizes_hashes': True}}, 'attribution': {'project': 'PCSX-Redux / nugget OpenBIOS', 'license': 'GPL-2.0-or-later', 'OpenBIOS_license': 'MIT', 'pcsx_commit': 'c313b116e6a55786bc127c9b3a07a90b55d97c21', 'openbios_commit': '7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30', 'sources': [{'path': 'src/core/r3000a.cc', 'url': 'https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/r3000a.cc', 'sha256': '77a2068343e98fc10728007f2943db164aa39b3a00d083434c31cdcb0046083c', 'copyright': ['Copyright (C) 2023 PCSX-Redux authors', 'g_system->printf(_("Copyright (C) 2019-%i PCSX-Redux authors\\n"), 2025);'], 'license': 'GPL-2.0-or-later'}, {'path': 'src/core/psxinterpreter.cc', 'url': 'https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/psxinterpreter.cc', 'sha256': '0c9eca067b3ed23c0ea9fd84d9a3752af3c92f2281ebc05316fa1f385392f2e5', 'copyright': ['Copyright (C) 2023 PCSX-Redux authors'], 'license': 'GPL-2.0-or-later'}], 'third_party_source_redistributed': False}, 'archived_counts': {'completed': 1981129, 'visits': 1981130, 'resume_completed': 42, 'resume_visits': 43, 'whole_ram_bytes': 2097152, 'gpr': 32, 'exception_cases': 128, 'rfe_cases': 8, 'witness_comparisons': 136, 'mutants': 6, 'mutant_comparisons_each': 136, 'closure_target_checks': 32, 'closure_atomic_rejects': 5, 'transitive_roots': 9, 'transitive_members': 833, 'reviewer_attempts': {'restored': 3, 'fresh': 3, 'failed_fresh': 1, 'accepted_fresh': 2}}, 'review_history': {'strict_passed': True, 'strict_logic_errors': [], 'strict_concerns': [], 'closure01': 'SEALED_FAIL_PRESERVED', 'original_review': 'UNSEALED_PRESERVED', 'closure02': 'UNSEALED_PRESERVED', 'closure03': 'STRICT_FINITE_PASS', 'self_report_264': 'REJECTED', 'firstFAIL': 'all historical errors and rejected attempts retained'}, 'limitations': ['Immediate-load software CPU semantics, not hardware oracle', 'RFE/BD/BREAK constructed only; no natural kernel return', 'Reused OpenBIOS ROM, no fresh firmware compilation', 'Device branches not traversed are not approved', 'Global/procedure FAIL unchanged: historical bootstrap/TDD/accounting limitations', 'Sony/reset/CD/GPU/hardware/gameplay not proved', 'BEV inherited ROM vector then flushCache; stop before BIU store; no natural RAM handler or RFE return'], 'natural_RFE': 0, 'kernel_RAM_handler_reached': False, 'BEV_inherited': True, 'new_service_returns': 0, 'rom_fresh_build': False, 'frontier': 'BEFORE_BIU_STORE', 'next_ticket': 'RE930', 'next_scope': 'real CPU/kernel/thread initialization before Exec; no BEV clear or injected thread'}
COMPATIBILITY_DELTAS={'scripts/reverse/re927_publication.py': {'before_sha256': '62b69c11032e3b73ad6e3a43eeaddd07c89dac6b307e6834e9c53db8eb3966ab', 'replacements': [('\ndef preceding_maintained(data):return inverse(data,MAINTAINED_SHA)', "\ndef preceding_maintained(data):\n if b'<!-- RE929 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re929_publication.py'))['preceding_maintained'](data)\n return inverse(data,MAINTAINED_SHA)\ndef read_maintained():\n data=(ROOT/MAINTAINED).read_bytes()\n if b'<!-- RE929 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re929_publication.py'))['preceding_maintained'](data)\n return data"), ("\n  if (ROOT/p).read_bytes()!=b:raise ValueError('generated drift '+p)", "\n  if (read_maintained() if p==MAINTAINED else (ROOT/p).read_bytes())!=b:raise ValueError('generated drift '+p)")]}, 'tests/reverse/test_re927_publication.py': {'before_sha256': 'ec7e09b104eef7aee1772d2cb51374b23916e394b35e060dc00d0506640d83a9', 'replacements': [('for p,b in out.items():assert (ROOT/p).read_bytes()==b;m.guard_output(p,b)', 'for p,b in out.items():assert (m.read_maintained() if p==m.MAINTAINED else (ROOT/p).read_bytes())==b;m.guard_output(p,b)')]}}
SECTION='\n<!-- RE929 PUBLICATION BEGIN -->\n<section id="re929-publication-v1" data-integration="false"><h2>CURRENT RE929 — CPU exception RE928 metadata</h2><p>SYSCALL +42completed/43visits ; fresh1981129/1981130. BEV hérité, ROM vecteur, flushCache : arrêt AVANT BIU store. 136=128exceptions+8RFE ; six mutants136 ; self-report264 REJECTED. closure03strictPASS82 ; closure01FAIL73, original/closure02UNSEALED préservés. BLOCKED handlerRAM/RFEretour/Sony/reset/CD/GPU/hardware/gameplay/integration. Global FAIL/procedure FAIL ; PENDING_INDEPENDENT_REVIEW.</p><p><a href="../stories/RE-929-cpu-exception-proof-publication.md">Story / acceptance</a> · <a href="functions/re929-cpu-exception-proof-publication.md">Evidence / blockers</a> · <a href="generated/re929-cpu-exception-proof-publication-v1.json">Status</a></p></section>\n<!-- RE929 PUBLICATION END -->\n'
DOC='# RE929 — publication metadata CPU exception RE928\n\n## Progression\n- [x] Inventaires exacts, tailles/SHA/seals authentifiés ; closure03 strict PASS82 membres.\n- [x] Source et données witness : 128exceptions + 8RFE = 136 ; six mutants chacun136. TDD RED/GREEN canonical/public-only, ZERO replay numérique.\n- [ ] PENDING_INDEPENDENT_REVIEW ; worktree-only aucun stage/commit/push.\n\n## Evidence\nSYSCALL franchi +42completed/43visits restored ; fresh1981129completed/1981130visits. BEV hérité -> ROM vecteur -> flushCache, arrêt AVANT BIU store non complété. RAM entière2MiB,32GPR,CP0,orderedPC,MMIO/clocks comparés indépendamment. Zéro nouveau service retourné, handlerRAM et RFE retour naturel NON obtenus. Witness extrait/adapté PCSX-Redux GPL-2.0-or-later ; ROM OpenBIOS MIT réutilisée, non recompilée, backend nonSony. Copyrights depuis headers authentifiés ; aucun source tierce redistribuée.\n\n## Reviewhistory\nclosure03 strict PASS fini archivé, neuf racines833membres ; closure-time32targetchecks/5atomicrejections, ZERO nouveau CPU/build/witness. Self-report264 REJECTED, code/données136. closure01 SEALED FAIL73 immutable ; originalreview UNSEALED et closure02 UNSEALED conservées. firstFAIL, historique TDD/authoringgap et global/procedure FAIL maintenus non rétrocertifiés.\n\n## Blockers\nLoads immédiats/software oracle, pas hardware. RFE/BD/BREAK construits seulement ; pas naturel handlerRAM/retour kernel. Sony/reset/CD/GPU/hardware/gameplay non prouvés, integration=false production_patch=false. BLOCKED-001/002 suppressions utilisateur, report/cache/assets/coldarchives/seals/firstFAIL/RE893partial préservés.\n\n## Acceptance\nSchema récursif types exacts et leaf mutants ; guards metadata/raw/secret/binary/paths ; dashboard versionné et maintained suffix inverse RE927 exact. Adapters immédiats inversibles exact HEAD, sans changer pins historiques. Compatibility baseline/current/export mêmes deux FAIL historiques RE830, pas full-suite PASS. Public-only sans preuve privée. PENDING_INDEPENDENT_REVIEW exact-public-hash.\n\n## Handoff\nNext RE930 BIU/cache et vraie initialisationCPU/kernel/thread avant Exec, sans BEV effacé ni thread injecté. Aucun nouveau job/successeur ni changement production.\n'
OUTPUT_PATHS=(STORY,REPORT,JSON_PATH,CSV_PATH,DASHBOARD,MAINTAINED)
PUBLIC_PATHS=OUTPUT_PATHS+(PRIOR_MAINTAINED,"scripts/reverse/re929_publication.py","tests/reverse/test_re929_publication.py")+tuple(COMPATIBILITY_DELTAS)
def metadata():return copy.deepcopy(EXPECTED)
def validate(data):
 def exact(a,b):
  if type(a) is not type(b):return False
  if isinstance(b,dict):return set(a)==set(b) and all(exact(a[k],b[k]) for k in b)
  if isinstance(b,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
  return a==b
 if not exact(data,EXPECTED):raise ValueError('exact RE929 recursive schema types/counts/hash/scope required')
 return data
def digest(b):return hashlib.sha256(b).hexdigest()
def inverse(data,sha):
 suffix=SECTION.encode()+b'</html>'
 if not data.endswith(suffix) or data.count(b'<!-- RE929 PUBLICATION BEGIN -->')!=1 or data.count(b'<!-- RE929 PUBLICATION END -->')!=1:raise ValueError('exact unique RE929 suffix required')
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
 if p.is_absolute() or '..' in p.parts or path not in PUBLIC_PATHS:raise ValueError('outside explicit RE929 public scope')
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
 for ticket,status in [('RE928','PRIVATE_EXCEPTION_FINITE_ACCEPTED'),('RE929','PUBLIC_METADATA_TESTS_ONLY')]:w.writerow([ticket,'archived proof' if ticket!='RE929' else 'fresh metadata',status,'false',d['publication_review']])
 out[CSV_PATH]=stream.getvalue().encode()
 for p,b in out.items():guard_output(p,b)
 return out
def original_compatibility(path,text):
 spec=COMPATIBILITY_DELTAS[path]
 for old,new in reversed(spec['replacements']):
  if text.count(new)!=1:raise ValueError('exact RE929 compatibility adapter required')
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
 print('RE929 PUBLIC_METADATA_TESTS_ONLY PASS; exact-public-hash independent review PENDING')
if __name__=='__main__':
 argparse.ArgumentParser(description=__doc__).parse_args();check()
