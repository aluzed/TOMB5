"""Fail-closed metadata-only RE-623 rank-89 narrow export."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse import re620_ghidra_second_window_rank_88_narrow_export as base

BAD, FIELDS = base.BAD, base.FIELDS
UPSTREAM = 'docs/reverse/generated/re622-ghidra-second-window-next-candidate-selection-handoff.csv'
PREFIX = 're623-ghidra-second-window-rank-89-narrow-export'
UPFIELDS = (
    'story_id', 'topic', 'upstream_handoff', 'closed_candidate_id', 'selected_rank',
    'selected_candidate_id', 'selected_bridge_class', 'source_symbol_context_count',
    'safe_context_status', 'ready_to_reopen_domain_count', 'source_patch_authorized_count',
    'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic',
    'metadata_work_readiness', 'code_change_readiness', 'stop_condition',
)
EXPECTED = {
    'story_id': 'RE-622', 'topic': 'ghidra-second-window-next-candidate-selection',
    'upstream_handoff': 'RE-621', 'closed_candidate_id': '702e56cbdb0b', 'selected_rank': '89',
    'selected_candidate_id': '9b740dde01c4', 'selected_bridge_class': 'mapped-caller-callee-bridge',
    'source_symbol_context_count': '5', 'safe_context_status': 'filtered-metadata-only',
    'ready_to_reopen_domain_count': '0', 'source_patch_authorized_count': '0',
    'selected_domain': 'none', 'selected_pivot': 'none', 'next_ticket': 'RE-623',
    'next_topic': 'ghidra-second-window-rank-89-narrow-export',
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
    row = dict(
        story_id='RE-623', topic='ghidra-second-window-rank-89-narrow-export',
        upstream_handoff='RE-622', selected_candidate_id='9b740dde01c4', selected_rank='89',
        selected_subcluster='mapped-caller-callee-bridge-readiness-gate',
        source_symbol_context_count='5', bridge_class='mapped-caller-callee-bridge',
        safe_context_status='filtered-metadata-only', candidate_level_proof_count='0',
        ready_to_reopen_domain_count='0', source_patch_authorized_count='0',
        selected_domain='none', selected_pivot='none', next_ticket='RE-624',
        next_topic='mapped-caller-callee-bridge-readiness-gate', metadata_work_readiness='ready',
        code_change_readiness='blocked',
        stop_condition='narrow rank-89 export requires readiness gate before proof-domain selection',
    )
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
        repo / 'docs/reverse/functions/re623-ghidra-second-window-rank-89-narrow-export.md': '# RE-623 rank-89 narrow export\n\nThe selected candidate is filtered metadata only; production and code work remain blocked.\n',
        repo / 'docs/stories/RE-623-ghidra-second-window-rank-89-narrow-export.md': '# RE-623 rank-89 narrow export\n\n## Progress tracker\n\n- [x] RE-622 handoff validated.\n- [x] Rank-89 context narrowed.\n- [x] Filtered metadata-only safety retained.\n- [x] Production and code work remain blocked.\n- [x] RE-624 selected; not executed.\n',
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
