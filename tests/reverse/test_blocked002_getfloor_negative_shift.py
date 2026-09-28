"""BLOCKED-002 GetFloor: negative-shift UBSan RED on pinned baseline, GREEN on current."""

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "tests/reverse/fixtures/re781/run_test.py"
OUT = ROOT / "build/reverse/blocked002-public-tests"
BASELINE = "929a8f78ebec66468864cb1082c1b705d9992a94"
UBSAN = "GETSTUFF.C:338:27: runtime error: left shift of negative value -32"


def _run(source_dir, tag):
    out = Path(tempfile.mkdtemp(prefix=f"b002-{tag}-", dir=OUT)) / "run"
    argv = [
        sys.executable,
        "-B",
        str(RUN),
        "--root",
        str(ROOT),
        "--source",
        str(source_dir / "GETSTUFF.C"),
        "--output",
        str(out),
        "--ubsan",
    ]
    return subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, timeout=240)


def test_blocked002_getfloor_negative_shift():
    OUT.mkdir(parents=True, exist_ok=True)
    baseline_dir = Path(tempfile.mkdtemp(prefix="b002-baseline-src-", dir=OUT))
    baseline = subprocess.run(
        ["git", "show", f"{BASELINE}:SPEC_PSXPC_N/GETSTUFF.C"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    (baseline_dir / "GETSTUFF.C").write_text(baseline)

    red = _run(baseline_dir, "red")
    assert red.returncode == 1, f"RED rc={red.returncode}\n{red.stdout}{red.stderr}"
    assert UBSAN in red.stderr, red.stderr

    green = _run(ROOT / "SPEC_PSXPC_N", "green")
    assert green.returncode == 0, (
        f"GREEN rc={green.returncode}\n{green.stdout}{green.stderr}"
    )
    assert "SUMMARY checks=288 failures=0" in green.stdout, green.stdout
    assert "runtime error" not in green.stdout and "runtime error" not in green.stderr
