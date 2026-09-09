"""RE762: synthetic GetFloor regression on the complete production TU.

Real GetDoor and triangle helpers, no service doubles or private inputs. The
instrumentation observes GetDoor entries under the explicitly checked i386 ABI;
this is neither exhaustive native access tracing nor a complete game build.
"""
import itertools
import json
from pathlib import Path
import struct
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[2]
SHAPES = ((5, 6), (4, 3))
CASES = tuple(itertools.product(range(2), range(6), range(6), range(3), range(4), (1, 2)))
HARNESS = r'''
#include "GETSTUFF.H"
#include "CONTROL.H"
#include "ROOMLOAD.H"
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstddef>
static_assert(sizeof(void*)==4 && sizeof(long)==4, "i386 required");
static_assert(sizeof(FLOOR_INFO)==8 && sizeof(room_info)==80, "layouts");
static_assert(offsetof(room_info,floor)==8 && offsetof(room_info,x)==20 &&
              offsetof(room_info,z)==28 && offsetof(room_info,x_size)==40 &&
              offsetof(room_info,y_size)==42, "room offsets");
room_info rooms[3]; room_info* room=rooms;
FLOOR_INFO cells[3][64]; short words[4]; short* floor_data=words;
unsigned selections[4][2], entries=0, exits=0;
extern "C" void __cyg_profile_func_enter(void* function, void*) {
    if (function != (void*)&GetDoor) return;
    auto frame=(uintptr_t*)__builtin_frame_address(1);
    uintptr_t p=frame[2], base=(uintptr_t)cells;
    if (entries>=4 || p<base || p+sizeof(FLOOR_INFO)>base+sizeof(cells) || (p-base)%8)
        __builtin_trap();
    selections[entries][0]=(p-base)/512;
    selections[entries++][1]=((p-base)%512)/8;
}
extern "C" void __cyg_profile_func_exit(void* function, void*) {
    if (function==(void*)&GetDoor) ++exits;
}
void dump(const char* label, const void* data, size_t size) {
    printf("%s ",label);
    for(size_t i=0;i<size;++i) printf("%02x",((const unsigned char*)data)[i]);
    puts("");
}
void snapshot(const char* phase) {
    puts(phase); dump("rooms",rooms,sizeof(rooms));
    dump("cells",cells,sizeof(cells)); dump("words",words,sizeof(words));
}
int main(int argc,char** argv) {
    if(argc!=7) return 2;
    int shape=atoi(argv[1]), xp=atoi(argv[2]), zp=atoi(argv[3]);
    int height=atoi(argv[4]), mode=atoi(argv[5]), dest=atoi(argv[6]);
    if(shape<0||shape>1||xp<0||xp>5||zp<0||zp>5||height<0||height>2||
       mode<0||mode>3||dest<1||dest>2) return 3;
    int xs=shape?4:5, ys=shape?3:6;
    for(int r=0;r<3;++r) {
        rooms[r].floor=cells[r]; rooms[r].x=r? -2048:1024;
        rooms[r].z=r? 1024:-2048;
        rooms[r].x_size=r?ys:xs; rooms[r].y_size=r?xs:ys;
        for(int i=0;i<64;++i) {
            cells[r][i].box=1+r*64+i; cells[r][i].fx=i%16;
            cells[r][i].pit_room=255; cells[r][i].sky_room=255;
            cells[r][i].floor=8; cells[r][i].ceiling=2;
            // Uniform portals mask the first-cell defect; asymmetric ones do not.
            cells[r][i].index=(r==0 && (mode==1 || mode==3 ||
                                      (mode==2 && i==2*xs-1)))?1:0;
        }
    }
    words[1]=1; words[2]=mode==3?255:dest; words[3]=1234;
    int xpositions[]={-1,0,1,ys-2,ys-1,ys};
    int zpositions[]={-1,0,1,xs-2,xs-1,xs};
    int heights[]={256,1024,2304};
    snapshot("before"); short rn=0;
    FLOOR_INFO* result=GetFloor(rooms[0].x+1024*xpositions[xp]+137,heights[height],
                              rooms[0].z+1024*zpositions[zp]+319,&rn);
    uintptr_t p=(uintptr_t)result,base=(uintptr_t)cells;
    if(p<base || p+8>base+sizeof(cells) || (p-base)%8 || entries!=exits) return 4;
    printf("result %d %u %u %u",rn,(unsigned)((p-base)/512),
           (unsigned)(((p-base)%512)/8),entries);
    for(unsigned i=0;i<entries;++i) printf(" %u %u",selections[i][0],selections[i][1]);
    puts(""); snapshot("after"); return 0;
}
'''


def selected_cell(x, z, xs, ys):
    """Geometric contract: low X uses lane 1 at either Z boundary."""
    lane_x, lane_z = x // 1024, z // 1024
    if lane_z <= 0 or lane_z >= xs-1:
        lane_z = 0 if lane_z <= 0 else xs-1
        lane_x = min(max(lane_x, 1), ys-2)
    else:
        lane_x = min(max(lane_x, 0), ys-1)
    return lane_x*xs+lane_z


