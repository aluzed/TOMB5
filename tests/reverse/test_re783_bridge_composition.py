"""BLOCKED-001 RE-783 public: composition/observer x current/baseline (fixtures identiques), normal+UBSan."""
import re, subprocess, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / 'tests/reverse/fixtures/re783/run_test.py'
OUT = ROOT / 'build/reverse/re783-public-tests'
EXP = {('composition','current'):(0,296,0), ('composition','baseline'):(1,296,52),
       ('observer','current'):(0,514,0), ('observer','baseline'):(1,514,132)}

def test_re783_matrix():
    OUT.mkdir(parents=True, exist_ok=True)
    for (suite, source),(rc,checks,fails) in EXP.items():
        for ubsan in (False, True):
            out = Path(tempfile.mkdtemp(prefix=f'r783-{suite}-{source}-', dir=OUT)) / 'run'
            argv=[sys.executable,'-B',str(RUN),'--root',str(ROOT),'--suite',suite,'--source',source,'--output',str(out)]
            if ubsan: argv.append('--ubsan')
            r=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=240)
            tag=f'{suite}/{source}/ubsan={ubsan}'
            assert r.returncode==rc, f'{tag} rc={r.returncode}\n{r.stdout}{r.stderr}'
            sums=re.findall(r'^SUMMARY .*checks=(\d+) failures=(\d+)', r.stdout, re.M)
            assert len(sums)==1, f'{tag} SUMMARY count={len(sums)}\n{r.stdout}'
            assert (int(sums[0][0]),int(sums[0][1]))==(checks,fails), f'{tag} {sums[0]}'
            if ubsan: assert 'runtime error' not in r.stdout and 'runtime error' not in r.stderr, f'{tag} UBSan diagnostic'
