import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re408-post-gameflow-save-runtime-next-ghidra-cluster-selection-handoff.csv').open()))[0]
 if r['selected_followup_cluster']!='actor-ai-cluster' or r['next_ticket']!='RE-409':raise ValueError('handoff drift')
 return {'story_id':'RE-409','topic':'ghidra-actor-ai-cluster-narrow-export','upstream_handoff':'RE-408','focus_cluster':'actor-ai-cluster','candidate_count':'1','selected_subcluster':'actor-ai-service','selected_candidate_id':'bcfb623df366','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-410','next_topic':'actor-ai-service-readiness-gate','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'narrow actor AI export selects sole candidate before proof-domain selection'}
def write(b,repo):
 repo=Path(repo);o=[]
 for n in ['candidates','summary','handoff']:
  p=repo/f'docs/reverse/generated/re409-ghidra-actor-ai-cluster-narrow-export-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re409-ghidra-actor-ai-cluster-narrow-export.md','# RE-409 actor AI narrow export\n\nSole candidate selected; readiness remains blocked.\n'),('docs/stories/RE-409-ghidra-actor-ai-cluster-narrow-export.md','# RE-409 actor AI narrow export\n\n## Progress tracker\n\n- [x] RE-408 handoff validated.\n- [x] Actor AI candidate narrowed.\n- [x] RE-410 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
