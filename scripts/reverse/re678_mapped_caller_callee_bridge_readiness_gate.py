"""Produce the fail-closed, metadata-only RE-678 readiness gate."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse import re672_mapped_callee_bridge_readiness_gate as base

BAD, UPFIELDS, FIELDS = base.BAD, base.UPFIELDS, base.FIELDS
UPSTREAM = 'docs/reverse/generated/re677-ghidra-second-window-rank-107-narrow-export-handoff.csv'
PREFIX = 're678-mapped-caller-callee-bridge-readiness-gate'
EXPECTED = {
    'story_id': 'RE-677', 'topic': 'ghidra-second-window-rank-107-narrow-export',
    'upstream_handoff': 'RE-676', 'selected_candidate_id': 'e16b24e1fe2c',
    'selected_rank': '107',
    'selected_subcluster': 'mapped-caller-callee-bridge-readiness-gate',
    'source_symbol_context_count': '4', 'bridge_class': 'mapped-caller-callee-bridge',
    'safe_context_status': 'filtered-metadata-only', 'candidate_level_proof_count': '0',
    'ready_to_reopen_domain_count': '0', 'source_patch_authorized_count': '0',
    'selected_domain': 'none', 'selected_pivot': 'none', 'next_ticket': 'RE-678',
    'next_topic': 'mapped-caller-callee-bridge-readiness-gate',
    'metadata_work_readiness': 'ready', 'code_change_readiness': 'blocked',
    'stop_condition': 'narrow rank-107 export requires readiness gate before proof-domain selection',
}
OUTPUT = {
    'story_id': 'RE-678', 'topic': 'mapped-caller-callee-bridge-readiness-gate',
    'upstream_handoff': 'RE-677', 'selected_candidate_id': 'e16b24e1fe2c',
    'selected_rank': '107',
    'selected_subcluster': 'mapped-caller-callee-bridge-readiness-gate',
    'source_symbol_context_count': '4', 'bridge_class': 'mapped-caller-callee-bridge',
    'safe_context_status': 'filtered-metadata-only', 'source_backed_callsite_count': '0',
    'candidate_level_proof_count': '0', 'repository_symbol_direct_proof_count': '0',
    'ready_to_reopen_domain_count': '0', 'source_patch_authorized_count': '0',
    'selected_domain': 'none', 'selected_pivot': 'none',
    'next_ticket': 'RE-679', 'next_topic': 'ghidra-second-window-next-candidate-selection',
    'metadata_work_readiness': 'ready', 'code_change_readiness': 'blocked',
    'stop_condition': 'metadata-only safety gate denies proof-domain selection and production changes',
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
    safety = (row['safe_context_status'], row['candidate_level_proof_count'],
              row['ready_to_reopen_domain_count'], row['source_patch_authorized_count'],
              row['selected_domain'], row['selected_pivot'],
              row['metadata_work_readiness'], row['code_change_readiness'])
    if safety != ('filtered-metadata-only', '0', '0', '0', 'none', 'none', 'ready', 'blocked'):
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
        repo / 'docs/reverse/functions/re678-mapped-caller-callee-bridge-readiness-gate.md': '# RE-678 readiness gate\n\nFiltered metadata-only decision; production and code work remain blocked.\n',
        repo / 'docs/stories/RE-678-mapped-caller-callee-bridge-readiness-gate.md': '# RE-678 readiness gate\n\n## Progress tracker\n\n- [x] RE-677 handoff validated.\n- [x] Filtered metadata decision recorded.\n- [x] Safety guard retained.\n- [x] Production and code work remain blocked.\n- [x] RE-679 selected; not executed.\n',
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
