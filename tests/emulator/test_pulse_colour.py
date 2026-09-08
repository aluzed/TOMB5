"""RE-739: real input/waterfall/text TUs, synthetic SDK and rendering fixtures.

These SDK doubles validate the portable C contract, NOT target SDK behaviour.
The target CFG/instruction proof is separate, under ignored local build evidence.
"""
import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def pulse_binary(tmp_path_factory):
    directory = tmp_path_factory.mktemp("pulse_colour")
    source = directory / "harness.cpp"
    executable = directory / "harness"
    source.write_text(r'''
#include "SPEC_PSXPC_N/PSXINPUT.C"
#include "TEXT_S.H"
#include "TEXT.H"
#include "GPU.H"
#include "OBJECTS.H"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <initializer_list>
#include "SETUP.H"
// GCC test-only seam to the actual function-local static, in this same TU.
// No copied function, modified production visibility, or production test hook.
extern int input_send asm("_ZZ13S_UpdateInputvE4send");
CVECTOR FontShades[10][16];
unsigned char PulseCnt, ScaleFlag;
unsigned short GlobalCounter;
DB_STRUCT db;
struct PSXTEXTI* AnimatingWaterfalls[6];
int AnimatingWaterfallsV[6];
struct object_info object_storage[NUMBER_OBJECTS];
struct object_info* objects=object_storage;
decltype(lara) lara;
struct ITEM_INFO item;
struct ITEM_INFO* lara_item = &item;
struct PHD_VECTOR OldPickupPos;
decltype(savegame) savegame;
struct GAMEFLOW gameflow;
struct GAMEFLOW* Gameflow = &gameflow;
decltype(BinocularRange) BinocularRange;
int SetDebounce, reset_flag;
unsigned char gfGameMode;
static int state, type, exid, alignment, calls, aligns;
void Emulator_UpdateInput() {}
void SayNo() { std::abort(); } // audio is not covered by this host fixture
int PadGetState(int port) { if(port) std::abort(); return state; }
int PadInfoMode(int port, int mode, int offset) {
    if(port || offset) std::abort();
    return mode == InfoModeCurID ? type : exid;
}
int PadSetActAlign(int port, unsigned char* values) {
    if(port || values[0]!=0 || values[1]!=1) std::abort();
    ++aligns; return alignment;
}
void PadSetAct(int port, unsigned char* motors, int count) {
    if(port || motors!=Motors || count!=2) std::abort();
    ++calls;
}
#define CHECK(c) do { if(!(c)) { std::printf("line %d: %s\n",__LINE__,#c); return false; } } while(0)
bool consume(unsigned colour) {
    CVECTOR before[10][16];
    std::memset(FontShades, 173, sizeof(FontShades));
    std::memcpy(before, FontShades, sizeof(before));
    const unsigned next=(PulseCnt+1)&31;
    const unsigned grey=((next>15 ? 32-next : next)*8)&255;
    UpdatePulseColour();
    CHECK(PulseCnt==next);
    for(int row=0;row<10;++row) for(int i=0;i<16;++i) {
        auto &v=FontShades[row][i];
        if(row==9) { CHECK(v.r==colour && v.g==0 && v.b==0 && v.cd==0); }
        else if(row==1) { CHECK(v.r==grey && v.g==grey && v.b==grey && v.cd==0); }
        else CHECK(std::memcmp(&v,&before[row][i],sizeof(v))==0);
    }
    for(int row : {1,9}) {
        POLY_GT4 polygons[2]={}; unsigned long ot[2]={};
        db.ot=ot; db.polyptr=reinterpret_cast<char*>(polygons);
        db.polybuf_limit=reinterpret_cast<char*>(polygons+2);
        CHARDEF glyph={}; glyph.w=9;glyph.h=13;glyph.TopShade=0;glyph.BottomShade=15;
        DrawChar(0,0,row,&glyph);
        CHECK(db.polyptr==reinterpret_cast<char*>(polygons+1));
        auto &p=polygons[0]; unsigned r=row==9?colour:grey, gb=row==9?0:grey;
        CHECK(p.r0==r && p.r1==r && p.r2==r && p.r3==r);
        CHECK(p.g0==gb && p.g1==gb && p.g2==gb && p.g3==gb);
        CHECK(p.b0==gb && p.b1==gb && p.b2==gb && p.b3==gb);
    }
    return true;
}
bool input_case(int s,int t,int e,int send,int a) {
    state=s;type=t;exid=e;input_send=send;alignment=a;calls=aligns=0;
    RawPad=RawEdge=input=123;PadConnected=1;reset_count=12;
    GPad1.data.pad=65535; SetDebounce=1;
    const bool admitted=s!=0 && (t==4 || t==7);
    const bool act=admitted && e!=0 && send!=0 && s!=1 && s!=4;
    const bool align_call=admitted && e!=0 && send==0 && s==6;
    S_UpdateInput();
    CHECK(PadConnected==admitted);
    CHECK(calls==int(act)); CHECK(aligns==int(align_call));
    if(!admitted) CHECK(RawPad==0 && RawEdge==0 && input==0 && reset_count==0);
    int expected_send=send;
    if(admitted && e) {
        if(s==1 || s==4) expected_send=0;
        if(expected_send==0 && (s==2 || (s==6 && a))) expected_send=1;
    }
    CHECK(input_send==expected_send);
    return consume(act?2:0);
}
int main(int argc,char**argv) {
    if(argc!=2) return 2;
    GlobalCounter=1;
    if(std::strcmp(argv[1],"reject")==0)
        return input_case(6,3,1,1,1)?0:1;
    if(std::strcmp(argv[1],"waterfall")==0) {
        AnimateWaterfalls(); // all objects unloaded still publishes the last phase
        return consume(60)?0:1;
    }
    if(std::strcmp(argv[1],"matrix")==0) {
        for(int s=0;s<256;++s) for(int t : {4,7})
        for(int e : {0,1,65535}) for(int send : {0,1,-1}) for(int a : {0,1})
            if(!input_case(s,t,e,send,a)) return 1;
        for(int t=0;t<256;++t) if(!input_case(6,t,1,-1,1)) return 1;
    } else if(std::strcmp(argv[1],"transitions")==0) {
        for(int first : {2,6}) for(int a : {0,1}) {
            if(!input_case(1,7,1,-1,a)) return 1;
            if(!input_case(first,7,1,input_send,a)) return 1;
            if(!input_case(6,7,1,input_send,a)) return 1;
            if(!input_case(6,7,0,input_send,a)) return 1;
            if(!input_case(6,3,1,input_send,a)) return 1;
            if(!input_case(6,7,65535,input_send,a)) return 1;
            if(!input_case(4,7,1,input_send,a)) return 1;
        }
    } else if(std::strcmp(argv[1],"phases")==0) {
        PSXTEXTI textures[6][2]={};
        for(int i=0;i<6;++i) AnimatingWaterfalls[i]=textures[i];
        for(unsigned counter=0;counter<65536;++counter) {
            GlobalCounter=counter;
            for(int i=0;i<6;++i) objects[WATERFALL1+i].loaded=(counter>>i)&1;
            if(!input_case(6,7,1,1,1)) return 1;
            AnimateWaterfalls();
            if(!consume((0u-4u*counter)&63)) return 1;
            if(!input_case(0,7,1,1,1)) return 1;
        }
        for(int initial=0;initial<256;++initial) {
            PulseCnt=initial;
            if(!input_case(6,4,1,1,1)) return 1;
        }
    } else return 2;
    return 0;
}
''')
    command = ["g++", "-O0", "-fpermissive", "-Wno-narrowing", "-ffunction-sections",
               "-fdata-sections", "-Wl,--gc-sections", "-DPSX_VERSION",
               "-DPSXPC_TEST", "-DNTSC_VERSION", "-DUSE_32_BIT_ADDR",
               "-I", str(REPO), "-I", str(REPO / "GAME"),
               "-I", str(REPO / "SPEC_PSXPC_N"), "-I", str(REPO / "EMULATOR"),
               "-I/usr/include/SDL2", str(source), str(REPO / "GAME/OBJECTS.C"),
               str(REPO / "SPEC_PSXPC_N/TEXT_S.C"), "-o", str(executable)]
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return executable


