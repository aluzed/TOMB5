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


def test_parse_line_f3_emits_two_flat_line_segments(tmp_path):
    source = tmp_path / "parse_line_f3_harness.cpp"
    executable = tmp_path / "parse_line_f3_harness"
    source.write_text(
        """
        #include <assert.h>
        #include <stdint.h>
        #include "LIBGPU.H"
        #include "EMULATOR.H"

        extern void ParseLineF3(LINE_F3 *line, bool semiTransparent);
        extern int g_vertexIndex;
        extern int g_splitIndex;
        struct TestVertexBufferSplit {
            TextureID textureId;
            unsigned short vIndex;
            unsigned short vCount;
            BlendMode blendMode;
            TexFormat texFormat;
        };
        extern TestVertexBufferSplit g_splits[];
        extern DRAWENV activeDrawEnv;
        TextureID whiteTexture = (TextureID)1;
        TextureID vramTexture = {};
        static int line_calls = 0;
        static short starts[2][2];
        static short ends[2][2];
        static unsigned char colours[2][6];

        void Emulator_GenerateLineArray(Vertex *, short *start, short *end) {
            starts[line_calls][0] = start[0];
            starts[line_calls][1] = start[1];
            ends[line_calls][0] = end[0];
            ends[line_calls][1] = end[1];
            ++line_calls;
        }
        void Emulator_GenerateTexcoordArrayLineZero(Vertex *, unsigned char) {}
        void Emulator_GenerateColourArrayLine(Vertex *, unsigned char *first, unsigned char *second) {
            colours[line_calls - 1][0] = first[0];
            colours[line_calls - 1][1] = first[1];
            colours[line_calls - 1][2] = first[2];
            colours[line_calls - 1][3] = second[0];
            colours[line_calls - 1][4] = second[1];
            colours[line_calls - 1][5] = second[2];
        }

        int main(void) {
            LINE_F3 line = {};
            SetLineF3(&line);
            setXY3(&line, 10, 20, 30, 40, 50, 60);
            setRGB0(&line, 1, 2, 3);

            g_vertexIndex = 0;
            g_splitIndex = 0;
            activeDrawEnv.tpage = getTPage(0, 2, 0, 0);
            ParseLineF3(&line, true);
            assert(line_calls == 2);
            assert(starts[0][0] == 10 && starts[0][1] == 20);
            assert(ends[0][0] == 30 && ends[0][1] == 40);
            assert(starts[1][0] == 30 && starts[1][1] == 40);
            assert(ends[1][0] == 50 && ends[1][1] == 60);
            for (int i = 0; i < 2; ++i) {
                for (int component = 0; component < 6; component += 3) {
                    assert(colours[i][component] == 1);
                    assert(colours[i][component + 1] == 2);
                    assert(colours[i][component + 2] == 3);
                }
            }
            assert(g_splitIndex == 1);
            assert(g_splits[1].blendMode == BM_SUBTRACT);
            assert(g_vertexIndex == 12);
            return 0;
        }
        """
    )
    subprocess.run(
        [
            "g++", "-Wno-narrowing", "-DUSE_32_BIT_ADDR", "-ffunction-sections",
            "-fdata-sections", "-Wl,--gc-sections", "-I/usr/include/SDL2", "-I",
            str(REPO / "EMULATOR"), str(source), str(REPO / "EMULATOR" / "LIBGPU.C"),
            "-o", str(executable),
        ], check=True, cwd=REPO,
    )
    subprocess.run([str(executable)], check=True)


