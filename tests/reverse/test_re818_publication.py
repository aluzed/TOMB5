"""RE818 metadata TDD; portable, no private binaries or replay."""
import csv,hashlib,io,json,re,runpy
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[2]
EXPECTED={'status': 'RECOVERED_PRIVATE_ACTUAL_TU_CALLER_COMPOSITION_PREREQUISITE_PASS', 'private_review': 'SCOPED_PRIVATE_PASS', 'private_verdict_sha256': 'f0cddda154ee0577dd9f1c09571fc01e7f0fc65fdad49ecad9ff7ba93ee77786', 'private_manifest_sha256': '881c6e34d4eacd4721adfafe04ff5825ac979324e91aa3322171e40d755b0335', 'private_seal_sha256': '672bcbbf6baa4e9c115ec02ed2e75bc29e911c4b3c8f2805e622cf53a998c226', 'manifest_entries': 184, 'original_timeout_files': 338, 'registration_visits': 601, 'caller_visits': 1147, 'projection_bytes': 2980, 'regions': 6, 'ordered_events': 11, 'snapshots': 17, 'byte_sensitivity': 2980, 'baseline_normal_exit': 1, 'baseline_strict_exit': 1, 'candidate_normal_exit': 0, 'candidate_strict_exit': 0, 'mutant_registration_exit': 1, 'mutant_caller_exit': 1, 'native_allocation_bytes': 82, 'target_allocation_bytes': 92, 'fixture_count': 1, 'native_chain': 'private SETUP initializer284 -> production InitialiseItem -> private DOOR -> real GETSTUFF COLLIDE ITEMS', 'no_pointer_injection_after_registration': True, 'control_poison_preserved': True, 'target_origin': 'authenticated RE816 archive only; conditional retained CPU/RAM A0/RA composition, constructed framework', 'domain': 'generic284 angle0 rooms0..3 portal2 absence255', 'allocator': 'declared native double; not real allocator', 'fresh_native_execution': True, 'fresh_target_replay': False, 'original_timeout_certified': False, 'first_review_attempt_accepted': False, 'whole_ObjectObjects_proven': False, 'startup_proven': False, 'general_domain_proven': False, 'real_allocator_proven': False, 'source_patch': False, 'integration_approved': False, 'activation_approved': False, 'production_ready': False, 'publication_review_approved': False, 'global_green': False, 'hardware_proven': False, 'next': 'RE819 smallest private real-allocator dependency proof then sensitive caller domain extension; no integration'}
OLD={'re811_provenance': '14a731b8485e930514469cc0b9e557b2aaa737e0cc99996297e5a243cb79c721', 're812_publication': '3799aee0d35d32d461d66a3b6ee9bc1c9ddb047770ff96481bcf054c7d416402', 're813_publication': '60cb31128854a2f2ff59510321c35f43d9dc50e8ff02e8d044c0e6ed35df8ea8', 're814_publication': 'f7e3e94612769970fecff3ee53d6c9cdaa376dd70a7bad4eab39192ee0fdcd52', 're815_publication': '91f981f0daf8f21b1a9144e793065c6f3ed51a0a4d9283385264464e6821bc6c', 're816_publication': 'd4ba6e98d5f0b81e58162a735d034a3c6ebeb76437a7db495a3af32f47e1c524', 're817_publication': 'ad538254e764dd911a6cfb79ccea9274e86cfad82315907266a20b1926f209ce'}
PRECEDING="ae791f9befe193f0370b68825cfe17d02616cc723661a8eaa07102caa2b75bc6"

def api():
 p=R/'scripts/reverse/re818_publication.py'
 assert p.exists(),'RED: RE818 metadata generator absent'
 return runpy.run_path(str(p))
