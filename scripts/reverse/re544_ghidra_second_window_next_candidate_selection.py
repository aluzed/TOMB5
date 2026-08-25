"""Fail-closed metadata-only RE-544 candidate selection."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse import re309_ghidra_unmapped_bridge_candidates as candidates

BAD = ('0x', 'fun_', 'sub_', 'word_le_hex', 'payload_offset', 'opcode', 'machine word', 'raw dump', 'raw evidence', 'raw_evidence', 'call_address', 'branch target', 'call target', 'ghidra_entry', 'ghidra_name', 'source_line_text', 'code.wad', 'gamewad.obj', 'secret', 'private key', 'credential', 'asset', 'raw binary', 'source patch', 'address', 'symbol evidence', 'copyright')
UPSTREAM = 'docs/reverse/generated/re543-mapped-caller-callee-bridge-readiness-gate-handoff.csv'
PREFIX = 're544-ghidra-second-window-next-candidate-selection'
UPFIELDS = ('story_id', 'topic', 'upstream_handoff', 'selected_candidate_id', 'selected_rank', 'selected_subcluster', 'source_symbol_context_count', 'bridge_class', 'safe_context_status', 'source_backed_callsite_count', 'candidate_level_proof_count', 'repository_symbol_direct_proof_count', 'ready_to_reopen_domain_count', 'source_patch_authorized_count', 'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic', 'metadata_work_readiness', 'code_change_readiness', 'stop_condition')
FIELDS = ('story_id', 'topic', 'upstream_handoff', 'closed_candidate_id', 'selected_rank', 'selected_candidate_id', 'selected_bridge_class', 'source_symbol_context_count', 'safe_context_status', 'ready_to_reopen_domain_count', 'source_patch_authorized_count', 'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic', 'metadata_work_readiness', 'code_change_readiness', 'stop_condition')


def ranked(repo):
    old = candidates.TOP_LIMIT
    try:
        candidates.TOP_LIMIT = 80
        rows, _ = candidates.build_bridge_candidates(Path(repo))
    finally:
        candidates.TOP_LIMIT = old
    return next((row for row in rows if row.rank == 63), None)


def build(repo):
    with (Path(repo) / UPSTREAM).open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != UPFIELDS:
            raise ValueError('handoff schema drift')
        rows = list(reader)
    if len(rows) != 1:
        raise ValueError('handoff row-count drift')
    expected = {'story_id': 'RE-543', 'topic': 'mapped-caller-callee-bridge-readiness-gate', 'upstream_handoff': 'RE-542', 'selected_candidate_id': '605d53c8fbfb', 'selected_rank': '62', 'selected_subcluster': 'mapped-caller-callee-bridge-readiness-gate', 'source_symbol_context_count': '6', 'bridge_class': 'mapped-caller-callee-bridge', 'safe_context_status': 'filtered-metadata-only', 'source_backed_callsite_count': '0', 'candidate_level_proof_count': '0', 'repository_symbol_direct_proof_count': '0', 'ready_to_reopen_domain_count': '0', 'source_patch_authorized_count': '0', 'selected_domain': 'none', 'selected_pivot': 'none', 'next_ticket': 'RE-544', 'next_topic': 'ghidra-second-window-next-candidate-selection', 'metadata_work_readiness': 'ready', 'code_change_readiness': 'blocked', 'stop_condition': 'metadata-only safety gate denies proof-domain selection and source changes'}
    if any(rows[0].get(key) != value for key, value in expected.items()):
        raise ValueError('handoff drift')
    candidate = ranked(repo)
    if candidate is None or (candidate.candidate_id, candidate.bridge_class, candidate.source_context_count, candidate.ready_to_reopen_domain, candidate.source_patch_authorized) != ('0887abf727ec', 'mapped-caller-callee-bridge', 6, 'no', 'no'):
        raise ValueError('ranked candidate drift')
    row = dict(story_id='RE-544', topic='ghidra-second-window-next-candidate-selection', upstream_handoff='RE-543', closed_candidate_id=rows[0]['selected_candidate_id'], selected_rank='63', selected_candidate_id='0887abf727ec', selected_bridge_class='mapped-caller-callee-bridge', source_symbol_context_count='6', safe_context_status='filtered-metadata-only', ready_to_reopen_domain_count='0', source_patch_authorized_count='0', selected_domain='none', selected_pivot='none', next_ticket='RE-545', next_topic='ghidra-second-window-rank-63-narrow-export', metadata_work_readiness='ready', code_change_readiness='blocked', stop_condition='next ranked metadata candidate selected; source changes remain blocked')
    validate(row)
    return row


def validate(row):
    if tuple(row) != FIELDS:
        raise ValueError('output schema drift')
    if any(item in '\n'.join(map(str, row.values())).lower() for item in BAD):
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
    documents = {repo / 'docs/reverse/functions/re544-ghidra-second-window-next-candidate-selection.md': '# RE-544 selection\n\nFiltered metadata-only decision; source and code work remain blocked.\n', repo / 'docs/stories/RE-544-ghidra-second-window-next-candidate-selection.md': '# RE-544 selection\n\n## Progress tracker\n\n- [x] RE-543 handoff validated.\n- [x] Filtered metadata decision recorded.\n- [x] RE-545 selected; not executed.\n'}
    for path, text in documents.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        outputs.append(path)
    if any(item in path.read_text(encoding='utf-8').lower() for path in outputs for item in BAD):
        raise ValueError('forbidden written fragment')
    return outputs


if __name__ == '__main__':
    write(build(ROOT), ROOT)
