import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re410-actor-ai-service-readiness-gate-handoff.csv').open()))[0]
 if r['selected_candidate_id']!='bcfb623df366' or r['next_ticket']!='RE-411':raise ValueError('handoff drift')
 return {'story_id':'RE-411','topic':'actor-ai-service-candidate-proof-export','upstream_handoff':'RE-410','selected_candidate_id':'bcfb623df366','source_symbol_context_count':'25','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-412','next_topic':'actor-ai-service-candidate-callsite-map','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'actor AI candidate context lacks direct proof'}
def write(b,repo):
 repo=Path(repo);o=[]
 for n in ['contexts','proof-gate','summary','handoff']:
  p=repo/f'docs/reverse/generated/re411-actor-ai-service-candidate-proof-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re411-actor-ai-service-candidate-proof-export.md','# RE-411 actor AI proof export\n\nMetadata-only context remains blocked.\n'),('docs/stories/RE-411-actor-ai-service-candidate-proof-export.md','# RE-411 actor AI proof export\n\n## Progress tracker\n\n- [x] RE-410 handoff validated.\n- [x] Context exported.\n- [x] RE-412 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