def expected_output(case, cells_address):
    shape, xp, zp, height, mode, dest = case
    xs, ys = SHAPES[shape]
    rooms, cells = bytearray(240), bytearray(1536)
    words = struct.pack('<hhhh', 0, 1, 255 if mode==3 else dest, 1234)
    for r in range(3):
        struct.pack_into('<I', rooms, r*80+8, cells_address+r*512)
        struct.pack_into('<iii', rooms, r*80+20, -2048 if r else 1024, 0, 1024 if r else -2048)
        struct.pack_into('<hh', rooms, r*80+40, ys if r else xs, xs if r else ys)
        for i in range(64):
            index = int(r==0 and (mode in (1, 3) or (mode==2 and i==2*xs-1)))
            struct.pack_into('<HHBBBB', cells, r*512+i*8, index,
                             ((1+r*64+i)<<4)|(i%16), 255, 8, 255, 2)
    x = (-1,0,1,ys-2,ys-1,ys)[xp]*1024+137
    z = (-1,0,1,xs-2,xs-1,xs)[zp]*1024+319
    cell = selected_cell(x,z,xs,ys)
    selections = [(0,cell)]
    rn = 0
    if mode==1 or (mode==2 and cell==2*xs-1):
        rn = dest
        selections.append((dest,selected_cell(x+3072,z-3072,ys,xs)))
    result = [rn, *selections[-1], len(selections), *itertools.chain.from_iterable(selections)]
    buffers = [label+' '+data.hex() for label,data in (('rooms',rooms),('cells',cells),('words',words))]
    return ['before',*buffers,'result '+' '.join(map(str,result)),'after',*buffers]


@pytest.fixture(scope='module')
def floor_binary(tmp_path_factory):
    directory=tmp_path_factory.mktemp('getfloor-clamp')
    harness=directory/'harness.cpp'
    harness.write_text(HARNESS)
    flags=['g++','-m32','-O0','-fno-omit-frame-pointer','-Wno-narrowing',
           '-ffunction-sections','-fdata-sections','-fno-pie','-no-pie',
           '-DPSX_VERSION=1','-DPSXPC_TEST=1','-DNTSC_VERSION=1',
           '-DUSE_32_BIT_ADDR=1','-DDEBUG_VERSION=0','-DDISC_VERSION=1',
           '-IGAME','-ISPEC_PSXPC_N','-IEMULATOR','-I/usr/include/SDL2']
    commands=[flags+['-MMD','-MF',str(directory/'tu.d'),'-finstrument-functions','-c',
                     'SPEC_PSXPC_N/GETSTUFF.C','-o',str(directory/'tu.o')],
              flags+['-MMD','-MF',str(directory/'harness.d'),'-c',str(harness),'-o',str(directory/'harness.o')],
              ['g++','-m32','-no-pie','-Wl,--gc-sections',str(directory/'harness.o'),
               str(directory/'tu.o'),'-o',str(directory/'host')]]
    for i,command in enumerate(commands):
        result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60)
        (directory/f'compile-{i}.json').write_text(json.dumps(dict(command=command,exit=result.returncode)))
        (directory/f'compile-{i}.log').write_text(result.stdout+result.stderr)
        assert result.returncode==0,result.stderr
    binary=directory/'host'
    header=binary.read_bytes()[:20]
    assert header[:5]==b'\x7fELF\x01' and header[18:20]==b'\x03\x00'
    symbols=subprocess.check_output(['nm','-n',str(binary)],text=True,cwd=ROOT)
    (directory/'symbols.txt').write_text(symbols)
    cells_address=int(next(line.split()[0] for line in symbols.splitlines() if line.split()[-1]=='cells'),16)
    return directory,binary,cells_address


@pytest.mark.parametrize('case',CASES)
def test_full_buffers_final_and_intermediate(floor_binary,case):
    directory,binary,cells_address=floor_binary
    command=[str(binary),*map(str,case)]
    result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=5)
    expected=expected_output(case,cells_address)
    (directory/('-'.join(map(str,case))+'.json')).write_text(json.dumps(dict(
        command=command,exit=result.returncode,stdout=result.stdout,stderr=result.stderr,expected=expected)))
    assert result.returncode==0,result.stderr
    assert result.stderr==''
    assert result.stdout.splitlines()==expected


@pytest.mark.parametrize('psx,psxpc',tuple(itertools.product((0,1),repeat=2)))
def test_backend_selection_only(psx,psxpc):
    # Preprocessor slice only; not a compilation/proof of alternative backends.
    source=(ROOT/'SPEC_PSXPC_N/GETSTUFF.C').read_text()
    branch=source.split('else if (dx > 0)',1)[1].split('else if (dx <= 0)',1)[0]
    result=subprocess.run(['g++','-E','-P','-x','c++',f'-DPSX_VERSION={psx}',
                           f'-DPSXPC_TEST={psxpc}','-'],input=branch,capture_output=True,text=True,timeout=10)
    assert result.returncode==0
    assert result.stdout.count('dx = 1;')==int(bool(psx and psxpc))
    assert result.stdout.count('dx = r->y_size - 2;')==(1 if psx and psxpc else 2)


def test_matrix_contract():
    assert len(CASES)==len(set(CASES))==1728
    assert set(CASES)==set(itertools.product(range(2),range(6),range(6),range(3),range(4),(1,2)))
