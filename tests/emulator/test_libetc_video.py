import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]


def test_set_video_mode_persists_the_requested_display_standard(tmp_path):
    source = tmp_path / "video_mode_harness.cpp"
    executable = tmp_path / "video_mode_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBETC.H"

        int main(void) {
            assert(GetVideoMode() == MODE_NTSC);
            assert(SetVideoMode(MODE_PAL) == MODE_PAL);
            assert(GetVideoMode() == MODE_PAL);
            assert(SetVideoMode(MODE_NTSC) == MODE_NTSC);
            assert(GetVideoMode() == MODE_NTSC);
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
