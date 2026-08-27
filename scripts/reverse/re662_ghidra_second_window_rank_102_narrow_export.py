"""Fail-closed metadata-only RE-662 rank-102 narrow export."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse import re659_ghidra_second_window_rank_101_narrow_export as base

BAD, FIELDS, UPFIELDS = base.BAD, base.FIELDS, base.UPFIELDS
UPSTREAM = 'docs/reverse/generated/re661-ghidra-second-window-next-candidate-selection-handoff.csv'
PREFIX = 're662-ghidra-second-window-rank-102-narrow-export'
EXPECTED = {
    'story_id': 'RE-661', 'topic': 'ghidra-second-window-next-candidate-selection',
    'upstream_handoff': 'RE-660', 'closed_candidate_id': '6b59cdbcb8e4', 'selected_rank': '102',
    'selected_candidate_id': '3de39d58a7ec', 'selected_bridge_class': 'mapped-callee-bridge',
    'source_symbol_context_count': '4', 'safe_context_status': 'filtered-metadata-only',
    'ready_to_reopen_domain_count': '0', 'source_patch_authorized_count': '0',
    'selected_domain': 'none', 'selected_pivot': 'none', 'next_ticket': 'RE-662',
    'next_topic': 'ghidra-second-window-rank-102-narrow-export',
    'metadata_work_readiness': 'ready', 'code_change_readiness': 'blocked',
    'stop_condition': 'next ranked metadata candidate selected; production changes remain blocked',
}


def build(repo):
    with (Path(repo) / UPSTREAM).open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != UPFIELDS:
            raise ValueError('handoff schema drift')
        rows = list(reader)
    if len(rows) != 1:
        raise ValueError('handoff row-count drift')
    for field, value in EXPECTED.items():
        if rows[0].get(field) != value:
            raise ValueError(f'handoff drift: {field}')
    row = dict(story_id='RE-662', topic='ghidra-second-window-rank-102-narrow-export', upstream_handoff='RE-661', selected_candidate_id='3de39d58a7ec', selected_rank='102', selected_subcluster='mapped-callee-bridge-readiness-gate', source_symbol_context_count='4', bridge_class='mapped-callee-bridge', safe_context_status='filtered-metadata-only', candidate_level_proof_count='0', ready_to_reopen_domain_count='0', source_patch_authorized_count='0', selected_domain='none', selected_pivot='none', next_ticket='RE-663', next_topic='mapped-callee-bridge-readiness-gate', metadata_work_readiness='ready', code_change_readiness='blocked', stop_condition='narrow rank-102 export requires readiness gate before proof-domain selection')
    validate(row)
    return row


def validate(row):
    if tuple(row) != FIELDS:
        raise ValueError('output schema drift')
    if any(fragment in '\n'.join(map(str, row.values())).lower() for fragment in BAD):
        raise ValueError('forbidden output fragment')
    if (row['code_change_readiness'], row['source_patch_authorized_count'], row['safe_context_status']) != ('blocked', '0', 'filtered-metadata-only'):
        raise ValueError('output safety drift')


def write(row, repo):
    validate(row)
    repo, outputs = Path(repo), []
    for suffix in ('contexts', 'summary', 'handoff'):
        path = repo / 'docs/reverse/generated' / f'{PREFIX}-{suffix}.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator='\n')
            writer.writeheader()
            writer.writerow(row)
        outputs.append(path)
    documents = {
        repo / 'docs/reverse/functions/re662-ghidra-second-window-rank-102-narrow-export.md': '# RE-662 rank-102 narrow export\n\nThe selected candidate is filtered metadata only; production and code work remain blocked.\n',
        repo / 'docs/stories/RE-662-ghidra-second-window-rank-102-narrow-export.md': '# RE-662 rank-102 narrow export\n\n## Progress tracker\n\n- [x] RE-661 handoff validated.\n- [x] Rank-102 context narrowed.\n- [x] Filtered metadata-only safety retained.\n- [x] Production and code work remain blocked.\n- [x] RE-663 selected; not executed.\n',
    }
    for path, text in documents.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        outputs.append(path)
    for path in outputs:
        if any(fragment in path.read_text(encoding='utf-8').lower() for fragment in BAD):
            raise ValueError('forbidden written fragment')
    return outputs


if __name__ == '__main__':
    write(build(ROOT), ROOT)
