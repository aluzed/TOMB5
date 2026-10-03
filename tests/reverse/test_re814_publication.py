"""Portable safe metadata contract; no private runtime dependency."""
import csv, hashlib, io, re, runpy
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[2]
PRECEDING='5c7b6d809cf6ffc00890ed0de5ee9744bc62579e10a742c67c218a13e943b081'
SECTION='<!-- start re814-bounded-continuation --><section id="re814"><h2>RE-814 — BOUNDED_CONTINUATION_CHARACTERIZATION</h2><p>Private corrected independent PASS scoped; original FAILED/noncertifié unchanged. 8 cases, 4 complete target returns and 4 stops BEFORE initializer, 3696 hook visits. Native i386 O0 normal + ASan/UBSan failfast: 8 returns/mode, status/room/floor 8/8, full 582 bytes 6/8; 2 expected active/head differences: native registration absent.</p><p>Authentic literal producer without initializer/controller injection; t9 GP/SP constructed. Generic target stop and native complete have different semantic frontiers; MIP complete. ITEM_ACTIVE rewritten after Add NULL without active/head activation. No production patch, activation, behavioral RED, startup, wholeRAM, hardware, gameplay or global GREEN. Original RE813 FAILED preserved. BLOCKED-006 remains; RE815 natural ObjectObjects producer entry and generic initializer dependencies NOT executed. Publication review pending. <a href="../stories/RE-814-bounded-continuation.md">Story</a> · <a href="functions/re814-bounded-continuation.md">Contract</a> · <a href="generated/re814-bounded-continuation.csv">CSV</a>.</p></section><!-- end re814-bounded-continuation -->\n'
def api():
 p=R/'scripts/reverse/re814_publication.py'
 assert p.exists(), 'RED: safe RE814 generator absent'
 return runpy.run_path(str(p))
def test_metadata_counts_limits_and_artifacts():
 g=api();d=g['metadata']();g['validate'](d)
 assert [d[k] for k in ['cases','target_complete_returns','target_initializer_stops','hook_visits','native_returns_per_mode','status_room_floor_equal_per_mode','full582_equal_per_mode','active_head_differences_per_mode']]==[8,4,4,3696,8,8,6,2]
 assert d['corrected_verdict_sha256']=='b4c4ded966675715a1096e98ef9571351f59703e43a16c3c2ce0fb788f7cbfd7'
 assert d['corrected_manifest_sha256']=='7bcd98de7a6bb4dc9b7f7932205a84748102e571249571fc1d1e2608b686fc02'
 assert d['corrected_review']=='PASS_scoped' and d['original_review']=='FAILED/noncertifié' and d['upstream_re813_original_review']=='FAILED'
 for k in ['source_patch','production_ready','global_green','publication_review_approved','behavioral_red','initializer_executed','controller_invoked','whole_startup_proven','whole_ram_proven','hardware_proven','gameplay_performed','fullbuild_performed','runtime_performed','DoorControl_activated','AnimateItem_activated','t7_t8_injected','re815_executed']:
  assert d[k] is False
 assert d['semantic_frontiers']=='generic target BEFORE initializer vs native complete; MIP target complete'
 assert d['constructed_registers']=='t9 GP SP' and d['status_rewrite']=='ITEM_ACTIVE after Add NULL without active/head activation'
 for p,k in [('GAME/ITEMS.C','items_sha256'),('GAME/SETUP.C','setup_sha256')]:
  assert hashlib.sha256((R/p).read_bytes()).hexdigest()==d[k]
 assert g['SECTION']==SECTION and g['PRECEDING']==PRECEDING
 for p,k in g['OUTPUTS'].items():assert (R/p).read_text()==g[k]
 assert list(csv.DictReader(io.StringIO(g['CSV_TEXT'])))==[g['csv_row']()]
 assert '- [x]' in g['STORY'] and '- [ ]' in g['STORY']
 for text in [g[k] for k in g['OUTPUTS'].values()]+[SECTION]:
  assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|payload_offset|word_le_hex|data:image|```(?:asm|mips|cpp|c)\b',text)
def test_exact_schema_types_fail_closed():
 g=api();good=g['metadata']()
 for k,v in good.items():
  bad=dict(good);bad[k]=not v if type(v) is bool else v+1 if type(v) is int else v+'changed'
  with pytest.raises(ValueError):g['validate'](bad)
 for bad in [{**good,'raw_opcode':'forbidden'},{k:v for k,v in good.items() if k!='cases'},{**good,'cases':8.0}]:
  with pytest.raises(ValueError):g['validate'](bad)
def test_append_only_exact_inverse():
 g=api();b=(R/'docs/reverse/reconstruction-progress.html').read_bytes();prior=g['dashboard_before_re814'](b)
 assert hashlib.sha256(prior).hexdigest()==PRECEDING and b==prior+SECTION.encode()
 for m in [b+b'foreign',b+SECTION.encode(),b.replace(g['END'].encode(),b'',1),b.replace(b'RE-809',b'RE-xxx',1)]:
  with pytest.raises(AssertionError):g['dashboard_before_re814'](m)
def test_predecessor_guards_accept_only_exact_named_re814():
 b=(R/'docs/reverse/reconstruction-progress.html').read_bytes()
 if SECTION.encode() not in b:b+=SECTION.encode()
 for name,fn in [('re813_publication','dashboard_before_re813'),('re812_publication','dashboard_before_re812'),('re811_provenance','dashboard_before_re811')]:
  old=runpy.run_path(str(R/('scripts/reverse/'+name+'.py')))
  assert hashlib.sha256(old[fn](b)).hexdigest()==old['PRECEDING']
  for m in [b+b'foreign',b+SECTION.encode(),b.replace(b'RE-809',b'RE-xxx',1),b.replace(b'3696 hook',b'3697 hook',1),b.replace(b'<!-- end re814-bounded-continuation -->',b'',1)]:
   with pytest.raises(AssertionError):old[fn](m)
