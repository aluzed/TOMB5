#!/usr/bin/env python3
"""Extract the FMV streams of the PSX disc and (optionally) decode them to AVI.

The PlayStation version of Tomb Raider: Chronicles stores its movies as
``FMV0.STR`` .. ``FMV7.STR`` at the root of the ISO9660 volume.  The port has
no MDEC/STR decoder, so ``S_PlayFMV`` can hand playback to ``ffplay`` when
``TOMB5_FMV_DIR`` points at a directory containing ``FMV<n>.avi``.

Typical use (disc image in ``build/porting/data-ntsc/TOMB5.BIN``)::

    python3 scripts/porting/prepare_fmvs.py \\
        --disc build/porting/data-ntsc/TOMB5.BIN \\
        --out build/porting/fmv \\
        --jpsxdec /path/to/jpsxdec.jar

Without ``--jpsxdec`` only the ``.STR`` files are extracted.  Decoding needs
Java and a jpsxdec release (https://github.com/m35/jpsxdec/releases); the
resulting ``FMV<n>.avi`` files are what ``TOMB5_FMV_DIR`` expects.

The disc image may be a raw MODE2/2352 image (as shipped) or a plain
2048-byte/sector ISO.  Game data is never written into the repository's
tracked files: the default output lives under ``build/``.
"""

from __future__ import annotations

import argparse
import struct
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

SECTOR_MODES = {
    # sector size -> offset of the 2048-byte user data
    2352: 24,  # MODE2/2352 (sync + header + CD-XA subheader)
    2048: 0,   # plain ISO9660 image
}

PVD_LBA = 16
PVD_SIGNATURE = b"CD001"


@dataclass(frozen=True)
class IsoEntry:
    name: str
    lba: int
    size: int


def _sector_reader(disc: Path):
    """Return (read_sector, sector_size) for the disc image."""
    file_size = disc.stat().st_size
    for sector_size, user_offset in SECTOR_MODES.items():
        if file_size % sector_size:
            continue
        with disc.open("rb") as f:
            f.seek(PVD_LBA * sector_size)
            raw = f.read(sector_size)
        if raw[user_offset + 1:user_offset + 6] != PVD_SIGNATURE:
            continue

        def read_sector(lba: int, _size=sector_size, _offset=user_offset) -> bytes:
            with disc.open("rb") as f:
                f.seek(lba * _size)
                raw = f.read(_size)
            return raw[_offset:_offset + 2048]

        return read_sector, sector_size
    raise SystemExit(f"{disc}: ni image MODE2/2352 ni ISO9660 2048 reconnue")


def iter_iso_entries(disc: Path) -> list[IsoEntry]:
    """List the files of the root directory of an ISO9660 image."""
    read_sector, _ = _sector_reader(disc)
    pvd = read_sector(PVD_LBA)
    root = pvd[156:156 + 34]
    root_lba = struct.unpack_from("<I", root, 2)[0]
    root_size = struct.unpack_from("<I", root, 10)[0]

    entries: list[IsoEntry] = []
    for index in range((root_size + 2047) // 2048):
        data = read_sector(root_lba + index)
        offset = 0
        while offset < len(data):
            record_len = data[offset]
            if record_len == 0:
                break
            record = data[offset:offset + record_len]
            name_len = record[32]
            name = record[33:33 + name_len].decode("ascii", "replace")
            lba = struct.unpack_from("<I", record, 2)[0]
            size = struct.unpack_from("<I", record, 10)[0]
            flags = record[25]
            if name not in ("\x00", "\x01") and not (flags & 0x02):
                entries.append(IsoEntry(name, lba, size))
            offset += record_len
    return entries


def extract_fmvs(disc: Path, out_dir: Path) -> list[Path]:
    """Extract ``FMV*.STR`` from the disc into *out_dir*."""
    read_sector, _ = _sector_reader(disc)
    fmvs = sorted(
        (e for e in iter_iso_entries(disc) if e.name.upper().startswith("FMV")),
        key=lambda e: e.name,
    )
    if not fmvs:
        raise SystemExit(f"{disc}: aucun fichier FMV*.STR dans le repertoire racine")

    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for entry in fmvs:
        # ISO names carry a ";1" version suffix.
        base = entry.name.split(";", 1)[0]
        target = out_dir / base
        remaining = entry.size
        with target.open("wb") as out:
            lba = entry.lba
            while remaining > 0:
                chunk = read_sector(lba)[:min(2048, remaining)]
                out.write(chunk)
                remaining -= len(chunk)
                lba += 1
        written.append(target)
        print(f"[FMV] {base}: {entry.size} octets -> {target}")
    return written


def decode_fmvs(jpsxdec: Path, str_files: list[Path], out_dir: Path) -> list[Path]:
    """Decode the extracted streams with jpsxdec and normalise the file names."""
    if not jpsxdec.exists():
        raise SystemExit(f"jpsxdec introuvable: {jpsxdec}")

    decoded = []
    out_dir = out_dir.resolve()
    for source in str_files:
        source = source.resolve()
        subprocess.run(
            ["java", "-jar", str(jpsxdec), "-f", str(source),
             "-a", "video", "-quality", "high", "-dir", str(out_dir)],
            check=True,
            # jpsxdec drops debug00.log/index.log/save.log in its cwd; keep
            # them next to the generated media rather than in the repository.
            cwd=str(out_dir),
        )
        # jpsxdec writes "FMV0.STR[0].avi"; S_PlayFMV looks for "FMV0.avi".
        produced = out_dir / f"{source.name}[0].avi"
        target = out_dir / f"{source.stem}.avi"
        if produced.exists():
            produced.replace(target)
        elif not target.exists():
            raise SystemExit(f"jpsxdec n'a produit ni {produced} ni {target}")
        decoded.append(target)
        print(f"[FMV] {target.name} pret")
    return decoded


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--disc", type=Path,
                        default=Path("build/porting/data-ntsc/TOMB5.BIN"),
                        help="image du disque (MODE2/2352 ou ISO 2048)")
    parser.add_argument("--out", type=Path, default=Path("build/porting/fmv"),
                        help="repertoire de sortie (defaut: build/porting/fmv)")
    parser.add_argument("--jpsxdec", type=Path,
                        help="jpsxdec.jar pour decoder les flux en AVI")
    args = parser.parse_args(argv)

    str_files = extract_fmvs(args.disc, args.out)
    if args.jpsxdec:
        decode_fmvs(args.jpsxdec, str_files, args.out)
        print(f"\nTOMB5_FMV_DIR={args.out}")
    else:
        print("\nFlux extraits. Relancer avec --jpsxdec pour produire les AVI.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
