import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re407-gameflow-save-runtime-service-next-candidate-callsite-readiness-gate-handoff.csv').open()))[0]
 if r['next_ticket']!='RE-408':raise ValueError('handoff drift')
 return {'story_id':'RE-408','topic':'post-gameflow-save-runtime-next-ghidra-cluster-selection','upstream_handoff':'RE-407','closed_clusters':'lara-combat-camera-cluster;gameflow-save-runtime-cluster','selected_followup_cluster':'actor-ai-cluster','selected_candidate_id':'','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-409','next_topic':'ghidra-actor-ai-cluster-narrow-export','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'gameflow runtime exhausted; select remaining deferred cluster'}
def write(b,repo):
 repo=Path(repo);o=[]
 for n in ['clusters','summary','handoff']:
  p=repo/f'docs/reverse/generated/re408-post-gameflow-save-runtime-next-ghidra-cluster-selection-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re408-post-gameflow-save-runtime-next-ghidra-cluster-selection.md','# RE-408 next Ghidra cluster selection\n\nActor AI selected; readiness blocked.\n'),('docs/stories/RE-408-post-gameflow-save-runtime-next-ghidra-cluster-selection.md','# RE-408 next Ghidra cluster selection\n\n## Progress tracker\n\n- [x] RE-407 handoff validated.\n- [x] Actor AI selected.\n- [x] RE-409 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
