"""BLOCKED-001 re783: independent dimensions --suite composition|observer, --source current|baseline.
Baseline = two TUs GETSTUFF.C + SETUP.C extracted from a10b06bb into output/src (same fixtures)."""
from pathlib import Path
import argparse, subprocess
p=argparse.ArgumentParser(); p.add_argument('--root',type=Path,required=True)
p.add_argument('--suite',choices=['composition','observer'],required=True)
p.add_argument('--source',choices=['current','baseline'],default='current')
p.add_argument('--ubsan',action='store_true'); p.add_argument('--output',type=Path,required=True)
a=p.parse_args(); root,out=a.root.resolve(),a.output.resolve()
here=Path(__file__).resolve().parent; out.mkdir(parents=True,exist_ok=False)
flags=['g++','-m32','-std=c++17','-O0','-Wno-narrowing','-ffunction-sections','-fdata-sections','-fno-pie','-no-pie',
 '-DPSX_VERSION=1','-DPSXPC_TEST=1','-DNTSC_VERSION=1','-DUSE_32_BIT_ADDR=1','-DDEBUG_VERSION=0','-DDISC_VERSION=1',
 '-IGAME','-ISPEC_PSXPC_N','-IEMULATOR','-I/usr/include/SDL2']
san=['-fsanitize=undefined','-fno-sanitize-recover=all'] if a.ubsan else []
if a.source=='current':
    gs=root/'SPEC_PSXPC_N/GETSTUFF.C'; setup=root/'GAME/SETUP.C'
else:
    src=out/'src'; src.mkdir()
    for rel in ('SPEC_PSXPC_N/GETSTUFF.C','GAME/SETUP.C'):
        txt=subprocess.run(['git','show','a10b06bbf424e80b9258a1c7a943e6fa238cb9c0:'+rel],cwd=root,
                           capture_output=True,text=True,check=True).stdout
        (src/Path(rel).name).write_text(txt)
    gs=src/'GETSTUFF.C'; setup=src/'SETUP.C'
host = here/('host_composition.cpp' if a.suite=='composition' else 'host_observer.cpp')
srcs=[('host',host),('getstuff',gs),('collide',root/'SPEC_PSXPC_N/COLLIDE_S.C'),('objects',root/'GAME/OBJECTS.C'),
      ('setup',setup),('cbs',root/'GAME/BRIDGE_CALLBACKS.C')]
for n,s in srcs: subprocess.run(flags+san+['-c',str(s),'-o',str(out/(n+'.o'))],cwd=root,check=True,timeout=120)
subprocess.run(['g++','-m32','-no-pie','-Wl,--gc-sections',*san,*[str(out/(n+'.o')) for n,_ in srcs],'-o',str(out/'re783')],
               cwd=root,check=True,timeout=120)
raise SystemExit(subprocess.run([str(out/'re783')],cwd=root,timeout=60).returncode)
