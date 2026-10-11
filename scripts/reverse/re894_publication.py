"""RE894 deterministic portable metadata only; no behavioral replay or integration."""
import argparse
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[2]
PRIOR_DASHBOARD='docs/reverse/tomb5-progress-dashboard-re891-v1.html'
DASHBOARD='docs/reverse/tomb5-progress-dashboard-re894-v1.html'
STORY='docs/stories/RE-894-private-repair-and-finite-caller-return-publication.md'
REPORT='docs/reverse/functions/re894-private-repair-and-finite-caller-return-publication.md'
JSON_PATH='docs/reverse/generated/re894-private-repair-and-finite-caller-return-v1.json'
CSV_PATH='docs/reverse/generated/re894-private-proof-tracker-v1.csv'
OUTPUT_PATHS=(STORY,REPORT,JSON_PATH,CSV_PATH,DASHBOARD)
PUBLIC_PATHS=OUTPUT_PATHS+('scripts/reverse/re894_publication.py','tests/reverse/test_re894_publication.py')
PRESERVED={PRIOR_DASHBOARD:'e4dff837eb09919a6ebc2ae6bc2384f29e2265b3ca025ec15175daf901e9f0ad','SPEC_PSXPC_N/MATHS.C':'59e70b260ae67d613e5fa74486c728a63bd3bb7ae4727537e293d4c057d9b7fa'}
CANDIDATE='9002cac7b27566f572a8b744cabddc36431b0b00fae9599d6342f156a523ba88'
COMMON=dict(execution_attribution='ARCHIVED_PRIVATE_PRODUCER_AND_INDEPENDENT_REVIEWER',candidate_sha256=CANDIDATE,fullraw_bytes=2528,integration=False,domain='constructed flags2 rate4 fractions1/2/3 identity nonsaturation bone7/-9/13 zero compact angles',abi='i386 O0 normal and fail-fast ASan UBSan actual MATHS SPHERES LIBGTE TUs')
EXPECTED={
 'schema':'re894-private-repair-and-finite-caller-return-v1',
 'publication_review':'PENDING_INDEPENDENT_EXACT_HASH_REVIEW',
 'fresh_execution_scope':'PUBLIC_METADATA_TESTS_ONLY',
 'integration':False,'production_patch':False,'public_helpers_green':False,
 'global_scope':'FAIL_HISTORIC_D9_NATURAL_NONZERO_GENERAL_UNPROVEN',
 'historic_d9':'FAIL_NON_REPLAYED',
 'procedure':'FAIL_HISTORICAL_LEDGER_AUTHORING_CHECKER_AND_ENOSPC_INCIDENTS_PRESERVED',
 'public_maths_scope':'unchanged previous mRotY only; GetSpheres public stub and frame helpers private unintegrated',
 'next_ticket':'RE895','next_objective':'natural upstream caller provenance or separately bounded nonzero rotation domain; do not rerun closed finite matrices',
 'projection':dict(gte_bytes=384,stacks_bytes=[1024,1024],scalars_bytes=32,separate_sentinels_bytes=64,position_bytes=12,whole_native_ram=False,adjacent_canaries=False),
 'target_cpu_comparison':'full RAM2MiB GTE96 GPR32 HI LO ordered visits/transfers; inherited independent CPU replayed in archives not newly authored',
 'unproved':['natural_startup','natural_dualstack_provenance','natural_camera','item.data','registration','hardware','gameplay','general_GTE','nonzero_rotation_geometry','O2_strict_aliasing','alternative_ABI','native_whole_RAM','transient_store_exhaustiveness'],
 'durable_review_archive':dict(path='build/reverse/autonomy-20261011/re893-review-evidence-durable.tar.xz',bytes=4310312,sha256='b7fb2dd9e9be3e4fad2720bb538df2f123fe2ca8742a1aacbc2ea0b37c73f50d',original_declared_roots_retained=True,parent_inventory_entries=[29,16,415,6],publication_verification='exact archive and two verdict member hashes only; full inventories authenticated by parent, not fresh publication raw audit'),
 'archived_private_results':[
 dict(COMMON,ticket='RE892',approved_verdict_sha256='7b03420c8563a49cd45c98e44d2f743b88843098a93d5c8624a8e6ed1024a9e0',content_scope='PASS_PRIVATE_FINITE_INTERPOLATEMATRIX_REPAIR',caller_returned=False,frontier='InterpolateMatrix returned and positions written; stop BEFORE mCopyMatrix body, native exception is not caller return',expression_scope=dict(algebra_inspected=12,translation_sensitive=3,identity_rotation_zero_difference=9),private_delta='12 function-local fraction3 expressions secondary minus arithmetic-shifted difference; only three translations behaviorally sensitive in this identity domain',reviewer_accepted=dict(target=3,cpu=3,declarative=3,native=42,cpu_mutants=3),producer_accepted=dict(target=3,cpu=3,declarative=3,native=54,cpu_mutants=3),baseline_native=dict(green=4,red=2),candidate_native_green=6,historical_failure='initial mutant SyntaxError FAIL seal immutable; separate qualification correction does not add 30 native replays'),
 dict(COMMON,ticket='RE893',approved_verdict_sha256='7d9ec09df201b7ec50067511dc37bacd55cf3932ada7ae1f7147bfe83051595f',completion_verdict_sha256='23bc5208ba55ba8c7f0440ca5d7fa101577da2b6daad4d403e1b88b9f9abeb2e',content_scope='PASS_PRIVATE_FINITE_CONSTRUCTED_FULL_CALLER_RETURN',caller_returned=True,frontier='real GetJointAbsPosition mCopyMatrix body through shared tail and completed target return with restored RA/SP; native direct RET without exception, including six uninstrumented executions',positions=[[26,-40,54],[34,-48,62],[43,-55,71]],reviewer_accepted=dict(target=3,cpu=3,declarative=3,initial_ram=3,native=36,candidate_green=6,ablation_red=18,pad_mutant_red=6,uninstrumented_direct_return=6,cpu_mutants=2),producer_accepted=dict(target=3,cpu=3,declarative=3,initial_ram=3,native=30,candidate_green=6,ablation_red=18,pad_mutant_red=6,cpu_mutants=2),ablation_scope='copy and push sensitive to RAW only, interpolation sensitive to RAW and positions; pad upper word sensitive',historical_failure='first producer positions-push expectation FAIL; initial canonical ENOSPC review FAIL, recovery reporter FAIL and partial archive FAIL immutable; accepted tmpfs evidence persisted later in exact durable compressed archive, original volatile completion limitation retained')
 ]}
