"""RE942 DRAFT: standalone complete EFFECTS TU, finite GCC i386 only.
Requires g++ multilib, binutils and system SDL2 development headers.
No CONTROL TU, AnimateItem, ignored assets, private proof or target executable.
Inherited compiler warnings are retained; runtime stderr must be empty.
"""
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import uuid
import pytest
ROOT=Path(__file__).resolve().parents[2]
OLD='item->pos.y_rot -= ANGLE(180);'
NEW='item->pos.y_rot = (short)((unsigned short)item->pos.y_rot - 32768u);'
@contextlib.contextmanager
def mutex(root=ROOT):
    p=Path(os.environ.get('RE942_MUTATION_LOCK',str(root/'build/reverse/autonomy-mutation.lock')))
    assert p.is_absolute()
    p.parent.mkdir(parents=True,exist_ok=True) # concurrency-safe lock bootstrap
    with p.open('a') as f:
        fcntl.flock(f,fcntl.LOCK_EX)
        try: yield
        finally: fcntl.flock(f,fcntl.LOCK_UN)
class Run:
    def __init__(self,path):self.path=path;path.mkdir(parents=True,exist_ok=False)
    def event(self,entry):
        with (self.path/'ledger.jsonl').open('a') as f:f.write(json.dumps(entry)+'\n')
    def write(self,path,data):
        if isinstance(data,str):data=data.encode()
        uid=str(uuid.uuid4());self.event(dict(uuid=uid,argv=['write',str(path)],cwd=str(ROOT),start=time.time(),sha256=hashlib.sha256(data).hexdigest(),exit=None))
        path.write_bytes(data);self.event(dict(uuid=uid,end=time.time(),exit=0))
    def run(self,label,argv,allowed=(0,)):
        argv=list(map(str,argv));uid=str(uuid.uuid4());self.event(dict(uuid=uid,label=label,argv=argv,cwd=str(ROOT),start=time.time(),timeout=45,exit=None))
        try:p=subprocess.run(argv,cwd=ROOT,capture_output=True,timeout=45,env=dict(os.environ,ASAN_OPTIONS='halt_on_error=1:detect_leaks=0',UBSAN_OPTIONS='halt_on_error=1:print_stacktrace=1'))
        except subprocess.TimeoutExpired as e:
            self.write(self.path/(uid+'.stdout'),e.stdout or b'');self.write(self.path/(uid+'.stderr'),e.stderr or b'');self.event(dict(uuid=uid,end=time.time(),exit=124));raise
        self.write(self.path/(uid+'.stdout'),p.stdout);self.write(self.path/(uid+'.stderr'),p.stderr);self.event(dict(uuid=uid,end=time.time(),exit=p.returncode))
        assert p.returncode in allowed,(label,p.returncode,p.stderr.decode(errors='replace'))
        return p

def flags(strict):
    f=['g++','-m32','-std=c++11','-O0','-fpermissive','-Wno-narrowing','-ffunction-sections','-fdata-sections','-fno-pie','-no-pie','-DPSX_VERSION=1','-DPSXPC_TEST=1','-DUSE_32_BIT_ADDR=1']
    f+=['-I'+str(ROOT/p) for p in ('SPEC_PSXPC_N','GAME','EMULATOR')]+['-I/usr/include/SDL2']
    if strict:f+=['-fsanitize=address,undefined','-fno-sanitize-recover=all','-fno-omit-frame-pointer']
    return f

def dependencies(r):
    """-MM uses canonical production source, never the scratch candidate."""
    result=set()
    for src in ('GAME/EFFECTS.C','tests/reverse/re942_turn180_actual_tu.cpp'):
        p=r.run('canonical-MM',flags(False)+['-x','c++','-MM',ROOT/src])
        for token in p.stdout.decode().replace('\\\n',' ').split(':',1)[1].split():
            path=Path(token).resolve();relative=path.relative_to(ROOT)
            assert relative.parts[0]!='build','ignored dependency prohibited'
            result.add(str(relative))
    pins={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(result)}
    r.write(r.path/'dependencies.json',json.dumps(pins,indent=2));return pins

