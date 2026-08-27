"""Produce the fail-closed, metadata-only RE-663 readiness gate."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse import re660_mapped_caller_bridge_readiness_gate as base

BAD, UPFIELDS, FIELDS = base.BAD, base.UPFIELDS, base.FIELDS
UPSTREAM = 'docs/reverse/generated/re662-ghidra-second-window-rank-102-narrow-export-handoff.csv'
PREFIX = 're663-mapped-callee-bridge-readiness-gate'
EXPECTED = {
    'story_id': 'RE-662', 'topic': 'ghidra-second-window-rank-102-narrow-export',
    'upstream_handoff': 'RE-661', 'selected_candidate_id': '3de39d58a7ec', 'selected_rank': '102',
    'selected_subcluster': 'mapped-callee-bridge-readiness-gate',
    'source_symbol_context_count': '4', 'bridge_class': 'mapped-callee-bridge',
    'safe_context_status': 'filtered-metadata-only', 'candidate_level_proof_count': '0',
    'ready_to_reopen_domain_count': '0', 'source_patch_authorized_count': '0',
    'selected_domain': 'none', 'selected_pivot': 'none', 'next_ticket': 'RE-663',
    'next_topic': 'mapped-callee-bridge-readiness-gate',
    'metadata_work_readiness': 'ready', 'code_change_readiness': 'blocked',
    'stop_condition': 'narrow rank-102 export requires readiness gate before proof-domain selection',
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
        story_id='RE-663', topic='mapped-callee-bridge-readiness-gate',
        upstream_handoff='RE-662', selected_candidate_id='3de39d58a7ec', selected_rank='102',
        selected_subcluster='mapped-callee-bridge-readiness-gate',
        source_symbol_context_count='4', bridge_class='mapped-callee-bridge',
        safe_context_status='filtered-metadata-only', source_backed_callsite_count='0',
        candidate_level_proof_count='0', repository_symbol_direct_proof_count='0',
        ready_to_reopen_domain_count='0', source_patch_authorized_count='0',
        selected_domain='none', selected_pivot='none', next_ticket='RE-664',
        next_topic='ghidra-second-window-next-candidate-selection', metadata_work_readiness='ready',
        code_change_readiness='blocked',
        stop_condition='metadata-only safety gate denies proof-domain selection and production changes',
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
    for suffix in ('gate', 'summary', 'handoff'):
        path = repo / 'docs/reverse/generated' / f'{PREFIX}-{suffix}.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator='\n')
            writer.writeheader()
            writer.writerow(row)
        outputs.append(path)
    documents = {
        repo / 'docs/reverse/functions/re663-mapped-callee-bridge-readiness-gate.md': '# RE-663 readiness gate\n\nFiltered metadata-only decision; production and code work remain blocked.\n',
        repo / 'docs/stories/RE-663-mapped-callee-bridge-readiness-gate.md': '# RE-663 readiness gate\n\n## Progress tracker\n\n- [x] RE-662 handoff validated.\n- [x] Filtered metadata decision recorded.\n- [x] Safety guard retained.\n- [x] Production and code work remain blocked.\n- [x] RE-664 selected; not executed.\n',
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
