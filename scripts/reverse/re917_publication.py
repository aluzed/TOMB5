"""RE917 metadata only portable publication; no private dependency."""
import argparse,copy,csv,hashlib,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PRIOR_DASHBOARD='docs/reverse/tomb5-progress-dashboard-re915-v1.html'
PRIOR_MAINTAINED='docs/reverse/tomb5-progress-dashboard-maintained-re915-v1.html'
DASHBOARD='docs/reverse/tomb5-progress-dashboard-re917-v1.html'
MAINTAINED='docs/reverse/tomb5-progress-dashboard.html'
STORY='docs/stories/RE-917-bios-exec-dependency-diagnostic-publication.md'
REPORT='docs/reverse/functions/re917-bios-exec-dependency-diagnostic-publication.md'
JSON_PATH='docs/reverse/generated/re917-bios-exec-dependency-diagnostic-publication-v1.json'
CSV_PATH='docs/reverse/generated/re917-bios-exec-dependency-diagnostic-tracker-v1.csv'
PRIOR_SHA='c579c3ece47a39440c7ec8103fa6b44920ec1853eb10164950ab758a31287d1c'
MAINTAINED_SHA='9960fe90b8d6fa271e4be0b1c1493d8568abc4bb05e58bad6eeb23edd8cb659b'
EXPECTED={'schema': 're917-bios-exec-dependency-diagnostic-publication-v1', 'publication_review': 'PENDING_INDEPENDENT_EXACT_HASH_REVIEW', 'fresh_execution_scope': 'PUBLIC_METADATA_TESTS_ONLY', 'fresh_target': 0, 'fresh_native': 0, 'integration': False, 'production_patch': False, 'global_scope': 'FAIL', 'procedure_scope': 'FAIL', 'naturalcaller': 'BLOCKED', 'authentication_scope': 'RE916 producer38 reviewer16 and RE914 producer17 exact sets sizes SHA seals freshly authenticated; zero replay', 'authentication': {'re916-bios-exec': {'entries': 38, 'manifest_sha256': 'd9fa461bff03d32c30374fd1dc6f53ac7c54afbe3e5803f606c822ef74a0dd6b', 'seal_sha256': '9b885e55672eb7453bac61eee5c5e6df5fc785035c2f5b61e7367668e4a293a5', 'verdict_sha256': 'ca0ffa82e9baba583fc3dcba29339c792ddf8646779b74725271a3001b407585'}, 're916-review': {'entries': 16, 'manifest_sha256': '6f4efda55f6dd392c81b862d219ab6cd277c416b53be98dccc660a38d50575b4', 'seal_sha256': '0424a3b20f96c126bef8e93be0357253f9330527049b27800e56a9e041a5be01', 'verdict_sha256': '61434fd898e98df40a81d7d9168834f308c952bdbd02a72b501a5fe1bffb6e17'}, 're914-startup-hardware-provenance': {'entries': 17, 'manifest_sha256': '355d7516262b1719ec6dcc47363523ecb1a2cc8cde00c9bbd9f8a0a981d3a614', 'seal_sha256': '6fa6f705d2b432661f28082cd637b404d484e17273933893612fcb0d8b6ff5c4', 'verdict_sha256': '61434fd898e98df40a81d7d9168834f308c952bdbd02a72b501a5fe1bffb6e17'}}, 'RE916': {'diagnostic': 'PASS_STRICT_STATIC_DEPENDENCY_ONLY', 'functional_passed': False, 'functional_GREEN': 0, 'consumer': {'operation': 'SW_RA_VIA_AT_NOT_SP', 'width_bytes': 4, 'RA': 'UNKNOWN', 'instruction_executed': False, 'BIOS_Exec_dispatcher': 'UNPROVEN', 'header_proves': 'PC_SP_GP_NOT_RA', 'raw_contract': 'PRIVATE_ONLY_NO_ADDRESS_OFFSET_OPCODE_PUBLIC'}, 'producer': {'historical_name_search_files': 320530, 'historical_size_search_files': 307294, 'size_candidates': 17, 'source_files': 210, 'hit_files': 2, 'Exec_LoadExec_stubs': 2, 'validator_mutants_rejected': 10, 'first_attempt_exit': 1, 'retry01_exit': 1, 'accepted_retry02_exit': 0}, 'reviewer': {'source_files_rescanned': 210, 'size_candidates_rehashed': 17, 'VRAM_candidates': 5, 'heap_candidates': 12, 'validator_mutants_rejected': 10, 'independent_contract_controls_rejected': 8, 'strict_passed': True, 'logic_errors': [], 'concerns': [], 'quoting_failure': 'BEFORE_CHECKER_PRESERVED'}, 'search_limit': 'BOUNDED_DECLARED_ROOTS_EXCLUSIONS_COLD_ARCHIVES_NOT_EXTRACTED_NOT_UNIVERSAL_ABSENCE', 'execution': {'fresh_CPU': 0, 'fresh_target': 0, 'fresh_native_build_run': 0, 'startup_replay': 0, 'RA_injection': 0, 'BIOS_SDK_return_double': 0, 'positive_sector_injection': 0, 'historical_RE914_visits': 1778375, 'historical_visits_not_fresh': True}, 'transport': {'producer_task_seconds': 368.39, 'producer_outer_seconds': 368.45, 'reviewer_task_seconds': 358.43, 'reviewer_outer_seconds': 358.48, 'source_readback_seconds': 360.32, 'distinct_origins': True}, 'next': 'Legitimate authenticated firmware with SHA model provenance boot chain OR authenticated POSTBIOS capture RA PC SP GP RAM boot chain; attribute dispatcher last RA producer before continuation; GPUSTAT Timer1 CD unresolved'}}
COMPATIBILITY_DELTAS={'scripts/reverse/re915_publication.py': {'before_sha256': '3f6a951e34737f0f468764f9f449845f6219418008ecf3afb637d9b037669eb9', 'replacements': [('\ndef preceding_maintained(data):return inverse(data,MAINTAINED_SHA)', "\ndef preceding_maintained(data):\n if b'<!-- RE917 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re917_publication.py'))['preceding_maintained'](data)\n return inverse(data,MAINTAINED_SHA)\ndef read_maintained():\n data=(ROOT/MAINTAINED).read_bytes()\n if b'<!-- RE917 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re917_publication.py'))['preceding_maintained'](data)\n return data"), ("\n  if (ROOT/p).read_bytes()!=b:raise ValueError('generated drift '+p)", "\n  if (read_maintained() if p==MAINTAINED else (ROOT/p).read_bytes())!=b:raise ValueError('generated drift '+p)")]}, 'tests/reverse/test_re915_publication.py': {'before_sha256': '76f1b2fddf7abd3dfa7fd48154e721deb75efa3b141b3d3b3ca3457ebf90491e', 'replacements': [('for p,b in out.items():assert (ROOT/p).read_bytes()==b;m.guard_output(p,b)', 'for p,b in out.items():assert (m.read_maintained() if p==m.MAINTAINED else (ROOT/p).read_bytes())==b;m.guard_output(p,b)')]}}
SECTION='\n<!-- RE917 PUBLICATION BEGIN -->\n<section id="re917-publication-v1" data-integration="false"><h2>CURRENT RE917 — RE916 BIOS Exec RA dependency diagnostic only</h2><p>SW RA via AT NOT SP, four-byte consumer; RA UNKNOWN, instruction NOT executed, BIOSExec UNPROVEN. Addresses offsets opcodes PRIVATE ONLY. Historical search320530names307294sizes17VRAMheap210sources2hitfiles2ExecLoadExecstubs. Independent reviewer210sources17rehashes10validator mutants8contract controls. Bounded scope NOT universal absence. Producer38/reviewer16/predecessor17 authenticated members. ZERO fresh CPU target native startup runtime.</p><p>Restant à faire : firmware légitime authentifié SHA modèle provenance boot OU capture POSTBIOS RA PC SP GP RAM boot ; attribuer dispatcher et dernière production RA avant continuation. GPUSTAT Timer1 CD unresolved. Functional naturalcaller BLOCKED/global FAIL/procedure FAIL/integration=false. FirstFAILs immutable; strict static diagnostic PASS only. PENDING_INDEPENDENT_EXACT_HASH_REVIEW.</p><p><a href="../stories/RE-917-bios-exec-dependency-diagnostic-publication.md">Story / acceptance</a> · <a href="functions/re917-bios-exec-dependency-diagnostic-publication.md">Evidence / blockers</a> · <a href="generated/re917-bios-exec-dependency-diagnostic-publication-v1.json">Status</a></p></section>\n<!-- RE917 PUBLICATION END -->\n'
DOC='# RE917 — publication du diagnostic de dépendance BIOS Exec / RA RE916\n\n## Progression\n- [x] Diagnostic statique strict RE916 authentifié, aucune nouvelle exécution numérique.\n- [x] RED/GREEN metadata portable, export public-only sans build/proof.\n- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW ; worktree-only, aucun stage/commit/push.\n\n## Evidence\nConsumer SW RA via AT, PAS SP ; largeur quatre octets. RA UNKNOWN et instruction NON exécutée. Contrat brut/adresse/déplacement/opcode restent privés. Le header authentifie PC/SP/GP mais ne fournit ni RA ni dispatcher BIOS Exec. Producteur : recherche historique320530 noms/307294 tailles,17 candidats VRAM/heap,210 sources,2 fichiers de hits et2 stubs Exec/LoadExec UNIMPLEMENTED return0. Reviewer indépendant :210 sources rescannées,17 rehashes (5VRAM/12heap),10 mutants validateur et8 contrôles contrat rejetés. Ces contrôles ne sont pas des exécutions cible. Authentification exhaustive38 membres RE916 producteur,16 reviewer,17 prédécesseur RE914 ; les55 membres predecessor reviewer sont38RE916+17RE914, distincts des16 artefacts de revue. ZERO CPU/target/native/startup/runtime nouveau ;1778375 visites RE914 historiques non recomptées.\n\n## Blockers\nFunctional/naturalcaller BLOCKED, global FAIL/procedure FAIL/integration=false. BIOSExec UNPROVEN ; absence locale bornée NON universelle, archives froides non extraites. Deux firstFAIL exit1 immuables (Unicorn absent puis hypothèse SP incorrecte), retry02 exit0 conservé ; reviewer quotingfailure avant checker conservé. Original author review PENDING immuable, revue externe stricte statique seulement, pas behavioral GREEN ni procédure historique réhabilitée. GPUSTAT/Timer1/CD non résolus. Producer368.39task368.45outer/reviewer358.43task358.48outer/source readback360.32 origines distinctes. BLOCKED-001/002 user deletes/report-tech/cache/assets/archives préservés.\n\n## Acceptance\n- [x] Schema récursif strict types/scalars/counts/pins, mutations négatives et benign même chemin.\n- [x] Dashboard versionné restant-à-faire et inverse exact RE915, hashes historiques inchangés.\n- [x] Public-only et compat baseline mêmes nodeids RE830 ; pas global GREEN.\n- [ ] Revue indépendante exacte des11 hashes publics PENDING.\n\n## Next — prérequis authentique uniquement\nFirmware légitimement disponible avec SHA/modèle/version/provenance/boot, OU capture POSTBIOS authentifiée RA/PC/SP/GP/RAM/boot. Attribuer vrai dispatcher et dernière production RA avant continuation ; aucun RA arbitraire, faux retour BIOS/SDK ou secteur positif. Cette publication ne lance ni recherche successeur, ni runtime, ni productionpatch.\n'
OUTPUT_PATHS=(STORY,REPORT,JSON_PATH,CSV_PATH,DASHBOARD,MAINTAINED)
PUBLIC_PATHS=OUTPUT_PATHS+(PRIOR_MAINTAINED,"scripts/reverse/re917_publication.py","tests/reverse/test_re917_publication.py")+tuple(COMPATIBILITY_DELTAS)
def metadata():return copy.deepcopy(EXPECTED)
def validate(data):
 def exact(a,b):
  if type(a) is not type(b):return False
  if isinstance(b,dict):return set(a)==set(b) and all(exact(a[k],b[k]) for k in b)
  if isinstance(b,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
  return a==b
 if not exact(data,EXPECTED):raise ValueError('exact RE917 recursive schema types/counts/hash/scope required')
 return data
def digest(b):return hashlib.sha256(b).hexdigest()
def inverse(data,sha):
 suffix=SECTION.encode()+b'</html>'
 if not data.endswith(suffix) or data.count(b'<!-- RE917 PUBLICATION BEGIN -->')!=1 or data.count(b'<!-- RE917 PUBLICATION END -->')!=1:raise ValueError('exact unique RE917 suffix required')
 before=data[:-len(suffix)]+b'</html>'
 if digest(before)!=sha:raise ValueError('exact predecessor bytes changed')
 return before
def preceding_dashboard(data):return inverse(data,PRIOR_SHA)
def preceding_maintained(data):
 if b'<!-- RE919 PUBLICATION' in data:
  import runpy
  data=runpy.run_path(str(ROOT/'scripts/reverse/re919_publication.py'))['preceding_maintained'](data)
 return inverse(data,MAINTAINED_SHA)
def read_maintained():
 data=(ROOT/MAINTAINED).read_bytes()
 if b'<!-- RE919 PUBLICATION' in data:
  import runpy
  data=runpy.run_path(str(ROOT/'scripts/reverse/re919_publication.py'))['preceding_maintained'](data)
 return data
def maintained_before():
 b=(ROOT/PRIOR_MAINTAINED).read_bytes()
 if digest(b)!=MAINTAINED_SHA:raise ValueError('maintained historical fixture drift')
 return b

RAW=re.compile(rb'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|raw_opcode|raw_pc|register_values|target_address|payload_offset|data:image|```(?:asm|mips|cpp|c)\b',re.I)
SECRET=re.compile(rb'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|(?:api[_-]?key|password|secret)\s*[:=]\s*[\"\x27][^\"\x27\s]{12,}',re.I)
def guard_added(path,payload):
 p=Path(path)
 if p.is_absolute() or '..' in p.parts or path not in PUBLIC_PATHS:raise ValueError('outside explicit RE917 public scope')
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
 if digest(before)!=PRIOR_SHA or not before.endswith(b'</html>'):raise ValueError('exact RE915 predecessor required')
 out={STORY:document().encode(),REPORT:document(True).encode(),JSON_PATH:(json.dumps(d,indent=2,sort_keys=True)+'\n').encode(),DASHBOARD:before[:-7]+SECTION.encode()+b'</html>',MAINTAINED:maintained_before()[:-7]+SECTION.encode()+b'</html>'}
 stream=io.StringIO(newline='');w=csv.writer(stream,lineterminator='\n');w.writerow(['ticket','scope','status','integration','publication_review'])
 for ticket,status in [('RE916','DIAGNOSTIC_PASS_FUNCTIONAL_BLOCKED_SDK'),('RE917','PUBLIC_METADATA_TESTS_ONLY')]:w.writerow([ticket,'archived proof' if ticket!='RE917' else 'fresh metadata',status,'false',d['publication_review']])
 out[CSV_PATH]=stream.getvalue().encode()
 for p,b in out.items():guard_output(p,b)
 return out
def original_compatibility(path,text):
 spec=COMPATIBILITY_DELTAS[path]
 for old,new in reversed(spec['replacements']):
  if text.count(new)!=1:raise ValueError('exact RE917 compatibility adapter required')
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
 print('RE917 PUBLIC_METADATA_TESTS_ONLY PASS; exact-public-hash independent review PENDING')
if __name__=='__main__':
 argparse.ArgumentParser(description=__doc__).parse_args();check()