SECTION='''
<!-- RE894 PUBLICATION BEGIN -->
<section id="re894-publication-v1" data-schema="re894-private-repair-and-finite-caller-return-v1" data-publication-review="PENDING_INDEPENDENT_EXACT_HASH_REVIEW" data-integration="false">
<h2>CURRENT RE894 — ARCHIVED RE892 private correction / RE893 finite constructed completed caller return</h2>
<p>This section alone is current; all preceding RE891 bytes remain historical and unchanged. <a href="../stories/RE-894-private-repair-and-finite-caller-return-publication.md">Story / acceptance</a> · <a href="functions/re894-private-repair-and-finite-caller-return-publication.md">Evidence / blockers</a> · <a href="generated/re894-private-repair-and-finite-caller-return-v1.json">Metadata</a> · <a href="generated/re894-private-proof-tracker-v1.csv">Tracker</a>.</p>
<p>RE892 fraction3 private repair:12 expressions algebra inspected,3 translations behaviorally sensitive,9 identity rotations zero difference. RE893 real GetJointAbsPosition mCopyMatrix body through shared tail and completed target return; native direct RET without exception,6 uninstrumented executions. Constructed fractions1/2/3 positions (26,-40,54), (34,-48,62), (43,-55,71).</p>
<p>Reviewer accepted RE892:3 target/3 CPU/3 declarative/42 native/3 CPU mutants; RE893:3 target/3 CPU/3 declarative/3 initialRAM/36 native/2 CPU mutants. Producer native54/30 separately scoped. FULLRAW2528 plus positions12, flags2 identity zero compact angles only. Natural upstream, hardware, general GTE and nonzero rotation unproved.</p>
<p>Global FAIL; historical procedure/checker/ENOSPC FAIL preserved; integration=false. No production patch; public MATHS previous mRotY only, GetSpheres stub and frame helpers unintegrated. Fresh PUBLIC_METADATA_TESTS_ONLY, not target/native replay. PENDING_INDEPENDENT_EXACT_HASH_REVIEW. Next RE895 natural provenance or bounded nonzero domain; no redundant closed matrices.</p>
</section>
<!-- RE894 PUBLICATION END -->
'''

