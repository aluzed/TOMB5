#!/usr/bin/env python3
"""Actual-TU regression: scalar matrix oracle + full native backing preservation.
Run under the repository mutation flock; no target payload or target fixture.
Whole TUs compile; section GC removes unrelated functions, strict retained link.
"""
from pathlib import Path
import subprocess, json, hashlib, struct, re, time, argparse, os
R=Path(__file__).resolve().parents[2]
MATRICES=[[4096,0,0,0,4096,0,0,0,4096],[3000,-1500,2000,-2200,2800,-1700,900,-3100,2400],[-32768,32767,-16384,16384,-32768,32767,-30000,30000,-1]]
ANGLES=[16,8192,16384,24576,32768,40960,49152,57344,65520,0,-16,-32768]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--phase',choices=['red','green'],required=True);a=ap.parse_args();P=Path(a.output);P.mkdir(exist_ok=True,parents=True)
 # Explicit caller owns mutation flock; canonical durable owner must still be live.
 if os.environ.get('RE862_OWNER_PID'):
  os.kill(int(os.environ['RE862_OWNER_PID']),0)
  assert subprocess.run(['flock','-n',str(R/'build/reverse/autonomy-repo.lock'),'true']).returncode==1
 def run(name,args):
  start=time.time();x=subprocess.run(args,cwd=R,capture_output=True,timeout=90)
  (P/(name+'.stdout')).write_bytes(x.stdout);(P/(name+'.stderr')).write_bytes(x.stderr)
  (P/(name+'.json')).write_text(json.dumps(dict(argv=args,cwd=str(R),start=start,end=time.time(),exit=x.returncode,lock='caller flock -w5 build/reverse/autonomy-mutation.lock'),indent=2));return x
 text=(R/'GAME/CAMERA.C').read_text().split('short rcossin_tbl[8192] =',1)[1].split('{',1)[1].split('}',1)[0]
 table=[int(x,0) for x in re.findall(r'-?0x[0-9a-fA-F]+|-?\d+',text)];assert len(table)==8192
 table=[(x+32768)%65536-32768 for x in table]
 (P/'table.bin').write_bytes(struct.pack('<8192h',*table))
 cases=[(m,ang) for m in MATRICES for ang in ANGLES]
 (P/'cases.bin').write_bytes(b''.join(struct.pack('<i9h',ang,*m) for m,ang in cases))
 pins={str(x.relative_to(R)):sha(x) for x in [Path(__file__),R/'tests/reverse/re862_mrotz_actual_tu.cpp',R/'SPEC_PSXPC_N/MATHS.C',R/'EMULATOR/LIBGTE.C',R/'GAME/CAMERA.C']}
 (P/(a.phase+'-pins.json')).write_text(json.dumps(pins,indent=2))
 def build(label,abi,opt,strict):
  flags=['g++','-m'+str(abi),'-std=c++11','-O'+str(opt),'-g','-ffunction-sections','-fdata-sections','-DPSXPC_TEST=1']+['-I'+str(R/x) for x in ['SPEC_PSXPC_N','GAME','EMULATOR']]+['-I/usr/include/SDL2']
  if abi==64:flags+=['-fpermissive'] # Existing unrelated pointer-to-int cast in mmPushMatrix.
  if strict:flags+=['-fsanitize=undefined','-fno-sanitize-recover=all']
  objects=[]
  for key,src in [('maths','SPEC_PSXPC_N/MATHS.C'),('gte','EMULATOR/LIBGTE.C')]:
   obj=P/(label+'-'+key+'.o');x=run(label+'-'+key,flags+['-x','c++','-c',str(R/src),'-o',str(obj)]);assert x.returncode==0,x.stderr.decode();objects.append(str(obj))
  exe=P/label;x=run(label+'-link',flags+[str(R/'tests/reverse/re862_mrotz_actual_tu.cpp')]+objects+['-Wl,--gc-sections,-z,defs','-o',str(exe)]);assert x.returncode==0,x.stderr.decode()
  run(label+'-elf',['file',str(exe)])
  return run(label+'-run',[str(exe),str(P/'table.bin'),str(P/'cases.bin')])
 def oracle(out):
  rows=[[int(v) for v in row.split()] for row in out.decode().splitlines()];assert len(rows)==len(cases)
  for row,(m,ang) in zip(rows,cases):
   idx=((ang & 0xffffffff)>>2)&0x3ffc;s,c=table[idx>>1],table[(idx>>1)|1];want=m[:]
   if idx:
    for k in range(3):
     want[k*3]=((m[k*3]*c+m[k*3+1]*s)//4096+32768)%65536-32768
     want[k*3+1]=((-m[k*3]*s+m[k*3+1]*c)//4096+32768)%65536-32768
   got=list(struct.unpack('<9h',struct.pack('<8I',*row[1:9])[:18]));assert got==want,(ang,got,want)
   assert len(row)==73
  return rows
 if a.phase=='red':
  results={}
  for abi in [32,64]:
   x=build('baseline'+str(abi),abi,0,False);assert x.returncode==0;oracle(x.stdout);results[str(abi)]=x.stdout.decode()
  (P/'baseline-outputs.json').write_text(json.dumps(results))
  x=build('red32',32,0,True);assert x.returncode!=0 and b'runtime error' in x.stderr and b'left shift' in x.stderr,x.stderr.decode()
  (P/'RED.json').write_text(json.dumps(dict(status='EXPECTED_LANGUAGE_UB',stderr=x.stderr.decode(),pins=pins),indent=2));print(x.stderr.decode());return
 if not (P/'baseline-outputs.json').exists():
  fresh={}
  for abi in [32,64]:
   x=build('reference'+str(abi),abi,0,False);assert x.returncode==0;oracle(x.stdout);fresh[str(abi)]=x.stdout.decode()
  (P/'baseline-outputs.json').write_text(json.dumps(fresh))
 baseline=json.loads((P/'baseline-outputs.json').read_text());checks=[]
 for abi in [32,64]:
  for opt in [0,2]:
   for strict in [False,True]:
    label='green%d-O%d-%s'%(abi,opt,'strict' if strict else 'normal');x=build(label,abi,opt,strict);assert x.returncode==0,x.stderr.decode();oracle(x.stdout);assert x.stdout.decode()==baseline[str(abi)],label+' native backing changed';checks.append(label)
 # Cross ABI complete output comparison is tested explicitly, not assumed.
 assert baseline['32']==baseline['64'],'baseline cross ABI differs'
 (P/'GREEN.json').write_text(json.dumps(dict(status='SCOPED_PASS_REVIEW_REQUIRED',cases=len(cases),configs=checks,pins=pins,complete_native_words=72),indent=2));print('PASS',len(cases),'cases;',len(checks),'configurations; all 72 output words unchanged; scalar matrices agree')
def test_actual_tu_defined_mrotz(tmp_path,monkeypatch):
 import sys
 monkeypatch.setattr(sys,'argv',[__file__,'--phase','green','--output',str(tmp_path)])
 main()
if __name__=='__main__':main()
