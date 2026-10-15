"""Documentary stop notice only; does not execute reverse-engineering evidence."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
BLOCKER = ROOT / "docs/stories/blocked/BLOCKED-009-autonomy-provider-stop-20261015.md"
DASHBOARD = ROOT / "docs/reverse/tomb5-progress-dashboard-re956-provider-pause-v1.html"

def test_documented_provider_stop_is_not_technical_progress():
    text = BLOCKER.read_text()
    for required in ("deleg_68f36480", "34.88", "Aucun replay", "integration=false", "production_patch=false", "18h45", "BLOCKED-008", "[x]", "[ ]"):
        assert required in text
    assert "13:32:47" in text and "13:33:22" in text

def test_dashboard_distinguishes_reviewed_milestone_from_stop():
    text = DASHBOARD.read_text()
    for required in ("RE956", "727a90d6", "refus fournisseur", "Aucun nouveau gain comportemental", "Pas de gameplay validé", "18h45", "BLOCKED-009"):
        assert required in text
    assert "<html lang=\"fr\">" in text

def test_local_links_resolve_without_private_evidence_exposure():
    for path in (BLOCKER, DASHBOARD):
        text = path.read_text()
        links = re.findall(r'href="([^"]+)"', text) if path.suffix == ".html" else re.findall(r'\]\(([^)]+)\)', text)
        assert links
        for link in links:
            assert not link.startswith(("http:", "https:", "/", "#"))
            assert (path.parent / link).resolve().is_file(), link
    html = DASHBOARD.read_text()
    assert "build/reverse" not in html and "<script" not in html
