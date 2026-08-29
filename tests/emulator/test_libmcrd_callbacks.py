import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]


def test_memcard_callback_replaces_and_returns_the_previous_callback(tmp_path):
    source = tmp_path / "memcard_callback_harness.cpp"
    executable = tmp_path / "memcard_callback_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBMCRD.H"

        static void first_callback(long, long) {}
        static void second_callback(long, long) {}

        int main(void) {
            assert(MemCardCallback(first_callback) == 0);
            assert(MemCardCallback(second_callback) == first_callback);
            assert(MemCardCallback(0) == second_callback);
            return 0;
        }
        """
    )
    subprocess.run(
        [
            "g++",
            "-ffunction-sections",
            "-fdata-sections",
            "-Wl,--gc-sections",
            "-I/usr/include/SDL2",
            "-I",
            str(REPO / "EMULATOR"),
            str(source),
            str(REPO / "EMULATOR" / "LIBMCRD.C"),
            "-o",
            str(executable),
        ],
        check=True,
        cwd=REPO,
    )
    subprocess.run([str(executable)], check=True)
