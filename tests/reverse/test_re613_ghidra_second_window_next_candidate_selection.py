import csv, sys
from pathlib import Path
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path: sys.path.insert(0, str(REPO))

def test_re613_metadata_only(tmp_path):
 from scripts.reverse import re613_ghidra_second_window_next_candidate_selection as m
 row=m.build(REPO)
 assert (row['story_id'],row['closed_candidate_id'],row['selected_rank'],row['selected_candidate_id'],row['selected_bridge_class'],row['next_ticket'],row['code_change_readiness'])==('RE-613','259084955c25','86','4fc5988c65ba','mapped-caller-callee-bridge','RE-614','blocked')
 assert len(m.write(row,tmp_path))==5

@pytest.mark.parametrize('field',('story_id','topic','upstream_handoff','selected_candidate_id','selected_rank','selected_subcluster','source_symbol_context_count','bridge_class','safe_context_status','source_backed_callsite_count','candidate_level_proof_count','repository_symbol_direct_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition'))
def test_re613_rejects_upstream_drift(tmp_path,field):
 from scripts.reverse import re613_ghidra_second_window_next_candidate_selection as m
 with (REPO/m.UPSTREAM).open(encoding='utf-8',newline='') as h:
  r=csv.DictReader(h); rows,fields=list(r),tuple(r.fieldnames or ())
 rows[0][field]='drift'; p=tmp_path/m.UPSTREAM; p.parent.mkdir(parents=True)
 with p.open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=fields,lineterminator='\n'); w.writeheader(); w.writerows(rows)
 with pytest.raises(ValueError,match=rf'handoff drift: {field}'):m.build(tmp_path)

def test_re613_rejects_schema_and_row_count(tmp_path):
 from scripts.reverse import re613_ghidra_second_window_next_candidate_selection as m
 p=tmp_path/m.UPSTREAM; p.parent.mkdir(parents=True); p.write_text('bad\nx\n',encoding='utf-8')
 with pytest.raises(ValueError,match='handoff schema drift'):m.build(tmp_path)
 valid=(REPO/m.UPSTREAM).read_text(encoding='utf-8');p.write_text(valid+valid.splitlines()[1]+'\n',encoding='utf-8')
 with pytest.raises(ValueError,match='handoff row-count drift'):m.build(tmp_path)
