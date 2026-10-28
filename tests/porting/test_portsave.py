"""Public contract for the port-level quick save/load serialiser.

Compiles GAME/PORTSAVE.C with a host harness that stubs the game services it
calls.  No game data, level or emulator runtime is required.
"""
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HARNESS = ROOT / "tests/porting/portsave_harness.cpp"
MODULE = ROOT / "GAME/PORTSAVE.C"
FLAGS = [
    "-std=c++11", "-O0", "-DPSX_VERSION=1", "-DPSXPC_TEST=1",
    "-DUSE_32_BIT_ADDR=1", "-DDISC_VERSION=1", "-DDEBUG_VERSION=0",
    "-DBETA_VERSION=0", "-DNTSC_VERSION=1", "-DRELOC=0",
    f"-I{ROOT/'GAME'}", f"-I{ROOT/'SPEC_PSXPC_N'}", f"-I{ROOT/'EMULATOR'}",
]


@pytest.fixture(scope="module")
def harness(tmp_path_factory):
    out = tmp_path_factory.mktemp("portsave")
    exe = out / "portsave_harness"
    result = subprocess.run(
        ["g++", *FLAGS, str(HARNESS), str(MODULE), "-o", str(exe)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    return exe


def test_round_trip_applies_position_and_rejects_corruption(harness, tmp_path):
    save = tmp_path / "TOMB5.SAV"
    result = subprocess.run([str(harness), str(save)],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "[SAVE] wrote" in result.stdout
    assert "[SAVE] loaded" in result.stdout
    assert "[SAVE] applied saved position" in result.stdout
    assert "checksum mismatch" in result.stdout
    assert "invalid save header" in result.stdout
    assert not save.exists()
