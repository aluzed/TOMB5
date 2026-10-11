"""RE915 metadata only portable publication; no private dependency."""
import argparse,copy,csv,hashlib,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PRIOR_DASHBOARD='docs/reverse/tomb5-progress-dashboard-re913-v1.html'
PRIOR_MAINTAINED='docs/reverse/tomb5-progress-dashboard-maintained-re913-v1.html'
DASHBOARD='docs/reverse/tomb5-progress-dashboard-re915-v1.html'
MAINTAINED='docs/reverse/tomb5-progress-dashboard.html'
STORY='docs/stories/RE-915-header-startup-diagnostic-publication.md'
REPORT='docs/reverse/functions/re915-header-startup-diagnostic-publication.md'
JSON_PATH='docs/reverse/generated/re915-header-startup-diagnostic-publication-v1.json'
CSV_PATH='docs/reverse/generated/re915-header-startup-diagnostic-tracker-v1.csv'
PRIOR_SHA='ddfc21ceb1a8a31457422acd8eac5517e54ad6be875e2ff5135a4c587147749d'
MAINTAINED_SHA='0616f8623d883c92b4661e9517b4a3d35a18a8916b7ad6c58abf07847f987cb1'
EXPECTED={'schema': 're915-header-startup-diagnostic-publication-v1', 'publication_review': 'PENDING_INDEPENDENT_EXACT_HASH_REVIEW', 'fresh_execution_scope': 'PUBLIC_METADATA_TESTS_ONLY', 'fresh_target': 0, 'fresh_native': 0, 'integration': False, 'production_patch': False, 'global_scope': 'FAIL', 'procedure_scope': 'FAIL', 'naturalcaller': 'BLOCKED', 'authentication_scope': 'all four RE914 root namespaces exact sets sizes hashes seals freshly verified; no numerical replay', 'authentication': {'re914-startup-hardware-provenance': {'entries': 17, 'manifest_sha256': '355d7516262b1719ec6dcc47363523ecb1a2cc8cde00c9bbd9f8a0a981d3a614', 'seal_sha256': '6fa6f705d2b432661f28082cd637b404d484e17273933893612fcb0d8b6ff5c4', 'verdict_sha256': '61434fd898e98df40a81d7d9168834f308c952bdbd02a72b501a5fe1bffb6e17'}, 're914-review': {'entries': 10, 'manifest_sha256': 'c5898099313c086f6cf9a4729ef10432f3bafde6b236959f7610bd8ed1e9f960', 'seal_sha256': 'e45761d32e5a5cc2fb4c86543201110357f5df1b095508ffb4eabba9a0257b22', 'verdict_sha256': '6c5a4fde50aa11cca7fd874de1d438d53a7978b743648e8948f6a31951590840'}, 're914-review/retry01': {'entries': 19, 'manifest_sha256': 'b3215020dcf88bea53306150db7a4966b28ecb539a493f7e3a08670c47392f39', 'seal_sha256': '777f654cffd26a95ea476b7a92f58cdc12ff96fdd3149e0379cf23258bbf6cb5', 'verdict_sha256': '61434fd898e98df40a81d7d9168834f308c952bdbd02a72b501a5fe1bffb6e17'}, 're914-review/retry01/audit-annex': {'entries': 5, 'manifest_sha256': '5878bce63f84c183e177fe7abb6f9153901b64deed508e1366a4dad874618e1d', 'seal_sha256': '11aa37b63112888e47cf154c6cf22bf5bd0ca94b183406128ba2bc21f8ff6a16', 'verdict_sha256': '61434fd898e98df40a81d7d9168834f308c952bdbd02a72b501a5fe1bffb6e17'}}, 'RE914': {'diagnostic': 'PASS_STRICT_FINITE_ONLY_WITH_ADDI_CLARIFICATION', 'functional_passed': False, 'functional_GREEN': 0, 'producer': {'accepted_target_runs': 1, 'independent_stdlib_oracle': 1, 'sensitivity_checks': 3}, 'reviewer_accepted': {'fresh_target': 1, 'independent_CPU_oracle': 1, 'sensitivity_checks': 5}, 'reviewer_cumulative': {'fresh_target': 1, 'independent_CPU_oracle': 2, 'first_attempt': 'FAIL_UNICORN_MISSING_AFTER_ORACLE', 'accepted_successor': 'retry01', 'clarification': 'retry01/audit-annex ZERO fresh executions'}, 'comparison': {'ordered_visits': 1778375, 'accesses': 355674, 'interpreted_stores': 355672, 'interpreted_loads': 2, 'RAM_bytes': 2097152, 'register_carriers': 32, 'known_GPR': 9, 'UNKNOWN_carriers': 23, 'full_RAM_GPR_PC_order_accesses_knownness_equal': True, 'visits_not_retired_instructions': True}, 'startup': {'header_PC_SP_GP_payload_MD5_CONTRIBUTING_authenticated': True, 'entry': 'POST_BIOS_EXECUTABLE_ENTRY_NOT_POWER_RESET', 'RAM_outside_payload': 'CONSTRUCTED_ZERO_NOT_NATURAL_RAM', 'unknown_carriers_authentically_consumed': False, 'stop_before_unknown_RA_store': True, 'BIOS_RA_absent_header': True, 'BSS_clear_stack_heap_setup': 'FINITE_AUTHENTIC_EXECUTED_PREFIX', 'GPU_Timer_writes': 0, 'SDK_BIOS_return_doubles': 0, 'arbitrary_RA_injection': False, 'GPU_setup_static_not_reached': True, 'RE910_RE912_replays': 0, 'native_compiles': 0, 'native_runs': 0, 'runtime': 0}, 'ADDI': {'executed': 1, 'checked_no_overflow': True, 'historical_boolean_rejected_as_written': True, 'universal_emulator_approval': False, 'no_syscall_COP_status_reached': True}, 'producer_task_seconds': 232.4, 'producer_outer_seconds': 232.44, 'reviewer_task_seconds': 297.65, 'reviewer_outer_seconds': 297.69, 'source_anchor_seconds_distinct': 304.6, 'first_FAIL_preserved': True, 'next': 'RE916 authentic BIOS Exec RA producer entry contract or authenticated state capture; upstream hardware gates remain BLOCKED; no positive CD sector or RA constant'}}
COMPATIBILITY_DELTAS={'scripts/reverse/re913_publication.py': {'before_sha256': '3af01e4b18ce311ec7f2930b4786972e3877f5d5a6952341995c3295e3afc330', 'replacements': [('\ndef preceding_maintained(data):return inverse(data,MAINTAINED_SHA)', "\ndef preceding_maintained(data):\n if b'<!-- RE915 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re915_publication.py'))['preceding_maintained'](data)\n return inverse(data,MAINTAINED_SHA)\ndef read_maintained():\n data=(ROOT/MAINTAINED).read_bytes()\n if b'<!-- RE915 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re915_publication.py'))['preceding_maintained'](data)\n return data"), ("\n  if (ROOT/p).read_bytes()!=b:raise ValueError('generated drift '+p)", "\n  if (read_maintained() if p==MAINTAINED else (ROOT/p).read_bytes())!=b:raise ValueError('generated drift '+p)")]}, 'tests/reverse/test_re913_publication.py': {'before_sha256': 'dc5615dd7d4d2c96f29cc901cb8bb68ca244d575f954507001d8b6b1095e1862', 'replacements': [('for p,b in out.items():assert (ROOT/p).read_bytes()==b;m.guard_output(p,b)', 'for p,b in out.items():assert (m.read_maintained() if p==m.MAINTAINED else (ROOT/p).read_bytes())==b;m.guard_output(p,b)')]}}
SECTION='\n<!-- RE915 PUBLICATION BEGIN -->\n<section id="re915-publication-v1" data-integration="false"><h2>CURRENT RE915 — RE914 finite header-startup diagnostic only</h2><p>Authenticated header POST BIOS entry, NOT reset. BSS/stack/heap finite prefix; stop BEFORE unknown BIOS-produced RA store. Constructed zero RAM outside payload;9known23UNKNOWN carriers not authentically consumed. Producer1target1oracle; acceptedreview1target1independentCPUoracle; cumulative1target2oracle including firstFAIL Unicorn missing. FULL2MiB RAM32carriers knownness PC order accesses equal:1778375visits355674accesses355672interpretedstores2loads. Visits not retired instructions. ADDI1 executed checked no overflow; immutable historical overbroad boolean rejected, separate audit-only clarification, not universal emulator approval.</p><p>Functional BLOCKED/global FAIL/procedure FAIL/integration=false/naturalcaller BLOCKED. GPU/Timer writes0, BIOS/SDK doubles0, RA injection0, native/runtime0. PENDING_INDEPENDENT_EXACT_HASH_REVIEW; publication ZERO numerical replays. RE916 authentic BIOS Exec RA producer entry contract or authenticated capture; upstream hardware gates remain blocked, no RA constant or positive CD sector.</p><p><a href="../stories/RE-915-header-startup-diagnostic-publication.md">Story / acceptance</a> · <a href="functions/re915-header-startup-diagnostic-publication.md">Evidence / blockers</a> · <a href="generated/re915-header-startup-diagnostic-publication-v1.json">Status</a></p></section>\n<!-- RE915 PUBLICATION END -->\n'
DOC="# RE915 — publication sûre du diagnostic fini RE914\n\n## Progression\n- [x] RED/GREEN metadata public-only, aucun replay numérique nouveau.\n- [x] Quatre namespaces RE914 authentifiés exact sets/size/SHA/seals ; retry01 et audit-annex strict passed true empty errors/concerns.\n- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW ; worktree-only aucun stage/commit/push.\n\n## Evidence\nHeader PC/SP/GP/payload/MD5 CONTRIBUTING authentifiés : entrée POST BIOS, pas power reset. Producteur1target1oracle indépendant, acceptedreview1target1CPUoracle ; cumulreview1target2oracle inclut firstFAIL Unicorn absent après oracle. Comparaison complète 2MiB RAM/32registercarriers/knownness/ordre PC/accesses égale : 1778375visits,355674accesses,355672interpretedstores,2loads ; visites pas instructions retirées. 9known23UNKNOWN carriers jamais authentiquement consommés. BSS/stack/heap setup fini exécuté ; arrêt AVANT SW RA inconnu parce que BIOS RA absent header. Producteur3/review5 sensitivity checks. GPU/Timer writes0, SDK/BIOS doubles0, RA injection0, RE910/912replays0, native compile/run/runtime0. Setup GPU statique non atteint.\n\n## Blockers\nFunctional BLOCKED/global FAIL/procedure FAIL/integration=false/naturalcaller BLOCKED. Zéros hors payload CONSTRUCTED, pas RAM naturelle. Oracle CPU logiciel indépendant pas hardware. FirstFAIL et checker errors immuables, retry distinct ; booléen audit ADDI rejeté tel quel et clarification audit-annex : une ADDI exécutée, non-overflow vérifié, pas approbation universelle de l'émulateur. Upstream hardware preconditions toujours bloquantes. Producer232.40task232.44outer reviewer297.65task297.69outer sourceanchor304.6 origine distincte. BLOCKED-001/002 user deletes/report-tech/cache/cold archives/RE893partial préservés.\n\n## Acceptance\n- [x] Schema recursive exact bool/int/float types/scalars ; contrôles négatifs et benign mêmes chemins légitimes.\n- [x] Dashboard versionné/maintenu suffixe unique inverse exact RE913 ; historical pins unchanged.\n- [x] Public-only sans ignored proofs ; compatibility same baseline nodeids, pas global GREEN.\n- [ ] Revue indépendante exacte des hashes publics PENDING.\n\n## Next — RE916\nContrat/producteur BIOS Exec RA authentique ou capture authentifiée de l'état d'entrée ; pas RA arbitraire ni secteur CD positif. Aucun sourcepatch/sourceproduction/native/runtime/cleanup/cron autorisé par cette publication.\n"
OUTPUT_PATHS=(STORY,REPORT,JSON_PATH,CSV_PATH,DASHBOARD,MAINTAINED)
PUBLIC_PATHS=OUTPUT_PATHS+(PRIOR_MAINTAINED,"scripts/reverse/re915_publication.py","tests/reverse/test_re915_publication.py")+tuple(COMPATIBILITY_DELTAS)
def metadata():return copy.deepcopy(EXPECTED)
def validate(data):
 def exact(a,b):
  if type(a) is not type(b):return False
  if isinstance(b,dict):return set(a)==set(b) and all(exact(a[k],b[k]) for k in b)
  if isinstance(b,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
  return a==b
 if not exact(data,EXPECTED):raise ValueError('exact RE915 recursive schema types/counts/hash/scope required')
 return data
def digest(b):return hashlib.sha256(b).hexdigest()
def inverse(data,sha):
 suffix=SECTION.encode()+b'</html>'
 if not data.endswith(suffix) or data.count(b'<!-- RE915 PUBLICATION BEGIN -->')!=1 or data.count(b'<!-- RE915 PUBLICATION END -->')!=1:raise ValueError('exact unique RE915 suffix required')
 before=data[:-len(suffix)]+b'</html>'
 if digest(before)!=sha:raise ValueError('exact predecessor bytes changed')
 return before
def preceding_dashboard(data):return inverse(data,PRIOR_SHA)
def preceding_maintained(data):
 if b'<!-- RE917 PUBLICATION' in data:
  import runpy
  data=runpy.run_path(str(ROOT/'scripts/reverse/re917_publication.py'))['preceding_maintained'](data)
 return inverse(data,MAINTAINED_SHA)
def read_maintained():
 data=(ROOT/MAINTAINED).read_bytes()
 if b'<!-- RE917 PUBLICATION' in data:
  import runpy
  data=runpy.run_path(str(ROOT/'scripts/reverse/re917_publication.py'))['preceding_maintained'](data)
 return data
def maintained_before():
 b=(ROOT/PRIOR_MAINTAINED).read_bytes()
 if digest(b)!=MAINTAINED_SHA:raise ValueError('maintained historical fixture drift')
 return b

RAW=re.compile(rb'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|raw_opcode|raw_pc|register_values|target_address|payload_offset|data:image|```(?:asm|mips|cpp|c)\b',re.I)
SECRET=re.compile(rb'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|(?:api[_-]?key|password|secret)\s*[:=]\s*[\"\x27][^\"\x27\s]{12,}',re.I)
def guard_added(path,payload):
 p=Path(path)
 if p.is_absolute() or '..' in p.parts or path not in PUBLIC_PATHS:raise ValueError('outside explicit RE915 public scope')
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
 if digest(before)!=PRIOR_SHA or not before.endswith(b'</html>'):raise ValueError('exact RE913 predecessor required')
 out={STORY:document().encode(),REPORT:document(True).encode(),JSON_PATH:(json.dumps(d,indent=2,sort_keys=True)+'\n').encode(),DASHBOARD:before[:-7]+SECTION.encode()+b'</html>',MAINTAINED:maintained_before()[:-7]+SECTION.encode()+b'</html>'}
 stream=io.StringIO(newline='');w=csv.writer(stream,lineterminator='\n');w.writerow(['ticket','scope','status','integration','publication_review'])
 for ticket,status in [('RE914','DIAGNOSTIC_PASS_FUNCTIONAL_BLOCKED_SDK'),('RE915','PUBLIC_METADATA_TESTS_ONLY')]:w.writerow([ticket,'archived proof' if ticket!='RE915' else 'fresh metadata',status,'false',d['publication_review']])
 out[CSV_PATH]=stream.getvalue().encode()
 for p,b in out.items():guard_output(p,b)
 return out
def original_compatibility(path,text):
 spec=COMPATIBILITY_DELTAS[path]
 for old,new in reversed(spec['replacements']):
  if text.count(new)!=1:raise ValueError('exact RE915 compatibility adapter required')
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
 print('RE915 PUBLIC_METADATA_TESTS_ONLY PASS; exact-public-hash independent review PENDING')
if __name__=='__main__':
 argparse.ArgumentParser(description=__doc__).parse_args();check()
