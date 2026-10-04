"""Portable RE819 publication contract: metadata tests, not target replay."""
import csv,hashlib,io,json,re,runpy
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[2]
H=lambda b:hashlib.sha256(b).hexdigest()
EXPECTED={'schema': 're819-real-allocator-prerequisite-v1', 'status': 'RECOVERED_PRIVATE_REAL_ALLOCATOR_PREREQUISITE_PASS', 'private_review': 'SCOPED_PRIVATE_PASS', 'public_review': 'PENDING_REVIEW', 'integration': 'BLOCKED', 'private_verdict_sha256': '65dca2fa90b05f0f77572d70b3e923c7f2df727f1ab5ba9f22667dec94859564', 'private_manifest_sha256': '548075adcde1439a2ceafc80de1bac1ed5d38690deb34327202f4cc52f85ac1d', 'private_seal_sha256': '6d42bf7a7cef33777606878acd02250798c26bfa81b48decbe867f68335f3fde', 'manifest_entries': 225, 'original_timeout_files': 240, 'baseline_normal_exit': 1, 'baseline_strict_exit': 1, 'candidate_normal_exit': 0, 'candidate_strict_exit': 0, 'rounding_mutant_exit': 1, 'native_request_bytes': 82, 'native_consumed_bytes': 84, 'target_request_consumed_bytes': 92, 'projection_bytes': 2980, 'whole_native_buffer_bytes': 1088324, 'caller_events': 17, 'snapshots': 17, 'dependency_events': 11, 'native_control_executions': 6, 'target_control_sequences': 3, 'rows_per_sequence': 17, 'whole_control_buffer_bytes': 2170880, 'whole_target_ram_bytes': 2097152, 'descriptor_mutants_rejected': 255, 'prefixes': '0/63/64', 'control_requests': '0,1,2,3,4,5,82,17; OOM1', 'allocator': 'real MALLOC.C linked and executed', 'target_caller_origin': 'ARCHIVE_RE816 authenticated via RE818; no fresh caller replay', 'size_alignment_only': True, 'pointer_realignment': False, 'prefix63_pointer_mod4': 3, 'prefix63_dereferenced': False, 'fresh_native_execution': True, 'fresh_target_malloc_free': True, 'fresh_target_caller': False, 'fresh_target_init': False, 'real_allocator_scoped_proven': True, 'raw_abi_identity': False, 'original_timeout_certified': False, 'production_patch': False, 'production_ready': False, 'integration_approved': False, 'activation_approved': False, 'publication_review_approved': False, 'global_green': False, 'startup_proven': False, 'hardware_proven': False, 'gameplay_proven': False, 'general_domain_proven': False, 'next': 'natural caller provenance and ABI compatibility prerequisites before any activation'}
SECTION='<!-- start re819-real-allocator-prerequisite --><section id="re819"><h2>RE-819 — allocateur réel, PASS privé borné</h2><p>MALLOC.C réel lié et exécuté dans SETUP privé → InitialiseItem production → DOOR privé → ITEMS/GETSTUFF/COLLIDE réels. Double baseline RED1 (82 contre84); candidat normal/strict GREEN0; mutant rounding RED1. Native demande82 consomme84, cible92: ABI distinctes. Projection2980, whole buffer1088324,17 événements/snapshots. Contrôles natifs6 et cible malloc/free fraîche3 séquences,17 lignes chacun, prefixes0/63/64; arrondi taille seul, pas réalignement pointeur.</p><p>Caller cible ARCHIVE_RE816 authentifié via RE818, pas replay caller frais ni startup/matériel/gameplay. Timeout240 fichiers NON CERTIFIÉ; publication pending revue, intégration/activation bloquées; BLOCKED-006 ouvert. <a href="../stories/RE-819-real-allocator-prerequisite.md">Story</a> · <a href="functions/re819-real-allocator-prerequisite.md">Contrat</a> · <a href="generated/re819-real-allocator-prerequisite.csv">CSV</a> · <a href="generated/re819-real-allocator-prerequisite-proof.json">Proof</a>.</p></section><!-- end re819-real-allocator-prerequisite -->\n'
PRECEDING='301e3235d55974210f54380ad3680ba05151cef7e95f208dd9d708656895f21c'
OLD={'scripts/reverse/re815_publication.py': 'a25776e584e75f5b376b107d6356f4fa3b408bfd619ca2e0570ecdd78f190c1a', 'scripts/reverse/re816_publication.py': '1fa2de31c1ba907c9cfdb6189a7d444aed1dfeb81d1d9cdd2b4cadacdfba2557', 'scripts/reverse/re813_publication.py': 'd6319348c5dd58666e208ce3514daa3952ad23f810a921b10ce4433595b12b1f', 'scripts/reverse/re812_publication.py': 'bfc80198a3079c14e4c26118d33a517609f56541bc445d169485f55330de3858', 'scripts/reverse/re818_publication.py': 'd00efcc187a38d53defd3b33fbb118a2e005479824dfcfc4150f1e1d6060694b', 'scripts/reverse/re811_provenance.py': '24306b4026e587158fa37bf0a69d183152c0e6cdd46bfd4e9d2b8dc000185e1b', 'scripts/reverse/re814_publication.py': '82a1f170822484a7f439292f4e5f49d9d414b964827e6c4f47505aae5df8b511', 'scripts/reverse/re817_publication.py': '1306163d0ff0ee64733075cf5898653a02d4490b657b331486f3c99be56514e8', 'tests/reverse/test_re817_publication.py': 'fa6c39e196216d5008e06c1f80e20e6437b429c9f06d491093c1d70bc44283c0', 'tests/reverse/test_re818_publication.py': '6f7544ccb6526cc5cd1944b51e0d43ea277eca8b81382fee8d0b570b27d9e79b'}
def api():
 p=R/'scripts/reverse/re819_publication.py'
 assert p.exists(),'RED: RE819 publication generator absent'
 return runpy.run_path(str(p))
