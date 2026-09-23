"""Public documentary contract for the bounded September 23 runtime milestone.

Never reads the proprietary CUE/BIN, executable, captures or private runtime bundle.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / 'docs/porting/runtime-20260923.md'
INDEX = ROOT / 'docs/porting/README.md'


def test_fresh_runtime_note_keeps_build_input_output_and_limits_separate():
    assert NOTE.is_file(), 'RED documentaire : nouvelle note runtime absente'
    note = NOTE.read_text(encoding='utf-8')
    for term in (
        '23 septembre 2026', 'cd95ce52', 'ELF32', 'GLEW',
        'build exit 0', 'XTest', 'WM_DELETE_WINDOW', 'application exit 0',
        '29 s', '81 s', '92 s', '104/107 s', '112 s', '117 s',
        'vue noire', 'LookCamera', 'stub', 'aucun correctif source',
        'comparaison de pixels', 'sans inspection visuelle directe',
        'aucune équivalence cible', 'PORT-004', 'In progress',
        'build/reverse/runtime-20260923-1935/',
        '## Tracker', '## Handoff', '- [x]', '- [ ]',
    ):
        assert term in note, term
    assert 'camera-foundations.md' in note
    assert not re.search(r'0x[0-9a-fA-F]+|\b[0-9a-fA-F]{64}\b|<img\b|data:image|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', note)
    assert not re.search(r'(?im)^\s*MEDIA:|!\[|\.png\)', note)


def test_existing_porting_history_remains_generated_and_unchanged():
    import importlib.util
    import json

    spec = importlib.util.spec_from_file_location('port_backlog', ROOT / 'scripts/porting/render_backlog.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    data = json.loads((ROOT / 'docs/porting/backlog.json').read_text(encoding='utf-8'))
    assert INDEX.read_text(encoding='utf-8') == module.render(data)['README.md']
