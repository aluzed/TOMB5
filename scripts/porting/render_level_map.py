#!/usr/bin/env python3
"""Render a top-down map of a level from the offline floor-data decoder.

Usage:
    python3 scripts/porting/render_level_map.py \
        --arena lv3_arena.bin --items lv3_items.bin \
        --room-ptr 0x... --floor-ptr 0x... --rooms 125 \
        --out map.png [--xmin 35000 --xmax 47000 --zmin 46000 --zmax 58000]

Cells are painted by floor height (dark = high, light = low) and labelled
with their room number; items are drawn as dots labelled with the object
number.  Useful to reason about level connectivity without running the game.
"""
import argparse
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from decode_level_floordata import LevelDecoder  # noqa: E402


def height_colour(h):
    if h == -32512:
        return (32, 32, 40)          # no floor
    # -20000 (high) .. +20000 (low) mapped to bright -> dark
    v = max(0, min(255, int(235 - (h + 12000) / 24000 * 180)))
    return (v, v, max(0, v - 20))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--arena', required=True)
    ap.add_argument('--items', required=True)
    ap.add_argument('--room-ptr', required=True, type=lambda v: int(v, 0))
    ap.add_argument('--floor-ptr', required=True, type=lambda v: int(v, 0))
    ap.add_argument('--rooms', type=int, default=None)
    ap.add_argument('--out', required=True)
    ap.add_argument('--scale', type=int, default=128, help='world units per pixel')
    ap.add_argument('--xmin', type=int, default=None)
    ap.add_argument('--xmax', type=int, default=None)
    ap.add_argument('--zmin', type=int, default=None)
    ap.add_argument('--zmax', type=int, default=None)
    ap.add_argument('--rooms-filter', type=int, nargs='*', default=None)
    args = ap.parse_args(argv)

    dec = LevelDecoder(open(args.arena, 'rb').read(),
                       open(args.items, 'rb').read(),
                       args.room_ptr, args.floor_ptr, args.rooms)

    xs = [r['x'] for r in dec.rooms] + [r['x'] + r['x_size'] * 1024 for r in dec.rooms]
    zs = [r['z'] for r in dec.rooms] + [r['z'] + r['y_size'] * 1024 for r in dec.rooms]
    xmin = args.xmin if args.xmin is not None else min(xs)
    xmax = args.xmax if args.xmax is not None else max(xs)
    zmin = args.zmin if args.zmin is not None else min(zs)
    zmax = args.zmax if args.zmax is not None else max(zs)

    s = args.scale
    w = max(1, (xmax - xmin) // s + 2)
    h = max(1, (zmax - zmin) // s + 2)
    img = Image.new('RGB', (w, h), (8, 8, 12))
    d = ImageDraw.Draw(img)

    def px(x, z):
        return (int((x - xmin) / s), int((z - zmin) / s))

    for r in dec.rooms:
        if args.rooms_filter and r['index'] not in args.rooms_filter:
            continue
        for cz in range(max(r['y_size'], 0)):
            for cx in range(max(r['x_size'], 0)):
                c = dec.cell(r, cx, cz)
                if not c:
                    continue
                x0 = r['x'] + cx * 1024
                z0 = r['z'] + cz * 1024
                p0 = px(x0, z0)
                p1 = px(x0 + 1023, z0 + 1023)
                col = height_colour(c['floor'])
                d.rectangle([p0, p1], fill=col)
                if c['index']:
                    d.point(p0, fill=(255, 80, 80))

    # room labels
    for r in dec.rooms:
        if args.rooms_filter and r['index'] not in args.rooms_filter:
            continue
        if r['x_size'] <= 0:
            continue
        p = px(r['x'] + 256, r['z'] + 256)
        if -20 <= p[0] <= w and -20 <= p[1] <= h:
            d.text((p[0] + 1, p[1] + 1), str(r['index']), fill=(120, 200, 255))

    # items
    for it in dec.items():
        p = px(it['x'], it['z'])
        if 0 <= p[0] < w and 0 <= p[1] < h:
            d.ellipse([p[0] - 1, p[1] - 1, p[0] + 1, p[1] + 1], fill=(255, 200, 0))
            d.text((p[0] + 2, p[1] - 3), str(it['object_number']), fill=(230, 230, 160))

    img = img.resize((w * 2, h * 2), Image.NEAREST)
    img.save(args.out)
    print('wrote %s (%dx%d)' % (args.out, w * 2, h * 2))


if __name__ == '__main__':
    sys.exit(main())
