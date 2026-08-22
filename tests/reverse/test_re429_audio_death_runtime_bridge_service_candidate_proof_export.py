import shutil
from pathlib import Path
import pytest
from scripts.reverse.re429_audio_death_runtime_bridge_service_candidate_proof_export import build, write

def test_re429_exports_blocked_metadata_only_proof_context(tmp_path):
    result=build(Path(__file__).resolve().parents[2])
    assert result['selected_candidate_id']=='61b63f61c1fd'
    assert result['candidate_level_proof_count']=='0'
    assert result['next_ticket']=='RE-430'
    forbidden=('0x','fun_','sub_','word_le_hex','payload_offset','opcode')
    assert all(not any(x in p.read_text(encoding='utf-8').lower() for x in forbidden) for p in write(result,tmp_path))

@pytest.mark.parametrize(('field','value'),(('selected_candidate_id','other'),('candidate_level_proof_count','1'),('ready_to_reopen_domain_count','1'),('source_patch_authorized_count','1'),('code_change_readiness','ready'),('source_symbol_context_count','sub_bad')))
def test_re429_rejects_upstream_drift(tmp_path,field,value):
    repo=Path(__file__).resolve().parents[2]
    source=repo/'docs/reverse/generated/re428-audio-death-runtime-bridge-service-readiness-gate-handoff.csv'
    target=tmp_path/'docs/reverse/generated/re428-audio-death-runtime-bridge-service-readiness-gate-handoff.csv'
    target.parent.mkdir(parents=True);shutil.copy2(source,target)
    header,row=target.read_text(encoding='utf-8').splitlines(); cols=header.split(','); values=row.split(',');values[cols.index(field)]=value
    target.write_text(header+'\n'+','.join(values)+'\n',encoding='utf-8')
    with pytest.raises(ValueError): build(tmp_path)
