"""Tests for the offline level tools.

`scripts/porting/decode_level_floordata.py` rebuilds a level's items,
per-cell floor info, triggers and room portals from a gdb arena dump;
`scripts/porting/render_level_map.py` renders that data as a top-down PNG.
The decoder ships a synthetic level builder (`--emit-selftest`) so both
tools can be exercised without the game or level data.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECODER = ROOT / "scripts" / "porting" / "decode_level_floordata.py"
RENDERER = ROOT / "scripts" / "porting" / "render_level_map.py"


def run(*args):
    return subprocess.run([sys.executable, "-B", *args],
                          capture_output=True, text=True, cwd=str(ROOT))


def test_decoder_selftest_passes():
    proc = run(str(DECODER), "--selftest")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "selftest OK" in proc.stdout


def test_decoder_rejects_missing_arguments():
    proc = run(str(DECODER), "dump")
    assert proc.returncode != 0


def test_map_renderer_works_on_the_synthetic_level(tmp_path):
    emit = run(str(DECODER), "--emit-selftest", str(tmp_path))
    assert emit.returncode == 0, emit.stdout + emit.stderr

    # "<dir> arena.bin items.bin 0xROOM 0xFLOOR N"
    parts = emit.stdout.split()
    room_ptr, floor_ptr, rooms = parts[-3], parts[-2], parts[-1]

    out = tmp_path / "map.png"
    proc = run(str(RENDERER),
               "--arena", str(tmp_path / "arena.bin"),
               "--items", str(tmp_path / "items.bin"),
               "--room-ptr", room_ptr,
               "--floor-ptr", floor_ptr,
               "--rooms", rooms,
               "--out", str(out))
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert out.exists()
    assert out.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
