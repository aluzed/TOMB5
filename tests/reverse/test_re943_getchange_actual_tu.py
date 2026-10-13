"""Finite actual-TU characterization, NOT production integration.
Prerequisites: GCC C++ multilib/i386 ASan+UBSan, public SDL2 and GLEW headers.
Standard-library entry: python3 tests/reverse/test_re943_getchange_actual_tu.py
"""
import os,re,json,struct,hashlib,subprocess,tempfile,unittest,fcntl,time,uuid,shutil
from pathlib import Path
from contextlib import contextmanager
ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent
PINS=[['1ec0e363e95f0d5093446ffa179cd480bde5eb82724b4b9a9ad730d1b4296983', '2063ca0a40e8b5170a9ee5394cb80a406b43d3e4e169822d6cadc47942c8db64', '971953c2cb5d0a29afad4bc66ac54224df375a6e55d4539415e1f9d274c3bd14'], ['1e6fb94de73376d1457128e60d47b0dedb33e714aec466a1dd75174169d9cd0d', '62a50d1affcf45da72e3b3f1337b97e6e44b7a4faee8022032ff7a9c69224940', '141e683ac0eb994b6d0a17966ce1ba97ca4553d1b4ecd517bb8e9dfce0619d73'], ['1a828dee88238b8db69cf32608aa9daeb83928fb68195b9c435f8727a92bbb35', '336125e452e0e89af6ef017c305adbc6ad28b41e17aca44c99a58e83223c3210', '47bbc48ad5f34cb88fce3120432ff5c6fb30776f74a012b7fb0b4da4edac496d'], ['27716d2bbb8f3716051a5c1a970e4fe662c332dc733ca9f7fd4f654d2225691d', 'ee41cd3ee88a5b634be249a3b88285cf0c0436ee27c1bbb4e30a6c46a8d3a222', 'f0fc6fae8397c506ee7ab8147636302cf6803f727f17143c69ba105126ca4480'], ['3e9211fdbad9520bfec9dded8461d07efc726690f73d89ddfb4ad6a298768d6a', '80ca2a64eca88a35db8c0e6d5c779c09bc21fb0400cc1430068a10e4385a30d2', '798632ad80c75a7c650261b261ae3505e6b7c2af22f9e5a973202463f16ae2fc'], ['2160b535c2e3df7daa4f032d6550031d2727cf59cf5c944fa9d23deaee468ba4', '92b57070f33ed60d4f62d85bb92e7f19931ef864908212b50587c3cc9463cc32', '682dd7be75e3f4d0b46277963e5ef6d200838250935fc9d12e45c7b2bdb0383b'], ['7f5143618aacb43916c15c4d54d74fbcaf942acc1843dc175a54b00b87d42fb9', '16953579e28be16f9ffa3b8f419d4a2f052902cc557661619ce389921ec82e7b', 'eb20806df728577e4067cfdf95a47be831047b9e39d1687c158aa8382921f7ff'], ['35db1eec73e3cec9f53e14292591b211d42d9a478811991b43a037aef7c023f2', 'b6d36068187a439570992448928de96c1a16414b97f59878934d63ede05cb854', 'f4dc31a5140414a92ad44259e34d58c0803898ec8b35ed1f12846359a19d26b8'], ['b1d78b0a57e564a0a1d022698664e7b5a227cb5a4645d25c410fb7e9eac19108', 'a2675df5e6b28ade3f810e0e38aee267754c8ecd39e9759ed789c8a1156b10cb', '7861fed809ae979cbca732b3e37f72177640aec13696875f6f76c07bd83217f5'], ['74c5b3e949c9a3214a0d3e3e18d6f1c08237da6b024b0dc4a6c5b800d21e9711', 'b1d4794c27354262ea0c39fbd0964b5a54db7acb9fb1b901d1f3d9cdfbdaba8a', 'c84fa94093eba7968634a89c63a7c0e53ecd4aaa0e7495f42f784e5d979f2f4d'], ['80f01238f141e4696f59e10e6946c7a6f9f3765cd0efa815c6675a22cb7b186b', 'beae3ebed52f5040fc46320e4cfaedb37c0c2793f52a77a6eeb70bed87750e5b', 'cb4126bdbc053f7ea2c26afc57759258a87fe9c850bd1656807b7ef235c3e100'], ['96f9ac4ddf0c07f0f33ad1fae65bed78371ba8f886cb523ec8d2cc79b2fb8359', 'e4f0f01e65855373bbe6cd80dc000bd8635e40624af3143cf5c6ab9f54caa3be', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'], ['838a6705664417abf70968e5d84a32714f795806b000db8d8142c1d368236c1f', '116a03b9c96dc78186630e63c8c437dcb9e6d9e6215e0326d238780d2a9a8a85', '63683668ed6bbec03b7b525d8a596d41a318146341bab39b3674be8cf37324f7'], ['6b037c33d0599af5ade5f4bb7d4da6cd9a767bba6e71a7098f2887eedbb1ac3a', 'f8749528c0c10abc3b6d6d4fbc461e99d70ac379cb32415188775e885966f815', '63683668ed6bbec03b7b525d8a596d41a318146341bab39b3674be8cf37324f7'], ['bd3f7fa5d098c216fdf2babde0feae8d0ce7fd47bb3d609b15408cf8a1f1e2ea', '7e6109156d2acffbdf4219c434cd1be0350474c3fa60f0f6a9fa0dab7f7dd7d6', '084e277f0c0fdbb80de6fbe1626248013a6573968f69d4637eeef4f594e176b6'], ['401426738ff17c4ff1dcd70cb3eb1bf04efabdd94c15d1c9cf3932843b0906a3', 'bb6efa9ca3bc9b9d8fbe637b838e6cc29b26b0df820773cb25093183824d7d1d', '798632ad80c75a7c650261b261ae3505e6b7c2af22f9e5a973202463f16ae2fc']]
MUTANTS={'no-current': [1, 2, 3, 4, 5, 6, 7, 15], 'no-required': [1, 2, 4, 15], 'no-helper': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15]}
FLAGS=['-m32','-std=c++11','-O0','-fpermissive','-Wno-narrowing','-ffunction-sections','-fdata-sections','-fno-pie','-no-pie','-DPSX_VERSION=1','-DPSXPC_TEST=1','-DUSE_32_BIT_ADDR=1','-I','SPEC_PSXPC_N','-I','GAME','-I','EMULATOR','-I','/usr/include/SDL2']
def guard():
    if os.environ.get('RE943_OWNER'):
        os.kill(int(os.environ['RE943_OWNER']),0)
        assert subprocess.run(['flock','-n',os.environ['RE943_REPO_LOCK'],'true'],capture_output=True).returncode==1
@contextmanager
def mutation():
    guard()
    with open(os.environ.get('RE943_MUTATION_LOCK','/tmp/re943-public-mutation.lock'),'a') as f:
        fcntl.flock(f,fcntl.LOCK_EX); yield
    guard()
def invoke(argv):
    uid=str(uuid.uuid4()); start=time.time(); ledger=Path(os.environ['RE943_LEDGER']) if os.environ.get('RE943_LEDGER') else None
    row=dict(uuid=uid,argv=list(map(str,argv)),cwd=str(ROOT),start=start,exit=None)
    if ledger:(ledger/(uid+'-prospective.json')).write_text(json.dumps(row)+'\n')
    try:
        p=subprocess.run(row['argv'],cwd=ROOT,capture_output=True,timeout=45,env={**os.environ,'ASAN_OPTIONS':'halt_on_error=1:detect_leaks=0','UBSAN_OPTIONS':'halt_on_error=1:print_stacktrace=1'})
        row.update(exit=p.returncode,duration_seconds=time.time()-start)
        if ledger:
            (ledger/(uid+'.stdout')).write_bytes(p.stdout);(ledger/(uid+'.stderr')).write_bytes(p.stderr)
        return p
    finally:
        if ledger:(ledger/(uid+'-invocation.json')).write_text(json.dumps(row)+'\n')
def fixtures():
    text=(ROOT/'GAME/CAMERA.C').read_text(); vals=list(map(int,re.findall(r'-?\d+',text.split('short rcossin_tbl[8192] =',1)[1].split('{',1)[1].split('}',1)[0])))
    assert len(vals)==8192; table=struct.pack('<8192h',*vals); rows=[]
    frames=[-11,-10,-9,-1,0,1,9,10,11,32766,-32768,0,0,0,0,0]
    chosen=[None,1,1,1,2,2,2,2,None,None,None,None,None,None,None,2]
    for c,f in enumerate(frames):
        b=bytearray((19+c+j*31)%256 for j in range(144))+bytearray(242)+table
        def put(fmt,off,*v):struct.pack_into(fmt,b,off,*v)
        cur=5;goal=5 if c==14 else 7;req=9 if c in (4,15) else 8 if c in (1,2) else -2
        put('<I',4,2882400018);put('<I',132,2779096497 & ~8)
        put('<6h',14,cur,goal,req,0,32767 if f==-32768 else f-1,0);put('<3h',30,17,23,0);put('<3i',64,100,-200,300);put('<h',78,12345)
        for j,state in enumerate([5,8,9]):
            put('<h',144+j*40+6,state);put('<6h',144+j*40+24,-32768,32767,0,0,3 if j==0 and c!=11 else 0,0)
        put('<9h',264,6,1,4,7,0 if c==12 else 2,0,7,1,2)
        if c==13:put('<h',270,6);put('<h',276,6)
        if c==12:put('<h',276,6)
        put('<20h',282,-10,-1,1,-7,0,10,2,5,0,10,1,-3,20,30,1,21,100,110,2,101)
        initial=bytes(b);put('<I',4,0);put('<I',132,struct.unpack_from('<I',b,132)[0]&~16);put('<h',22,f);put('<h',30,0)
        win=chosen[c];nf=-7 if win==1 else 5 if win==2 else f;ns=8 if win==1 else 9 if win==2 else cur
        if win:put('<h',20,win);put('<h',22,nf);put('<h',14,ns);put('<h',18,0 if req==ns else req)
        ev=b'' if c==11 else struct.pack('<12i',0,cur,goal,req,0,f,1,cur,goal,req,win or 0,nf)
        row=(initial,bytes(b),ev)
        assert [hashlib.sha256(x).hexdigest() for x in row]==PINS[c]
        rows.append(row)
    return rows
def execute(tmp,mode,rows):
    with mutation():
        source=(ROOT/'GAME/CONTROL.C').read_text(); old='void AnimateItem(struct ITEM_INFO* item)\n{\n\tUNIMPLEMENTED();\n}'
        assert source.count(old)==1; control=ROOT/'GAME/CONTROL.C'
        if not mode.startswith('baseline'):
            body=(HERE/'re943_animateitem_candidate.inc').read_text()
            if mode=='no-current':body=body.replace('item->current_anim_state=a->current_anim_state;',';')
            if mode=='no-required':body=body.replace('item->required_anim_state=0;',';')
            if mode=='no-helper':body=body.replace('GetChange(item,a)','false')
            control=tmp/(mode+'.cpp');control.write_text('#include <cassert>\nextern int GetChange(struct ITEM_INFO*,struct ANIM_STRUCT*);\nextern bool re943_fixture_domain(struct ITEM_INFO*);\n'+source.replace(old,body))
        for c,row in enumerate(rows):
            for suffix,data in zip(('input','expected','events'),row):(tmp/('case-%02d.'%c+suffix)).write_bytes(data)
        fs=FLAGS+(['-fsanitize=address,undefined','-fno-sanitize-recover=all'] if 'strict' in mode else []);objs=[]
        for name,path,extra in [('control',control,[]),('helper',ROOT/'SPEC_PSXPC_N/CONTROL_S.C',['-finstrument-functions']),('camera',ROOT/'GAME/CAMERA.C',[]),('harness',HERE/'re943_getchange_actual_tu.cpp',[])]:
            obj=tmp/(mode+'-'+name+'.o');p=invoke(['c++',*fs,*extra,'-x','c++','-c',path,'-o',obj]);assert p.returncode==0,p.stderr.decode();objs.append(obj)
        exe=tmp/mode;p=invoke(['c++',*fs,*objs,'-Wl,--gc-sections','-o',exe]);assert p.returncode==0,p.stderr.decode()
        p=invoke([exe,tmp,mode]);assert p.returncode in (0,1),p.stderr.decode();assert not p.stderr,p.stderr.decode()
        ids=[]
        for c,row in enumerate(rows):
            if (tmp/('%s-case-%02d.native'%(mode,c))).read_bytes()!=row[1] or (tmp/('%s-case-%02d.events'%(mode,c))).read_bytes()!=row[2]:ids.append(c)
        assert p.returncode==bool(ids)
        if mode=='normal':
            p=invoke([exe,tmp,mode,'invalid']);assert p.returncode!=0,'changed byte must be rejected'
        return ids
class GetChangePublication(unittest.TestCase):
    def test_fresh_actual_tu(self):
        rows=fixtures()
        with mutation():tmp=Path(tempfile.mkdtemp(prefix='re943-public-'))
        try:
            modes=[('baseline',list(range(16))),('baseline-strict',list(range(16)))]
            if not os.environ.get('RE943_RED_ONLY'):modes += [('normal',[]),('strict',[]),*MUTANTS.items()]
            for mode,ids in modes:
                self.assertEqual(execute(tmp,mode,rows),ids,mode);print('RE943',mode,'differing cases',ids,flush=True)
        finally:
            with mutation():shutil.rmtree(tmp)
    def test_documentary_links(self):
        if os.environ.get('RE943_RED_ONLY'):return
        story=ROOT/'docs/stories/RE-943-getchange-public-actual-tu.md';dash=ROOT/'docs/reverse/tomb5-progress-dashboard-re943-v1.html'
        for p in (story,dash):
            text=p.read_text();self.assertIn('PUBLICATION_REVIEW_REQUIRED',text)
            links=re.findall(r'href="([^"]+)"',text) if p==dash else re.findall(r'\]\(([^)]+)\)',text)
            self.assertTrue(links)
            for link in links:self.assertTrue((p.parent/link).resolve().is_file(),link)
if __name__=='__main__':unittest.main()
