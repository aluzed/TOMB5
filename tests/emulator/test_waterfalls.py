"""Synthetic meshes exercise real SETUP/OBJECTS translation units, not copied code.

The internal setup unit is called directly: full level I/O and SDK execution are
outside this harness. A separate guard checks its placement in LoadLevel.
"""
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module", params=[False, True], ids=["consumer", "producer-chain"])
def waterfall_binary(request, tmp_path_factory):
    directory = tmp_path_factory.mktemp("waterfalls")
    source = directory / "harness.cpp"
    executable = directory / "harness"
    source.write_text(r'''
#include "GAME/SETUP.C"
#include <cstdlib>
#include <cstdio>
struct PSXTEXTI* AnimatingWaterfalls[6];
int AnimatingWaterfallsV[6];
struct PSXTEXTSTRUCT* psxtextinfo;
short** meshes;
unsigned short GlobalCounter;
int main(int argc, char** argv) {
    const int mask = std::atoi(argv[1]);
    GlobalCounter = std::atoi(argv[2]);
    const int packed = std::atoi(argv[3]);
    const int half = packed >= 0 ? packed / 2 : -((-packed + 1) / 2);
    short storage[6][33000] = {};
    short* pointers[6];
    PSXTEXTI textures[40];
    unsigned char expected[sizeof(textures)];
    auto bytes = reinterpret_cast<unsigned char*>(textures);
    for (unsigned j=0; j<sizeof(textures); ++j) bytes[j]=(j*19+7)&255;
    meshes=pointers;
    psxtextinfo=reinterpret_cast<PSXTEXTSTRUCT*>(textures);
    for (int i=0; i<6; ++i) {
        pointers[i]=storage[i]+16400;
        pointers[i][5]=packed;
        pointers[i][8+half]=2+i*5;
        objects[WATERFALL1+i].loaded=(mask>>i)&1;
        objects[WATERFALL1+i].mesh_index=i;
        textures[2+i*5].v0=(233+i*17)&255;
        AnimatingWaterfalls[i]=textures+39;
        AnimatingWaterfallsV[i]=12345;
#ifndef TEST_PRODUCER
        if ((mask>>i)&1) {
            AnimatingWaterfalls[i]=textures+2+i*5;
            AnimatingWaterfallsV[i]=textures[2+i*5].v0;
        }
#endif
    }
#ifdef TEST_PRODUCER
    InitialiseWaterfalls();
#endif
    for (int i=0; i<6; ++i) {
        const bool loaded=(mask>>i)&1;
        if (AnimatingWaterfalls[i] != textures+(loaded ? 2+i*5 : 39)) return 10+i;
        if (AnimatingWaterfallsV[i] != (loaded ? textures[2+i*5].v0 : 12345)) return 20+i;
    }
    for (unsigned j=0; j<sizeof(textures); ++j) expected[j]=bytes[j];
    for (int i=0; i<6; ++i) if ((mask>>i)&1) {
        int phase=(-int(GlobalCounter)*(i<5 ? 7 : 4))&63;
        int top=textures[2+i*5].v0+phase;
        for (int n=0; n<(i<4 ? 2 : 1); ++n) {
            auto record=expected+(2+i*5+n)*sizeof(PSXTEXTI);
            record[1]=record[5]=top;
            record[9]=record[13]=top+63;
        }
    }
    AnimateWaterfalls();
    for (unsigned j=0; j<sizeof(textures); ++j)
        if (bytes[j]!=expected[j]) { std::printf("texture byte %u: %u != %u\n",j,bytes[j],expected[j]); return 30; }
    return 0;
}
''')
    command = ["g++", "-fpermissive", "-Wno-narrowing", "-ffunction-sections",
               "-fdata-sections", "-Wl,--gc-sections", "-DPSX_VERSION",
               "-DPSXPC_TEST", "-DNTSC_VERSION", "-DUSE_32_BIT_ADDR",
               "-I", str(REPO), "-I", str(REPO / "GAME"),
               "-I", str(REPO / "SPEC_PSXPC_N"), "-I", str(REPO / "EMULATOR"),
               "-I/usr/include/SDL2", str(source), str(REPO / "GAME/OBJECTS.C"),
               str(REPO / "SPEC_PSXPC_N/TEXT_S.C"),
               "-o", str(executable)]
    if request.param:
        command.append("-DTEST_PRODUCER")
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return executable


@pytest.mark.parametrize("packed", [0, 1, 2, 3, 20, 21, 126, 127, -1, -2, -17, 32767, -32768])
def test_initialisation_then_animation(waterfall_binary, packed):
    for mask in range(64):
        for counter in [0, 1, 7, 15, 31, 32, 63, 64, 255, 1024, 65535]:
            result = subprocess.run([str(waterfall_binary), str(mask), str(counter), str(packed)],
                                    capture_output=True, text=True)
            assert result.returncode == 0, (mask, counter, packed, result.returncode, result.stdout)


def test_load_level_invokes_psx_initialisation():
    source = (REPO / "GAME/SETUP.C").read_text()
    region = source.split("GLOBAL_gunflash_meshptr =", 1)[1].split("MonitorScreenTI = NULL", 1)[0]
    assert "#if PSX_VERSION\n\tInitialiseWaterfalls();\n#endif" in region
