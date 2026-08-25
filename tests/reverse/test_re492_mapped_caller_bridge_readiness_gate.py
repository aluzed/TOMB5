import csv,shutil,sys
from pathlib import Path
import pytest
REPO=Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:sys.path.insert(0,str(REPO))
def test_re492_gate_is_metadata_only_and_emits_re493(tmp_path):
 from scripts.reverse import re492_mapped_caller_bridge_readiness_gate as gate
 r=gate.build(REPO)
 assert (r['story_id'],r['upstream_handoff'],r['selected_candidate_id'],r['selected_rank'],r['next_ticket'],r['next_topic'],r['code_change_readiness'])==('RE-492','RE-491','3eb366db63dd','45','RE-493','ghidra-second-window-next-candidate-selection','blocked')
 for p in gate.write(r,tmp_path):assert not any(x in p.read_text(encoding='utf-8').lower() for x in gate.FORBIDDEN_OUTPUT_FRAGMENTS)
@pytest.mark.parametrize('field,value',[('story_id','RE-999'),('topic','wrong'),('selected_candidate_id','wrong'),('selected_rank','999'),('safe_context_status','source-backed'),('candidate_level_proof_count','1'),('ready_to_reopen_domain_count','1'),('source_patch_authorized_count','1'),('selected_domain','reopened'),('next_ticket','RE-999'),('code_change_readiness','ready')])
def test_re492_rejects_re491_handoff_drift(tmp_path,field,value):
 from scripts.reverse import re492_mapped_caller_bridge_readiness_gate as gate
 shutil.copytree(REPO/'docs/reverse',tmp_path/'docs/reverse');p=tmp_path/'docs/reverse/generated/re491-ghidra-second-window-rank-45-narrow-export-handoff.csv'
 with p.open(encoding='utf-8',newline='') as h:reader=csv.DictReader(h);rows=list(reader);fields=reader.fieldnames
 rows[0][field]=value
 with p.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
 with pytest.raises(ValueError,match=field):gate.build(tmp_path)
