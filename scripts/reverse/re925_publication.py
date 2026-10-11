"""RE925 portable metadata publication; no private runtime dependency."""
import argparse,copy,csv,hashlib,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PRIOR_DASHBOARD='docs/reverse/tomb5-progress-dashboard-re923-v1.html'
PRIOR_MAINTAINED='docs/reverse/tomb5-progress-dashboard-maintained-re923-v1.html'
DASHBOARD='docs/reverse/tomb5-progress-dashboard-re925-v1.html'
MAINTAINED='docs/reverse/tomb5-progress-dashboard.html'
STORY='docs/stories/RE-925-dma-proof-publication.md'
REPORT='docs/reverse/functions/re925-dma-proof-publication.md'
JSON_PATH='docs/reverse/generated/re925-dma-proof-publication-v1.json'
CSV_PATH='docs/reverse/generated/re925-dma-proof-tracker-v1.csv'
PRIOR_SHA='5971629c88d40bc94e330a842f480a0104a44bc0328e2601b4efc90725cdfd2a'
MAINTAINED_SHA='91ef9d2f51ac210f7224a57677cb6439fbac18471202a8d49e20f744798c6c3e'
EXPECTED={'schema': 're925-dma-proof-publication-v1', 'publication_review': 'PENDING_INDEPENDENT_EXACT_HASH_REVIEW', 'fresh_execution_scope': 'PUBLIC_METADATA_TESTS_ONLY', 'fresh_target': 0, 'fresh_native': 0, 'integration': False, 'production_patch': False, 'global_scope': 'FAIL', 'procedure_scope': 'FAIL', 'naturalcaller': 'BLOCKED', 'backend_boundary': 'RE924-PCSX-Redux-DPCR-DICR-subset', 'authentication': {'re924-dma-mmio': {'members': 85, 'manifest_sha256': 'c425623ea296d3700c125d8cbe0adc104f7694ae13f04c0ed6c9f1417fcc464a', 'seal_sha256': 'fab8b8b58f8312cc1578701ab1803a79610a1398846b083b822896e74f516a56', 'verdict_sha256': '820e97617b44de7b83797d2a006d88b8d7591f95f80d29b29fd719bffc34e3ee', 'exactset_all_sizes_hashes': True}, 're924-review': {'members': 70, 'manifest_sha256': '555c64baa95f28115235e5b5a9b73a0a65e8998531b39b00f45293f28769d823', 'seal_sha256': 'a99abe186b996e5cad9acd8e09c96b4b878f985aecdc9e2800c8c61ffd79bd77', 'verdict_sha256': '561a877c4ab57ddd94979db3f090ffcc5799578f0f8abe437f25171808246c72', 'exactset_all_sizes_hashes': True}, 're924-review-scope-clarification01': {'members': 7, 'manifest_sha256': '8ef0f29125e4306d196d1e664576df7610b1f85c04a9afa3de8851dfcabb4e11', 'seal_sha256': '39e44a8df73d8d757f1a9ffc3dfdff2ef6cbe4cc12a256606b450973b4e28b45', 'verdict_sha256': 'b97f3ae3194b1a7a141f14e7b2351a4574e3d9dd9c513bad0260d3994b0ec23c', 'exactset_all_sizes_hashes': True}}, 'attribution': {'project': 'PCSX-Redux / nugget OpenBIOS', 'license': 'GPL-2.0-or-later', 'OpenBIOS_license': 'MIT', 'pcsx_commit': 'c313b116e6a55786bc127c9b3a07a90b55d97c21', 'openbios_commit': '7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30', 'sources': [{'path': 'src/core/psxhw.cc', 'url': 'https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/psxhw.cc', 'sha256': 'db7fbff756774848150fa1acf0e7c04c3bd2c5a87e3b4aacffcacd88e21388de', 'copyright': 'Copyright (C) 2023 PCSX-Redux authors', 'license': 'GPL-2.0-or-later'}, {'path': 'src/core/psxmem.h', 'url': 'https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/psxmem.h', 'sha256': '9e5658aeeef2f01af73a80f892f5e345fadee35c83d2f220daeafb40409fe6a0', 'copyright': 'Copyright (C) 2023 PCSX-Redux authors', 'license': 'GPL-2.0-or-later'}], 'third_party_source_redistributed': False}, 'archived_counts': {'retired': 1980769, 'visits': 1980770, 'additional_completed': 4274, 'resume_completed': 4274, 'resume_visits': 4275, 'mmio_attempts': 5, 'supported_mmio': 4, 'supported_dma': 1, 'whole_ram_bytes': 2097152, 'gpr': 32, 'ordered_pc': 1980770, 'producer_methods': 11, 'producer_DICR_comparisons': 45, 'reviewer_DICR_comparisons': 45, 'reviewer_seeded_comparisons': 2048, 'reviewer_width_alias_cases': 54, 'reviewer_atomic_rejections': 4}, 'review_history': {'original': 'REJECTED', 'original_passed': False, 'original_concerns': ['Incidents reviewer conservés : import initial FAIL corrigé par invocation distincte; branche DICR inutilisée du decoder initial rejetée puis corrigée et réexécutée distinctement. Aucun rejet initial rétrocertifié.', 'Procédure globale historique FAIL conservée : incidents antérieurs et discovery-ledger non exhaustif ne sont pas rétrocertifiés par cette revue fraîche.'], 'clarification01': 'SCOPED_PASS_ARCHIVE_ONLY', 'clarification_new_replays': 0, 'firstFAIL': 'producer tests and reviewer import/decoder failures retained, corrected invocations distinct'}, 'limitations': ['natural reset boot', 'hardware equivalence', 'DMA channel transfers/scheduling', 'active CPU exception delivery', 'load delays/cache', 'timer semantics after stopping frontier', 'CD sectors', 'gameplay', 'production integration', 'DICR seulement construit; jamais traversé naturellement', 'ROM réutilisée, aucun build firmware frais', 'witness extrait/adapté, pas build complet PCSX-Redux', 'ABI/RAM/caller construits; pas boot reset naturel', 'comparaisons indépendantes du trajet, pas preuve universelle du decoder ni de toutes branches', 'aucune certification exhaustive des découvertes/transactions historiques', 'aucune publication, mutation git, jobs ou production'], 'dicr_natural': False, 'rom_fresh_build': False, 'frontier': 'SDK_TIMER1_MODE_write32_BEFORE_EFFECT', 'returned_services': ['A0:13', 'B0:19'], 'retirement': 'previous instruction completed at next code hook; not microarchitectural retirement', 'oracle': 'fresh independent reviewer decoder full RAM/GPR/ordered PC/MMIO; finite software not hardware'}
COMPATIBILITY_DELTAS={'scripts/reverse/re923_publication.py': {'before_sha256': 'bcf8bdbc0c25a0181a734999515c398e303cd019c43f4413335ad5ef9e1e590e', 'replacements': [('\ndef preceding_maintained(data):return inverse(data,MAINTAINED_SHA)', "\ndef preceding_maintained(data):\n if b'<!-- RE925 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re925_publication.py'))['preceding_maintained'](data)\n return inverse(data,MAINTAINED_SHA)\ndef read_maintained():\n data=(ROOT/MAINTAINED).read_bytes()\n if b'<!-- RE925 PUBLICATION' in data:\n  import runpy\n  data=runpy.run_path(str(ROOT/'scripts/reverse/re925_publication.py'))['preceding_maintained'](data)\n return data"), ("\n  if (ROOT/p).read_bytes()!=b:raise ValueError('generated drift '+p)", "\n  if (read_maintained() if p==MAINTAINED else (ROOT/p).read_bytes())!=b:raise ValueError('generated drift '+p)")]}, 'tests/reverse/test_re923_publication.py': {'before_sha256': 'e3ed7ec7c641f99561f2fa771d85728b4ae123109ef016e9229bb7aa1f79a0f8', 'replacements': [('for p,b in out.items():assert (ROOT/p).read_bytes()==b;m.guard_output(p,b)', 'for p,b in out.items():assert (m.read_maintained() if p==m.MAINTAINED else (ROOT/p).read_bytes())==b;m.guard_output(p,b)')]}}
SECTION='\n<!-- RE925 PUBLICATION BEGIN -->\n<section id="re925-publication-v1" data-integration="false"><h2>CURRENT RE925 — DMA RE924 metadata</h2><p>RE924 DPCR franchi ; A0:13 et B0:19 retournent. 1980769 completed/1980770 visits ; arrêt AVANT Timer1 MODE write32. DICR construit seulement, ROM réutilisée. Original REJECTED, clarification01 distinct SCOPED_PASS_ARCHIVE_ONLY ZERO replay. GPL-2.0-or-later device/MIT firmware, pas Sony. BLOCKED reset/CD/hardware/gameplay/integration ; global FAIL/procedure FAIL. PENDING_INDEPENDENT_EXACT_HASH_REVIEW.</p><p><a href="../stories/RE-925-dma-proof-publication.md">Story / acceptance</a> · <a href="functions/re925-dma-proof-publication.md">Evidence / blockers</a> · <a href="generated/re925-dma-proof-publication-v1.json">Status</a></p></section>\n<!-- RE925 PUBLICATION END -->\n'
DOC='# RE925 — publication metadata DMA RE924\n\n## Progression\n- [x] Preuves privées archivées authentifiées : ensembles exacts85/70/7, tailles/SHA/seals.\n- [x] TDD RED puis GREEN metadata canonical/public-only, zéro replay numérique.\n- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW ; worktree-only, pas stage/commit/push.\n\n## Evidence\nRE924-PCSX-Redux-DPCR-DICR-subset : DPCR réellement franchi, retours A0:13/B0:19, arrêt AVANT Timer1 MODE write32 non complété. 1980769 instructions complétées/1980770 visites ; +4274 depuis RE922, reprise4274/4275. Observation du hook suivant, pas retraite microarchitecture. RAM entière2097152octets,32GPR, PC/MMIO ordonnés concordent avec decoder reviewer frais indépendant. Producteur11méthodes,45comparaisons DICR; reviewer45 +2048semées,54width/alias,4refus atomiques. DICR construit seulement, jamais traversé naturellement. Publication ajoute ZERO target/native/replay. Witness extrait/adapté GPL-2.0-or-later, pas émulateur complet; ROM OpenBIOS MIT réutilisée, pas compilation firmware fraîche. Copyright (C) 2023 PCSX-Redux authors pour psxhw.cc et psxmem.h ; URLs/digests explicites dans metadata. Aucune source tierce redistribuée.\n\n## Reviewhistory\nOriginal verdict passed=false, deux concerns : REJECTED inchangé. Clarification01 distincte SCOPED_PASS_ARCHIVE_ONLY, strict passed=true/errors=[]/concerns=[], ZERO nouvelle exécution. Concerns originales et limitations conservées intégralement. firstFAIL producteur, reviewer import et decoder initial inutilisé erroné retenus ; corrigés dans invocations distinctes, aucun rejet rétrocertifié.\n\n## Blockers\nABI/RAM/caller construits, loads immédiats et quatre miroirs RAM, pas load-delay/cache. Aucun transfert DMA/scheduling/completion, événements timer, IRQ active/exception, reset naturel/Sony, secteurs CD, hardware/gameplay/intégration prouvés. Global FAIL/procedure FAIL maintenus ; integration=false. BLOCKED-001/002 restent supprimés selon volonté utilisateur, non restaurés. Aucun patch production.\n\n## Acceptance\nAuthentification documentaire et tests publics seulement, pas numerical replay. Export sans build/private dependency. Compatibility baseline/current/export même collection et mêmes nodeids des deux FAIL historiques RE830, non affaiblis. Dashboard suffix exact réversible sur bytes prédécesseurs RE923 ; guards raw/secret/binary et allowlist explicite. Livraison worktree-only ; revue indépendante exact-hash PENDING_INDEPENDENT_EXACT_HASH_REVIEW.\n'
OUTPUT_PATHS=(STORY,REPORT,JSON_PATH,CSV_PATH,DASHBOARD,MAINTAINED)
PUBLIC_PATHS=OUTPUT_PATHS+(PRIOR_MAINTAINED,"scripts/reverse/re925_publication.py","tests/reverse/test_re925_publication.py")+tuple(COMPATIBILITY_DELTAS)
def metadata():return copy.deepcopy(EXPECTED)
def validate(data):
 def exact(a,b):
  if type(a) is not type(b):return False
  if isinstance(b,dict):return set(a)==set(b) and all(exact(a[k],b[k]) for k in b)
  if isinstance(b,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
  return a==b
 if not exact(data,EXPECTED):raise ValueError('exact RE925 recursive schema types/counts/hash/scope required')
 return data
def digest(b):return hashlib.sha256(b).hexdigest()
def inverse(data,sha):
 suffix=SECTION.encode()+b'</html>'
 if not data.endswith(suffix) or data.count(b'<!-- RE925 PUBLICATION BEGIN -->')!=1 or data.count(b'<!-- RE925 PUBLICATION END -->')!=1:raise ValueError('exact unique RE925 suffix required')
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
 if p.is_absolute() or '..' in p.parts or path not in PUBLIC_PATHS:raise ValueError('outside explicit RE925 public scope')
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
 for ticket,status in [('RE924','PRIVATE_DMA_FINITE_SCOPED_ACCEPTED'),('RE925','PUBLIC_METADATA_TESTS_ONLY')]:w.writerow([ticket,'archived proof' if ticket!='RE925' else 'fresh metadata',status,'false',d['publication_review']])
 out[CSV_PATH]=stream.getvalue().encode()
 for p,b in out.items():guard_output(p,b)
 return out
def original_compatibility(path,text):
 spec=COMPATIBILITY_DELTAS[path]
 for old,new in reversed(spec['replacements']):
  if text.count(new)!=1:raise ValueError('exact RE925 compatibility adapter required')
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
 print('RE925 PUBLIC_METADATA_TESTS_ONLY PASS; exact-public-hash independent review PENDING')
if __name__=='__main__':
 argparse.ArgumentParser(description=__doc__).parse_args();check()
