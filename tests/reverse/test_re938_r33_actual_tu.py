"""Fresh RE938 public actual-TU pytest contract. Requires g++ multilib and SDL2 headers.
Finite four constructed nonorthonormal pairs, twelve calls; ABI32LE only.
No private input, target/hardware/allangles/LP64/natural gameplay claim.
"""
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import pytest
ROOT=Path(__file__).resolve().parents[2]
OLD='R33 = m.m22;'
NEW='const int r33_word = m.m22; for (unsigned j = 0; j < 4; ++j) ((unsigned char*)&gteRegs.CP2C.p[4].d)[j] = ((const unsigned char*)&r33_word)[j];'
@contextlib.contextmanager
def mutex():
    override=os.environ.get('RE938_MUTATION_LOCK')
    lock=Path(override) if override else ROOT/'build/reverse/autonomy-mutation.lock'
    if not lock.is_absolute(): raise ValueError('absolute canonical mutex required')
    lock.parent.mkdir(parents=True,exist_ok=True) # concurrency-safe bootstrap, not locked
    with lock.open('a') as fd:
        fcntl.flock(fd,fcntl.LOCK_EX)
        try: yield
        finally: fcntl.flock(fd,fcntl.LOCK_UN)
def expected():
    """Independent integer interpolation and complete raw96 backing-bank oracle."""
    a=(120,-240,360,-480,600,-720,840,-960,1200,100,-200,300)
    b=(-41,82,-123,164,-205,246,-287,328,1601,-61,122,-183)
    rows=[]
    for pair in range(4):
        x=[v+17*(pair%2) for v in a];y=[v+29*(pair%2) for v in b]
        if pair>=2:x[8],y[8]=-1201,-1602
        for fraction in (1,2,3):
            v=[(l+r)//2 if fraction==2 else l+(r-l)//4 if fraction==1 else r-(r-l)//4 for l,r in zip(x,y)]
            words=[(0xa5c39b27^(j*0x1020301))&0xffffffff for j in range(96)]
            for j in range(4):words[64+j]=(v[2*j]&65535)|((v[2*j+1]&65535)<<16)
            words[68]=v[8]&0xffffffff
            words[69:72]=[t&0xffffffff for t in v[9:]]
            words[77:80]=[31,0xffffffd1,59]
            rows.append([pair,fraction]+words)
    return rows
class Run:
    def __init__(self,path):self.path=path;path.mkdir(parents=True,exist_ok=False)
    def event(self,**entry):
        with (self.path/'ledger.jsonl').open('a') as f:f.write(json.dumps(entry)+'\n')
    def write(self,path,data):
        if isinstance(data,str):data=data.encode()
        self.event(op='write',argv=['write',str(path)],cwd=str(ROOT),start=time.time(),timeout=0,sha256=hashlib.sha256(data).hexdigest())
        path.write_bytes(data);self.event(op='write-end',end=time.time(),exit=0)
    def run(self,label,argv):
        argv=list(map(str,argv));self.event(op='run',label=label,argv=argv,cwd=str(ROOT),start=time.time(),timeout=40)
        try:
            p=subprocess.run(argv,cwd=ROOT,capture_output=True,timeout=40,env=dict(os.environ,ASAN_OPTIONS='halt_on_error=1:detect_leaks=0',UBSAN_OPTIONS='halt_on_error=1:print_stacktrace=1'))
            rc,out,err=p.returncode,p.stdout,p.stderr
        except subprocess.TimeoutExpired as e:rc,out,err=124,e.stdout or b'',e.stderr or b''
        self.write(self.path/(label+'.stdout'),out);self.write(self.path/(label+'.stderr'),err)
        self.event(op='run-end',label=label,end=time.time(),exit=rc)
        assert rc==0,(label,rc,err.decode(errors='replace'))
        return out,err
def execute(tmp_path,opt,strict,variant):
    with mutex():
        output=Path(os.environ.get('RE938_OUTPUT',str(tmp_path)))
        r=Run(output/('%s-O%s-%s-%s'%(variant,opt,strict,time.time_ns())))
        source=(ROOT/'SPEC_PSXPC_N/MATHS.C').read_text()
        assert (source.count(OLD),source.count(NEW)) in ((1,0),(0,1)), 'source drift/mixed correction'
        if variant!='source':
            corrected=source.replace(OLD,NEW) if OLD in source else source
            replacement={'inverse':OLD,'zeroextend':NEW.replace('= m.m22;','= (unsigned short)m.m22;'),'constant':NEW.replace('= m.m22;','= 0;')}[variant]
            source=corrected.replace(NEW,replacement)
        maths=r.path/'MATHS.C';r.write(maths,source)
        flags=['g++','-m32','-std=c++11','-ffunction-sections','-fdata-sections','-DPSXPC_TEST=1','-O'+str(opt)]
        flags+=['-I'+str(ROOT/p) for p in ('SPEC_PSXPC_N','GAME','EMULATOR')]+['-I/usr/include/SDL2']
        if strict:flags+=['-fsanitize=address,undefined','-fno-sanitize-recover=all','-fno-omit-frame-pointer']
        objects=[]
        for label,src in [('maths',maths),('gte',ROOT/'EMULATOR/LIBGTE.C')]:
            obj=r.path/(label+'.o');r.run(label+'-compile',flags+['-x','c++','-c',src,'-o',obj]);objects.append(obj)
        exe=r.path/'actual-tu';r.run('link',flags+[ROOT/'tests/reverse/re938_r33_actual_tu.cpp',*objects,'-Wl,--gc-sections,-z,defs','-o',exe])
        out,err=r.run('program',[exe]);assert not err,err.decode(errors='replace')
        rows=[[int(v) for v in line.split()] for line in out.decode().splitlines()]
        oracle=expected();assert len(rows)==12 and all(len(row)==98 for row in rows)
        mismatch=[{'row':i,'columns':[j for j,(v,w) in enumerate(zip(row,want)) if v!=w]} for i,(row,want) in enumerate(zip(rows,oracle)) if row!=want]
        r.write(r.path/'comparison.json',json.dumps({'variant':variant,'program_exit':0,'equal':rows==oracle,'differences':mismatch,'low16_equal':all((row[70]&65535)==(want[70]&65535) for row,want in zip(rows,oracle)),'expected':oracle},indent=2))
        return rows,oracle
@pytest.mark.parametrize('opt,strict',[(0,False),(2,False),(0,True),(2,True)])
def test_complete_actual_tu_fullword(tmp_path,opt,strict):
    rows,oracle=execute(tmp_path,opt,strict,'source')
    assert rows==oracle,'raw96 R33 fullword differs (stack/ABI/program checks passed)'
@pytest.mark.parametrize('variant',['inverse','zeroextend','constant'])
@pytest.mark.parametrize('opt',[0,2])
def test_fullword_mutants_sensitive(tmp_path,opt,variant):
    rows,oracle=execute(tmp_path,opt,False,variant)
    assert rows!=oracle,'mutant insensitive'
    if variant in ('inverse','zeroextend'):
        assert all((row[70]&65535)==(want[70]&65535) for row,want in zip(rows,oracle))
def test_public_documentation_contract():
    story=ROOT/'docs/stories/RE-938-interpolatematrix-r33-fullword-correction.md'
    dashboard=ROOT/'docs/reverse/tomb5-progress-dashboard-re938-v1.html'
    assert story.is_file() and dashboard.is_file(),'RE938 publication missing'
    for path in (story,dashboard):
        text=path.read_text()
        for token in ('RE938','12','ABI32','PENDING_REVIEW','RE895','ARCHIVAL','RE930','Nettoyage, conservation de l’essentiel et mesure espace avant/après'):
            assert token in text,(path,token)
        assert 'integration_approved=false' in text