def execute(tmp_path,variant='source',strict=False):
    with mutex():
        output=Path(os.environ.get('RE942_OUTPUT',str(tmp_path)))
        r=Run(output/('%s-%s-%s'%(variant,strict,time.time_ns())))
        pins=dependencies(r) # authenticate canonical dependencies BEFORE compile
        source=(ROOT/'GAME/EFFECTS.C').read_text()
        assert (source.count(OLD),source.count(NEW)) in ((1,0),(0,1)),'selected expression drift'
        if variant=='baseline':source=source.replace(NEW,OLD)
        elif variant=='xneg':
            source=source.replace(OLD,NEW);old='item->pos.x_rot = -item->pos.x_rot;';assert source.count(old)==1;source=source.replace(old,'item->pos.x_rot = item->pos.x_rot;')
        elif variant!='source':raise ValueError(variant)
        scratch=r.path/'EFFECTS.C';r.write(scratch,source)
        objects=[]
        for label,src in [('effects',scratch),('harness',ROOT/'tests/reverse/re942_turn180_actual_tu.cpp')]:
            obj=r.path/(label+'.o');r.run(label+'-compile',flags(strict)+['-x','c++','-c',src,'-o',obj]);objects.append(obj)
        # Ordinary linking with complete actual TU; no source extraction/include tricks.
        # Every undefined EFFECTS boundary traps. Finite no-reach, not global gameplay.
        nm=r.run('undefined-symbols',['nm','-u',objects[0]])
        harness=r.run('harness-defined',['nm','--defined-only',objects[1]])
        defined={line.split()[-1] for line in harness.stdout.decode().splitlines() if line.split()}
        external={line.split()[-1] for line in nm.stdout.decode().splitlines() if line.split()}
        boundaries=sorted(x for x in external-defined if not x.startswith('__') and x not in ('abort','memcpy','memset','printf','puts','sqrt','sin','cos'))
        r.write(r.path/'trap-boundaries.json',json.dumps(boundaries))
        exe=r.path/'actual-tu';r.run('link',flags(strict)+objects+['-Wl,--no-demangle','-Wl,-z,defs','-o',exe]+['-Wl,--defsym='+x+'=unreached_boundary' for x in boundaries])
        p=r.run('program',[exe],(0,1));assert not p.stderr,'runtime stderr must be empty'
        match=re.search(rb'cases=(\d+) failures=(\d+) controls=(\d+)',p.stdout);assert match,p.stdout
        cases,fail,controls=map(int,match.groups());assert cases==65585 and controls==cases-fail
        assert p.returncode==(1 if fail else 0)
        assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in pins.items()),'canonical dependency changed'
        r.write(r.path/'result.json',json.dumps(dict(variant=variant,strict=strict,cases=cases,failures=fail,controls=controls,program_exit=p.returncode,limits='GCC i386; no AnimateItem, natural gameplay, target execution or ISO-wide portability',compile_warnings='inherited and retained, not runtime stderr')))
        return fail

@pytest.mark.parametrize('strict',[False,True])
def test_production_actual_tu(tmp_path,strict):assert execute(tmp_path,'source',strict)==0

def test_fresh_baseline_red(tmp_path):assert execute(tmp_path,'baseline')==65585

def test_xneg_mutant_red(tmp_path):assert execute(tmp_path,'xneg')==65569

def test_lock_bootstrap(tmp_path):
    root=tmp_path/'public-only';assert not (root/'build').exists()
    with mutex(root):
        p=Path(os.environ.get('RE942_MUTATION_LOCK',str(root/'build/reverse/autonomy-mutation.lock')))
        with p.open('a') as f:
            with pytest.raises(BlockingIOError):fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)

def test_public_metadata_contract():
    story=ROOT/'docs/stories/RE-942-turn180-isolated-correction.md';dashboard=ROOT/'docs/reverse/tomb5-progress-dashboard-re942-v1.html'
    for p in (story,dashboard):
        text=p.read_text();assert 'DRAFT' in text and 'integration_turn180_patch_pending_public_review=true' in text and 'AnimateItem integration=false' in text and 'globalprocedure=false' in text
        links=re.findall(r'href="([^"]+)"',text) if p.suffix=='.html' else re.findall(r'\]\(([^)]+)\)',text)
        for link in links:
            if not link.startswith(('http:','https:','#')):assert (p.parent/link.split('#')[0]).is_file(),(p,link)
