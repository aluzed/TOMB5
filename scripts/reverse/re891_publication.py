"""RE891 deterministic PUBLIC_METADATA_TESTS_ONLY publication; no behavioral replay."""
import argparse
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
ROOT=Path(__file__).resolve().parents[2]
PRIOR_DASHBOARD='docs/reverse/tomb5-progress-dashboard-re882-v1.html'
DASHBOARD='docs/reverse/tomb5-progress-dashboard-re891-v1.html'
STORY='docs/stories/RE-891-reviewed-private-proof-publication.md'
REPORT='docs/reverse/functions/re891-reviewed-private-proof-publication.md'
JSON_PATH='docs/reverse/generated/re891-reviewed-private-proof-publication-v1.json'
CSV_PATH='docs/reverse/generated/re891-reviewed-private-proof-tracker-v1.csv'
OUTPUT_PATHS=(STORY,REPORT,JSON_PATH,CSV_PATH,DASHBOARD)
PUBLIC_PATHS=OUTPUT_PATHS+('scripts/reverse/re891_publication.py','tests/reverse/test_re891_publication.py')
PRESERVED={PRIOR_DASHBOARD:'bb8a7fd25083b1d4388cd459e6ec5d9d6f6f5cff9fe8f536b4c3b4b3d41893c2','SPEC_PSXPC_N/MATHS.C':'59e70b260ae67d613e5fa74486c728a63bd3bb7ae4727537e293d4c057d9b7fa'}
COMMON=dict(execution_attribution='ARCHIVED_PRIVATE_PRODUCER_AND_INDEPENDENT_REVIEWER',candidate_sha256='a23d973e7f99876092411ffe8e4c159670318fd1c8e6f2d15a5c1811af9377cb',fullraw_bytes=2528,caller_returned=False,integration=False,global_scope='FAIL_HISTORIC_D9_AND_UNPROVEN_FRONTIERS',procedure='FAIL_HISTORICAL_LEDGER_AND_AUTHORING_INCIDENTS',domain='constructed flags2 fractions1/2/3 identity nonsaturation; zero compact angles only',abi='i386 O0 normal and fail-fast ASan UBSan actual MATHS SPHERES LIBGTE TUs')
EXPECTED={
 'schema':'re891-reviewed-private-proof-publication-v1',
 'publication_review':'PENDING_INDEPENDENT_EXACT_HASH_REVIEW',
 'fresh_execution_scope':'PUBLIC_METADATA_TESTS_ONLY',
 'integration':False,'production_patch':False,'public_helpers_green':False,
 'global_scope':'FAIL_HISTORIC_D9_AND_UNPROVEN_FRONTIERS',
 'historic_d9':'FAIL_NON_REPLAYED',
 'procedure':'FAIL_HISTORICAL_LEDGER_EXPIRED_AUTHORING_LEASES_AND_CHECKER_ARCHIVES',
 'public_maths_scope':'unchanged mRotY previous integration only; private helpers unintegrated',
 'next_ticket':'RE892','next_objective':'bounded authentic InterpolateMatrix private proof; not whole caller return',
 'projection':dict(gte_bytes=384,stacks_bytes=[1024,1024],scalars_bytes=32,separate_sentinels_bytes=64,whole_native_ram=False,adjacent_canaries=False),
 'target_cpu_comparison':'full RAM2MiB GTE96 words GPR32 HI LO ordered visits and transfers; inherited independent CPU freshly replayed in archives, not newly authored',
 'unproved':['natural_startup','natural_dualstack_provenance','natural_camera','item.data','registration','hardware','gameplay','general_GTE','nonzero_rotation_geometry','complete_caller_return','O2_strict_aliasing','alternative_ABI','native_whole_RAM','transient_store_exhaustiveness'],
 'archived_private_results':[
 dict(COMMON,ticket='RE886',approved_verdict_sha256='d19a201e8c2a9fdde08439f223bfb311dc805dd51c709e34ca1c000e483b13cd',content_scope='PASS_PRIVATE_FINITE_FULLRAW_RE886',private_delta='three signed full32 IR1 IR2 IR3 writers in iTranslateXYZ2; all later composition candidate unchanged',frontier='stop before iPushMatrix body; caller never returned',reviewer_accepted=dict(target=3,cpu=3,declarative=3,native=18,baseline_red=6,candidate_green=6,rollback_red=6),producer_accepted=dict(target=3,cpu=3,native=42,baseline_red=6,candidate_green=6,individual_mutant_native=18,causal_native=12)),
 dict(COMMON,ticket='RE887',approved_verdict_sha256='40951d551720e671ffc790d672f61dd41b14df00293414694406207b345d742d',content_scope='PASS_PRIVATE_FINITE_IPUSH_RETURN',frontier='real iPushMatrix tail-jump mPushMatrix returned; stop before bone iTranslateXYZ; caller never returned',reviewer_accepted=dict(target=3,cpu=3,declarative=3,native=12,candidate_green=6,pushstub_red=6),producer_accepted=dict(target=3,cpu=3,declarative=3,native=12,candidate_green=6,pushstub_red=6),reviewer_cumulative=dict(completed_replays=4,target=12,cpu=12,native=48,candidate_green=24,pushstub_red=24),historical_failure='four checker FAIL namespaces preserved; expired150s authoring holder not retrocertified'),
 dict(COMMON,ticket='RE888',approved_verdict_sha256='25e152cffb4c0090218a8617c4dbfcaf86e87f1091cbb8c2d533f03266bb13cd',content_scope='PASS_PRIVATE_FINITE_BONE_TRANSLATION_RETURN',frontier='bone iTranslateXYZ returned; stop before primary compact bone rotation; caller never returned',reviewer_accepted=dict(target=3,cpu=3,declarative=3,native=18,candidate_green=6,translationstub_red=6,pushstub_red=6),producer_accepted=dict(target=3,cpu=3,declarative=3,native=18,candidate_green=6,translationstub_red=6,pushstub_red=6),historical_failure='initial checker FAIL retained; sealed aggregate false compared combined12 RED with6; each ablation group6 sensitive independently'),
 dict(COMMON,ticket='RE889',approved_verdict_sha256='4451340ccbe61b959ce1210ae08641be886c4813bd2bf0f73efb31de735895e7',content_scope='PRIVATE_FINITE_PRIMARY_BONE_ZERO_COMPACT',frontier='primary compact zero Y X Z returned; frames10 to12 short elements, four bytes; stop before secondary rotation; caller never returned',reviewer_accepted=dict(target=3,cpu=3,declarative=3,native=18,candidate_green=6,rotationstub_pointer_red=6,rotationstub_fullraw_green=6,pushstub_fullraw_red=6),producer_accepted=dict(target=3,cpu=3,declarative=3,native=18,candidate_green=6,rotationstub_pointer_red=6,pushstub_fullraw_red=6),producer_attempt_totals=dict(attempts=2,target=6,cpu=6,declarative=6,native=36),reviewer_additional_declarative=3,historical_failure='producer PIC checker FAIL and reviewer expectation FAIL preserved; zero rotation ablation sensitive only to pointer, not geometry'),
 dict(COMMON,ticket='RE890',approved_verdict_sha256='7f1f8f1ef622386f651091abf129b7091ae1113467d68c63fddf374eb33282bf',content_scope='PASS_PRIVATE_FINITE_SECONDARY_COMPOSITION',frontier='secondary compact zero Y X Z returned, frames22 to24 short elements four bytes; position translate zero returned; stop BEFORE InterpolateMatrix; caller never returned',reviewer_accepted=dict(target=3,cpu=3,declarative=3,native=18,candidate_green=6,rotationstub_pointer_red=6,rotationstub_fullraw_green=6,pushstub_fullraw_red=6),producer_accepted=dict(target=3,cpu=3,declarative=3,native=18,candidate_green=6,rotationstub_pointer_red=6,pushstub_fullraw_red=6),producer_attempt_totals=dict(target=9,cpu=9,declarative=9,native=37),producer_attempt_native=[1,18,18],corrected_review_rerun=False,historical_failure='first FAIL archives immutable; corrected independent archive checker clarification only, no extra target CPU native replay')
 ]}
