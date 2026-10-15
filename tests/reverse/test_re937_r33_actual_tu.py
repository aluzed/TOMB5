#!/usr/bin/env python3
"""RE937 finite ABI32 actual-TU regression; no private build inputs.
Requires g++, multilib C++ runtime and SDL2 development headers.
Only two constructed pairs / rate4 / fractions1,2,3; R33 positive and negative,
distinct initial upper16. No all-angles, saturation, LP64 or hardware claim.
"""
import argparse, contextlib, fcntl, hashlib, json, os, pathlib, subprocess, time
FIELDS='m00 m01 m02 m10 m11 m12 m20 m21 m22 tx ty tz'.split()
ROOT=pathlib.Path(__file__).resolve().parents[2]
@contextlib.contextmanager
def mutation_lock(root=ROOT):
    p=pathlib.Path(os.environ.get('RE937_MUTATION_LOCK',str(root/'build/reverse/autonomy-mutation.lock')))
    if not p.is_absolute(): raise ValueError('absolute canonical RE937_MUTATION_LOCK required')
    p.parent.mkdir(parents=True,exist_ok=True) # concurrency-safe bootstrap, before open
    with p.open('a') as f:
        fcntl.flock(f,fcntl.LOCK_EX)
        try: yield
        finally: fcntl.flock(f,fcntl.LOCK_UN)
def deltas():
    return [('R33 = m.m22;', 'const int r33_word = m.m22; for (unsigned j = 0; j < 4; ++j) ((unsigned char*)&gteRegs.CP2C.p[4].d)[j] = ((const unsigned char*)&r33_word)[j];')]
def forms(text):
    a,b=deltas()[0]
    assert text.count(a)==1
    return text,text.replace(a,b)
