import csv
from pathlib import Path


def build(repo):
    repo = Path(repo)
    handoff = list(
        csv.DictReader(
            (repo / 'docs/reverse/generated/re427-ghidra-second-window-rank-28-narrow-export-handoff.csv').open(encoding='utf-8')
        )
    )[0]
    if handoff['next_ticket'] != 'RE-428':
        raise ValueError('handoff drift')
    if handoff['selected_candidate_id'] != '61b63f61c1fd':
        raise ValueError('candidate drift')
    if handoff['selected_subcluster'] != 'audio-death-runtime-bridge-service':
        raise ValueError('subcluster drift')
    if handoff['candidate_level_proof_count'] != '0':
        raise ValueError('candidate-proof drift')
    if handoff['safe_context_status'] != 'filtered-raw-symbolic-artifact':
        raise ValueError('safety-status drift')
    if any(
        (
            handoff['ready_to_reopen_domain_count'] != '0',
            handoff['source_patch_authorized_count'] != '0',
            handoff['code_change_readiness'] != 'blocked',
        )
    ):
        raise ValueError('safety-gate drift')
    return {
        'story_id': 'RE-428',
        'topic': 'audio-death-runtime-bridge-service-readiness-gate',
        'upstream_handoff': 'RE-427',
        'selected_candidate_id': handoff['selected_candidate_id'],
        'selected_subcluster': handoff['selected_subcluster'],
        'source_symbol_context_count': handoff['source_symbol_context_count'],
        'candidate_level_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-429',
        'next_topic': 'audio-death-runtime-bridge-service-candidate-proof-export',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'audio/death bridge context remains prioritization signal without candidate proof',
    }


def write(result, repo):
    repo = Path(repo)
    outputs = []
    for name in ('gate', 'summary', 'handoff'):
        path = repo / f'docs/reverse/generated/re428-audio-death-runtime-bridge-service-readiness-gate-{name}.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=result.keys(), lineterminator='\n')
            writer.writeheader()
            writer.writerow(result)
        outputs.append(path)
    documents = {
        'docs/reverse/functions/re428-audio-death-runtime-bridge-service-readiness-gate.md': (
            '# RE-428 audio/death runtime bridge readiness gate\n\n'
            'Candidate proof absent; source changes blocked.\n'
        ),
        'docs/stories/RE-428-audio-death-runtime-bridge-service-readiness-gate.md': (
            '# RE-428 audio/death runtime bridge readiness gate\n\n'
            '## Progress tracker\n\n'
            '- [x] RE-427 handoff validated.\n'
            '- [x] Candidate proof absence confirmed.\n'
            '- [x] Source changes blocked.\n'
            '- [x] RE-429 selected.\n'
        ),
    }
    for relative, text in documents.items():
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        outputs.append(path)
    return outputs
