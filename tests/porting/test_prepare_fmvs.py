"""Tests for the FMV extraction helper.

The real disc contains ``FMV0.STR`` .. ``FMV7.STR``; the tests build a tiny
synthetic ISO9660 volume (both MODE2/2352 and plain 2048-byte images) so the
parser and extractor can be checked without any game data.
"""
from __future__ import annotations

import importlib.util
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "porting" / "prepare_fmvs.py"

SECTOR_COUNT = 21
PVD_LBA = 16
ROOT_LBA = 17
FMV0_LBA = 18
FMV0_SIZE = 4000
FMV1_LBA = 20
FMV1_SIZE = 1000


def module():
    spec = importlib.util.spec_from_file_location("prepare_fmvs", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def dir_record(name: bytes, lba: int, size: int, flags: int = 0) -> bytes:
    length = 33 + len(name)
    if length % 2:
        length += 1
    record = bytearray(length)
    record[0] = length
    struct.pack_into("<I", record, 2, lba)
    struct.pack_into("<I", record, 10, size)
    record[25] = flags
    record[28:30] = b"\x01\x00"
    record[32] = len(name)
    record[33:33 + len(name)] = name
    return bytes(record)


def payload(lba: int) -> bytes:
    return bytes([0xA0 + lba]) * 2048


def build_disc(path: Path, sector_size: int, with_fmvs: bool = True) -> None:
    sectors = {}

    pvd = bytearray(2048)
    pvd[0] = 1
    pvd[1:6] = b"CD001"
    struct.pack_into("<H", pvd, 128, 2048)
    pvd[156:156 + 34] = dir_record(b"\x00", ROOT_LBA, 2048, flags=2)
    sectors[PVD_LBA] = bytes(pvd)

    root = b""
    if with_fmvs:
        root += dir_record(b"FMV0.STR;1", FMV0_LBA, FMV0_SIZE)
        root += dir_record(b"FMV1.STR;1", FMV1_LBA, FMV1_SIZE)
    sectors[ROOT_LBA] = root.ljust(2048, b"\x00")

    if with_fmvs:
        for lba, value in ((FMV0_LBA, 0xAA), (FMV0_LBA + 1, 0xBB),
                           (FMV1_LBA, 0xCC)):
            sectors[lba] = bytes([value]) * 2048

    with path.open("wb") as out:
        for lba in range(SECTOR_COUNT):
            data = sectors.get(lba, b"\x00" * 2048)
            if sector_size == 2048:
                out.write(data)
            else:
                header = bytes([lba // 75 // 60, lba // 75 % 60, lba % 75, 2])
                out.write(b"\x00" + b"\xff" * 10 + b"\x00" + header)
                out.write(b"\x00\x00\x08\x00" * 2)
                out.write(data)
                out.write(b"\x00" * (2352 - 24 - 2048))


@pytest.mark.parametrize("sector_size", [2352, 2048])
def test_extract_fmvs(tmp_path: Path, sector_size: int):
    mod = module()
    disc = tmp_path / "disc.bin"
    build_disc(disc, sector_size)

    names = [e.name for e in mod.iter_iso_entries(disc)]
    assert names == ["FMV0.STR;1", "FMV1.STR;1"]

    out = tmp_path / "fmv"
    written = mod.extract_fmvs(disc, out)
    assert [p.name for p in written] == ["FMV0.STR", "FMV1.STR"]

    fmv0 = (out / "FMV0.STR").read_bytes()
    assert len(fmv0) == FMV0_SIZE
    assert fmv0[:2048] == bytes([0xAA]) * 2048
    assert fmv0[2048:] == bytes([0xBB]) * (FMV0_SIZE - 2048)

    fmv1 = (out / "FMV1.STR").read_bytes()
    assert len(fmv1) == FMV1_SIZE
    assert fmv1 == bytes([0xCC]) * FMV1_SIZE


def test_extract_rejects_disc_without_fmvs(tmp_path: Path):
    mod = module()
    disc = tmp_path / "disc.bin"
    build_disc(disc, 2352, with_fmvs=False)

    with pytest.raises(SystemExit):
        mod.extract_fmvs(disc, tmp_path / "fmv")
