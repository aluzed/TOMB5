"""Autonomous synthetic GetChange regression; production is intentionally RED.

GetChange is defined in SPEC_PSXPC_N/CONTROL_S.C, NOT GAME/ITEMS.C.
Both complete production TUs are compiled; ITEMS is not a claimed caller.
No private build artifact or target evidence is an input. Logs are outputs only.
"""
import json, os, shlex, shutil, subprocess, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FIXTURE=ROOT/'tests/reverse/fixtures/re805/getchange.cpp'

def run_contract(source=None, output=None):
    source=Path(source) if source else ROOT/'SPEC_PSXPC_N/CONTROL_S.C'
    out=Path(output) if output else Path(tempfile.mkdtemp(prefix='re805-contract-'))
    out.mkdir(parents=True,exist_ok=True)
    ledger=[]; observations=[]
    def run(argv,label):
        p=subprocess.run(list(map(str,argv)),cwd=ROOT,capture_output=True,text=True,timeout=70,
            env={**os.environ,'ASAN_OPTIONS':'detect_leaks=0:halt_on_error=1','UBSAN_OPTIONS':'halt_on_error=1:print_stacktrace=1'})
        (out/(label+'.stdout')).write_text(p.stdout);(out/(label+'.stderr')).write_text(p.stderr)
        ledger.append({'name':label,'argv':list(map(str,argv)),'cwd':str(ROOT),'exit':p.returncode})
        (out/'commands.json').write_text(json.dumps(ledger,indent=2))
        return p
    compiler=shutil.which('c++')
    if not compiler:raise unittest.SkipTest('Prerequisite unavailable: C++ compiler')
    glew=next((p for p in (Path('/usr/include'),Path('/usr/local/include')) if (p/'GL/glew.h').is_file()),None)
    if glew is None:raise unittest.SkipTest('Prerequisite unavailable: installed public GLEW development headers')
    sdl=run(['pkg-config','--cflags','sdl2'],'sdl-discovery')
    if sdl.returncode:raise unittest.SkipTest('Prerequisite unavailable: installed public SDL2 development headers')
    flags=[compiler,'-m32','-std=c++11','-O0','-fpermissive','-Wno-narrowing','-ffunction-sections','-fdata-sections','-fno-pie','-no-pie','-fno-omit-frame-pointer',
           '-DPSX_VERSION=1','-DPSXPC_TEST=1','-DUSE_32_BIT_ADDR=1','-I',ROOT/'SPEC_PSXPC_N','-I',ROOT/'GAME','-I',ROOT/'EMULATOR','-I',glew,*shlex.split(sdl.stdout)]
    probe=out/'prerequisite.cpp';probe.write_text('static_assert(sizeof(void*)==4,"i386"); int main(){return 0;}')
    for mode,san in [('normal',[]),('strict',['-fsanitize=address,undefined','-fno-sanitize-recover=all'])]:
        pr=run([*flags,*san,probe,'-o',out/(mode+'-probe')],mode+'-prerequisite-build')
        if pr.returncode:raise unittest.SkipTest('Prerequisite unavailable: i386 compiler/sanitizer; logs='+str(out))
        pr=run([out/(mode+'-probe')],mode+'-prerequisite-run')
        if pr.returncode:raise unittest.SkipTest('Prerequisite unavailable: i386 runtime; logs='+str(out))
        built=run([*flags,*san,'-x','c++',source,ROOT/'GAME/ITEMS.C',FIXTURE,'-Wl,--gc-sections','-o',out/mode],mode+'-build')
        if built.returncode:raise AssertionError('Actual TU build failed: '+built.stderr+' logs='+str(out))
        result=run([out/mode],mode+'-run')
        observations.append({'mode':mode,'exit':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
    return out,observations

class GetChangeContract(unittest.TestCase):
    def test_independent_synthetic_oracle_actual_tus(self):
        out,rows=run_contract()
        for row in rows:
            with self.subTest(mode=row['mode']):
                self.assertEqual(row['exit'],0,'Behavioral RED (production reset defect): '+row['stdout']+row['stderr']+' logs='+str(out))
                self.assertIn('SUMMARY cases=1440 failures=0 reset_failures=0',row['stdout'])
                self.assertEqual(row['stderr'],'')

if __name__=='__main__':unittest.main()
