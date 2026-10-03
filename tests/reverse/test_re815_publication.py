"""RE815 metadata TDD, no target execution or protected payload publication."""
import csv, hashlib, io, re, runpy
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[2]
VERDICT='91a64b4efe5c16fbe416806feb46073a5bccd63404c43f2c341f428ef9dc5460'
MANIFEST='0784525f0d9eb2cd020554acf15bf23d0b79a745b5032574ebf3d4d8ffb173e8'
def api():
 p=R/'scripts/reverse/re815_publication.py'
 assert p.exists(), 'RED: safe RE815 generator absent'
 return runpy.run_path(str(p))
def test_contract_counts_truth_and_outputs():
 g=api();d=g['metadata']();g['validate'](d)
 assert d['private_verdict_sha256']==VERDICT and d['private_manifest_sha256']==MANIFEST
 assert d['private_review']=='PASS_scoped' and d['status']=='REGISTRATION_PREFIX_PASS_NATIVE_REQUIREMENT_RED'
 assert [d[k] for k in ['slots','hook_visits','oracle_bytes','corruptions_rejected','independent_stores','native_requirement_exit','strict_requirement_exit','native_characterization_exit','strict_characterization_exit']]==[14,601,896,896,70,1,1,0,0]
 assert d['constructed_registers']=='GP SP RA' and d['native_runtime_stderr_empty'] is True
 for k in ['source_patch','integration_approved','publication_review_approved','production_ready','global_green','startup_proven','full_target_return','initializer_invoked','controller_invoked','whole_ram_oracle','hardware_proven','t7_t8_t9_injected','re816_publication_approved']:
  assert d[k] is False
 assert d['next']=='RE816 private composition executed; independent review pending; NO publication'
 for p,k in [('GAME/ITEMS.C','items_sha256'),('GAME/SETUP.C','setup_sha256'),('GAME/DOOR.C','door_sha256')]:
  assert hashlib.sha256((R/p).read_bytes()).hexdigest()==d[k]
 assert list(csv.DictReader(io.StringIO(g['CSV_TEXT'])))==[g['csv_row']()]
 for p,k in g['OUTPUTS'].items():assert (R/p).read_text()==g[k]
 assert '- [x]' in g['STORY'] and '- [ ]' in g['STORY']
 for text in [g[k] for k in g['OUTPUTS'].values()]+[g['SECTION']]:
  assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|payload_offset|word_le_hex|data:image|```(?:asm|mips|cpp|c)\b',text)
def test_schema_mutations_fail_closed():
 g=api();good=g['metadata']()
 for k,v in good.items():
  bad=dict(good);bad[k]=not v if type(v) is bool else v+1 if type(v) is int else v+'changed'
  with pytest.raises(ValueError):g['validate'](bad)
 for bad in [{**good,'raw_opcode':'forbidden'},{k:v for k,v in good.items() if k!='slots'},{**good,'slots':14.0}]:
  with pytest.raises(ValueError):g['validate'](bad)
def test_exact_append_inverse_and_predecessors():
 g=api();b=(R/'docs/reverse/reconstruction-progress.html').read_bytes()
 successor816=runpy.run_path(str(R/'scripts/reverse/re816_publication.py'))
 if successor816['START'].encode() in b:b=successor816['dashboard_before_re816'](b)
 if g['START'].encode() not in b:b+=g['SECTION'].encode()
 before=g['dashboard_before_re815'](b)
 assert hashlib.sha256(before).hexdigest()==g['PRECEDING']
 assert b==before+g['SECTION'].encode()
 checks=[g['dashboard_before_re815']]
 for n in ['re814_publication','re813_publication','re812_publication','re811_provenance']:
  old=runpy.run_path(str(R/('scripts/reverse/'+n+'.py')))
  fn=old['dashboard_before_'+n[:5]];checks.append(fn)
  assert hashlib.sha256(fn(b)).hexdigest()==old['PRECEDING']
 for fn in checks:
  for m in [b+b'foreign',b+g['SECTION'].encode(),b.replace(g['END'].encode(),b'',1),b.replace(b'RE-809',b'RE-xxx',1),b.replace(b'601',b'602',1)]:
   with pytest.raises(AssertionError):fn(m)
def test_private_approval_manifest_authenticated():
 g=api();d=g['consume_approval']()
 assert d['passed'] is True and d['manifest_entries']==33
 assert d['integration_approved'] is False and d['production_approved'] is False
