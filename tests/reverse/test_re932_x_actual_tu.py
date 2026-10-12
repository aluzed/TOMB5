#!/usr/bin/env python3
"""RE932: independently bounded X actual-TU proof; public inputs only.
Self-locking: never put an outer flock around this runner.
"""
import argparse, contextlib, fcntl, hashlib, json, os, pathlib, re, struct, subprocess, time
R=pathlib.Path(__file__).resolve().parents[2]
OUT=None
DELTA={457:('VZ1 = t6;','gteRegs.CP2D.p[3].d = t6;'),703:('VZ0 = t5;','gteRegs.CP2D.p[1].d = (uint32_t)t5;'),711:('t5 <<= 16;','t5 = mRotX_signed32((uint32_t)t5 << 16);'),716:('VZ1 = t6;','gteRegs.CP2D.p[3].d = (uint32_t)t6;')}
HARNESS=r'''#include "MATHS.H"
#include "GTEREG.H"
#include <cstdio>
#include <cstring>
#include <cstdint>
MATRIX3D MatrixStack[32],iMatrixStack[32];
MATRIX3D *Matrix=MatrixStack,*iMatrix=iMatrixStack;
unsigned short MatrixSP;
long iFrac,iRate,iAmbientR,iAmbientG,iAmbientB;
short rcossin_tbl[8192];
int main(int argc,char **argv){
 static_assert(sizeof(long)==4 && sizeof(MATRIX3D)==32,"ABI32 required");
 if(argc!=3)return 79; setbuf(stdout,NULL);
 FILE *f=fopen(argv[1],"rb");if(!f)return 80;
 if(fread(rcossin_tbl,2,8192,f)!=8192)return 81;fclose(f);
 f=fopen(argv[2],"rb");if(!f)return 82;
 int axis,angle,id=0;short m[9];
 while(fread(&axis,4,1,f)==1){
  if(fread(&angle,4,1,f)!=1 || fread(m,2,9,f)!=9)return 83;
  memset(&gteRegs,0,sizeof(gteRegs));memset(MatrixStack,0,sizeof(MatrixStack));memset(iMatrixStack,0,sizeof(iMatrixStack));
  Matrix=MatrixStack;iMatrix=iMatrixStack;MatrixSP=0;
  memcpy(axis?iMatrixStack:MatrixStack,m,18);
  for(int j=0;j<4;j++)memcpy(&gteRegs.CP2C.r[(axis?8:0)+j],m+2*j,4);
  gteRegs.CP2C.r[(axis?8:0)+4]=(uint16_t)m[8];
  gteRegs.CP2D.r[1]=0x12345678;gteRegs.CP2D.r[3]=0xabcd7654;
  if(axis)iRotX(angle);else mRotX(angle);
  if(Matrix!=MatrixStack || iMatrix!=iMatrixStack)return 84;
  printf("%d",id++);
  for(int b=0;b<2;b++)for(int j=0;j<256;j++){uint32_t w;memcpy(&w,(char*)(b?iMatrixStack:MatrixStack)+4*j,4);printf(" %u",w);}
  for(int b=0;b<3;b++)for(int j=0;j<32;j++)printf(" %u",b==0?gteRegs.CP2D.r[j]:b==1?gteRegs.CP2C.r[j]:gteRegs.CP0.r[j]);
  printf(" %u\n",MatrixSP);
 }fclose(f);return 0;
}
'''
@contextlib.contextmanager
def locked():
 print(time.strftime('%Y-%m-%dT%H:%M:%S%z'),flush=True)
 (R/'build/reverse').mkdir(parents=True,exist_ok=True)
 with pathlib.Path(os.environ.get('RE932_MUTATION_LOCK',str(R/'build/reverse/autonomy-mutation.lock'))).open('a') as f:
  owner=os.environ.get('RE932_OWNER_PID')
  if owner:
   os.kill(int(owner),0)
   assert subprocess.run(['flock','-n',os.environ.get('RE932_REPO_LOCK',str(R/'build/reverse/autonomy-repo.lock')),'true'],capture_output=True).returncode==1
  fcntl.flock(f,fcntl.LOCK_EX)
  try:yield
  finally:
   if owner:
    os.kill(int(owner),0)
    assert subprocess.run(['flock','-n',os.environ.get('RE932_REPO_LOCK',str(R/'build/reverse/autonomy-repo.lock')),'true'],capture_output=True).returncode==1

