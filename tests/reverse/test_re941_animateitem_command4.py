"""Portable finite command4 test-only proof. Requires public i386 GCC, SDL2/GLEW headers.
No private inputs, target executable, assets or ignored headers at runtime.
"""
import hashlib, os, struct, re, subprocess, tempfile, unittest, json, uuid, time, fcntl
from pathlib import Path
from contextlib import contextmanager
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
INPUT_SHA='a1ffc291eb2e3c84e4ae3b53ee526bc06be359780af6c867d070692e96fc8ea9'
EXPECTED_SHA='514273e27b87f2712bcbc99d224e0af3458563855765843e9a869adbfa6b6ece'
@contextmanager
def mutation():
    owner=os.environ.get('RE941_OWNER')
    if owner:
        os.kill(int(owner),0)
        assert subprocess.run(['flock','-n',os.environ['RE941_REPO_LOCK'],'true'],capture_output=True).returncode==1
    path=os.environ.get('RE941_MUTATION_LOCK','/tmp/re941-public-mutation.lock')
    with open(path,'a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        yield
    if owner: os.kill(int(owner),0)
def invoke(args,cwd=ROOT):
    uid=str(uuid.uuid4()); start=time.time()
    p=subprocess.run(args,cwd=cwd,capture_output=True,timeout=60,env={**os.environ,'ASAN_OPTIONS':'halt_on_error=1:detect_leaks=0','UBSAN_OPTIONS':'halt_on_error=1:print_stacktrace=1'})
    ledger=os.environ.get('RE941_LEDGER')
    if ledger:
        base=Path(ledger)
        (base/(uid+'.stdout')).write_bytes(p.stdout)
        (base/(uid+'.stderr')).write_bytes(p.stderr)
        (base/(uid+'-invocation.json')).write_text(json.dumps(dict(uuid=uid,argv=args,cwd=str(cwd),start=start,end=time.time(),exit=p.returncode))+'\n')
    return p
def expected_buffers():
    text=(ROOT/'GAME/CAMERA.C').read_text()
    values=list(map(int,re.findall(r'-?\d+',text.split('short rcossin_tbl[8192] =',1)[1].split('{',1)[1].split('}',1)[0])))
    assert len(values)==8192
    table=struct.pack('<8192h',*values); inputs=[];outputs=[]
    for c in range(16):
        b=bytearray((19+31*j+c)%256 for j in range(144))+bytearray(188)+table+bytearray((71+7*j)%256 for j in range(192))
        def put(fmt,off,*v): struct.pack_into(fmt,b,off,*v)
        fl=[0,1,2,65533][c%4]; death=[0,7,-7][c//4%3];oid=1+c%2;control=c>=12
        put('<I',4,0xfedc1234);put('<I',132,(0xa5a5a5a1&~8)|((c%4)<<1));put('<h',12,oid)
        put('<6h',14,1,7,2,0,9 if control else 10,0);put('<3h',30,17,23,0);put('<h',48,death)
        put('<3i',64,100+c,-200-c,300+c);put('<h',78,12345)
        put('<h',150,1);put('<4h',168,2,10,1,2);put('<2h',180,2,0)
        put('<h',190,3);put('<4h',208,2,20,1,2);put('<2h',268,4,4)
        for j in range(3):put('<H',16716+j*64+50,fl if j==oid else fl^2)
        inputs.append(bytes(b));flags=struct.unpack_from('<I',b,132)[0]&~16
        put('<I',4,0);put('<h',22,10 if control else 2);put('<h',30,0)
        if not control:
            flags=(flags&~6)|4
            if fl&2 and death==0:put('<h',48,1)
            put('<h',20,1);put('<2h',14,3,3)
        put('<I',132,flags);outputs.append(bytes(b))
    assert hashlib.sha256(b''.join(inputs)).hexdigest()==INPUT_SHA
    assert hashlib.sha256(b''.join(outputs)).hexdigest()==EXPECTED_SHA
    return inputs,outputs
def compile_run(directory,mode):
    with mutation():
        source=(ROOT/'GAME/CONTROL.C').read_text()
        old='void AnimateItem(struct ITEM_INFO* item)\n{\n\tUNIMPLEMENTED();\n}'
        assert source.count(old)==1,'Production remains stub'
        control=ROOT/'GAME/CONTROL.C'
        if mode!='baseline':
            body=(HERE/'re941_animateitem_candidate.inc').read_text()
            if mode=='wrong-object':body=body.replace('objects[item->object_number]','objects[0]')
            if mode=='omit-status':body=body.replace('item->status=2;',';')
            if mode=='overwrite-after-death':body=body.replace(' && item->after_death==0','')
            control=directory/(mode+'.cpp');control.write_text('#include <cassert>\n'+source.replace(old,body))
        exe=directory/mode
        cmd=['c++','-m32','-std=c++11','-O0','-fpermissive','-Wno-narrowing','-ffunction-sections','-fdata-sections','-fno-pie','-no-pie','-DPSX_VERSION=1','-DPSXPC_TEST=1','-DUSE_32_BIT_ADDR=1','-I','SPEC_PSXPC_N','-I','GAME','-I','EMULATOR','-I','/usr/include/SDL2']
        if mode=='strict':cmd+=['-fsanitize=address,undefined','-fno-sanitize-recover=all']
        cmd+=['-x','c++',str(control),'SPEC_PSXPC_N/CONTROL_S.C','GAME/CAMERA.C',str(HERE/'re941_animateitem_command4.cpp'),'-Wl,--gc-sections','-o',str(exe)]
        p=invoke(cmd);assert p.returncode==0,p.stderr.decode()
        p=invoke([str(exe)]);assert p.returncode==0,(mode,p.returncode,p.stderr.decode());assert not p.stderr,p.stderr.decode()
        rows=[r.split() for r in p.stdout.decode().splitlines() if r.startswith('ROW ')]
        assert [int(r[1]) for r in rows]==list(range(16))
        result=[(bytes.fromhex(r[2]),bytes.fromhex(r[3])) for r in rows]
        if mode=='normal':
            p=invoke([str(exe),'invalid']);assert p.returncode!=0,'Out-of-domain input must abort'
        return result
class Command4Publication(unittest.TestCase):
    def test_fresh_actual_tu_exact_identities(self):
        inputs,expected=expected_buffers()
        with mutation():tmp=tempfile.mkdtemp(prefix='re941-public-')
        try:
            for mode,ids in [('baseline',list(range(16))),('normal',[]),('strict',[]),('wrong-object',[0,1,2,3]),('omit-status',[0,1,3,4,5,7,8,9,11]),('overwrite-after-death',[6,10])]:
                rows=compile_run(Path(tmp),mode)
                self.assertEqual([r[0] for r in rows],inputs,mode)
                self.assertEqual([i for i,r in enumerate(rows) if r[1]!=expected[i]],ids,mode)
                print('RE941',mode,'differences',len(ids),'ids',ids)
        finally:
            with mutation():__import__('shutil').rmtree(tmp)
    def test_public_limits_and_links(self):
        body=(HERE/'re941_animateitem_candidate.inc').read_text()
        self.assertIn('assert(re941_fixture_domain(item))',body)
        self.assertNotIn('hit_points',body)
        story=ROOT/'docs/stories/RE-941-animateitem-command4-private-proof.md'
        dashboard=ROOT/'docs/reverse/tomb5-progress-dashboard-re941-v1.html'
        self.assertIn('PUBLICATION_REVIEW_REQUIRED',story.read_text())
        self.assertIn('naturalité BLOCKED',story.read_text())
        for href in re.findall(r'href="([^"]+)"',dashboard.read_text()):
            if not href.startswith(('https:','#')):self.assertTrue((dashboard.parent/href).resolve().is_file(),href)
if __name__=='__main__':unittest.main()