def test_parse_line_g3_emits_two_gouraud_line_segments(tmp_path):
    source = tmp_path / "parse_line_g3_harness.cpp"
    executable = tmp_path / "parse_line_g3_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBGPU.H"
        #include "EMULATOR.H"

        extern void ParseLineG3(LINE_G3 *line, bool semiTransparent);
        extern int g_vertexIndex;
        extern int g_splitIndex;
        struct TestVertexBufferSplit {
            TextureID textureId;
            unsigned short vIndex;
            unsigned short vCount;
            BlendMode blendMode;
            TexFormat texFormat;
        };
        extern TestVertexBufferSplit g_splits[];
        extern DRAWENV activeDrawEnv;
        TextureID whiteTexture = (TextureID)1;
        TextureID vramTexture = {};
        static int line_calls = 0;
        static short starts[2][2];
        static short ends[2][2];
        static unsigned char colours[2][6];

        void Emulator_GenerateLineArray(Vertex *, short *start, short *end) {
            starts[line_calls][0] = start[0]; starts[line_calls][1] = start[1];
            ends[line_calls][0] = end[0]; ends[line_calls][1] = end[1];
            ++line_calls;
        }
        void Emulator_GenerateTexcoordArrayLineZero(Vertex *, unsigned char) {}
        void Emulator_GenerateColourArrayLine(Vertex *, unsigned char *first, unsigned char *second) {
            colours[line_calls - 1][0] = first[0]; colours[line_calls - 1][1] = first[1];
            colours[line_calls - 1][2] = first[2]; colours[line_calls - 1][3] = second[0];
            colours[line_calls - 1][4] = second[1]; colours[line_calls - 1][5] = second[2];
        }

        int main(void) {
            LINE_G3 line = {};
            line.x0 = 10; line.y0 = 20; line.x1 = 30; line.y1 = 40; line.x2 = 50; line.y2 = 60;
            line.r0 = 1; line.g0 = 2; line.b0 = 3;
            line.r1 = 4; line.g1 = 5; line.b1 = 6;
            line.r2 = 7; line.g2 = 8; line.b2 = 9;
            g_vertexIndex = 0; g_splitIndex = 0;
            activeDrawEnv.tpage = getTPage(0, 0, 0, 0);

            ParseLineG3(&line, false);

            assert(line_calls == 2);
            assert(starts[0][0] == 10 && starts[0][1] == 20);
            assert(ends[0][0] == 30 && ends[0][1] == 40);
            assert(starts[1][0] == 30 && starts[1][1] == 40);
            assert(ends[1][0] == 50 && ends[1][1] == 60);
            const unsigned char expected[2][6] = {{1, 2, 3, 4, 5, 6}, {4, 5, 6, 7, 8, 9}};
            for (int i = 0; i < 2; ++i)
                for (int component = 0; component < 6; ++component)
                    assert(colours[i][component] == expected[i][component]);
            assert(g_splitIndex == 1);
            assert(g_splits[1].blendMode == BM_NONE);
            assert(g_vertexIndex == 12);
            return 0;
        }
        """
    )
    subprocess.run(
        [
            "g++", "-Wno-narrowing", "-DUSE_32_BIT_ADDR", "-ffunction-sections",
            "-fdata-sections", "-Wl,--gc-sections", "-I/usr/include/SDL2", "-I",
            str(REPO / "EMULATOR"), str(source), str(REPO / "EMULATOR" / "LIBGPU.C"),
            "-o", str(executable),
        ], check=True, cwd=REPO,
    )
    subprocess.run([str(executable)], check=True)


def test_parse_line_f4_emits_three_flat_line_segments(tmp_path):
    source = tmp_path / "parse_line_f4_harness.cpp"
    executable = tmp_path / "parse_line_f4_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBGPU.H"
        #include "EMULATOR.H"

        extern void ParseLineF4(LINE_F4 *line, bool semiTransparent);
        extern int g_vertexIndex;
        extern int g_splitIndex;
        struct TestVertexBufferSplit {
            TextureID textureId;
            unsigned short vIndex;
            unsigned short vCount;
            BlendMode blendMode;
            TexFormat texFormat;
        };
        extern TestVertexBufferSplit g_splits[];
        extern DRAWENV activeDrawEnv;
        TextureID whiteTexture = (TextureID)1;
        TextureID vramTexture = {};
        static int line_calls = 0;
        static short starts[3][2];
        static short ends[3][2];
        static unsigned char colours[3][6];

        void Emulator_GenerateLineArray(Vertex *, short *start, short *end) {
            starts[line_calls][0] = start[0]; starts[line_calls][1] = start[1];
            ends[line_calls][0] = end[0]; ends[line_calls][1] = end[1];
            ++line_calls;
        }
        void Emulator_GenerateTexcoordArrayLineZero(Vertex *, unsigned char) {}
        void Emulator_GenerateColourArrayLine(Vertex *, unsigned char *first, unsigned char *second) {
            for (int component = 0; component < 3; ++component) {
                colours[line_calls - 1][component] = first[component];
                colours[line_calls - 1][component + 3] = second[component];
            }
        }

        int main(void) {
            LINE_F4 line = {};
            line.x0 = 10; line.y0 = 20; line.x1 = 30; line.y1 = 40;
            line.x2 = 50; line.y2 = 60; line.x3 = 70; line.y3 = 80;
            line.r0 = 1; line.g0 = 2; line.b0 = 3;
            g_vertexIndex = 0; g_splitIndex = 0;
            activeDrawEnv.tpage = getTPage(0, 2, 0, 0);

            ParseLineF4(&line, true);

            const short expected_starts[3][2] = {{10, 20}, {30, 40}, {50, 60}};
            const short expected_ends[3][2] = {{30, 40}, {50, 60}, {70, 80}};
            assert(line_calls == 3);
            for (int i = 0; i < 3; ++i) {
                assert(starts[i][0] == expected_starts[i][0] && starts[i][1] == expected_starts[i][1]);
                assert(ends[i][0] == expected_ends[i][0] && ends[i][1] == expected_ends[i][1]);
                for (int component = 0; component < 6; component += 3) {
                    assert(colours[i][component] == 1);
                    assert(colours[i][component + 1] == 2);
                    assert(colours[i][component + 2] == 3);
                }
            }
            assert(g_splitIndex == 1);
            assert(g_splits[1].blendMode == BM_SUBTRACT);
            assert(g_vertexIndex == 18);
            return 0;
        }
        """
    )
    subprocess.run(
        [
            "g++", "-Wno-narrowing", "-DUSE_32_BIT_ADDR", "-ffunction-sections",
            "-fdata-sections", "-Wl,--gc-sections", "-I/usr/include/SDL2", "-I",
            str(REPO / "EMULATOR"), str(source), str(REPO / "EMULATOR" / "LIBGPU.C"),
            "-o", str(executable),
        ], check=True, cwd=REPO,
    )
    subprocess.run([str(executable)], check=True)
