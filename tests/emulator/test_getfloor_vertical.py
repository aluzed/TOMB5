"""RE765: public synthetic vertical regression, complete actual GETSTUFF.C TU.

No private data, copied implementation, service doubles or unresolved-symbol
suppression. Function-boundary events are not exhaustive native store tracing.
"""
import itertools
import json
from datetime import datetime
from pathlib import Path
import struct
import subprocess
import time

import pytest

ROOT = Path(__file__).resolve().parents[2]
CASES = tuple(itertools.product((1, 2), (512, 1024, 1536), (512, 1024, 1536),
                                (-1, 0, 1), (-1, 0, 1), (0, 1), (0, 1)))
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
static_assert(offsetof(room_info,floor)==8 && offsetof(room_info,y)==24 &&
              offsetof(room_info,minfloor)==32 && offsetof(room_info,x_size)==40,
              "room offsets");
room_info rooms[4]; room_info* room=rooms;
FLOOR_INFO cells[4][16]; short words[4]; short* floor_data=words;
short rn; bool tracking=false;
struct Event { int kind, cell, room; } events[16]; int count=0;
int cell_id(uintptr_t p) {
    uintptr_t base=(uintptr_t)cells;
    if(p<base || p+8>base+sizeof(cells) || (p-base)%8) __builtin_trap();
    return (p-base)/8;
}
void event(int kind,int cell) {
    if(count>=16) __builtin_trap();
    events[count++]={kind,cell,rn};
}
extern "C" void __cyg_profile_func_enter(void* f, void*) {
    if(!tracking) return;
    if(f==(void*)&GetFloor) { event(1,-1); return; }
    int kind=f==(void*)&GetDoor?2:f==(void*)&CheckNoColFloorTriangle?3:
             f==(void*)&CheckNoColCeilingTriangle?4:0;
    if(kind) { auto frame=(uintptr_t*)__builtin_frame_address(1);
               event(kind,cell_id(frame[2])); }
}
extern "C" void __cyg_profile_func_exit(void* f, void*) {
    if(!tracking) return;
    int kind=f==(void*)&GetFloor?1:f==(void*)&GetDoor?2:
             f==(void*)&CheckNoColFloorTriangle?3:f==(void*)&CheckNoColCeilingTriangle?4:0;
    if(kind) event(-kind,-1);
}
void dump(const char* label,const void* p,size_t n) {
    printf("%s ",label);
    for(size_t i=0;i<n;++i) printf("%02x",((const unsigned char*)p)[i]);
    puts("");
}
void snapshot(const char* label) {
    puts(label); dump("rooms",rooms,sizeof(rooms));
    dump("cells",cells,sizeof(cells)); dump("words",words,sizeof(words));
}
int main(int argc,char** argv) {
    if(argc!=8) return 2;
    int current=atoi(argv[1]), minimum=atoi(argv[2]), zero=atoi(argv[3]);
    int relation=atoi(argv[4]), helper=atoi(argv[5]), link=atoi(argv[6]), sky=atoi(argv[7]);
    if(current<1||current>2||minimum<512||minimum>1536||zero<512||zero>1536||
       relation< -1||relation>1||helper< -1||helper>1||link<0||link>1||sky<0||sky>1) return 3;
    for(int r=0;r<4;++r) {
        rooms[r].floor=cells[r]; rooms[r].x_size=4; rooms[r].y_size=4;
        rooms[r].minfloor=r==0?zero:minimum; rooms[r].y=minimum;
        for(int i=0;i<16;++i) {
            cells[r][i].box=1+r*16+i; cells[r][i].fx=i%16;
            cells[r][i].pit_room=255; cells[r][i].sky_room=255;
            cells[r][i].floor=r==current?(sky?16:0):16;
            cells[r][i].ceiling=r==current&&sky?12:0;
        }
    }
    cells[current][5].index=helper?1:0;
    if(sky) cells[current][5].sky_room=link?3:255;
    else cells[current][5].pit_room=link?3:255;
    words[1]=helper?((sky?15:11)+(helper==1))|0x8000:0;
    words[2]=1234; words[3]=2345;
    int direct=sky?CheckNoColCeilingTriangle(&cells[current][5],1161,1343):
                   CheckNoColFloorTriangle(&cells[current][5],1161,1343);
    printf("helper %d\n",direct); snapshot("before");
    rn=current; tracking=true;
    FLOOR_INFO* result=GetFloor(1161,minimum+relation,1343,&rn);
    tracking=false;
    printf("result %d %d\n",rn,cell_id((uintptr_t)result));
    for(int i=0;i<count;++i) printf("event %d %d %d\n",events[i].kind,events[i].cell,events[i].room);
    snapshot("after"); return 0;
}
'''


def invoke(command, directory, name, **kwargs):
    """Archive real invocation metadata, including successful native returns."""
    record = dict(command=command, cwd=str(ROOT), start=datetime.now().astimezone().isoformat())
    path = directory / (name+'.json')
    assert not path.exists()
    path.write_text(json.dumps(record))
    start = time.monotonic()
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60, **kwargs)
    record.update(end=datetime.now().astimezone().isoformat(), elapsed=time.monotonic()-start,
                  exit=result.returncode, stdout=result.stdout, stderr=result.stderr)
    path.write_text(json.dumps(record))
    assert result.returncode == 0, result.stderr
    return result.stdout


@pytest.fixture(scope='module')
def vertical_binary(tmp_path_factory):
    directory = tmp_path_factory.mktemp('getfloor-vertical')
    harness = directory/'harness.cpp'
    harness.write_text(HARNESS)
    flags = ['g++','-m32','-O0','-fno-omit-frame-pointer','-Wno-narrowing',
             '-ffunction-sections','-fdata-sections','-fno-pie','-no-pie',
             '-DPSX_VERSION=1','-DPSXPC_TEST=1','-DNTSC_VERSION=1',
             '-DUSE_32_BIT_ADDR=1','-DDEBUG_VERSION=0','-DDISC_VERSION=1',
             '-IGAME','-ISPEC_PSXPC_N','-IEMULATOR','-I/usr/include/SDL2']
    commands = [flags+['-MMD','-MF',str(directory/'tu.d'),'-finstrument-functions','-c',
                      'SPEC_PSXPC_N/GETSTUFF.C','-o',str(directory/'tu.o')],
                flags+['-MMD','-MF',str(directory/'harness.d'),'-c',str(harness),'-o',str(directory/'harness.o')],
                ['g++','-m32','-no-pie','-Wl,--gc-sections',str(directory/'harness.o'),
                 str(directory/'tu.o'),'-o',str(directory/'host')]]
    for i, command in enumerate(commands):
        invoke(command,directory,f'compile-{i}')
    binary = directory/'host'
    header = binary.read_bytes()[:20]
    assert header[:5] == b'\x7fELF\x01' and header[18:20] == b'\x03\x00'
    symbols = invoke(['nm','-n',str(binary)],directory,'symbols')
    for name in ('GetFloor','GetDoor','CheckNoColFloorTriangle','CheckNoColCeilingTriangle'):
        assert name in symbols
    address = int(next(line.split()[0] for line in symbols.splitlines() if line.split()[-1]=='cells'),16)
    return directory,binary,address


def expected(case, address):
    """Independent buffer reconstruction and declarative traversal truth table."""
    current, minimum, zero, relation, helper, link, sky = case
    rooms, cells = bytearray(320), bytearray(512)
    for r in range(4):
        struct.pack_into('<I',rooms,r*80+8,address+r*128)
        struct.pack_into('<i',rooms,r*80+24,minimum)
        struct.pack_into('<i',rooms,r*80+32,zero if r==0 else minimum)
        struct.pack_into('<hh',rooms,r*80+40,4,4)
        for i in range(16):
            selected = r==current and i==5
            struct.pack_into('<HHBBBB',cells,r*128+i*8,
                             int(selected and helper!=0),((1+r*16+i)<<4)|(i%16),
                             3 if selected and link and not sky else 255,
                             0 if r==current and not sky else 16,
                             3 if selected and link and sky else 255,
                             12 if r==current and sky else 0)
    tag = (32768 + (15 if sky else 11) + int(helper==1)) if helper else 0
    words = struct.pack('<HHHH',0,tag,1234,2345)
    buffers = [label+' '+data.hex() for label,data in (('rooms',rooms),('cells',cells),('words',words))]
    # -1 floor traverses at equality/above; -1 ceiling below only.
    allowed = {0: {-1: relation in (0,1), 0: True, 1: False},
               1: {-1: relation==-1, 0: True, 1: False}}[sky][helper]
    final = 3 if link and allowed else current
    events = [(1,-1,current),(2,current*16+5,current),(-2,-1,current)]
    if link:
        kind = 4 if sky else 3
        events += [(kind,current*16+5,current),(-kind,-1,current)]
    events += [(-1,-1,final)]
    return [f'helper {helper}','before',*buffers,f'result {final} {final*16+5}',
            *('event '+' '.join(map(str,e)) for e in events),'after',*buffers]


@pytest.mark.parametrize('case',CASES)
def test_vertical_full_buffers_and_ordered_events(vertical_binary,case):
    directory,binary,address = vertical_binary
    output = invoke([str(binary),*map(str,case)],directory,'case-'+'-'.join(map(str,case)))
    assert output.splitlines() == expected(case,address)


@pytest.mark.parametrize('psx,psxpc',tuple(itertools.product((0,1),repeat=2)))
def test_vertical_gate_selection_only(psx,psxpc,tmp_path):
    # Selection only, not four architecture/backend builds.
    source = (ROOT/'SPEC_PSXPC_N/GETSTUFF.C').read_text()
    branch = source.split('if (v0 == -1)',1)[1].split('//loc_78AAC',1)[0]
    output = invoke(['g++','-E','-P','-x','c++',f'-DPSX_VERSION={psx}',
                     f'-DPSXPC_TEST={psxpc}','-'],tmp_path,'preprocess',input=branch)
    assert ('if (y < r->minfloor)' in output) == bool(psx and psxpc)
    assert ('if (y >= room->minfloor)' in output) == (not (psx and psxpc))


def test_vertical_matrix_independence():
    # Reconstruct separately in a different iteration order, no producer import.
    independent = {(r,m,z,d,h,l,s) for s in range(2) for l in range(2)
                   for h in (-1,0,1) for d in (-1,0,1) for z in (512,1024,1536)
                   for m in (512,1024,1536) for r in (1,2)}
    assert len(CASES) == len(set(CASES)) == 648
    assert set(CASES) == independent
    controls = [c for c in CASES if c[4:]==(-1,1,0)]
    assert len(controls) == 54
    assert all(sum(c[3]==d for c in controls)==18 for d in (-1,0,1))
    # Both plausible incomplete corrections must be observably discriminated.
    assert any((c[1]+c[3] < c[2]) != (c[3]<0) for c in controls)
    assert all((c[3]>=0) != (c[3]<0) for c in controls)
