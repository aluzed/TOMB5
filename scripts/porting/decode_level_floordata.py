#!/usr/bin/env python3
"""Decode PSX/PC level floor data, items and room portals from a runtime dump.

The port relocates the level file into a single arena at level load (see
``LoadLevel``/``relocate`` in ``GAME/SETUP.C``): room array, then for every
room its ``data``/``door``/``floor``/``light``/``mesh`` blocks, then
``floor_data``.  Dumping that arena with gdb is enough to rebuild the whole
level database offline:

    dump binary memory /tmp/lv3_arena.bin room (char*)floor_data+65536
    dump binary memory /tmp/lv3_items.bin items items+level_items

Usage:

    python3 scripts/porting/decode_level_floordata.py dump \
        --arena lv3_arena.bin --items lv3_items.bin \
        --room-ptr 0x... --floor-ptr 0x...

``--room-ptr``/``--floor-ptr`` are the absolute addresses printed by the gdb
probe (``printf "%p", room`` / ``printf "%p", floor_data``); they are needed
to turn the relocated pointers stored in the arena into arena offsets.

``--selftest`` decodes a synthetic level built in memory and checks the
results, so the decoder itself can be validated without the game.
"""

import argparse
import struct
import sys

ROOM_INFO_SIZE = 80
FLOOR_INFO_SIZE = 8
ITEM_INFO_SIZE = 144

TRIGGER_TYPE = 4

TRIGGER_TYPES = {
    0: 'TRIGGER', 1: 'PAD', 2: 'SWITCH', 3: 'KEY', 4: 'PICKUP', 5: 'HEAVY',
    6: 'ANTIPAD', 7: 'COMBAT', 8: 'DUMMY', 9: 'ANTITRIGGER', 10: 'HEAVYSWITCH',
    11: 'HEAVYANTI', 12: 'MONKEY', 13: 'SKELETON', 14: 'TIGHTROPE',
    15: 'CRAWLDUCK', 16: 'CLIMB',
}

TARGET_TYPES = {
    0: 'OBJECT', 1: 'CAMERA', 2: 'SINK', 3: 'FLIPMAP', 4: 'FLIPON', 5: 'FLIPOFF',
    6: 'TARGET', 7: 'FINISH', 8: 'CD', 9: 'FLIPEFFECT', 10: 'SECRET',
    11: 'BODYBAG', 12: 'FLYBY', 13: 'CUTSCENE',
}


