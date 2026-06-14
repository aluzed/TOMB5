#!/usr/bin/env python3
"""Extract a small per-function MIPS disassembly dump from the verified PS-X payload.

The dump is intentionally written under `build/reverse/re007/` by default because
it contains original game instructions/bytes and must not be committed.
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path

TEXT_BASE_DEFAULT = 0x80010000
MAP_DEFAULT = "docs/reverse/generated/repo-function-map.csv"
PAYLOAD_DEFAULT = "build/reverse/extracted/SLUS_013.11.payload.bin"
OUT_DEFAULT = "build/reverse/re007/original"

REG = [
    "zero", "at", "v0", "v1", "a0", "a1", "a2", "a3",
    "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7",
    "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",
    "t8", "t9", "k0", "k1", "gp", "sp", "fp", "ra",
]

SPECIAL = {
    0x00: "sll", 0x02: "srl", 0x03: "sra", 0x04: "sllv", 0x06: "srlv", 0x07: "srav",
    0x08: "jr", 0x09: "jalr", 0x0c: "syscall", 0x0d: "break",
    0x10: "mfhi", 0x11: "mthi", 0x12: "mflo", 0x13: "mtlo",
    0x18: "mult", 0x19: "multu", 0x1a: "div", 0x1b: "divu",
    0x20: "add", 0x21: "addu", 0x22: "sub", 0x23: "subu", 0x24: "and", 0x25: "or",
    0x26: "xor", 0x27: "nor", 0x2a: "slt", 0x2b: "sltu",
}
REGIMM = {0x00: "bltz", 0x01: "bgez", 0x10: "bltzal", 0x11: "bgezal"}
OP = {
    0x02: "j", 0x03: "jal", 0x04: "beq", 0x05: "bne", 0x06: "blez", 0x07: "bgtz",
    0x08: "addi", 0x09: "addiu", 0x0a: "slti", 0x0b: "sltiu", 0x0c: "andi", 0x0d: "ori",
    0x0e: "xori", 0x0f: "lui", 0x20: "lb", 0x21: "lh", 0x22: "lwl", 0x23: "lw",
    0x24: "lbu", 0x25: "lhu", 0x26: "lwr", 0x28: "sb", 0x29: "sh", 0x2a: "swl",
    0x2b: "sw", 0x2e: "swr", 0x30: "lwc0", 0x31: "lwc1", 0x32: "lwc2", 0x33: "lwc3",
    0x38: "swc0", 0x39: "swc1", 0x3a: "swc2", 0x3b: "swc3",
}


@dataclass(frozen=True)
class FunctionRow:
    final_psx_address: str
    beta_psx_address: str
    repo_function: str
    file: str
    line: int
    markers: str
    mapping_status: str
    ghidra_entry: str
    ghidra_name: str
    body_size: int


def parse_int(text: str | None) -> int:
    try:
        return int(text or "0")
    except ValueError:
        return 0


def parse_addr(text: str) -> int:
    value = int(text, 16)
    if value < 0x80000000:
        value |= 0x80000000
    return value


def safe_name(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", text).strip("_") or "function"


def read_map(path: Path) -> list[FunctionRow]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = []
        for raw in csv.DictReader(f):
            rows.append(FunctionRow(
                final_psx_address=raw.get("final_psx_address", ""),
                beta_psx_address=raw.get("beta_psx_address", ""),
                repo_function=raw.get("repo_function", ""),
                file=raw.get("file", ""),
                line=parse_int(raw.get("line")),
                markers=raw.get("markers", ""),
                mapping_status=raw.get("mapping_status", ""),
                ghidra_entry=raw.get("ghidra_entry", ""),
                ghidra_name=raw.get("ghidra_name", ""),
                body_size=parse_int(raw.get("body_size")),
            ))
        return rows


def resolve(rows: list[FunctionRow], selector: str) -> FunctionRow:
    needle = selector.lower()
    matches = []
    for row in rows:
        if needle in {row.repo_function.lower(), row.ghidra_name.lower(), row.final_psx_address.lower(), row.ghidra_entry.lower()}:
            matches.append(row)
    if not matches and needle.startswith("0x"):
        addr = parse_addr(needle)
        matches = [row for row in rows if row.final_psx_address and parse_addr(row.final_psx_address) == addr]
    if not matches:
        raise SystemExit(f"No mapped function matched selector: {selector}")
    mapped = [row for row in matches if row.mapping_status == "mapped" and row.body_size > 0]
    chosen = (mapped or matches)[0]
    if len(matches) > 1:
        print(f"warning: {len(matches)} matches for {selector}; using {chosen.repo_function} {chosen.final_psx_address} {chosen.file}:{chosen.line}")
    return chosen


def sext16(value: int) -> int:
    return value - 0x10000 if value & 0x8000 else value


def disasm_word(word: int, pc: int) -> str:
    op = (word >> 26) & 0x3f
    rs = (word >> 21) & 0x1f
    rt = (word >> 16) & 0x1f
    rd = (word >> 11) & 0x1f
    sh = (word >> 6) & 0x1f
    fn = word & 0x3f
    imm = word & 0xffff
    simm = sext16(imm)
    target = word & 0x03ffffff

    if word == 0:
        return "nop"
    if op == 0x00:
        m = SPECIAL.get(fn, f"special_0x{fn:02x}")
        if m in {"sll", "srl", "sra"}:
            return f"{m} ${REG[rd]}, ${REG[rt]}, {sh}"
        if m in {"sllv", "srlv", "srav"}:
            return f"{m} ${REG[rd]}, ${REG[rt]}, ${REG[rs]}"
        if m == "jr":
            return f"jr ${REG[rs]}"
        if m == "jalr":
            return f"jalr ${REG[rd]}, ${REG[rs]}"
        if m in {"mfhi", "mflo"}:
            return f"{m} ${REG[rd]}"
        if m in {"mthi", "mtlo"}:
            return f"{m} ${REG[rs]}"
        if m in {"mult", "multu", "div", "divu"}:
            return f"{m} ${REG[rs]}, ${REG[rt]}"
        if m in {"syscall", "break"}:
            return m
        return f"{m} ${REG[rd]}, ${REG[rs]}, ${REG[rt]}"
    if op == 0x01:
        m = REGIMM.get(rt, f"regimm_0x{rt:02x}")
        dest = pc + 4 + (simm << 2)
        return f"{m} ${REG[rs]}, 0x{dest:08x}"
    if op in {0x02, 0x03}:
        m = OP[op]
        dest = ((pc + 4) & 0xf0000000) | (target << 2)
        return f"{m} 0x{dest:08x}"
    if op in {0x04, 0x05}:
        m = OP[op]
        dest = pc + 4 + (simm << 2)
        return f"{m} ${REG[rs]}, ${REG[rt]}, 0x{dest:08x}"
    if op in {0x06, 0x07}:
        m = OP[op]
        dest = pc + 4 + (simm << 2)
        return f"{m} ${REG[rs]}, 0x{dest:08x}"
    if op == 0x0f:
        return f"lui ${REG[rt]}, 0x{imm:04x}"
    if op in {0x08, 0x09, 0x0a, 0x0b}:
        return f"{OP[op]} ${REG[rt]}, ${REG[rs]}, {simm}"
    if op in {0x0c, 0x0d, 0x0e}:
        return f"{OP[op]} ${REG[rt]}, ${REG[rs]}, 0x{imm:04x}"
    if op in {0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x28, 0x29, 0x2a, 0x2b, 0x2e, 0x30, 0x31, 0x32, 0x33, 0x38, 0x39, 0x3a, 0x3b}:
        return f"{OP[op]} ${REG[rt]}, {simm}(${REG[rs]})"
    return f".word 0x{word:08x}"


def dump_function(repo: Path, row: FunctionRow, payload: Path, text_base: int, out_dir: Path, max_bytes: int | None) -> tuple[Path, Path, int]:
    start = parse_addr(row.final_psx_address or row.ghidra_entry)
    size = row.body_size or max_bytes or 128
    if max_bytes is not None:
        size = min(size, max_bytes)
    size -= size % 4
    if size <= 0:
        raise SystemExit(f"Invalid dump size for {row.repo_function}: {size}")
    start_off = start - text_base
    if start_off < 0:
        raise SystemExit(f"Address 0x{start:08x} is before text base 0x{text_base:08x}")
    data = payload.read_bytes()
    if start_off + size > len(data):
        raise SystemExit(f"Requested range exceeds payload: offset=0x{start_off:x} size=0x{size:x} payload=0x{len(data):x}")

    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{safe_name(row.repo_function)}_{start:08x}"
    csv_path = out_dir / f"{stem}.csv"
    md_path = out_dir / f"{stem}.md"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        fields = ["index", "ram_address", "payload_offset", "word_le_hex", "instruction"]
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for idx, off in enumerate(range(start_off, start_off + size, 4)):
            pc = text_base + off
            word = int.from_bytes(data[off:off + 4], "little")
            writer.writerow({
                "index": idx,
                "ram_address": f"0x{pc:08x}",
                "payload_offset": f"0x{off:06x}",
                "word_le_hex": f"0x{word:08x}",
                "instruction": disasm_word(word, pc),
            })
    lines = [
        f"# Original MIPS dump — {row.repo_function}",
        "",
        "This file contains original game instructions/bytes. Keep it under ignored `build/reverse/re007/`; do not commit.",
        "",
        f"- function: `{row.repo_function}`",
        f"- source: `{row.file}:{row.line}`",
        f"- final PSX address: `{row.final_psx_address}`",
        f"- Ghidra: `{row.ghidra_entry}` `{row.ghidra_name}`",
        f"- bytes dumped: `{size}`",
        f"- CSV: `{csv_path}`",
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return csv_path, md_path, size


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("selector", help="repo function name, Ghidra name, or PSX address, e.g. SaveLevelData or 0x80053f10")
    parser.add_argument("--repo", default=".", help="TOMB5 repo root; default current directory")
    parser.add_argument("--map", default=MAP_DEFAULT, help="repo-function-map CSV relative to repo")
    parser.add_argument("--payload", default=PAYLOAD_DEFAULT, help="raw PS-X payload relative to repo")
    parser.add_argument("--text-base", default=f"0x{TEXT_BASE_DEFAULT:08x}", help="payload load address")
    parser.add_argument("--out-dir", default=OUT_DEFAULT, help="ignored output dir relative to repo")
    parser.add_argument("--max-bytes", type=int, default=None, help="cap dumped bytes for quick inspection")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    rows = read_map(repo / args.map)
    row = resolve(rows, args.selector)
    csv_path, md_path, size = dump_function(
        repo=repo,
        row=row,
        payload=repo / args.payload,
        text_base=parse_addr(args.text_base),
        out_dir=repo / args.out_dir,
        max_bytes=args.max_bytes,
    )
    print(f"dumped {size} bytes for {row.repo_function} {row.final_psx_address}")
    print(f"csv={csv_path}")
    print(f"md={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
