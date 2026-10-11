"""RE882 portable metadata publication, not target/native behavioral execution.

Default checks only versioned public metadata. --write uses one canonical mutation
lock per output transaction. --check-staged scans exact added paths/lines; raw
vocabulary in guard/test definitions is not treated as published raw evidence.
"""
import argparse
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
PRIOR_DASHBOARD = 'docs/reverse/tomb5-progress-dashboard.html'
DASHBOARD = 'docs/reverse/tomb5-progress-dashboard-re882-v1.html'
REPORT = 'docs/reverse/functions/re882-reviewed-private-proof-publication.md'
JSON_PATH = 'docs/reverse/generated/re882-reviewed-private-proof-publication-v1.json'
CSV_PATH = 'docs/reverse/generated/re882-reviewed-private-proof-tracker-v1.csv'
STORIES = {
    'RE880': 'docs/stories/RE-880-private-push-pop-reviewed-proof.md',
    'RE881': 'docs/stories/RE-881-private-interpolation-transfer-reviewed-proof.md',
    'RE882': 'docs/stories/RE-882-reviewed-private-proof-publication.md',
}
OUTPUT_PATHS = tuple(STORIES.values()) + (REPORT, JSON_PATH, CSV_PATH, DASHBOARD)
PUBLIC_PATHS = OUTPUT_PATHS + ('scripts/reverse/re882_publication.py', 'tests/reverse/test_re882_publication.py')
PRESERVED = {
    PRIOR_DASHBOARD: '7a53c9a86444ede3ace0a6ea23a30d5d004b16d744e7139272b4cdfcf40ea9fc',
    'docs/reverse/reconstruction-progress.html': 'bdec8a44abdc4c2d154a078c982393af1266d72b599969f21e0477620506516f',
    'SPEC_PSXPC_N/MATHS.C': '59e70b260ae67d613e5fa74486c728a63bd3bb7ae4727537e293d4c057d9b7fa',
}
COMMON = {
    'execution_attribution': 'ARCHIVED_PRIVATE_PRODUCER_AND_INDEPENDENT_REVIEWER',
    'global_scope': 'FAIL_HISTORIC_D9_AND_UNPROVEN_FRONTIERS',
    'integration': False, 'full_ram_bytes': 2097152, 'gte_bytes': 384,
    'each_stack_bytes': 1024, 'entry_and_canaries_bytes': 64,
    'stack_external_canaries_proven': False,
    'abi': 'i386 O0 normal and fail-fast ASan UBSan',
}
EXPECTED = {
    'schema': 're882-reviewed-private-proof-publication-v1',
    'publication_review': 'PENDING_INDEPENDENT_EXACT_HASH_REVIEW',
    'fresh_execution_scope': 'PUBLIC_METADATA_TESTS_ONLY',
    'integration': False, 'production_patch': False, 'public_helpers_green': False,
    'historic_d9': 'FAIL_NON_REPLAYED',
    'historic_re879': {'content_scope': 'PASS', 'global_scope': 'FAIL', 'procedure': 'FAIL_LEDGER_AND_NESTED_LOCK', 'integration': False},
    'public_head': 'c4614066bc6a48ad93bf4e047ab2912c84c72a8a',
    'public_maths_scope': 'mRotY only; no new helper integration',
    'next_ticket': 'RE883',
    'next_objective': 'natural dualstack provenance and one bounded authentic caller; no invented proof',
    'unproved': ['natural_camera', 'item.data', 'registration', 'natural_dualstack_provenance', 'hardware', 'gameplay', 'complete_callers', 'GPR_complete', 'transient_stores', 'O2_strict_aliasing', 'alternative_ABI'],
    'archived_private_results': [
        dict(COMMON, ticket='RE880', content_scope='PASS_PRIVATE_EXACT_HASH_FINITE_PUSH_POP',
             procedure='FAIL_LEDGER_COVERAGE_AND_PREFLIGHT_INCIDENTS', fixtures=48,
             direct=32, compose=16, depths=[1,30], target_calls_per_executor=80,
             native_processes_per_executor=384, baseline_returned_red=96,
             baseline_ubsan_aborts_not_returns=0, candidate_green=96,
             mutant_rejections=[48,40,48,16], mutant_cases_each=48,
             producer_manifest_files=2284, reviewer_manifest_files=1776,
             approved_verdict_sha256='e34b91f4e66df6f3c7081088fec501a66a3cc974e1c84d5108eb6b1ed66e4f07',
             candidate_sha256='1db1f98b2bf6f5cd803587d1165221cbb37b01aa6dc3108d6dbf76a47500657c',
             baseline_sha256='16e31d730e8fe870be4f99c89942805d3f0c60c2f2151cc9d7313886fa61b494',
             private_delta='mPushMatrix complete fourth word; short mPop composition'),
        dict(COMMON, ticket='RE881', content_scope='PASS_PRIVATE_EXACT_HASH_FINITE_INTERPOLATION_TRANSFER',
             procedure='FAIL_LEDGER_GAPS_AND_PREFLIGHT_INCIDENTS', fixtures=72,
             direct=48, compose=24, direct_push=24, direct_load=24, depths=[1,15,30],
             target_calls_per_engine=144, producer_target_engines=2,
             reviewer_target_calls=144, native_processes_per_executor=504,
             baseline_returned_red=120, baseline_ubsan_aborts_not_returns=24,
             candidate_green=144, mutant_rejections=[48,48,48], mutant_cases_each=72,
             producer_manifest_files=3125, reviewer_manifest_files=2887,
             approved_verdict_sha256='769611ea40940e0e2156038c2e74e3aaef5e32a1eed8c2a63b0d1bc498087cdc',
             candidate_sha256='8c61396366365a3de53136cf7070e1696df4546a8c89306f36207c7a4557cd52',
             baseline_sha256='1db1f98b2bf6f5cd803587d1165221cbb37b01aa6dc3108d6dbf76a47500657c',
             private_delta='iPushMatrix complete rotation words; iLoadMatrix complete fourth word; bounded iPop composition',
             static_caller_candidates=5, executed_callers=0),
    ],
}
SECTION = '''
<!-- RE882 PUBLICATION BEGIN -->
<section id="re882-publication-v1" data-schema="re882-reviewed-private-proof-publication-v1" data-publication-review="PENDING_INDEPENDENT_EXACT_HASH_REVIEW" data-integration="false">
<h2>ACTIVE RE882 — private-reviewed proof delivery history / metadata only</h2>
<p>Cette section seule est courante; les sections antérieures sont historiques et conservées. <a href="../stories/RE-882-reviewed-private-proof-publication.md">RE882 tracker / acceptance</a> · <a href="functions/re882-reviewed-private-proof-publication.md">Evidence / blockers</a> · <a href="generated/re882-reviewed-private-proof-publication-v1.json">Versioned metadata</a>.</p>
<p>ARCHIVED RE880: 48 fixtures (32 direct,16 compose); 80 target calls et384 native processes par producteur/reviewer, baseline96 returned RED etcandidate96 GREEN normal/strict. <a href="../stories/RE-880-private-push-pop-reviewed-proof.md">RE880 private push/pop</a>.</p>
<p>ARCHIVED RE881: 72 fixtures, depths1/15/30; baseline120 returned RED +24 UBSan aborts, PAS valid returns; candidate144 GREEN,504 native processes par producteur/reviewer. Producteur144 target calls par moteur (deux moteurs), reviewer144. <a href="../stories/RE-881-private-interpolation-transfer-reviewed-proof.md">RE881 private interpolation transfer</a>.</p>
<p>Finite private content PASS only. Global FAIL_HISTORIC_D9_AND_UNPROVEN_FRONTIERS; RE880 procedure FAIL_LEDGER_COVERAGE_AND_PREFLIGHT_INCIDENTS; RE881 procedure FAIL_LEDGER_GAPS_AND_PREFLIGHT_INCIDENTS; integration=false. RE879 global FAIL / procedure FAIL_LEDGER_AND_NESTED_LOCK conservés. Historic D9 FAIL nonreplayed.</p>
<p>Fresh public tests are metadata only, not fresh target/native replay. Public MATHS mRotY only; GetSpheres stub; frame helpers private/unintegrated. Natural camera, item.data, registration, dualstacks, hardware and gameplay unproved. Five static caller candidates are not executed. Prochaine proposition RE883: natural dualstack provenance and bounded caller. Publication pending independent exact-hash review, no commit/source integration.</p>
</section>
<!-- RE882 PUBLICATION END -->
'''

