"""RE923 portable metadata publication; no private runtime dependency."""
import argparse,copy,csv,hashlib,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PRIOR_DASHBOARD='docs/reverse/tomb5-progress-dashboard-re921-v1.html'
PRIOR_MAINTAINED='docs/reverse/tomb5-progress-dashboard-maintained-re921-v1.html'
DASHBOARD='docs/reverse/tomb5-progress-dashboard-re923-v1.html'
MAINTAINED='docs/reverse/tomb5-progress-dashboard.html'
STORY='docs/stories/RE-923-irq-proof-publication.md'
REPORT='docs/reverse/functions/re923-irq-proof-publication.md'
JSON_PATH='docs/reverse/generated/re923-irq-proof-publication-v1.json'
CSV_PATH='docs/reverse/generated/re923-irq-proof-tracker-v1.csv'
PRIOR_SHA='ec7773c2ad450b63aad72c4501edaac522d7e9b1389690600a114f1ceda8923c'
MAINTAINED_SHA='4cf426329b18bae2300e3a5318d2a553feffdae2af013a2f4ee8138d4da0c52d'
EXPECTED={'schema': 're923-irq-proof-publication-v1', 'publication_review': 'PENDING_INDEPENDENT_EXACT_HASH_REVIEW', 'fresh_execution_scope': 'PUBLIC_METADATA_TESTS_ONLY', 'fresh_target': 0, 'fresh_native': 0, 'integration': False, 'production_patch': False, 'global_scope': 'FAIL', 'procedure_scope': 'FAIL', 'naturalcaller': 'BLOCKED', 'backend_boundary': 'RE922-PCsxRedux-IRQ-subset', 'authentication': {'re922-interrupt-mmio': {'members': 112, 'manifest_sha256': '3a7465def56d0074975152e05edd4d7807a23a84c0775d2503046156d72cc1c1', 'seal_sha256': '5d2b37d4687bf165ebeed2ee2c6605f059a05a8a9727ab9045193d13447707cf', 'verdict_sha256': '664b7958a7e55f24b5b898f71cc49c25a794e3d23ee32c0ea590320664a3aea5'}, 're922-review': {'members': 33, 'manifest_sha256': '3de2ba11543e9eb4b024d91d01494594bea2b5fb79fa4ebe6bcfc9014b41787f', 'seal_sha256': '3aaebf3bf4755877cf0142262299558689ab80e5da57b6d2d90694d29f4808a0', 'verdict_sha256': 'df7536d86a86a54319fe31f96e97497055fc91f87bdf604f531862cee03bf4c4'}, 're922-review-correction01': {'members': 52, 'manifest_sha256': '24b2c029fe1d8245f5b1db7551011d937baaa4e14e8e1532b1926af1292b5311', 'seal_sha256': 'da9aff76d26528770d632da03807bdbba46635e5fdde48d24e4e2b494448521c', 'verdict_sha256': 'd4cb2474e8aedc797d5d93c696188ad021529bd467a3d04779287037b5f9056e'}, 're922-review-correction02': {'members': 51, 'manifest_sha256': 'af7d3b786928465c1e6bd25f66b1f3946344b993b5129f62f4da1f241ddc980b', 'seal_sha256': '91c18368336e36b0055ab2b9ea30a35281cf5a7bd40c27208862df2ce820aa72', 'verdict_sha256': 'c563ea903c491596e665114e50b57edc7e5a0bf2563f4d4b54bfe489bc705e9d'}, 're922-review-clarification03': {'members': 11, 'manifest_sha256': 'cdea1d8078807c0e191bc59c5041e4e6c701f5d656851714e79378dc53fe36b0', 'seal_sha256': 'a84f53edc785d7c613b926f6f1c65fe69749f0f22e87e687b73719cb0b0c7c4b', 'verdict_sha256': 'b97f3ae3194b1a7a141f14e7b2351a4574e3d9dd9c513bad0260d3994b0ec23c'}}, 'attribution': {'project': 'PCSX-Redux / nugget OpenBIOS', 'license': 'GPL-2.0-or-later', 'OpenBIOS_license': 'MIT', 'pcsx_redux_commit': 'c313b116e6a55786bc127c9b3a07a90b55d97c21', 'nugget_commit': '7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30', 'copyright': 'Copyright (C) 2023 PCSX-Redux authors', 'source_url': 'https://github.com/pcsx-redux/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/psxhw.cc'}, 'archived_counts': {'retired': 1976495, 'visits': 1976496, 'mmio': 4, 'supported': 3, 'irq_ablation_retired_delta': 7, 'fresh_tests': 17, 'public_mmio_comparisons': 216, 'cp0_predicates': 20, 'fresh_continuous_runs': 3}, 'review_history': {'review': 'FAILED_RETAINED', 'correction01': 'FAILED_RETAINED', 'correction02': 'REJECTED_CONCERNS_NONEMPTY', 'prior_summary_false_claim': True, 'clarification03': 'SCOPED_PASS_ARCHIVE_ONLY', 'clarification03_new_numerical_runs': 0}, 'limitations': ['Global/procedure historiques FAIL conservés; integration=false.', 'ROM compilée héritée, non reconstruite; ABI/RAM construits, loads immédiats Unicorn, pas reset/Sony/CD/gameplay/hardware.', 'GPL-2.0-or-later psxhw/r3000a; OpenBIOS MIT; aucun ajout production.', 'Retirement mesuré par instruction terminée avant hook suivant, pas preuve microarchitecturale.'], 'frontier': 'DMA_DP_CR_32_UNSUPPORTED_ATTEMPT_NOT_RETIRED', 'active_irq': 'FAIL_CLOSED_REFUSED', 'oracle': {'whole_ram_bytes': 2097152, 'gpr': 32, 'ordered_pc': 1976496, 'mmio': 4, 'independent_decoder': True, 'hardware_oracle': False, 'independent_register_lanes': 32, 'fail_closed_controls': 50, 'executed_CP0_instructions': 0}}
COMPATIBILITY_DELTAS={'scripts/reverse/re921_publication.py': {'before_sha256': '35abd39e4986eaad9720c2bf2a926c82aa3210aa190d1e580d3ac18f318bc534', 'replacements': [('\ndef preceding_maintained(data):return inverse(data,MAINTAINED_SHA)', "\ndef preceding_maintained(data):\n if b'<!-- RE923 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re923_publication.py'))['preceding_maintained'](data)\n return inverse(data,MAINTAINED_SHA)\ndef read_maintained():\n data=(ROOT/MAINTAINED).read_bytes()\n if b'<!-- RE923 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re923_publication.py'))['preceding_maintained'](data)\n return data"), ("\n  if (ROOT/p).read_bytes()!=b:raise ValueError('generated drift '+p)", "\n  if (read_maintained() if p==MAINTAINED else (ROOT/p).read_bytes())!=b:raise ValueError('generated drift '+p)")]}, 'tests/reverse/test_re921_publication.py': {'before_sha256': '9a51f361d25408c506e5274c4bb2945486bea1c087c6e9987261a6d8b78bc843', 'replacements': [('for p,b in out.items():assert (ROOT/p).read_bytes()==b;m.guard_output(p,b)', 'for p,b in out.items():assert (m.read_maintained() if p==m.MAINTAINED else (ROOT/p).read_bytes())==b;m.guard_output(p,b)')]}}
SECTION='\n<!-- RE923 PUBLICATION BEGIN -->\n<section id="re923-publication-v1" data-integration="false"><h2>CURRENT RE923 — IRQ RE922 metadata</h2><p>RE922-PCsxRedux-IRQ-subset GPL-2.0-or-later / OpenBIOS MIT.1976495retired/1976496visits,3supported MMIO puis DMA_DP_CR32 tentative NONretirée. Retirement hook pas microarchitecture ; IRQactive failclosed. Correction02 REJECTED_CONCERNS_NONEMPTY, prior_summary_false_claim=true ; clarification03 distinct SCOPED_PASS_ARCHIVE_ONLY, ZERO new replay. BLOCKED reset/Sony/CD/hardware/gameplay ; ROM héritée ABI/RAM construits loads immédiats. Global FAIL/procedure FAIL/integration=false. PENDING_INDEPENDENT_EXACT_HASH_REVIEW.</p><p><a href="../stories/RE-923-irq-proof-publication.md">Story / acceptance</a> · <a href="functions/re923-irq-proof-publication.md">Evidence / blockers</a> · <a href="generated/re923-irq-proof-publication-v1.json">Status</a></p></section>\n<!-- RE923 PUBLICATION END -->\n'
DOC='# RE923 — publication metadata IRQ RE922\n\n## Progression\n- [x] Authentification complète size/SHA/seals et ensembles exacts112/33/52/51/11.\n- [x] TDD RED avant implémentation, tests metadata canonical/public-only.\n- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW ; worktree-only, aucun stage/commit/push.\n\n## Evidence\nRE922-PCsxRedux-IRQ-subset : références logicielles distinctes du hardware ; PCSX-Redux psxhw/r3000a GPL-2.0-or-later, OpenBIOS MIT. Copyright (C) 2023 PCSX-Redux authors (psxhw). Aucune source tierce redistribuée. Préfixe construit franchit I_MASK :1976495 instructions terminées,1976496 visites hook,4MMIO dont3supportés ; arrêt AVANT DMA_DP_CR écriture32bits non retirée. Retirement : instruction terminée avant hook suivant, pas microarchitecture. Producteur17tests216comparaisonsMMIO20prédicatsCPU ; reviewer compilation fraîche et3replays continus, oracle decoder indépendant RAM entière2097152octets32GPR1976496PC4MMIO,32lanes50failclosed. Ablation IRQ7retired supplémentaires. Aucun CP0 exécuté ;20prédicats distincts ne signifient pas20instructions CP0. A0 ablation peut atteindre jeu via B0 fallback ; pas preuve absence entrée.\n\n## Reviewhistory\nOriginal review et correction01 FAILED retenus. Correction02 passed=true mais quatre concerns NONEMPTY : REJECTED_CONCERNS_NONEMPTY ; prior_summary_false_claim=true, jamais rétroapprouvé. Clarification03 distincte SCOPED_PASS_ARCHIVE_ONLY, passed=true errors/concerns vides, zéro nouvelle replay numérique. Les quatre limitations originales sont conservées intégralement dans metadata. firstFAIL API/compile/braces et anciennes revues restent immuables.\n\n## Blockers\nActive IRQ fail-closed refusée : pas exception matérielle simulée universelle. ROM OpenBIOS héritée non recompilée RE922, ABI/RAM construits, loads immédiats Unicorn ; logiciel pas oracle hardware. Pas reset naturel, Sony BIOS/RA, CD, boot complet, gameplay ou intégration. Global FAIL/procedure FAIL historiques ; integration=false. BLOCKED-001/002 suppressions utilisateur, report/cache/assets/coldarchives/seals/RE893partial préservés. Frontière DMA_DP_CR non supportée ne reçoit aucune valeur succès fabriquée.\n\n## Acceptance\n- [x] Schéma exact récursif, mutants, guards metadata-only, inverse suffixe exact et adapters historiques hash-authentifiés.\n- [x] ZERO fresh target/native : seulement tests metadata, aucun replay numérique.\n- [ ] Revue indépendante exacte requise ; publication PASS ne vaut pas intégration.\n\n## Next\nRE924 : modèle DMA cohérent depuis références libres, preuve bornée séparée, pas production autorisée.\n'
OUTPUT_PATHS=(STORY,REPORT,JSON_PATH,CSV_PATH,DASHBOARD,MAINTAINED)
PUBLIC_PATHS=OUTPUT_PATHS+(PRIOR_MAINTAINED,"scripts/reverse/re923_publication.py","tests/reverse/test_re923_publication.py")+tuple(COMPATIBILITY_DELTAS)
def metadata():return copy.deepcopy(EXPECTED)
def validate(data):
 def exact(a,b):
  if type(a) is not type(b):return False
  if isinstance(b,dict):return set(a)==set(b) and all(exact(a[k],b[k]) for k in b)
  if isinstance(b,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
  return a==b
 if not exact(data,EXPECTED):raise ValueError('exact RE923 recursive schema types/counts/hash/scope required')
 return data
def digest(b):return hashlib.sha256(b).hexdigest()
def inverse(data,sha):
 suffix=SECTION.encode()+b'</html>'
 if not data.endswith(suffix) or data.count(b'<!-- RE923 PUBLICATION BEGIN -->')!=1 or data.count(b'<!-- RE923 PUBLICATION END -->')!=1:raise ValueError('exact unique RE923 suffix required')
 before=data[:-len(suffix)]+b'</html>'
 if digest(before)!=sha:raise ValueError('exact predecessor bytes changed')
 return before
def preceding_dashboard(data):return inverse(data,PRIOR_SHA)
def preceding_maintained(data):
 if b'<!-- RE925 PUBLICATION' in data:
  import runpy
  data=runpy.run_path(str(ROOT/'scripts/reverse/re925_publication.py'))['preceding_maintained'](data)
 return inverse(data,MAINTAINED_SHA)
def read_maintained():
 data=(ROOT/MAINTAINED).read_bytes()
 if b'<!-- RE925 PUBLICATION' in data:
  import runpy
  data=runpy.run_path(str(ROOT/'scripts/reverse/re925_publication.py'))['preceding_maintained'](data)
 return data
def maintained_before():
 b=(ROOT/PRIOR_MAINTAINED).read_bytes()
 if digest(b)!=MAINTAINED_SHA:raise ValueError('maintained historical fixture drift')
 return b

RAW=re.compile(rb'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|raw_opcode|raw_pc|register_values|target_address|payload_offset|data:image|```(?:asm|mips|cpp|c)\b',re.I)
SECRET=re.compile(rb'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|(?:api[_-]?key|password|secret)\s*[:=]\s*[\"\x27][^\"\x27\s]{12,}',re.I)
def guard_added(path,payload):
 p=Path(path)
 if p.is_absolute() or '..' in p.parts or path not in PUBLIC_PATHS:raise ValueError('outside explicit RE923 public scope')
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
 for ticket,status in [('RE922','PRIVATE_IRQ_FINITE_SCOPED_ACCEPTED'),('RE923','PUBLIC_METADATA_TESTS_ONLY')]:w.writerow([ticket,'archived proof' if ticket!='RE923' else 'fresh metadata',status,'false',d['publication_review']])
 out[CSV_PATH]=stream.getvalue().encode()
 for p,b in out.items():guard_output(p,b)
 return out
def original_compatibility(path,text):
 spec=COMPATIBILITY_DELTAS[path]
 for old,new in reversed(spec['replacements']):
  if text.count(new)!=1:raise ValueError('exact RE923 compatibility adapter required')
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
 print('RE923 PUBLIC_METADATA_TESTS_ONLY PASS; exact-public-hash independent review PENDING')
if __name__=='__main__':
 argparse.ArgumentParser(description=__doc__).parse_args();check()
