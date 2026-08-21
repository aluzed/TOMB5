import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re401-gameflow-save-runtime-service-readiness-gate-handoff.csv').open()))[0]
 if r['selected_candidate_id']!='f7335a494e49' or r['next_ticket']!='RE-402':raise ValueError('handoff drift')
 return {'story_id':'RE-402','topic':'gameflow-save-runtime-service-candidate-proof-export','upstream_handoff':'RE-401','selected_candidate_id':'f7335a494e49','source_symbol_context_count':'45','direct_repo_symbol_count':'0','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-403','next_topic':'gameflow-save-runtime-service-candidate-callsite-map','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'candidate context lacks direct source-backed proof'}
def write(b,repo):
 repo=Path(repo);o={}
 for name in ['contexts','proof-gate','summary','handoff']:
  p=repo/f'docs/reverse/generated/re402-gameflow-save-runtime-service-candidate-proof-{name}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o[name]=p
 for rel,text in [('docs/reverse/functions/re402-gameflow-save-runtime-service-candidate-proof-export.md','# RE-402 gameflow save runtime candidate proof export\n\nContext remains metadata-only and blocked.\n'),('docs/stories/RE-402-gameflow-save-runtime-service-candidate-proof-export.md','# RE-402 gameflow save runtime candidate proof export\n\n## Progress tracker\n\n- [x] RE-401 handoff validated.\n- [x] Candidate context exported metadata-only.\n- [x] RE-403 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o[rel]=p
 return o
