"""Standalone public documentary contract. No native execution."""
import copy,hashlib,json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PATHS=['docs/stories/RE-956-cd-init-reviewed-frontiers.md', 'docs/reverse/generated/re956_cd_init_reviewed_frontiers.json', 'docs/reverse/tomb5-progress-dashboard-re956-v1.html', 'tests/reverse/test_re956_cd_init_reviewed_frontiers.py', 'docs/stories/blocked/BLOCKED-008-re956-mips-allocator-engine-handoff.md']
EXPECTED={'ticket': 'RE956', 'kind': 'metadata-only documentary checkpoint', 'publication_review_snapshot': 'PENDING', 'strict': 'INCOMPLETE', 'procedure': 'INCOMPLETE', 'integration': False, 'production_patch': False, 'new_native_replay': False, 'new_RE': False, 'pins': {'redux': 'c313b116e6a55786bc127c9b3a07a90b55d97c21', 'openbios': '7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30'}, 'archives': [{'root': 'cd-init-unit16', 'manifest_sha256': '8337c79ad14643dafc723c8b44247e3f1997cb2d999902e4b6c2e21ece4129a8', 'members': 115}, {'root': 'cd-init-unit16-review', 'manifest_sha256': 'f6ef8180d81615f329647026a38d96e500bbe24fc5c4da07bfeb71e689fbb8e7', 'members': 134}, {'root': 'cd-init-unit17', 'manifest_sha256': 'b646ab88b1425c8d988264b7d701fd6684ac3e00a9791cd5b324e7a206abeeff', 'members': 153}, {'root': 'cd-init-unit17-review', 'manifest_sha256': 'd2b9b4439ecea1f2df589f399b4dadbab04236823038dd2d01cbe42629a6101c', 'members': 324}, {'root': 'cd-init-unit18', 'manifest_sha256': '685ed686dc74e6598d8fa10cc639dc0db475606104bfcda2c279bfb9fd1183be', 'members': 270}, {'root': 'cd-init-unit18-review', 'manifest_sha256': 'c7bfb65c825b55cd33810f7ef2dc003dac733d505e5f001c0970dfbd100f1ffb', 'members': 123}], 'unit16': {'finite': 'SCOPED_PASS', 'delivery': 'conditional HOST polling after CPU; genuine OpenBIOS ACK and Complete consumption', 'fresh_review_builds': 5, 'fresh_review_native_runs': 5, 'positive_controls': 2, 'normal_mutants': 3, 'native_mutant_exit': 0, 'oracle_mutant_exit': 1, 'natural_cpu_irq': False, 'ack_cycle': 26996, 'complete_cycle': 4091252}, 'unit17': {'finite': 'SCOPED_PASS', 'delivery': 'genuine Memory IRQ from cdlInit ACK through actual CPU branchTest and architectural exception tail', 'fresh_review_builds': 4, 'fresh_review_native_runs': 4, 'positive_controls': 2, 'normal_mutants': 2, 'native_mutant_exit': 0, 'oracle_mutant_exit': 1, 'fresh_vector_elf_identical': True, 'CP0_effect_checked': True, 'vector_instructions_retired': 4, 'handler_nops_retired': 4, 'total_instructions_retired': 8, 'attempted_fetch_addresses': 9, 'ninth_fetch_retired': False, 'fixture_initial_CP0_Status': True, 'fixture_vector_handler_placement': True, 'complete_handler_executed': False, 'natural_boot': False}, 'unit18': {'finite_attempt': 'SCOPED_PASS_DIAGNOSTIC_ONLY', 'producer_consumer_objective': 'INCOMPLETE', 'positive_GREEN': 0, 'engine': 'Unicorn 2.1.4 MIPS32; different engine, not continuation of unit17', 'full_unchanged_target_TUs': ['threads.c', 'alloc.c'], 'abi': 'MIPS R3000 o32 little-endian; linked with GC', 'caller': 'private heap -> kern_initheap -> initThreads -> B0Handler -> kern_malloc', 'fresh_review_elf_identical': True, 'fresh_native_exit': 0, 'fresh_oracle_exit': 1, 'hook_visits': 105, 'hook_visit_is_retirement': False, 'processBlockSize': 4, 'process_pointer': 0, 'thread_pointer': 0, 'consumer_executed': False, 'error': 'UC_ERR_EXCEPTION', 'diagnostic_engine_exception': 20, 'engine_exception_is_hardware_CP0_Cause': False, 'last_branch_legal': True, 'micro_branch_pass_is_full_state_solution': False, 'no_PC_read_hook_unblocks': False, 'alternatives_failed': ['O2', '24KC', 'separated data'], 'UBSan': 'target compile only; freestanding link fails missing runtime; NOT PASS'}, 'distinctions': {'unit17_vector_composed_with_unit16_handler': False, 'unit18_continues_unit17_CPU': False, 'innerInit_return': 0, 'innerInit_return_before_CPU': True, 'innerInit_success': False, 'full_CPU_TU': False, 'Sony_hardware_gameplay': False}, 'historical_limits': ['bootstrap and authoring ledger gaps retained', 'timeout and doublelock failures retained', 'oracle corrections and read3 warnings retained', 'unit17 postseal clock and no-persistent-jobs qualifications retained without seal rewrite'], 'blocker': 'BLOCKED-008', 'next_gate': 'isolate full engine state and delay-slot retirement or validated alternate engine with same ELF and inputs; genuine allocator returns and pointers before consumer', 'global_blocker_terminal': False}
DOC_HASHES={'docs/stories/RE-956-cd-init-reviewed-frontiers.md': 'fab54108f6d1b8eb2e2fc207e42659394b120177a21a8be7b3bdd805dbb7164c', 'docs/reverse/tomb5-progress-dashboard-re956-v1.html': '48ea2f088bb024da2c472c7bc9f848c64f5230d18a7b8ade7326e3efc6e58da5', 'docs/stories/blocked/BLOCKED-008-re956-mips-allocator-engine-handoff.md': '63b79fcba9e0a4d1552095bdcd76191953a4c91e20912bc253fc7c8077f35a34'}
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
def handoff_recipe(text):
    commands=re.findall(r'`([^`]+)`',text)
    required=[
        'python3 -m venv .venv',
        '.venv/bin/python -m pip install unicorn==2.1.4',
        'PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -c "import unicorn; from unicorn import mips_const; assert unicorn.__version__ == \'2.1.4\'; print(unicorn.__version__, unicorn.__file__)"',
        'PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B engine-v2.py green >green-native.stdout 2>green-native.stderr',
        'PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B oracle.py green-native.stdout >green-oracle.stdout 2>green-oracle.stderr',
    ]
    import shlex
    parsed=[shlex.split(c) for c in commands]
    for c in required:
        if shlex.split(c) not in parsed: raise ValueError('missing exact future command: '+c)
    positions=[parsed.index(shlex.split(c)) for c in required]
    if positions != sorted(positions): raise ValueError('provision before replay')
    for phrase in ['cwd = root neuf', 'aucun deps copié', 'native_exit=$?', 'oracle_exit=$?', 'native_exit=0', 'oracle_exit=1', 'non exécutée']:
        if phrase not in text: raise ValueError('missing future gate: '+phrase)

