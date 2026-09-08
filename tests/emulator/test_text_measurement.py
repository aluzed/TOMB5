"""Host execution of the real text unit with synthetic, non-asset glyph data.

Scope: proven ASCII whitespace behavior only; accents remain unproven for
safe host indexing. The normal translation unit is compiled, not a copied body.
"""

import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def measurement_binary(tmp_path_factory):
    directory = tmp_path_factory.mktemp("text_measurement")
    source = directory / "harness.cpp"
    executable = directory / "harness"
    source.write_text(r'''
#include "TEXT_S.H"
#include "TEXT.H"
#include <cstdio>
#include <cstdlib>
CHARDEF CharDef[106] = {};
char AccentTable[46][2] = {};
unsigned char ScaleFlag = 0;
int main(int argc, char **argv) {
    if (argc != 5) return 2;
    ScaleFlag = static_cast<unsigned char>(std::atoi(argv[1]));
    // Synthetic metrics, not the game's font table.
    for (int i = 0; i < 106; ++i) {
        CharDef[i].w = 9;
        CharDef[i].h = 13;
        CharDef[i].YOffset = static_cast<char>(std::atoi(argv[2]));
    }
    unsigned short top = 123, bottom = 456, width = 0, height = 0;
    const int mask = std::atoi(argv[3]);
    int length = GetStringLength(argv[4], mask & 1 ? &top : nullptr,
                                mask & 2 ? &bottom : nullptr);
    GetStringDimensions(argv[4], &width, &height);
    std::printf("%d %u %u %u %u %u\n", length, top, bottom,
                width, height, ScaleFlag);
    return 0;
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


def measure(binary, text, *, scale=0, top=-11, mask=3):
    result = subprocess.run(
        [str(binary), str(scale), str(top), str(mask), text],
        check=True, capture_output=True, text=True,
    )
    return tuple(map(int, result.stdout.split()))


@pytest.mark.parametrize("text, expected", [(" ", 6), ("  ", 12), ("A A", 20)])
def test_scaled_space_advances_six(measurement_binary, text, expected):
    result = measure(measurement_binary, text, scale=1)
    assert result[0] == expected
    assert result[5] == 1


@pytest.mark.parametrize("top, expected", [(-13, -13), (-12, -12), (-11, -12), (-10, -12)])
def test_tab_preserves_or_extends_glyph_top(measurement_binary, top, expected):
    result = measure(measurement_binary, "A\t", top=top)
    assert result[0] == 49
    assert result[1] == expected % 65536


@pytest.mark.parametrize("scale, width", [(0, 8), (1, 6), (255, 6)])
def test_space_does_not_change_vertical_sentinels(measurement_binary, scale, width):
    assert measure(measurement_binary, " ", scale=scale) == (
        width, 1024, 64512, width, 63490, scale,
    )


@pytest.mark.parametrize("scale", [0, 1])
def test_tab_sets_vertical_bounds(measurement_binary, scale):
    assert measure(measurement_binary, "\t", scale=scale) == (40, 65524, 2, 40, 16, scale)


@pytest.mark.parametrize("mask", [0, 1, 2, 3])
def test_optional_metrics_remain_optional(measurement_binary, mask):
    result = measure(measurement_binary, "A \t", scale=1, mask=mask)
    assert result == (53, 65524 if mask & 1 else 123,
                      2 if mask & 2 else 456, 53, 16, 1)


@pytest.mark.parametrize("text, length, width, height", [
    ("", 0, 0, 63490),
    ("A\nA A", 7, 20, 30),
    ("A\n\nA", 7, 7, 46),
    ("A\n", 7, 7, 15),
    ("\x01A\x13", 7, 7, 15),
])
def test_line_measurement_preserves_existing_control_contract(
    measurement_binary, text, length, width, height,
):
    result = measure(measurement_binary, text, scale=1)
    assert result[0] == length
    assert result[3:5] == (width, height)
