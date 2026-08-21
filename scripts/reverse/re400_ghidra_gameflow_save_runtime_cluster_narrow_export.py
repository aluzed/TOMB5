import csv
from pathlib import Path
BASE='docs/reverse/generated/re400-ghidra-gameflow-save-runtime-cluster-narrow-export'
def build(repo):
 rows=[r for r in csv.DictReader((Path(repo)/'docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-candidates.csv').open()) if r['source_cluster']=='gameflow-save-runtime-cluster']
 if [r['candidate_id'] for r in rows]!=['f7335a494e49','64182b59acd1']:raise ValueError('candidate drift')
 return {'story_id':'RE-400','topic':'ghidra-gameflow-save-runtime-cluster-narrow-export','upstream_handoff':'RE-399','focus_cluster':'gameflow-save-runtime-cluster','candidate_count':'2','selected_subcluster':'gameflow-save-runtime-service','selected_candidate_id':'f7335a494e49','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-401','next_topic':'gameflow-save-runtime-service-readiness-gate','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'narrow export selects first candidate before proof-domain selection'}
def write(b,repo):
 repo=Path(repo);paths={'handoff':repo/(BASE+'-handoff.csv'),'candidates':repo/(BASE+'-candidates.csv'),'md':repo/'docs/reverse/functions/re400-ghidra-gameflow-save-runtime-cluster-narrow-export.md','story':repo/'docs/stories/RE-400-ghidra-gameflow-save-runtime-cluster-narrow-export.md'}
 for key in ('handoff','candidates'):
  p=paths[key];p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
 paths['md'].parent.mkdir(parents=True,exist_ok=True);paths['md'].write_text('# RE-400 gameflow save runtime narrow export\n\nSelected metadata-only candidate; readiness remains blocked.\n')
 paths['story'].parent.mkdir(parents=True,exist_ok=True);paths['story'].write_text('# RE-400 gameflow save runtime narrow export\n\n## Progress tracker\n\n- [x] RE-399 handoff validated.\n- [x] Candidate queue narrowed.\n- [x] RE-401 selected.\n')
 return paths
