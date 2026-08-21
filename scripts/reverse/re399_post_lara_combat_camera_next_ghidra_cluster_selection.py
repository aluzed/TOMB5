import csv
from pathlib import Path
OUT='docs/reverse/generated/re399-post-lara-combat-camera-next-ghidra-cluster-selection-handoff.csv'
def build(repo):
 repo=Path(repo);h=list(csv.DictReader((repo/'docs/reverse/generated/re398-combat-camera-service-callsite-readiness-gate-handoff.csv').open()))[0]
 if h['next_ticket']!='TBD' or h['code_change_readiness']!='blocked':raise ValueError('RE-398 drift')
 rows=list(csv.DictReader((repo/'docs/reverse/generated/re391-post-maths-render-next-ghidra-cluster-selection-clusters.csv').open()))
 expected=['lara-combat-camera-cluster','gameflow-save-runtime-cluster','actor-ai-cluster']
 if [x['cluster'] for x in rows]!=expected:raise ValueError('parent queue drift')
 return {'story_id':'RE-399','topic':'post-lara-combat-camera-next-ghidra-cluster-selection','upstream_handoff':'RE-398','closed_clusters':'lara-combat-camera-cluster','selected_followup_cluster':'gameflow-save-runtime-cluster','selected_candidate_ids':'','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-400','next_topic':'ghidra-gameflow-save-runtime-cluster-narrow-export','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'lara/combat/camera cluster exhausted; select next deferred Ghidra bridge cluster'}
def write(b,repo):
 repo=Path(repo);p=repo/OUT;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
 for rel,text in [('docs/reverse/functions/re399-post-lara-combat-camera-next-ghidra-cluster-selection.md','# RE-399 post lara combat camera next Ghidra cluster selection\n\nSelected gameflow/save runtime while readiness remains blocked.\n'),('docs/stories/RE-399-post-lara-combat-camera-next-ghidra-cluster-selection.md','# RE-399 post lara combat camera next Ghidra cluster selection\n\n## Progress tracker\n\n- [x] RE-398 terminal handoff validated.\n- [x] Parent queue re-opened.\n- [x] gameflow/save runtime selected.\n')]:
  q=repo/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(text)
 return {'handoff':p}
