"""Public fresh actual-TU characterization; NOT AnimateItem integration.
Requires GCC-compatible i386 C++ toolchain, SDL2 and GLEW public headers.
No assets, target binary, ignored archive or generated inputs are read.
"""
import hashlib
import os
from pathlib import Path
import re
import struct
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
INPUT_SHA = 'bc0206e069646c4e98cd25403e9928b731e3458bfd9ff567df328955c601f4bd'
EXPECTED_SHA = '51f8f6e630819f938dfa23a6b018fc655924b984d1c05acfe773eb35a6c9eb12'
CASES = [(3,327680,131072,-458752,196608,0), (4,-589824,-65536,524288,-131072,8192), (5,65535,1,-65537,1,-16384), (6,1114112,0,-1245184,0,12345), (7,2147483640,2147483640,-2147483640,-2147483640,-12345), (8,2147418112,65536,65536,65536,16384), (9,-2147483648,-65536,-65536,-65536,-32768), (10,196608,-65536,-131072,65536,4096)]

def signed(value, bits):
    return (value + (1 << (bits-1))) % (1 << bits) - (1 << (bits-1))


def expected_buffers():
    text = (ROOT/'GAME/CAMERA.C').read_text()
    values = list(map(int, re.findall(r'-?\d+', text.split('short rcossin_tbl[8192] =',1)[1].split('{',1)[1].split('}',1)[0])))
    assert len(values) == 8192
    table = struct.pack('<8192h', *values)
    inputs, outputs = [], []
    for c,(frame,v,ac,xv,xa,angle) in enumerate(CASES):
        b = bytearray((23+31*j+c)%256 for j in range(144)) + bytearray(188) + table
        def put(fmt, offset, *args):
            struct.pack_into(fmt, b, offset, *args)
        put('<I',4,0xfedc1234); put('<I',60,0); put('<I',132,0xabcdefa7 & ~8)
        put('<6h',14,1,7,2,0,frame,0); put('<3h',30,17,23,0)
        put('<3i',64,100+c,-200-c,300+c); put('<h',78,angle)
        put('<h',150,1); put('<4i',152,v,ac,xv,xa); put('<4h',168,2,100,1,2)
        inputs.append(bytes(b))
        delta=frame+1-2
        speed=signed(signed(v+ac*delta,32)>>16,16)
        lateral=signed(xv+xa*delta,32)>>16
        idx=((angle&65535)>>3)&0x1ffe
        li=(((angle&65535)+16384)>>3)&0x1ffe
        dx=signed(values[idx]*speed,32)>>12
        dz=signed(values[idx+1]*speed,32)>>12
        put('<I',4,0); put('<I',132,(0xabcdefa7 & ~8) & ~16)
        put('<h',22,frame+1); put('<h',30,speed)
        put('<i',64,signed(100+c+dx+(dx>>12),32))
        put('<i',72,signed(300+c+dz+(signed(values[li+1]*lateral,32)>>12),32))
        outputs.append(bytes(b))
    assert hashlib.sha256(b''.join(inputs)).hexdigest() == INPUT_SHA
    assert hashlib.sha256(b''.join(outputs)).hexdigest() == EXPECTED_SHA
    return inputs, outputs


def compile_run(directory, mode):
    source=(ROOT/'GAME/CONTROL.C').read_text()
    old='void AnimateItem(struct ITEM_INFO* item)\n{\n\tUNIMPLEMENTED();\n}'
    assert source.count(old)==1, 'Production must remain stub: no integration claim'
    control=ROOT/'GAME/CONTROL.C'
    if mode != 'baseline':
        body=(HERE/'re940_animateitem_candidate.inc').read_text()
        if mode=='no-acceleration':
            body=body.replace('+(unsigned)a->acceleration*(unsigned)d','').replace('+(unsigned)a->Xacceleration*(unsigned)d','')
        if mode=='no-lateral':
            body=body.replace('dz+((rcossin_tbl[li+1]*lateral)>>12)','dz')
        control=directory/(mode+'.cpp')
        control.write_text('#include <cassert>\n'+source.replace(old,body))
    executable=directory/mode
    cmd=['c++','-m32','-std=c++11','-O0','-fpermissive','-Wno-narrowing','-ffunction-sections','-fdata-sections','-fno-pie','-no-pie','-DPSX_VERSION=1','-DPSXPC_TEST=1','-DUSE_32_BIT_ADDR=1','-I','SPEC_PSXPC_N','-I','GAME','-I','EMULATOR','-I','/usr/include/SDL2']
    if mode=='strict':
        cmd+=['-fsanitize=address,undefined','-fno-sanitize-recover=all']
    cmd+=['-x','c++',str(control),'SPEC_PSXPC_N/CONTROL_S.C','GAME/CAMERA.C',str(HERE/'re940_animateitem_movement.cpp'),'-Wl,--gc-sections','-o',str(executable)]
    p=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=60)
    assert p.returncode==0,p.stderr.decode()
    p=subprocess.run([str(executable)],capture_output=True,timeout=30,env={**os.environ,'ASAN_OPTIONS':'halt_on_error=1:detect_leaks=0','UBSAN_OPTIONS':'halt_on_error=1:print_stacktrace=1'})
    assert p.returncode==0,(mode,p.returncode,p.stderr.decode())
    assert not p.stderr,p.stderr.decode()
    rows=[line.split() for line in p.stdout.decode().splitlines() if line.startswith('ROW ')]
    assert len(rows)==8
    assert [int(r[1]) for r in rows]==list(range(8))
    return [(bytes.fromhex(r[2]),bytes.fromhex(r[3])) for r in rows]


class MovementPublication(unittest.TestCase):
    def test_fresh_baseline_candidate_strict_and_causal_mutants(self):
        inputs,expected=expected_buffers()
        with tempfile.TemporaryDirectory(prefix='re940-public-') as tmp:
            for mode,count in [('baseline',8),('normal',0),('strict',0),('no-acceleration',6),('no-lateral',6)]:
                rows=compile_run(Path(tmp),mode)
                self.assertEqual([r[0] for r in rows],inputs,mode)
                differences=[i for i,r in enumerate(rows) if r[1]!=expected[i]]
                self.assertEqual(len(differences),count,mode)
                if mode=='no-acceleration':
                    self.assertEqual(differences,[0,1,2,5,6,7])
                if mode=='no-lateral':
                    self.assertEqual(differences,[1,2,3,4,5,7])
                print('RE940',mode,'differences',len(differences),'controls',8-len(differences))

    def test_limits_and_public_artifacts(self):
        body=(HERE/'re940_animateitem_candidate.inc').read_text()
        for token in ['assert(', '!item->gravity_status','number_changes==0','number_commands==0','frame_end','frame_number>=']:
            self.assertIn(token,body)
        self.assertNotIn('build' + '/reverse', body)
        self.assertNotIn('build' + '/reverse', (HERE/'re940_animateitem_movement.cpp').read_text())
        story=ROOT/'docs/stories/RE-940-animateitem-movement-private-proof.md'
        dashboard=ROOT/'docs/reverse/tomb5-progress-dashboard-re940-v1.html'
        self.assertTrue(story.is_file()); self.assertTrue(dashboard.is_file())
        self.assertIn('PUBLICATION_REVIEW_REQUIRED',story.read_text())
        self.assertIn('../stories/RE-940-animateitem-movement-private-proof.md',dashboard.read_text())
        self.assertTrue((dashboard.parent/'../stories/RE-940-animateitem-movement-private-proof.md').resolve().is_file())

if __name__=='__main__':
    unittest.main()