class LevelDecoder:
    def __init__(self, arena, items, room_ptr, floor_ptr, number_rooms=None):
        self.arena = arena
        self.items_bin = items
        self.room_ptr = room_ptr
        self.floor_ptr = floor_ptr
        self.number_rooms = number_rooms if number_rooms is not None else len(arena) // ROOM_INFO_SIZE
        self.rooms = [self._room(i) for i in range(self.number_rooms)]

    # -- low level -----------------------------------------------------------
    def _u16(self, off):
        if off < 0 or off + 2 > len(self.arena):
            return 0x8000
        return struct.unpack_from('<H', self.arena, off)[0]

    def _room(self, i):
        base = i * ROOM_INFO_SIZE
        r = {}
        r['index'] = i
        r['data'] = struct.unpack_from('<I', self.arena, base + 0)[0]
        r['door'] = struct.unpack_from('<I', self.arena, base + 4)[0]
        r['floor'] = struct.unpack_from('<I', self.arena, base + 8)[0]
        r['x'] = struct.unpack_from('<i', self.arena, base + 20)[0]
        r['y'] = struct.unpack_from('<i', self.arena, base + 24)[0]
        r['z'] = struct.unpack_from('<i', self.arena, base + 28)[0]
        r['minfloor'] = struct.unpack_from('<i', self.arena, base + 32)[0]
        r['maxceiling'] = struct.unpack_from('<i', self.arena, base + 36)[0]
        r['x_size'] = struct.unpack_from('<h', self.arena, base + 40)[0]
        r['y_size'] = struct.unpack_from('<h', self.arena, base + 42)[0]
        r['flip'] = self.arena[base + 53]
        r['item_number'] = struct.unpack_from('<h', self.arena, base + 72)[0]
        r['fx_number'] = struct.unpack_from('<h', self.arena, base + 74)[0]
        r['flipped_room'] = struct.unpack_from('<h', self.arena, base + 76)[0]
        r['flags'] = struct.unpack_from('<H', self.arena, base + 78)[0]
        return r

    def cell(self, room, cx, cz):
        """FLOOR_INFO of cell (cx, cz), or None when outside the dump."""
        off = (room['floor'] - self.room_ptr) + (cz * room['x_size'] + cx) * FLOOR_INFO_SIZE
        if off < 0 or off + FLOOR_INFO_SIZE > len(self.arena):
            return None
        index = struct.unpack_from('<H', self.arena, off)[0]
        fxbox = struct.unpack_from('<H', self.arena, off + 2)[0]
        return {
            'index': index,
            'fx': fxbox & 0xF,
            'box': fxbox >> 4,
            'pit_room': self.arena[off + 4],
            'floor': struct.unpack_from('<b', self.arena, off + 5)[0] * 256,
            'sky_room': self.arena[off + 6],
            'ceiling': struct.unpack_from('<b', self.arena, off + 7)[0] * 256,
        }

    def word(self, i):
        return self._u16((self.floor_ptr - self.room_ptr) + i * 2)

    # -- high level ----------------------------------------------------------
    def chain(self, index):
        """Decode the floor-data chain starting at short index ``index``."""
        feats = []
        i = index
        for _ in range(400):
            w = self.word(i)
            fn = w & 0x1F
            end = bool(w & 0x8000)
            if fn == TRIGGER_TYPE:
                ttype = (w >> 8) & 0x3F
                flags = self.word(i + 1)
                j = i + 2
                targets = []
                while True:
                    tw = self.word(j)
                    j += 1
                    targets.append({'action': (tw & 0x3FFF) >> 10,
                                    'value': tw & 0x3FF,
                                    'raw': tw})
                    if tw & 0x8000:
                        break
                feats.append({'kind': 'TRIGGER', 'type': ttype,
                              'type_name': TRIGGER_TYPES.get(ttype, '?'),
                              'flags': flags, 'targets': targets, 'at': i})
                i = j
            elif fn == 2:
                feats.append({'kind': 'TILT', 'at': i})
                i += 2
            elif fn in (7, 12, 13):
                feats.append({'kind': 'SPLIT', 'fn': fn, 'at': i})
                i += 2
            else:
                feats.append({'kind': 'FUNC', 'fn': fn, 'at': i})
                i += 1
            if end:
                break
        return feats

    def triggers(self):
        out = []
        for room in self.rooms:
            for cz in range(max(room['y_size'], 0)):
                for cx in range(max(room['x_size'], 0)):
                    f = self.cell(room, cx, cz)
                    if not f or not f['index']:
                        continue
                    for feat in self.chain(f['index']):
                        if feat['kind'] != 'TRIGGER':
                            continue
                        out.append({
                            'room': room['index'],
                            'cx': cx, 'cz': cz,
                            'x': room['x'] + cx * 1024 + 512,
                            'z': room['z'] + cz * 1024 + 512,
                            'floor': f['floor'],
                            'trigger': feat,
                        })
        return out

    def items(self):
        n = len(self.items_bin) // ITEM_INFO_SIZE
        out = []
        for i in range(n):
            base = i * ITEM_INFO_SIZE
            out.append({
                'index': i,
                'object_number': struct.unpack_from('<h', self.items_bin, base + 12)[0],
                'anim_number': struct.unpack_from('<h', self.items_bin, base + 20)[0],
                'room_number': struct.unpack_from('<h', self.items_bin, base + 24)[0],
                'ocb': struct.unpack_from('<h', self.items_bin, base + 44)[0],
                'x': struct.unpack_from('<i', self.items_bin, base + 64)[0],
                'y': struct.unpack_from('<i', self.items_bin, base + 68)[0],
                'z': struct.unpack_from('<i', self.items_bin, base + 72)[0],
            })
        return out

    def portals(self, room_index):
        """Decode the door (portal) array of a room.

        Layout: short count, then ``count`` blocks of 16 shorts; the first word
        of each block is the destination room number.
        """
        room = self.rooms[room_index]
        off = room['door'] - self.room_ptr
        if room['door'] == 0 or off < 0 or off + 2 > len(self.arena):
            return []
        count = struct.unpack_from('<h', self.arena, off)[0]
        out = []
        off += 2
        for _ in range(max(0, min(count, 64))):
            vals = struct.unpack_from('<16h', self.arena, off)
            out.append({'room': vals[0], 'raw': vals})
            off += 32
        return out


def describe(feat):
    parts = []
    for t in feat['targets']:
        parts.append('%s(%d)' % (TARGET_TYPES.get(t['action'], 'TO_%d' % t['action']), t['value']))
    return '%s flags=0x%04x -> %s' % (feat['type_name'], feat['flags'], ', '.join(parts))


def dump(args):
    arena = open(args.arena, 'rb').read()
    items = open(args.items, 'rb').read()
    dec = LevelDecoder(arena, items, args.room_ptr, args.floor_ptr, args.rooms)

    print('== items ==')
    for it in dec.items():
        print('item %3d obj %3d room %3d ocb %-5d at %d,%d,%d' %
              (it['index'], it['object_number'], it['room_number'], it['ocb'],
               it['x'], it['y'], it['z']))

    print('== triggers ==')
    for t in dec.triggers():
        print('room %3d cell(%d,%d) %d,%d floor=%d : %s' %
              (t['room'], t['cx'], t['cz'], t['x'], t['z'], t['floor'], describe(t['trigger'])))

    if args.portals:
        print('== portals ==')
        for index in args.portals:
            print('room %d -> %s' % (index, [p['room'] for p in dec.portals(index)]))


