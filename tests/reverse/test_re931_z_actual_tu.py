#!/usr/bin/env python3
"""Public finite actual-TU regression. No ignored/private input dependency.
Self-locking per writer/compiler/output operation; do NOT wrap in an outer lock.
ABI32, PSXPC_TEST; full MATHS and LIBGTE TUs, normal defined-symbol link.
"""
import argparse, contextlib, fcntl, hashlib, json, os, pathlib, re, struct, subprocess, time
R=pathlib.Path(__file__).resolve().parents[2]
@contextlib.contextmanager
def locked():
 (R/'build/reverse').mkdir(parents=True,exist_ok=True)
 with (R/'build/reverse/autonomy-mutation.lock').open('a') as f:
  fcntl.flock(f,fcntl.LOCK_EX);yield

def write(p,data):
 with locked():
  p.parent.mkdir(parents=True,exist_ok=True)
  payload=data if isinstance(data,bytes) else data.encode()
  ledger=p.parent/'output-operations.jsonl'
  with ledger.open('a') as log:log.write(json.dumps({'operation':'write','path':str(p),'start':time.time(),'sha256':hashlib.sha256(payload).hexdigest(),'bytes':len(payload),'lock':'explicit canonical flock'})+'\n')
  p.write_bytes(payload)
  with ledger.open('a') as log:log.write(json.dumps({'operation':'write-complete','path':str(p),'end':time.time(),'exit':0})+'\n')
def record(p,obj):write(p,json.dumps(obj,indent=2)+'\n')
def run(p,name,argv):
 with locked():
  rec=dict(argv=list(map(str,argv)),cwd=str(R),start=time.time(),end=None,exit=None,timeout_seconds=75,lock='explicit canonical flock')
  q=p/(name+'.invocation.json');q.write_text(json.dumps(rec,indent=2))
  try:
   x=subprocess.run(rec['argv'],cwd=R,capture_output=True,timeout=75)
   rec.update(end=time.time(),exit=x.returncode)
   (p/(name+'.stdout')).write_bytes(x.stdout);(p/(name+'.stderr')).write_bytes(x.stderr)
   return x
  except subprocess.TimeoutExpired:
   rec.update(end=time.time(),exit='TIMEOUT');raise
  finally:q.write_text(json.dumps(rec,indent=2))