def metadata():
    return copy.deepcopy(EXPECTED)

def validate(data):
    # JSON canonical equality plus recursive type equality rejects bool/int aliasing.
    def exact(a,b):
        if type(a) is not type(b): return False
        if isinstance(b,dict): return set(a)==set(b) and all(exact(a[k],b[k]) for k in b)
        if isinstance(b,list): return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
        return a==b
    if not exact(data, EXPECTED): raise ValueError('exact reviewed RE882 schema/counts/scopes/pins required')
    return data

def preceding_dashboard(data):
    suffix = SECTION.encode() + b'</html>'
    if not data.endswith(suffix) or data.count(b'<!-- RE882 PUBLICATION BEGIN -->')!=1 or data.count(b'<!-- RE882 PUBLICATION END -->')!=1:
        raise ValueError('RE882 exact versioned suffix required')
    before = data[:-len(suffix)] + b'</html>'
    if hashlib.sha256(before).hexdigest()!=PRESERVED[PRIOR_DASHBOARD]:
        raise ValueError('historical dashboard changed')
    return before

LIMITS = '''integration=false; production_patch=false; public_helpers_green=false.
Historic D9 FAIL nonreplayed. RE879 content_scope PASS / global FAIL /
procedure FAIL_LEDGER_AND_NESTED_LOCK / integration=false preserved.
Public MATHS is mRotY only at HEAD c4614066bc6a48ad93bf4e047ab2912c84c72a8a;
GetSpheres public stub; GetBestFrame/GetFramesCL private and unintegrated.
five static caller candidates are not executed; no indirect/overlay completeness.
Natural camera, item.data, registration, natural dualstack provenance, hardware
and gameplay unproved. Raw software COP2 transfers are not independent hardware
arithmetic/sign-extension evidence. No complete GPR or transient-store proof.
Full final RAM2MiB, GTE384, two stacks1024 each and entry64 with canaries checked
in private finite proofs; external stack canaries were NOT established.
Finite i386 O0 actual-TU normal/fail-fast ASan UBSan does not prove O2
strict-aliasing or another ABI. No public source/helper behavior GREEN claimed.
'''