class Recorder:
    def __init__(self,p):
        self.p=p; p.mkdir(parents=True,exist_ok=False);self.ledger=p/'ledger.jsonl'
    def event(self,**x):
        with self.ledger.open('a') as f:f.write(json.dumps(x)+'\n');f.flush();os.fsync(f.fileno())
    def write(self,p,b):
        if isinstance(b,str):b=b.encode()
        self.event(op='write',path=str(p),argv=['write',str(p)],cwd=str(ROOT),start=time.time(),timeout=0,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
        p.write_bytes(b);self.event(op='write-end',path=str(p),end=time.time(),exit=0)
    def rec(self,name,x):self.write(self.p/name,json.dumps(x,indent=2)+'\n')
    def run(self,name,args,timeout=35):
        args=list(map(str,args));self.event(op='run',argv=args,cwd=str(ROOT),start=time.time(),timeout=timeout)
        try:q=subprocess.run(args,cwd=ROOT,capture_output=True,timeout=timeout);rc=q.returncode;out=q.stdout;err=q.stderr
        except subprocess.TimeoutExpired as e:rc=124;out=e.stdout or b'';err=e.stderr or b''
        self.write(self.p/(name+'.stdout'),out);self.write(self.p/(name+'.stderr'),err);self.event(op='run-end',name=name,end=time.time(),exit=rc)
        return rc,out,err
def oracle():
    A=[120,-240,360,-480,600,-720,840,-960,1200,100,-200,300];B=[-41,82,-123,164,-205,246,-287,328,1601,-61,122,-183];rows=[]
    for c in range(4):
        a=[v+(c%2)*17 for v in A];b=[v+(c%2)*29 for v in B]
        if c>=2:a[8]=-1201;b[8]=-1602
        for f in (1,2,3):
            v=[(x+y)//2 if f==2 else x+(y-x)//4 if f==1 else y-(y-x)//4 for x,y in zip(a,b)]
            assert all(-32768<=x<=32767 for x in v[:9])
            bank=[(0xa5c39b27^(j*0x1020301))&0xffffffff for j in range(96)];bank[68]=[0,0x12340000,0,0xabcd0000][c]
            for j in range(4):bank[64+j]=(v[2*j]&65535)|((v[2*j+1]&65535)<<16)
            bank[68]=v[8]&0xffffffff;bank[69:72]=[z&0xffffffff for z in v[9:12]];bank[77:80]=[31,(-47)&0xffffffff,59];rows.append([c,f]+bank)
    return rows
def execute(mode,p):
    with mutation_lock():
        r=Recorder(p);results=[];initial=os.statvfs(ROOT)
        r.rec('contract.json',dict(mode=mode,domain='four constructed nonorthonormal pairs; twelve calls; rate4 fractions1/2/3; ABI32 little-endian; arithmetic right shift implementation; R33 positive and negative and distinct initial upper16',limits='no allangles/saturation/LP64/natural callers/gameplay/hardware/fresh target; complete raw96 independent expected words and complete stack return invariants, not transient store order',mutex=os.environ.get('RE937_MUTATION_LOCK',str(ROOT/'build/reverse/autonomy-mutation.lock'))))
        flags=['g++','-m32','-std=c++11','-ffunction-sections','-fdata-sections','-DPSXPC_TEST=1']+['-I'+str(ROOT/x) for x in ['SPEC_PSXPC_N','GAME','EMULATOR']]+['-I/usr/include/SDL2']
        cache={};expected=oracle();r.rec('oracle.json',expected)
        def build(label,src,opt,strict):
            ff=flags+['-O'+str(opt)]+(['-fsanitize=address,undefined','-fno-sanitize-recover=all','-fno-omit-frame-pointer'] if strict else [])
            key=(opt,strict)
            if key not in cache:
                obj=p/('gte-%s-%s.o'%key);assert r.run(obj.stem,ff+['-x','c++','-c',ROOT/'EMULATOR/LIBGTE.C','-o',obj])[0]==0;cache[key]=obj
            obj=p/(label+'.o');assert r.run(label+'-compile',ff+['-x','c++','-c',src,'-o',obj])[0]==0
            exe=p/label;assert r.run(label+'-link',ff+[ROOT/'tests/reverse/re937_r33_actual_tu.cpp',obj,cache[key],'-Wl,--gc-sections,-z,defs','-o',exe])[0]==0
            rc,out,err=r.run(label+'-run',[exe]);assert rc==0 and not err,(label,rc,err.decode())
            rows=[[int(x) for x in line.split()] for line in out.decode().splitlines()];assert len(rows)==12 and all(len(x)==98 for x in rows)
            differences=[dict(row=i,columns=[j for j,(x,y) in enumerate(zip(row,exp)) if x!=y]) for i,(row,exp) in enumerate(zip(rows,expected)) if row!=exp]
            low16_equal=all((row[70]&65535)==(exp[70]&65535) for row,exp in zip(rows,expected))
            check_rc,_,_=r.run(label+'-assertion',['python3',pathlib.Path(__file__),'--check-output',p/(label+'-run.stdout')])
            assert check_rc==(1 if differences else 0)
            entry=dict(label=label,program_exit=rc,assertion_exit=check_rc,architectural_low16_equal=low16_equal,equal=not differences,differences=differences);results.append(entry);r.rec(label+'-comparison.json',entry);return not differences
        failure=None
        try:
            source=(ROOT/'SPEC_PSXPC_N/MATHS.C').read_text();base=source;candidate=None
            if (ROOT/'.git').exists():assert subprocess.check_output(['git','show','HEAD:SPEC_PSXPC_N/MATHS.C'],cwd=ROOT)==source.encode()
            if mode in ('gate','all'):base,candidate=forms(source)
            r.rec('input-pins.json',{str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in [ROOT/'SPEC_PSXPC_N/MATHS.C',ROOT/'EMULATOR/LIBGTE.C',ROOT/'EMULATOR/GTEREG.H',ROOT/'tests/reverse/re937_r33_actual_tu.cpp',pathlib.Path(__file__)]})
            if mode in ('red','all'):
                src=p/'baseline-MATHS.C';r.write(src,base)
                for o in (0,2):
                    for s in (False,True):assert not build('baseline-O%d-%s'%(o,s),src,o,s),'expected RED not observed'
                r.rec('RED.json',dict(status='PUBLIC_ACTUAL_TU_RED',program_exit=0,oracle_equal=False,assertion_exit=1,expected_red_wrapper_exit=0,configs=4))
            if mode in ('gate','all'):
                src=p/'candidate-MATHS.C';r.write(src,candidate)
                for o in (0,2):
                    for s in (False,True):assert build('candidate-O%d-%s'%(o,s),src,o,s)
                insensitive=[]
                for field,(a,b) in zip(['store_width'],deltas()):
                    src=p/('rollback-'+field+'-MATHS.C');r.write(src,candidate.replace(b,a))
                    for o in (0,2):
                        if build('rollback-'+field+'-O'+str(o),src,o,False):insensitive.append([field,o])
                r.rec('sensitivity.json',dict(individual_expressions=1,configs='O0/O2 normal',insensitive=insensitive));assert not insensitive
                a,b=deltas()[0]
                for field,replacement in [('zero_extend',b.replace('= m.m22;', '= (unsigned short)m.m22;')),('constant_zero',b.replace('= m.m22;', '= 0;'))]:
                    src=p/('mutant-'+field+'-MATHS.C');r.write(src,candidate.replace(b,replacement))
                    for o in (0,2):assert not build('mutant-'+field+'-O'+str(o),src,o,False)
            if mode in ('production','all'):
                assert source==candidate,'production not corrected'
                for o in (0,2):
                    for s in (False,True):assert build('production-O%d-%s'%(o,s),ROOT/'SPEC_PSXPC_N/MATHS.C',o,s)
        except Exception as e:
            failure=repr(e);r.rec('first-failure.json',dict(error=failure))
        r.rec('results.json',results);r.rec('verdict.json',dict(status='FAIL' if failure else 'FINITE_'+mode.upper()+'_GREEN',error=failure,integration_approved=False))
        r.run('df-before',['df','-B1',ROOT]);before=os.statvfs(ROOT);removed=[]
        for obj in sorted(p.glob('*.o')):
            size=obj.stat().st_size;r.event(op='unlink',sha256=hashlib.sha256(obj.read_bytes()).hexdigest(),ownership='new objects from this exclusive attempt',path=str(obj),bytes=size,start=time.time(),argv=['unlink',str(obj)],cwd=str(ROOT),timeout=0);obj.unlink();r.event(op='unlink-end',path=str(obj),end=time.time(),exit=0);removed.append(dict(path=str(obj),bytes=size))
        after=os.statvfs(ROOT);r.run('df-after',['df','-B1',ROOT])
        r.rec('cleanup.json',dict(status='DONE',title='Nettoyage, conservation de l’essentiel et mesure espace avant/après',before_available=before.f_bavail*before.f_frsize,after_available=after.f_bavail*after.f_frsize,initial_available=initial.f_bavail*initial.f_frsize,removed=removed,removed_bytes=sum(x['bytes'] for x in removed),preserve='inputs executables baselineFAIL outputs firstFAIL ledger',attribution='shared filesystem delta not exclusively attributable'))
        return 1 if failure else 0
if __name__=='__main__':
    import sys
    if len(sys.argv)==3 and sys.argv[1]=='--check-output':
        rows=[[int(x) for x in line.split()] for line in pathlib.Path(sys.argv[2]).read_text().splitlines()]
        raise SystemExit(0 if rows==oracle() else 1)
    a=argparse.ArgumentParser();a.add_argument('--mode',choices=['red','gate','production','all'],required=True);a.add_argument('--output',type=pathlib.Path,required=True);v=a.parse_args();raise SystemExit(execute(v.mode,v.output.resolve()))
