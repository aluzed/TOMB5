"""Public actual ITEMS.C i386 synthetic regression, independent of private archives."""
import json,os,shlex,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def run_contract(source=None,output=None):
 source=Path(source) if source else ROOT/'GAME/ITEMS.C'
 out=Path(output) if output else Path(tempfile.mkdtemp(prefix='re811-'))
 out.mkdir(parents=True,exist_ok=True);ledger=[];rows=[]
 def run(argv,name):
  p=subprocess.run(list(map(str,argv)),cwd=ROOT,capture_output=True,text=True,timeout=60,env={**os.environ,'ASAN_OPTIONS':'detect_leaks=0:halt_on_error=1','UBSAN_OPTIONS':'halt_on_error=1:print_stacktrace=1'})
  (out/(name+'.stdout')).write_text(p.stdout);(out/(name+'.stderr')).write_text(p.stderr)
  ledger.append({'name':name,'argv':list(map(str,argv)),'exit':p.returncode});(out/'commands.json').write_text(json.dumps(ledger,indent=2));return p
 sdl=run(['pkg-config','--cflags','sdl2'],'sdl-discovery');assert sdl.returncode==0,sdl.stderr
 flags=['c++','-m32','-std=c++11','-O0','-fpermissive','-Wno-narrowing','-ffunction-sections','-fdata-sections','-fno-pie','-no-pie','-fno-omit-frame-pointer','-DPSX_VERSION=1','-DPSXPC_TEST=1','-DUSE_32_BIT_ADDR=1','-I',ROOT/'SPEC_PSXPC_N','-I',ROOT/'GAME','-I',ROOT/'EMULATOR',*shlex.split(sdl.stdout)]
 for mode,san in [('normal',[]),('strict',['-fsanitize=address,undefined','-fno-sanitize-recover=all'])]:
  p=run([*flags,*san,'-x','c++',source,ROOT/'tests/reverse/fixtures/re811/removeactiveitem.cpp','-Wl,--gc-sections','-o',out/mode],mode+'-build');assert p.returncode==0,p.stderr
  p=run([out/mode],mode+'-run');rows.append({'mode':mode,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 (out/'results.json').write_text(json.dumps(rows,indent=2));return out,rows
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--source');p.add_argument('--output');a=p.parse_args()
 out,rows=run_contract(a.source,a.output);print(json.dumps(rows,indent=2));raise SystemExit(int(any(r['exit'] for r in rows)))
