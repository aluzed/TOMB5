from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "GAME" / "SAVEGAME.C"


def _function_body(name: str) -> str:
    text = SOURCE.read_text(encoding="utf-8")
    signature = f"void {name}(int FullSave)"
    start = text.index(signature)
    brace = text.index("{", start)
    depth = 0
    for pos in range(brace, len(text)):
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
            if depth == 0:
                return text[brace + 1:pos]
    raise AssertionError(f"function not closed: {name}")


def test_save_level_data_has_no_psx_unimplemented_fallback():
    body = _function_body("SaveLevelData")

    assert "// todo check for psx" not in body
    assert "UNIMPLEMENTED();" not in body


def test_save_level_data_is_not_hidden_behind_pc_version_only():
    body = _function_body("SaveLevelData")

    assert "#if PC_VERSION" not in body
    assert "#else" not in body
