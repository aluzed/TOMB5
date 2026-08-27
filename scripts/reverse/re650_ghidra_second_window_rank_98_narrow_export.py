"""Fail-closed metadata-only RE-650 rank-98 narrow export."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse import re647_ghidra_second_window_rank_97_narrow_export as base

BAD, FIELDS, UPFIELDS = base.BAD, base.FIELDS, base.UPFIELDS
UPSTREAM = 'docs/reverse/generated/re649-ghidra-second-window-next-candidate-selection-handoff.csv'
PREFIX = 're650-ghidra-second-window-rank-98-narrow-export'
EXPECTED = {
    'story_id': 'RE-649', 'topic': 'ghidra-second-window-next-candidate-selection',
    'upstream_handoff': 'RE-648', 'closed_candidate_id': '9453fad2974f', 'selected_rank': '98',
    'selected_candidate_id': '0f32795d8e8f', 'selected_bridge_class': 'mapped-caller-callee-bridge',
    'source_symbol_context_count': '4', 'safe_context_status': 'filtered-metadata-only',
    'ready_to_reopen_domain_count': '0', 'source_patch_authorized_count': '0',
    'selected_domain': 'none', 'selected_pivot': 'none', 'next_ticket': 'RE-650',
    'next_topic': 'ghidra-second-window-rank-98-narrow-export',
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
        story_id='RE-650', topic='ghidra-second-window-rank-98-narrow-export',
        upstream_handoff='RE-649', selected_candidate_id='0f32795d8e8f', selected_rank='98',
        selected_subcluster='mapped-caller-callee-bridge-readiness-gate',
        source_symbol_context_count='4', bridge_class='mapped-caller-callee-bridge',
        safe_context_status='filtered-metadata-only', candidate_level_proof_count='0',
        ready_to_reopen_domain_count='0', source_patch_authorized_count='0',
        selected_domain='none', selected_pivot='none', next_ticket='RE-651',
        next_topic='mapped-caller-callee-bridge-readiness-gate', metadata_work_readiness='ready',
        code_change_readiness='blocked',
        stop_condition='narrow rank-98 export requires readiness gate before proof-domain selection',
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
        repo / 'docs/reverse/functions/re650-ghidra-second-window-rank-98-narrow-export.md': '# RE-650 rank-98 narrow export\n\nThe selected candidate is filtered metadata only; production and code work remain blocked.\n',
        repo / 'docs/stories/RE-650-ghidra-second-window-rank-98-narrow-export.md': '# RE-650 rank-98 narrow export\n\n## Progress tracker\n\n- [x] RE-649 handoff validated.\n- [x] Rank-98 context narrowed.\n- [x] Filtered metadata-only safety retained.\n- [x] Production and code work remain blocked.\n- [x] RE-651 selected; not executed.\n',
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