SECTION='''
<!-- RE891 PUBLICATION BEGIN -->
<section id="re891-publication-v1" data-schema="re891-reviewed-private-proof-publication-v1" data-publication-review="PENDING_INDEPENDENT_EXACT_HASH_REVIEW" data-integration="false">
<h2>CURRENT RE891 — ARCHIVED private RE886–RE890 finite proof / public metadata only</h2>
<p>This section alone is current; inherited sections remain byte-identical historical records. <a href="../stories/RE-891-reviewed-private-proof-publication.md">Story / acceptance</a> · <a href="functions/re891-reviewed-private-proof-publication.md">Evidence / blockers</a> · <a href="generated/re891-reviewed-private-proof-publication-v1.json">Versioned metadata</a> · <a href="generated/re891-reviewed-private-proof-tracker-v1.csv">Tracker</a>.</p>
<p>RE886 three signed full32 IR stores private correction; RE887 real iPush return; RE888 bone translation return; RE889 primary compact zero rotation return; RE890 secondary compact zero rotation and position translate zero return, stop BEFORE InterpolateMatrix. Caller never returned.</p>
<p>Each accepted reviewer matrix:3 target,3 inherited CPU,3 declarative. Native totals18/12/18/18/18 respectively. RE887 cumulative12 target/12 CPU/48 native separate; RE889 extra3 reviewer declaratives; RE890 corrected review no rerun. Pointer-only zero-angle sensitivity is not geometry proof.</p>
<p>FULLRAW2528 unmasked projection, constructed identity/nonsaturation only. Global FAIL, historical ledger/expired authoring leases/checker FAIL immutable; integration=false. Public MATHS unchanged mRotY previous only. Fresh public tests metadata-only, not fresh target/native execution. PENDING_INDEPENDENT_EXACT_HASH_REVIEW. Next RE892: bounded InterpolateMatrix; natural startup/camera/item.data/registration/hardware/gameplay remain unproved.</p>
</section>
<!-- RE891 PUBLICATION END -->
'''

