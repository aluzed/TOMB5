"""RE817 portable TDD, no private evidence required."""
import csv,hashlib,io,re,runpy
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[2]
EXPECTED={'status': 'RECOVERED_PRIVATE_NATIVE_INITIALIZER_PREREQUISITE_PASS', 'private_review': 'PRIVATE_ONLY_PASS', 'private_verdict_sha256': '292a83d4c523f0d1f9e05607f89c3800c93d6fccafad798faa28d2d72ff73141', 'private_manifest_sha256': 'eb338c1e1950dbfbd025ed65fb3856818d905d8ab3137a79a465717f4605ed76', 'candidate_sha256': '449d24af4532ee267f3ba07f8e9c2f7792cbdf0005d3d1d4f7b286ffe8b9f5dd', 'manifest_entries': 235, 'target_visits': 994, 'target_selected_bytes': 2992, 'native_selected_bytes': 2980, 'target_allocation_bytes': 92, 'native_allocation_bytes': 82, 'byte_corruptions_rejected_per_mode': 2980, 'event_corruptions_rejected_per_mode': 11, 'code_mutants_rejected': 2, 'baseline_normal_exit': 1, 'baseline_strict_exit': 1, 'candidate_normal_exit': 0, 'candidate_strict_exit': 0, 'getdoor_calls': 5, 'shut_calls': 4, 'itemnewroom_calls': 1, 'fixture_count': 1, 'domain': 'generic284 angle0 rooms0..3 portal2 sentinel255', 'allocator': 'declared double, not production allocator', 'target_origin': 'direct initializer from archived RE816 RAM; not retained caller CPU', 'abi': 'declared projection and pointer rebasing; not ABI identity', 'native_entry': 'private weak direct initializer; no registration or InitialiseItem', 'original_timeout_certified': False, 'first_reviewer_attempt_accepted': False, 'native_registration_proven': False, 'native_caller_composition_proven': False, 'general_input_domain_proven': False, 'real_allocator_proven': False, 'source_patch': False, 'activation_approved': False, 'integration_approved': False, 'production_ready': False, 'publication_review_approved': False, 'global_green': False, 'hardware_proven': False, 'startup_proven': False, 'whole_ram_oracle': False, 'next': 'RE818 actual-native conditional producer/caller composition prerequisite; not performed'}
SECTION='<!-- start re817-native-initializer-prerequisite --><section id="re817"><h2>RE-817 — RECOVERED_PRIVATE_NATIVE_INITIALIZER_PREREQUISITE_PASS</h2><p>Récupération indépendante PRIVATE_ONLY_PASS distincte du timeout600 NON CERTIFIÉ et de attempt01 rejetée. Cible directe RAM archivée, 994 visites, 2992 octets; actual-TU privé normal/strict baseline RED1 candidat GREEN0, projection2980, corruptions2980 et événements11 rejetés par mode, deux mutants code rejetés. Allocateur double82 vs cible92; une fixture generic284 angle0 rooms0..3 portal2 sentinelle255. Pas registration/InitialiseItem ni composition caller natifs, domaine général ou allocateur réel.</p><p>Publication metadata-only pending revue finale parent; aucune production/intégration/activation ni GREEN global. Historiques RE815/816 gelés; BLOCKED-003/004/006 ouverts, 001/002 non recréés. RE818 actual-native conditional producer/caller prerequisite non effectué. <a href="../stories/RE-817-native-initializer-prerequisite.md">Story</a> · <a href="functions/re817-native-initializer-prerequisite.md">Contrat</a> · <a href="generated/re817-native-initializer-prerequisite.csv">CSV</a>.</p></section><!-- end re817-native-initializer-prerequisite -->\n'
PRECEDING='b100509e34a75f6a8590bcce38b5c9430e818c8661a32858a0a94facf8b4e071'
NAMES=['re811_provenance', 're812_publication', 're813_publication', 're814_publication', 're815_publication', 're816_publication']
def api():
 p=R/'scripts/reverse/re817_publication.py'
 assert p.exists(), 'RED: RE817 generator absent'
 return runpy.run_path(str(p))
def test_exact_schema():
 g=api();assert g['metadata']()==EXPECTED and g['PRECEDING']==PRECEDING and g['SECTION']==SECTION
 assert g['validate'](dict(EXPECTED))==EXPECTED
 for k,v in EXPECTED.items():
  bad=dict(EXPECTED);bad[k]=not v if type(v) is bool else v+1 if type(v) is int else v+'altered'
  with pytest.raises(ValueError):g['validate'](bad)
 for bad in [{**EXPECTED,'opcode':'bad'},{k:v for k,v in EXPECTED.items() if k!='target_visits'},{**EXPECTED,'target_visits':994.0},{**EXPECTED,'baseline_normal_exit':True}]:
  with pytest.raises(ValueError):g['validate'](bad)
def test_artifacts():
 g=api()
 for p,k in g['OUTPUTS'].items():assert (R/p).read_text()==g[k]
 assert list(csv.DictReader(io.StringIO(g['CSV_TEXT'])))==[g['csv_row']()]
 assert '- [x]' in g['STORY'] and '- [ ]' in g['STORY']
 for t in [g[k] for k in g['OUTPUTS'].values()]+[SECTION]:assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|payload_offset|word_le_hex|data:image|```(?:asm|mips|cpp|c)\b',t)
def mutants(b):
 start=b'<!-- start re817-native-initializer-prerequisite -->';end=b'<!-- end re817-native-initializer-prerequisite -->'
 return [b+b'foreign',b+SECTION.encode(),b.replace(start,b'',1),b.replace(end,b'',1),b.replace(start,b'TEMP',1).replace(end,start,1).replace(b'TEMP',end,1),b.replace(b'RE-809',b'RE-xxx',1),b+b'<!-- start re818-unknown -->bad<!-- end re818-unknown -->',b.replace(b'projection2980',b'projection2981',1)]
def test_append_only_and_predecessors():
 g=api();b=(R/'docs/reverse/reconstruction-progress.html').read_bytes()
 # RE818 exact suffix only; preserve historical RE817 assertion on its old bytes.
 start818=b'<!-- start re818-actual-tu-caller-prerequisite -->';end818=b'<!-- end re818-actual-tu-caller-prerequisite -->'
 if start818 in b or end818 in b:
  assert b.count(start818)==b.count(end818)==1
  a818=b.index(start818)
  assert hashlib.sha256(b[a818:]).hexdigest()=='133512b16df78502d62a52334174b04201d864b54165866985b5186b13b4ab8b'
  b=b[:a818]
  assert hashlib.sha256(b).hexdigest()=='ae791f9befe193f0370b68825cfe17d02616cc723661a8eaa07102caa2b75bc6'
 before=g['dashboard_before_re817'](b);assert hashlib.sha256(before).hexdigest()==PRECEDING and b==before+SECTION.encode()
 funcs=[g['dashboard_before_re817']]
 for n in NAMES:
  old=runpy.run_path(str(R/('scripts/reverse/'+n+'.py')));fn=old['dashboard_before_'+n[:5]]
  assert hashlib.sha256(fn(b)).hexdigest()==old['PRECEDING'];funcs.append(fn)
 for fn in funcs:
  for m in mutants(b):
   with pytest.raises(AssertionError):fn(m)
