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


def test_save_level_data_active_item_writes_control_word_before_payload():
    body = _function_body("SaveLevelData")
    active = body.index("word = 0x8000;")
    header_write = body.index("Write(&word, 2);", active)
    position_payload = body.index("if (obj->save_position)", active)

    assert active < header_write < position_payload


def test_save_level_data_save_flags_writes_packed_low_flags_and_active_bits():
    body = _function_body("SaveLevelData")
    save_flags_block = body[body.index("if (obj->save_flags)"):]

    assert "int flags = (unsigned short)item->flags" in save_flags_block
    assert "(item->ai_bits << 9)" in save_flags_block
    assert "(item->really_active << 14)" in save_flags_block
    assert "Write(&flags, 4);" in save_flags_block