def test_exact_contract_fail_closed():
 g=api();assert g['metadata']()==EXPECTED;assert g['PRECEDING']==PRECEDING
 for k,v in EXPECTED.items():
  bad=dict(EXPECTED);bad[k]=not v if type(v) is bool else v+1 if type(v) is int else v+'drift'
  with pytest.raises(ValueError):g['validate'](bad)
 for bad in [{**EXPECTED,'raw':'bad'},{**EXPECTED,'regions':6.0},{**EXPECTED,'candidate_normal_exit':False},{}]:
  with pytest.raises(ValueError):g['validate'](bad)
def test_generated_safe_outputs():
 g=api()
 for p,k in g['OUTPUTS'].items():assert (R/p).read_text()==g[k]
 assert json.loads(g['PROOF_JSON'])==EXPECTED
 assert list(csv.DictReader(io.StringIO(g['CSV_TEXT'])))==[g['csv_row']()]
 for t in [g[k] for k in g['OUTPUTS'].values()]+[g['SECTION']]:
  assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|payload_offset|word_le_hex|data:image|```(?:asm|mips|cpp|c)\b',t)
 assert '- [x]' in g['STORY'] and '- [ ]' in g['STORY']
 assert 'RE817' in g['FUNCTIONDOC'] and 'poison99' in g['FUNCTIONDOC']
def test_append_inverse_guards_and_sensitive_mutants():
 g=api();b=(R/'docs/reverse/reconstruction-progress.html').read_bytes()
 before=g['dashboard_before_re818'](b);assert hashlib.sha256(before).hexdigest()==PRECEDING
 funcs=[g['dashboard_before_re818']]
 for n,h in OLD.items():
  text=(R/('scripts/reverse/'+n+'.py')).read_text();block=g['PREDECESSOR_DELTA']
  if n=='re812_publication':block=''.join('   '+l for l in block.splitlines(True))
  assert text.count(block)==1
  assert hashlib.sha256(text.replace(block,'',1).encode()).hexdigest()==h
  old=runpy.run_path(str(R/('scripts/reverse/'+n+'.py')));fn=old['dashboard_before_'+n[:5]]
  assert hashlib.sha256(fn(b)).hexdigest()==old['PRECEDING'];funcs.append(fn)
 mutants=[b+b'foreign',b+g['SECTION'].encode(),b.replace(g['START'].encode(),b'',1),b.replace(g['END'].encode(),b'',1),b.replace(b'RE-809',b'RE-xxx',1),b.replace(b'RE-818',b'RE-xxx',1),b+b'<!-- start re819-unknown -->x<!-- end re819-unknown -->']
 for fn in funcs:
  for m in mutants:
   with pytest.raises(AssertionError):fn(m)
def test_blocker_append_preserves_history():
 g=api();b=(R/g['BLOCKER_PATH']).read_bytes();assert b.endswith(g['BLOCKER_APPEND'].encode())
 assert hashlib.sha256(b[:-len(g['BLOCKER_APPEND'].encode())]).hexdigest()==g['BLOCKER_BEFORE']

def test_re817_test_exact_inverse_delta():
 text=(R/'tests/reverse/test_re817_publication.py').read_text()
 block=" # RE818 exact suffix only; preserve historical RE817 assertion on its old bytes.\n start818=b'<!-- start re818-actual-tu-caller-prerequisite -->';end818=b'<!-- end re818-actual-tu-caller-prerequisite -->'\n if start818 in b or end818 in b:\n  assert b.count(start818)==b.count(end818)==1\n  a818=b.index(start818)\n  assert hashlib.sha256(b[a818:]).hexdigest()=='133512b16df78502d62a52334174b04201d864b54165866985b5186b13b4ab8b'\n  b=b[:a818]\n  assert hashlib.sha256(b).hexdigest()=='ae791f9befe193f0370b68825cfe17d02616cc723661a8eaa07102caa2b75bc6'\n"
 assert text.count(block)==1
 assert hashlib.sha256(text.replace(block,'',1).encode()).hexdigest()=='f821d408655b88dbd1c949a616a07fb5c1eb0d12c53ed8657a3e3a04f404f133'
