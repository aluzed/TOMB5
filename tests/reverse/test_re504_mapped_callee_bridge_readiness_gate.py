import csv
import shutil
import sys
from pathlib import Path
import pytest
REPO=Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:sys.path.insert(0,str(REPO))
from scripts.reverse import re504_mapped_callee_bridge_readiness_gate as m

def test_re504_metadata_only_gate(tmp_path):
 r=m.build(REPO)
 assert (r['story_id'],r['selected_candidate_id'],r['selected_rank'],r['bridge_class'],r['next_ticket'],r['code_change_readiness'])==('RE-504','a6117c5f5023','49','mapped-callee-bridge','RE-505','blocked')
 outputs=m.write(r,tmp_path)
 assert len(outputs)==5
 for output in outputs:
  assert not any(fragment in output.read_text(encoding='utf-8').lower() for fragment in m.BAD)

def test_re504_rejects_upstream_and_output_drift(tmp_path):
 upstream=tmp_path/'docs/reverse/generated/re503-ghidra-second-window-rank-49-narrow-export-handoff.csv'
 upstream.parent.mkdir(parents=True)
 shutil.copy2(REPO/'docs/reverse/generated/re503-ghidra-second-window-rank-49-narrow-export-handoff.csv',upstream)
 with upstream.open(encoding='utf-8',newline='') as handle:
  row=next(csv.DictReader(handle));fields=tuple(row)
 row['source_patch_authorized_count']='1'
 with upstream.open('w',encoding='utf-8',newline='') as handle:
  writer=csv.DictWriter(handle,fieldnames=fields,lineterminator='\n');writer.writeheader();writer.writerow(row)
 with pytest.raises(ValueError,match='handoff drift: source_patch_authorized_count'):
  m.build(tmp_path)
 result=m.build(REPO)
 with pytest.raises(ValueError,match='forbidden output fragment'):
  m.write(dict(result,stop_condition='unsafe 0x value'),tmp_path)
 with pytest.raises(ValueError,match='output safety drift: code_change_readiness'):
  m.write(dict(result,code_change_readiness='ready'),tmp_path)
 with pytest.raises(ValueError,match='output schema drift'):
  m.write(dict(result,call_address='metadata-only'),tmp_path)
