"""RE947 finite actual-TU preparation; g++ multilib + SDL2 headers required.
Run python3 tests/reverse/test_re947_rng_actual_tu.py --output ABSENT_DIRECTORY.
No private inputs, target replay, assets or production application.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('re945', ROOT/'tests/reverse/test_re945_rng_actual_tu.py')
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)
BASE_SHA = 'cc943333afdcb2777a70f3f8db744257ab39004f2ae109f0787a97c6ac82c989'
FUTURE_SHA = '81928509ec45fe9c4a66d771886e131eac1bc6b91754fde116a49fb44fd0ce32'
PAIRS = ((0,1),(0x7fffffff,0x80000000),(0xffffffff,0xfffffffe),(0x80000001,0x7ffffffe),(0xffff,0xffff0000),(0x10000,0x8000),(0xd371f947,0xaabbccdd),(0x55555555,0xaaaaaaaa))

def sequences():
    return [[['seed_control',s],['seed_draw',t],['control',0],['draw',0],['draw',0],['control',0],['seed_control',t],['draw',0],['control',0],['seed_draw',s],['control',0],['draw',0],['draw',0],['control',0]] + [['control',0],['draw',0],['draw',0],['control',0]]*3 for s,t in PAIRS]

def oracle(seq):
    states = [0x11223344,0xaabbccdd]
    rows = []
    for name,seed in seq:
        stream = 0 if name in ('seed_control','control') else 1
        ret = 0
        if name.startswith('seed'):
            states[stream] = seed
        else:
            states[stream] = (states[stream]*1103515245+12345) % (2**32)
            ret = (states[stream] // (2**16)) % (2**15)
        rows.append([ret,*states])
    return rows

def proposed(baseline):
    text = baseline.decode().replace('#include "MISC.H"','#include "MISC.H"\n#include <stdint.h>',1)
    for n in (1,2):
        old = f'rand_{n} = (rand_{n} * 0x41C64E6D) + 0x3039;'
        new = f'uint32_t state = (uint32_t)((uint64_t)(uint32_t)rand_{n} * UINT64_C(1103515245) + UINT64_C(12345));\n\trand_{n} = state <= UINT32_C(2147483647) ? (long)state : (long)((int64_t)state - INT64_C(4294967296));'
        assert text.count(old)==1
        text = text.replace(old,new)
        old = f'return (rand_{n} >> 16) '+('&' if n==1 else '*')+' 0x7FFF;'
        assert text.count(old)==1
        text = text.replace(old,'return (long)((state >> 16) & UINT32_C(32767));')
    result = text.encode()
    assert hashlib.sha256(result).hexdigest()==FUTURE_SHA
    return result

# Archived approved finite observations, not data regenerated from native output.
APPROVED = {'baseline': [{'exit': 0, 'mismatch_steps': [3, 4, 7, 12, 15, 16, 19, 20, 23, 24]}, {'exit': 0, 'mismatch_steps': [3, 4, 7, 11, 12, 15, 16, 19, 20, 23, 24]}, {'exit': 0, 'mismatch_steps': [3, 4, 7, 11, 12, 15, 16, 19, 20, 23, 24]}, {'exit': 0, 'mismatch_steps': [3, 4, 7, 11, 12, 15, 16, 19, 20, 23, 24]}, {'exit': 0, 'mismatch_steps': [3, 4, 7, 11, 12, 15, 16, 19, 20, 23, 24]}, {'exit': 0, 'mismatch_steps': [3, 4, 7, 11, 12, 15, 16, 19, 20, 23, 24]}, {'exit': 0, 'mismatch_steps': [3, 4, 7, 11, 12, 15, 16, 19, 20, 23, 24]}, {'exit': 0, 'mismatch_steps': [3, 4, 7, 11, 12, 15, 16, 19, 20, 23, 24]}], 'baseline-strict': [{'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}], 'candidate': [{'exit': 0, 'mismatch_steps': []}, {'exit': 0, 'mismatch_steps': []}, {'exit': 0, 'mismatch_steps': []}, {'exit': 0, 'mismatch_steps': []}, {'exit': 0, 'mismatch_steps': []}, {'exit': 0, 'mismatch_steps': []}, {'exit': 0, 'mismatch_steps': []}, {'exit': 0, 'mismatch_steps': []}], 'candidate-strict': [{'exit': 0, 'mismatch_steps': []}, {'exit': 0, 'mismatch_steps': []}, {'exit': 0, 'mismatch_steps': []}, {'exit': 0, 'mismatch_steps': []}, {'exit': 0, 'mismatch_steps': []}, {'exit': 0, 'mismatch_steps': []}, {'exit': 0, 'mismatch_steps': []}, {'exit': 0, 'mismatch_steps': []}], 'signedoverflow-1': [{'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}], 'signedoverflow-2': [{'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}, {'exit': 1, 'mismatch_steps': []}], 'extractionbad': [{'exit': 0, 'mismatch_steps': [3, 4, 5, 7, 8, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 4, 5, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}], 'swapstate': [{'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}], 'draw-multiply': [{'exit': 0, 'mismatch_steps': [3, 4, 5, 7, 8, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}, {'exit': 0, 'mismatch_steps': [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}]}
FINGERPRINT = 'b2ce731009c8142ae9a5ade7a5be73a93d7e60d6d464bfef6a6c03f766b62384'

class Recorder(legacy.Recorder):
    def __init__(self,path):
        with legacy.mutation_lock():
            super().__init__(path)
    def write(self,name,data):
        with legacy.mutation_lock():
            super().write(name,data)
    def run(self,name,args,timeout=40,input=None):
        import time,uuid
        args = list(map(str,args))
        ident,start = str(uuid.uuid4()),time.time()
        with legacy.mutation_lock():
            self.event(uuid=ident,phase='start',name=name,argv=args,cwd=str(ROOT),start=start,timeout=timeout)
            p = subprocess.run(args,cwd=ROOT,input=input,capture_output=True,timeout=timeout)
            # No nested flock: write under this operation's lock directly.
            for suffix,data in (('.stdout',p.stdout),('.stderr',p.stderr)):
                (self.path/(name+suffix)).write_bytes(data)
            self.event(uuid=ident,phase='end',exit=p.returncode,end=time.time(),duration=time.time()-start)
        return p.returncode,p.stdout,p.stderr

def metadata_contract():
    for name in ('docs/stories/RE-947-rng-arithmetic-correction.md','docs/reverse/tomb5-progress-dashboard-re947-v1.html'):
        text=(ROOT/name).read_text()
        for marker in ('PRIVATE_ACCEPTED','PUBLIC_REVIEW_PENDING','INTEGRATION_NOT_YET','8 sequences','208 events','natural excluded','globalprocedure=false'):
            assert marker in text,(name,marker)

def execute(path):
    rec=Recorder(path)
    source=ROOT/'SPEC_PSXPC_N/MISC.C'
    original=source.read_bytes()
    baseline=legacy.frozen_baseline(original)
    assert hashlib.sha256(baseline).hexdigest()==BASE_SHA
    seqs=sequences()
    fingerprint=hashlib.sha256(json.dumps([seqs,[oracle(s) for s in seqs]],separators=(',',':')).encode()).hexdigest()
    assert fingerprint==FINGERPRINT
    assert (2**32-1)*1103515245+12345==4739561886808924620 < 2**64
    rec.record('contract.json',dict(scope='finite actual-TU preparation',private_review='accepted',public_review='pending',integration=False,source_sha256=hashlib.sha256(original).hexdigest(),baseline_sha256=BASE_SHA,proposed_sha256=FUTURE_SHA,fixture_oracle_sha256=fingerprint,sequences=8,events=208,arithmetic_max_wide=4739561886808924620,store_range=[-2147483648,2147483647],natural=False,globalprocedure=False))
    rec.write('historical-MISC.C',baseline)
    flags=['g++','-m32','-std=c++11','-O0','-fpermissive','-Wno-narrowing','-ffunction-sections','-fdata-sections','-fno-pie','-no-pie','-DPSX_VERSION=1','-DPSXPC_TEST=1','-DUSE_32_BIT_ADDR=1']+['-I'+str(ROOT/p) for p in ('SPEC_PSXPC_N','GAME','EMULATOR')]+['-I/usr/include/SDL2']
    harness=ROOT/'tests/reverse/re947_rng_actual_tu.cpp'
    def build(label,src,strict):
        ff=flags+(['-fsanitize=undefined','-fno-sanitize-recover=all'] if strict else [])
        obj,exe=path/(label+'.o'),path/label
        assert rec.run(label+'-compile',ff+['-x','c++','-c',src,'-o',obj])[0]==0
        assert rec.run(label+'-link',ff+[harness,obj,'-Wl,--gc-sections,-z,defs','-o',exe])[0]==0
        return exe
    def observe(label,src,strict=False):
        exe=build(label,src,strict)
        observed=[]
        ops={'seed_control':0,'seed_draw':1,'control':2,'draw':3}
        for c,seq in enumerate(seqs):
            data=''.join(f'{ops[n]} {s:x}\n' for n,s in seq).encode()
            rc,out,err=rec.run(label+f'-case-{c}',[exe,str(c)],input=data)
            rows=[list(map(int,line.split())) for line in out.splitlines()]
            want=oracle(seq)
            bad=[j for j in range(min(len(rows),len(want))) if rows[j]!=want[j]]
            entry=APPROVED[label][c]
            assert bad==entry['mismatch_steps'],(label,c,bad,entry)
            assert rc==entry['exit'],(label,c,rc)
            if rc:
                assert b'signed integer overflow' in err
            else:
                assert len(rows)==26 and not err
            observed.append(dict(case=c,exit=rc,observed_rows=len(rows),mismatch_steps=bad))
        return exe,observed
    results={}
    strict_exe=None
    for label,strict in (('baseline',False),('baseline-strict',True)):
        exe,results[label]=observe(label,path/'historical-MISC.C',strict)
        if strict: strict_exe=exe
    for name,op in (('control',2),('draw',3)):
        rc,out,err=rec.run('strict-first-'+name,[strict_exe,"--first-"+name],input=f'0 d371f947\n1 d371f947\n{op} 0\n'.encode())
        assert rc==1 and b'signed integer overflow' in err
    # Historical behavioral RED and strict RED have completed before future source creation.
    candidate=proposed(baseline).decode()
    rec.write('proposed-MISC.C',candidate)
    for label,strict in (('candidate',False),('candidate-strict',True)):
        _,results[label]=observe(label,path/'proposed-MISC.C',strict)
    mutants={}
    for n in (1,2):
        old=f'uint32_t state = (uint32_t)((uint64_t)(uint32_t)rand_{n} * UINT64_C(1103515245) + UINT64_C(12345));'
        mutants[f'signedoverflow-{n}']=(candidate.replace(old,f'uint32_t state = (uint32_t)((rand_{n} * 0x41C64E6D) + 0x3039);'),True)
    mutants['extractionbad']=(candidate.replace('state >> 16','state >> 15'),False)
    mutants['swapstate']=(candidate.replace('rand_1','rand_TEMP').replace('rand_2','rand_1').replace('rand_TEMP','rand_2').replace('rand_2 = seed;','rand_TEMP = seed;').replace('rand_1 = seed;','rand_2 = seed;').replace('rand_TEMP = seed;','rand_1 = seed;'),False)
    # Archived label is historical: this exact mutant changes BOTH extraction returns.
    mutants['draw-multiply']=(candidate.replace('return (long)((state >> 16) & UINT32_C(32767));','return (long)((state >> 16) * UINT32_C(32767));',2),False)
    for label,(text,strict) in mutants.items():
        rec.write(label+'-MISC.C',text)
        _,results[label]=observe(label,path/(label+'-MISC.C'),strict)
    for c,args in enumerate(([],['x'],['8'],['-1'])):
        rc,_,_=rec.run('invalid-'+str(c),[exe]+args)
        assert rc==2
    rc,out,err=rec.run('changed-fixture-rejected',[path/'candidate','0'],input=b'0 2\n'+b''.join(f'{dict(seed_control=0,seed_draw=1,control=2,draw=3)[n]} {s:x}\n'.encode() for n,s in seqs[0][1:]))
    assert rc==2 and not out and not err, 'changed supplied fixture must reject before execution'
    assert source.read_bytes()==original
    rec.record('results.json',dict(results=results,production_unchanged=True,integration=False,public_review='pending',current_is_proposed=hashlib.sha256(original).hexdigest()==FUTURE_SHA))
    return 0

def test_unknown_source_rejected():
    for data in (b'',b'unknown', (ROOT/'SPEC_PSXPC_N/MISC.C').read_bytes()+b'\n'):
        try: legacy.frozen_baseline(data)
        except ValueError: pass
        else: raise AssertionError('unknown source accepted')

def test_metadata_contract(): metadata_contract()
def test_actual_tu():
    import tempfile
    with legacy.mutation_lock(): path=Path(tempfile.mkdtemp(prefix='re947-'))/'fresh'
    execute(path)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    metadata_contract();test_unknown_source_rejected()
    sys.exit(execute(args.output.resolve()))
