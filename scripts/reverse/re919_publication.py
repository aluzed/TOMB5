"""RE919 portable metadata publication; no private runtime dependency."""
import argparse,copy,csv,hashlib,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PRIOR_DASHBOARD='docs/reverse/tomb5-progress-dashboard-re917-v1.html'
PRIOR_MAINTAINED='docs/reverse/tomb5-progress-dashboard-maintained-re917-v1.html'
DASHBOARD='docs/reverse/tomb5-progress-dashboard-re919-v1.html'
MAINTAINED='docs/reverse/tomb5-progress-dashboard.html'
STORY='docs/stories/RE-919-openbios-executable-proof-publication.md'
REPORT='docs/reverse/functions/re919-openbios-executable-proof-publication.md'
JSON_PATH='docs/reverse/generated/re919-openbios-executable-proof-publication-v1.json'
CSV_PATH='docs/reverse/generated/re919-openbios-executable-proof-tracker-v1.csv'
PRIOR_SHA='24dbf50114a499469c9674820a3a2ba15aa903ae04d0f94f69023f9d82885f98'
MAINTAINED_SHA='2eef47f2fa0983c80068f846110857ae83bb67bda8eb04eb3b927d4b34ad315f'
EXPECTED={'schema': 're919-openbios-executable-proof-publication-v1', 'publication_review': 'PENDING_INDEPENDENT_EXACT_HASH_REVIEW', 'fresh_execution_scope': 'PUBLIC_METADATA_TESTS_ONLY', 'fresh_target': 0, 'fresh_native': 0, 'integration': False, 'production_patch': False, 'global_scope': 'FAIL', 'procedure_scope': 'FAIL', 'naturalcaller': 'BLOCKED', 'backend_boundary': 'OPENBIOS_REPLACEMENT_NOT_SONY_BIOS', 'authentication_scope': 'Publisher freshly authenticated both complete private92-member inventories; parent earlier verified same roots. No numerical replay.', 'authentication': {'re918-openbios': {'entries': 92, 'manifest_sha256': '093dc01dadd97038aef080264f77aac05e1607d2ca3bbb07330a4f78e912142a', 'seal_file_sha256': 'a47cb98851a0e28b9da66f8a097158f82bd26fed03ddb936856985e0e38ba591', 'verdict_sha256': '342348ea06fa915a2f1a78e0f5350178f53c452cb5f290b0fe529b7218e3f46a'}, 're918-review': {'entries': 92, 'manifest_sha256': '09095261de2d785f41787f8ef93d214cbdf83300b64459c9b867b5744f605d9e', 'seal_file_sha256': 'dfac3c0fa6b4f24add8273edccf8975fa2f851ad3388672ad207a1c1160a0d70', 'verdict_sha256': 'f6f2321435d75b9ef95c9243b123f83f877d1903ffbbd48318eb365aceea336d'}}, 'attribution': {'project': 'PCSX-Redux / nugget OpenBIOS', 'license': 'MIT', 'copyright': ['Copyright (c) 2020 PCSX-Redux authors'], 'source_path': 'src/mips/openbios/kernel/psxexec.s', 'source_sha256': 'baa154b1eb86343f1fd468b17f46dab155fb836e023ca2d4eeedce2c3c73ef8c', 'source_unchanged': True, 'redux_commit': 'c313b116e6a55786bc127c9b3a07a90b55d97c21', 'nugget_commit': '7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30', 'source_url': 'https://github.com/pcsx-redux/nugget/blob/7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30/openbios/kernel/psxexec.s', 'redistributed_source': False}, 'RE918': {'accepted_scope': 'PRIVATE_OPENBIOS_ROUNDTRIP_AND_AUTHENTIC_GAME_RA_SAVE', 'producer': {'roundtrips': 4, 'code_mutants_rejected': 4, 'game_entry_prefixes': 2, 'game_target_visits': 1778397, 'independent_game_cpu_prefixes': 1, 'whole_ram_bytes_compared': 2097152, 'gpr_compared': 32, 'game_positive_prefixes': 1, 'game_code_mutants_rejected': 1, 'game_mutant_target_visits': 1778397}, 'reviewer': {'roundtrips': 4, 'code_mutants_rejected': 4, 'game_entry_prefixes': 2, 'game_target_visits': 1778397, 'independent_game_cpu_prefixes': 1, 'whole_ram_bytes_compared': 2097152, 'gpr_compared': 32, 'game_positive_prefixes': 1, 'game_code_mutants_rejected': 1, 'game_mutant_target_visits': 1778397}, 'timing': {'producer_game_seconds': 5.583026170730591, 'reviewer_closure_seconds': 328.76693964004517}, 'frontier': 'Constructed ABI caller -> unchanged MIT exec assembled ELF MIPS-I -> authentic game entry -> SW RA via AT executed -> immediate stop. Replacement backend RA, not Sony RA.', 'oracle': 'Independent stdlib reconstruction from ISO and fresh binaries; full ordered visits, final RAM and32GPR. Software comparison, not hardware.', 'limits': ['Four synthetic ABI domains: BSS empty/nonempty and selected/unselected stack; not complete ABI.', 'Each game_entry_prefixes=2 means ONE positive and ONE actual link mutant, not two positives.', 'Independent CPU positive counts are separate comparisons, not extra game target positives.', 'Constructed BIOS caller and initial RAM outside payload; no natural full boot, SDK return, CD success sector, gameplay or integration.', 'MIPS32 Unicorn immediate loads; no R3000 load-delay certification.', 'Synthetic RETURN fixture is not game return; real game stop immediately after RA store.'], 'firstFAIL': ['Producer KSEG API physical-memory access error preserved; retry keeps CPU KSEG addresses.', 'Reviewer BOOT parser firstFAIL preserved; corrected parser retry distinct.', 'Historical global/procedure FAIL not rehabilitated.']}}
COMPATIBILITY_DELTAS={'scripts/reverse/re917_publication.py': {'before_sha256': '81118cbec0d365b2c62e10788de39b61fe85f8a48ed5ff65dec9a3957fb6b3b1', 'replacements': [('\ndef preceding_maintained(data):return inverse(data,MAINTAINED_SHA)', "\ndef preceding_maintained(data):\n if b'<!-- RE919 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re919_publication.py'))['preceding_maintained'](data)\n return inverse(data,MAINTAINED_SHA)\ndef read_maintained():\n data=(ROOT/MAINTAINED).read_bytes()\n if b'<!-- RE919 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re919_publication.py'))['preceding_maintained'](data)\n return data"), ("\n  if (ROOT/p).read_bytes()!=b:raise ValueError('generated drift '+p)", "\n  if (read_maintained() if p==MAINTAINED else (ROOT/p).read_bytes())!=b:raise ValueError('generated drift '+p)")]}, 'tests/reverse/test_re917_publication.py': {'before_sha256': 'c938b53aeea25a8953102c43b18a0b231d132e06da9f9ad4a29d5e138692cb1f', 'replacements': [('for p,b in out.items():assert (ROOT/p).read_bytes()==b;m.guard_output(p,b)', 'for p,b in out.items():assert (m.read_maintained() if p==m.MAINTAINED else (ROOT/p).read_bytes())==b;m.guard_output(p,b)')]}}
SECTION='\n<!-- RE919 PUBLICATION BEGIN -->\n<section id="re919-publication-v1" data-integration="false"><h2>CURRENT RE919 — preuve exécutable OpenBIOS RE918 / publication metadata</h2><p>PCSX-Redux / nugget MIT unchanged psxexec.s ELF MIPS-I. OPENBIOS_REPLACEMENT_NOT_SONY_BIOS. Producer/reviewer chacun4roundtrips4mutants, ONE positive game prefix + ONE link mutant ;1778397 ordered visits,2097152 RAM bytes32GPR indépendant. Caller ABI construit, vraie entrée jeu puis SW RA via AT exécuté ; arrêt immédiatement après. ZERO fresh target/native RE919.</p><p>Restant à faire : startup/CD du backend explicite. Sony RA UNKNOWN ; natural boot/gameplay/hardware/R3000 load delay nonprouvés. Functional naturalcaller BLOCKED/global FAIL/procedure FAIL/integration=false. firstFAIL KSEG et BOOT parser conservés. PENDING_INDEPENDENT_EXACT_HASH_REVIEW.</p><p><a href="../stories/RE-919-openbios-executable-proof-publication.md">Story / acceptance</a> · <a href="functions/re919-openbios-executable-proof-publication.md">Evidence / blockers</a> · <a href="generated/re919-openbios-executable-proof-publication-v1.json">Status</a></p></section>\n<!-- RE919 PUBLICATION END -->\n'
DOC="# RE919 — publication fidèle de la preuve exécutable OpenBIOS RE918\n\n## Progression\n- [x] RE918 privé accepté et inventaires producteur92 / reviewer92 authentifiés.\n- [x] Publication metadata TDD RED avant générateur, ZERO nouvelle exécution cible/native.\n- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW ; worktree-only, aucun stage/commit/push.\n\n## Evidence\nPCSX-Redux / nugget OpenBIOS, source MIT psxexec.s inchangée compilée ELF MIPS-I. Attribution source et pins ci-dessous ; aucun source tiers redistribué. Quatre aller-retours ABI synthétiques et quatre mutants exécutés par producteur et reviewer fresh. Une entrée authentique positive et un mutant link chacun, pas deux positives. Caller construit → backend compilé → véritable entrée jeu → SW RA via AT exécuté, arrêt immédiatement suivant. 1778397 visites ordonnées, RAM entière2097152 octets,32GPR comparés à un oracle stdlib indépendant reconstruit depuis ISO ; aucune nouvelle replay RE919.\n\n## Blockers\nOPENBIOS_REPLACEMENT_NOT_SONY_BIOS : RA Sony UNKNOWN. Backend de remplacement, caller et contexte initial construits. Pas de full natural boot, retour SDK positif, secteur CD succès, gameplay, hardware ni intégration. Unicorn MIPS32 avec loads immédiats, pas certification load-delay R3000. Quatre fixtures finies, pas totalité ABI ; RETURN synthétique n'est pas retour jeu. Global FAIL/procedure FAIL/integration=false. firstFAIL KSEG API producteur et BOOT parser reviewer préservés, retries distincts ; FAIL historiques non réhabilités. BLOCKED-001/002 suppressions utilisateur, report-tech, cache, assets et archives froides préservés ; firstFAIL893 intact.\n\n## Acceptance\n- [x] Schéma récursif exact types/valeurs/counts/timing/pins et inconnus rejetés.\n- [x] Guards contenu brut/secret/binaire avec benign sur même chemin admis.\n- [x] Story/tracker/evidence/blockers et dashboard versionné à suffixe exact ; inverse restitue prédécesseur byte-identique, sans réécriture de ses hashes.\n- [ ] Revue indépendante des hashes publics finaux ; metadata GREEN ne vaut pas intégration.\n\n## Restant à faire\nContinuer explicitement depuis ce backend de remplacement vers startup/CD sans oracle hardware imaginaire ni secteur/SDK positif fabriqué ; provenance Sony et boot complet restent ouverts.\n"
OUTPUT_PATHS=(STORY,REPORT,JSON_PATH,CSV_PATH,DASHBOARD,MAINTAINED)
PUBLIC_PATHS=OUTPUT_PATHS+(PRIOR_MAINTAINED,"scripts/reverse/re919_publication.py","tests/reverse/test_re919_publication.py")+tuple(COMPATIBILITY_DELTAS)
def metadata():return copy.deepcopy(EXPECTED)
def validate(data):
 def exact(a,b):
  if type(a) is not type(b):return False
  if isinstance(b,dict):return set(a)==set(b) and all(exact(a[k],b[k]) for k in b)
  if isinstance(b,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
  return a==b
 if not exact(data,EXPECTED):raise ValueError('exact RE919 recursive schema types/counts/hash/scope required')
 return data
def digest(b):return hashlib.sha256(b).hexdigest()
def inverse(data,sha):
 suffix=SECTION.encode()+b'</html>'
 if not data.endswith(suffix) or data.count(b'<!-- RE919 PUBLICATION BEGIN -->')!=1 or data.count(b'<!-- RE919 PUBLICATION END -->')!=1:raise ValueError('exact unique RE919 suffix required')
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
 if p.is_absolute() or '..' in p.parts or path not in PUBLIC_PATHS:raise ValueError('outside explicit RE919 public scope')
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
 for ticket,status in [('RE918','PRIVATE_OPENBIOS_EXECUTABLE_PROOF_ACCEPTED'),('RE919','PUBLIC_METADATA_TESTS_ONLY')]:w.writerow([ticket,'archived proof' if ticket!='RE919' else 'fresh metadata',status,'false',d['publication_review']])
 out[CSV_PATH]=stream.getvalue().encode()
 for p,b in out.items():guard_output(p,b)
 return out
def original_compatibility(path,text):
 spec=COMPATIBILITY_DELTAS[path]
 for old,new in reversed(spec['replacements']):
  if text.count(new)!=1:raise ValueError('exact RE919 compatibility adapter required')
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
 print('RE919 PUBLIC_METADATA_TESTS_ONLY PASS; exact-public-hash independent review PENDING')
if __name__=='__main__':
 argparse.ArgumentParser(description=__doc__).parse_args();check()
