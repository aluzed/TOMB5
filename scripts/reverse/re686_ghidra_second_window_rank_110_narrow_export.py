"""Fail-closed metadata-only RE-686 rank-110 narrow export."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse import re685_ghidra_second_window_next_candidate_selection as selection
from scripts.reverse import re683_ghidra_second_window_rank_109_narrow_export as shape

BAD, FIELDS, UPFIELDS = selection.BAD, shape.FIELDS, selection.FIELDS
UPSTREAM = 'docs/reverse/generated/re685-ghidra-second-window-next-candidate-selection-handoff.csv'
PREFIX = 're686-ghidra-second-window-rank-110-narrow-export'
EXPECTED = {
    'story_id': 'RE-685', 'topic': 'ghidra-second-window-next-candidate-selection',
    'upstream_handoff': 'RE-684', 'closed_candidate_id': '08963c88efc1',
    'selected_rank': '110', 'selected_candidate_id': '47dbffdb0518',
    'selected_bridge_class': 'mapped-callee-bridge', 'source_symbol_context_count': '2',
    'safe_context_status': 'filtered-metadata-only', 'ready_to_reopen_domain_count': '0',
    'source_patch_authorized_count': '0', 'selected_domain': 'none', 'selected_pivot': 'none',
    'next_ticket': 'RE-686', 'next_topic': 'ghidra-second-window-rank-110-narrow-export',
    'metadata_work_readiness': 'ready', 'code_change_readiness': 'blocked',
    'stop_condition': 'next ranked metadata candidate selected; production changes remain blocked',
}
OUTPUT = {
    'story_id': 'RE-686', 'topic': 'ghidra-second-window-rank-110-narrow-export',
    'upstream_handoff': 'RE-685', 'selected_candidate_id': '47dbffdb0518', 'selected_rank': '110',
    'selected_subcluster': 'mapped-callee-bridge-readiness-gate',
    'source_symbol_context_count': '2', 'bridge_class': 'mapped-callee-bridge',
    'safe_context_status': 'filtered-metadata-only', 'candidate_level_proof_count': '0',
    'ready_to_reopen_domain_count': '0', 'source_patch_authorized_count': '0',
    'selected_domain': 'none', 'selected_pivot': 'none', 'next_ticket': 'RE-687',
    'next_topic': 'mapped-callee-bridge-readiness-gate',
    'metadata_work_readiness': 'ready', 'code_change_readiness': 'blocked',
    'stop_condition': 'narrow rank-110 export requires readiness gate before proof-domain selection',
}


def build(repo):
    with (Path(repo) / UPSTREAM).open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != UPFIELDS:
            raise ValueError('handoff schema drift')
        rows = list(reader)
    if any(None in row for row in rows):
        raise ValueError('handoff row schema drift')
    if len(rows) != 1:
        raise ValueError('handoff row-count drift')
    for field, value in EXPECTED.items():
        if rows[0].get(field) != value:
            raise ValueError(f'handoff drift: {field}')
    row = dict(OUTPUT)
    validate(row)
    return row


def validate(row):
    if tuple(row) != FIELDS:
        raise ValueError('output schema drift')
    if row != OUTPUT:
        raise ValueError('output drift')
    if any(fragment in '\n'.join(map(str, row.values())).lower() for fragment in BAD):
        raise ValueError('forbidden output fragment')
    safety = tuple(row[key] for key in ('safe_context_status', 'candidate_level_proof_count', 'ready_to_reopen_domain_count', 'source_patch_authorized_count', 'selected_domain', 'selected_pivot', 'metadata_work_readiness', 'code_change_readiness'))
    if safety != ('filtered-metadata-only', '0', '0', '0', 'none', 'none', 'ready', 'blocked'):
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
        repo / 'docs/reverse/functions/re686-ghidra-second-window-rank-110-narrow-export.md': '# RE-686 rank-110 narrow export\n\nThe selected candidate is filtered metadata only; production and code work remain blocked.\n',
        repo / 'docs/stories/RE-686-ghidra-second-window-rank-110-narrow-export.md': '# RE-686 rank-110 narrow export\n\n## Progress tracker\n\n- [x] RE-685 handoff validated.\n- [x] Rank-110 context narrowed.\n- [x] Filtered metadata-only safety retained.\n- [x] Production and code work remain blocked.\n- [x] RE-687 selected; not executed.\n',
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
