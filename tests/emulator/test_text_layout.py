"""Execute PrintString and DrawChar from the real translation unit.

Synthetic font metrics isolate multiline layout from the still-unreconstructed
font table selection and accent paths. No binary assets are required.
"""
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def layout_binary(tmp_path_factory):
    directory = tmp_path_factory.mktemp("text_layout")
    source = directory / "harness.cpp"
    executable = directory / "harness"
    source.write_text(r'''
#include "TEXT_S.H"
#include "TEXT.H"
#include "GPU.H"
#include <cstdio>
#include <cstdlib>
CHARDEF CharDef[106] = {};
extern CHARDEF loc_92020[139];
char AccentTable[46][2] = {};
unsigned char ScaleFlag = 0;
unsigned long GnFrameCounter = 0;
CVECTOR FontShades[10][16] = {};
DB_STRUCT db = {};
int main(int argc, char **argv) {
    if (argc != 7) return 2;
    // Both legacy rendering storage and measurement storage receive the same
    // invented metrics. This suite does not claim their mapping is correct.
    CHARDEF glyph = {};
    glyph.w = 9; glyph.h = 13; glyph.YOffset = -11;
    for (auto &g : CharDef) g = glyph;
    for (auto &g : loc_92020) g = glyph;
    for (int c = 0; c < 10; ++c)
        for (auto &shade : FontShades[c]) shade.r = c;
    POLY_GT4 polygons[128] = {};
    unsigned long ot[2] = {};
    db.ot = ot;
    db.polyptr = reinterpret_cast<char *>(polygons);
    db.polybuf_limit = reinterpret_cast<char *>(polygons + 128);
    GnFrameCounter = std::strtoul(argv[4], nullptr, 0);
    ScaleFlag = std::atoi(argv[5]);
    PrintString(std::atoi(argv[1]), std::atoi(argv[2]), 3, argv[6],
                std::strtoul(argv[3], nullptr, 0));
    auto count = (db.polyptr - reinterpret_cast<char *>(polygons)) / sizeof(POLY_GT4);
    std::printf("%u\n", ScaleFlag);
    for (unsigned i = 0; i < count; ++i)
        std::printf("%d %d %d %u\n", polygons[i].x0, polygons[i].y0,
                    polygons[i].x1 - polygons[i].x0, polygons[i].r0);
}
''')
    subprocess.run(
        ["g++", "-ffunction-sections", "-fdata-sections", "-Wno-narrowing",
         "-Wl,--gc-sections", "-DPSX_VERSION", "-DPSXPC_TEST", "-DNTSC_VERSION",
         "-DUSE_32_BIT_ADDR", "-I", str(REPO / "GAME"),
         "-I", str(REPO / "SPEC_PSXPC_N"), "-I", str(REPO / "EMULATOR"),
         "-I/usr/include/SDL2", str(source),
         str(REPO / "SPEC_PSXPC_N/TEXT_S.C"), "-o", str(executable)],
        check=True, cwd=REPO, capture_output=True, text=True,
    )
    return executable


def render(binary, text, *, flags=0, x=100, y=50, frame=0, scale=0):
    result = subprocess.run(
        [str(binary), str(x), str(y), str(flags), str(frame), str(scale), text],
        check=True, capture_output=True, text=True,
    )
    lines = result.stdout.splitlines()
    return int(lines[0]), [tuple(map(int, line.split())) for line in lines[1:]]


@pytest.mark.parametrize("flags, positions, width", [
    (0, [100, 100, 109], 9),
    (0x4000, [91, 82, 91], 9),
    (0x8000, [96, 91, 100], 9),
    (0xC000, [96, 91, 100], 9),
    (0x5000, [93, 86, 93], 8),
])
def test_each_line_is_aligned_to_original_anchor(layout_binary, flags, positions, width):
    scale, draws = render(layout_binary, "A\nAA", flags=flags)
    assert scale == 0
    assert draws == [(positions[0], 39, width, 3),
                     (positions[1], 54, width, 3),
                     (positions[2], 54, width, 3)]


@pytest.mark.parametrize("text, ys", [
    ("A\n\nA", [39, 68]),
    ("A\n\n\nA", [39, 84]),
    ("\n\nA", [68]),
    ("A\n\nA\nA", [39, 68, 83]),
])
def test_blank_line_resets_previous_bottom(layout_binary, text, ys):
    scale, draws = render(layout_binary, text)
    assert scale == 0
    assert draws == [(100, y, 9, 3) for y in ys]


@pytest.mark.parametrize("flags, second_x, width", [(0, 165, 9), (0x1000, 159, 8)])
def test_whitespace_and_colour_survive_line_transition(layout_binary, flags, second_x, width):
    scale, draws = render(layout_binary, "\x02A \t A\n\n\x04A", flags=flags)
    assert scale == 0
    assert draws == [(100, 39, width, 1), (second_x, 39, width, 1), (100, 68, width, 3)]


@pytest.mark.parametrize("text", ["", "A\n", "A\n\n"])
def test_trailing_lines_do_not_emit_glyphs(layout_binary, text):
    scale, draws = render(layout_binary, text, scale=7)
    assert scale == 0
    assert draws == ([(100, 39, 9, 3)] if text else [])


def test_blink_early_exit_preserves_scale_state(layout_binary):
    assert render(layout_binary, "A\n\nA", flags=0x3000, frame=16, scale=7) == (7, [])
