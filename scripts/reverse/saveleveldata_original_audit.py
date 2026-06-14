#!/usr/bin/env python3
"""Audit source-level SaveLevelData writes against the original PSX dump metadata.

This script reads the ignored disassembly CSV produced by `disasm_extract.py`, but
its committed outputs deliberately contain only counts, addresses, and verdicts —
no original instruction rows or machine words.
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.reverse.savegame_schema import WriteRow, parse_save_level_data_writes

DEFAULT_ORIGINAL_DUMP = "build/reverse/re007/original/SaveLevelData_80053f10.csv"
DEFAULT_SOURCE = "GAME/SAVEGAME.C"
DEFAULT_OUT_MD = "docs/reverse/functions/saveleveldata-original-audit.md"
DEFAULT_WRITE_SG_ADDRESS = "0x80053b04"


@dataclass(frozen=True)
class SaveLevelDataAudit:
    source: Path
    original_dump: Path
    write_sg_address: str
    original_instruction_count: int
    original_write_sg_call_count: int
    source_write_site_count: int
    source_rows: tuple[WriteRow, ...]
    status: str

    def versionable_lines(self) -> list[str]:
        """Return safe-to-version metadata lines with no original bytes/instructions."""
        return [
            f"source: {self.source}",
            f"original_dump: {self.original_dump}",
            f"write_sg_address: {self.write_sg_address.lower()}",
            f"original_instruction_count: {self.original_instruction_count}",
            f"original_write_sg_call_count: {self.original_write_sg_call_count}",
            f"source_write_site_count: {self.source_write_site_count}",
            f"status: {self.status}",
        ]


def _normalize_address(text: str) -> str:
    return text.strip().lower()


def count_jal_calls_to(dump_csv: Path, target_address: str) -> tuple[int, int]:
    target = _normalize_address(target_address)
    instruction_count = 0
    call_count = 0
    with dump_csv.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            instruction_count += 1
            instruction = (row.get("instruction") or "").strip().lower()
            if instruction == f"jal {target}":
                call_count += 1
    return instruction_count, call_count


def _relative_to_repo(path: Path, repo: Path) -> Path:
    try:
        return path.resolve().relative_to(repo.resolve())
    except ValueError:
        return path


def audit_save_level_data(repo: Path, original_dump: Path, source: Path, write_sg_address: str) -> SaveLevelDataAudit:
    rows = tuple(parse_save_level_data_writes(source))
    instruction_count, call_count = count_jal_calls_to(original_dump, write_sg_address)
    status = "candidate-matched" if call_count == len(rows) else "needs-control-flow-audit"
    return SaveLevelDataAudit(
        source=_relative_to_repo(source, repo),
        original_dump=_relative_to_repo(original_dump, repo),
        write_sg_address=_normalize_address(write_sg_address),
        original_instruction_count=instruction_count,
        original_write_sg_call_count=call_count,
        source_write_site_count=len(rows),
        source_rows=rows,
        status=status,
    )


def write_markdown(audit: SaveLevelDataAudit, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    loop_rows = [row for row in audit.source_rows if row.context != "top-level"]
    top_level_rows = [row for row in audit.source_rows if row.context == "top-level"]
    lines = [
        "# SaveLevelData original dump audit",
        "",
        "Status: Generated",
        "Story: `docs/stories/RE-012-saveleveldata-original-audit.md`",
        "",
        "## Progress tracker",
        "",
        "- [x] Count original `WriteSG` calls from the ignored original dump CSV.",
        "- [x] Count source-level `Write(...)` sites from `GAME/SAVEGAME.C`.",
        "- [x] Record only versionable metadata, not original instruction rows or bytes.",
        "- [x] State the current marker verdict explicitly.",
        "",
        "## Inputs",
        "",
        f"- Source: `{audit.source}`",
        f"- Original dump CSV: `{audit.original_dump}` (ignored; not versioned)",
        f"- `WriteSG` final PSX address: `{audit.write_sg_address}`",
        "",
        "## Counts",
        "",
        f"- original instruction count: `{audit.original_instruction_count}`",
        f"- original `WriteSG` call count: `{audit.original_write_sg_call_count}`",
        f"- source `Write(...)` site count: `{audit.source_write_site_count}`",
        f"- top-level source write sites: `{len(top_level_rows)}`",
        f"- loop/conditional-context source write sites: `{len(loop_rows)}`",
        f"- status: `{audit.status}`",
        "",
        "## Interpretation",
        "",
        "The original PSX function is still represented only by ignored local dump data.",
        "The current source schema has fewer static `Write(...)` sites than the original `WriteSG` call count because source rows include loops and conditionals that must be audited against control flow before any completeness marker is justified.",
        "",
        "## Verdict",
        "",
        "- `(**)`: no — no rebuilt comparable object/binary comparison was produced.",
        "- `(F)`: no — the source stream is a useful hypothesis, but the original control-flow and per-call field mapping remain unaudited.",
        "- `(D)`: no — no runtime save/restore validation was performed.",
        "- Do not add `(F)`, `(D)`, or `(**)` from this report alone.",
        "",
        "## Source schema rows",
        "",
        "These are source-level expressions only and are safe to version; they do not include original instructions or bytes.",
        "",
    ]
    for row in audit.source_rows:
        lines.append(f"- `{row.index}` line `{row.line}`: `{row.expression}` size `{row.size}` context `{row.context}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="TOMB5 repo root")
    parser.add_argument("--original-dump", default=DEFAULT_ORIGINAL_DUMP, help="ignored original dump CSV, relative to repo")
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="source file relative to repo")
    parser.add_argument("--write-sg-address", default=DEFAULT_WRITE_SG_ADDRESS, help="final PSX address for WriteSG")
    parser.add_argument("--md", default=DEFAULT_OUT_MD, help="versionable markdown output, relative to repo")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    audit = audit_save_level_data(
        repo=repo,
        original_dump=repo / args.original_dump,
        source=repo / args.source,
        write_sg_address=args.write_sg_address,
    )
    out = repo / args.md
    write_markdown(audit, out)
    print(f"original_write_sg_calls={audit.original_write_sg_call_count}")
    print(f"source_write_sites={audit.source_write_site_count}")
    print(f"status={audit.status}")
    print(f"md={out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
