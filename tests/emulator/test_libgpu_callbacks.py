import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]


def test_draw_sync_callback_returns_the_callback_it_replaces(tmp_path):
    source = tmp_path / "draw_sync_callback_harness.cpp"
    executable = tmp_path / "draw_sync_callback_harness"
    source.write_text(
        """
        #include <assert.h>
        #include <stdint.h>
        #include "LIBGPU.H"

        static void first(void) {}
        static void second(void) {}

        int main(void) {
            assert(DrawSyncCallback(first) == 0);
            assert((uintptr_t)DrawSyncCallback(second) == (uintptr_t)first);
            assert((uintptr_t)DrawSyncCallback(0) == (uintptr_t)second);
            return 0;
        }
        """
    )
    subprocess.run(
        [
            "g++",
            "-Wno-narrowing",
            "-DUSE_32_BIT_ADDR",
            "-ffunction-sections",
            "-fdata-sections",
            "-Wl,--gc-sections",
            "-I/usr/include/SDL2",
            "-I",
            str(REPO / "EMULATOR"),
            str(source),
            str(REPO / "EMULATOR" / "LIBGPU.C"),
            "-o",
            str(executable),
        ],
        check=True,
        cwd=REPO,
    )
    subprocess.run([str(executable)], check=True)
