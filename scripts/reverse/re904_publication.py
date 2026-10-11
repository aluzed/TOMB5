"""RE904 portable safe metadata only; no private dependencies."""
import argparse,copy,csv,hashlib,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PRIOR_DASHBOARD='docs/reverse/tomb5-progress-dashboard-re901-v1.html'
PRIOR_MAINTAINED='docs/reverse/tomb5-progress-dashboard-maintained-re901-v1.html'
DASHBOARD='docs/reverse/tomb5-progress-dashboard-re904-v1.html'
MAINTAINED='docs/reverse/tomb5-progress-dashboard.html'
STORY='docs/stories/RE-904-private-z-proof-publication.md'
REPORT='docs/reverse/functions/re904-private-z-proof-publication.md'
JSON_PATH='docs/reverse/generated/re904-private-proof-publication-v1.json'
CSV_PATH='docs/reverse/generated/re904-private-proof-tracker-v1.csv'
PRIOR_SHA='183bde811d0c5dcd9033f4cf7d0cd3e72706d9fbc62352b4c3997581a62f0583'
MAINTAINED_SHA='5c8d5185f02ec56f95f37e5c54d75767d42a3fcf436430a2b0d27e005c97bb43'
SOURCE_SHA='59e70b260ae67d613e5fa74486c728a63bd3bb7ae4727537e293d4c057d9b7fa'
EXPECTED={'schema': 're904-private-z-proof-publication-v1', 'publication_review': 'PENDING_INDEPENDENT_EXACT_HASH_REVIEW', 'fresh_execution_scope': 'PUBLIC_METADATA_TESTS_ONLY', 'fresh_target': 0, 'fresh_native': 0, 'integration': False, 'production_patch': False, 'public_helpers_green': False, 'global_scope': 'FAIL', 'procedure_scope': 'FAIL', 'next_ticket': 'RE905', 'next_objective': 'separately authorized new natural provenance; no repetition of closed finite X/Y/Z controls', 'limits': 'finite constructed Z nonsaturating callers only; no natural startup, dual stacks, camera, gameplay, GTE hardware, saturation, general axes or universal definedness. CPU/math independent; target bridge shares software LIBGTE. RAW2528+Position12 selected projection, not whole native RAM; aborts have no final projection.', 'archived_private_results': [{'ticket': 'RE902', 'scope': 'PASS_FINITE_CHARACTERIZATION_NOT_STRICT_CODE_APPROVAL', 'geometry': 'PASS', 'fullraw_verdict': 'FAIL', 'strict_verdict': 'FAIL', 'target': 9, 'cpu': 9, 'math': 9, 'native': {'attempts': 36, 'returns': 24, 'aborts': 12, 'raw_mismatches': 24, 'position_mismatches': 0}, 'reviewer_native': {'attempts': 36, 'returns': 24, 'aborts': 12}, 'producer_diagnostics': {'attempts': 4, 'returns': 3, 'aborts': 1}, 'reviewer_diagnostics': {'attempts': 6, 'returns': 4, 'aborts': 2}, 'review_verdict_sha256': '0058cc5efd78006adf62f5ccf4a04c5325d6ddb291c4235299ca22bccb31b256', 'causal_attribution': 'four Z scratch stores native16 versus target32; iRotZ signed packing shifts UB; two secondary normal stores observed including same-value writes', 'historical_failures': ['provider refusal RE902 112.45/112.5 preserved; no numerical replay', 'first empty wrong-signature static bodies preserved, exact signature recovery separate']}, {'ticket': 'RE903', 'scope': 'PRIVATE_SCOPED_APPROVED_NOT_INTEGRATION', 'fullraw_verdict': 'PASS_FINITE_SELECTED_PROJECTION', 'strict_verdict': 'PASS_FINITE_CASES', 'candidate_sha256': 'eee7b22f5cc66b314d144db227b187d40a4c0846d6248c03974c90a5f2308d01', 'baseline_sha256': '89999eaaf2818eb5b1073d8c206a8867c56e57a27a5155c8fcf297de08085f0c', 'producer_accepted': {'target': 9, 'cpu': 9, 'math': 9, 'native_attempts': 291, 'native_returns': 253, 'native_aborts': 38, 'probes': 3}, 'producer_firstfail': {'target': 9, 'cpu': 9, 'math': 9, 'native_attempts': 255, 'native_returns': 229, 'native_aborts': 26, 'probes': 3}, 'producer_roots_total': {'target': 18, 'native_attempts': 546, 'native_returns': 482, 'native_aborts': 64}, 'reviewer': {'target': 9, 'cpu': 9, 'math': 9, 'native_attempts': 288, 'native_returns': 252, 'native_aborts': 36}, 'stage_counts': {'baseline': {'attempts': 36, 'returns': 24, 'UBSanaborts': 12, 'raw_available': 24, 'raw_mismatches': 24, 'position_mismatches': 0}, 'candidate': {'attempts': 36, 'returns': 36, 'UBSanaborts': 0, 'raw_available': 36, 'raw_mismatches': 0, 'position_mismatches': 0}, 'rollback-packing0': {'attempts': 36, 'returns': 24, 'UBSanaborts': 12, 'raw_available': 24, 'raw_mismatches': 0, 'position_mismatches': 0}, 'rollback-packing1': {'attempts': 36, 'returns': 24, 'UBSanaborts': 12, 'raw_available': 24, 'raw_mismatches': 0, 'position_mismatches': 0}, 'rollback-primary-VZ0': {'attempts': 36, 'returns': 36, 'UBSanaborts': 0, 'raw_available': 36, 'raw_mismatches': 12, 'position_mismatches': 0}, 'rollback-primary-VZ1': {'attempts': 36, 'returns': 36, 'UBSanaborts': 0, 'raw_available': 36, 'raw_mismatches': 12, 'position_mismatches': 0}, 'rollback-secondary-VZ0': {'attempts': 36, 'returns': 36, 'UBSanaborts': 0, 'raw_available': 36, 'raw_mismatches': 12, 'position_mismatches': 0}, 'rollback-secondary-VZ1': {'attempts': 36, 'returns': 36, 'UBSanaborts': 0, 'raw_available': 36, 'raw_mismatches': 12, 'position_mismatches': 0}}, 'review_verdict_sha256': '04f527e7f102cf1c0fe6fa02815658293ad3334c4a04c4c46b0a1addf6f53662', 'repair': 'six lines: four explicit full32 Z scratch clears plus two unsigned packings with explicit signed32 conversion; private candidate only', 'static_annex': {'candidate_bodies': 20, 'baseline_bodies': 8, 'compiled_storewidths': 32, 'new_native': 0, 'verdict_sha256': 'bcae7a2fc3d79adcb9d84b7458a7fdc143e7fc8f95c6ec0e63eaf4e95aab4122'}, 'historical_failures': ['original firstFAIL: unscoped rollback replaced inherited iRotX helper; recovery01 scoped exact iRotZ occurrence', 'review discovery firstFAIL duplicate expression uniqueness; zero native executions', 'initial failed static inspection preserved; accepted static annex zero replay'], 'rollback_summary': 'four writer rollbacks36 each return36, RAW mismatches12 geometry unchanged; two packing rollbacks36 each return24 abort12, RAW/geometry same among returns; candidate36 GREEN O0/O2 normal/strict RAW2528+Position12'}]}
COMPATIBILITY_DELTAS={'scripts/reverse/re901_publication.py': {'before_sha256': 'ab6cb060151eaec60bf2ff0a8d538b8e2bfb8dce59ef6c1541a54a3f337aa281', 'replacements': [('def preceding_maintained(data):return inverse(data,MAINTAINED_SHA)', "def preceding_maintained(data):\n if b'<!-- RE904 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re904_publication.py'))['preceding_maintained'](data)\n return inverse(data,MAINTAINED_SHA)\ndef read_maintained():\n data=(ROOT/MAINTAINED).read_bytes()\n if b'<!-- RE904 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re904_publication.py'))['preceding_maintained'](data)\n return data"), ('def original_compatibility(path,text):\n', "def original_compatibility(path,text):\n if path=='tests/reverse/test_re830_table_provenance_publication.py' and '# RE904 exact authenticated successor' in text:\n  import runpy\n  text=runpy.run_path(str(ROOT/'scripts/reverse/re904_publication.py'))['original_compatibility'](path,text)\n"), ("\n  if (ROOT/p).read_bytes()!=b:raise ValueError('generated drift '+p)", "\n  if (read_maintained() if p==MAINTAINED else (ROOT/p).read_bytes())!=b:raise ValueError('generated drift '+p)")]}, 'tests/reverse/test_re901_publication.py': {'before_sha256': 'd1956c5e2cecdef74f0a1b952ba3ce66f11ca63b122b99a29ea89c6d0377d1d2', 'replacements': [('for p,b in out.items():assert (ROOT/p).read_bytes()==b;m.guard_output(p,b)', 'for p,b in out.items():assert (m.read_maintained() if p==m.MAINTAINED else (ROOT/p).read_bytes())==b;m.guard_output(p,b)')]}, 'tests/reverse/test_re830_table_provenance_publication.py': {'before_sha256': 'cfc3ea47fc6302c325ede5087e3bb11fca0c92a595dce7d47f2a8c3da0cfc722', 'replacements': [('    # RE901 exact authenticated append-only successor; historical guards unchanged.\n', "    # RE904 exact authenticated successor; preserve contiguous older adapters.\n    if b'<!-- RE904 PUBLICATION' in data:\n        import runpy\n        try:\n            data = runpy.run_path(str(ROOT / 'scripts/reverse/re904_publication.py'))['preceding_maintained'](data)\n        except ValueError as error:\n            raise AssertionError('RE904 successor malformed or predecessor changed') from error\n    # RE901 exact authenticated append-only successor; historical guards unchanged.\n")]}}
OUTPUT_PATHS=(STORY,REPORT,JSON_PATH,CSV_PATH,DASHBOARD,MAINTAINED)
PUBLIC_PATHS=OUTPUT_PATHS+(PRIOR_MAINTAINED,'scripts/reverse/re904_publication.py','tests/reverse/test_re904_publication.py','scripts/reverse/re901_publication.py','tests/reverse/test_re901_publication.py','tests/reverse/test_re830_table_provenance_publication.py')
SECTION='\n<!-- RE904 PUBLICATION BEGIN -->\n<section id="re904-publication-v1" data-integration="false"><h2>CURRENT RE904 — ARCHIVED RE902–RE903 Z privé fini</h2><p><a href="../stories/RE-904-private-z-proof-publication.md">Story / acceptance</a> · <a href="functions/re904-private-z-proof-publication.md">Evidence / blockers</a> · <a href="generated/re904-private-proof-publication-v1.json">Metadata</a> · <a href="generated/re904-private-proof-tracker-v1.csv">Tracker</a> · <a href="tomb5-progress-dashboard-re904-v1.html#re904-publication-v1">Dashboard</a>.</p><p>RE902 geometry PASS, RAW FAIL, strict FAIL:36 tentatives24 retours12 aborts. RE903 six lignes PRIVÉES: accepted291 native dont3 probes; review288 tentatives252 retours36 aborts. Deux racines producteur546/482/64. Candidate36 GREEN; quatre rollback writers RAW-only, deux packings sanitizer-only. Tous firstFAIL conservés; annexe statique32 widths zéro replay.</p><p>Global FAIL / procédure FAIL / integration=false / public_helpers_green=false. PENDING_INDEPENDENT_EXACT_HASH_REVIEW. Finite constructed Z non naturel; startup/dual stacks/camera/hardware/saturation/gameplay non prouvés. Aucun replay numérique nouveau.</p></section>\n<!-- RE904 PUBLICATION END -->\n'
def metadata():return copy.deepcopy(EXPECTED)
def validate(data):
 def exact(a,b):
  if type(a) is not type(b):return False
  if isinstance(b,dict):return set(a)==set(b) and all(exact(a[k],b[k]) for k in b)
  if isinstance(b,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
  return a==b
 if not exact(data,EXPECTED):raise ValueError('exact RE904 recursive schema types/counts/hash/scope required')
 return data
def digest(b):return hashlib.sha256(b).hexdigest()
def inverse(data,sha):
 suffix=SECTION.encode()+b'</html>'
 if not data.endswith(suffix) or data.count(b'<!-- RE904 PUBLICATION BEGIN -->')!=1 or data.count(b'<!-- RE904 PUBLICATION END -->')!=1:raise ValueError('exact unique RE904 suffix required')
 before=data[:-len(suffix)]+b'</html>'
 if digest(before)!=sha:raise ValueError('exact predecessor bytes changed')
 return before
def preceding_dashboard(data):return inverse(data,PRIOR_SHA)
def preceding_maintained(data):
 if b'<!-- RE906 PUBLICATION' in data:
  import runpy
  data=runpy.run_path(str(ROOT/'scripts/reverse/re906_publication.py'))['preceding_maintained'](data)
 return inverse(data,MAINTAINED_SHA)
def read_maintained():
 data=(ROOT/MAINTAINED).read_bytes()
 if b'<!-- RE906 PUBLICATION' in data:
  import runpy
  data=runpy.run_path(str(ROOT/'scripts/reverse/re906_publication.py'))['preceding_maintained'](data)
 return data
def maintained_before():
 b=(ROOT/PRIOR_MAINTAINED).read_bytes()
 if digest(b)!=MAINTAINED_SHA:raise ValueError('maintained historical fixture drift')
 return b

RAW=re.compile(rb'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|raw_opcode|raw_pc|register_values|target_address|payload_offset|data:image|```(?:asm|mips|cpp|c)\b',re.I)
SECRET=re.compile(rb'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|(?:api[_-]?key|password|secret)\s*[:=]\s*[\"\x27][^\"\x27\s]{12,}',re.I)
def guard_added(path,payload):
 p=Path(path)
 if p.is_absolute() or '..' in p.parts or path not in PUBLIC_PATHS:raise ValueError('outside explicit RE904 public scope')
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
 text='# RE904 — publication metadata Z privée, v1\n\n## Progression\n- [x] RED46 générateur absent avant implémentation.\n- [x] Seals/verdicts sélectionnés authentifiés, full inventories vérifiés auparavant par parent.\n- [x] Schéma exact, tracker, dashboard append-only avec inverse.\n- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW.\n\n## Evidence\n'
 for row in EXPECTED['archived_private_results']:text+='\n### '+row['ticket']+'\n'+json.dumps(row,indent=2,sort_keys=True)+'\n'
 text+='\n## Blockers\nintegration=false; production_patch=false; public_helpers_green=false. Global FAIL / procédure FAIL.\n'+EXPECTED['limits']+'\nfirstFAIL, provider refusal et récupérations immuables distincts. Temps transport parent séparés du clock interne des proofs. Source MATHS publique inchangée. BLOCKED-001/002 supprimés restent supprimés; rapport technique untracked conservé.\n\n## Acceptance\n- [x] Types, counts, hashes, mutants non-noop, raw/secret/binary guards.\n- [x] Export public-only sans build privé et compatibilité mêmes nodeids baseline.\n- [ ] Revue indépendante exacte.\n- [ ] Naturalité/hardware/gameplay non prouvés.\n\n## Handoff\nRE905: nouvel amont naturel séparément autorisé, pas répétition des contrôles X/Y/Z fermés.\n'
 prefix='../' if report else '../reverse/'
 return text+'[Metadata]('+prefix+'generated/re904-private-proof-publication-v1.json) · [Tracker]('+prefix+'generated/re904-private-proof-tracker-v1.csv) · [Dashboard]('+prefix+'tomb5-progress-dashboard-re904-v1.html).\n'
def render():
 d=validate(metadata());before=(ROOT/PRIOR_DASHBOARD).read_bytes()
 if digest(before)!=PRIOR_SHA or not before.endswith(b'</html>'):raise ValueError('exact RE901 predecessor required')
 out={STORY:document().encode(),REPORT:document(True).encode(),JSON_PATH:(json.dumps(d,indent=2,sort_keys=True)+'\n').encode(),DASHBOARD:before[:-7]+SECTION.encode()+b'</html>',MAINTAINED:maintained_before()[:-7]+SECTION.encode()+b'</html>'}
 stream=io.StringIO(newline='');w=csv.writer(stream,lineterminator='\n');w.writerow(['ticket','scope','fullraw_verdict','strict_verdict','review_verdict_sha256','integration','publication_review'])
 for row in d['archived_private_results']:w.writerow([row['ticket'],row['scope'],row['fullraw_verdict'],row['strict_verdict'],row['review_verdict_sha256'],'false',d['publication_review']])
 out[CSV_PATH]=stream.getvalue().encode()
 for p,b in out.items():guard_output(p,b)
 return out
def original_compatibility(path,text):
 if path=='tests/reverse/test_re830_table_provenance_publication.py' and '# RE906 exact authenticated successor' in text:
  import runpy
  text=runpy.run_path(str(ROOT/'scripts/reverse/re906_publication.py'))['original_compatibility'](path,text)
 if '# RE909 exact authenticated successor' in text:
  import runpy
  text=runpy.run_path(str(ROOT/'scripts/reverse/re909_publication.py'))['original_compatibility'](path,text)
 spec=COMPATIBILITY_DELTAS[path]
 for old,new in reversed(spec['replacements']):
  if text.count(new)!=1:raise ValueError('exact RE904 compatibility adapter required')
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
 print('RE904 PUBLIC_METADATA_TESTS_ONLY PASS; exact-public-hash independent review PENDING')
if __name__=='__main__':
 argparse.ArgumentParser(description=__doc__).parse_args();check()
