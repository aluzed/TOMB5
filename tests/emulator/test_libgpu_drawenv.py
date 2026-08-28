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


def test_put_disp_env_copies_environment_and_returns_source(tmp_path):
    source = tmp_path / "put_disp_env_harness.cpp"
    executable = tmp_path / "put_disp_env_harness"
    source.write_text(
        """
        #include <assert.h>
        #include <string.h>
        #include "LIBGPU.H"
        int main(void) {
            DISPENV expected = {};
            DISPENV received = {};
            expected.disp.x = 12;
            expected.disp.y = 34;
            expected.disp.w = 320;
            expected.disp.h = 240;
            expected.screen.x = -8;
            expected.screen.y = 16;
            expected.isrgb24 = 1;
            expected.isinter = 1;

            assert(PutDispEnv(&expected) == &expected);
            assert(GetDispEnv(&received) == &received);
            assert(memcmp(&received, &expected, sizeof(DISPENV)) == 0);
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


def test_parse_draw_move_copies_the_encoded_vram_rectangle(tmp_path):
    source = tmp_path / "parse_draw_move_harness.cpp"
    executable = tmp_path / "parse_draw_move_harness"
    source.write_text(
        """
        #include <assert.h>
        #include <stdint.h>
        #include "LIBGPU.H"

        extern void ParseDrawMove(DR_MOVE *move);

        static int calls = 0;
        static unsigned short *received_source = (unsigned short *)1;
        static int received_x = 0;
        static int received_y = 0;
        static int received_w = 0;
        static int received_h = 0;
        static int received_dst_x = 0;
        static int received_dst_y = 0;

        void Emulator_CopyVRAM(unsigned short *source, int x, int y, int w, int h,
                               int dst_x, int dst_y) {
            ++calls;
            received_source = source;
            received_x = x;
            received_y = y;
            received_w = w;
            received_h = h;
            received_dst_x = dst_x;
            received_dst_y = dst_y;
        }

        int main(void) {
            DR_MOVE move = {};
            RECT16 source = { 12, 34, 56, 78 };

            SetDrawMove(&move, &source, 90, 123);
            ParseDrawMove(&move);
            assert(calls == 1);
            assert(received_source == 0);
            assert(received_x == 12);
            assert(received_y == 34);
            assert(received_w == 56);
            assert(received_h == 78);
            assert(received_dst_x == 90);
            assert(received_dst_y == 123);
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


def test_put_draw_env_copies_environment_and_returns_source(tmp_path):
    source = tmp_path / "put_draw_env_harness.cpp"
    executable = tmp_path / "put_draw_env_harness"
    source.write_text(
        """
        #include <assert.h>
        #include <string.h>
        #include "LIBGPU.H"
        int main(void) {
            DRAWENV expected = {};
            DRAWENV received = {};
            expected.clip.x = 12;
            expected.clip.y = 34;
            expected.clip.w = 320;
            expected.clip.h = 240;
            expected.ofs[0] = -8;
            expected.ofs[1] = 16;
            expected.tpage = 10;
            expected.dtd = 1;
            expected.dfe = 1;

            assert(PutDrawEnv(&expected) == &expected);
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
