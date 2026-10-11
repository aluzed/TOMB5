"""RE898 versioned strict metadata schema/fixtures; no private proof dependency."""
import argparse,copy,csv,hashlib,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PRIOR_DASHBOARD='docs/reverse/tomb5-progress-dashboard-re894-v1.html'
DASHBOARD='docs/reverse/tomb5-progress-dashboard-re898-v1.html'
MAINTAINED='docs/reverse/tomb5-progress-dashboard.html'
STORY='docs/stories/RE-898-private-nonzero-proof-publication.md'
REPORT='docs/reverse/functions/re898-private-nonzero-proof-publication.md'
JSON_PATH='docs/reverse/generated/re898-private-proof-publication-v1.json'
CSV_PATH='docs/reverse/generated/re898-private-proof-tracker-v1.csv'
OUTPUT_PATHS=(STORY,REPORT,JSON_PATH,CSV_PATH,DASHBOARD,MAINTAINED)
PUBLIC_PATHS=OUTPUT_PATHS+('scripts/reverse/re898_publication.py','tests/reverse/test_re898_publication.py','tests/reverse/test_re830_table_provenance_publication.py','scripts/reverse/re882_publication.py','docs/reverse/tomb5-progress-dashboard-re830-v1.html')
PRIOR_SHA='d075302171f8d778ba7fdc6f928d92029aad86782c4c704ab9cc4102fdadef55'
MAINTAINED_SHA='7a53c9a86444ede3ace0a6ea23a30d5d004b16d744e7139272b4cdfcf40ea9fc'
SOURCE_SHA='59e70b260ae67d613e5fa74486c728a63bd3bb7ae4727537e293d4c057d9b7fa'
EXPECTED={
 'schema':'re898-private-proof-publication-v1','publication_review':'PENDING_INDEPENDENT_EXACT_HASH_REVIEW',
 'fresh_execution_scope':'PUBLIC_METADATA_TESTS_ONLY','integration':False,'production_patch':False,'public_helpers_green':False,
 'global_scope':'FAIL_NATURAL_GENERAL_HARDWARE_GAMEPLAY_UNPROVEN','procedure_scope':'FAIL_HISTORICAL',
 'next_ticket':'RE899','next_objective':'natural upstream provenance OR a new geometrically sensitive axis; separately authorized, no repeat of closed Y matrices',
 'limits':'constructed finite i386 domains only; shared actual target/native LIBGTE software is not hardware; independent CPU/math not saturation; no natural upstream, general axes, portable ABI, gameplay or hardware proof. FULLRAW2528 is a projection, not whole native RAM. O2 accepted only for RE897 finite domain, not global pointer-cast portability.',
 'projection':dict(gte_bytes=384,stack_bytes=[1024,1024],scalar_bytes=32,sentinel_bytes=64,positions_bytes=12,whole_native_ram=False),
 'archived_private_results':[
 dict(ticket='RE895',scope='PASS_PRIVATE_FINITE_DIRECT_INTERPOLATEMATRIX',fullraw_verdict='PASS_FINITE',caller_returned=False,callee_returned=True,gte_commands=0,domain='one constructed nonorthonormal unequal signed pair; fractions1/2/3 rate4',private_delta='one full32 assignment; nine rotation expressions sensitive; no public source patch',candidate_sha256='22940da9716976618ed031853f59c0044b04fa8d373aff2fab0c187fc762ec51',review_verdict_sha256='c62e45e752532018fd2a52a58d8abd03b6f3bd09e4d5d44066a32bf1e32473d5',producer=dict(target=3,cpu=3,math=3,native=24),reviewer_accepted=dict(target=3,cpu=3,math=3,native=24),native_matrix=dict(baseline_red=6,candidate_green=6,rollback_red=2,rollback_green=4,noop_red=6),historical_failures=['provider refusal after discovery/bootstrap: zero execution, distinct from actual 5.316s driver','historical unledgered discovery retained','inherited caller/bridge labels wrong; callee returned, NOT caller'],manifest_entries=261),
 dict(ticket='RE896',scope='PASS_FINITE_CHARACTERIZATION_NOT_STRICT_CODE_APPROVAL',fullraw_verdict='FAIL_FOUR_BYTES',caller_returned=True,callee_returned=True,domain='constructed real GetJointAbsPosition packed unequal nonzero Y using authentic table; fractions1/2/3',positions=[[26,-35,35],[31,-43,44],[36,-50,53]],candidate_sha256='22940da9716976618ed031853f59c0044b04fa8d373aff2fab0c187fc762ec51',review_verdict_sha256='72ed116273e8c2b030e971c4a1bf0f93ac2b07cf7066a2114eb6e4a298a3d18c',producer=dict(target=3,cpu=6,math=3,native=18),reviewer_accepted=dict(target=3,cpu=3,native=6),reviewer_initial=dict(target=3,cpu=3,native=3),reviewer_debugger=dict(native=7),reviewer_total=dict(target=6,cpu=6,native=16),geometry='PASS, three positions sensitive to primary and secondary ablations',last_writer='secondary iRotY dynamically attributed; target full32 versus native16 stores',historical_failures=['first producer fullraw FAIL remains immutable','initial reviewer math oracle FAIL and finalizer/header-only attempts preserved','characterization PASS is NOT strict code approval; FULLRAW FAIL retained'],manifest_entries=246,review_manifest_entries=250),
 dict(ticket='RE897',scope='PASS_FINITE_FULLRAW_REPAIR',fullraw_verdict='PASS_FINITE',caller_returned=True,callee_returned=True,domain='two finite constructed Y caller domains, i386 O0/O2 normal and strict; not natural',private_delta='two explicit signed full32 register-member writes; inherited RE895 pointer cast remains private',candidate_sha256='a9be03a8196e8f73bae09ede0d0aa270ee50cf1d6d0daf91fe8a0103c80610a2',review_verdict_sha256='1dcd2e05ad1603f7dbd80fc9b84643d6799cda14e3d912314fd75a5a4951a419',audit_verdict_sha256='4b1484555cd6b804ada4ccc0dacddf8b0035b77e89735b856fd3b5ab7b3849bf',producer=dict(target=6,cpu=6,math=6,native=60),reviewer_accepted=dict(target=6,cpu=6,math=6,native=60),native_matrix=dict(baseline_red=12,candidate_green=24,rollback_first=12,rollback_second=12),rollback_scope='RAW-only sensitivity; geometry unchanged, not geometric ablation proof',audit_additional=dict(target=0,native=0),historical_failures=['first producer math decode FAIL:3 target/3 CPU/0 native;47 inventory entries','first reviewer setup FAIL:zero execution;6 inventory entries','RE896 historical FULLRAW FAIL never overwritten by later repair'],manifest_entries=535,review_manifest_entries=539,audit_manifest_entries=50)
 ]}
