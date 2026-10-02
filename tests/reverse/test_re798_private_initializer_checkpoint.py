"""RE798 documents private, reviewed proof without claiming production integration."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-798-private-generic-door-initializer.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'


def test_private_initializer_checkpoint_has_no_activation_claim():
    assert STORY.exists(), 'RED: reviewed private initializer checkpoint missing'
    text = STORY.read_text()
    for token in ('## Tracker', '- [x]', '- [ ]', '32/32', 'InDrawRoom',
                  'draw_room', 'link', '16/32', 'ASan', 'UBSan', 'privé',
                  'pas de GREEN global', 'RE-799', 'ObjectObjects non activé'):
        assert token in text, token
    assert 'eebc7730a0c0f3bb04716c50ed6e172a661f7876c7a35a5d9e2668ec0da0744d' in text
    assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|data:image|```(?:asm|mips)\b', text)


def test_dashboard_names_private_checkpoint_without_new_section():
    text = DASH.read_text()
    section = text.split('<section id="re794">', 1)[1].split('<!-- end re794 -->', 1)[0]
    assert 'RE-798 — Prototype privé' in section
    assert 'Initialiseur non intégré' in section
    assert 'RE-799' in section
    assert text.count('<section id="re794">') == 1


def test_private_story_pins_the_delivered_source_baseline():
    assert STORY.exists(), 'RED: private checkpoint missing'
    assert '4fd35a2eb49a68ae7c79c7cd6e27955d3e065d1850c1216276c400086fd8c055' in STORY.read_text()