def story(ticket, data):
    rows = data['archived_private_results']
    row = next((r for r in rows if r['ticket']==ticket),None)
    text = '# '+ticket+' — reviewed private proof / metadata-only publication\n\n'
    text += 'Private content independently reviewed; public exact publication PENDING_INDEPENDENT_EXACT_HASH_REVIEW.\n\n'
    text += '## Progression\n- [x] Archived private producer/reviewer content decisions read and verdict hashes pinned.\n- [x] Versioned metadata contract, tracker, evidence and blockers supplied.\n- [ ] Independent review of exact RE882 staged hashes.\n- [ ] Source integration approval (not requested here).\n\n'
    text += '## Evidence\nARCHIVED_PRIVATE_PRODUCER_AND_INDEPENDENT_REVIEWER; no behavioral replay by this publication.\n'
    if row:
        text += '\n```json\n'+json.dumps(row,ensure_ascii=False,sort_keys=True,indent=2)+'\n```\n'
    else:
        text += 'RE880 and RE881 private scoped verdicts are summarized, not retroactively globally approved.\n'
        text += 'Fresh public metadata RED before generator implementation, followed by deterministic metadata GREEN; no public native/target tests.\n'
        text += 'Public hashes are supplied separately for independent exact delivery review.\n'
    text += '\n## Blockers\n'+LIMITS
    text += '\n## Acceptance\n- [x] Finite private content accepted only at pinned reviewed hashes, ARCHIVED attribution.\n- [x] Preserve global FAIL and procedural FAIL independently from content PASS.\n- [x] Deterministic portable public metadata; no ignored proof dependency in public regressions.\n- [ ] Independent publication security/content review against staged delivery hashes.\n- [ ] Prove naturally produced compatible dualstacks, upstream state and one bounded caller before any integration.\n- [ ] Hardware/gameplay validation remains outside this publication.\n\n'
    text += '## Handoff\nProposed RE883: natural dualstack provenance and one bounded authentic caller. No invented proof or re-enactment of closed finite matrices.\n'
    text += '[Publication / evidence](../reverse/functions/re882-reviewed-private-proof-publication.md) · [Versioned dashboard](../reverse/tomb5-progress-dashboard-re882-v1.html).\n'
    return text