class Contract(unittest.TestCase):
    def test_metadata(self): exact(json.loads((ROOT/PATHS[1]).read_text()),EXPECTED)
    def test_document_bytes(self):
        for p,h in DOC_HASHES.items(): self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)
    def test_all_leaf_mutations(self):
        for p,v in leaves(EXPECTED):
            wrong=not v if type(v)is bool else v+1 if type(v)is int else v+'!'
            wrongtype=int(v) if type(v)is bool else bool(v) if type(v)is int else 0
            for x in (wrong,wrongtype):
                with self.subTest(path=p),self.assertRaises(ValueError): exact(replace(EXPECTED,p,x),EXPECTED)
    def test_nested_exact_schema(self):
        def walk(v):
            if isinstance(v,dict):
                for k,x in v.items():
                    bad=copy.deepcopy(v);del bad[k]
                    with self.assertRaises(ValueError):exact(bad,v)
                    walk(x)
                with self.assertRaises(ValueError):exact(dict(v,unexpected=False),v)
            elif isinstance(v,list):
                with self.assertRaises(ValueError):exact(v[:-1],v)
                for x in v:walk(x)
        walk(EXPECTED)
    def test_public_safety_and_links(self):
        handoff_recipe((ROOT/PATHS[4]).read_text())
        for p in PATHS:guard(ROOT/p,(ROOT/p).read_text())
    def test_negative_guards(self):
        for text in ['<scr'+'ipt>bad</scr'+'ipt>','<a href="../../../build/private.json">bad</a>','<a href="missing.json">bad</a>','raw_'+'opcodes: forbidden','AKIA'+'A'*16]:
            with self.assertRaises(ValueError):guard(ROOT/PATHS[2],text)
        text=(ROOT/PATHS[4]).read_text()
        for old,new in [('engine-v2.py green >','engine-v2.py green.elf >'),(' >green-native.stdout',''),('unicorn==2.1.4','unicorn')]:
            self.assertIn(old,text)
            with self.subTest(mutation=old),self.assertRaises(ValueError): handoff_recipe(text.replace(old,new))
if __name__=='__main__':unittest.main()
