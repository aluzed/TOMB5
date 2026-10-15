"""Public checkpoint contract, distinct from recorder behavior."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-959-linux32-recorder-labels.md'
DASHBOARD = ROOT / 'docs/reverse/tomb5-progress-dashboard-re959-v1.html'


def test_story_contract_and_local_links():
    text = STORY.read_text()
    for token in ('12 FAIL', '16 PASS', '477 PASS', 'integration=false', 'production_patch=false', 'Cleanup', 'BLOCKED-008/009/RE944'):
        assert token in text
    links = re.findall(r'\]\(([^)]+)\)', text)
    assert links
    for link in links:
        assert (STORY.parent / link.split('#')[0]).is_file(), link


def test_dashboard_contract_and_local_links():
    text = DASHBOARD.read_text()
    for token in ('RE959', '128', '06h15', '07h00', 'integration=false', 'production_patch=false', 'gameplay'):
        assert token in text
    links = re.findall(r'href="([^"]+)"', text)
    assert links
    for link in links:
        assert (DASHBOARD.parent / link.split('#')[0]).is_file(), link
