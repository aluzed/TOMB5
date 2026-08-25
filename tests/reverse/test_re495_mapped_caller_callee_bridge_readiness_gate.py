import csv,shutil,sys
from pathlib import Path
import pytest
REPO=Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:sys.path.insert(0,str(REPO))
def test_re495_metadata_only_gate(tmp_path):
 from scripts.reverse import re495_mapped_caller_callee_bridge_readiness_gate as m
 r=m.build(REPO)
 assert (r['story_id'],r['selected_candidate_id'],r['selected_rank'],r['bridge_class'],r['next_ticket'],r['code_change_readiness'])==('RE-495','8ac39f9a6a85','46','mapped-caller-callee-bridge','RE-496','blocked')
 assert len(m.write(r,tmp_path))==5
@pytest.mark.parametrize('field,value',[('story_id','RE-999'),('topic','wrong'),('upstream_handoff','RE-999'),('selected_candidate_id','wrong'),('selected_rank','999'),('selected_subcluster','wrong'),('source_symbol_context_count','999'),('bridge_class','wrong'),('safe_context_status','source-backed'),('candidate_level_proof_count','1'),('ready_to_reopen_domain_count','1'),('source_patch_authorized_count','1'),('selected_domain','reopened'),('selected_pivot','reopened'),('next_ticket','RE-999'),('next_topic','wrong'),('metadata_work_readiness','blocked'),('code_change_readiness','ready'),('stop_condition','wrong')])
def test_re495_rejects_upstream_drift(tmp_path,field,value):
 from scripts.reverse import re495_mapped_caller_callee_bridge_readiness_gate as m
 shutil.copytree(REPO/'docs/reverse',tmp_path/'docs/reverse');p=tmp_path/'docs/reverse/generated/re494-ghidra-second-window-rank-46-narrow-export-handoff.csv'
 with p.open(encoding='utf-8',newline='') as h:r=csv.DictReader(h);rows=list(r);fields=r.fieldnames
 rows[0][field]=value
 with p.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
 with pytest.raises(ValueError,match=field):m.build(tmp_path)