def render(before):
    d = validate(metadata())
    if hashlib.sha256(before).hexdigest()!=PRESERVED[PRIOR_DASHBOARD] or not before.endswith(b'</html>'):
        raise ValueError('pinned historical dashboard required')
    out = {STORIES[t]: story(t,d).encode() for t in STORIES}
    out[JSON_PATH] = (json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
    fields = ['ticket','execution_attribution','fixtures','baseline_returned_red','baseline_ubsan_aborts_not_returns','candidate_green','native_processes_per_executor','content_scope','global_scope','procedure','integration','approved_verdict_sha256']
    stream=io.StringIO(newline=''); writer=csv.DictWriter(stream,fieldnames=fields,lineterminator='\n'); writer.writeheader()
    for row in d['archived_private_results']:
        writer.writerow({k: ('false' if row[k] is False else row[k]) for k in fields})
    out[CSV_PATH] = stream.getvalue().encode()
    out[REPORT] = ('''# RE882 — reviewed private proof publication v1

Publication PENDING_INDEPENDENT_EXACT_HASH_REVIEW; fresh public metadata checks
only. ARCHIVED private outcomes below are not fresh execution or public GREEN.

## Tracker / reviewed scope
RE880: 48 fixtures,32 direct/16 compose,80 fresh target calls and384 native
processes per producer AND reviewer, including mutants;96 baseline returned RED
and96 candidate GREEN normal/strict. Four mutants reject48/40/48/16 of48;
remaining coincident controls are not failures or accepted mutants.
RE881:72 fixtures (24 push,24 load,24 compose),depths1/15/30;120 baseline
returned RED +24 UBSan aborts (not valid returned comparisons);144 candidate
GREEN,504 native processes including216 mutants per producer AND reviewer.
Producer144 target calls per engine,two engines;reviewer144 target calls.
Three mutants reject48/72 each,24 coincident controls each. Independent expected
bytes and target executor authored by reviewer; reused native harness disclosed.

## Evidence provenance
Private candidate RE880 complete fourth-word push and short pop composition;
RE881 interpolation rotation-word push and fourth-word load/pop composition.
Parent archived manifest checks: RE880 producer2284/reviewer1776;
RE881 producer3125/reviewer2887, seals verified. This is parent verification
attribution, not a fresh manifest audit or target/native execution by RE882.
Exact verdict and candidate hashes live in the versioned JSON and stories.
RE880 procedure FAIL_LEDGER_COVERAGE_AND_PREFLIGHT_INCIDENTS;
RE881 procedure FAIL_LEDGER_GAPS_AND_PREFLIGHT_INCIDENTS.
Both global FAIL_HISTORIC_D9_AND_UNPROVEN_FRONTIERS remain unchanged.
RE880 prior private baseline16e31d730e8fe870be4f99c89942805d3f0c60c2f2151cc9d7313886fa61b494.

## Blockers / acceptance boundary
'''+LIMITS+'''
## Public acceptance / deterministic guards
Metadata tests fail closed on unknown fields, counts, status/type/hash drift;
raw evidence, secrets, binary/heavy additions and unapproved paths rejected.
Guard vocabulary in Python definitions is tested as code, not published raw
proof. No blanket legacy allowlist and no replacement historical guard hashes.
The new versioned HTML preserves all predecessor bytes via an exact reversible
section insertion before the closing html tag. Existing dashboard files untouched.
No raw code, opcodes, copyrighted assets/binaries or sealed archive edits.
User deletions BLOCKED-001/002 and the untracked technical report preserved.
Public metadata GREEN is not public helper GREEN or integration approval.
Fresh documentary selection RE821/RE830/RE866/RE882:64 passed,2 failed;
legacy RE830 predecessor guards: two failures preserved, caused by the older
RE820 exact-suffix guard seeing the unchanged RE866 reconstruction dashboard.
No historical hash guard repaired or weakened here. This is not a globally
GREEN regression suite; RE882's own31 metadata tests pass independently.

## Acceptance / next objective
- [x] Separate private content acceptance, retained global/procedure failures.
- [x] Portable deterministic metadata and versioned dashboard contract.
- [ ] Independent exact staged-hash publication review.
- [ ] Integration requires separately reviewed actual-TU regressions and scope.
- [ ] Proposed RE883 natural dualstack provenance and bounded authentic caller;
      camera/item.data/registration/hardware/gameplay remain unproved.
''').encode()
    out[DASHBOARD] = before[:-7]+SECTION.encode()+b'</html>'
    for path,payload in out.items(): guard_output(path,payload)
    return out

RAW = re.compile(rb'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|raw_opcode|payload_offset|data:image|```(?:asm|mips|cpp|c)\b', re.I)
SECRET = re.compile(rb'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|(?:api[_-]?key|password|secret)\s*[:=]\s*[\"\x27][^\"\x27\s]{12,}',re.I)

def guard_added(path, payload):
    p=Path(path)
    if p.is_absolute() or '..' in p.parts or p.suffix not in {'.md','.html','.json','.csv','.py'}:
        raise ValueError('unsafe or heavy path')
    if path not in PUBLIC_PATHS:
        raise ValueError('outside explicit RE882 publication scope')
    if len(payload)>100000 or b'\0' in payload:
        raise ValueError('heavy/binary content')
    payload.decode('utf-8')
    if SECRET.search(payload): raise ValueError('secret content')
    # Guard/test sources contain intentionally rejected strings; no raw-output bypass.
    if p.suffix!='.py' and RAW.search(payload): raise ValueError('raw evidence content')

def guard_output(path,payload):
    if path not in OUTPUT_PATHS: raise ValueError('not generated public metadata')
    if path==DASHBOARD:
        preceding_dashboard(payload)
        guard_added(path, SECTION.encode())
    else:
        guard_added(path,payload)

def check():
    for path,pin in PRESERVED.items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=pin:
            raise ValueError('preserved source/dashboard changed: '+path)
    for path,data in render((ROOT/PRIOR_DASHBOARD).read_bytes()).items():
        if (ROOT/path).read_bytes()!=data: raise ValueError('generated drift: '+path)
    print('RE882 deterministic public metadata and preserved historical/source pins PASS')

def check_staged():
    paths=subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=ROOT).decode().split('\0')
    paths=[p for p in paths if p]
    if set(paths)!=set(PUBLIC_PATHS): raise ValueError('index must contain exactly explicit RE882 paths')
    for path in paths:
        data=subprocess.check_output(['git','show',':'+path],cwd=ROOT)
        if data!=(ROOT/path).read_bytes(): raise ValueError('index/worktree drift: '+path)
        diff=subprocess.check_output(['git','diff','--cached','--unified=0','--',path],cwd=ROOT)
        added=b'\n'.join(line[1:] for line in diff.splitlines() if line.startswith(b'+') and not line.startswith(b'+++'))
        if path==DASHBOARD:
            # Every inherited byte pinned, new section scanned; no wholesale allowlist.
            preceding_dashboard(data); guard_added(path,SECTION.encode())
        else: guard_added(path,added)
    check()
    print('RE882 exact staged scope/index equality/secret/heavy/raw-added-line guards PASS: '+str(len(paths))+' files')

def generate():
    import fcntl
    with (ROOT/'build/reverse/autonomy-mutation.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        out=render((ROOT/PRIOR_DASHBOARD).read_bytes())
        for path,data in out.items():
            p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    check()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    parser.add_argument('--check-staged',action='store_true')
    args=parser.parse_args()
    if args.write: generate()
    elif args.check_staged: check_staged()
    else: check()
