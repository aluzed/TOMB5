import importlib.util,json,copy
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
def api():
 p=ROOT/'scripts/reverse/re906_publication.py';assert p.exists(),'RED: RE906 metadata generator absent'
 s=importlib.util.spec_from_file_location('re906',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_contract():
 m=api();d=m.metadata();assert m.validate(d)==d
 assert d['integration'] is False and d['global_scope']==d['procedure_scope']=='FAIL'
 assert d['fresh_target']==d['fresh_native']==0 and d['publication_review']=='PENDING_INDEPENDENT_EXACT_HASH_REVIEW'
 assert d['producer']['target_prefixes']==7 and d['reviewer']['target_prefixes']==6
 assert d['producer']['native_returns']==d['reviewer']['native_returns']==0
 assert d['normal_only'] is True and d['naturalcaller']=='BLOCKED'
@pytest.mark.parametrize('key,value',[('fresh_native',False),('integration',0),('fresh_target',1),('naturalcaller','PASS'),('normal_only',False),('publication_review','PASS'),('global_scope','PASS'),('procedure_scope','PASS'),('producer',{}),('reviewer',{}),('unknown',1)])
def test_schema_mutants(key,value):
 m=api();d=m.metadata();before=repr(d);d[key]=value;assert repr(d)!=before
 with pytest.raises(ValueError):m.validate(d)
def test_fixtures():
 m=api();out=m.render();assert set(out)==set(m.OUTPUT_PATHS)
 for p,b in out.items():assert (m.read_maintained() if p==m.MAINTAINED else (ROOT/p).read_bytes())==b;m.guard_output(p,b)
 assert m.preceding_dashboard(out[m.DASHBOARD])==(ROOT/m.PRIOR_DASHBOARD).read_bytes()
 assert m.preceding_maintained(out[m.MAINTAINED])==(ROOT/m.PRIOR_MAINTAINED).read_bytes()
 m.check()
@pytest.mark.parametrize('which',['dashboard','maintained'])
@pytest.mark.parametrize('change',['history','missing','duplicate','altered','trailing','unknown'])
def test_inverse_mutants(which,change):
 m=api();data=m.render()[m.DASHBOARD if which=='dashboard' else m.MAINTAINED];original=data;s=m.SECTION.encode()
 if change=='history':data=b'foreign'+data
 if change=='missing':data=data.replace(b'<!-- RE906 PUBLICATION END -->',b'')
 if change=='duplicate':data=data[:-7]+s+b'</html>'
 if change=='altered':data=data.replace(s,s.replace(b'ARCHIVED',b'FRESH'))
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
def test_documents():
 m=api();out=m.render()
 for p in (m.STORY,m.REPORT):
  for phrase in ['## Progression','## Evidence','## Blockers','## Acceptance','PENDING_INDEPENDENT_EXACT_HASH_REVIEW','integration=false','RE905','RE906','firstFAIL','BLOCKED-001/002']:
   assert phrase in out[p].decode()
def test_compatibility():api().compatibility_pins()

def test_story_link_and_exact_re904_frontier():
 m=api();assert m.STORY=='docs/stories/RE-906-upstream-prefix-publication.md'
 assert m.PRIOR_DASHBOARD.endswith('re904-v1.html')
 assert m.PRIOR_MAINTAINED.endswith('maintained-re904-v1.html')
 assert m.metadata()['prefix']['animation']==578 and m.metadata()['prefix']['frame']==0

def leaves(d,p=()):
 if isinstance(d,dict):
  for k,v in d.items():yield from leaves(v,p+(k,))
 elif isinstance(d,list):
  for k,v in enumerate(d):yield from leaves(v,p+(k,))
 else:yield p,d

def test_every_nested_leaf_discriminates():
 m=api();d=m.metadata()
 for path,value in leaves(d):
  mutant=copy.deepcopy(d);node=mutant
  for k in path[:-1]:node=node[k]
  changed=not value if type(value) is bool else value+1 if type(value) is int else value+'FOREIGN'
  node[path[-1]]=changed;assert repr(mutant)!=repr(d)
  with pytest.raises(ValueError):m.validate(mutant)
  if type(value) in (int,bool):
   node[path[-1]]=int(value) if type(value) is bool else bool(value)
   assert repr(mutant)!=repr(d)
   with pytest.raises(ValueError):m.validate(mutant)

@pytest.mark.parametrize('path',['scripts/reverse/re904_publication.py','tests/reverse/test_re904_publication.py','tests/reverse/test_re830_table_provenance_publication.py'])
def test_exact_compatibility_inverse_mutants(path):
 m=api();text=(ROOT/path).read_text();m.original_compatibility(path,text)
 for old,new in m.COMPATIBILITY_DELTAS[path]['replacements']:
  assert text.count(new)==1
  for mutant in (text.replace(new,''),text.replace(new,new+new),text+'foreign'):
   assert mutant!=text
   with pytest.raises(ValueError):m.original_compatibility(path,mutant)
