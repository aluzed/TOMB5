"""RE913 metadata only portable publication; no private dependency."""
import argparse,copy,csv,hashlib,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PRIOR_DASHBOARD='docs/reverse/tomb5-progress-dashboard-re911-v1.html'
PRIOR_MAINTAINED='docs/reverse/tomb5-progress-dashboard-maintained-re911-v1.html'
DASHBOARD='docs/reverse/tomb5-progress-dashboard-re913-v1.html'
MAINTAINED='docs/reverse/tomb5-progress-dashboard.html'
STORY='docs/stories/RE-913-sdk-prerequisite-diagnostic-publication.md'
REPORT='docs/reverse/functions/re913-sdk-prerequisite-diagnostic-publication.md'
JSON_PATH='docs/reverse/generated/re913-sdk-prerequisite-diagnostic-publication-v1.json'
CSV_PATH='docs/reverse/generated/re913-sdk-prerequisite-diagnostic-tracker-v1.csv'
PRIOR_SHA='0c8f2ed94df0b05db19742d71766bb3d9b086e9d7214806cbf299727016a3a53'
MAINTAINED_SHA='a5236df659e2c8d4752323dca21afb468083947405d2664832c9e6d9ea8f943d'
EXPECTED={'schema': 're913-sdk-prerequisite-diagnostic-publication-v1', 'publication_review': 'PENDING_INDEPENDENT_EXACT_HASH_REVIEW', 'fresh_execution_scope': 'PUBLIC_METADATA_TESTS_ONLY', 'fresh_target': 0, 'fresh_native': 0, 'integration': False, 'production_patch': False, 'global_scope': 'FAIL', 'procedure_scope': 'FAIL', 'naturalcaller': 'BLOCKED', 'authentication_scope': 'all three RE912 inventories exact file sets sizes hashes and seals freshly verified; no numerical replay', 'authentication': {'re912-gpustat-prerequisite': {'entries': 71, 'manifest_sha256': '2b3b7095bc8db4d0e5b498d07fc057ef4545cdbd8021221e4f75255172b77b58', 'seal_sha256': '01b16b178ddb0f02130f335c785eb9d4e40b800323dc594806ce0e5333ae014a', 'verdict_sha256': 'bd2f0a4a4430d37bfcdfcef3ede314e4fe9d3c2365d8f9167ff89ec6b4e9fe10', 'verification_sha256': '7007bed3fddaf9626fc7d37e4a4589463600a9c0b101c90609d93bd61e1f4d42'}, 're912-review': {'entries': 84, 'manifest_sha256': '2b9cdc9c348610747e4d980624dbe25c00d2afe60b0c30ea95679ddb42e3bbae', 'seal_sha256': '7e81a736bce980850aa49aff52a5de4c9b801daa618ff5a3ff6e35e2e8e785b1', 'verdict_sha256': '61434fd898e98df40a81d7d9168834f308c952bdbd02a72b501a5fe1bffb6e17', 'verification_sha256': '6f90f2bebe62a3ace6054c8a8611c9165b79417cbbdda1faeacb5f375ec05d49'}, 're912-review/retry01': {'entries': 58, 'manifest_sha256': '220d4d99f5863500c0985a829becea9d4e4e73a7345d91ab1809797e764b4a3d', 'seal_sha256': 'c57429559f910bf23c0570cf2c86c018130d888245702475f8147beed56ebccd', 'verdict_sha256': '61434fd898e98df40a81d7d9168834f308c952bdbd02a72b501a5fe1bffb6e17', 'verification_sha256': 'd0ff2f77acd41e99089f40f75ca854077eaa6ced45cb0a24a79a21db8da9fa72'}}, 'RE912': {'diagnostic': 'PASS_ONLY', 'functional_passed': False, 'functional_GREEN': 0, 'producer': {'accepted_target_runs': 1, 'target_visits': 124, 'archive_comparison_not_fresh_oracle': True, 'complete_TU_compiles': 8, 'normal_compiles': 4, 'ASan_UBSan_compiles': 4, 'native_links': 0, 'native_runs': 0}, 'reviewer_accepted': {'fresh_target': 1, 'stdlib_oracle': 1, 'RAM_bytes': 4194304, 'GPR': 32, 'PC_visits': 124, 'accesses': 54, 'stores': 45, 'calls': 3, 'complete_TU_compiles': 8, 'native_links': 0, 'native_runs': 0}, 'reviewer_cumulative': {'fresh_target': 2, 'stdlib_oracle': 2, 'first_attempt': 'FAIL_OPERAND_DECODE', 'accepted_successor': 'retry01'}, 'SDK': {'argument': -1, 'GPUSTAT_initial_read_required': True, 'Timer1_stable_pair_required': True, 'first_invocation_parity_toggle_wait_required': False, 'suffix_static_not_executed': True}, 'source_scan_files': 40, 'source_scan_universal_absence': False, 'native_SDL_GetTicks_g_swapTime_counters': 'NOT_AUTHENTIC_SDK_MMIO_GPUSTAT_PRODUCER', 'sanitizer_clean_execution_claim': False, 'entry': 'constructed framework archived RAM not natural startup', 'producer_task_seconds': 419.17, 'producer_outer_seconds': 419.22, 'reviewer_task_seconds': 275.86, 'reviewer_outer_seconds': 275.91, 'source_anchor_seconds_distinct': 398.857, 'failed_runs_preserved': ['producer SyntaxError', 'review bootstrap SyntaxError', 'author lease postcheck expiry', 'first operand-decode FAIL'], 'next': 'RE914 authentic startup GPUSTAT initial and coherent Timer1 producer attribution or authenticated hardware capture bridge; no arbitrary constants/native VSync SDK double/sector injection'}}
COMPATIBILITY_DELTAS={'scripts/reverse/re911_publication.py': {'before_sha256': 'c06bfa5f36abc4613512c2f8d87898adccad35fca230f072b3ded0eb1ceee896', 'replacements': [('\ndef preceding_maintained(data):return inverse(data,MAINTAINED_SHA)', "\ndef preceding_maintained(data):\n if b'<!-- RE913 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re913_publication.py'))['preceding_maintained'](data)\n return inverse(data,MAINTAINED_SHA)\ndef read_maintained():\n data=(ROOT/MAINTAINED).read_bytes()\n if b'<!-- RE913 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re913_publication.py'))['preceding_maintained'](data)\n return data"), ("\n  if (ROOT/p).read_bytes()!=b:raise ValueError('generated drift '+p)", "\n  if (read_maintained() if p==MAINTAINED else (ROOT/p).read_bytes())!=b:raise ValueError('generated drift '+p)")]}, 'tests/reverse/test_re911_publication.py': {'before_sha256': '8a53b19c877fa8e0eaa04f4248a39d936e4814f87d95a804a06a48fef8a8421b', 'replacements': [('for p,b in out.items():assert (ROOT/p).read_bytes()==b;m.guard_output(p,b)', 'for p,b in out.items():assert (m.read_maintained() if p==m.MAINTAINED else (ROOT/p).read_bytes())==b;m.guard_output(p,b)')]}}
SECTION='\n<!-- RE913 PUBLICATION BEGIN -->\n<section id="re913-publication-v1" data-integration="false"><h2>CURRENT RE913 — RE912 SDK prerequisite diagnostic only</h2><p>VSync(-1) requires initial GPUSTAT then stable Timer1 pair, no first-invocation parity toggle wait. Suffix static NOT executed. Producer1fresh124visits archive comparison; reviewer accepted1target1stdlib FULL RAM4194304 GPR32 PC124 accesses54 stores45 calls3; cumulative2target2oracle includes immutable firstFAIL. Each8complete-TU compiles4normal4ASanUBSan i386, ZERO native link/run or sanitizer-clean claim; bounded40file scan not universal absence.</p><p>Functional BLOCKED/global FAIL/procedure FAIL/integration=false/naturalcaller BLOCKED. PENDING_INDEPENDENT_EXACT_HASH_REVIEW; publication adds ZERO numerical replays. RE914 authentic startup GPUSTAT initial and coherent Timer1 producer attribution or authenticated hardware capture; no SDK double, forced status, sectors, seek/read, AI registration InitialiseItem or runtime.</p><p><a href="../stories/RE-913-sdk-prerequisite-diagnostic-publication.md">Story / acceptance</a> · <a href="functions/re913-sdk-prerequisite-diagnostic-publication.md">Evidence / blockers</a> · <a href="generated/re913-sdk-prerequisite-diagnostic-publication-v1.json">Status</a></p></section>\n<!-- RE913 PUBLICATION END -->\n'
DOC='# RE913 — publication sûre du diagnostic RE912\n\n## Progression\n- [x] RED/GREEN metadata public-only; zéro replay numérique nouveau.\n- [x] Trois inventories RE912 authentifiés exact file sets/size/SHA/seals; retry01 strict passed true, empty errors/concerns.\n- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW; worktree-only aucun stage/commit/push.\n\n## Evidence\nPremière SDK VSync(-1): GPUSTAT initial puis paire Timer1 stable; pas de premier wait/toggle parité. Suffixe statique NON exécuté. Producteur1 fresh124visits archivecomparison pas fresh oracle. Reviewer first1target1stdlib FAIL operand decode puis retry01 indépendant1target1stdlib accepté: FULL RAM4194304/GPR32/124PC/54accesses/45stores/3calls. Cumul reviewer2target2oracle distinct accepté1+1. Chacun8compiles réels4completeTUs EMULATOR/LIBETC/LIBAPI/LIBGPU i3864normal4ASanUBSan exit0; ZEROlink/run/native/sanitizer-clean claim. SDL_GetTicks/g_swapTime/counters ne produisent pas le bus SDK GPUSTAT; scan40files borné pas absence universelle.\n\n## Blockers\nFunctional BLOCKED/global FAIL/procedure FAIL/integration=false/naturalcaller BLOCKED. Aucun CDdouble/statusforced/sector injection/seekread/AI/registration/InitialiseItem/runtime/sourcepatch. CPU framework et RAM archives construits ≠ natural startup; software oracle ≠ hardware. firstFAIL producerSyntaxError reviewerbootstrapSyntaxError authorleasepostcheckexpiry et operanddecodeFAIL immuables retry distinct. Producer419.17task419.22outer reviewer275.86task275.91outer source398.857origine distincte. BLOCKED-001/002 user deletes/report-tech/cache/cold archives préservés.\n\n## Acceptance\n- [x] Schema recursive exact types/scalars, negative et benign safety controls.\n- [x] Dashboard versionné/maintenu unique suffixe inverse exact RE911; historical pins unchanged.\n- [x] TDD public-only sans ignored proofs et compatibility same baseline nodeids.\n- [ ] Revue indépendante exacte des hashes publics PENDING.\n\n## Next — RE914\nProducteur GPUSTAT initial + Timer1 cohérent startup attribution ou capture hardware authentifiée, bridge déclaré; pas constant arbitraire/native VSync SDKdouble/secteur18040 injecté.\n'
OUTPUT_PATHS=(STORY,REPORT,JSON_PATH,CSV_PATH,DASHBOARD,MAINTAINED)
PUBLIC_PATHS=OUTPUT_PATHS+(PRIOR_MAINTAINED,"scripts/reverse/re913_publication.py","tests/reverse/test_re913_publication.py")+tuple(COMPATIBILITY_DELTAS)
def metadata():return copy.deepcopy(EXPECTED)
def validate(data):
 def exact(a,b):
  if type(a) is not type(b):return False
  if isinstance(b,dict):return set(a)==set(b) and all(exact(a[k],b[k]) for k in b)
  if isinstance(b,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
  return a==b
 if not exact(data,EXPECTED):raise ValueError('exact RE913 recursive schema types/counts/hash/scope required')
 return data
def digest(b):return hashlib.sha256(b).hexdigest()
def inverse(data,sha):
 suffix=SECTION.encode()+b'</html>'
 if not data.endswith(suffix) or data.count(b'<!-- RE913 PUBLICATION BEGIN -->')!=1 or data.count(b'<!-- RE913 PUBLICATION END -->')!=1:raise ValueError('exact unique RE913 suffix required')
 before=data[:-len(suffix)]+b'</html>'
 if digest(before)!=sha:raise ValueError('exact predecessor bytes changed')
 return before
def preceding_dashboard(data):return inverse(data,PRIOR_SHA)
def preceding_maintained(data):
 if b'<!-- RE915 PUBLICATION' in data:
  import runpy
  data=runpy.run_path(str(ROOT/'scripts/reverse/re915_publication.py'))['preceding_maintained'](data)
 return inverse(data,MAINTAINED_SHA)
def read_maintained():
 data=(ROOT/MAINTAINED).read_bytes()
 if b'<!-- RE915 PUBLICATION' in data:
  import runpy
  data=runpy.run_path(str(ROOT/'scripts/reverse/re915_publication.py'))['preceding_maintained'](data)
 return data
def maintained_before():
 b=(ROOT/PRIOR_MAINTAINED).read_bytes()
 if digest(b)!=MAINTAINED_SHA:raise ValueError('maintained historical fixture drift')
 return b

RAW=re.compile(rb'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|raw_opcode|raw_pc|register_values|target_address|payload_offset|data:image|```(?:asm|mips|cpp|c)\b',re.I)
SECRET=re.compile(rb'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|(?:api[_-]?key|password|secret)\s*[:=]\s*[\"\x27][^\"\x27\s]{12,}',re.I)
def guard_added(path,payload):
 p=Path(path)
 if p.is_absolute() or '..' in p.parts or path not in PUBLIC_PATHS:raise ValueError('outside explicit RE913 public scope')
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
 if digest(before)!=PRIOR_SHA or not before.endswith(b'</html>'):raise ValueError('exact RE911 predecessor required')
 out={STORY:document().encode(),REPORT:document(True).encode(),JSON_PATH:(json.dumps(d,indent=2,sort_keys=True)+'\n').encode(),DASHBOARD:before[:-7]+SECTION.encode()+b'</html>',MAINTAINED:maintained_before()[:-7]+SECTION.encode()+b'</html>'}
 stream=io.StringIO(newline='');w=csv.writer(stream,lineterminator='\n');w.writerow(['ticket','scope','status','integration','publication_review'])
 for ticket,status in [('RE912','DIAGNOSTIC_PASS_FUNCTIONAL_BLOCKED_SDK'),('RE913','PUBLIC_METADATA_TESTS_ONLY')]:w.writerow([ticket,'archived proof' if ticket!='RE913' else 'fresh metadata',status,'false',d['publication_review']])
 out[CSV_PATH]=stream.getvalue().encode()
 for p,b in out.items():guard_output(p,b)
 return out
def original_compatibility(path,text):
 spec=COMPATIBILITY_DELTAS[path]
 for old,new in reversed(spec['replacements']):
  if text.count(new)!=1:raise ValueError('exact RE913 compatibility adapter required')
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
 print('RE913 PUBLIC_METADATA_TESTS_ONLY PASS; exact-public-hash independent review PENDING')
if __name__=='__main__':
 argparse.ArgumentParser(description=__doc__).parse_args();check()