def write(p,data):
 payload=data if isinstance(data,bytes) else data.encode()
 with locked():
  p.parent.mkdir(parents=True,exist_ok=True)
  ledger=OUT/'operations.jsonl'
  with ledger.open('a') as f:f.write(json.dumps(dict(operation='write',path=str(p),start=time.time(),sha256=hashlib.sha256(payload).hexdigest(),bytes=len(payload)))+'\n')
  p.write_bytes(payload)
  with ledger.open('a') as f:f.write(json.dumps(dict(operation='write-complete',path=str(p),end=time.time(),exit=0))+'\n')
def record(p,obj):write(p,json.dumps(obj,indent=2)+'\n')
def run(p,name,argv):
 with locked():
  rec=dict(argv=list(map(str,argv)),cwd=str(R),start=time.time(),end=None,exit=None,timeout_seconds=75)
  q=p/(name+'.invocation.json');q.write_text(json.dumps(rec,indent=2))
  try:
   x=subprocess.run(rec['argv'],cwd=R,capture_output=True,timeout=75)
   rec.update(end=time.time(),exit=x.returncode)
   (p/(name+'.stdout')).write_bytes(x.stdout);(p/(name+'.stderr')).write_bytes(x.stderr)
   return x
  except subprocess.TimeoutExpired as e:
   rec.update(end=time.time(),exit='TIMEOUT');(p/(name+'.stderr')).write_bytes(e.stderr or b'');raise
  finally:q.write_text(json.dumps(rec,indent=2))
def transform(text,forward=True,one=None):
 lines=text.splitlines(True)
 for n,(old,new) in DELTA.items():
  if one is not None and n!=one:continue
  a,b=(old,new) if forward else (new,old)
  assert lines[n-1].strip()==a,(n,lines[n-1]);lines[n-1]=lines[n-1].replace(a,b)
 return ''.join(lines)