def test_exact_metadata_types_and_negative_flags():
 g=api();assert g['metadata']()==EXPECTED
 for k,v in EXPECTED.items():
  for replacement in [None,not v if type(v) is bool else v+1 if type(v) is int else v+'drift']:
   with pytest.raises(ValueError):g['validate']({**EXPECTED,k:replacement})
 for bad in [{}, {**EXPECTED,'raw':'forbidden'}, {**EXPECTED,'candidate_normal_exit':False},{**EXPECTED,'projection_bytes':2980.0}]:
  with pytest.raises(ValueError):g['validate'](bad)
def test_safe_generated_artifacts():
 g=api()
 for p,k in g['OUTPUTS'].items():assert (R/p).read_text()==g[k]
 assert json.loads(g['PROOF_JSON'])==EXPECTED
 assert list(csv.DictReader(io.StringIO(g['CSV_TEXT'])))==[g['csv_row']()]
 for text in [g[k] for k in g['OUTPUTS'].values()]+[SECTION]:
  assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|payload_offset|word_le_hex|data:image|```(?:asm|mips|cpp|c)\b',text)
 assert '- [x]' in g['STORY'] and '- [ ]' in g['STORY']
 assert 'NON CERTIFIÉ' in g['STORY'] and 'sans déréférencement' in g['FUNCTIONDOC']
@pytest.mark.parametrize('path',[p for p in OLD if p.startswith('scripts/')])
def test_predecessor_exact_successor_acceptance(path):
 old=runpy.run_path(str(R/path));n=Path(path).name[:5];b=(R/'docs/reverse/reconstruction-progress.html').read_bytes();g820=runpy.run_path(str(R/'scripts/reverse/re820_publication.py'));b=g820['dashboard_before_re820'](b)
 if not b.endswith(SECTION.encode()):b+=SECTION.encode()
 fn=old['dashboard_before_'+n];assert H(fn(b))==old['PRECEDING']
 for mutant in [b+b'foreign',b+SECTION.encode(),b.replace(b'RE-819',b'RE-xxx'),b.replace(b'RE-809',b'RE-xxx'),b.replace(b'<!-- end re819-real-allocator-prerequisite -->',b''),b+b'<!-- start re820-unknown -->x<!-- end re820-unknown -->']:
  with pytest.raises(AssertionError):fn(mutant)
def blocker_before_re830(data):
 # Only the exact authenticated RE830 successor is reversible; no generic append.
 if b'## RE830' in data:
  contract=runpy.run_path(str(R/'tests/reverse/test_re830_table_provenance_publication.py'))
  before=contract['preceding_blocker'](data)
  assert H(before)=='a9c5a04d69c030a8e8c47915a345223e44a32eecadaa5c6cd5f7d20e8bbb4a59'
  return before
 assert H(data)=='a9c5a04d69c030a8e8c47915a345223e44a32eecadaa5c6cd5f7d20e8bbb4a59', 'RE830 successor malformed or history altered'
 return data
def test_append_only_dashboard_blocker_and_exact_inverse_code():
 g=api();b=(R/'docs/reverse/reconstruction-progress.html').read_bytes();g820=runpy.run_path(str(R/'scripts/reverse/re820_publication.py'));b=g820['dashboard_before_re820'](b);assert H(g['dashboard_before_re819'](b))==PRECEDING
 for path,h in OLD.items():
  text=(R/path).read_text();assert H(g['inverse_code'](text,path).encode())==h
 c=blocker_before_re830((R/g['BLOCKER_PATH']).read_bytes());append=g['BLOCKER_APPEND'].encode()
 assert c.endswith(append) and H(c[:-len(append)])==g['BLOCKER_BEFORE']
def test_provenance_schema_portable():
 g=api();assert g['PRIVATE_PINS']=={n:EXPECTED['private_'+n.replace('.json','')+'_sha256'] for n in ['verdict.json','manifest.json','seal.json']}
 assert EXPECTED['private_verdict_sha256']=='65dca2fa90b05f0f77572d70b3e923c7f2df727f1ab5ba9f22667dec94859564'

@pytest.mark.parametrize('mutation', ['foreign', 'duplicate', 'altered', 'missing', 'history', 'unknown'])
def test_re830_blocker_successor_fail_closed(mutation):
 contract=runpy.run_path(str(R/'tests/reverse/test_re830_table_provenance_publication.py'))
 data=(R/contract['BLOCKER']).read_bytes(); addition=contract['APPEND'].encode()
 assert blocker_before_re830(data)==contract['preceding_blocker'](data)
 mutants={'foreign':data+b'foreign','duplicate':data+addition,'altered':data.replace(addition,addition.replace(b'620',b'621')),'missing':data.replace(b'## RE830',b'## RE83X'),'history':b'foreign'+data,'unknown':data+b'\n## RE831\nunknown\n'}
 with pytest.raises(AssertionError):blocker_before_re830(mutants[mutation])

@pytest.mark.parametrize('name',['verdict.json','manifest.json','seal.json'])
def test_private_provenance_rejects_counterfeit_without_replay(tmp_path,name):
 g=api();fn=g['consume_approval'];fn.__globals__['ROOT']=tmp_path
 p=tmp_path/'build/reverse/autonomy-20261003/re819-recovery-independent-review';p.mkdir(parents=True)
 for n in ['verdict.json','manifest.json','seal.json']:(p/n).write_text('{}\n')
 (p/name).write_text('{"passed":true,"integration_approved":true}\n')
 with pytest.raises(AssertionError):fn()
