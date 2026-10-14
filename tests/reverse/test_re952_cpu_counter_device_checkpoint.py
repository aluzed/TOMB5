"""Standalone public metadata contract, no private imports or behavioral replays."""
import copy
import hashlib
import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PATHS=['docs/stories/RE-952-cpu-counter-device-composition-checkpoint.md', 'docs/reverse/generated/re952_cpu_counter_device_checkpoint.json', 'docs/reverse/tomb5-progress-dashboard-re952-v1.html', 'tests/reverse/test_re952_cpu_counter_device_checkpoint.py']
EXPECTED={'schema': 're952.cpu-counter-device.checkpoint.v1', 'private_finite': 'PASS', 'global_strict_passed': False, 'procedure': 'INCOMPLETE', 'public_gate': 'PENDING', 'integration': False, 'production_patch': False, 'new_cpu_replays': 0, 'new_native_builds': 0, 'cpu_frontier_unchanged': True, 'branchTest03_certified': False, 'source': {'name': 'PCSX-Redux', 'revision': 'c313b116e6a55786bc127c9b3a07a90b55d97c21', 'license': 'GPL-2.0-or-later', 'publication': 'no source copied'}, 'authentication': [{'name': 'cd-init-unit08', 'members': 111, 'manifest_sha256': 'e3045f9e1ee78bc81da9ecfc3335a0236d9942e3501eb0240345c2f013dd143e', 'selected_hashes': {'HANDOFF.md': 'e304de99d3ec3b0b0c2cd6a37724cdf3ab5759cf59d30ae84813d59445dfcd83', 'acceptance.json': '8e2d29d3c8c75231c27653b47963b2c53697b4efacbf1bdcd78b506697fc5976', 'verdict.json': '023f5f65cbae948fab94c2efc19d3c31a82528045e0b593908cf09d17743749d'}}, {'name': 'cd-init-unit08-review', 'members': 175, 'manifest_sha256': '88e49dbcbb09e0664bb897cade803096fad7f0a2bf6d7770fb68b5055c489719', 'selected_hashes': {'HANDOFF.md': '37b1f3437805f13621bc7bd2f7896df569faa235e242d0b137cdab95262135ce', 'acceptance.json': '9a10065f6a72d45bb1a87f30cfca670e66ad7c0375aeff7ce76e80146756c27b', 'verdict.json': '681af331da2740869326cde0ec2ad418e049b9471816565ecccf0c5014eb8807'}}, {'name': 'cd-init-unit09', 'members': 82, 'manifest_sha256': '445707c88a1669136190bdf5ea59543c696d983b77dcdd3132f6bb34dce913ca', 'selected_hashes': {'HANDOFF.md': '54fa108496690a6a5da0bdae2c78691b1a83a777d2537b5c634304b4d14edcad', 'acceptance.json': 'f3bceda26648d786505dc5b6979314813260bb359afb470c49f99eafcf1a2a95', 'verdict.json': '496a3b0c17cf5543d0fbf4dd155ab650d3548d1a60419e389d717a92a5a88403'}}, {'name': 'cd-init-unit09-review', 'members': 277, 'manifest_sha256': '66e7f8f681804e275ece11becd8934bff5d9a8d4afaef3769aeb630d639f9b2d', 'selected_hashes': {}}, {'name': 'cd-init-unit09-review-closure', 'members': 296, 'manifest_sha256': 'b6c540ea778f647f5410f0017c4c3bb8e6c58edcb070b173a85eb392d64ce188', 'selected_hashes': {'HANDOFF.md': '5380391cdd0d42690d1280238698bbac78ab691bc7078adf127f4e24e9d957ca', 'acceptance.json': 'fe4be0e02d9ca47979eb59cbefa440d8ab53ab61197cd5e1eeb367477af90ff5', 'verdict.json': '3559de63f89a95a66430f5e8caa98eda5ec90344637cd6cb44c264a9801f25ca'}}, {'name': 'cd-init-unit10', 'members': 190, 'manifest_sha256': '8f27642c4ec778fe0410aa1350da846baffd1c78105b0e94459772593dca35d5', 'selected_hashes': {'HANDOFF.md': 'aa9b173e9b62718eed57e7c54ac3a3bf37bb5f0163e7f2d2a3849aff42b4baa4', 'acceptance.json': 'df7e604ea1a07f739d2bd803ee902639934b510c5a722d63e948b16cabf0dcfd', 'verdict.json': 'd8860c60fb227688c0fc5860b63b719221229351bc587570e1a3db2b1f68a691'}}, {'name': 'cd-init-unit10-review', 'members': 530, 'manifest_sha256': '3b14ced2b90949729d90ed906b9e9faa3c43687a6d9b80249247cd649889665d', 'selected_hashes': {'HANDOFF.md': '8f3f68cb8309b742f8efe4887a9202a5b2ca5f111a273e24a102e0618cb2170f', 'acceptance.json': '07ddea57ac975c1530cd6bbe86e5ea4c9c7a4f6e64861f640a6bef5335b5aab6', 'verdict.json': 'fd866fd9902e78563a2e800f77af816e4c7dee8895bf2308f974cd341c4f5e59'}}], 'units': [{'unit': '08', 'finite': 'PASS', 'strict_passed': False, 'review_assertions': 720, 'normal_runs': 4, 'UBSan_runs': 4, 'assertion_mutants': 2, 'scope': 'real continuous SDL device to unchanged full counter TU and genuine header with -fno-access-control; constructed JSON settings and CPU delta; adapted providers; audio excerpt not full TU', 'preserved_refusal': 'author private/public header alteration and missing strict schema; fresh genuine-header review does not erase refusal'}, {'unit': '09', 'finite': 'PASS', 'strict_passed': False, 'author_instructions_each': 30, 'author_assertions_each_build': 1140, 'author_normal_runs': 5, 'author_strict_runs': 5, 'review_additional_cases_each_build': 12, 'review_arithmetic_edges_each_build': 9, 'scope': 'byte-exact branchless CPU excerpts execBlock<true,false>; adapted class header memory observer; constructed program/state; not full CPU TU or ABI', 'preserved_refusal': 'initial reviewer 277-member incomplete root retained; separate 296-member closure; historical bootstrap and ledger gaps'}, {'unit': '10', 'finite': 'PASS', 'strict_passed': False, 'branch_cases_each_mode': 8, 'branch_comparisons_author': 120, 'branch_modes': ['normal', 'ASan+UBSan failfast nonPIE'], 'accepted_branch_assertion_mutants': ['no_transfer', 'no_cycle'], 'mixed_branch_control': {'name': 'wrong_target', 'assertion_rejections': 4, 'SIGABRT': 4, 'counted_as_uniform_assertion_mutant': False}, 'excluded_crash_controls': ['no_slot', 'wrong_condition'], 'composition_modes': ['normal', 'UBSan failfast'], 'composition_assertion_mutants': ['no_forward', 'no_wait'], 'constructed_blocks': 846720, 'observed_fetches': 1693440, 'produced_cycles': 3386880, 'cycles_injected': False, 'full_counter_oracle': True, 'scope': 'continuous nondebug BEQ/BNE and delay-slot excerpts with constructed RAM/ROM program; produced clock forwarded into adapted counter facade; unchanged full counter TU genuine header; real continuous SDL dummy device; ordered previousCycles before wait audioFrames after wait, four counters hsync next event; not natural scheduler', 'chronology': 'branch author RED then GREEN; composition GREEN then ablations is characterization not corrective TDD'}], 'next_dependency': 'ACTUAL_CPU_BRANCHTEST_SCHEDULER_COUNTER_CALLSITE_AND_NATURAL_SYSTEM_CONFIG', 'not_proven': ['natural GUI', 'System settings loader', 'natural scheduler', 'complete CPU TU ABI', 'global startup', 'CD success', 'gameplay', 'hardware'], 'cleanup': {'policy': 'conservation', 'private_traces': 'kept private', 'deletions': 0, 'production_changes': 0, 'historical_mutations': 0, 'scope': 'publication owned paths only; user dirty paths untouched; export retained privately with measured inventory'}, 'dashboard': 'standalone; no predecessor mutation', 'authentication_scope': 'selected manifest members only; parent authenticated seven full roots; no archived writer rerun'}
TEXT_PINS={'docs/stories/RE-952-cpu-counter-device-composition-checkpoint.md': '78e5eb1cbef1156649b6602e47e2eff90d95294120998629f530bc6def85d198', 'docs/reverse/tomb5-progress-dashboard-re952-v1.html': 'c4e9fc9122a4ec611c76dd055c1100ab5e48e7c0c229860db052c5423cb9086a'}
def exact(a,e):
    assert type(a) is type(e), 'exact type drift'
    if isinstance(e,dict):
        assert set(a)==set(e), 'schema drift'
        for k in e:exact(a[k],e[k])
    elif isinstance(e,list):
        assert len(a)==len(e), 'length drift'
        for x,y in zip(a,e):exact(x,y)
    else:assert a==e, 'value drift'
