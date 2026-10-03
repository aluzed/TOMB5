"""RE806 provenance migration: versioned bytes only, no raw snapshot or private input."""
import copy, hashlib, json, runpy
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
BASELINE='a1f7e696b08476bdcd3f616cef569e2ac99c6a1764b9c9086ee0304f1dd6545c'
CANDIDATE='359970bfdd33ee5342a60c96dbe06be649028e26918250c290850b34a21fd8c1'
RESET=b'\t\t\t\t\tj = 0;\n'
RANGE=b'\t\t\t\t\trange = &ranges[change->range_index];\n'
def guard():
    g=runpy.run_path(str(ROOT/'tests/reverse/test_re804_private_animation_change_checkpoint.py'))
    assert callable(g.get('re806_baseline_from_approved_source')), 'RED: exact successor reconstruction guard missing'
    return g['re806_baseline_from_approved_source']
def source():
    return (ROOT/'SPEC_PSXPC_N/CONTROL_S.C').read_bytes()
def metadata():
    return json.loads((ROOT/'docs/reverse/generated/re806-getchange-integration.json').read_text())
def test_exact_approved_candidate_reconstructs_frozen_baseline():
    b=source(); assert hashlib.sha256(b).hexdigest()==CANDIDATE
    restored=guard()(b,metadata())
    assert hashlib.sha256(restored).hexdigest()==BASELINE
    assert b==restored.replace(RANGE,RESET+RANGE,1)
def test_reject_second_unrelated_source_mutation():
    check=guard()
    with pytest.raises(AssertionError): check(source()+b'\n',metadata())
@pytest.mark.parametrize('kind',['missing','duplicate','moved'])
def test_reject_reset_transformation_mutants(kind):
    b=source(); assert b.count(RESET+RANGE)==1
    if kind=='missing': b=b.replace(RESET+RANGE,RANGE,1)
    elif kind=='duplicate': b=b.replace(RESET+RANGE,RESET+RESET+RANGE,1)
    else: b=b.replace(RESET+RANGE,RANGE+RESET,1)
    check=guard()
    with pytest.raises(AssertionError): check(b,metadata())
@pytest.mark.parametrize('key,value',[
    ('schema','forged'),('integration_approved',False),('source_integrated',False),
    ('integration_approved',1),('source_sha256',BASELINE),
    ('integration_review_sha256','0'*64),('only_integrated_delta','unrelated')])
def test_reject_forged_successor_metadata(key,value):
    d=copy.deepcopy(metadata());d[key]=value
    check=guard()
    with pytest.raises(AssertionError): check(source(),d)
def test_historical_baseline_pin_is_not_replaced():
    g=runpy.run_path(str(ROOT/'tests/reverse/test_re804_private_animation_change_checkpoint.py'))
    assert g['FROZEN']['SPEC_PSXPC_N/CONTROL_S.C']==BASELINE
