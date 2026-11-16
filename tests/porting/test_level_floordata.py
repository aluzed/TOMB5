"""Tests for the offline level decoder (scripts/porting/decode_level_floordata.py).

The decoder rebuilds a level's items, per-cell floor info, triggers and room
portals from a gdb arena dump.  Its selftest builds a synthetic level in
memory, so the whole decoding path is covered without the game running.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "scripts" / "porting" / "decode_level_floordata.py"


def test_decoder_selftest_passes():
    proc = subprocess.run(
        [sys.executable, "-B", str(TOOL), "--selftest"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "selftest OK" in proc.stdout


def test_decoder_rejects_missing_arguments():
    proc = subprocess.run(
        [sys.executable, "-B", str(TOOL), "dump"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert proc.returncode != 0
