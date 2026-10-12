"""Public documentation contract; no executable or private proof import."""
from pathlib import Path
import hashlib
import re
import pytest
ROOT=Path(__file__).resolve().parents[2]
STORY='docs/stories/blocked/BLOCKED-007-re930-provider-refusal.md'
DASH='docs/reverse/tomb5-progress-dashboard-re930-incident-v1.html'
INDEX='docs/stories/README.md'

def test_durable_story_exists():
 assert (ROOT/STORY).is_file(), 'provider incident lacks durable blocker story'

def test_story_scope_and_tracker():
 text=(ROOT/STORY).read_text()
 for token in ['Status: `Blocked`','## Progression','## Preuves','## Critères de réouverture','PROVIDER_SAFETY_FILTER_BLOCKED','deleg_d079cd72','17.06','ZERO nouveau build','ZERO nouvelle exécution CPU','aucun contournement','integration=false','Sony','OpenBIOS','[x]','[ ]','0edd91701bff3dcc37dab8948812fce503f296ca','c2300e5f95adfd5407976e7abf2bcdfc8afad85d207a9f8f43843b98e99385cc']:
  assert token in text, token
 assert not re.search(r'0x[0-9a-fA-F]+|word_le_hex|raw_opcode|payload_offset',text)

def test_index_links_blocker():
 assert '(blocked/BLOCKED-007-re930-provider-refusal.md)' in (ROOT/INDEX).read_text()

def test_versioned_dashboard_honest_and_linked():
 text=(ROOT/DASH).read_text()
 for token in ['RE930','PROVIDER_SAFETY_FILTER_BLOCKED','data-integration="false"','BLOCKED-007-re930-provider-refusal.md','aucun nouveau build','RE929','RE928','aucun contournement']:
  assert token in text, token
 for href in re.findall(r'href="([^"]+)"',text):
  assert ((ROOT/DASH).parent/href.split('#')[0]).is_file(), href

def test_preceding_maintained_dashboard_unchanged():
 assert hashlib.sha256((ROOT/'docs/reverse/tomb5-progress-dashboard.html').read_bytes()).hexdigest()==MAINTAINED_CURRENT_SHA

MAINTAINED_CURRENT_SHA='620616cdf4bec219954a35547d09acfd079b4cc91caf50eecb7ea475d5970e36'

def test_deleted_user_blockers_not_restored():
 assert not (ROOT/'docs/stories/blocked/BLOCKED-001-RE783-closure.md').exists()
 assert not (ROOT/'docs/stories/blocked/BLOCKED-002-getfloor-ubsan-closure.md').exists()
