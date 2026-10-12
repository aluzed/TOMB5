import importlib.util,copy,json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
def api():
 p=ROOT/'scripts/reverse/re927_publication.py';assert p.exists(),'RED: RE927 generator absent'
 s=importlib.util.spec_from_file_location('re927',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_contract():
 m=api();d=m.metadata();m.validate(d)
 assert d['backend_boundary']=='RE926-PCSX-Redux-Timer1-local-free-running-subset'
 assert d['publication_review']=='PENDING_INDEPENDENT_REVIEW'
 assert d['integration'] is False and d['production_patch'] is False
 assert d['global_scope']==d['procedure_scope']=='FAIL'
 assert d['fresh_target']==d['fresh_native']==0
 assert d['archived_counts']['completed']==1981087 and d['archived_counts']['visits']==1981088
 assert d['archived_counts']['resume_completed']==318 and d['archived_counts']['resume_visits']==319
 assert d['natural_mode_writes']==1 and d['natural_counter_reads']==0
 assert d['review_history']['stale_ablation']=='REJECTED_NON_CERTIFIED'
 assert d['review_history']['archived_clock']==7912652 and d['review_history']['corrected_fresh_clock']==7921560
 assert d['frontier']=='BEFORE_SYSCALL_OpenBIOS_EnterCriticalSection'
 assert d['authentication']['re926-timer-mmio']['members']==153 and d['authentication']['re926-review']['members']==107
 assert d['authentication']['re926-parent-checkpoint']['members']==4
 assert d['rom_fresh_build'] is False
 assert d['attribution']['sources'][0]['url']=='https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/psxcounters.cc'
 assert 'Copyright (C) 2010 by Blade_Arma' in d['attribution']['sources'][0]['copyright']
 assert m.PRIOR_DASHBOARD=='docs/reverse/tomb5-progress-dashboard-re925-v1.html'
 assert m.PRIOR_MAINTAINED=='docs/reverse/tomb5-progress-dashboard-maintained-re925-v1.html'
def leaves(d,p=()):
 if isinstance(d,dict):
  for k,v in d.items():yield from leaves(v,p+(k,))
 elif isinstance(d,list):
  for k,v in enumerate(d):yield from leaves(v,p+(k,))
 else:yield p,d
def test_recursive_leaf_mutants():
 m=api();d=m.metadata()
 for path,v in leaves(d):
  choices=[not v] if type(v) is bool else [v+1] if type(v) in (int,float) else [v+'FOREIGN']
  if type(v) in (int,bool):choices.append(int(v) if type(v) is bool else bool(v))
  for value in choices:
   mutant=copy.deepcopy(d);n=mutant
   for k in path[:-1]:n=n[k]
   n[path[-1]]=value;assert repr(mutant)!=repr(d)
   with pytest.raises(ValueError):m.validate(mutant)
def test_unknown_fields():
 m=api();d=m.metadata();d['unknown']=1
 with pytest.raises(ValueError):m.validate(d)
def test_generated():
 m=api();out=m.render();assert set(out)==set(m.OUTPUT_PATHS)
 for p,b in out.items():assert (ROOT/p).read_bytes()==b;m.guard_output(p,b)
 assert m.preceding_dashboard(out[m.DASHBOARD])==(ROOT/m.PRIOR_DASHBOARD).read_bytes()
 assert m.preceding_maintained(out[m.MAINTAINED])==(ROOT/m.PRIOR_MAINTAINED).read_bytes()
 m.check()
@pytest.mark.parametrize('which',['dashboard','maintained'])
@pytest.mark.parametrize('change',['history','missing','duplicate','altered','trailing','unknown'])
def test_inverse_mutants(which,change):
 m=api();original=m.render()[m.DASHBOARD if which=='dashboard' else m.MAINTAINED];data=original;s=m.SECTION.encode()
 if change=='history':data=b'foreign'+data
 if change=='missing':data=data.replace(b'<!-- RE927 PUBLICATION END -->',b'')
 if change=='duplicate':data=data[:-7]+s+b'</html>'
 if change=='altered':data=data.replace(s,s.replace(b'BLOCKED',b'PASS'))
 if change=='trailing':data+=b'foreign'
 if change=='unknown':data=data[:-7]+b'<!-- unknown successor -->'+b'</html>'
 assert data!=original
 with pytest.raises(ValueError):(m.preceding_dashboard if which=='dashboard' else m.preceding_maintained)(data)
@pytest.mark.parametrize('bad',[b'0x80012345',b'FUN_80012345',b'word_le_hex',b'raw_opcode',b'payload_offset',b'data:image/png;base64,',b'-----BEGIN '+b'PRIVATE KEY-----',b'ghp_'+b'a'*30,b'```mips\n',b'\0',b'raw_pc=123',b'register_values=[1]',b'target_address=123',b'a'*100001])
def test_content_guard(bad):
 m=api();m.guard_added(m.STORY,b'safe symbolic metadata')
 with pytest.raises(ValueError):m.guard_added(m.STORY,bad)
@pytest.mark.parametrize('p',['SPEC_PSXPC_N/MATHS.C','build/reverse/proof.bin','assets/x.png','../escape.md','/tmp/x'])
def test_path_guard(p):
 with pytest.raises(ValueError):api().guard_added(p,b'safe metadata')
def test_story_and_attribution():
 m=api();assert m.STORY=='docs/stories/RE-927-timer-proof-publication.md'
 assert '../stories/RE-927-timer-proof-publication.md' in m.SECTION
 for p in (m.STORY,m.REPORT):
  for text in ['## Progression','## Evidence','## Blockers','## Acceptance','MIT','GPL-2.0-or-later','PCSX-Redux','firstFAIL','BLOCKED-001/002','integration=false','PENDING_INDEPENDENT_REVIEW']:
   assert text in m.render()[p].decode()
def test_compatibility():api().compatibility_pins()
def test_compatibility_adapter_mutants():
 m=api()
 for p,spec in m.COMPATIBILITY_DELTAS.items():
  text=(ROOT/p).read_text()
  for old,new in spec['replacements']:
   assert text.count(new)==1
   for replacement in ['',new+new,new+'FOREIGN']:
    mutant=text.replace(new,replacement);assert mutant!=text
    with pytest.raises(ValueError):m.original_compatibility(p,mutant)
