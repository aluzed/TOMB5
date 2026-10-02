"""Synthetic OpenThatDoor contract on the complete real TU, i386 only.

No target payload, private snapshots or build artifacts are test inputs.
Disjoint valid buffers; primary mesh requires third; five LOT slots.
This regression intentionally fails until independently accepted integration.
"""
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/reverse/fixtures/re800/openthatdoor.cpp"
OUTPUT = ROOT / "build/reverse/autonomy-20261002/re800-public-contract"


class OpenThatDoorContract(unittest.TestCase):
    def test_synthetic_3328_matrix_actual_translation_unit(self):
        self.run_contract(ROOT / "GAME/DOOR.C")

    def run_contract(self, source):
        compiler = shutil.which("c++")
        if not compiler:
            self.skipTest("Prerequisite unavailable: C++ compiler")
        OUTPUT.mkdir(parents=True, exist_ok=True)
        out = Path(tempfile.mkdtemp(prefix="contract-", dir=OUTPUT))
        ledger = []

        def run(argv, name):
            result = subprocess.run(
                [str(x) for x in argv], cwd=ROOT, capture_output=True, text=True,
                timeout=90, env={**os.environ,
                                 "ASAN_OPTIONS": "detect_leaks=0:halt_on_error=1",
                                 "UBSAN_OPTIONS": "halt_on_error=1:print_stacktrace=1"})
            (out / (name + ".stdout")).write_text(result.stdout)
            (out / (name + ".stderr")).write_text(result.stderr)
            ledger.append({"name": name, "argv": [str(x) for x in argv],
                           "cwd": str(ROOT), "exit": result.returncode})
            (out / "commands.json").write_text(json.dumps(ledger, indent=2))
            return result

        # Discover installed headers, falling back to existing local dependency
        # trees without downloading anything or requiring a particular timestamp.
        glew = next((p for p in (Path("/usr/include"), Path("/usr/local/include"))
                     if (p / "GL/glew.h").is_file()), None)
        if glew is None:
            headers = sorted((ROOT / "build").glob("**/dependency/glew-*/include/GL/glew.h"))
            if headers:
                glew = headers[0].parents[1]
        if glew is None:
            self.skipTest("Prerequisite unavailable: GLEW headers (system or existing build dependency)")
        pkgconfig = shutil.which("pkg-config")
        sdl_flags = []
        if pkgconfig:
            result = run([pkgconfig, "--cflags", "sdl2"], "sdl-discovery")
            if result.returncode == 0:
                sdl_flags = shlex.split(result.stdout)
        if not sdl_flags:
            sdl = next((p for p in (Path("/usr/include/SDL2"), Path("/usr/local/include/SDL2"))
                        if (p / "SDL.h").is_file()), None)
            if sdl is None:
                self.skipTest("Prerequisite unavailable: SDL2 development headers")
            sdl_flags = ["-I", str(sdl)]
        flags = [compiler, "-m32", "-std=c++11", "-O0", "-fpermissive",
                 "-Wno-narrowing", "-ffunction-sections", "-fdata-sections",
                 "-fno-pie", "-no-pie", "-fno-omit-frame-pointer",
                 "-DPSX_VERSION=1", "-DPSXPC_TEST=1", "-DUSE_32_BIT_ADDR=1",
                 "-I", str(ROOT / "SPEC_PSXPC_N"), "-I", str(ROOT / "GAME"),
                 "-I", str(ROOT / "EMULATOR"), "-I", str(glew), *sdl_flags]
        probe = out / "prerequisite.cpp"
        probe.write_text('#include <cstdio>\n#include <GL/glew.h>\n#include <SDL.h>\n'
                         'static_assert(sizeof(void*) == 4, "i386");\nint main(){return 0;}\n')
        for mode, sanitizer in (
                ("normal", []),
                ("asan-ubsan", ["-fsanitize=address,undefined", "-fno-sanitize-recover=all"])):
            with self.subTest(mode=mode):
                probe_exe = out / (mode + "-prerequisite")
                prerequisite = run([*flags, *sanitizer, probe, "-o", probe_exe], mode + "-prerequisite-build")
                if prerequisite.returncode:
                    self.skipTest("Prerequisite unavailable: i386 C++/headers/sanitizer toolchain; "
                                  + prerequisite.stderr + " ledger=" + str(out))
                prerequisite = run([probe_exe], mode + "-prerequisite-run")
                if prerequisite.returncode:
                    self.skipTest("Prerequisite unavailable: i386 runtime; "
                                  + prerequisite.stderr + " ledger=" + str(out))
                executable = out / mode
                built = run([*flags, *sanitizer, "-x", "c++", source,
                             FIXTURE, "-Wl,--gc-sections", "-o", executable], mode + "-build")
                self.assertEqual(built.returncode, 0, "Actual TU build failed (not a skip):\n"
                                 + built.stderr + "\nledger=" + str(out))
                result = run([executable], mode + "-run")
                self.assertEqual(result.returncode, 0, "Behavioral contract failed:\n"
                                 + result.stdout + result.stderr + "\nledger=" + str(out))
                self.assertIn("SUMMARY cases=3328 failures=0", result.stdout)
                self.assertNotIn("runtime error:", result.stderr)
                self.assertNotIn("ERROR: AddressSanitizer", result.stderr)


if __name__ == "__main__":
    unittest.main()
