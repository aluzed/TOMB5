"""Public contract for the configurable keyboard/gamepad keymap.

Compiles the pure INPUTMAP module with a small host harness; no game data,
emulator runtime or controller is required.
"""
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HARNESS = ROOT / "tests/porting/inputmap_harness.cpp"
MODULE = ROOT / "EMULATOR/INPUTMAP.C"


@pytest.fixture(scope="module")
def harness(tmp_path_factory):
    out = tmp_path_factory.mktemp("inputmap")
    exe = out / "inputmap_harness"
    command = [
        "g++", "-std=c++11", "-O0", "-DPSXPC_TEST=1",
        f"-I{ROOT/'EMULATOR'}", f"-I{ROOT/'GAME'}", f"-I{ROOT/'SPEC_PSXPC_N'}",
        "-I/usr/include/SDL2", str(HARNESS), str(MODULE), "-o", str(exe),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return exe


def run(harness, *args):
    return subprocess.run([str(harness), *map(str, args)],
                          capture_output=True, text=True)


def write(tmp_path, text):
    path = tmp_path / "input.cfg"
    path.write_text(text, encoding="utf-8")
    return path


def eval(harness, path, *tokens):
    result = run(harness, "eval", path, *tokens)
    assert result.returncode == 0, result.stdout + result.stderr
    values = {}
    for line in result.stdout.splitlines():
        key, _, value = line.partition("=")
        values[key] = value
    return values


def test_defaults_are_saved_with_two_columns_and_reload(harness, tmp_path):
    path = tmp_path / "defaults.cfg"
    result = run(harness, "defaults-save", path)
    assert result.returncode == 0, result.stdout + result.stderr
    text = path.read_text()
    for section in ("[devices]", "[gameplay]", "[keyboard]", "[gamepad]"):
        assert section in text
    for section in ("[keyboard]", "[gamepad]"):
        block = text.split(section, 1)[1].split("\n[", 1)[0]
        for action in ("forward", "back", "left", "right", "action", "jump",
                       "draw", "roll", "look", "duck", "walk", "sprint", "start", "select"):
            lines = [line for line in block.splitlines() if line.startswith(action)]
            assert len(lines) == 1, (section, action)
            assert lines[0].count(",") == 1, lines[0]
    values = eval(harness, path, "K:W")
    assert values["actions"] == "forward"
    assert values["pad"] == "FFEF"
    assert values["loaded"] == "1"


def test_save_is_deterministic_and_reloadable(harness, tmp_path):
    one = tmp_path / "one.cfg"
    two = tmp_path / "two.cfg"
    assert run(harness, "defaults-save", one).returncode == 0
    assert run(harness, "defaults-save", two).returncode == 0
    assert one.read_bytes() == two.read_bytes()


def test_keyboard_double_bind_accepts_either_slot(harness, tmp_path):
    path = write(tmp_path, """
[keyboard]
forward = W, UP
back = S, DOWN
""")
    assert eval(harness, path, "K:W")["actions"] == "forward"
    assert eval(harness, path, "K:UP")["actions"] == "forward"
    assert eval(harness, path, "K:S")["actions"] == "back"
    assert eval(harness, path, "K:DOWN")["actions"] == "back"
    assert eval(harness, path, "K:Q")["actions"] == ""


def test_gamepad_double_bind_button_and_axis(harness, tmp_path):
    path = write(tmp_path, """
[devices]
axis_deadzone = 0.50

[gamepad]
forward = DPAD_UP, LEFTY-
left = DPAD_LEFT, LEFTX-
""")
    assert eval(harness, path, "P:DPAD_UP")["actions"] == "forward"
    assert eval(harness, path, "A:LEFTY-:-0.9")["actions"] == "forward"
    assert eval(harness, path, "A:LEFTY-:-0.2")["actions"] == ""
    assert eval(harness, path, "P:DPAD_LEFT")["actions"] == "left"
    assert eval(harness, path, "A:LEFTX-:-0.8")["actions"] == "left"


def test_axis_deadzone_is_honoured(harness, tmp_path):
    path = write(tmp_path, """
[devices]
axis_deadzone = 0.80

[gamepad]
forward = LEFTY-
""")
    assert eval(harness, path, "A:LEFTY-:-0.70")["actions"] == ""
    assert eval(harness, path, "A:LEFTY-:-0.90")["actions"] == "forward"


def test_trigger_axes(harness, tmp_path):
    path = write(tmp_path, """
[devices]
axis_deadzone = 0.50

[gamepad]
duck = TRIGGERLEFT
sprint = RT
""")
    assert eval(harness, path, "A:TRIGGERLEFT:0.90")["actions"] == "duck"
    assert eval(harness, path, "A:TRIGGERLEFT:0.40")["actions"] == ""
    assert eval(harness, path, "A:TRIGGERRIGHT:0.90")["actions"] == "sprint"


def test_device_selection_disables_a_device(harness, tmp_path):
    keyboard_off = write(tmp_path, """
[devices]
keyboard = 0
gamepad = 1

[keyboard]
forward = W, UP

[gamepad]
forward = DPAD_UP, NONE
""")
    assert eval(harness, keyboard_off, "K:W")["actions"] == ""
    assert eval(harness, keyboard_off, "P:DPAD_UP")["actions"] == "forward"

    gamepad_off = write(tmp_path, """
[devices]
keyboard = 1
gamepad = 0

[keyboard]
action = C, NONE

[gamepad]
action = A, NONE
""")
    assert eval(harness, gamepad_off, "K:C")["actions"] == "action"
    assert eval(harness, gamepad_off, "P:A")["actions"] == ""


def test_start_and_select_emit_menu_pad_bits(harness, tmp_path):
    path = write(tmp_path, """
[keyboard]
start = RETURN, NONE
select = SPACE, NONE
""")
    start = eval(harness, path, "K:RETURN")
    assert start["actions"] == ""
    assert start["pad"] == "FFF7"
    select = eval(harness, path, "K:SPACE")
    assert select["actions"] == ""
    assert select["pad"] == "FFFE"


def test_use_control_option_flag_is_reported(harness, tmp_path):
    path = write(tmp_path, """
[gameplay]
use_control_option = 1
""")
    values = eval(harness, path, "K:W")
    assert values["use_control_option"] == "1"


def test_comments_case_and_whitespace(harness, tmp_path):
    path = write(tmp_path, """
# leading comment
[KEYBOARD]
  Forward = w ,  up   ; trailing comment
[Gamepad]
  action = a , none
""")
    assert eval(harness, path, "K:W")["actions"] == "forward"
    assert eval(harness, path, "P:A")["actions"] == "action"


def test_invalid_key_is_reported_with_line(harness, tmp_path):
    path = write(tmp_path, """
[keyboard]
forward = W, NOT_A_KEY
""")
    result = run(harness, "error", path)
    assert result.returncode == 0
    assert "loaded=-1" in result.stdout
    assert "input.cfg:3" in result.stdout
    assert "unknown keyboard key" in result.stdout


def test_too_many_bindings_are_rejected(harness, tmp_path):
    path = write(tmp_path, """
[keyboard]
forward = W, UP, Q
""")
    result = run(harness, "error", path)
    assert "loaded=-1" in result.stdout
    assert "more than 2 bindings" in result.stdout


def test_unknown_action_and_section_are_rejected(harness, tmp_path):
    action = write(tmp_path, """
[keyboard]
fly = W, UP
""")
    result = run(harness, "error", action)
    assert "unknown action 'fly'" in result.stdout

    section = write(tmp_path, """
[joystick]
forward = W, UP
""")
    result = run(harness, "error", section)
    assert "unknown section [joystick]" in result.stdout


def test_invalid_gamepad_name_and_guid(harness, tmp_path):
    button = write(tmp_path, """
[gamepad]
jump = BUTTON_X, NONE
""")
    result = run(harness, "error", button)
    assert "unknown gamepad control 'BUTTON_X'" in result.stdout

    guid = write(tmp_path, """
[devices]
gamepad_guid = not-a-guid!
""")
    result = run(harness, "error", guid)
    assert "gamepad_guid" in result.stdout


def test_gamepad_index_bounds(harness, tmp_path):
    valid = write(tmp_path, """
[devices]
gamepad_index = -1
""")
    assert eval(harness, valid, "K:W")["index"] == "-1"

    invalid = write(tmp_path, """
[devices]
gamepad_index = -2
""")
    result = run(harness, "error", invalid)
    assert "gamepad_index" in result.stdout


def test_empty_slots_are_none(harness, tmp_path):
    path = write(tmp_path, """
[keyboard]
forward = , NONE
action = NONE,
""")
    assert eval(harness, path, "K:W")["actions"] == ""
    assert eval(harness, path, "K:C")["actions"] == ""


def test_missing_file_uses_defaults(harness, tmp_path):
    values = eval(harness, tmp_path / "missing.cfg", "K:W")
    assert values["loaded"] == "0"
    assert values["actions"] == "forward"