def leaves(v,p=()):
    if isinstance(v,dict):
        for k,x in v.items():yield from leaves(x,p+(k,))
    elif isinstance(v,list):
        for k,x in enumerate(v):yield from leaves(x,p+(k,))
    else:yield p,v
def safety(path,text):
    assert path in PATHS[:3], 'not generated output'
    assert len(text.encode())<=100000 and '\0' not in text, 'binary/heavy'
    assert not re.search(r'0[xX][0-9a-fA-F]+|word_le_hex|raw_opcode|payload_offset|build/reverse|BEGIN .*PRIVATE KEY|(?:api_key|password|secret|token)\s*[=:]|#include|\b(?:void|uint32_t)\s+\w+\s*\(',text), 'raw/source/secret'
    assert not re.search(r'<(?:script|iframe|img|link|object|embed)\b|\bsrc\s*=',text,re.I), 'assets/active content'
def links(path,text):
    found=re.findall(r'\]\(([^)]+)\)|href="([^"]+)"',text)
    for a,b in found:
        url=a or b
        assert ':' not in url and not url.startswith('/') and '\\' not in url, 'unsafe URL'
        target=(ROOT/path).parent.joinpath(url).resolve()
        assert target.is_relative_to(ROOT) and target.is_file(), 'unresolved link'
    return len(found)
