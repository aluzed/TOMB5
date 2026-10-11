"""RE906 portable safe metadata only; no private dependencies."""
import argparse,copy,csv,hashlib,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PRIOR_DASHBOARD='docs/reverse/tomb5-progress-dashboard-re904-v1.html'
PRIOR_MAINTAINED='docs/reverse/tomb5-progress-dashboard-maintained-re904-v1.html'
DASHBOARD='docs/reverse/tomb5-progress-dashboard-re906-v1.html'
MAINTAINED='docs/reverse/tomb5-progress-dashboard.html'
STORY='docs/stories/RE-906-upstream-prefix-publication.md'
REPORT='docs/reverse/functions/re906-upstream-prefix-publication.md'
JSON_PATH='docs/reverse/generated/re906-upstream-prefix-publication-v1.json'
CSV_PATH='docs/reverse/generated/re906-upstream-prefix-tracker-v1.csv'
PRIOR_SHA='4378dc09906c3f53911d36c05ee020db901e242d813c40996295c4acf3b9db96'
MAINTAINED_SHA='8d556879fdfd3325c2fa8b85673af74fb57c90e8242c03466b393be1627608c1'
EXPECTED={'schema': 're906-upstream-prefix-publication-v1', 'publication_review': 'PENDING_INDEPENDENT_EXACT_HASH_REVIEW', 'fresh_execution_scope': 'PUBLIC_METADATA_TESTS_ONLY', 'fresh_target': 0, 'fresh_native': 0, 'integration': False, 'production_patch': False, 'public_helpers_green': False, 'global_scope': 'FAIL', 'procedure_scope': 'FAIL', 'naturalcaller': 'BLOCKED', 'normal_only': True, 'strict_sanitizers_executed': False, 'archived_loader_inputs': {'RE853': 49, 'RE855': 62, 'manifest_entries_total': 111, 'fresh_loaders': 0}, 'producer': {'target_prefixes': 7, 'accepted_prefixes': 4, 'unmodified_prefixes': 2, 'sensitive_mutants': 2, 'initial_failed_prefixes': 3, 'GetFrames_returns': 1, 'native_prefixes': 1, 'native_returns': 0, 'GetJointAbsPosition_calls': 0}, 'reviewer': {'target_prefixes': 6, 'accepted_prefixes': 4, 'failed_consumer_prefixes': 2, 'sensitive_mutants': 2, 'GetFrames_returns': 1, 'native_prefixes': 1, 'native_returns': 0, 'GetJointAbsPosition_calls': 0}, 'prefix': {'item': 128, 'object': 284, 'animation': 578, 'frame': 0, 'native_projection_bytes': 144, 'native_build': 'whole actual ITEMS.C i386 O0 normal', 'stop': 'before first suffix write; no InitialiseItem return'}, 'consumer': {'kind': 'explicit constructed arguments and return frontier in retained CPU/RAM; not natural caller', 'frame_windows': 2, 'bytes_each': 20, 'rate': 1, 'fraction': 0, 'frame_size': 10}, 'authentication': {'re905-upstream-provenance': {'seal_sha256': '7eba768c655c3cfe59cc95611766d0e9154332465ff79db1a79474e89a28f0db', 'manifest_sha256': 'dd1aa0c3d0f868d8b56422c10af59a16bc1991fecf0ed62ffdbf564dc17a700a', 'manifest_entries': 50, 'verdict_sha256': '8f371b405acbee95125df9cc8925e959fa08341f8a0a14844d8186e45223df8c'}, 're905-review': {'seal_sha256': 'af2e8dea14ae23f2ed2a9dbd236aab967cfd6d4af72e9fbef24def42616d9067', 'manifest_sha256': '5371df70d8a630be4615432d20cdaab64776014fafb61b379d21ca75419de1b4', 'manifest_entries': 55, 'verdict_sha256': '17c4841d7be2b7ff453d83b82e4e61063ecf5782530efc9f1a3dfa6ad0d0227c'}}, 'failures': ['initial insensitive frame-store NOP: frame0 already framebase0; retained and replaced by distinct sensitive mutant', 'producer and reviewer UC_ERR_EXCEPTION memory-write-hook failures retained; retry without hook; cause not diagnosed', 'two parent read-only schema failures retained; not technical results'], 'limits': 'archived loader inputs, fresh prefix normal-only; selected projection independent oracle, not whole RAM; zero native InitialiseItem return; no ASan/UBSan, natural caller, GetJointAbsPosition, startup, gameplay, hardware or global equivalence.', 'next_ticket': 'RE907', 'next_objective': 'real object284 registration/relocation then InitialiseItem continuation AddActiveItem room/floor/callback; ControlBlinker pos.x unassigned is unsafe hypothesis, not activation'}
COMPATIBILITY_DELTAS={'scripts/reverse/re904_publication.py': {'before_sha256': '496e5bd0145d1372ceb07a75d12f703cedb08d0333278d5de18a151ef0c9b011', 'replacements': [('def preceding_maintained(data):return inverse(data,MAINTAINED_SHA)', "def preceding_maintained(data):\n if b'<!-- RE906 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re906_publication.py'))['preceding_maintained'](data)\n return inverse(data,MAINTAINED_SHA)\ndef read_maintained():\n data=(ROOT/MAINTAINED).read_bytes()\n if b'<!-- RE906 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re906_publication.py'))['preceding_maintained'](data)\n return data"), ('def original_compatibility(path,text):\n', "def original_compatibility(path,text):\n if path=='tests/reverse/test_re830_table_provenance_publication.py' and '# RE906 exact authenticated successor' in text:\n  import runpy\n  text=runpy.run_path(str(ROOT/'scripts/reverse/re906_publication.py'))['original_compatibility'](path,text)\n"), ("\n  if (ROOT/p).read_bytes()!=b:raise ValueError('generated drift '+p)", "\n  if (read_maintained() if p==MAINTAINED else (ROOT/p).read_bytes())!=b:raise ValueError('generated drift '+p)")]}, 'tests/reverse/test_re904_publication.py': {'before_sha256': '1d8c764b5aca93f8aac4df2261e294484cc403b6fd90f2a17d59115d083660fc', 'replacements': [('for p,b in out.items():assert (ROOT/p).read_bytes()==b;m.guard_output(p,b)', 'for p,b in out.items():assert (m.read_maintained() if p==m.MAINTAINED else (ROOT/p).read_bytes())==b;m.guard_output(p,b)')]}, 'tests/reverse/test_re830_table_provenance_publication.py': {'before_sha256': '65c53f07e50c096272688ca2923bdfcb819c63fc43d7873576172317deddcd29', 'replacements': [('    # RE904 exact authenticated successor; preserve contiguous older adapters.\n', "    # RE906 exact authenticated successor; preserve contiguous older adapters.\n    if b'<!-- RE906 PUBLICATION' in data:\n        import runpy\n        try:\n            data = runpy.run_path(str(ROOT / 'scripts/reverse/re906_publication.py'))['preceding_maintained'](data)\n        except ValueError as exc:\n            raise AssertionError('invalid RE906 successor') from exc\n    # RE904 exact authenticated successor; preserve contiguous older adapters.\n")]}}
OUTPUT_PATHS=(STORY,REPORT,JSON_PATH,CSV_PATH,DASHBOARD,MAINTAINED)
PUBLIC_PATHS=OUTPUT_PATHS+(PRIOR_MAINTAINED,'scripts/reverse/re906_publication.py','tests/reverse/test_re906_publication.py','scripts/reverse/re904_publication.py','tests/reverse/test_re904_publication.py','tests/reverse/test_re830_table_provenance_publication.py')
SECTION='\n<!-- RE906 PUBLICATION BEGIN -->\n<section id="re906-publication-v1" data-integration="false"><h2>CURRENT RE906 — ARCHIVED RE905 genuine upstream prefix</h2><p>InitialiseItem item128/object284: animation578 frame0. Archived loaders111, zero fresh loader. Producer7 prefixes (4 accepted,3 firstFAIL); reviewer6 (4 accepted,2 failed consumer). Each:1 native normal-only prefix, ZERO InitialiseItem returns;1 explicitly constructed GetFrames return,2 windows20 bytes rate1 fraction0 frame size10. Retained CPU/RAM, not natural caller. No sanitizers.</p><p>Global FAIL / procedure FAIL / integration=false / naturalcaller BLOCKED. PENDING_INDEPENDENT_EXACT_HASH_REVIEW. Memory-write-hook exceptions and retries preserved, cause not diagnosed. No source activation or global equivalence. Next: registration/relocation object284 then continuation room/floor/callback.</p><p><a href="../stories/RE-906-upstream-prefix-publication.md">Story / acceptance</a> · <a href="functions/re906-upstream-prefix-publication.md">Evidence / limits</a> · <a href="generated/re906-upstream-prefix-publication-v1.json">Metadata</a> · <a href="generated/re906-upstream-prefix-tracker-v1.csv">Tracker</a>.</p></section>\n<!-- RE906 PUBLICATION END -->\n'
def metadata():return copy.deepcopy(EXPECTED)
def validate(data):
 def exact(a,b):
  if type(a) is not type(b):return False
  if isinstance(b,dict):return set(a)==set(b) and all(exact(a[k],b[k]) for k in b)
  if isinstance(b,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
  return a==b
 if not exact(data,EXPECTED):raise ValueError('exact RE906 recursive schema types/counts/hash/scope required')
 return data
def digest(b):return hashlib.sha256(b).hexdigest()
def inverse(data,sha):
 suffix=SECTION.encode()+b'</html>'
 if not data.endswith(suffix) or data.count(b'<!-- RE906 PUBLICATION BEGIN -->')!=1 or data.count(b'<!-- RE906 PUBLICATION END -->')!=1:raise ValueError('exact unique RE906 suffix required')
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
 if p.is_absolute() or '..' in p.parts or path not in PUBLIC_PATHS:raise ValueError('outside explicit RE906 public scope')
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
 text='# RE906 — publication sûre RE905 metadata-only\n\n## Progression\n- [x] RED discriminant avant générateur, GREEN metadata seulement.\n- [x] Seals/verdicts sélectionnés authentifiés; inventories parent, pas replay frais.\n- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW.\n\n## Evidence\n'+json.dumps(EXPECTED,indent=2,sort_keys=True)+'\n\n## Blockers\nintegration=false; global FAIL / procédure FAIL; naturalcaller BLOCKED.\nfirstFAIL et retries immuables: causalité hook non diagnostiquée. Animation antérieure0 incompatible corrigée par préfixe authentique578, pas activation source.\nBLOCKED-001/002 restent supprimés, rapport technique untracked conservé.\n\n## Acceptance\n- [x] Schéma exact types/comptes/hash, inverse append RE904 strict.\n- [x] Gardes contenu/path sur même chemin permis, export public-only.\n- [ ] Revue indépendante exacte publique.\n- [ ] Naturalité, suffixe InitialiseItem, sanitizers et équivalence globale non prouvés.\n\n## Handoff\n'+EXPECTED['next_objective']+'\n'
 return text
def render():
 d=validate(metadata());before=(ROOT/PRIOR_DASHBOARD).read_bytes()
 if digest(before)!=PRIOR_SHA or not before.endswith(b'</html>'):raise ValueError('exact RE904 predecessor required')
 out={STORY:document().encode(),REPORT:document(True).encode(),JSON_PATH:(json.dumps(d,indent=2,sort_keys=True)+'\n').encode(),DASHBOARD:before[:-7]+SECTION.encode()+b'</html>',MAINTAINED:maintained_before()[:-7]+SECTION.encode()+b'</html>'}
 stream=io.StringIO(newline='');w=csv.writer(stream,lineterminator='\n');w.writerow(['ticket','role','target_prefixes','GetFrames_returns','native_prefixes','native_returns','integration','publication_review'])
 for role in ('producer','reviewer'):
  row=d[role];w.writerow(['RE905',role,row['target_prefixes'],row['GetFrames_returns'],row['native_prefixes'],row['native_returns'],'false',d['publication_review']])
 out[CSV_PATH]=stream.getvalue().encode()
 for p,b in out.items():guard_output(p,b)
 return out
def original_compatibility(path,text):
 spec=COMPATIBILITY_DELTAS[path]
 for old,new in reversed(spec['replacements']):
  if text.count(new)!=1:raise ValueError('exact RE906 compatibility adapter required')
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
 print('RE906 PUBLIC_METADATA_TESTS_ONLY PASS; exact-public-hash independent review PENDING')
if __name__=='__main__':
 argparse.ArgumentParser(description=__doc__).parse_args();check()
