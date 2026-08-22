import csv
from pathlib import Path


UPSTREAM = 'docs/reverse/generated/re433-ghidra-second-window-rank-29-narrow-export-handoff.csv'
PREFIX = 're434-runtime-bridge-service-readiness-gate'


def build(repo):
    repo = Path(repo)
    with (repo / UPSTREAM).open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise ValueError('handoff row-count drift')
    handoff = rows[0]
    if handoff['next_ticket'] != 'RE-434' or handoff['next_topic'] != 'runtime-bridge-service-readiness-gate':
        raise ValueError('handoff drift')
    if handoff['metadata_work_readiness'] != 'ready':
        raise ValueError('metadata-readiness drift')
    if handoff['selected_candidate_id'] != '763c9cd0e3f7':
        raise ValueError('candidate drift')
    if handoff['selected_rank'] != '29':
        raise ValueError('rank drift')
    if handoff['selected_subcluster'] != 'runtime-bridge-service':
        raise ValueError('subcluster drift')
    safety_fields = (
        'candidate_level_proof_count',
        'ready_to_reopen_domain_count',
        'source_patch_authorized_count',
    )
    if any(handoff[field] != '0' for field in safety_fields):
        raise ValueError('safety-count drift')
    if handoff['selected_domain'] != 'none' or handoff['selected_pivot'] != 'none':
        raise ValueError('unsafe selection drift')
    if handoff['code_change_readiness'] != 'blocked':
        raise ValueError('code-readiness drift')
    return {
        'story_id': 'RE-434',
        'topic': 'runtime-bridge-service-readiness-gate',
        'upstream_handoff': 'RE-433',
        'selected_candidate_id': handoff['selected_candidate_id'],
        'selected_rank': handoff['selected_rank'],
        'selected_subcluster': handoff['selected_subcluster'],
        'source_symbol_context_count': handoff['source_symbol_context_count'],
        'candidate_level_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-435',
        'next_topic': 'runtime-bridge-service-candidate-proof-export',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'runtime bridge context remains prioritization signal without candidate proof',
    }


def write(result, repo):
    repo = Path(repo)
    outputs = []
    for name in ('gate', 'summary', 'handoff'):
        path = repo / f'docs/reverse/generated/{PREFIX}-{name}.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=result.keys(), lineterminator='\n')
            writer.writeheader()
            writer.writerow(result)
        outputs.append(path)
    documents = {
        'docs/reverse/functions/re434-runtime-bridge-service-readiness-gate.md': (
            '# RE-434 runtime bridge service readiness gate\n\n'
            'Candidate proof is absent; source changes remain blocked.\n'
        ),
        'docs/stories/RE-434-runtime-bridge-service-readiness-gate.md': (
            '# RE-434 runtime bridge service readiness gate\n\n'
            '## Progress tracker\n\n'
            '- [x] RE-433 handoff validated.\n'
            '- [x] Candidate-proof absence confirmed.\n'
            '- [x] Source changes blocked.\n'
            '- [x] RE-435 selected.\n'
        ),
    }
    for relative, text in documents.items():
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        outputs.append(path)
    return outputs