@pytest.mark.parametrize("case", ["reject", "matrix", "transitions", "phases", "waterfall"])
def test_producer_to_real_colour_and_drawchar(pulse_binary, case):
    result = subprocess.run([str(pulse_binary), case], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("path, producers", [
    ("GAME/CONTROL.C", ["AnimateWaterfalls"]),
    ("GAME/NEWINV2.C", ["S_UpdateInput", "S_UpdateInput"]),
    ("SPEC_PSXPC_N/SPECIFIC.C", ["S_UpdateInput", "S_UpdateInput"]),
])
def test_five_preprocessed_callsites_keep_their_producer(path, producers):
    # Integration guard only: this does not execute the enclosing game loops.
    result = subprocess.run(
        ["g++", "-E", "-P", "-DPSX_VERSION", "-DPSXPC_TEST", "-DNTSC_VERSION",
         "-DUSE_32_BIT_ADDR", "-IGAME", "-ISPEC_PSXPC_N", "-IEMULATOR",
         "-I/usr/include/SDL2", path], cwd=REPO, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    text = result.stdout
    consumers = list(re.finditer(r"(?m)^\s*UpdatePulseColour\(\);", text))
    assert len(consumers) == len(producers)
    for consumer, producer in zip(consumers, producers):
        preceding = text[:consumer.start()]
        calls = list(re.finditer(r"\b(S_UpdateInput|AnimateWaterfalls)\(\);", preceding))
        assert calls[-1].group(1) == producer
        # Only benign inventory bookkeeping/diagnostics separates the calls.
        between = preceding[calls[-1].end():].strip()
        assert between in ("", "input = inputBusy;",
                           'printf("Input Normal: %x\\n", input);\n   input = inputBusy;')


def test_shared_waterfall_publication_is_backend_local():
    capability = "PSXPC_N_INHERITED_PULSE_COLOUR"
    defining_headers = [p.relative_to(REPO).as_posix()
                        for p in REPO.glob("SPEC_*/SPECIFIC.H")
                        if f"#define {capability} " in p.read_text()]
    assert defining_headers == ["SPEC_PSXPC_N/SPECIFIC.H"]
    source = (REPO / "GAME/OBJECTS.C").read_text()
    publication = source.split(f"#ifdef {capability}\n", 1)[1].split("#endif", 1)[0]
    assert "SecondaryPulseColour =" in publication
    assert source.count("SecondaryPulseColour") == 1
