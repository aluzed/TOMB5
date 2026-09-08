"""PSXPC_N control-glyph colour contract, real TU and synthetic tables only."""
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
FLAGS = (0, 0x1000, 0x4000, 0x5000, 0x8000, 0x9000, 0xC000, 0xD000)


@pytest.fixture(scope="module")
def colour_binary(tmp_path_factory):
    directory = tmp_path_factory.mktemp("text_colour")
    source = directory / "harness.cpp"
    executable = directory / "harness"
    source.write_text(r'''
#include "TEXT_S.H"
#include "TEXT.H"
#include "GPU.H"
#include <cstdio>
#include <cstdlib>
CHARDEF CharDef[106] = {};
char AccentTable[46][2] = {};
unsigned char ScaleFlag = 0;
unsigned long GnFrameCounter = 0;
CVECTOR FontShades[10][16] = {};
DB_STRUCT db = {};
int main(int argc, char **argv) {
    if (argc != 5) return 2;
    for (int i = 0; i < 106; ++i) {
        CHARDEF g = {};
        g.u = i; g.v = 7; g.w = 9; g.h = 13; g.YOffset = -11;
        g.TopShade = i % 16; g.BottomShade = (i + 5) % 16;
        CharDef[i] = g; loc_92020[i + 33] = g;
        if (i >= 74) word_9230E[i - 74] = g;
    }
    for (int c = 0; c < 10; ++c)
        for (int s = 0; s < 16; ++s) {
            FontShades[c][s].r = c;
            FontShades[c][s].g = s;
            FontShades[c][s].b = 255 - c - s;
        }
    POLY_GT4 polygons[128] = {};
    unsigned long ot[2] = {};
    db.ot = ot;
    db.polyptr = reinterpret_cast<char *>(polygons);
    db.polybuf_limit = reinterpret_cast<char *>(polygons + 128);
    GnFrameCounter = std::strtoul(argv[3], nullptr, 0);
    PrintString(100, 50, std::atoi(argv[1]), argv[4],
                std::strtoul(argv[2], nullptr, 0));
    auto count = (db.polyptr - reinterpret_cast<char *>(polygons)) / sizeof(POLY_GT4);
    std::printf("%u\n", ScaleFlag);
    for (unsigned i = 0; i < count; ++i) {
        auto &p = polygons[i];
        std::printf("%d %d %d %u", p.x0, p.y0, p.x1 - p.x0, p.u0);
        std::printf(" %u %u %u %u %u %u %u %u %u %u %u %u\n",
            p.r0, p.g0, p.b0, p.r1, p.g1, p.b1,
            p.r2, p.g2, p.b2, p.r3, p.g3, p.b3);
    }
}
''')
    subprocess.run(
        ["g++", "-fsigned-char", "-ffunction-sections", "-fdata-sections",
         "-Wno-narrowing", "-Wl,--gc-sections", "-DPSX_VERSION", "-DPSXPC_TEST",
         "-DNTSC_VERSION", "-DUSE_32_BIT_ADDR", "-I", str(REPO / "GAME"),
         "-I", str(REPO / "SPEC_PSXPC_N"), "-I", str(REPO / "EMULATOR"),
         "-I/usr/include/SDL2", str(source), str(REPO / "SPEC_PSXPC_N/TEXT_S.C"),
         "-o", str(executable)], check=True, cwd=REPO, capture_output=True, text=True,
    )
    return executable


def render(binary, text, colour=3, flags=0, frame=0):
    result = subprocess.run([str(binary), str(colour), str(flags), str(frame), text],
                            check=True, capture_output=True, text=True)
    lines = result.stdout.splitlines()
    assert lines[0] == "0"
    return [tuple(map(int, line.split())) for line in lines[1:]]


def expected(x, y, glyph, colour, scaled):
    top, bottom = glyph % 16, (glyph + 5) % 16
    rgb = tuple(v for shade in (top, top, bottom, bottom)
                for v in (colour, shade, 255 - colour - shade))
    return (x, y, 8 if scaled else 9, glyph, *rgb)


@pytest.mark.parametrize("flags", FLAGS)
@pytest.mark.parametrize("colour", range(10))
@pytest.mark.parametrize("control", range(20, 32))
def test_control_colour_override_is_local(colour_binary, flags, colour, control):
    # Four glyphs, distinct UV/shade identities. Override affects only control;
    # the following ordinary glyph must retain the incoming colour state.
    text = "A" + chr(control) + "ZA"
    scaled = bool(flags & 0x1000)
    advance = 7 if scaled else 9
    width = 4 * advance
    x = 100 - (width // 2 if flags & 0x8000 else width if flags & 0x4000 else 0)
    colours = [colour, colour if 24 <= control <= 27 else 0, colour, colour]
    glyphs = [32, control + 74, 57, 32]
    assert render(colour_binary, text, colour, flags) == [
        expected(x + i * advance, 39, g, c, scaled)
        for i, (g, c) in enumerate(zip(glyphs, colours))]


@pytest.mark.parametrize("flags", FLAGS)
@pytest.mark.parametrize("selector", range(1, 9))
def test_selectors_persist_across_override_whitespace_and_lines(colour_binary, flags, selector):
    text = chr(selector) + "A\x14 \t\n\n\x18Z"
    draws = render(colour_binary, text, 9, flags)
    assert [d[3] for d in draws] == [32, 94, 98, 57]
    assert [d[4] for d in draws] == [selector - 1, 0, selector - 1, selector - 1]
    assert [d[1] for d in draws] == [39, 39, 68, 68]


def test_blink_skips_control_glyphs(colour_binary):
    assert render(colour_binary, "\x02A\x14\x18Z", flags=0x2000, frame=16) == []
