"""Fail-closed metadata-only RE-676 candidate selection."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse import re673_ghidra_second_window_next_candidate_selection as base
from scripts.reverse import re556_ghidra_second_window_next_candidate_selection as candidate_source

BAD, UPFIELDS, FIELDS = base.BAD, base.UPFIELDS, base.FIELDS
UPSTREAM = 'docs/reverse/generated/re675-mapped-callee-bridge-readiness-gate-handoff.csv'
PREFIX = 're676-ghidra-second-window-next-candidate-selection'
EXPECTED = {
    'story_id': 'RE-675', 'topic': 'mapped-callee-bridge-readiness-gate',
    'upstream_handoff': 'RE-674', 'selected_candidate_id': 'd46dbf9103fe', 'selected_rank': '106',
    'selected_subcluster': 'mapped-callee-bridge-readiness-gate',
    'source_symbol_context_count': '4', 'bridge_class': 'mapped-callee-bridge',
    'safe_context_status': 'filtered-metadata-only', 'source_backed_callsite_count': '0',
    'candidate_level_proof_count': '0', 'repository_symbol_direct_proof_count': '0',
    'ready_to_reopen_domain_count': '0', 'source_patch_authorized_count': '0',
    'selected_domain': 'none', 'selected_pivot': 'none', 'next_ticket': 'RE-676',
    'next_topic': 'ghidra-second-window-next-candidate-selection',
    'metadata_work_readiness': 'ready', 'code_change_readiness': 'blocked',
    'stop_condition': 'metadata-only safety gate denies proof-domain selection and production changes',
}
OUTPUT = {
    'story_id': 'RE-676', 'topic': 'ghidra-second-window-next-candidate-selection',
    'upstream_handoff': 'RE-675', 'closed_candidate_id': 'd46dbf9103fe',
    'selected_rank': '107', 'selected_candidate_id': 'e16b24e1fe2c',
    'selected_bridge_class': 'mapped-caller-callee-bridge', 'source_symbol_context_count': '4',
    'safe_context_status': 'filtered-metadata-only', 'ready_to_reopen_domain_count': '0',
    'source_patch_authorized_count': '0', 'selected_domain': 'none', 'selected_pivot': 'none',
    'next_ticket': 'RE-677', 'next_topic': 'ghidra-second-window-rank-107-narrow-export',
    'metadata_work_readiness': 'ready', 'code_change_readiness': 'blocked',
    'stop_condition': 'next ranked metadata candidate selected; production changes remain blocked',
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
    old_limit = candidate_source.candidates.TOP_LIMIT
    try:
        candidate_source.candidates.TOP_LIMIT = 109
        entries, _ = candidate_source.candidates.build_bridge_candidates(Path(repo))
    finally:
        candidate_source.candidates.TOP_LIMIT = old_limit
    candidate = next((entry for entry in entries if entry.rank == 107), None)
    actual = None if candidate is None else (candidate.candidate_id, candidate.bridge_class, candidate.source_context_count, candidate.ready_to_reopen_domain, candidate.source_patch_authorized)
    if actual != ('e16b24e1fe2c', 'mapped-caller-callee-bridge', 4, 'no', 'no'):
        raise ValueError('ranked candidate drift')
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
    safety = (row['safe_context_status'], row['ready_to_reopen_domain_count'], row['source_patch_authorized_count'], row['selected_domain'], row['selected_pivot'], row['metadata_work_readiness'], row['code_change_readiness'])
    if safety != ('filtered-metadata-only', '0', '0', 'none', 'none', 'ready', 'blocked'):
        raise ValueError('output safety drift')


def write(row, repo):
    validate(row)
    repo, outputs = Path(repo), []
    for suffix in ('candidates', 'summary', 'handoff'):
        path = repo / 'docs/reverse/generated' / f'{PREFIX}-{suffix}.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator='\n')
            writer.writeheader(); writer.writerow(row)
        outputs.append(path)
    documents = {
        repo / 'docs/reverse/functions/re676-ghidra-second-window-next-candidate-selection.md': '# RE-676 selection\n\nFiltered metadata-only decision; production and code work remain blocked.\n',
        repo / 'docs/stories/RE-676-ghidra-second-window-next-candidate-selection.md': '# RE-676 selection\n\n## Progress tracker\n\n- [x] RE-675 handoff validated.\n- [x] Rank-107 candidate selected from the fixed safe ranking.\n- [x] Filtered metadata-only safety retained.\n- [x] Production and code work remain blocked.\n- [x] RE-677 selected; not executed.\n',
    }
    for path, text in documents.items():
        path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text, encoding='utf-8'); outputs.append(path)
    for path in outputs:
        if any(fragment in path.read_text(encoding='utf-8').lower() for fragment in BAD):
            raise ValueError('forbidden written fragment')
    return outputs


if __name__ == '__main__':
    write(build(ROOT), ROOT)
