import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]


def test_get_draw_env_copies_the_active_environment_and_returns_destination(tmp_path):
    source = tmp_path / "get_draw_env_harness.cpp"
    executable = tmp_path / "get_draw_env_harness"
    source.write_text(
        """
        #include <assert.h>
        #include <string.h>
        #include "LIBGPU.H"
        int main(void) {
            DRAWENV expected = {};
            DRAWENV received = {};
            expected.clip.x = 10;
            expected.clip.y = 20;
            expected.clip.w = 30;
            expected.clip.h = 40;
            expected.ofs[0] = -3;
            expected.ofs[1] = 9;
            expected.isbg = 1;
            expected.dtd = 1;
            activeDrawEnv = expected;
            assert(GetDrawEnv(&received) == &received);
            assert(memcmp(&received, &expected, sizeof(DRAWENV)) == 0);
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
