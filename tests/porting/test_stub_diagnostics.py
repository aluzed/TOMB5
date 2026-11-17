"""Garde-fou sur les diagnostics des stubs appeles a chaque frame.

`UpdateFireSparks`, `UpdateGunShells`, `ProcessClosedDoors`,
`WadeSplash`, `PadSetActAlign`, etc. sont invoquees a chaque frame. Avec un
`UNIMPLEMENTED()` classique, chacune imprimait une ligne par frame : le log
devenait illisible (9 000 lignes pour 200 frames) et le printf coutait cher.
Elles utilisent desormais `UNIMPLEMENTED_ONCE()`, qui n'annonce l'absence
qu'une fois. Le comportement (no-op) est inchange.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

HOT_STUBS = [
    ("GAME/CONTROL.C", "void UpdateFireSparks()"),
    ("GAME/CONTROL.C", "void UpdateGunShells()"),
    ("GAME/CONTROL.C", "void UpdateRats()"),
    ("GAME/CONTROL.C", "void UpdateBats()"),
    ("GAME/CONTROL.C", "void KlaxonTremor()"),
    ("GAME/DOOR.C", "void ProcessClosedDoors()"),
    ("SPEC_PSXPC_N/FXTRIG.C",
     "void WadeSplash(struct ITEM_INFO* item, int water_height, int water_depth)"),
    ("EMULATOR/LIBPAD.C", "int PadSetActAlign(int unk00, unsigned char* unk01)"),
    ("EMULATOR/LIBPAD.C", "void PadStartCom()"),
]


def _body(text, signature):
    """Return the source of one function, up to its matching closing brace."""
    start = text.find(signature)
    assert start >= 0, signature
    brace = text.find("{", start)
    depth = 0
    for index in range(brace, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[brace:index + 1]
    raise AssertionError("unterminated function: " + signature)


def test_once_macro_is_defined_on_both_sides():
    assert "UNIMPLEMENTED_ONCE" in (ROOT / "SPEC_PSXPC_N" / "SPECIFIC.H").read_text(
        errors="ignore")
    assert "UNIMPLEMENTED_ONCE" in (ROOT / "EMULATOR" / "EMULATOR.H").read_text(
        errors="ignore")


def test_hot_stubs_only_report_once():
    cache = {}
    for path, signature in HOT_STUBS:
        if path not in cache:
            cache[path] = (ROOT / path).read_text(errors="ignore")
        body = _body(cache[path], signature)
        assert "UNIMPLEMENTED_ONCE();" in body, (path, signature)
        assert "UNIMPLEMENTED();" not in body, (path, signature)
