"""Synthetic joint and signed-CV controls, actual full retained TUs.
Caller must own mutation flock. No hardware or authentic producer claim.
"""
from pathlib import Path
import subprocess, time, json, hashlib, struct, re, argparse
R=Path(__file__).resolve().parents[2]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--phase',choices=['red','green'],required=True);a=ap.parse_args();P=Path(a.output);P.mkdir(parents=True,exist_ok=True)
 def run(label,argv):
  start=time.time();x=subprocess.run(argv,cwd=R,capture_output=True,timeout=90)
  (P/(label+'.stdout')).write_bytes(x.stdout);(P/(label+'.stderr')).write_bytes(x.stderr)
  (P/(label+'.json')).write_text(json.dumps(dict(argv=argv,cwd=str(R),start=start,end=time.time(),exit=x.returncode),indent=2));return x
 tabletext=(R/'GAME/CAMERA.C').read_text().split('short rcossin_tbl[8192] =',1)[1].split('{',1)[1].split('}',1)[0]
 table=[(int(x,0)+32768)%65536-32768 for x in re.findall(r'-?0x[0-9a-fA-F]+|-?\d+',tabletext)];assert len(table)==8192
 (P/'table.bin').write_bytes(struct.pack('<8192h',*table))
 cases=[]
 for cv in [0,1,3]:
  for sf in [0,1]:
   for lm in [0,1]:
    for tr in [[-1,2,-3],[-2147483648,2147483647,-1],[2147483647,-2147483648,0],[0,0,0],[32768,-32769,4096]]:
     b=[(0x13579bdf+i*12345)&0xffffffff for i in range(64)];m=[4096,-2048,1024,-3000,2500,-1700,900,-3100,2400];v=[-32768,32767,-1234]
     for k in range(4):b[32+k]=(m[2*k]&65535)|((m[2*k+1]&65535)<<16)
     b[36]=m[8]&65535;b[0]=(v[0]&65535)|((v[1]&65535)<<16);b[1]=(b[1]&0xffff0000)|(v[2]&65535)
     for k in range(3):b[32+(5 if cv==0 else 13)+k]=tr[k]&0xffffffff
     op=0x12|(cv<<13)|(sf<<19)|(lm<<10);cases.append((op,b,m,v,tr if cv!=3 else [0,0,0],sf,lm))
 (P/'cases.bin').write_bytes(b''.join(struct.pack('<65I',op,*b) for op,b,*_ in cases))
 def oracle(out):
  rows=[list(map(int,l.split())) for l in out.decode().splitlines()];assert len(rows)==60
  for idx,(row,case) in enumerate(zip(rows,cases)):
   op,b,m,v,tr,sf,lm=case;want=b.copy();flag=0
   for j in range(3):
    acc=tr[j]*4096+sum(m[3*j+k]*v[k] for k in range(3))
    if acc>0x7ffffffffff:flag|=(1<<31)|(1<<(30-j))
    if acc< -0x8000000000:flag|=(1<<31)|(1<<(27-j))
    mac=(acc//4096 if sf else acc)&0xffffffff;signed=mac if mac<0x80000000 else mac-0x100000000
    ir=max(0 if lm else -32768,min(32767,signed))
    if ir!=signed:flag|=((1<<31)|(1<<(24-j))) if j<2 else 1<<22
    want[25+j]=mac;want[9+j]=(want[9+j]&0xffff0000)|(ir&65535)
   want[63]=flag;assert row==[idx]+want,(idx,row,[idx]+want)
 def build(kind,abi,opt,strict):
  label=f'{a.phase}-{kind}-{abi}-O{opt}-{strict}'
  flags=['g++',f'-m{abi}','-std=c++11',f'-O{opt}','-g','-ffunction-sections','-fdata-sections','-DPSXPC_TEST=1']+['-I'+str(R/x) for x in ['SPEC_PSXPC_N','GAME','EMULATOR']]+['-I/usr/include/SDL2']
  if abi==64:flags+=['-fpermissive']
  if strict:flags+=['-fsanitize=undefined,address','-fno-sanitize-recover=all','-fno-pie','-no-pie']
  objects=[]
  for key,src in ([('spheres','SPEC_PSXPC_N/SPHERES.C'),('maths','SPEC_PSXPC_N/MATHS.C')] if kind=='joint' else [])+[('gte','EMULATOR/LIBGTE.C')]:
   obj=P/(label+key+'.o');x=run(label+key,flags+['-x','c++','-c',str(R/src),'-o',str(obj)]);assert x.returncode==0,x.stderr.decode();objects.append(str(obj))
  exe=P/label;harness=R/('tests/reverse/re862_'+('joint' if kind=='joint' else 'mvmva')+'_actual_tu.cpp')
  x=run(label+'link',flags+[str(harness)]+objects+['-Wl,--gc-sections,-z,defs','-o',str(exe)]);assert x.returncode==0,x.stderr.decode()
  x=run(label+'run',[str(exe),str(P/('table.bin' if kind=='joint' else 'cases.bin'))]);return x
 pins={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),R/'tests/reverse/re862_joint_actual_tu.cpp',R/'tests/reverse/re862_mvmva_actual_tu.cpp']};(P/(a.phase+'-test-pins.json')).write_text(json.dumps(pins,indent=2))
 if a.phase=='red':
  baseline={}
  for kind in ['joint','cv']:
   x=build(kind,32,0,False);assert x.returncode==0,x.stderr.decode()
   if kind=='cv':oracle(x.stdout)
   baseline[kind]=x.stdout.decode();x=build(kind,32,0,True);assert x.returncode!=0 and b'left shift' in x.stderr,x.stderr.decode()
  (P/'baseline.json').write_text(json.dumps(baseline));print('EXPECTED RED joint and signed CV');return
 baseline=json.loads((P/'baseline.json').read_text()) if (P/'baseline.json').exists() else {}
 for kind,abis in [('joint',[32]),('cv',[32,64])]:
  for abi in abis:
   for opt in [0,2]:
    for strict in [False,True]:
     x=build(kind,abi,opt,strict);assert x.returncode==0,x.stderr.decode()
     if kind=='cv':oracle(x.stdout)
     if kind not in baseline:baseline[kind]=x.stdout.decode()
     assert x.stdout.decode()==baseline[kind],kind+' complete native state changed'
 print('PASS joint0/1 full stacks/GTE and unchanged inputs; 60 CV all64 oracle; joint32 O0/O2 normal/strict; CV32/64 O0/O2 normal/strict')
def test_composed_actual_tus(tmp_path,monkeypatch):
 import sys
 monkeypatch.setattr(sys,'argv',[__file__,'--phase','green','--output',str(tmp_path)]);main()
if __name__=='__main__':main()
