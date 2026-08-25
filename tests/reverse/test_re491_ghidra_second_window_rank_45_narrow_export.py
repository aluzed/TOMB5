import csv
import shutil
import sys
from pathlib import Path
import pytest
REPO=Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:sys.path.insert(0,str(REPO))

def test_re491_metadata_only_export_and_re492_handoff(tmp_path):
 from scripts.reverse import re491_ghidra_second_window_rank_45_narrow_export as export
 result=export.build(REPO)
 assert {key:result[key] for key in ('story_id','upstream_handoff','selected_candidate_id','selected_rank','selected_subcluster','bridge_class','next_ticket','next_topic','code_change_readiness')}=={'story_id':'RE-491','upstream_handoff':'RE-490','selected_candidate_id':'3eb366db63dd','selected_rank':'45','selected_subcluster':'mapped-caller-bridge-readiness-gate','bridge_class':'mapped-caller-bridge','next_ticket':'RE-492','next_topic':'mapped-caller-bridge-readiness-gate','code_change_readiness':'blocked'}
 for path in export.write(result,tmp_path):assert not any(token in path.read_text(encoding='utf-8').lower() for token in export.FORBIDDEN_OUTPUT_FRAGMENTS)

@pytest.mark.parametrize('field,value',[('story_id','RE-999'),('topic','wrong'),('upstream_handoff','RE-999'),('closed_candidate_id','wrong'),('selected_rank','999'),('selected_candidate_id','wrong'),('selected_bridge_class','wrong'),('source_symbol_context_count','999'),('safe_context_status','source-backed'),('ready_to_reopen_domain_count','1'),('source_patch_authorized_count','1'),('selected_domain','reopened'),('selected_pivot','reopened'),('next_ticket','RE-999'),('next_topic','wrong'),('metadata_work_readiness','blocked'),('code_change_readiness','ready'),('stop_condition','wrong')])
def test_re491_rejects_every_re490_handoff_drift(tmp_path,field,value):
 from scripts.reverse import re491_ghidra_second_window_rank_45_narrow_export as export
 shutil.copytree(REPO/'docs/reverse',tmp_path/'docs/reverse');path=tmp_path/'docs/reverse/generated/re490-ghidra-second-window-next-candidate-selection-handoff.csv'
 with path.open(encoding='utf-8',newline='') as handle:reader=csv.DictReader(handle);rows=list(reader);fields=reader.fieldnames
 rows[0][field]=value
 with path.open('w',encoding='utf-8',newline='') as handle:writer=csv.DictWriter(handle,fieldnames=fields,lineterminator='\n');writer.writeheader();writer.writerows(rows)
 with pytest.raises(ValueError,match=field):export.build(tmp_path)

@pytest.mark.parametrize('field,value',[('candidate_level_proof_count','1'),('ready_to_reopen_domain_count','1'),('source_patch_authorized_count','1'),('selected_domain','reopened'),('code_change_readiness','ready')])
def test_re491_rejects_output_safety_drift(tmp_path,field,value):
 from scripts.reverse import re491_ghidra_second_window_rank_45_narrow_export as export
 with pytest.raises(ValueError,match='output safety drift'):export.write(dict(export.build(REPO),**{field:value}),tmp_path)
