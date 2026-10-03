"""Versionable metadata only: no dependency on ignored private replay files."""
import csv,hashlib,io,re,runpy
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[2]
VERDICT='16ce302f58d9c55e00c53893240937adc32d26f29f228e4ecd9997d4011b66ab'
def api():
 p=R/'scripts/reverse/re813_publication.py'
 assert p.exists(), 'RED: RE813 safe generator missing'
 return runpy.run_path(str(p))
def test_exact_counts_bindings_and_public_artifacts():
 g=api();d=g['metadata']();g['validate'](d)
 assert [d[k] for k in ['cases','target_nonnull_controls','native_registration_nonnull','add_mismatches_per_mode','remove_equal_per_mode']]==[4,2,0,2,4]
 assert d['corrected_verdict_sha256']==VERDICT
 assert d['original_producer_review']=='FAILED' and d['corrected_fixture_review']=='PASS_scoped'
 assert d['normal_strict_scope']=='i386 O0 normal + ASan/UBSan failfast only'
 for k in ['production_ready','global_green','source_patch','DoorControl_activated','AnimateItem_activated','natural_startup_proven','runtime_performed','gameplay_performed','publication_review_approved']:
  assert d[k] is False
 assert hashlib.sha256((R/'GAME/ITEMS.C').read_bytes()).hexdigest()==d['items_sha256']
 assert hashlib.sha256((R/'GAME/SETUP.C').read_bytes()).hexdigest()==d['setup_sha256']
 for path,key in g['OUTPUTS'].items():
  assert (R/path).read_text()==g[key]
 assert list(csv.DictReader(io.StringIO(g['CSV_TEXT'])))==[g['csv_row']()]
 assert '## Tracker' in g['STORY'] and '- [x]' in g['STORY'] and '- [ ]' in g['STORY']
 for text in [g[k] for k in g['OUTPUTS'].values()]+[g['SECTION']]:
  assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|payload_offset|word_le_hex|data:image|```(?:asm|mips|cpp|c)\b',text)
def test_failclosed_all_fields_and_types():
 g=api();good=g['metadata']()
 for k,v in good.items():
  bad=dict(good);bad[k]=not v if type(v) is bool else v+1 if type(v) is int else v+'changed'
  with pytest.raises(ValueError):g['validate'](bad)
 for bad in [{**good,'raw_opcode':'forbidden'},{k:v for k,v in good.items() if k!='cases'},{**good,'cases':4.0}]:
  with pytest.raises(ValueError):g['validate'](bad)
def test_append_only_exact_inverse_and_named_predecessors():
 g=api();b=(R/'docs/reverse/reconstruction-progress.html').read_bytes()
 successor815=runpy.run_path(str(R/'scripts/reverse/re815_publication.py'))
 if successor815['START'].encode() in b:b=successor815['dashboard_before_re815'](b)
 successor=runpy.run_path(str(R/'scripts/reverse/re814_publication.py'))
 if successor['START'].encode() in b:
  before=successor['dashboard_before_re814'](b)
  assert b==before+successor['SECTION'].encode()
  b=before
 prior=g['dashboard_before_re813'](b)
 assert hashlib.sha256(prior).hexdigest()==g['PRECEDING']
 assert b==prior+g['SECTION'].encode()
 for m in [b+b'foreign',b+g['SECTION'].encode(),b.replace(g['END'].encode(),b'',1),b.replace(b'RE-809',b'RE-xxx',1),b+ b'<!-- start re814 --><!-- end re814 -->']:
  with pytest.raises(AssertionError):g['dashboard_before_re813'](m)
 for n in ['re812_publication','re811_provenance']:
  old=runpy.run_path(str(R/('scripts/reverse/'+n+'.py')))
  fn=old['dashboard_before_re812' if '812' in n else 'dashboard_before_re811']
  assert hashlib.sha256(fn(b)).hexdigest()==old['PRECEDING']
  for m in [b+b'foreign',b.replace(b'RE-809',b'RE-xxx',1),b+g['SECTION'].encode()]:
   with pytest.raises(AssertionError):fn(m)
