import csv
from pathlib import Path


def build(repo):
    repo = Path(repo)
    handoff = list(
        csv.DictReader(
            (repo / 'docs/reverse/generated/re426-ghidra-second-window-next-candidate-selection-handoff.csv').open()
        )
    )[0]
    if handoff['next_ticket'] != 'RE-427':
        raise ValueError('handoff drift')
    if handoff['selected_candidate_id'] != '61b63f61c1fd' or handoff['selected_rank'] != '28':
        raise ValueError('candidate drift')
    if handoff['safe_context_status'] != 'filtered-raw-symbolic-artifact':
        raise ValueError('safety-status drift')
    return {
        'story_id': 'RE-427',
        'topic': 'ghidra-second-window-rank-28-narrow-export',
        'upstream_handoff': 'RE-426',
        'selected_candidate_id': handoff['selected_candidate_id'],
        'selected_rank': handoff['selected_rank'],
        'selected_subcluster': 'audio-death-runtime-bridge-service',
        'source_symbol_context_count': handoff['source_symbol_context_count'],
        'bridge_class': handoff['selected_bridge_class'],
        'safe_context_status': handoff['safe_context_status'],
        'candidate_level_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-428',
        'next_topic': 'audio-death-runtime-bridge-service-readiness-gate',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'narrow export requires readiness gate before proof-domain selection',
    }


def write(result, repo):
    repo = Path(repo)
    outputs = []
    for name in ('contexts', 'summary', 'handoff'):
        path = repo / f'docs/reverse/generated/re427-ghidra-second-window-rank-28-narrow-export-{name}.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=result.keys(), lineterminator='\n')
            writer.writeheader()
            writer.writerow(result)
        outputs.append(path)
    documents = {
        'docs/reverse/functions/re427-ghidra-second-window-rank-28-narrow-export.md': (
            '# RE-427 rank-28 narrow export\n\n'
            'Audio/death runtime bridge selected from filtered symbolic context.\n'
        ),
        'docs/stories/RE-427-ghidra-second-window-rank-28-narrow-export.md': (
            '# RE-427 rank-28 narrow export\n\n'
            '## Progress tracker\n\n'
            '- [x] RE-426 handoff validated.\n'
            '- [x] Rank-28 context narrowed.\n'
            '- [x] Filtered symbolic context retained safely.\n'
            '- [x] RE-428 selected.\n'
        ),
    }
    for relative, text in documents.items():
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        outputs.append(path)
    return outputs
