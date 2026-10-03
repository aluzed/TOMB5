"""RE811 safe publication and scoped approval contracts."""
import hashlib,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def test_safe_scoped_publication():
 p=R/'docs/reverse/generated/re811-removeactiveitem-integration.json'
 assert p.exists(),'RED: public RE811 metadata missing'
 d=json.loads(p.read_text());assert d['schema']=='re811-removeactiveitem-integration-v1'
 assert d['source_sha256']=='4e4374916bf454fd577fb92d89e7160a1b818e5a744e9244ad89c44fbb0ef84f'
 assert hashlib.sha256((R/'GAME/ITEMS.C').read_bytes()).hexdigest()==d['source_sha256']
 assert d['baseline_failures_per_mode']==74 and d['cases_per_mode']==106 and d['candidate_failures_per_mode']==0
 assert d['independent_publication_review']=='PASS_scoped'
 assert d['technical_review_scope']=='RE810-private-scoped-RemoveActiveItem-only'
 assert d['fullbuild']['exit']==0 and d['fullbuild']['elf_class']=='ELF32' and d['fullbuild']['machine']=='Intel 80386'
 for k in ['gameplay_performed','runtime_performed','global_green','production_ready','AnimateItem_activated','DoorControl_activated','target_matrix_replayed']:
  assert d[k] is False
 story=(R/'docs/stories/RE-811-removeactiveitem-integration.md').read_text()
 assert '## Tracker' in story and '- [x]' in story and '- [ ]' in story
 for text in [p.read_text(),story]:
  assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|payload_offset|word_le_hex|data:image|```(?:asm|mips|cpp|c)\b',text)

def test_current_independent_review_status_contract():
 d=json.loads((R/'docs/reverse/generated/re811-removeactiveitem-integration.json').read_text())
 assert d['independent_publication_review']=='PASS_scoped', 'RED: current independent review still pending'
 review=d['current_publication_review']
 assert review['verdict_sha256']=='76e0814267b9f6e6a037c644b317443809ee808992b732677de2549fc0e8f5d8'
 assert review['proof_verdict_sha256']=='f336e7336e0abb942ed7434c1598e50c9b4d874df3c486d543a670067e01ad77'
 assert review['scope']=='exact-reviewed-18-author-hashes-only; reconciliation-awaits-final-independent-review'
 assert d['target_matrix_replayed'] is False
 assert d['reviewer_target_matrix_replayed'] is True
 assert review['target_cases']==106 and review['target_events']==212 and review['public_buffer_bytes']==866
 assert review['full_memory_bytes']==2097152
 assert review['build_validation']=='archived-incremental-ledger-and-current-ELF32-hash-not-fresh-review-build'
 assert review['first_missing_link_log_preserved'] is False
 for k in ['gameplay_performed','runtime_performed','global_green','production_ready','AnimateItem_activated','DoorControl_activated']:
  assert d[k] is False
 assert 'software ISA, not hardware' in review['limits']
 assert 'no alternative architectures or natural producer reachability acceptance' in review['limits']
 story=(R/'docs/stories/RE-811-removeactiveitem-integration.md').read_text()
 assert '- [x] Revue indépendante de ce livrable public' in story
 assert '## CURRENT — revue finale de publication indépendante' in story
 assert review['verdict_sha256'] in story and review['proof_verdict_sha256'] in story
 dashboard=(R/'docs/reverse/reconstruction-progress.html').read_text()
 current=dashboard.split('<!-- start re811-removeactiveitem-integration -->')[1]
 assert 'CURRENT RE811: PASS_scoped' in current
 assert review['verdict_sha256'] in current and review['proof_verdict_sha256'] in current
