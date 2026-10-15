"""Documentary contract only; no native execution or production approval."""
import copy, hashlib, json, re, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PATHS=['docs/stories/RE-955-cd-init-handler-checkpoint.md', 'docs/reverse/generated/re955_cd_init_handler_checkpoint.json', 'docs/reverse/tomb5-progress-dashboard-re955-v1.html', 'tests/reverse/test_re955_cd_init_handler_checkpoint.py']
EXPECTED={'ticket': 'RE955', 'scope': 'private constructed Init handler checkpoint; metadata-only publication', 'redux_pin': 'c313b116e6a55786bc127c9b3a07a90b55d97c21', 'openbios_pin': '7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30', 'producer_manifest': '827b2b77dce087bb88d35cd07525c7f1cf9696fb3204ba97823a63c031f1e6d2', 'review_manifest': '7ecd959ba26cbc5364c77bb138c5511a5c7c3f1bd9f97b426afdb9037855ab77', 'producer_members': 254, 'review_members': 183, 'finite_review': 'SCOPED_PASS', 'strict_review': 'INCOMPLETE', 'procedure_review': 'INCOMPLETE', 'publication_review_snapshot': 'PENDING', 'integration': False, 'production_patch': False, 'new_frontier_executed': False, 'handler_body_executed': True, 'openbios': {'return': 0, 'result': 'host timeout before CPU; not success', 'host_cpu_cycles': [0, 0], 'bios_irq_delivery': False}, 'observations': {'ack': {'cause': 3, 'payload': [2], 'cycle': 26996}, 'delay_ms': 120, 'delay_cycles': 4064256, 'complete': {'cause': 2, 'payload': [2], 'cycle': 4091252}, 'irq_facade': {'operation': 'OR', 'start': 4, 'final': 5, 'counter_bit': 1}, 'fetches_per_control': 2045626, 'hsyncs_per_control': 1906}, 'review_fresh': {'builds': 10, 'native_runs': 10, 'oracle_acceptances': 2, 'mutant_rejections': 8, 'native_mutant_exit': 0, 'oracle_mutant_exit': 1, 'modes': ['normal', 'UBSan'], 'mutants': ['no_schedule', 'wrong_delay', 'no_irq', 'wrong_complete']}, 'author_archived': {'mutants': 6, 'modes': 2, 'rejections': 12, 'replayed_for_publication': False}, 'historical_procedure': {'worker_timeout_seconds': 600, 'recovery_closure_seconds': 246.28, 'recovery_budget_seconds': 240, 'review_dispatch_seconds': 491.03, 'review_reserve_seconds': 100, 'review_reserve_respected': False, 'review_first_renderer_seconds_approx': 447, 'failures_gaps_warnings_retained': True}, 'limits': ['constructed CPU/MMIO/memory/audio fixture, not natural startup', 'source excerpts, not full CD TU or OpenBIOS ABI', 'IRQ OR facade, not genuine IRQ delivery to BIOS', 'no real sector, Sony firmware, hardware or gameplay', 'no injected success or preseeded response; open handlers produce responses'], 'next_frontier': 'coexecute OpenBIOS wait and CPU with genuine IRQ producer; not executed'}
STORY_SHA='80a3d3202e81a3518573aba213a58311cf5ab4567108681dac4e839809cf9665'
DASH_SHA='99ad69c46272299831b076258e5208554baa940417ddca428fe0926892b80824'
def exact(actual, expected):
    if type(actual) is not type(expected): raise ValueError('type')
    if isinstance(expected,dict):
        if set(actual)!=set(expected): raise ValueError('keys')
        for k in expected: exact(actual[k],expected[k])
    elif isinstance(expected,list):
        if len(actual)!=len(expected): raise ValueError('length')
        for a,b in zip(actual,expected): exact(a,b)
    elif actual!=expected: raise ValueError('value')
def guard(path, text):
    if re.search(r'<(?:script|iframe|object)\b|javascript\x3a|onload\s*=|-----BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{16}',text,re.I): raise ValueError('unsafe')
    if re.search(r'0x[0-9a-f]{8}|(?:raw_opcodes|sector_dump)\s*[:=]',text,re.I): raise ValueError('raw payload')
    if path.suffix in ('.html','.md'):
        links=re.findall(r'href=["\']([^"\']+)',text)+re.findall(r'\]\(([^)]+)\)',text)
        for link in links:
            if ':' in link or link.startswith(('/', '#')): raise ValueError('nonlocal')
            target=(path.parent/link).resolve()
            if not target.is_relative_to(ROOT) or not target.is_file(): raise ValueError('link')
def leaves(v,p=()):
    if isinstance(v,dict):
        for k,x in v.items(): yield from leaves(x,p+(k,))
    elif isinstance(v,list):
        for k,x in enumerate(v): yield from leaves(x,p+(k,))
    else: yield p,v
def replace(v,p,x):
    out=copy.deepcopy(v); cursor=out
    for k in p[:-1]: cursor=cursor[k]
    cursor[p[-1]]=x; return out
class Contract(unittest.TestCase):
    def test_metadata(self): exact(json.loads((ROOT/PATHS[1]).read_text()),EXPECTED)
    def test_document_bytes(self):
        for path,want in [(PATHS[0],STORY_SHA),(PATHS[2],DASH_SHA)]: self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),want)
    def test_leaf_value_and_type_mutations(self):
        for p,v in leaves(EXPECTED):
            wrong=not v if type(v)is bool else v+1 if type(v)in(int,float) else v+'!'
            wrongtype=int(v) if type(v)is bool else bool(v) if type(v)is int else str(v) if type(v)is float else 0
            for x in (wrong,wrongtype):
                with self.subTest(path=p,value=x),self.assertRaises(ValueError): exact(replace(EXPECTED,p,x),EXPECTED)
    def test_nested_schema_counts(self):
        def walk(v,p=()):
            if isinstance(v,dict):
                for k,x in v.items():
                    bad=copy.deepcopy(v); del bad[k]
                    with self.assertRaises(ValueError): exact(bad,v)
                    yield from walk(x,p+(k,))
                bad=copy.deepcopy(v); bad['unexpected']=False
                with self.assertRaises(ValueError): exact(bad,v)
            elif isinstance(v,list):
                with self.assertRaises(ValueError): exact(v[:-1],v)
                for x in v: yield from walk(x,p)
            yield None
        list(walk(EXPECTED))
    def test_public_safety_and_links(self):
        for p in PATHS: guard(ROOT/p,(ROOT/p).read_text())
    def test_same_path_guard_negative_controls(self):
        path=ROOT/PATHS[2]
        for text in ['<scr'+'ipt>alert(1)</scr'+'ipt>','<a href="../../../build/private.json">bad</a>','<a href="missing.json">bad</a>','raw_'+'opcodes: forbidden','AKIA'+'A'*16]:
            with self.subTest(text=text),self.assertRaises(ValueError): guard(path,text)
if __name__=='__main__': unittest.main()
