"""Fail-closed metadata-only RE-508 candidate selection."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse import re309_ghidra_unmapped_bridge_candidates as candidates

BAD = ('0x', 'fun_', 'sub_', 'opcode', 'machine word', 'raw dump', 'raw evidence', 'call_address', 'ghidra_entry', 'code.wad', 'gamewad.obj', 'secret', 'credential', 'asset', 'raw binary', 'source patch', 'address', 'copyright')
FIELDS = ('story_id', 'topic', 'upstream_handoff', 'closed_candidate_id', 'selected_rank', 'selected_candidate_id', 'selected_bridge_class', 'source_symbol_context_count', 'safe_context_status', 'ready_to_reopen_domain_count', 'source_patch_authorized_count', 'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic', 'metadata_work_readiness', 'code_change_readiness', 'stop_condition')
UPFIELDS = ('story_id', 'topic', 'upstream_handoff', 'selected_candidate_id', 'selected_rank', 'selected_subcluster', 'source_symbol_context_count', 'bridge_class', 'safe_context_status', 'source_backed_callsite_count', 'candidate_level_proof_count', 'repository_symbol_direct_proof_count', 'ready_to_reopen_domain_count', 'source_patch_authorized_count', 'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic', 'metadata_work_readiness', 'code_change_readiness', 'stop_condition')


def ranked(repo):
    old = candidates.TOP_LIMIT
    try:
        candidates.TOP_LIMIT = 70
        rows, _ = candidates.build_bridge_candidates(Path(repo))
    finally:
        candidates.TOP_LIMIT = old
    return next((row for row in rows if row.rank == 51), None)


def build(repo):
    path = Path(repo) / 'docs/reverse/generated/re507-mapped-caller-callee-bridge-readiness-gate-handoff.csv'
    with path.open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != UPFIELDS:
            raise ValueError('handoff schema drift')
        rows = list(reader)
    if len(rows) != 1:
        raise ValueError('handoff row-count drift')
    handoff = rows[0]
    expected = {'story_id': 'RE-507', 'topic': 'mapped-caller-callee-bridge-readiness-gate', 'upstream_handoff': 'RE-506', 'selected_candidate_id': 'bdb92ce23200', 'selected_rank': '50', 'selected_subcluster': 'mapped-caller-callee-bridge-readiness-gate', 'source_symbol_context_count': '7', 'bridge_class': 'mapped-caller-callee-bridge', 'safe_context_status': 'filtered-metadata-only', 'source_backed_callsite_count': '0', 'candidate_level_proof_count': '0', 'repository_symbol_direct_proof_count': '0', 'ready_to_reopen_domain_count': '0', 'source_patch_authorized_count': '0', 'selected_domain': 'none', 'selected_pivot': 'none', 'next_ticket': 'RE-508', 'next_topic': 'ghidra-second-window-next-candidate-selection', 'metadata_work_readiness': 'ready', 'code_change_readiness': 'blocked', 'stop_condition': 'metadata-only safety gate denies proof-domain selection and source changes'}
    for key, value in expected.items():
        if handoff.get(key) != value:
            raise ValueError(f'handoff drift: {key}')
    candidate = ranked(repo)
    if candidate is None or (candidate.candidate_id, candidate.bridge_class, candidate.source_context_count, candidate.ready_to_reopen_domain, candidate.source_patch_authorized) != ('27952a832b99', 'mapped-caller-callee-bridge', 7, 'no', 'no'):
        raise ValueError('ranked candidate drift')
    row = dict(story_id='RE-508', topic='ghidra-second-window-next-candidate-selection', upstream_handoff='RE-507', closed_candidate_id=handoff['selected_candidate_id'], selected_rank='51', selected_candidate_id='27952a832b99', selected_bridge_class='mapped-caller-callee-bridge', source_symbol_context_count='7', safe_context_status='filtered-metadata-only', ready_to_reopen_domain_count='0', source_patch_authorized_count='0', selected_domain='none', selected_pivot='none', next_ticket='RE-509', next_topic='ghidra-second-window-rank-51-narrow-export', metadata_work_readiness='ready', code_change_readiness='blocked', stop_condition='next ranked metadata candidate selected; source changes remain blocked')
    validate(row)
    return row


def validate(row):
    if tuple(row) != FIELDS:
        raise ValueError('output schema drift')
    if any(fragment in '\n'.join(row.values()).lower() for fragment in BAD):
        raise ValueError('forbidden output fragment')
    if (row['code_change_readiness'], row['source_patch_authorized_count'], row['safe_context_status']) != ('blocked', '0', 'filtered-metadata-only'):
        raise ValueError('output safety drift')


def write(row, repo):
    validate(row)
    repo = Path(repo); outputs = []; prefix = 're508-ghidra-second-window-next-candidate-selection'
    for suffix in ('candidates', 'summary', 'handoff'):
        path = repo / 'docs/reverse/generated' / f'{prefix}-{suffix}.csv'; path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator='\n'); writer.writeheader(); writer.writerow(row)
        outputs.append(path)
    documents = {repo / 'docs/reverse/functions/re508-ghidra-second-window-next-candidate-selection.md': '# RE-508 selection\n\nFiltered metadata-only decision; source and code work remain blocked.\n', repo / 'docs/stories/RE-508-ghidra-second-window-next-candidate-selection.md': '# RE-508 selection\n\n## Progress tracker\n\n- [x] RE-507 handoff validated.\n- [x] Filtered metadata decision recorded.\n- [x] RE-509 selected; not executed.\n'}
    for path, text in documents.items():
        path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text, encoding='utf-8'); outputs.append(path)
    for path in outputs:
        if any(fragment in path.read_text(encoding='utf-8').lower() for fragment in BAD):
            raise ValueError('forbidden written fragment')
    return outputs


if __name__ == '__main__':
    write(build(ROOT), ROOT)