def main():
 global OUT
 ap=argparse.ArgumentParser();ap.add_argument('--phase',choices=['red','candidate','green'],required=True);ap.add_argument('--output',required=True);a=ap.parse_args();p=pathlib.Path(a.output).resolve();OUT=p
 with locked():p.mkdir(parents=True,exist_ok=True)
 tabletext=(R/'GAME/CAMERA.C').read_text().split('short rcossin_tbl[8192] =',1)[1].split('{',1)[1].split('}',1)[0]
 table=[(int(v,0)+32768)%65536-32768 for v in re.findall(r'-?0x[0-9a-fA-F]+|-?\d+',tabletext)];assert len(table)==8192
 # Finite domain declared before execution: 2 routines x 3 angles, one matrix per angle.
 # Positive/negative col3 selected to make both resulting rotated columns nonnegative.
 cases=[(axis,angle,[1024,0,d,512,0,d//2,256,0,d//4]) for axis in [0,1] for angle,d in [(0,1024),(8192,1024),(40960,-1024)]]
 record(p/'contract.json',{'abi':'32','cases':cases,'configs':['O0 normal','O0 strict','O2 normal','O2 strict'],'oracle':'Python exact integer Q12; signed16 narrowing','raw_fields':[1,3],'review':'PENDING_REVIEW','cleanup':'OPEN','exclusions':['ABI64','other angles','saturation','hardware','gameplay','RE930']})
 write(p/'table.bin',struct.pack('<8192h',*table));write(p/'cases.bin',b''.join(struct.pack('<ii9h',ax,an,*m) for ax,an,m in cases));write(p/'harness.cpp',HARNESS)
 source=R/'SPEC_PSXPC_N/MATHS.C';base=source.read_text()
 record(p/'input-pins.json',{str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest() for q in [pathlib.Path(__file__),source,R/'EMULATOR/LIBGTE.C',R/'GAME/CAMERA.C',R/'EMULATOR/GTEREG.H',R/'SPEC_PSXPC_N/MATHS.H']})
 states=[base.splitlines()[n-1].strip() for n in DELTA]
 assert states in [[old for old,new in DELTA.values()],[new for old,new in DELTA.values()]],'mixed/drifted X scope'
 if a.phase!='green' and states==[new for old,new in DELTA.values()]:base=transform(base,False)
 def build(label,src,opt,strict):
  flags=['g++','-m32','-std=c++11','-O'+str(opt),'-g','-ffunction-sections','-fdata-sections','-DPSXPC_TEST=1']+['-I'+str(R/x) for x in ['SPEC_PSXPC_N','GAME','EMULATOR']]+['-I/usr/include/SDL2']
  if strict:flags+=['-fsanitize=undefined','-fno-sanitize-recover=all']
  objs=[]
  for key,s in [('maths',src),('gte',R/'EMULATOR/LIBGTE.C')]:
   obj=p/(label+'-'+key+'.o');x=run(p,label+'-'+key,flags+['-x','c++','-c',s,'-o',obj]);assert x.returncode==0,x.stderr.decode();objs.append(obj)
  exe=p/label;x=run(p,label+'-link',flags+[p/'harness.cpp',*objs,'-Wl,--gc-sections,-z,defs','-o',exe]);assert x.returncode==0,x.stderr.decode()
  return run(p,label+'-run',[exe,p/'table.bin',p/'cases.bin'])
 def check(x,raw=True):
  assert x.returncode==0,x.stderr.decode();assert not x.stderr,x.stderr.decode()
  rows=[[int(v) for v in line.split()] for line in x.stdout.decode().splitlines()];assert len(rows)==len(cases)
  failures=[]
  for i,(row,(axis,angle,m)) in enumerate(zip(rows,cases)):
   assert len(row)==610 and row[0]==i and row[-1]==0
   idx=(angle>>2)&0x3ffc;s,c=table[idx>>1],table[(idx>>1)|1];want=m[:]
   if idx:
    for k in range(3):
     want[3*k+1]=((m[3*k+1]*c+m[3*k+2]*s)//4096+32768)%65536-32768
     want[3*k+2]=((-m[3*k+1]*s+m[3*k+2]*c)//4096+32768)%65536-32768
   expected=bytearray(2048);expected[1024*axis:1024*axis+18]=struct.pack('<9h',*want)
   assert struct.pack('<512I',*row[1:513])==expected,('GEOMETRY',i)
   assert row[577:609]==[0]*32
   words=[row[514],row[516]]
   # mRotX VZ0 intentionally remains a low16 store; only VZ1 full32 is contracted.
   desired=[0x12340000|(s&65535),c&65535] if not axis else [((c&65535)<<16)|(s&65535),c&0xffffffff]
   if not angle:desired=[0x12345678,0xabcd7654]
   if words!=desired:failures.append({'case':i,'actual':words,'expected':desired})
  if raw:assert not failures,('RAW_ONLY',failures)
  return rows,failures
 if a.phase=='red':
  src=p/'baseline-MATHS.C';write(src,base)
  x=build('baseline-normal-O0',source if states==[old for old,new in DELTA.values()] else src,0,False);rows,failures=check(x,False);assert failures
  record(p/'behavioral-RED.json',{'raw':'FAIL','geometry':'PASS','failures':failures,'exit':x.returncode})
  x=build('baseline-strict-O0',source if states==[old for old,new in DELTA.values()] else src,0,True);assert x.returncode!=0 and b'left shift' in x.stderr,x.stderr.decode()
  record(p/'RED.json',{'status':'PUBLIC_BASELINE_RED','ubsan_exit':x.returncode,'stderr':x.stderr.decode(),'production_patch':False});return
 if a.phase=='candidate':source=p/'candidate-MATHS.C';write(source,transform(base))
 reference=None
 for opt in [0,2]:
  for strict in [False,True]:
   x=build('O%d-%s'%(opt,'strict' if strict else 'normal'),source,opt,strict);check(x)
   if reference is None:reference=x.stdout
   assert x.stdout==reference,'cross-config drift'
 record(p/'GREEN.json',{'status':'FINITE_PUBLIC_GREEN_PENDING_REVIEW','cases':len(cases),'configs':4,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
 if a.phase=='candidate':
  corrected=source.read_text()
  for n in DELTA:
   mutant=p/('rollback-%d-MATHS.C'%n);write(mutant,transform(corrected,False,n));strict=n==711;x=build('rollback-%d'%n,mutant,0,strict)
   if strict:
    sensitive=x.returncode!=0 and b'left shift' in x.stderr
    if not sensitive:check(x)
    kind='UBSAN' if sensitive else 'INSENSITIVE_OBSERVABLY_GREEN'
   else:
    rows,failures=check(x,False);sensitive=bool(failures);kind='RAW_ONLY_GEOMETRY_UNCHANGED' if sensitive else 'INSENSITIVE_OBSERVABLY_GREEN'
   record(p/('rollback-%d-result.json'%n),{'line':n,'sensitive':sensitive,'exit':x.returncode,'kind':kind,'configuration':'O0 strict' if strict else 'O0 normal'})
  results=[json.loads((p/('rollback-%d-result.json'%n)).read_text()) for n in DELTA]
  record(p/'candidate-verdict.json',{'verdict':'PENDING_REVIEW_FOUR_LINE_CANDIDATE','all_four_sensitive':all(x['sensitive'] for x in results),'mutants':results})
  assert all(x['sensitive'] for x in results),'four-line gate unresolved; no production patch'
 print('RE932 FINITE GREEN',a.phase)
def test_x_actual_tu(tmp_path):
 import sys
 from unittest.mock import patch
 with patch.object(sys,'argv',[__file__,'--phase','green','--output',str(tmp_path)]):main()
def test_four_line_scope():
 assert set(DELTA)=={457,703,711,716}
 text=(R/'SPEC_PSXPC_N/MATHS.C').read_text()
 assert text.splitlines()[698].strip()=='t5 = (rcossin_tbl[rx >> 1] & 0xFFFF) | ((rcossin_tbl[rx >> 1 | 1] & 0xFFFF) << 16);'
 states=[text.splitlines()[n-1].strip() for n in DELTA]
 base=transform(text,False) if states==[new for old,new in DELTA.values()] else text
 candidate=transform(base)
 assert transform(candidate,False)==base
 assert [i+1 for i,(a,b) in enumerate(zip(base.splitlines(),candidate.splitlines())) if a!=b]==sorted(DELTA)
 assert candidate.splitlines()[698]==base.splitlines()[698]
def test_lock_exclusion():
 with locked():
  assert subprocess.run(['flock','-n',os.environ.get('RE932_MUTATION_LOCK',str(R/'build/reverse/autonomy-mutation.lock')),'true'],capture_output=True).returncode==1
def test_transform_rejects_drift():
 import pytest
 text=(R/'SPEC_PSXPC_N/MATHS.C').read_text()
 states=[text.splitlines()[n-1].strip() for n in DELTA]
 base=transform(text,False) if states==[new for old,new in DELTA.values()] else text
 for n in DELTA:
  lines=base.splitlines(True);lines[n-1]='unexpected drift;\n'
  mutant=''.join(lines);assert mutant!=base
  with pytest.raises(AssertionError):transform(mutant)
if __name__=='__main__':main()
