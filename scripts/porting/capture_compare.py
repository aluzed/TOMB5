#!/usr/bin/env python3
"""Compare two deterministic frame captures (RMIG-007).

Usage:
    python3 scripts/porting/capture_compare.py --a cap32.bmp --b cap64.bmp \
        --out-dir docs/porting/replay

The PSX renderer is integer-exact, so two runs of the same binary must
produce byte-identical images.  Between 32-bit and 64-bit builds the
geometry is expected to be identical; colour/filtering differences are
reported separately with a global-gain estimate and a tolerance count.
"""

import argparse
import hashlib
import os

from PIL import Image, ImageChops


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def compare(a_path, b_path, out_dir):
    a = Image.open(a_path).convert("RGB")
    b = Image.open(b_path).convert("RGB")
    if a.size != b.size:
        raise SystemExit("size mismatch: %s vs %s" % (a.size, b.size))

    pa = list(a.getdata())
    pb = list(b.getdata())

    n = len(pa)
    diff = 0
    sum_a = 0
    sum_aa = 0
    sum_ab = 0

    for ca, cb in zip(pa, pb):
        for x, y in zip(ca, cb):
            diff += abs(x - y)
        for x, y in zip(ca, cb):
            sum_a += x
            sum_aa += x * x
            sum_ab += x * y

    mean_diff = diff / (n * 3.0)
    gain = sum_ab / sum_aa if sum_aa else 1.0

    # Error after applying the least-squares global gain to A.
    err_after = 0
    within = 0
    for ca, cb in zip(pa, pb):
        worst = 0
        for x, y in zip(ca, cb):
            d = abs(int(round(x * gain)) - y)
            err_after += d
            if d > worst:
                worst = d
        if worst <= 8:
            within += 1

    diff_img = ImageChops.difference(a, b)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        a.save(os.path.join(out_dir, "ref32.png"))
        b.save(os.path.join(out_dir, "ref64.png"))
        diff_img.save(os.path.join(out_dir, "diff32_64.png"))
        side = Image.new("RGB", (a.width * 2, a.height))
        side.paste(a, (0, 0))
        side.paste(b, (a.width, 0))
        side.save(os.path.join(out_dir, "side32_64.png"))

    print("A %s sha256=%s" % (a_path, sha256(a_path)))
    print("B %s sha256=%s" % (b_path, sha256(b_path)))
    print("size=%dx%d pixels=%d" % (a.width, a.height, n))
    print("mean_abs_diff=%.3f" % mean_diff)
    print("global_gain=%.6f" % gain)
    print("mean_abs_diff_after_gain=%.3f" % (err_after / (n * 3.0)))
    print("pixels_within_8_after_gain=%d (%.2f%%)" % (within, 100.0 * within / n))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", required=True, help="reference capture (32-bit)")
    parser.add_argument("--b", required=True, help="capture to compare (64-bit)")
    parser.add_argument("--out-dir", default=None)
    args = parser.parse_args()
    compare(args.a, args.b, args.out_dir)


if __name__ == "__main__":
    main()