def metadata():return copy.deepcopy(EXPECTED)
def validate(data):
    def exact(a,b):
        if type(a) is not type(b):return False
        if isinstance(b,dict):return set(a)==set(b) and all(exact(a[k],b[k]) for k in b)
        if isinstance(b,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
        return a==b
    if not exact(data,EXPECTED):raise ValueError('exact RE891 schema types counts scopes and verdict pins required')
    return data

def preceding_dashboard(data):
    suffix=SECTION.encode()+b'</html>'
    if not data.endswith(suffix) or data.count(b'<!-- RE891 PUBLICATION BEGIN -->')!=1 or data.count(b'<!-- RE891 PUBLICATION END -->')!=1:raise ValueError('exact unique RE891 suffix required')
    before=data[:-len(suffix)]+b'</html>'
    if hashlib.sha256(before).hexdigest()!=PRESERVED[PRIOR_DASHBOARD]:raise ValueError('predecessor bytes changed')
    return before

LIMITS='''integration=false; production_patch=false; public_helpers_green=false.
Global FAIL_HISTORIC_D9_AND_UNPROVEN_FRONTIERS; historic D9 FAIL nonreplayed.
Procedure historical FAIL: discovery/transport ledger gaps, expired authoring
leases and checker FAIL archives retained immutably, no retrocertification.
Public MATHS unchanged: previous mRotY only. GetSpheres public stub; frame and
other repaired helpers private/unintegrated. Shared actual LIBGTE software is
not hardware evidence; inherited standalone CPU freshly replayed in archived
proofs is independent of Unicorn, not newly authored reviewer interpreter.
FULLRAW2528 unmasked native projection: GTE384, stacks1024 each, scalars32,
separate sentinels64; not whole native RAM or physically adjacent canaries.
Item144 and position12 invariants, no exhaustive transient-store proof.
Finite constructed flags2 fractions1/2/3 identity nonsaturation bone7/-9/13;
zero compact Y/X/Z angles. Pointer-only ablation sensitivity is NOT geometric
sensitivity or general trig coverage. i386 O0 normal/fail-fast ASan UBSan actual
TUs do not establish O2 strict aliasing or another ABI. Native stop hook after
callee prologue before semantic body with exception is NOT caller return.
caller never returned. Natural startup, natural dualstack provenance, camera,
item.data, registration, hardware and gameplay remain unproved.
User deletions BLOCKED-001/002 and untracked technical report preserved.
'''

def document(report=False):
    text='# RE891 — reviewed private proof publication v1\n\nPENDING_INDEPENDENT_EXACT_HASH_REVIEW; ARCHIVED evidence, PUBLIC_METADATA_TESTS_ONLY fresh execution.\n\n'
    text+='## Progression\n- [x] Tests authored before generator; RED missing generator observed.\n- [x] Five independently accepted private verdict hashes pinned.\n- [x] Portable metadata, tracker, evidence and versioned HTML delivered.\n- [ ] Independent exact-public-hash publication review.\n- [ ] Integration approval, not requested.\n\n## Evidence\n'
    for r in EXPECTED['archived_private_results']:
        text+= '\n### '+r['ticket']+' — '+r['content_scope']+'\n'+r['frontier']+'\nApproved private verdict SHA256: '+r['approved_verdict_sha256']+'\nArchived reviewer accepted matrix: '+json.dumps(r['reviewer_accepted'],sort_keys=True)+'.\n'
        for key in ['producer_accepted','producer_attempt_totals','reviewer_cumulative','reviewer_additional_declarative','corrected_review_rerun','historical_failure']:
            if key in r:text+=key+': '+json.dumps(r[key],sort_keys=True)+'.\n'
    text+='\nCandidate SHA256 shared across five proofs: '+COMMON['candidate_sha256']+'. RE886 private delta is exactly three signed full32 IR stores; later units extend composition without candidate changes.\n'
    text+='No target/native proof rerun by RE891. Counts above describe archived scoped reviewer execution. Accepted matrices, producer attempt totals and reviewer cumulative replays are separate; corrected RE890 clarification adds ZERO executions. Earlier FAIL verdicts/seals immutable. Parent HANDOFF authenticates lineage inventories; RE891 directly verifies five verdict hashes, not a new full raw archive audit.\n'
    text+='\n## Blockers\n'+LIMITS
    text+='\n## Acceptance\n- [x] Finite private content PASS only; global/procedure FAIL retained separately.\n- [x] Exact recursive types reject bool/int aliases, unknown fields and hash/count drift.\n- [x] Deterministic public-only metadata export without ignored proof dependencies.\n- [x] Raw/secret/heavy guards with benign same-path controls; generator vocabulary separate.\n- [x] Unique exact HTML suffix inversely preserves predecessor bytes; no predecessor guard rewrite.\n- [ ] Independent publication review remains PENDING, no producer commit/push claim.\n- [ ] Broader compatibility result recorded in private delivery evidence, not assumed globally GREEN.\n- [ ] Natural/hardware/gameplay validation and integration remain blocked.\n\n## Handoff\nRE892: bounded authentic InterpolateMatrix private proof; stop BEFORE InterpolateMatrix remains RE890 frontier, not whole caller return.\n[Tracker](../generated/re891-reviewed-private-proof-tracker-v1.csv) · [Metadata](../generated/re891-reviewed-private-proof-publication-v1.json).\n'
    if not report:
        text=text.replace('(../generated/', '(../reverse/generated/')
        text+='[Evidence / blockers](../reverse/functions/re891-reviewed-private-proof-publication.md) · [Dashboard](../reverse/tomb5-progress-dashboard-re891-v1.html).\n'
    return text

def render(before):
    d=validate(metadata())
    if hashlib.sha256(before).hexdigest()!=PRESERVED[PRIOR_DASHBOARD] or not before.endswith(b'</html>'):raise ValueError('pinned predecessor required')
    out={STORY:document().encode(),REPORT:document(True).encode(),JSON_PATH:(json.dumps(d,indent=2,sort_keys=True)+'\n').encode(),DASHBOARD:before[:-7]+SECTION.encode()+b'</html>'}
    fields=['ticket','execution_attribution','content_scope','fullraw_bytes','reviewer_target','reviewer_cpu','reviewer_declarative','reviewer_native','frontier','global_scope','procedure','integration','approved_verdict_sha256']
    stream=io.StringIO(newline='');w=csv.DictWriter(stream,fieldnames=fields,lineterminator='\n');w.writeheader()
    for r in d['archived_private_results']:
        row={k:r[k] for k in fields if k in r};row['integration']='false'
        for k in ['target','cpu','declarative','native']:row['reviewer_'+k]=r['reviewer_accepted'][k]
        w.writerow(row)
    out[CSV_PATH]=stream.getvalue().encode()
    for p,b in out.items():guard_output(p,b)
    return out

RAW=re.compile(rb'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|raw_opcode|payload_offset|data:image|```(?:asm|mips|cpp|c)\b',re.I)
SECRET=re.compile(rb'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|(?:api[_-]?key|password|secret)\s*[:=]\s*[\"\x27][^\"\x27\s]{12,}',re.I)
def guard_added(path,payload):
    p=Path(path)
    if p.is_absolute() or '..' in p.parts or path not in PUBLIC_PATHS:raise ValueError('outside explicit RE891 scope')
    if len(payload)>100000 or b'\0' in payload:raise ValueError('heavy binary content')
    payload.decode('utf-8')
    if SECRET.search(payload):raise ValueError('secret')
    if p.suffix!='.py' and RAW.search(payload):raise ValueError('raw evidence')
def guard_output(path,payload):
    if path not in OUTPUT_PATHS:raise ValueError('not generated metadata')
    if path==DASHBOARD:preceding_dashboard(payload);guard_added(path,SECTION.encode())
    else:guard_added(path,payload)
def check():
    for p,h in PRESERVED.items():
        if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h:raise ValueError('preserved drift '+p)
    for p,b in render((ROOT/PRIOR_DASHBOARD).read_bytes()).items():
        if (ROOT/p).read_bytes()!=b:raise ValueError('generated drift '+p)
    print('RE891 deterministic PUBLIC_METADATA_TESTS_ONLY guards PASS')
def check_staged():
    paths=subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=ROOT).decode().split('\0');paths=[p for p in paths if p]
    if set(paths)!=set(PUBLIC_PATHS):raise ValueError('exact RE891 staged scope required')
    for p in paths:
        b=subprocess.check_output(['git','show',':'+p],cwd=ROOT)
        if b!=(ROOT/p).read_bytes():raise ValueError('index/worktree drift '+p)
        if p==DASHBOARD:guard_output(p,b)
        else:guard_added(p,b)
    check()
def generate():
    import fcntl
    import datetime
    import os
    def owner():
        for pid in (1925646,1925613):os.kill(pid,0)
        if datetime.datetime.now(datetime.timezone.utc)>=datetime.datetime.fromisoformat('2026-10-11T11:56:00+02:00'):raise RuntimeError('expired ownership')
        if subprocess.run(['flock','-n','-E','1',str(ROOT/'build/reverse/autonomy-repo.lock'),'true']).returncode!=1:raise RuntimeError('no owner contention')
    for p,b in render((ROOT/PRIOR_DASHBOARD).read_bytes()).items():
        owner()
        with (ROOT/'build/reverse/autonomy-mutation.lock').open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX);owner();(ROOT/p).write_bytes(b);owner()
        owner()
    check()
if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--write',action='store_true');a.add_argument('--check-staged',action='store_true');args=a.parse_args()
    if args.write:generate()
    elif args.check_staged:check_staged()
    else:check()
