import csv
import sys
from pathlib import Path
import pytest
REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path: sys.path.insert(0, str(REPO))

def test_re684_gate_is_metadata_only(tmp_path):
 from scripts.reverse import re684_mapped_caller_bridge_readiness_gate as module
 row=module.build(REPO)
 assert (row['story_id'],row['selected_rank'],row['selected_candidate_id'],row['bridge_class'],row['next_ticket'],row['code_change_readiness'])==('RE-684','109','08963c88efc1','mapped-caller-bridge','RE-685','blocked')
 assert len(module.write(row,tmp_path))==5

def test_re684_rejects_every_upstream_field_drift(tmp_path):
 from scripts.reverse import re684_mapped_caller_bridge_readiness_gate as module
 with (REPO/module.UPSTREAM).open(encoding='utf-8',newline='') as f:
  reader=csv.DictReader(f); original,fields=next(reader),tuple(reader.fieldnames or ())
 assert set(module.EXPECTED)==set(fields)
 for field in module.EXPECTED:
  row=dict(original);row[field]='drift';target=tmp_path/module.UPSTREAM;target.parent.mkdir(parents=True,exist_ok=True)
  with target.open('w',encoding='utf-8',newline='') as f:
   writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');writer.writeheader();writer.writerow(row)
  with pytest.raises(ValueError,match=rf'handoff drift: {field}'): module.build(tmp_path)
