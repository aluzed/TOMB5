"""Fail-closed metadata-only RE-562 candidate selection."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse import re556_ghidra_second_window_next_candidate_selection as base

BAD = base.BAD
UPSTREAM = 'docs/reverse/generated/re561-mapped-callee-bridge-readiness-gate-handoff.csv'
PREFIX = 're562-ghidra-second-window-next-candidate-selection'
UPFIELDS = base.UPFIELDS
FIELDS = base.FIELDS


def build(repo):
    with (Path(repo) / UPSTREAM).open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != UPFIELDS:
            raise ValueError('handoff schema drift')
        rows = list(reader)
    expected = {'story_id': 'RE-561', 'topic': 'mapped-callee-bridge-readiness-gate', 'upstream_handoff': 'RE-560', 'selected_candidate_id': 'b7ab26b5c07b', 'selected_rank': '68', 'selected_subcluster': 'mapped-callee-bridge-readiness-gate', 'source_symbol_context_count': '4', 'bridge_class': 'mapped-callee-bridge', 'safe_context_status': 'filtered-metadata-only', 'source_backed_callsite_count': '0', 'candidate_level_proof_count': '0', 'repository_symbol_direct_proof_count': '0', 'ready_to_reopen_domain_count': '0', 'source_patch_authorized_count': '0', 'selected_domain': 'none', 'selected_pivot': 'none', 'next_ticket': 'RE-562', 'next_topic': 'ghidra-second-window-next-candidate-selection', 'metadata_work_readiness': 'ready', 'code_change_readiness': 'blocked', 'stop_condition': 'metadata-only safety gate denies proof-domain selection and source changes'}
    if len(rows) != 1 or any(rows[0].get(key) != value for key, value in expected.items()):
        raise ValueError('handoff drift')
    old = base.candidates.TOP_LIMIT
    try:
        base.candidates.TOP_LIMIT = 80
        entries, _ = base.candidates.build_bridge_candidates(Path(repo))
    finally:
        base.candidates.TOP_LIMIT = old
    candidate = next((entry for entry in entries if entry.rank == 69), None)
    if candidate is None or (candidate.candidate_id, candidate.bridge_class, candidate.source_context_count, candidate.ready_to_reopen_domain, candidate.source_patch_authorized) != ('e5b9063e77db', 'mapped-caller-callee-bridge', 6, 'no', 'no'):
        raise ValueError('ranked candidate drift')
    row = dict(story_id='RE-562', topic='ghidra-second-window-next-candidate-selection', upstream_handoff='RE-561', closed_candidate_id=rows[0]['selected_candidate_id'], selected_rank='69', selected_candidate_id='e5b9063e77db', selected_bridge_class='mapped-caller-callee-bridge', source_symbol_context_count='6', safe_context_status='filtered-metadata-only', ready_to_reopen_domain_count='0', source_patch_authorized_count='0', selected_domain='none', selected_pivot='none', next_ticket='RE-563', next_topic='ghidra-second-window-rank-69-narrow-export', metadata_work_readiness='ready', code_change_readiness='blocked', stop_condition='next ranked metadata candidate selected; source changes remain blocked')
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
    repo = Path(repo)
    outputs = []
    for suffix in ('candidates', 'summary', 'handoff'):
        path = repo / 'docs/reverse/generated' / f'{PREFIX}-{suffix}.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator='\n')
            writer.writeheader()
            writer.writerow(row)
        outputs.append(path)
    documents = {
        repo / 'docs/reverse/functions/re562-ghidra-second-window-next-candidate-selection.md': '# RE-562 selection\n\nFiltered metadata-only decision; source and code work remain blocked.\n',
        repo / 'docs/stories/RE-562-ghidra-second-window-next-candidate-selection.md': '# RE-562 selection\n\n## Progress tracker\n\n- [x] RE-561 handoff validated.\n- [x] Filtered metadata decision recorded.\n- [x] RE-563 selected; not executed.\n',
    }
    for path, text in documents.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        outputs.append(path)
    if any(fragment in path.read_text(encoding='utf-8').lower() for path in outputs for fragment in BAD):
        raise ValueError('forbidden written fragment')
    return outputs


if __name__ == '__main__':
    write(build(ROOT), ROOT)