class Checkpoint(unittest.TestCase):
    def test_exact_recursive_metadata(self):
        self.assertTrue((ROOT/PATHS[1]).is_file(),'metadata missing')
        exact(json.loads((ROOT/PATHS[1]).read_text()),EXPECTED)
    def test_every_leaf_mutation_types_pins_scope(self):
        for p,v in leaves(EXPECTED):
            variants=[not v,int(v)] if type(v) is bool else [v+1,bool(v),float(v)] if type(v) is int else [v+'-drift',None]
            for new in variants:
                m=copy.deepcopy(EXPECTED);q=m
                for k in p[:-1]:q=q[k]
                q[p[-1]]=new
                with self.subTest(path=p,kind=type(new).__name__):
                    with self.assertRaises(AssertionError):exact(m,EXPECTED)
        for v in ({},[],{'unknown':True}):
            with self.assertRaises(AssertionError):exact(v,EXPECTED)
    def test_story_dashboard_substantive_exact_bytes(self):
        for p,pin in TEXT_PINS.items():
            self.assertTrue((ROOT/p).is_file(),'document missing')
            text=(ROOT/p).read_text()
            self.assertEqual(hashlib.sha256(text.encode()).hexdigest(),pin)
            self.assertGreaterEqual(links(p,text),4)
        text=(ROOT/PATHS[0]).read_text()
        for marker in ('## Tracker','## Nettoyage','## Gate indépendante','720','1140','846720','1693440','3386880','4 assertions et 4 SIGABRT','PENDING','INCOMPLETE','integration=false',EXPECTED['next_dependency']):self.assertIn(marker,text)
    def test_generated_output_safety(self):
        for p in PATHS[:3]:
            self.assertTrue((ROOT/p).is_file(),'output missing')
            safety(p,(ROOT/p).read_text())
    def test_same_path_safety_negative_controls(self):
        safety(PATHS[0],'Benign metadata counts 720 GPL')
        for bad in ('0x1234','raw_opcode','word_le_hex','payload_offset','build/reverse/x','BEGIN RSA PRIVATE KEY','api_key=secret','password:secret','#include <x>','void secret_fn()','<img src="x">','<script>x</script>','binary\0','a'*100001):
            with self.assertRaises(AssertionError):safety(PATHS[0],bad)
    def test_links_same_path_negative_controls(self):
        self.assertEqual(links(PATHS[0],'[OK](../reverse/generated/re952_cpu_counter_device_checkpoint.json)'),1)
        for bad in ('missing-re952.json','../../../../etc/passwd','/etc/passwd','https://example.com'):
            with self.assertRaises(AssertionError):links(PATHS[0],'[bad]('+bad+')')
    def test_deliverable_secret_size_assets_guard_including_test(self):
        for p in PATHS:
            data=(ROOT/p).read_bytes()
            self.assertLessEqual(len(data),100000)
            self.assertNotIn(b'\0',data)
            self.assertTrue(p.endswith(('.md','.json','.html','.py')))
            self.assertFalse(re.search(rb'(?:sk-[A-Za-z0-9]{24,}|AKIA[A-Z0-9]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)',data))
if __name__=='__main__':unittest.main()
