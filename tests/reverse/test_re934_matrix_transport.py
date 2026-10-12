#!/usr/bin/env python3
"""Public finite full32 transport proof, self-locking; outputs only under build.
No private TU/table dependency. Raw software storage, not hardware semantics.
"""
import argparse, contextlib, fcntl, hashlib, json, pathlib, struct, subprocess, time
R=pathlib.Path(__file__).resolve().parents[2]
DELTA={265:('Matrix->m22 = R33;','for (unsigned j = 0; j < 4; ++j) ((unsigned char*)Matrix)[16 + j] = ((const unsigned char*)&gteRegs.CP2C.p[4].d)[j];'),998:('R33 = m->m22;','for (unsigned j = 0; j < 4; ++j) ((unsigned char*)&gteRegs.CP2C.p[4].d)[j] = ((const unsigned char*)m)[16 + j];')}
@contextlib.contextmanager
def locked():
 (R/'build/reverse').mkdir(parents=True,exist_ok=True)
 with (R/'build/reverse/autonomy-mutation.lock').open('a') as f:
  fcntl.flock(f,fcntl.LOCK_EX);yield
P=None
def event(x):
 with (P/'ledger.jsonl').open('a') as f:f.write(json.dumps(x)+'\n')
def write(p,data):
 with locked():
  p.parent.mkdir(parents=True,exist_ok=True);b=data if isinstance(data,bytes) else data.encode()
  event(dict(operation='write',path=str(p),start=time.time(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()));p.write_bytes(b);event(dict(operation='write-end',path=str(p),end=time.time(),exit=0))
def record(p,x):write(p,json.dumps(x,indent=2)+'\n')
def run(name,args):
 with locked():
  argv=list(map(str,args));event(dict(operation='run',name=name,argv=argv,cwd=str(R),start=time.time(),timeout=60))
  try:x=subprocess.run(argv,cwd=R,capture_output=True,timeout=60)
  except subprocess.TimeoutExpired as e:event(dict(operation='run-end',name=name,end=time.time(),exit='TIMEOUT'));raise
  (P/(name+'.stdout')).write_bytes(x.stdout);(P/(name+'.stderr')).write_bytes(x.stderr);event(dict(operation='run-end',name=name,end=time.time(),exit=x.returncode));return x

def oracle():
 rows=[];id=0
 for hi in [0,0x1234,0x8000,0xffff]:
  for lo in [0,0x1000,0x8000,0xffff]:
   for d in [0,29]:
    for mode in [0,1,2]:
     bank=[((j*0x1020301)^0xa5c39b27)&0xffffffff for j in range(96)];bank[68]=(hi<<16)|lo
     stack=bytearray([0x39]*1024);istack=bytes([0x75]*1024);index=d
     words=[0x01020304,0x81234567,0xffff0101,0x80001234,(hi<<16)|lo,0x12345678,0x80000001,0xffffffff]
     inp=bytes([0x6b]*16)+struct.pack('<8I',*words)+bytes([0x5a]*16)
     def snap(stage):rows.append([id,stage]+bank[:]+list(struct.unpack('<256I',stack))+list(struct.unpack('<256I',istack))+list(struct.unpack('<16I',inp))+[index,7,23])
     def push():
      nonlocal index
      index+=1;stack[index*32:(index+1)*32]=struct.pack('<8I',*bank[64:72])
     if mode==0:push();snap(0)
     elif mode==1:bank[64:72]=words;snap(0)
     else:
      push();snap(0)
      bank[64:72]=list(struct.unpack_from('<8I',stack,index*32));snap(1)
      push();snap(2)
      index-=1;bank[64:72]=list(struct.unpack_from('<8I',stack,index*32));snap(3)
     id+=1
 return rows

def main():
 global P
 ap=argparse.ArgumentParser();ap.add_argument('--phase',choices=['red','candidate','green'],required=True);ap.add_argument('--output',required=True);a=ap.parse_args();P=pathlib.Path(a.output).resolve()
 assert P.is_relative_to(R/'build'), 'outputs must stay under ignored build'
 with locked():P.mkdir(parents=True,exist_ok=True)
 source=R/'SPEC_PSXPC_N/MATHS.C';base=source.read_text();lines=base.splitlines(True);states=[lines[n-1].strip() for n in DELTA]
 assert states in [[x[0] for x in DELTA.values()],[x[1] for x in DELTA.values()]],'mixed/drifted transport unit'
 for n,(old,new) in DELTA.items():lines[n-1]=lines[n-1].replace(new,old)
 baseline=''.join(lines)
 def corrected(text):
  l=text.splitlines(True)
  for n,(old,new) in DELTA.items():assert l[n-1].strip()==old;l[n-1]=l[n-1].replace(old,new)
  return ''.join(l)
 pins={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,R/'EMULATOR/LIBGTE.C',R/'EMULATOR/GTEREG.H',R/'SPEC_PSXPC_N/MATHS.H',pathlib.Path(__file__),R/'tests/reverse/re934_matrix_transport.cpp']};record(P/'input-pins.json',pins)
 expected=oracle();assert len(expected)==192;record(P/'oracle.json',expected)
 def build(label,src,opt,strict):
  flags=['g++','-m32','-std=c++11','-O'+str(opt),'-g','-ffunction-sections','-fdata-sections','-DPSXPC_TEST=1']+['-I'+str(R/q) for q in ['SPEC_PSXPC_N','GAME','EMULATOR']]+['-I/usr/include/SDL2']
  if strict:flags+=['-fsanitize=address,undefined','-fno-sanitize-recover=all','-fno-omit-frame-pointer']
  objects=[]
  for part,p in [('maths',src),('gte',R/'EMULATOR/LIBGTE.C')]:
   o=P/(label+'-'+part+'.o');x=run(label+'-'+part,flags+['-x','c++','-c',p,'-o',o]);assert x.returncode==0,x.stderr.decode();objects.append(o)
  exe=P/label;x=run(label+'-link',flags+[R/'tests/reverse/re934_matrix_transport.cpp',*objects,'-Wl,--gc-sections,-z,defs','-o',exe]);assert x.returncode==0,x.stderr.decode()
  x=run(label+'-run',[exe]);assert x.returncode==0 and not x.stderr,x.stderr.decode();rows=[[int(v) for v in l.split()] for l in x.stdout.decode().splitlines()];assert len(rows)==192
  differences=[{'row':i,'columns':[j for j,(v,w) in enumerate(zip(g,e)) if v!=w]} for i,(g,e) in enumerate(zip(rows,expected)) if g!=e];record(P/(label+'-comparison.json'),dict(equal=not differences,differences=differences));return differences
 if a.phase=='red':
  src=P/'baseline-MATHS.C';write(src,baseline)
  for opt in [0,2]:
   for strict in [False,True]:
    label='baseline-O%d-%s'%(opt,strict);dif=build(label,src,opt,strict);assert dif,'baseline must be behavioral RED'
    x=run(label+'-assertion',['python3','-B','-c','import json,sys; assert json.load(open(sys.argv[1]))["equal"], "full32 transport mismatch"',P/(label+'-comparison.json')]);assert x.returncode==1 and b'full32 transport mismatch' in x.stderr
  record(P/'RED.json',dict(status='ACTUAL_TU_FULL32_RED',cases=96,snapshots=192,configs=4));print('PUBLIC BASELINE RED: full32 state assertion fails; binaries exit0, stderr empty');return
 src=source
 if a.phase=='candidate':src=P/'candidate-MATHS.C';write(src,corrected(baseline))
 for opt in [0,2]:
  for strict in [False,True]:assert not build('green-O%d-%s'%(opt,strict),src,opt,strict),'candidate mismatch'
 if a.phase=='candidate':
  text=src.read_text()
  for n,(old,new) in DELTA.items():
   l=text.splitlines(True);assert l[n-1].strip()==new;l[n-1]=l[n-1].replace(new,old);m=P/('rollback-%d-MATHS.C'%n);write(m,''.join(l))
   for opt in [0,2]:assert build('rollback-%d-O%d'%(n,opt),m,opt,False),'insensitive rollback'
 record(P/'GREEN.json',dict(status='FINITE_RAW_TRANSPORT_GREEN_PENDING_REVIEW',cases=96,snapshots=192,configs=4,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),hardware=False,target_fresh=False));print('FINITE GREEN: 96 cases / 192 snapshots; O0 O2 normal + ASanUBSan')
def test_bootstrap(tmp_path,monkeypatch):
 monkeypatch.setattr(__import__(__name__,fromlist=['R']),'R',tmp_path)
 assert not (tmp_path/'build').exists()
 with locked():
  with (tmp_path/'build/reverse/autonomy-mutation.lock').open('a') as f:
   try:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
   except BlockingIOError:pass
   else:raise AssertionError('lock not held')
def test_actual_tu_transport():
 import sys
 from unittest.mock import patch
 with patch.object(sys,'argv',[__file__,'--phase','green','--output',str(R/'build/reverse/re934-pytest-public')]):main()
if __name__=='__main__':main()