def selftest():
    """Build a 2-room synthetic level and check the decoded values."""
    number_rooms = 2
    floor0 = number_rooms * ROOM_INFO_SIZE
    floor1 = floor0 + FLOOR_INFO_SIZE
    door0 = floor1 + FLOOR_INFO_SIZE
    floor_data = door0 + 2 + 16 * 2          # count + one 32-byte door block
    arena = bytearray(floor_data + 64)

    def put16(off, value):
        struct.pack_into('<H', arena, off, value & 0xFFFF)

    def put32(off, value):
        struct.pack_into('<I', arena, off, value & 0xFFFFFFFF)

    # room 0: 1x1 cell, room 1: 1x1 cell, sharing one door block
    room_ptr = 0x10000000

    def room(i, floor_off, door_off, flip, flipped):
        base = i * ROOM_INFO_SIZE
        put32(base + 4, room_ptr + door_off)
        put32(base + 8, room_ptr + floor_off)
        struct.pack_into('<i', arena, base + 20, i * 1024)
        struct.pack_into('<i', arena, base + 28, 0)
        struct.pack_into('<h', arena, base + 40, 1)
        struct.pack_into('<h', arena, base + 42, 1)
        arena[base + 53] = flip
        struct.pack_into('<h', arena, base + 76, flipped)

    room(0, floor0, door0, 2, 1)
    room(1, floor1, door0, 2, 0)

    # room 0 cell -> trigger chain at short index 1:
    #   word 1 : header, type TRIGGER(4) + action PAD(1) << 8
    #   word 2 : flags 0x3E00
    #   word 3 : target  TO_OBJECT(0) item 7, no end bit
    #   word 4 : target  TO_FLIPMAP(3) flip 2, end bit
    put16(floor0, 1)
    struct.pack_into('<b', arena, floor0 + 5, 3)
    # room 1 cell -> no floor data
    put16(floor1, 0)

    # door block of room 0 -> room 1
    put16(door0, 1)
    struct.pack_into('<h', arena, door0 + 2, 1)

    fd_off = floor_data
    put16(fd_off + 1 * 2, 4 | (1 << 8))
    put16(fd_off + 2 * 2, 0x3E00)
    put16(fd_off + 3 * 2, 0x0007)
    put16(fd_off + 4 * 2, 0x8000 | (3 << 10) | 2)

    items = bytearray(ITEM_INFO_SIZE * 2)
    struct.pack_into('<h', items, 12, 61)          # item 0 object
    struct.pack_into('<h', items, 24, 3)           # room
    struct.pack_into('<h', items, 44, 512)         # ocb
    struct.pack_into('<i', items, 64, 100)
    struct.pack_into('<i', items, 68, -200)
    struct.pack_into('<i', items, 72, 300)

    dec = LevelDecoder(bytes(arena), bytes(items), room_ptr, room_ptr + floor_data, number_rooms)

    fail = []

    def check(cond, msg):
        if not cond:
            fail.append(msg)

    check(len(dec.rooms) == 2, 'room count')
    check(dec.rooms[0]['flipped_room'] == 1, 'flipped_room')
    check(dec.rooms[0]['flip'] == 2, 'flip number')
    cell = dec.cell(dec.rooms[0], 0, 0)
    check(cell is not None and cell['index'] == 1, 'floor index')
    check(cell['floor'] == 768, 'floor height')

    trigs = dec.triggers()
    check(len(trigs) == 1, 'one trigger found')
    if trigs:
        t = trigs[0]
        check(t['room'] == 0, 'trigger room')
        check(t['trigger']['type_name'] == 'PAD', 'trigger type')
        check(t['trigger']['flags'] == 0x3E00, 'trigger flags')
        check([x['action'] for x in t['trigger']['targets']] == [0, 3], 'target actions')
        check([x['value'] for x in t['trigger']['targets']] == [7, 2], 'target values')

    its = dec.items()
    check(len(its) == 2, 'item count')
    check(its[0]['object_number'] == 61, 'item object')
    check(its[0]['room_number'] == 3, 'item room')
    check(its[0]['ocb'] == 512, 'item ocb')
    check((its[0]['x'], its[0]['y'], its[0]['z']) == (100, -200, 300), 'item position')

    ports = dec.portals(0)
    check(len(ports) == 1 and ports[0]['room'] == 1, 'portal destination')

    if fail:
        print('selftest FAILED: ' + ', '.join(fail))
        return 1

    print('selftest OK')
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--selftest', action='store_true')
    sub = parser.add_subparsers(dest='command')

    d = sub.add_parser('dump', help='decode a gdb arena dump')
    d.add_argument('--arena', required=True)
    d.add_argument('--items', required=True)
    d.add_argument('--room-ptr', required=True, type=lambda v: int(v, 0))
    d.add_argument('--floor-ptr', required=True, type=lambda v: int(v, 0))
    d.add_argument('--rooms', type=int, default=None)
    d.add_argument('--portals', type=int, nargs='*', default=[])

    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.command == 'dump':
        dump(args)
        return 0

    parser.print_help()
    return 1


if __name__ == '__main__':
    sys.exit(main())
