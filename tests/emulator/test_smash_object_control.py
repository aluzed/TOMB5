"""RE758 public synthetic actual-TU regression; no private imports or assets.

Compile the complete OBJECTS.C and retain its real wrapper AND consumer. Only
three external services are no-memory-effect ABI doubles. No unresolved symbols
are accepted. Requires g++ multilib; this is not a complete game build.
"""
import itertools
import json
from pathlib import Path
import struct
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[2]
CASES = tuple(itertools.product(range(2), range(4), range(2), range(2), range(4)))
HARNESS = r'''
#include "OBJECTS.H"
#include "BOX.H"
#include "ITEMS.H"
#include "TOMB4FX.H"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstddef>
static_assert(sizeof(void*) == 4 && sizeof(long) == 4, "i386 ABI required");
static_assert(sizeof(ITEM_INFO) == 144 && sizeof(box_info) == 8 &&
              sizeof(FLOOR_INFO) == 8 && sizeof(room_info) == 80, "layouts");
static_assert(offsetof(ITEM_INFO, mesh_bits) == 8 && offsetof(ITEM_INFO, flags) == 40 &&
              offsetof(ITEM_INFO, pos) == 64, "item fields");
static_assert(BOX_LAST == 32768 && BOX_BLOCKED == 16384 &&
              IFLAG_INVISIBLE == 256 && ITEM_ACTIVE == 1 && ITEM_DEACTIVATED == 2, "flags");
ITEM_INFO item_buffer[4]; box_info box_buffer[4];
FLOOR_INFO sector_buffer[8]; room_info room_buffer[1];
ITEM_INFO* items = item_buffer; box_info* boxes = box_buffer; room_info* room = room_buffer;
long SoundEffect(short sound, PHD_3DPOS* position, int flags) {
    printf("sound %d %ld %d\n", sound, (long)((char*)position-(char*)items), flags);
    return 0;
}
int ExplodingDeath2(short index, long mask, short flags) {
    printf("explode %d %ld %d\n", index, mask, flags); return 0;
}
void RemoveActiveItem(short index) { printf("remove %d\n", index); }
void dump(const char* name, const void* buffer, size_t size) {
    printf("%s ", name);
    for (size_t i=0; i<size; ++i) printf("%02x", ((const unsigned char*)buffer)[i]);
    puts("");
}
int main(int argc, char** argv) {
    if (argc != 6) return 2;
    int wrapper=atoi(argv[1]), index=atoi(argv[2]), last=atoi(argv[3]);
    int blocked=atoi(argv[4]), state=atoi(argv[5]);
    if (wrapper<0 || wrapper>1 || index<0 || index>3 || last<0 || last>1 ||
        blocked<0 || blocked>1 || state<0 || state>3) return 3;
    room[0].x=8192; room[0].z=-4096; room[0].x_size=2; room[0].floor=sector_buffer;
    for (int i=0; i<8; ++i) sector_buffer[i].box=i/2;
    for (int i=0; i<4; ++i) {
        boxes[i].left=3+i; boxes[i].right=13+i; boxes[i].top=23+i;
        boxes[i].bottom=33+i; boxes[i].height=200+i;
        boxes[i].overlap_index=(last ? BOX_LAST : 0) | (blocked ? BOX_BLOCKED : 0) | (7+i);
        items[i].pos.x_pos=8192+1024*i; items[i].pos.z_pos=-4096;
        items[i].pos.y_pos=512+i; items[i].mesh_bits=0x12345670u+i;
        items[i].flags=64+i; items[i].collidable=1; items[i].status=state;
    }
    unsigned char room_before[sizeof room_buffer];
    memcpy(room_before, room_buffer, sizeof room_buffer);
    if (wrapper) SmashObjectControl(index); else SmashObject(index);
    dump("items", item_buffer, sizeof item_buffer);
    dump("boxes", box_buffer, sizeof box_buffer);
    dump("sectors", sector_buffer, sizeof sector_buffer);
    dump("room-before", room_before, sizeof room_before);
    dump("room-after", room_buffer, sizeof room_buffer);
    return 0;
}
'''