# Exact line numbers authenticated against current public baseline; not private candidate.
DELTA={579:('VZ0 = 0;','gteRegs.CP2D.p[1].d = 0;'),595:('VZ1 = 0;','gteRegs.CP2D.p[3].d = 0;'),767:('t2 = t0 << 16;','t2 = mRotX_signed32((uint32_t)t0 << 16);'),772:('VZ0 = 0;','gteRegs.CP2D.p[1].d = 0;'),788:('VZ1 = 0;','gteRegs.CP2D.p[3].d = 0;'),808:('t5 <<= 16;','t5 = mRotX_signed32((uint32_t)t5 << 16);')}
def candidate(text):
 lines=text.splitlines(True)
 for n,(old,new) in DELTA.items():
  assert lines[n-1].strip()==old,(n,lines[n-1]);lines[n-1]=lines[n-1].replace(old,new)
 return ''.join(lines)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--phase',choices=['red','candidate','green'],required=True);a=ap.parse_args();p=pathlib.Path(a.output).resolve()
 with locked():p.mkdir(parents=True,exist_ok=True)
 text=(R/'GAME/CAMERA.C').read_text().split('short rcossin_tbl[8192] =',1)[1].split('{',1)[1].split('}',1)[0]
 table=[(int(v,0)+32768)%65536-32768 for v in re.findall(r'-?0x[0-9a-fA-F]+|-?\d+',text)];assert len(table)==8192
 matrices=[[4096,0,0,2048,2048,0,1024,1024,0],[2048,0,1,1024,1024,0,512,512,1]]
 cases=[(axis,angle,m) for axis in [0,1] for angle in [0,8192] for m in matrices]
 write(p/'table.bin',struct.pack('<8192h',*table));write(p/'cases.bin',b''.join(struct.pack('<ii9h',ax,an,*m) for ax,an,m in cases))
 def build(label,source,opt,strict):
  flags=['g++','-m32','-std=c++11','-O'+str(opt),'-g','-ffunction-sections','-fdata-sections','-DPSXPC_TEST=1']+['-I'+str(R/x) for x in ['SPEC_PSXPC_N','GAME','EMULATOR']]+['-I/usr/include/SDL2']
  if strict:flags+=['-fsanitize=undefined','-fno-sanitize-recover=all']
  objects=[]
  for key,src in [('maths',source),('gte',R/'EMULATOR/LIBGTE.C')]:
   obj=p/(label+'-'+key+'.o');x=run(p,label+'-'+key,flags+['-x','c++','-c',src,'-o',obj]);assert x.returncode==0,x.stderr.decode();objects.append(obj)
  exe=p/label;x=run(p,label+'-link',flags+[R/'tests/reverse/re931_z_actual_tu.cpp',*objects,'-Wl,--gc-sections,-z,defs','-o',exe]);assert x.returncode==0,x.stderr.decode()
  return run(p,label+'-run',[exe,p/'table.bin',p/'cases.bin'])
 def check(x,raw=True):
  assert x.returncode==0,x.stderr.decode();assert not x.stderr,x.stderr.decode()
  rows=[[int(v) for v in line.split()] for line in x.stdout.decode().splitlines()];assert len(rows)==8
  for i,(row,(axis,angle,m)) in enumerate(zip(rows,cases)):
   assert len(row)==610 and row[0]==i and row[-1]==0
   idx=((angle & 0xffffffff)>>2)&0x3ffc;s,c=table[idx>>1],table[(idx>>1)|1];want=m[:]
   if idx:
    for k in range(3):
     want[3*k]=((m[3*k]*c+m[3*k+1]*s)//4096+32768)%65536-32768
     want[3*k+1]=((-m[3*k]*s+m[3*k+1]*c)//4096+32768)%65536-32768
   start=1+256*axis;got=list(struct.unpack('<9h',struct.pack('<5I',*row[start:start+5])[:18]));assert got==want,(i,got,want)
   # Independent complete stacks, including preserved third column and padding.
   expected=bytearray(2048);expected[1024*axis:1024*axis+18]=struct.pack('<9h',*want)
   assert struct.pack('<512I',*row[1:513])==expected
   assert row[577:609]==[0]*32
   z=[row[514],row[516]];w=[0,0] if angle else [0x12345678,0xabcd7654]
   if raw:assert z==w,('RAW_ONLY',i,z,w)
  return rows
 source=R/'SPEC_PSXPC_N/MATHS.C';base=source.read_text();checks=[]
 pins={str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest() for q in [pathlib.Path(__file__),R/'tests/reverse/re931_z_actual_tu.cpp',source,R/'EMULATOR/LIBGTE.C',R/'GAME/CAMERA.C',R/'EMULATOR/GTEREG.H',R/'SPEC_PSXPC_N/MATHS.H']}
 record(p/'input-pins.json',pins)
 # Public inverse supports baseline replay from the corrected source, without private files.
 if a.phase in ['red','candidate']:
  lines=base.splitlines(True)
  states=[lines[n-1].strip() for n in DELTA]
  if states==[new for old,new in DELTA.values()]:
   for n,(old,new) in DELTA.items():lines[n-1]=lines[n-1].replace(new,old)
   base=''.join(lines)
  else:assert states==[old for old,new in DELTA.values()], 'mixed/drifted six-line scope'
  if a.phase=='red':
   source=p/'baseline-MATHS.C';write(source,base)
 if a.phase=='red':
  x=build('baseline-normal-O0',source,0,False);check(x,False)
  try:check(x)
  except AssertionError as e:record(p/'behavioral-RED.json',{'status':'RAW_ONLY_RED','failure':str(e)})
  else:raise AssertionError('baseline must discriminate full32 Z scratch clears')
  x=build('baseline-strict-O0',source,0,True);assert x.returncode!=0 and b'left shift' in x.stderr,x.stderr.decode()
  record(p/'RED.json',{'status':'PUBLIC_BASELINE_RED','normal_geometry':'PASS','raw':'FAIL','ubsan_exit':x.returncode,'stderr':x.stderr.decode()});print('PUBLIC RED: raw full32 mismatch + fail-fast UBSan; geometry PASS');return
 if a.phase=='candidate':
  source=p/'candidate-MATHS.C';write(source,candidate(base))
 reference=None
 for opt in [0,2]:
  for strict in [False,True]:
   label='O%d-%s'%(opt,'strict' if strict else 'normal');x=build(label,source,opt,strict);check(x)
   if reference is None:reference=x.stdout
   assert x.stdout==reference,'full-state cross-config drift';checks.append(label)
 record(p/'GREEN.json',{'status':'FINITE_PUBLIC_GREEN_REVIEW_REQUIRED','cases':8,'configs':checks,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'geometry':'independent scalar','raw':'sensitive full32 scratch words; no hardware/gameplay claim'})
 if a.phase=='candidate':
  corrected=source.read_text()
  for n,(old,new) in DELTA.items():
   lines=corrected.splitlines(True);assert lines[n-1].strip()==new;lines[n-1]=lines[n-1].replace(new,old)
   mutant=p/('rollback-%d-MATHS.C'%n);write(mutant,''.join(lines));x=build('rollback-%d'%n,mutant,0,n in [767,808])
   if n in [767,808]:assert x.returncode!=0 and b'left shift' in x.stderr,x.stderr.decode()
   else:
    check(x,False)
    try:check(x)
    except AssertionError as e:assert 'RAW_ONLY' in str(e)
    else:raise AssertionError('insensitive rollback '+str(n))
   record(p/('rollback-%d-result.json'%n),{'line':n,'sensitive':True,'exit':x.returncode,'kind':'UBSan' if n in [767,808] else 'RAW_ONLY_GEOMETRY_UNCHANGED'})
 print('FINITE PUBLIC GREEN',a.phase,checks)
def test_lock_bootstrap_on_fresh_root(tmp_path, monkeypatch):
 monkeypatch.setattr(__import__(__name__, fromlist=['R']), 'R', tmp_path)
 lock_path=tmp_path/'build/reverse/autonomy-mutation.lock'
 assert not lock_path.parent.exists()
 with locked():
  assert lock_path.is_file()
  with lock_path.open('a') as contender:
   try:fcntl.flock(contender,fcntl.LOCK_EX | fcntl.LOCK_NB)
   except BlockingIOError:pass
   else:raise AssertionError('canonical lock not held')
 with lock_path.open('a') as contender:
  fcntl.flock(contender,fcntl.LOCK_EX | fcntl.LOCK_NB)

def test_actual_tu_z_defined(tmp_path):
 import sys
 from unittest.mock import patch
 with patch.object(sys,'argv',[__file__,'--phase','green','--output',str(tmp_path)]):main()
if __name__=='__main__':main()
