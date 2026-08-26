import csv, sys
from pathlib import Path
import pytest
REPO=Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path: sys.path.insert(0,str(REPO))
def test_re608_metadata_only(tmp_path):
 from scripts.reverse import re608_ghidra_second_window_rank_84_narrow_export as m
 row=m.build(REPO); assert (row['story_id'],row['selected_rank'],row['selected_candidate_id'],row['bridge_class'],row['next_ticket'],row['code_change_readiness'])==('RE-608','84','8f58d6e07fc8','mapped-callee-bridge','RE-609','blocked'); assert len(m.write(row,tmp_path))==5
@pytest.mark.parametrize('field',('story_id','topic','upstream_handoff','closed_candidate_id','selected_rank','selected_candidate_id','selected_bridge_class','source_symbol_context_count','safe_context_status','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition'))
def test_re608_rejects_upstream_drift(tmp_path,field):
 from scripts.reverse import re608_ghidra_second_window_rank_84_narrow_export as m
 with (REPO/m.UPSTREAM).open(encoding='utf-8',newline='') as h: r=csv.DictReader(h); rows,fields=list(r),tuple(r.fieldnames or ())
 rows[0][field]='drift'; target=tmp_path/m.UPSTREAM; target.parent.mkdir(parents=True)
 with target.open('w',encoding='utf-8',newline='') as h: w=csv.DictWriter(h,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
 with pytest.raises(ValueError,match=rf'handoff drift: {field}'):m.build(tmp_path)
def test_re608_rejects_schema_and_row_count(tmp_path):
 from scripts.reverse import re608_ghidra_second_window_rank_84_narrow_export as m
 target=tmp_path/m.UPSTREAM;target.parent.mkdir(parents=True);target.write_text('bad\nx\n',encoding='utf-8')
 with pytest.raises(ValueError,match='handoff schema drift'):m.build(tmp_path)
 valid=(REPO/m.UPSTREAM).read_text(encoding='utf-8');target.write_text(valid+valid.splitlines()[1]+'\n',encoding='utf-8')
 with pytest.raises(ValueError,match='handoff row-count drift'):m.build(tmp_path)
