"""Fail-closed metadata-only RE-664 candidate selection."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse import re661_ghidra_second_window_next_candidate_selection as base
from scripts.reverse import re556_ghidra_second_window_next_candidate_selection as candidate_source

BAD, UPFIELDS, FIELDS = base.BAD, base.UPFIELDS, base.FIELDS
UPSTREAM = 'docs/reverse/generated/re663-mapped-callee-bridge-readiness-gate-handoff.csv'
PREFIX = 're664-ghidra-second-window-next-candidate-selection'
EXPECTED = {
    'story_id': 'RE-663', 'topic': 'mapped-callee-bridge-readiness-gate',
    'upstream_handoff': 'RE-662', 'selected_candidate_id': '3de39d58a7ec', 'selected_rank': '102',
    'selected_subcluster': 'mapped-callee-bridge-readiness-gate',
    'source_symbol_context_count': '4', 'bridge_class': 'mapped-callee-bridge',
    'safe_context_status': 'filtered-metadata-only', 'source_backed_callsite_count': '0',
    'candidate_level_proof_count': '0', 'repository_symbol_direct_proof_count': '0',
    'ready_to_reopen_domain_count': '0', 'source_patch_authorized_count': '0',
    'selected_domain': 'none', 'selected_pivot': 'none', 'next_ticket': 'RE-664',
    'next_topic': 'ghidra-second-window-next-candidate-selection',
    'metadata_work_readiness': 'ready', 'code_change_readiness': 'blocked',
    'stop_condition': 'metadata-only safety gate denies proof-domain selection and production changes',
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
    old_limit = candidate_source.candidates.TOP_LIMIT
    try:
        candidate_source.candidates.TOP_LIMIT = 105
        entries, _ = candidate_source.candidates.build_bridge_candidates(Path(repo))
    finally:
        candidate_source.candidates.TOP_LIMIT = old_limit
    candidate = next((entry for entry in entries if entry.rank == 103), None)
    actual = None if candidate is None else (candidate.candidate_id, candidate.bridge_class, candidate.source_context_count, candidate.ready_to_reopen_domain, candidate.source_patch_authorized)
    if actual != ('e95e1266523c', 'mapped-caller-callee-bridge', 4, 'no', 'no'):
        raise ValueError('ranked candidate drift')
    row = dict(story_id='RE-664', topic='ghidra-second-window-next-candidate-selection', upstream_handoff='RE-663', closed_candidate_id=rows[0]['selected_candidate_id'], selected_rank='103', selected_candidate_id='e95e1266523c', selected_bridge_class='mapped-caller-callee-bridge', source_symbol_context_count='4', safe_context_status='filtered-metadata-only', ready_to_reopen_domain_count='0', source_patch_authorized_count='0', selected_domain='none', selected_pivot='none', next_ticket='RE-665', next_topic='ghidra-second-window-rank-103-narrow-export', metadata_work_readiness='ready', code_change_readiness='blocked', stop_condition='next ranked metadata candidate selected; production changes remain blocked')
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
    for suffix in ('candidates', 'summary', 'handoff'):
        path = repo / 'docs/reverse/generated' / f'{PREFIX}-{suffix}.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator='\n')
            writer.writeheader()
            writer.writerow(row)
        outputs.append(path)
    documents = {
        repo / 'docs/reverse/functions/re664-ghidra-second-window-next-candidate-selection.md': '# RE-664 selection\n\nFiltered metadata-only decision; production and code work remain blocked.\n',
        repo / 'docs/stories/RE-664-ghidra-second-window-next-candidate-selection.md': '# RE-664 selection\n\n## Progress tracker\n\n- [x] RE-663 handoff validated.\n- [x] Rank-103 candidate selected from the fixed safe ranking.\n- [x] Filtered metadata-only safety retained.\n- [x] Production and code work remain blocked.\n- [x] RE-665 selected; not executed.\n',
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
