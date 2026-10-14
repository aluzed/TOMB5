"""Standalone public metadata contract, no private imports or behavioral replays."""
import copy
import hashlib
import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PATHS=['docs/stories/RE-953-cpu-cd-scheduler-checkpoint.md', 'docs/reverse/generated/re953_cpu_cd_scheduler_checkpoint.json', 'docs/reverse/tomb5-progress-dashboard-re953-v1.html', 'tests/reverse/test_re953_cpu_cd_scheduler_checkpoint.py']
EXPECTED={'schema': 're953.cpu-cd-scheduler.checkpoint.v1', 'private_finite': 'PASS', 'global_strict_passed': False, 'procedure': 'INCOMPLETE', 'public_gate': 'PENDING', 'integration': False, 'production_patch': False, 'new_cpu_replays': 0, 'new_native_builds': 0, 'cpu_frontier_unchanged': True, 'branchTest03_certified': False, 'source': {'name': 'PCSX-Redux', 'revision': 'c313b116e6a55786bc127c9b3a07a90b55d97c21', 'license': 'GPL-2.0-or-later', 'publication': 'no source copied'}, 'authentication': [{'name': 'cd-init-unit11', 'members': 155, 'manifest_sha256': '90cfa839fdb407495fb37c8755a8b02af92b8277b33b64c3f76a0d7457041259', 'selected_hashes': {'HANDOFF.md': '45d626564ecd5a58a8049d727f112ba059bf93bc27d40241f506b0253987d70d', 'acceptance.json': '7db0d6999b02847a953ca2371d0b83e71c73cd2f9752ec5d8d511bb5877b91da', 'finite-verdict.json': 'f89af0238df3afaef614480299583e1dbbc8d20db25b433423161373ac93405d', 'verdict.json': '048cf13b31477cdf1496b1c9b76b174422009418a561a860ec3b6d75bb839057'}}, {'name': 'cd-init-unit11-review', 'members': 208, 'manifest_sha256': 'ead6feee09c6b9e119287bbd658f88c8cad52df7659a88e549ecabcabe0b8bd3', 'selected_hashes': {'HANDOFF.md': '7a516c0901f3ffd390d2dad1274dfaa73fb3ff40143c0c4259ae71bea39ee393', 'acceptance.json': 'aad992dca49525b6876526c54a9e878ca5f2531b4fe2a0eb40187f7e2eb47954', 'finite-verdict.json': 'd620f15dee27b0d2f3e9283c0dfb1e21c4fc61456e815d0cf963002ff4ffa2b7', 'strict-verdict.json': '376ba6e3c7be1fc9c9162c0c4b1757f412eede9de6d5198e87d4c606d06a0ffa'}}, {'name': 'cd-init-unit12', 'members': 245, 'manifest_sha256': '3c2c748b8512df880316143b66aa62ad617c17f201cca396d12e8bfc045cd72b', 'selected_hashes': {'HANDOFF.md': '26327f14e55af180a6b27e98b0b6f71b175374b5ec75ec6a3f1d558d49b81c97', 'acceptance.json': '61d8ed7dcc91a1702bae01a1be5e176b4aaa49e747350a07da188c40307e2005', 'finite-verdict.json': 'd620f15dee27b0d2f3e9283c0dfb1e21c4fc61456e815d0cf963002ff4ffa2b7', 'strict-verdict.json': '3a73a768f20a1329343ff6838d8679c64b5806abf33761aff7de2f91b712718f'}}, {'name': 'cd-init-unit12-review', 'members': 151, 'manifest_sha256': '476024f41fce741187983fd40d79709b2ab24d4f522ef1db997cbd4e54096401', 'selected_hashes': {'HANDOFF.md': '736b101c84563a8d638a29da4c7ce690fdc0cb163194f5fb75c1ea8eb2c4ee74', 'acceptance.json': '436bfea2e418f0da22465d5515543ecef9a9a3ecd9a40ce2a76cc4073a95d318', 'finite-verdict.json': 'd620f15dee27b0d2f3e9283c0dfb1e21c4fc61456e815d0cf963002ff4ffa2b7', 'strict-verdict.json': '5178f320383a109988cec2795094dd141877cc43113aacdacf19a474f36c9615'}}], 'units': [{'unit': '11', 'finite': 'PASS', 'strict_passed': False, 'blocks': 4000, 'fetches': 8000, 'produced_cycles': 16000, 'counter_events': [2148, 4292, 6440, 8584, 10732, 12876, 15024], 'next_counter': 17168, 'modes': ['normal', 'UBSan failfast'], 'assertion_mutants': ['no_call', 'no_update', 'late_gate'], 'native_mutant_exit': 0, 'scope': 'same CPU producer -> full branchTest body -> unchanged entire counters TU and genuine header -fno-access-control -> real continuous SDL dummy device and actual wait', 'preserved_failures': ['initial enum LogClass compileFAIL', 'review initial normal FAIL and distinct normal_fast retry', 'partial diagnostic retention'], 'cycles_injected': False}, {'unit': '12', 'finite': 'PASS', 'strict_passed': False, 'target': 26993, 'stop_cycles': 26996, 'blocks': 6749, 'fetches': 13498, 'hardware_provider_reads': 13496, 'counter_events': 12, 'next_counter': 27898, 'modes': ['normal', 'UBSan failfast'], 'assertion_mutants': ['no_ack', 'wrong_index', 'no_schedule', 'no_dispatch', 'duration_retry'], 'native_mutant_exit': 0, 'scope': 'actual CD MMIO write ack -> actual scheduleFifo durationToCycles -> actual CPU schedule -> same CPU generated cycles -> full branchTest clears CDRFIFO bit and calls excluded guard before genuine fifoScheduledCallback BODY', 'command_fifo': 'constructed empty genuine class excerpt', 'callback_body_executed': False, 'runCommand_executed': False, 'CD_success': False, 'preserved_failures': ['initial Setting nested compileFAIL', 'duration+1 INSENSITIVE due to quantization; distinct duration_retry sensitive'], 'cycles_injected': False}], 'constructed': ['CPU class and memory', 'CD class and empty command FIFO', 'MMIO providers', 'System settings and video', 'source excerpts and adapters'], 'not_proven': ['whole CPU TU ABI', 'whole CD TU ABI', 'natural frontend configuration', 'hardware', 'Sony startup', 'global OpenBIOS gain', 'gameplay', 'callback body', 'produced command FIFO'], 'historical_reservations': ['pre-ledger discovery', 'unit11 partial diagnostic retention', 'historical holders', 'historical requested budget exceeded', 'RE944 excluded; no circumvention'], 'next_dependency': 'ACTUAL_CDRFIFO_CALLBACK_BODY_WITH_PRODUCED_COMMAND_FIFO_AND_NATURAL_FRONTEND_CONFIGURATION', 'cleanup': {'policy': 'conservation', 'deletions': 0, 'production_changes': 0, 'historical_mutations': 0, 'private_traces': 'kept private'}, 'dashboard': {'predecessor': 'docs/reverse/tomb5-progress-dashboard-re952-v1.html', 'predecessor_sha256': 'c4e9fc9122a4ec611c76dd055c1100ab5e48e7c0c229860db052c5423cb9086a', 'inverse': 'remove only new RE953 successor; predecessor bytes unchanged'}, 'authentication_scope': 'all four complete roots authenticated read-only; no archived writer or private proof rerun'}
TEXT_PINS={'docs/stories/RE-953-cpu-cd-scheduler-checkpoint.md': 'a7be70c15517955b715c2acc5ebeeb0507efe36c2e1dc658d98971dc2880cf65', 'docs/reverse/tomb5-progress-dashboard-re953-v1.html': '70fa2b6c5a4e41e6b20548089bf938d5ada78dd1035053b2731bc4753f632c9f'}
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
    assert not re.search(r'(?i)\b\S+\.(?:BIN|CUE|WAD|OBJ)\b|RAM\s+opcode|Authorization\s*:',text), 'asset/raw/secret'
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
        for marker in ('## Tracker','## Nettoyage','## Gate indépendante','4000','8000','16000','26993','26996','13496','duration+1 INSENSITIVE','PENDING','INCOMPLETE','integration=false',EXPECTED['next_dependency']):self.assertIn(marker,text)
    def test_generated_output_safety(self):
        for p in PATHS[:3]:
            self.assertTrue((ROOT/p).is_file(),'output missing')
            safety(p,(ROOT/p).read_text())
    def test_same_path_safety_negative_controls(self):
        safety(PATHS[0],'Benign metadata counts 720 GPL')
        for bad in ('0x1234','raw_opcode','word_le_hex','payload_offset','build/reverse/x','BEGIN RSA PRIVATE KEY','api_key=secret','password:secret','#include <x>','void secret_fn()','<img src="x">','<script>x</script>','binary\0','a'*100001):
            with self.assertRaises(AssertionError):safety(PATHS[0],bad)
    def test_links_same_path_negative_controls(self):
        self.assertEqual(links(PATHS[0],'[OK](../reverse/generated/re953_cpu_cd_scheduler_checkpoint.json)'),1)
        for bad in ('missing-re952.json','../../../../etc/passwd','/etc/passwd','https://example.com'):
            with self.assertRaises(AssertionError):links(PATHS[0],'[bad]('+bad+')')
    def test_deliverable_secret_size_assets_guard_including_test(self):
        for p in PATHS:
            data=(ROOT/p).read_bytes()
            self.assertLessEqual(len(data),100000)
            self.assertNotIn(b'\0',data)
            self.assertTrue(p.endswith(('.md','.json','.html','.py')))
            self.assertFalse(re.search(rb'(?:sk-[A-Za-z0-9]{24,}|AKIA[A-Z0-9]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)',data))

    def test_schema_container_and_provenance_mutations(self):
        for key in EXPECTED:
            for mode in ('delete','add'):
                m=copy.deepcopy(EXPECTED)
                if mode=='delete':del m[key]
                else:m['unexpected']=True
                with self.assertRaises(AssertionError):exact(m,EXPECTED)
        for key in ('units','authentication','constructed','not_proven'):
            m=copy.deepcopy(EXPECTED);m[key]=m[key][:-1]
            with self.assertRaises(AssertionError):exact(m,EXPECTED)
    def test_predecessor_inverse_pin(self):
        predecessor=ROOT/EXPECTED['dashboard']['predecessor']
        self.assertEqual(hashlib.sha256(predecessor.read_bytes()).hexdigest(),EXPECTED['dashboard']['predecessor_sha256'])
    def test_asset_raw_secret_failclosed(self):
        for bad in ('asset.BIN','disc.CUE','texture.WAD','mesh.OBJ','RAM opcode dump','Authorization: Bearer abc','token=abc','<iframe>','<object>','<embed>','<link href="x">'):
            with self.assertRaises(AssertionError):safety(PATHS[0],bad)

if __name__=='__main__':unittest.main()
