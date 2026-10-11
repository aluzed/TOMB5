"""Public metadata contract: never requires ignored private proof or reruns helpers."""
import copy
import hashlib
import importlib.util
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'scripts/reverse/re882_publication.py'

def api():
    assert SCRIPT.exists(), 'RED: RE882 deterministic metadata generator absent'
    s = importlib.util.spec_from_file_location('re882', SCRIPT)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

def test_exact_schema_archived_counts_and_scope():
    m = api()
    d = m.metadata()
    assert d['schema'] == 're882-reviewed-private-proof-publication-v1'
    assert d['publication_review'] == 'PENDING_INDEPENDENT_EXACT_HASH_REVIEW'
    assert d['integration'] is False
    assert d['historic_re879'] == {'content_scope': 'PASS', 'global_scope': 'FAIL', 'procedure': 'FAIL_LEDGER_AND_NESTED_LOCK', 'integration': False}
    a,b = d['archived_private_results']
    assert a['ticket'] == 'RE880' and a['fixtures'] == 48 and a['direct'] == 32 and a['compose'] == 16
    assert a['target_calls_per_executor'] == 80 and a['native_processes_per_executor'] == 384
    assert a['baseline_returned_red'] == a['candidate_green'] == 96
    assert a['approved_verdict_sha256'] == 'e34b91f4e66df6f3c7081088fec501a66a3cc974e1c84d5108eb6b1ed66e4f07'
    assert b['ticket'] == 'RE881' and b['fixtures'] == 72 and b['depths'] == [1,15,30]
    assert b['baseline_returned_red'] == 120 and b['baseline_ubsan_aborts_not_returns'] == 24
    assert b['candidate_green'] == 144 and b['native_processes_per_executor'] == 504
    assert b['target_calls_per_engine'] == 144 and b['producer_target_engines'] == 2
    assert b['approved_verdict_sha256'] == '769611ea40940e0e2156038c2e74e3aaef5e32a1eed8c2a63b0d1bc498087cdc'
    assert a['procedure'] == 'FAIL_LEDGER_COVERAGE_AND_PREFLIGHT_INCIDENTS'
    assert b['procedure'] == 'FAIL_LEDGER_GAPS_AND_PREFLIGHT_INCIDENTS'
    for row in (a,b):
        assert row['execution_attribution'] == 'ARCHIVED_PRIVATE_PRODUCER_AND_INDEPENDENT_REVIEWER'
        assert row['global_scope'] == 'FAIL_HISTORIC_D9_AND_UNPROVEN_FRONTIERS'
        assert row['full_ram_bytes'] == 2097152 and row['gte_bytes'] == 384 and row['each_stack_bytes'] == 1024
        assert row['integration'] is False
    assert m.validate(d) == d
    assert m.metadata() == d

@pytest.mark.parametrize('mutation', ['unknown','count','scope','type','pin','abort','integration'])
def test_schema_drift_rejected(mutation):
    m = api(); d = m.metadata()
    if mutation == 'unknown': d['raw_opcode'] = 'forbidden'
    if mutation == 'count': d['archived_private_results'][0]['fixtures'] = 49
    if mutation == 'scope': d['archived_private_results'][1]['global_scope'] = 'PASS'
    if mutation == 'type': d['integration'] = 0
    if mutation == 'pin': d['archived_private_results'][0]['approved_verdict_sha256'] = '0'*64
    if mutation == 'abort': d['archived_private_results'][1]['baseline_ubsan_aborts_not_returns'] = 0
    if mutation == 'integration': d['integration'] = True
    with pytest.raises(ValueError): m.validate(d)

def test_outputs_deterministic_and_checked_in():
    m = api(); before = (ROOT / m.PRIOR_DASHBOARD).read_bytes()
    one = m.render(before); two = m.render(before)
    assert one == two
    assert set(one) == set(m.OUTPUT_PATHS)
    for name, data in one.items():
        assert (ROOT/name).read_bytes() == data
        m.guard_output(name, data)
    assert m.preceding_dashboard(one[m.DASHBOARD]) == before
    assert hashlib.sha256(before).hexdigest() == '7a53c9a86444ede3ace0a6ea23a30d5d004b16d744e7139272b4cdfcf40ea9fc'

@pytest.mark.parametrize('mutation', ['history','missing','duplicate','altered','trailing','unknown'])
def test_versioned_dashboard_fails_closed(mutation):
    m = api(); data = m.render((ROOT/m.PRIOR_DASHBOARD).read_bytes())[m.DASHBOARD]
    section = m.SECTION.encode()
    if mutation == 'history': data = b'foreign'+data
    if mutation == 'missing': data = data.replace(b'<!-- RE882 PUBLICATION END -->', b'')
    if mutation == 'duplicate': data = data[:-7]+section+b'</html>'
    if mutation == 'altered': data = data.replace(section, section.replace(b'ARCHIVED', b'FRESH'))
    if mutation == 'trailing': data += b'foreign'
    if mutation == 'unknown': data = data[:-7]+b'<!-- RE883 -->'+b'</html>'
    with pytest.raises(ValueError): m.preceding_dashboard(data)

@pytest.mark.parametrize('bad', [b'0x80012345', b'FUN_80012345', b'word_le_hex', b'raw_opcode', b'data:image/png;base64,', b'-----BEGIN '+b'PRIVATE KEY-----', b'ghp_'+b'a'*30, b'```mips\n', b'\x00'])
def test_raw_secret_added_content_rejected(bad):
    m = api()
    with pytest.raises(ValueError): m.guard_added('docs/stories/RE-882-reviewed-private-proof-publication.md', bad)

@pytest.mark.parametrize('path', ['SPEC_PSXPC_N/MATHS.C','build/reverse/proof.bin','assets/new.png','docs/reverse/proof.exe','../escape.md'])
def test_stage_scope_and_heavy_files_rejected(path):
    with pytest.raises(ValueError): api().guard_added(path, b'safe prose')

def test_documentation_acceptance_and_frontier_not_integration():
    m = api(); outputs = m.render((ROOT/m.PRIOR_DASHBOARD).read_bytes())
    for ticket in ['880','881','882']:
        path = next(p for p in outputs if p.startswith('docs/stories/RE-'+ticket+'-'))
        text = outputs[path].decode()
        for phrase in ['## Progression', '## Evidence', '## Blockers', '## Acceptance', '- [x]', '- [ ]', 'integration=false', 'ARCHIVED', 'RE883']:
            assert phrase in text, (path,phrase)
    assert b'five static caller candidates are not executed' in outputs[m.REPORT]
    assert b'GetSpheres public stub' in outputs[m.REPORT]
    assert b'GetBestFrame/GetFramesCL private and unintegrated' in outputs[m.REPORT]
    assert b'legacy RE830 predecessor guards: two failures preserved' in outputs[m.REPORT]

def test_public_source_and_legacy_dashboard_pins():
    m = api()
    for path, pin in m.PRESERVED.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == pin
