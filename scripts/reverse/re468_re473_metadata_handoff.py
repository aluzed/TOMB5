"""Fail-closed metadata-only handoffs for the authorized RE-468--RE-473 batch."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse import re309_ghidra_unmapped_bridge_candidates as candidates

FORBIDDEN_OUTPUT_FRAGMENTS = (
    '0x', 'fun_', 'sub_', 'word_le_hex', 'payload_offset', 'opcode', 'machine word',
    'raw dump', 'raw evidence', 'raw_evidence', 'call_address', 'branch target', 'call target',
    'ghidra_entry', 'ghidra_name', 'source_line_text', 'code.wad', 'gamewad.obj',
    'secret', 'private key', 'credential', 'asset', 'raw binary', 'source patch', 'address',
    'symbol evidence', 'copyright',
)
NARROW_FIELDS = (
    'story_id', 'topic', 'upstream_handoff', 'selected_candidate_id', 'selected_rank',
    'selected_subcluster', 'source_symbol_context_count', 'bridge_class',
    'safe_context_status', 'candidate_level_proof_count', 'ready_to_reopen_domain_count',
    'source_patch_authorized_count', 'selected_domain', 'selected_pivot', 'next_ticket',
    'next_topic', 'metadata_work_readiness', 'code_change_readiness', 'stop_condition',
)
GATE_FIELDS = (
    'story_id', 'topic', 'upstream_handoff', 'selected_candidate_id', 'selected_rank',
    'selected_subcluster', 'source_symbol_context_count', 'bridge_class',
    'safe_context_status', 'source_backed_callsite_count', 'candidate_level_proof_count',
    'repository_symbol_direct_proof_count', 'ready_to_reopen_domain_count',
    'source_patch_authorized_count', 'selected_domain', 'selected_pivot', 'next_ticket',
    'next_topic', 'metadata_work_readiness', 'code_change_readiness', 'stop_condition',
)
SELECTION_FIELDS = (
    'story_id', 'topic', 'upstream_handoff', 'closed_candidate_id', 'selected_rank',
    'selected_candidate_id', 'selected_bridge_class', 'source_symbol_context_count',
    'safe_context_status', 'ready_to_reopen_domain_count', 'source_patch_authorized_count',
    'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic',
    'metadata_work_readiness', 'code_change_readiness', 'stop_condition',
)

CONFIG = {
    'RE-468': dict(topic='mapped-caller-callee-bridge-readiness-gate', kind='gate', upstream='RE-467',
        candidate='c03793ac47a9', rank='37', bridge='mapped-caller-callee-bridge', contexts='8',
        next_ticket='RE-469', next_topic='ghidra-second-window-next-candidate-selection'),
    'RE-469': dict(topic='ghidra-second-window-next-candidate-selection', kind='selection', upstream='RE-468',
        candidate='6c0aef5fd528', rank='38', bridge='mapped-callee-bridge', contexts='6',
        next_ticket='RE-470', next_topic='ghidra-second-window-rank-38-narrow-export'),
    'RE-470': dict(topic='ghidra-second-window-rank-38-narrow-export', kind='narrow', upstream='RE-469',
        candidate='6c0aef5fd528', rank='38', bridge='mapped-callee-bridge', contexts='6',
        next_ticket='RE-471', next_topic='mapped-callee-bridge-readiness-gate'),
    'RE-471': dict(topic='mapped-callee-bridge-readiness-gate', kind='gate', upstream='RE-470',
        candidate='6c0aef5fd528', rank='38', bridge='mapped-callee-bridge', contexts='6',
        next_ticket='RE-472', next_topic='ghidra-second-window-next-candidate-selection'),
    'RE-472': dict(topic='ghidra-second-window-next-candidate-selection', kind='selection', upstream='RE-471',
        candidate='c9a7379cc772', rank='39', bridge='mapped-callee-bridge', contexts='6',
        next_ticket='RE-473', next_topic='ghidra-second-window-rank-39-narrow-export'),
    'RE-473': dict(topic='ghidra-second-window-rank-39-narrow-export', kind='narrow', upstream='RE-472',
        candidate='c9a7379cc772', rank='39', bridge='mapped-callee-bridge', contexts='6',
        next_ticket='RE-474', next_topic='mapped-callee-bridge-readiness-gate'),
}


def fields_for(kind):
    return {'narrow': NARROW_FIELDS, 'gate': GATE_FIELDS, 'selection': SELECTION_FIELDS}[kind]


def prefix(ticket, config):
    return f"re{ticket[3:]}-{config['topic']}"


def upstream_path(repo, ticket, config):
    previous = CONFIG.get(config['upstream'])
    if previous:
        return Path(repo) / 'docs/reverse/generated' / f"{prefix(config['upstream'], previous)}-handoff.csv"
    return Path(repo) / 'docs/reverse/generated/re467-ghidra-second-window-rank-37-narrow-export-handoff.csv'


def read_upstream(repo, ticket, config):
    previous = CONFIG.get(config['upstream'])
    expected_fields = fields_for(previous['kind']) if previous else NARROW_FIELDS
    with upstream_path(repo, ticket, config).open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != expected_fields:
            raise ValueError('handoff schema drift')
        rows = list(reader)
    if len(rows) != 1:
        raise ValueError('handoff row-count drift')
    row = rows[0]
    required = {'story_id': config['upstream'], 'next_ticket': ticket,
                'metadata_work_readiness': 'ready', 'code_change_readiness': 'blocked',
                'source_patch_authorized_count': '0', 'selected_domain': 'none', 'selected_pivot': 'none'}
    if previous:
        required.update({'topic': previous['topic'], 'selected_candidate_id': previous['candidate'],
                         'selected_rank': previous['rank']})
    else:
        required.update({'topic': 'ghidra-second-window-rank-37-narrow-export',
                         'selected_candidate_id': 'c03793ac47a9', 'selected_rank': '37'})
    for key, value in required.items():
        if row.get(key) != value:
            raise ValueError(f'handoff drift: {key}')
    return row


def ranked_candidate(repo, rank):
    old_limit = candidates.TOP_LIMIT
    try:
        candidates.TOP_LIMIT = 50
        rows, _ = candidates.build_bridge_candidates(Path(repo))
    finally:
        candidates.TOP_LIMIT = old_limit
    return next((row for row in rows if row.rank == int(rank)), None)


def build(ticket, repo):
    config = CONFIG[ticket]
    upstream = read_upstream(repo, ticket, config)
    if config['kind'] == 'selection':
        candidate = ranked_candidate(repo, config['rank'])
        expected = (config['candidate'], config['bridge'], int(config['contexts']))
        if candidate is None or (candidate.candidate_id, candidate.bridge_class, candidate.source_context_count) != expected:
            raise ValueError('ranked candidate drift')
        if candidate.ready_to_reopen_domain != 'no' or candidate.source_patch_authorized != 'no':
            raise ValueError('candidate readiness drift')
    common = dict(story_id=ticket, topic=config['topic'], upstream_handoff=config['upstream'],
        selected_candidate_id=config['candidate'], selected_rank=config['rank'],
        source_symbol_context_count=config['contexts'], safe_context_status='filtered-metadata-only',
        ready_to_reopen_domain_count='0', source_patch_authorized_count='0', selected_domain='none',
        selected_pivot='none', next_ticket=config['next_ticket'], next_topic=config['next_topic'],
        metadata_work_readiness='ready', code_change_readiness='blocked',
        stop_condition='metadata-only safety gate denies proof-domain selection and source changes')
    if config['kind'] == 'selection':
        return dict(story_id=ticket, topic=config['topic'], upstream_handoff=config['upstream'],
            closed_candidate_id=upstream['selected_candidate_id'], selected_rank=config['rank'],
            selected_candidate_id=config['candidate'], selected_bridge_class=config['bridge'],
            source_symbol_context_count=config['contexts'], safe_context_status='filtered-metadata-only',
            ready_to_reopen_domain_count='0', source_patch_authorized_count='0', selected_domain='none',
            selected_pivot='none', next_ticket=config['next_ticket'], next_topic=config['next_topic'],
            metadata_work_readiness='ready', code_change_readiness='blocked',
            stop_condition='next ranked metadata candidate selected; source changes remain blocked')
    common['selected_subcluster'] = config['topic'] if config['kind'] == 'gate' else config['next_topic']
    common['bridge_class'] = config['bridge']
    if config['kind'] == 'gate':
        common.update(source_backed_callsite_count='0', candidate_level_proof_count='0',
                      repository_symbol_direct_proof_count='0')
    else:
        common['candidate_level_proof_count'] = '0'
    return {field: common[field] for field in fields_for(config['kind'])}


def validate_output(ticket, result):
    config = CONFIG[ticket]
    if tuple(result) != fields_for(config['kind']):
        raise ValueError('output schema drift')
    text = '\n'.join(str(value).lower() for value in result.values())
    if any(fragment in text for fragment in FORBIDDEN_OUTPUT_FRAGMENTS):
        raise ValueError('forbidden output fragment')
    expected = {'story_id': ticket, 'topic': config['topic'], 'upstream_handoff': config['upstream'],
                'selected_candidate_id': config['candidate'], 'selected_rank': config['rank'],
                'source_symbol_context_count': config['contexts'],
                'next_ticket': config['next_ticket'], 'next_topic': config['next_topic'],
                'metadata_work_readiness': 'ready', 'code_change_readiness': 'blocked',
                'source_patch_authorized_count': '0', 'selected_domain': 'none', 'selected_pivot': 'none',
                'stop_condition': ('next ranked metadata candidate selected; source changes remain blocked'
                                   if config['kind'] == 'selection'
                                   else 'metadata-only safety gate denies proof-domain selection and source changes')}
    if config['kind'] == 'selection':
        expected.update(closed_candidate_id=(CONFIG[config['upstream']]['candidate']
                                             if config['upstream'] in CONFIG else 'c03793ac47a9'),
                        selected_bridge_class=config['bridge'])
    else:
        expected.update(selected_subcluster=(config['topic'] if config['kind'] == 'gate' else config['next_topic']),
                        bridge_class=config['bridge'], candidate_level_proof_count='0')
        if config['kind'] == 'gate':
            expected.update(source_backed_callsite_count='0', repository_symbol_direct_proof_count='0')
    for key, value in expected.items():
        if result.get(key) != value:
            raise ValueError(f'output safety drift: {key}')
    safety_expected = {
        'safe_context_status': 'filtered-metadata-only',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'code_change_readiness': 'blocked',
    }
    if config['kind'] != 'selection':
        safety_expected['candidate_level_proof_count'] = '0'
    if config['kind'] == 'gate':
        safety_expected.update(source_backed_callsite_count='0', repository_symbol_direct_proof_count='0')
    for key, value in safety_expected.items():
        if result.get(key) != value:
            raise ValueError('output safety drift')


def write(ticket, result, repo):
    validate_output(ticket, result)
    config = CONFIG[ticket]
    repo = Path(repo)
    output = []
    suffixes = {'gate': ('gate', 'summary', 'handoff'), 'selection': ('candidates', 'summary', 'handoff'), 'narrow': ('contexts', 'summary', 'handoff')}[config['kind']]
    for suffix in suffixes:
        path = repo / 'docs/reverse/generated' / f"{prefix(ticket, config)}-{suffix}.csv"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=result.keys(), lineterminator='\n')
            writer.writeheader(); writer.writerow(result)
        output.append(path)
    docs = {
        repo / 'docs/reverse/functions' / f"re{ticket[3:]}-{config['topic']}.md":
            f"# {ticket} {config['topic']}\n\nFiltered metadata-only decision; source and code work remain blocked.\n",
        repo / 'docs/stories' / f"{ticket}-{config['topic']}.md":
            f"# {ticket} {config['topic']}\n\n## Progress tracker\n\n- [x] {config['upstream']} handoff validated.\n- [x] Filtered metadata decision recorded.\n- [x] Safety guard retained.\n- [x] Source and code work remain blocked.\n- [x] {config['next_ticket']} selected; not executed.\n",
    }
    for path, content in docs.items():
        path.parent.mkdir(parents=True, exist_ok=True); path.write_text(content, encoding='utf-8'); output.append(path)
    for path in output:
        if any(fragment in path.read_text(encoding='utf-8').lower() for fragment in FORBIDDEN_OUTPUT_FRAGMENTS):
            raise ValueError('forbidden written fragment')
    return output
