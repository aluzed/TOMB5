import csv
import shutil
import sys
from pathlib import Path
import pytest
REPO=Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:sys.path.insert(0,str(REPO))


def test_re494_metadata_only_export_and_re495_handoff(tmp_path):
 from scripts.reverse import re494_ghidra_second_window_rank_46_narrow_export as export
 result=export.build(REPO)
 assert {key:result[key] for key in ('story_id','upstream_handoff','selected_candidate_id','selected_rank','selected_subcluster','bridge_class','next_ticket','next_topic','code_change_readiness')}=={'story_id':'RE-494','upstream_handoff':'RE-493','selected_candidate_id':'8ac39f9a6a85','selected_rank':'46','selected_subcluster':'mapped-caller-callee-bridge-readiness-gate','bridge_class':'mapped-caller-callee-bridge','next_ticket':'RE-495','next_topic':'mapped-caller-callee-bridge-readiness-gate','code_change_readiness':'blocked'}
 paths=export.write(result,tmp_path)
 assert len(paths)==5
 for path in paths:assert not any(token in path.read_text(encoding='utf-8').lower() for token in export.FORBIDDEN_OUTPUT_FRAGMENTS)


@pytest.mark.parametrize('field,value',[('story_id','RE-999'),('topic','wrong'),('upstream_handoff','RE-999'),('closed_candidate_id','wrong'),('selected_rank','999'),('selected_candidate_id','wrong'),('selected_bridge_class','wrong'),('source_symbol_context_count','999'),('safe_context_status','source-backed'),('ready_to_reopen_domain_count','1'),('source_patch_authorized_count','1'),('selected_domain','reopened'),('selected_pivot','reopened'),('next_ticket','RE-999'),('next_topic','wrong'),('metadata_work_readiness','blocked'),('code_change_readiness','ready'),('stop_condition','wrong')])
def test_re494_rejects_every_re493_handoff_drift(tmp_path,field,value):
 from scripts.reverse import re494_ghidra_second_window_rank_46_narrow_export as export
 shutil.copytree(REPO/'docs/reverse',tmp_path/'docs/reverse');path=tmp_path/'docs/reverse/generated/re493-ghidra-second-window-next-candidate-selection-handoff.csv'
 with path.open(encoding='utf-8',newline='') as handle:reader=csv.DictReader(handle);rows=list(reader);fields=reader.fieldnames
 rows[0][field]=value
 with path.open('w',encoding='utf-8',newline='') as handle:writer=csv.DictWriter(handle,fieldnames=fields,lineterminator='\n');writer.writeheader();writer.writerows(rows)
 with pytest.raises(ValueError,match=field):export.build(tmp_path)


@pytest.mark.parametrize('field,value',[('story_id','RE-999'),('topic','wrong'),('upstream_handoff','RE-999'),('selected_candidate_id','wrong'),('selected_rank','999'),('selected_subcluster','wrong'),('source_symbol_context_count','999'),('bridge_class','wrong'),('safe_context_status','source-backed'),('candidate_level_proof_count','1'),('ready_to_reopen_domain_count','1'),('source_patch_authorized_count','1'),('selected_domain','reopened'),('selected_pivot','reopened'),('next_ticket','RE-999'),('next_topic','wrong'),('metadata_work_readiness','blocked'),('code_change_readiness','ready'),('stop_condition','wrong')])
def test_re494_rejects_output_identity_and_safety_drift(tmp_path,field,value):
 from scripts.reverse import re494_ghidra_second_window_rank_46_narrow_export as export
 with pytest.raises(ValueError,match='output safety drift'):export.write(dict(export.build(REPO),**{field:value}),tmp_path)


def test_re494_rejects_forbidden_output_content(tmp_path):
 from scripts.reverse import re494_ghidra_second_window_rank_46_narrow_export as export
 with pytest.raises(ValueError,match='forbidden output fragment'):export.write(dict(export.build(REPO),**{'stop_condition':'contains 0x'}),tmp_path)
