"""Portable RE812 publication contract; private execution is not production approval."""
import csv, hashlib, io, runpy
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[2]
CSV=R/'docs/reverse/generated/re812-addactiveitem-characterization.csv'
def api():
    p=R/'scripts/reverse/re812_publication.py'
    assert p.exists(), 'RED: RE812 safe generator missing'
    return runpy.run_path(str(p))
def test_missing_metadata_red_then_exact_generated_publication():
    assert CSV.exists(), 'RED: RE812 characterization metadata missing'
    g=api(); text=CSV.read_text(); rows=list(csv.DictReader(io.StringIO(text)))
    assert len(rows)==1 and rows[0]==g['csv_row']()
    assert text==g['render_csv']()
    assert hashlib.sha256((R/'GAME/ITEMS.C').read_bytes()).hexdigest()==g['SOURCE']
    for path,key in [('docs/reverse/functions/re812-addactiveitem-composition.md','FUNCTIONDOC'),('docs/stories/RE-812-addactiveitem-characterization.md','STORY')]:
        assert (R/path).read_text()==g[key]
    assert '## Tracker' in g['STORY'] and '- [x]' in g['STORY'] and '- [ ]' in g['STORY']
def test_failclosed_metadata_mutants():
    g=api(); good=g['metadata'](); g['validate'](good)
    for key,value in [('production_ready',True),('historical_lock_compliance',True),('returns',191),('status','production-ready'),('verdict_sha256','f'*64),('control_callbacks_invoked',True),('interior_removal_tested',True)]:
        bad=dict(good); bad[key]=value
        with pytest.raises(AssertionError): g['validate'](bad)
    for bad in [{**good,'raw_opcode':'forbidden'}, {k:v for k,v in good.items() if k!='runtime_performed'}, {**good,'returns':192.0}]:
        with pytest.raises(AssertionError): g['validate'](bad)
def test_append_only_dashboard_and_failclosed_mutants():
    g=api(); b=(R/'docs/reverse/reconstruction-progress.html').read_bytes()
    successor814=runpy.run_path(str(R/'scripts/reverse/re814_publication.py'))
    if successor814['START'].encode() in b:
        before=successor814['dashboard_before_re814'](b)
        assert b==before+successor814['SECTION'].encode()
        b=before
    prior=g['dashboard_before_re812'](b)
    assert hashlib.sha256(prior).hexdigest()==g['PRECEDING']
    successor=runpy.run_path(str(R/'scripts/reverse/re813_publication.py'))
    if successor['START'].encode() in b:
        before=successor['dashboard_before_re813'](b)
        assert b==before+successor['SECTION'].encode()
        b=before
    assert b==prior+g['SECTION'].encode()
    start=g['START'].encode(); end=g['END'].encode()
    mutations=[b+b'foreign', b+g['SECTION'].encode(), b.replace(end,b'',1),b.replace(start,b'',1), b.replace(start,end,1),b.replace(b'RE-809',b'RE-xxx',1),b.replace(b'CURRENT RE811',b'ALTERED RE811',1),b.replace(b'PRIVATECHARACTERIZATIONPASS',b'production-ready',1)]
    for mutant in mutations:
        with pytest.raises(AssertionError):g['dashboard_before_re812'](mutant)
    old=runpy.run_path(str(R/'scripts/reverse/re811_provenance.py'))
    for mutant in mutations[:-1]:
        with pytest.raises(AssertionError):old['dashboard_before_re811'](mutant)