def expected_output(index, last, blocked, state):
    """Independent byte construction from the public 32-bit layout, not TU output."""
    items = bytearray(576)
    boxes = bytearray(32)
    sectors = bytearray(64)
    for i in range(4):
        base = i * 144
        selected = i == index
        struct.pack_into('<I', items, base + 8, 65534 if selected else 0x12345670 + i)
        struct.pack_into('<H', items, base + 40, (64 + i) | (256 if selected else 0))
        struct.pack_into('<iii', items, base + 64, 8192 + 1024*i, 512+i, -4096)
        # Public ITEM_INFO bitfields: active, status:2, gravity, hit, collidable.
        struct.pack_into('<I', items, base + 132, 4 if selected else 32 | (state << 1))
        overlap = (last << 15) | (blocked << 14) | (7+i)
        if selected and last:
            overlap &= ~16384
        struct.pack_into('<BBBBhH', boxes, i*8, 3+i, 13+i, 23+i, 33+i, 200+i, overlap)
    for i in range(8):
        struct.pack_into('<H', sectors, i*8+2, (i//2) << 4)
    events = [f'sound 12 {index*144+64} 0', f'explode {index} -1 257']
    if state == 1:
        events.append(f'remove {index}')
    return events + [name+' '+buf.hex() for name, buf in
                     [('items', items), ('boxes', boxes), ('sectors', sectors)]]


@pytest.fixture(scope='module')
def smash_binary(tmp_path_factory):
    directory = tmp_path_factory.mktemp('smash-object-control')
    harness = directory / 'harness.cpp'
    harness.write_text(HARNESS)
    executable = directory / 'host'
    command = ['g++', '-m32', '-O0', '-Wno-narrowing', '-ffunction-sections',
               '-fdata-sections', '-fno-pie', '-no-pie', '-Wl,--gc-sections',
               '-DPSX_VERSION=1', '-DPSXPC_TEST=1', '-DNTSC_VERSION=1',
               '-DUSE_32_BIT_ADDR=1', '-DDEBUG_VERSION=0', '-DDISC_VERSION=1',
               '-IGAME', '-ISPEC_PSXPC_N', '-IEMULATOR', '-I/usr/include/SDL2',
               str(harness), 'GAME/OBJECTS.C', '-o', str(executable)]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
    (directory / 'compile.json').write_text(json.dumps(command))
    (directory / 'compile.log').write_text(result.stdout + result.stderr)
    assert result.returncode == 0, result.stderr
    return directory, executable


@pytest.mark.parametrize('wrapper,index,last,blocked,state', CASES)
def test_complete_buffers_and_ordered_events(smash_binary, wrapper, index, last, blocked, state):
    directory, executable = smash_binary
    case = (wrapper, index, last, blocked, state)
    command = [str(executable), *map(str, case)]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=5)
    key = '-'.join(map(str, case))
    (directory / (key+'.json')).write_text(json.dumps(dict(command=command,
        exit=result.returncode, stdout=result.stdout, stderr=result.stderr), indent=2))
    assert result.returncode == 0, result.stderr
    assert result.stderr == ''
    lines = result.stdout.splitlines()
    assert lines[-2].startswith('room-before ') and lines[-1].startswith('room-after ')
    assert len(bytes.fromhex(lines[-1].split()[1])) == 80
    assert lines[-2].split()[1] == lines[-1].split()[1], 'complete room changed'
    assert lines[:-2] == expected_output(index, last, blocked, state)


@pytest.mark.parametrize('psx,psxpc', [(0, 0), (0, 1), (1, 0), (1, 1)])
def test_backend_scope_preprocessor(psx, psxpc):
    # This is only a guard-selection check, NOT a build of other backends.
    source = (ROOT / 'GAME/OBJECTS.C').read_text()
    wrapper = source.split('void SmashObjectControl(short item_number)', 1)[1].split(
        'void BridgeFlatFloor', 1)[0]
    result = subprocess.run(['g++', '-E', '-P', '-x', 'c++',
                             f'-DPSX_VERSION={psx}', f'-DPSXPC_TEST={psxpc}', '-'],
                            input=wrapper, capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, result.stderr
    call = 'SmashObject(item_number);' if psx and psxpc else 'SmashObject(item_number << 16);'
    assert call in result.stdout
    assert result.stdout.count('SmashObject(') == 1


def test_matrix_is_cartesian():
    assert len(CASES) == len(set(CASES)) == 128
    assert set(CASES) == set(itertools.product(range(2), range(4), range(2), range(2), range(4)))
