#!/usr/bin/env python3
"""Emit the fail-closed RE-459 mapped-caller readiness decision."""
import csv
from pathlib import Path
UPSTREAM = 'docs/reverse/generated/re458-ghidra-second-window-rank-34-narrow-export-handoff.csv'
PREFIX = 're459-mapped-caller-bridge-readiness-gate'
FORBIDDEN_OUTPUT_FRAGMENTS = ('0x','fun_','sub_','word_le_hex','payload_offset','opcode','machine word','raw dump','raw_evidence','call_address','branch target','call target','ghidra_entry','ghidra_name','source_line_text','code.wad','gamewad.obj','secret','asset','raw binary','address','symbol evidence','copyright')
UPSTREAM_FIELDS = ('story_id','topic','upstream_handoff','selected_candidate_id','selected_rank','selected_subcluster','source_symbol_context_count','bridge_class','safe_context_status','candidate_level_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
FIELDS = ('story_id','topic','upstream_handoff','selected_candidate_id','selected_rank','selected_subcluster','source_symbol_context_count','bridge_class','safe_context_status','source_backed_callsite_count','candidate_level_proof_count','repository_symbol_direct_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
def one_row(path):
    with path.open(encoding='utf-8', newline='') as f:
        reader=csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != UPSTREAM_FIELDS: raise ValueError('handoff schema drift')
        rows=list(reader)
    if len(rows) != 1: raise ValueError('handoff row-count drift')
    return rows[0]
def build(repo):
    h=one_row(Path(repo)/UPSTREAM)
    expected={'story_id':'RE-458','topic':'ghidra-second-window-rank-34-narrow-export','upstream_handoff':'RE-457','selected_candidate_id':'aaf42cb3b10b','selected_rank':'34','selected_subcluster':'mapped-caller-bridge-readiness-gate','source_symbol_context_count':'9','bridge_class':'mapped-caller-bridge','safe_context_status':'filtered-metadata-only','next_ticket':'RE-459','next_topic':'mapped-caller-bridge-readiness-gate','metadata_work_readiness':'ready','code_change_readiness':'blocked'}
    for k,v in expected.items():
        if h.get(k)!=v: raise ValueError(f'handoff drift: {k}')
    if any(h.get(k)!='0' for k in ('candidate_level_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count')): raise ValueError('safety-count drift')
    return {'story_id':'RE-459','topic':'mapped-caller-bridge-readiness-gate','upstream_handoff':'RE-458','selected_candidate_id':h['selected_candidate_id'],'selected_rank':h['selected_rank'],'selected_subcluster':h['selected_subcluster'],'source_symbol_context_count':h['source_symbol_context_count'],'bridge_class':h['bridge_class'],'safe_context_status':h['safe_context_status'],'source_backed_callsite_count':'0','candidate_level_proof_count':'0','repository_symbol_direct_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-460','next_topic':'ghidra-second-window-next-candidate-selection','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'mapped caller bridge candidate has no safe source-backed proof context'}
def validate_output(r):
    if tuple(r)!=FIELDS: raise ValueError('output schema drift')
    if any(x in '\n'.join(str(v).lower() for v in r.values()) for x in FORBIDDEN_OUTPUT_FRAGMENTS): raise ValueError('forbidden output fragment')
    identity={'story_id':'RE-459','topic':'mapped-caller-bridge-readiness-gate','upstream_handoff':'RE-458','selected_candidate_id':'aaf42cb3b10b','selected_rank':'34','next_ticket':'RE-460','next_topic':'ghidra-second-window-next-candidate-selection','metadata_work_readiness':'ready'}
    if any(r.get(k)!=v for k,v in identity.items()): raise ValueError('output identity drift')
    safety={'source_backed_callsite_count':'0','candidate_level_proof_count':'0','repository_symbol_direct_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','code_change_readiness':'blocked'}
    if any(r.get(k)!=v for k,v in safety.items()): raise ValueError('output safety drift')
def write(r,repo):
    validate_output(r); repo=Path(repo); outputs=[]
    for suffix in ('gate','summary','handoff'):
        p=repo/f'docs/reverse/generated/{PREFIX}-{suffix}.csv'; p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('w',newline='',encoding='utf-8') as f: w=csv.DictWriter(f,fieldnames=r.keys(),lineterminator='\n');w.writeheader();w.writerow(r)
        outputs.append(p)
    docs={'docs/reverse/functions/re459-mapped-caller-bridge-readiness-gate.md':'# RE-459 mapped caller bridge readiness gate\n\nNo safe source-backed proof context is available; source and code work remain blocked.\n','docs/stories/RE-459-mapped-caller-bridge-readiness-gate.md':'# RE-459 mapped caller bridge readiness gate\n\n## Progress tracker\n\n- [x] RE-458 handoff validated.\n- [x] Candidate proof-context absence confirmed.\n- [x] Filtered metadata-only safety retained.\n- [x] Source and code work remain blocked.\n- [x] RE-460 selected; not executed.\n'}
    for rel,text in docs.items():
        p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');outputs.append(p)
    for p in outputs:
        if any(x in p.read_text(encoding='utf-8').lower() for x in FORBIDDEN_OUTPUT_FRAGMENTS): raise ValueError('forbidden written fragment')
    return outputs
if __name__=='__main__':
    root=Path(__file__).resolve().parents[2];write(build(root),root)
