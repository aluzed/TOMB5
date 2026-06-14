#!/usr/bin/env python3
"""Compare two per-function instruction dumps produced by disasm_extract.py.

The right-hand dump is expected to be produced from a rebuilt comparable target or
another extraction pass with the same CSV schema. Reports go under
`build/reverse/re007/compare/` by default and should not be committed if they
contain original instructions.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

OUT_DEFAULT = "build/reverse/re007/compare"


@dataclass(frozen=True)
class Insn:
    index: int
    ram_address: str
    payload_offset: str
    word_le_hex: str
    instruction: str


def read_dump(path: Path) -> list[Insn]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = []
        for raw in csv.DictReader(f):
            rows.append(Insn(
                index=int(raw.get("index") or len(rows)),
                ram_address=raw.get("ram_address", ""),
                payload_offset=raw.get("payload_offset", ""),
                word_le_hex=(raw.get("word_le_hex", "") or raw.get("word_hex", "")).lower(),
                instruction=raw.get("instruction", ""),
            ))
        return rows


def compare(left: list[Insn], right: list[Insn]) -> list[dict[str, object]]:
    max_len = max(len(left), len(right))
    out: list[dict[str, object]] = []
    for idx in range(max_len):
        l = left[idx] if idx < len(left) else None
        r = right[idx] if idx < len(right) else None
        if l and r:
            word_match = l.word_le_hex == r.word_le_hex
            asm_match = l.instruction == r.instruction
            status = "match" if word_match else "asm-only-match" if asm_match else "diff"
        else:
            word_match = False
            asm_match = False
            status = "left-only" if l else "right-only"
        out.append({
            "index": idx,
            "status": status,
            "word_match": "yes" if word_match else "no",
            "asm_match": "yes" if asm_match else "no",
            "left_address": l.ram_address if l else "",
            "left_word": l.word_le_hex if l else "",
            "left_instruction": l.instruction if l else "",
            "right_address": r.ram_address if r else "",
            "right_word": r.word_le_hex if r else "",
            "right_instruction": r.instruction if r else "",
        })
    return out


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fields = [
        "index", "status", "word_match", "asm_match",
        "left_address", "left_word", "left_instruction",
        "right_address", "right_word", "right_instruction",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_markdown(path: Path, rows: list[dict[str, object]], left: Path, right: Path, limit: int) -> None:
    total = len(rows)
    matches = sum(1 for row in rows if row["status"] == "match")
    asm_only = sum(1 for row in rows if row["status"] == "asm-only-match")
    diffs = [row for row in rows if row["status"] != "match"]
    lines = [
        "# Function binary/disassembly comparison",
        "",
        f"Generated: `{datetime.now(timezone.utc).isoformat()}`",
        f"Left/original: `{left}`",
        f"Right/comparable: `{right}`",
        "",
        "## Summary",
        "",
        f"- instructions compared: `{total}`",
        f"- exact word matches: `{matches}`",
        f"- asm-only matches: `{asm_only}`",
        f"- differences: `{len(diffs)}`",
        f"- exact match: `{'yes' if matches == total and total > 0 else 'no'}`",
        "",
        "## First differences",
        "",
    ]
    if not diffs:
        lines.append("- none")
    for row in diffs[:limit]:
        lines.extend([
            f"- index `{row['index']}` status `{row['status']}`",
            f"  - left: `{row['left_address']}` `{row['left_word']}` `{row['left_instruction']}`",
            f"  - right: `{row['right_address']}` `{row['right_word']}` `{row['right_instruction']}`",
        ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("left", help="original dump CSV, usually under build/reverse/re007/original")
    parser.add_argument("right", help="rebuilt/comparable dump CSV with the same schema")
    parser.add_argument("--repo", default=".", help="TOMB5 repo root; default current directory")
    parser.add_argument("--out-dir", default=OUT_DEFAULT, help="ignored output dir relative to repo")
    parser.add_argument("--name", default="comparison", help="output report basename")
    parser.add_argument("--limit", type=int, default=30, help="number of differences in markdown")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    left_path = (repo / args.left).resolve() if not Path(args.left).is_absolute() else Path(args.left)
    right_path = (repo / args.right).resolve() if not Path(args.right).is_absolute() else Path(args.right)
    rows = compare(read_dump(left_path), read_dump(right_path))
    out_dir = repo / args.out_dir
    csv_path = out_dir / f"{args.name}.csv"
    md_path = out_dir / f"{args.name}.md"
    write_csv(csv_path, rows)
    write_markdown(md_path, rows, left_path, right_path, args.limit)
    exact = all(row["status"] == "match" for row in rows) and bool(rows)
    print(f"exact_match={'yes' if exact else 'no'} differences={sum(1 for row in rows if row['status'] != 'match')} total={len(rows)}")
    print(f"csv={csv_path}")
    print(f"md={md_path}")
    return 0 if exact else 1


if __name__ == "__main__":
    raise SystemExit(main())
