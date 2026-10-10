#!/usr/bin/env python3
"""Synthetic actual-TU proof, not target execution or hardware validation.
Invoke under the canonical mutation lock. Full 608-word state + SP/index;
independent nine-short scalar oracle, baseline full-state comparison.
"""
from pathlib import Path
import argparse, hashlib, json, os, re, struct, subprocess, time
R=Path(__file__).resolve().parents[2]
MATRICES=[[4096,0,0,0,4096,0,0,0,4096],[3000,-1500,2000,-2200,2800,-1700,900,-3100,2400],[-32768,32767,-16384,16384,-32768,32767,-30000,30000,-1]]
ANGLES=[16,8192,16384,24576,32768,40960,49152,57344,65520,0,-16,-32768]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--phase',choices=['red','green'],required=True);a=ap.parse_args()
 P=Path(a.output);P.mkdir(parents=True,exist_ok=True)
 def run(name,args):
  start=time.time();x=subprocess.run(args,cwd=R,capture_output=True,timeout=90)
  (P/(name+'.stdout')).write_bytes(x.stdout);(P/(name+'.stderr')).write_bytes(x.stderr)
  (P/(name+'.command.json')).write_text(json.dumps(dict(argv=args,cwd=str(R),start=start,end=time.time(),exit=x.returncode,lock='build/reverse/autonomy-mutation.lock'),indent=2));return x
 text=(R/'GAME/CAMERA.C').read_text().split('short rcossin_tbl[8192] =',1)[1].split('{',1)[1].split('}',1)[0]
 table=[int(x,0) for x in re.findall(r'-?0x[0-9a-fA-F]+|-?\d+',text)];assert len(table)==8192
 table=[(x+32768)%65536-32768 for x in table]
 (P/'table.bin').write_bytes(struct.pack('<8192h',*table))
 cases=[(m,angle) for m in MATRICES for angle in ANGLES];assert len(cases)==36
 (P/'cases.bin').write_bytes(b''.join(struct.pack('<i9h',angle,*m) for m,angle in cases))
 pins={str(p.relative_to(R)):sha(p) for p in [Path(__file__),R/'tests/reverse/re866_mroty_actual_tu.cpp',R/'SPEC_PSXPC_N/MATHS.C',R/'EMULATOR/LIBGTE.C',R/'SPEC_PSXPC_N/SPHERES.C',R/'GAME/CAMERA.C']}
 (P/(a.phase+'-pins.json')).write_text(json.dumps(pins,indent=2))
 def build(label,abi,opt,strict):
  flags=['g++','-m'+str(abi),'-std=c++11','-O'+str(opt),'-g','-ffunction-sections','-fdata-sections','-DPSXPC_TEST=1']+['-I'+str(R/p) for p in ['SPEC_PSXPC_N','GAME','EMULATOR']]+['-I/usr/include/SDL2']
  if abi==64:flags+=['-fpermissive'] # unrelated discarded mmPushMatrix cast
  if strict:flags+=['-fsanitize=undefined','-fno-sanitize-recover=all']
  objects=[]
  for key,src in [('maths','SPEC_PSXPC_N/MATHS.C'),('gte','EMULATOR/LIBGTE.C')]:
   obj=P/(label+'-'+key+'.o');x=run(label+'-'+key,flags+['-x','c++','-c',str(R/src),'-o',str(obj)]);assert x.returncode==0,x.stderr.decode();objects.append(str(obj))
  exe=P/label;x=run(label+'-link',flags+[str(R/'tests/reverse/re866_mroty_actual_tu.cpp')]+objects+['-Wl,--gc-sections,-z,defs','-o',str(exe)]);assert x.returncode==0,x.stderr.decode()
  run(label+'-elf',['file',str(exe)])
  return run(label+'-run',[str(exe),str(P/'table.bin'),str(P/'cases.bin')])
 def oracle(out):
  rows=[[int(v) for v in row.split()] for row in out.decode().splitlines()];assert len(rows)==36
  for caseid,(row,(m,angle)) in enumerate(zip(rows,cases)):
   assert len(row)==611 and row[0]==caseid and row[-2:]==[0,0]
   idx=((angle & 0xffffffff)>>2)&0x3ffc;s,c=table[idx>>1],table[(idx>>1)|1];want=m[:]
   if idx:
    for k in range(3):
     want[k*3]=((m[k*3]*c-m[k*3+2]*s)//4096+32768)%65536-32768
     want[k*3+2]=((m[k*3]*s+m[k*3+2]*c)//4096+32768)%65536-32768
   got=list(struct.unpack('<9h',struct.pack('<8I',*row[1:9])[:18]));assert got==want,(angle,got,want)
   assert row[9:513]==[0]*504 # remaining matrix bytes and entire interpolation stack
   assert row[577:609]==[0]*32 # complete CP0 bank
  return rows
 if a.phase=='red':
  baseline={}
  for abi in [32,64]:
   x=build('baseline'+str(abi),abi,0,False);assert x.returncode==0;oracle(x.stdout);baseline[str(abi)]=x.stdout.decode()
  assert baseline['32']==baseline['64'];(P/'baseline-outputs.json').write_text(json.dumps(baseline))
  failures=[]
  for abi in [32,64]:
   x=build('red'+str(abi),abi,0,True)
   assert x.returncode!=0 and b'runtime error' in x.stderr and b'left shift' in x.stderr,x.stderr.decode()
   failures.append(dict(abi=abi,exit=x.returncode,stderr=x.stderr.decode()))
  (P/'RED.json').write_text(json.dumps(dict(status='EXPECTED_SANITIZER_RED',normal_behavior='scalar PASS; no invented behavioral mismatch',failures=failures,pins=pins),indent=2));print('RED: actual public TU negative-shift UBSan on ELF32 and ELF64; normal scalar behavior PASS');return
 baseline=json.loads((P/'baseline-outputs.json').read_text()) if (P/'baseline-outputs.json').exists() else None
 checks=[];reference=None
 for abi in [32,64]:
  for opt in [0,2]:
   for strict in [False,True]:
    label='green%d-O%d-%s'%(abi,opt,'strict' if strict else 'normal');x=build(label,abi,opt,strict);assert x.returncode==0,x.stderr.decode();assert not x.stderr,x.stderr.decode();oracle(x.stdout)
    if baseline:assert x.stdout.decode()==baseline[str(abi)],label+' complete state drift'
    if reference is None:reference=x.stdout
    assert x.stdout==reference,'cross-config complete state drift';checks.append(label)
 (P/'GREEN.json').write_text(json.dumps(dict(status='SCOPED_PASS_REVIEW_REQUIRED',cases=36,configs=checks,words=608,metadata=2,baseline_compared=baseline is not None,pins=pins),indent=2));print('PASS 36 cases x 8 configurations; 608 complete state words + SP/index; independent scalar nine shorts')
def test_actual_tu_defined_mroty(tmp_path,monkeypatch):
 import sys
 monkeypatch.setattr(sys,'argv',[__file__,'--phase','green','--output',str(tmp_path)]);main()
if __name__=='__main__':main()
