"""RE755: execute only the boxes slice of the real SETUP.C, synthetic RAM.

Requires g++ multilib and GDB with Python. Never run the incompletely linked
executable standalone: GDB stops before any loader body and audits the slice
before stepping it. No private assets, historical probes or copied loop.
"""
import json
import os
from pathlib import Path
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def boxes_binary(tmp_path_factory):
    directory = tmp_path_factory.mktemp("setup-boxes")
    harness = directory / "harness.cpp"
    harness.write_text('''#include "SETUP.H"
#include "BOX.H"
static_assert(sizeof(void*) == 4 && sizeof(long) == 4, "target ABI");
static_assert(sizeof(box_info) == 8, "box layout");
static_assert(sizeof(Level) == 228, "level layout");
Level fixture_level = {};
box_info fixture_boxes[6] = {};
box_info* boxes;
int number_boxes;
int fixture_last = BOX_LAST;
int fixture_blocked = BOX_BLOCKED;
int main() { LoadLevel(); return fixture_last + fixture_blocked; }
''')
    executable = directory / "host"
    command = ["g++", "-g", "-m32", "-O0", "-Wno-narrowing",
               "-ffunction-sections", "-fno-pie", "-no-pie",
               "-Wl,--gc-sections", "-Wl,--unresolved-symbols=ignore-all",
               "-DPSX_VERSION=1", "-DPSXPC_TEST=1", "-DNTSC_VERSION=1",
               "-DUSE_32_BIT_ADDR=1", "-DDEBUG_VERSION=0", "-DDISC_VERSION=1",
               "-IGAME", "-ISPEC_PSXPC_N", "-IEMULATOR", "-I/usr/include/SDL2",
               str(harness), "GAME/SETUP.C", "-o", str(executable)]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    (directory / "compile.json").write_text(json.dumps(command))
    (directory / "compile.log").write_text(result.stdout + result.stderr)
    lines = (ROOT / "GAME/SETUP.C").read_text().splitlines()
    def line(text):
        matches = [i + 1 for i, value in enumerate(lines) if value.strip() == text]
        assert len(matches) == 1
        return matches[0]
    return (directory, executable, line("number_boxes = level->numBoxes;"),
            line("camera.fixed = (struct OBJECT_VECTOR*)ptr;"), line("char* ptr = NULL;"))


@pytest.mark.parametrize("count,mask", [(0, 0), (1, 0), (1, 1),
                                        (4, 0), (4, 1), (4, 8), (4, 9)])
def test_boxes_endpoints_and_counter(boxes_binary, count, mask):
    directory, executable, start_line, stop_line, entry_line = boxes_binary
    result_file = directory / f"result-{count}-{mask}.json"
    script = directory / f"case-{count}-{mask}.py"
    # GDB's embedded Python needs only its standard library, not pytest.
    script.write_text(f'''
import gdb, json, re
try:
    gdb.execute("set pagination off")
    gdb.execute("set confirm off")
    gdb.execute("set disassembly-flavor intel")
    gdb.Breakpoint("GAME/SETUP.C:{entry_line}")
    gdb.execute("run")
    assert gdb.selected_frame().name() == "LoadLevel"
    def address(line):
        locations = gdb.decode_line("GAME/SETUP.C:" + str(line))[1]
        assert len(locations) == 1
        return int(locations[0].pc)
    start, stop = address({start_line}), address({stop_line})
    assert start < stop
    instructions = gdb.selected_frame().architecture().disassemble(start, stop - 1)
    pcs = {{int(ins["addr"]) for ins in instructions}}
    assert instructions[-1]["addr"] + instructions[-1]["length"] == stop
    assert sum(ins["length"] for ins in instructions) == stop-start
    # Fail closed before executing: no calls, returns, indirect or escaping jumps.
    branches = 0
    for ins in instructions:
        asm = ins["asm"].strip()
        mnemonic = asm.split()[0]
        assert mnemonic in {{"mov", "movzx", "movsx", "lea", "add", "sub", "and", "or", "test", "cmp", "nop", "shl"}} or mnemonic.startswith("j"), asm
        if mnemonic.startswith("j"):
            target = re.match(r"j\\w+\\s+(0x[0-9a-f]+)", asm)
            assert target and int(target[1], 16) in pcs | {{stop}}, asm
            branches += 1
    assert branches > 0
    gdb.execute("set variable level = &fixture_level")
    gdb.execute("set variable fixture_level.numBoxes = {count}")
    gdb.execute("set variable boxes = fixture_boxes")
    gdb.execute("set variable i = 37")
    gdb.execute("set variable number_boxes = -1")
    last = int(gdb.parse_and_eval("fixture_last"))
    blocked = int(gdb.parse_and_eval("fixture_blocked"))
    base = int(gdb.parse_and_eval("&fixture_boxes[0]"))
    inferior = gdb.selected_inferior()
    size = int(gdb.parse_and_eval("sizeof(fixture_boxes)"))
    inferior.write_memory(base, bytes((j*19+7)&255 for j in range(size)))
    for index in range({count}):
        value = 23 + index + (last if ({mask} >> index) & 1 else 0)
        gdb.execute("set variable fixture_boxes[%d].overlap_index = %d" % (index, value))
    # Adjacent record is deliberately sensitive to the erroneous last iteration.
    assert last & blocked == 0
    gdb.execute("set variable fixture_boxes[{count}].overlap_index = %d" % (last | 7))
    before = bytes(inferior.read_memory(base, size))
    expected = bytearray(before)
    field = int(gdb.parse_and_eval("&fixture_boxes[0].overlap_index")) - base
    stride = int(gdb.parse_and_eval("sizeof(box_info)"))
    for index in range({count}):
        offset = index * stride + field
        value = int.from_bytes(before[offset:offset+2], "little")
        if value & last:
            expected[offset:offset+2] = (value | blocked).to_bytes(2, "little")
    gdb.execute("set $pc = %d" % start)
    steps = 0
    while int(gdb.parse_and_eval("$pc")) != stop:
        assert int(gdb.parse_and_eval("$pc")) in pcs
        assert steps < 300
        gdb.execute("stepi", to_string=True)
        steps += 1
    actual = bytes(inferior.read_memory(base, size))
    output = {{"actual": list(actual), "expected": list(expected),
              "counter": int(gdb.parse_and_eval("i")),
              "number_boxes": int(gdb.parse_and_eval("number_boxes")),
              "steps": steps, "audited_instructions": len(instructions)}}
    gdb.execute("kill")
    with open({str(result_file)!r}, "w") as stream:
        json.dump(output, stream)
except Exception:
    import traceback
    traceback.print_exc()
    gdb.execute("quit 1")
''')
    run = subprocess.run(["gdb", "-q", "-nx", "-batch", str(executable),
                          "-ex", f"source {script}"], cwd=ROOT,
                         env={**os.environ, "DEBUGINFOD_URLS": ""},
                         capture_output=True, text=True, timeout=30)
    (directory / f"gdb-{count}-{mask}.log").write_text(run.stdout + run.stderr)
    assert run.returncode == 0, run.stdout + run.stderr
    data = json.loads(result_file.read_text())
    assert data["actual"] == data["expected"], "boxes endpoints / adjacent sentinel differ"
    assert data["counter"] == (37 if count == 0 else 0)
    assert data["number_boxes"] == count