def metadata():return copy.deepcopy(EXPECTED)
def validate(data):
    def exact(a,b):
        if type(a) is not type(b):return False
        if isinstance(b,dict):return set(a)==set(b) and all(exact(a[k],b[k]) for k in b)
        if isinstance(b,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
        return a==b
    if not exact(data,EXPECTED):raise ValueError('exact RE894 recursive types counts scopes hashes required')
    return data

def preceding_dashboard(data):
    suffix=SECTION.encode()+b'</html>'
    if not data.endswith(suffix) or data.count(b'<!-- RE894 PUBLICATION BEGIN -->')!=1 or data.count(b'<!-- RE894 PUBLICATION END -->')!=1:raise ValueError('exact unique RE894 suffix required')
    before=data[:-len(suffix)]+b'</html>'
    if hashlib.sha256(before).hexdigest()!=PRESERVED[PRIOR_DASHBOARD]:raise ValueError('predecessor bytes changed')
    return before

LIMITS='''integration=false; production_patch=false; public_helpers_green=false.
Global FAIL: historic D9 nonreplayed; natural/nonzero/general frontier unproved.
Procedure historical FAIL: ledger gaps, expired authoring leases, checker FAILs
and ENOSPC incidents preserved; no retrocertification of any original seal.
Public MATHS unchanged previous mRotY only; GetSpheres public stub; frame and
other private helpers NOT activated. Shared real LIBGTE software is not hardware.
Inherited independent CPU freshly replayed in archived reviews, not newly authored.
FULLRAW2528 unmasked projection GTE384, two stacks1024, scalars32, separate
sentinels64 plus positions12: not whole native RAM or adjacent canary coverage.
Constructed flags2 rate4 fractions1/2/3 identity nonsaturation, compact angles
zero; no general rotation geometry or saturation proof. Item upstream constructed,
not naturally reached startup/camera/item.data/registration/gameplay provenance.
Actual TUs i386 O0 normal/fail-fast ASan UBSan do not prove O2 strict aliasing,
alternative ABI or exhaustive transient stores. RE893 completed direct RET is
real finite caller completion, not natural upstream proof. RE892 exception stop
was NOT caller completion. Producer and reviewer accepted counts separate;
failed attempts and previous closed matrices excluded, never retroactively GREEN.
RE893 accepted original tmpfs roots preserved in exact durable compressed archive;
completion verdict's original volatile-storage warning remains immutable. Initial
ENOSPC and partial durable copy FAIL retained; publication hashes archive/member
verdicts only, parent authenticated full inventory/seal lineage separately.
User deletions BLOCKED-001/002 and untracked technical report preserved.
'''

def document(report=False):
    text='# RE894 — private repair and finite caller-return publication v1\n\nARCHIVED private evidence; fresh PUBLIC_METADATA_TESTS_ONLY. PENDING_INDEPENDENT_EXACT_HASH_REVIEW.\n\n'
    text+='## Progression\n- [x] Tests authored before generator, missing-generator RED observed.\n- [x] Exact RE892 and durable RE893 verdict identities authenticated.\n- [x] Portable metadata, tracker, evidence/blockers and versioned dashboard delivered.\n- [ ] Independent exact-public-hash publication review.\n- [ ] Production integration approval, not requested.\n\n## Evidence\n'
    for r in EXPECTED['archived_private_results']:
        text+='\n### '+r['ticket']+' — '+r['content_scope']+'\n'+r['frontier']+'\nApproved private verdict SHA256: '+r['approved_verdict_sha256']+'\n'
        for k in ['completion_verdict_sha256','private_delta','expression_scope','positions','reviewer_accepted','producer_accepted','baseline_native','candidate_native_green','ablation_scope','historical_failure']:
            if k in r:text+=k+': '+json.dumps(r[k],sort_keys=True)+'.\n'
    text+='\nPrivate candidate SHA256: '+CANDIDATE+'. No public integration.\nDurable review archive: '+json.dumps(EXPECTED['durable_review_archive'],sort_keys=True)+'.\nNo fresh target/native replay by RE894; counts describe archived accepted matrices, not publication executions or failed-attempt totals. RE893 completion rechecks the same accepted replay, not another matrix.\n'
    text+='\n## Blockers\n'+LIMITS
    text+='\n## Acceptance\n- [x] Private finite content PASS separated from global/procedure FAIL.\n- [x] Real finite caller return distinguished from natural caller provenance.\n- [x] Exact recursive types, unknown-field/count/hash/frontier drift fail closed.\n- [x] Raw/secret/heavy guards include benign same-path controls.\n- [x] New dashboard inverse preserves all RE891 predecessor bytes.\n- [x] Public-only export requires no ignored proof dependencies.\n- [ ] External exact-public-hash review remains PENDING; producer self-check not review.\n- [ ] Broad global GREEN not claimed; historical two RE830 failures unchanged and not rerun here.\n- [ ] Natural/hardware/nonzero/general GTE and integration remain blocked.\n\n## Handoff\nRE895: natural upstream caller provenance or separately bounded nonzero rotation domain, not another replay of closed finite matrices.\n'
    prefix='../' if report else '../reverse/'
    text+='[Tracker]('+prefix+'generated/re894-private-proof-tracker-v1.csv) · [Metadata]('+prefix+'generated/re894-private-repair-and-finite-caller-return-v1.json) · [Dashboard]('+prefix+'tomb5-progress-dashboard-re894-v1.html).\n'
    if not report:text+='[Evidence / blockers](../reverse/functions/re894-private-repair-and-finite-caller-return-publication.md).\n'
    return text

def render(before):
    d=validate(metadata())
    if hashlib.sha256(before).hexdigest()!=PRESERVED[PRIOR_DASHBOARD] or not before.endswith(b'</html>'):raise ValueError('pinned predecessor required')
    out={STORY:document().encode(),REPORT:document(True).encode(),JSON_PATH:(json.dumps(d,indent=2,sort_keys=True)+'\n').encode(),DASHBOARD:before[:-7]+SECTION.encode()+b'</html>'}
    fields=['ticket','content_scope','execution_attribution','caller_returned','fullraw_bytes','reviewer_target','reviewer_cpu','reviewer_declarative','reviewer_native','producer_native','frontier','integration','approved_verdict_sha256']
    stream=io.StringIO(newline='');w=csv.DictWriter(stream,fieldnames=fields,lineterminator='\n');w.writeheader()
    for r in d['archived_private_results']:
        row={k:r[k] for k in fields if k in r};row['integration']='false';row['caller_returned']=str(r['caller_returned']).lower();row['producer_native']=r['producer_accepted']['native']
        for k in ['target','cpu','declarative','native']:row['reviewer_'+k]=r['reviewer_accepted'][k]
        w.writerow(row)
    out[CSV_PATH]=stream.getvalue().encode()
    for p,b in out.items():guard_output(p,b)
    return out
RAW=re.compile(rb'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|raw_opcode|raw_pc|register_values|target_address|payload_offset|data:image|```(?:asm|mips|cpp|c)\b',re.I)
SECRET=re.compile(rb'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|(?:api[_-]?key|password|secret)\s*[:=]\s*[\"\x27][^\"\x27\s]{12,}',re.I)
def guard_added(path,payload):
    p=Path(path)
    if p.is_absolute() or '..' in p.parts or path not in PUBLIC_PATHS:raise ValueError('outside explicit RE894 scope')
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
    for p in PUBLIC_PATHS:
        if p!=DASHBOARD:guard_added(p,(ROOT/p).read_bytes())
    print('RE894 deterministic PUBLIC_METADATA_TESTS_ONLY worktree guards PASS; external review PENDING')
def generate():
    import datetime
    import fcntl
    import os
    import subprocess
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
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--write',action='store_true');args=a.parse_args()
    if args.write:generate()
    else:check()