SECTION='''
<!-- RE898 PUBLICATION BEGIN -->
<section id="re898-publication-v1" data-schema="re898-private-proof-publication-v1" data-publication-review="PENDING_INDEPENDENT_EXACT_HASH_REVIEW" data-integration="false">
<h2>CURRENT RE898 — ARCHIVED RE895–RE897, preuves privées finies uniquement</h2>
<p>Ce bloc seul est courant; tous les bytes précédents restent historiques inchangés. <a href="../stories/RE-898-private-nonzero-proof-publication.md">Story / acceptance</a> · <a href="functions/re898-private-nonzero-proof-publication.md">Evidence / blockers</a> · <a href="generated/re898-private-proof-publication-v1.json">Schema / metadata</a> · <a href="generated/re898-private-proof-tracker-v1.csv">Tracker</a> · <a href="tomb5-progress-dashboard-re898-v1.html#re898-publication-v1">Dashboard versionné RE898</a>.</p>
<p>RE895 direct InterpolateMatrix: callee retourné, PAS caller; une paire construite non orthonormale, fractions123/rate4, zéro commande GTE; 3 target/3 CPU/3 math/24 native producteur et reviewer. RE896 caller nonzero Y réel construit: géométrie PASS, FULLRAW FAIL quatre bytes conservé; producteur3 target/6 CPU/3 math/18 native; reviewer accepté3 target/3 CPU/6 native, total avec tentative initiale et debugger6 target/6 CPU/16 native. Ce PASS est caractérisation, PAS strict code approval.</p>
<p>RE897 réparation privée deux writers full32:6 target/6 CPU/6 math/60 native producteur et reviewer chacun;12 baseline RED,24 candidate GREEN O0/O2 normal/strict,12 rollbacks par writer. Rollback RAW-only, géométrie inchangée. Audit indépendant supplémentaire sans replay,0 cible/0 natif. Premiers math decode FAIL et setup FAIL scellés conservés.</p>
<p>Global FAIL / procédure historique FAIL / integration=false / production_patch=false. Fresh PUBLIC_METADATA_TESTS_ONLY; shared actual LIBGTE logiciel, CPU/math indépendants non saturants, pas hardware. Naturel, axes généraux, saturation, ABI portable et gameplay non prouvés. Aucune activation publique ni readiness upgrade. PENDING_INDEPENDENT_EXACT_HASH_REVIEW, pas auto-approbation. RE899: provenance naturelle upstream OU nouvel axe géométriquement sensible autorisé séparément; ne pas répéter les matrices Y fermées.</p>
</section>
<!-- RE898 PUBLICATION END -->
'''
def metadata():return copy.deepcopy(EXPECTED)
def validate(data):
 def exact(a,b):
  if type(a) is not type(b):return False
  if isinstance(b,dict):return set(a)==set(b) and all(exact(a[k],b[k]) for k in b)
  if isinstance(b,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
  return a==b
 if not exact(data,EXPECTED):raise ValueError('exact RE898 recursive schema types/counts/hash/scope required')
 return data
def digest(b):return hashlib.sha256(b).hexdigest()
def inverse(data,sha):
 suffix=SECTION.encode()+b'</html>'
 if not data.endswith(suffix) or data.count(b'<!-- RE898 PUBLICATION BEGIN -->')!=1 or data.count(b'<!-- RE898 PUBLICATION END -->')!=1:raise ValueError('exact unique RE898 suffix required')
 before=data[:-len(suffix)]+b'</html>'
 if digest(before)!=sha:raise ValueError('exact predecessor bytes changed')
 return before
def preceding_dashboard(data):return inverse(data,PRIOR_SHA)
def preceding_maintained(data):return inverse(data,MAINTAINED_SHA)
def maintained_before():
 before=(ROOT/PRIOR_DASHBOARD).read_bytes()[:38106]+b'</html>'
 if digest(before)!=MAINTAINED_SHA:raise ValueError('maintained predecessor projection drift')
 return before
RAW=re.compile(rb'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|raw_opcode|raw_pc|register_values|target_address|payload_offset|data:image|```(?:asm|mips|cpp|c)\b',re.I)
SECRET=re.compile(rb'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|(?:api[_-]?key|password|secret)\s*[:=]\s*[\"\x27][^\"\x27\s]{12,}',re.I)
def guard_added(path,payload):
 p=Path(path)
 if p.is_absolute() or '..' in p.parts or path not in PUBLIC_PATHS:raise ValueError('outside explicit RE898 public scope')
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
 text='# RE898 — publication metadata privée nonzero, v1\n\nARCHIVED; fresh PUBLIC_METADATA_TESTS_ONLY. PENDING_INDEPENDENT_EXACT_HASH_REVIEW.\n\n## Progression\n- [x] RED frais générateur absent avant implémentation.\n- [x] Verdicts archivés indépendants lus, hashes vérifiés; pas de nouveaux replays privés.\n- [x] Schéma exact récursif et fixtures publiques déterministes; tracker trois lignes.\n- [x] Dashboard maintenu append-only et versionné, inverse exact prédécesseur.\n- [ ] Revue indépendante des hashes publics exacts.\n- [ ] Intégration production distincte, non autorisée.\n\n## Evidence\n'
 for r in EXPECTED['archived_private_results']:
  text+='\n### '+r['ticket']+' — '+r['scope']+'\n'+json.dumps(r,sort_keys=True,ensure_ascii=False,indent=2)+'\n'
 text+='\nLes comptes producteur/reviewer sont archivés, distincts des tests publics RE898. RE896 total inclut initial3 target/3 CPU/3 native et debugger7 native; accepté3/3/6 seulement. RE897 audit ajoute zéro replay. RE896 FULLRAW FAIL quatre bytes immuable, caractérisation géométrie PASS seulement.\n\n## Blockers\nintegration=false; production_patch=false; public_helpers_green=false. Global FAIL / procédure historique FAIL.\n'+EXPECTED['limits']+'\nPublic MATHS inchangé, ancien mRotY seulement; GetSpheres stub, helpers privés non intégrés. Inherited wrong caller/bridge labels RE895 explicitement qualifiés. Premiers FAIL producteur et reviewer conservés; aucun seal rétrocertifié. BLOCKED-001/002 supprimés par utilisateur restent supprimés, rapport technique untracked conservé. Aucun screenshot runtime ni nouvelle compilation cible/native.\n\n## Acceptance\n- [x] Types stricts bool/int, drift hash/count/frontière et champs inconnus rejetés.\n- [x] Secrets, raw tokens, chemins hors scope et heavy assets rejetés avec contrôles bénins.\n- [x] Export public-only sans dépendance proof ignorée.\n- [x] Inverse exact maintenu et RE894, bytes historiques non normalisés.\n- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW: auteur non reviewer.\n- [ ] GREEN global, gameplay/hardware/saturation/naturalité non revendiqués.\n\n## Handoff\nRE899: provenance naturelle upstream OU nouvel axe géométriquement sensible; autorisation et revue séparées, ne pas répéter matrices Y fermées.\n'
 prefix='../' if report else '../reverse/'
 text+='[Metadata]('+prefix+'generated/re898-private-proof-publication-v1.json) · [Tracker]('+prefix+'generated/re898-private-proof-tracker-v1.csv) · [Dashboard]('+prefix+'tomb5-progress-dashboard-re898-v1.html).\n'
 return text
def render(before):
 d=validate(metadata())
 if digest(before)!=PRIOR_SHA or not before.endswith(b'</html>'):raise ValueError('pinned RE894 predecessor required')
 out={STORY:document().encode(),REPORT:document(True).encode(),JSON_PATH:(json.dumps(d,indent=2,sort_keys=True)+'\n').encode(),DASHBOARD:before[:-7]+SECTION.encode()+b'</html>',MAINTAINED:maintained_before()[:-7]+SECTION.encode()+b'</html>'}
 stream=io.StringIO(newline='');fields=['ticket','scope','fullraw_verdict','producer_target','producer_cpu','producer_math','producer_native','reviewer_target','reviewer_cpu','reviewer_native','review_verdict_sha256','integration','publication_review'];w=csv.DictWriter(stream,fieldnames=fields,lineterminator='\n');w.writeheader()
 for r in d['archived_private_results']:
  row={k:r[k] for k in ('ticket','scope','fullraw_verdict','review_verdict_sha256')};row.update(integration='false',publication_review=d['publication_review'])
  for k,v in r['producer'].items():row['producer_'+k]=v
  for k in ('target','cpu','native'):row['reviewer_'+k]=r['reviewer_accepted'][k]
  w.writerow(row)
 out[CSV_PATH]=stream.getvalue().encode()
 for p,b in out.items():guard_output(p,b)
 return out

ADAPTER="    # RE898 exact authenticated successor only; all old RE830 guards retained.\n    if b'<!-- RE898 PUBLICATION' in data:\n        import runpy\n        successor = runpy.run_path(str(ROOT / 'scripts/reverse/re898_publication.py'))\n        try:\n            data = successor['preceding_maintained'](data)\n        except ValueError as error:\n            raise AssertionError('RE898 successor malformed or predecessor changed') from error\n"
def original_test830(text):
 if text.count(ADAPTER)!=1:raise ValueError('exact unique historical adapter required')
 before=text.replace(ADAPTER,'',1)
 if digest(before.encode())!='a0a9350be61d985bc60cb22c25aceab02e0922f659596db80d66bc2b45df82b3':raise ValueError('historical guard weakened')
 return before

def check():
 original_test830((ROOT/'tests/reverse/test_re830_table_provenance_publication.py').read_text())
 for p,b in render((ROOT/PRIOR_DASHBOARD).read_bytes()).items():
  if (ROOT/p).read_bytes()!=b:raise ValueError('generated drift '+p)
 for p in PUBLIC_PATHS:
  if p not in (DASHBOARD,MAINTAINED) and 'test_re830' not in p:guard_added(p,(ROOT/p).read_bytes())
 assert digest((ROOT/'docs/reverse/tomb5-progress-dashboard-re830-v1.html').read_bytes())==MAINTAINED_SHA
 assert digest((ROOT/'scripts/reverse/re882_publication.py').read_text().replace("PRIOR_DASHBOARD = 'docs/reverse/tomb5-progress-dashboard-re830-v1.html'","PRIOR_DASHBOARD = 'docs/reverse/tomb5-progress-dashboard.html'",1).encode())=='ca961e9d0f0359a7b7238025f620cd730f10b033d0597711f281351778fc0c61'
 print('RE898 PUBLIC_METADATA_TESTS_ONLY PASS; independent exact-public-hash review PENDING')
if __name__=='__main__':
 a=argparse.ArgumentParser(description=__doc__);a.parse_args();check()
