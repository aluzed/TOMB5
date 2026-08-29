import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]


def test_stop_callback_clears_the_vsync_callback(tmp_path):
    source = tmp_path / "stop_callback_harness.cpp"
    executable = tmp_path / "stop_callback_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBETC.H"

        extern void (*vsync_callback)(void);

        static void callback(void) {}

        int main(void) {
            VSyncCallback(callback);
            assert(vsync_callback == callback);
            assert(StopCallback() == 0);
            assert(vsync_callback == 0);
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
            str(REPO / "EMULATOR" / "LIBETC.C"),
            "-o",
            str(executable),
        ],
        check=True,
        cwd=REPO,
    )
    subprocess.run([str(executable)], check=True)
