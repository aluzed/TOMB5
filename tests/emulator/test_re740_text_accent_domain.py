"""RE-740: character domain and accent glyph-selection safety for PSXPC_N text.

Scope: provable/safe parts of the accented-char path only. Full accent overlay
extent/width combination and RE-732's 12 space/space "zone preceding first glyph"
entries remain unproven and are not asserted correct here.
"""

import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def accent_binary(tmp_path_factory):
    directory = tmp_path_factory.mktemp("text_accent_domain")
    source = directory / "harness.cpp"
    executable = directory / "harness"
    source.write_text(r'''
#include "TEXT_S.H"
#include "TEXT.H"
#include <cstdio>
#include <cstdlib>
#include <cstring>
CHARDEF CharDef[106] = {};
char AccentTable[46][2] = {};
unsigned char ScaleFlag = 0;
static struct CHARDEF *glyph_for(unsigned char c) {
    if (c < 0x20) return &CharDef[c + 74];
    if (c < 0x80) return &CharDef[c - 33];
    return &CharDef[0];
}
int main(int argc, char **argv) {
    if (argc < 4) return 2;
    /* Synthetic metrics only. */
    for (int i = 0; i < 106; ++i) {
        CharDef[i].w = 9; CharDef[i].h = 13; CharDef[i].YOffset = 0;
    }
    /* Map 0x80 -> base '{' (0x7B), accent space: no overlay proven in draw path. */
    AccentTable[0][0] = '{'; AccentTable[0][1] = ' ';
    glyph_for('{')->w = 11; glyph_for('{')->h = 15; glyph_for('{')->YOffset = -3;
    /* Map 0x81 -> base 'u', accent '^' (overlay exists): not fully reconstructed. */
    AccentTable[1][0] = 'u'; AccentTable[1][1] = '^';
    glyph_for('u')->w = 10; glyph_for('u')->h = 11; glyph_for('u')->YOffset = -2;
    glyph_for('^')->w = 7;  glyph_for('^')->h = 5;  glyph_for('^')->YOffset = -8;

    ScaleFlag = static_cast<unsigned char>(std::atoi(argv[1]));
    const int mode = std::atoi(argv[2]);
    const char *text = argv[3];
    unsigned short top = 123, bottom = 456;
    if (mode == 0) {
        int length = GetStringLength(const_cast<char*>(text), &top, &bottom);
        std::printf("%d %u %u %u\n", length, top, bottom, ScaleFlag);
        return 0;
    }
    return 3;
}
''')
    subprocess.run(
        ["g++", "-ffunction-sections", "-fdata-sections", "-Wno-narrowing",
         "-Wl,--gc-sections", "-DNDEBUG",
         "-DPSX_VERSION", "-DPSXPC_TEST", "-DNTSC_VERSION",
         "-DUSE_32_BIT_ADDR", "-I", str(REPO / "GAME"),
         "-I", str(REPO / "SPEC_PSXPC_N"), "-I", str(REPO / "EMULATOR"),
         "-I/usr/include/SDL2", str(source),
         str(REPO / "SPEC_PSXPC_N/TEXT_S.C"), "-o", str(executable)],
        check=True, cwd=REPO, capture_output=True, text=True,
    )
    return executable


def measure(binary, text, *, scale=0):
    result = subprocess.run(
        [str(binary), str(scale), "0", text],
        check=True, capture_output=True, text=True,
    )
    return tuple(map(int, result.stdout.split()))


def test_accent_no_overlay_uses_base_glyph_metrics(accent_binary):
    # 0x80 maps to base '{' (w=11,h=15,y=-3), accent space => no overlay.
    # ScaleFlag off: width contribution is base width. GetStringLength applies
    # its existing t5 accent adjustment (top -= 4) when any accented char is seen.
    length, top, bottom, scale = measure(accent_binary, "\x80", scale=0)
    assert length == 11
    assert top == (65536 - 7) % 65536  # base YOffset -3, then t5 adjustment -4
    assert bottom == 12  # -3 + 15
    assert scale == 0


def test_accent_no_overlay_respects_scale(accent_binary):
    # ScaleFlag on: w - (w>>2) = 11 - 2 = 9
    length, _top, _bottom, scale = measure(accent_binary, "\x80", scale=1)
    assert length == 9
    assert scale == 1


def test_plain_ascii_unaffected_by_accent_table_setup(accent_binary):
    # 'u' has distinctive metrics in the harness, proving normal lookup still works.
    length, top, bottom, _scale = measure(accent_binary, "u", scale=0)
    assert length == 10
    assert top == (65536 - 2) % 65536
    assert bottom == 9
