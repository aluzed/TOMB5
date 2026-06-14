#!/usr/bin/env python3
"""Generate a versionable savegame stream schema from GAME/SAVEGAME.C.

This script deliberately extracts source-level `Write(...)` metadata only. It does
not read original game bytes/instructions and its outputs may be committed.
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path

DEFAULT_SOURCE = "GAME/SAVEGAME.C"
DEFAULT_OUT_CSV = "docs/reverse/generated/savegame-level-data-schema.csv"
DEFAULT_OUT_MD = "docs/reverse/generated/savegame-level-data-schema.md"


@dataclass(frozen=True)
class WriteRow:
    index: int
    line: int
    expression: str
    size: str
    context: str


def _split_args(text: str) -> tuple[str, str] | None:
    depth = 0
    for idx, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            return text[:idx].strip(), text[idx + 1 :].strip()
    return None


def _context_from_stack(stack: list[str]) -> str:
    if not stack:
        return "top-level"
    return " / ".join(stack[-4:])


def parse_save_level_data_writes(source: Path) -> list[WriteRow]:
    """Return the ordered source-level `Write(expr, size)` calls in the PC branch.

    The current PSX branch is unimplemented, so the PC branch is used as the best
    available field-order hypothesis for reconstruction. Loops and conditionals
    are intentionally preserved as context instead of expanded, because many
    counts depend on runtime values such as `number_rooms` and `level_items`.
    """

    lines = source.read_text(encoding="utf-8").splitlines()
    in_func = False
    in_pc_branch = False
    brace_depth = 0
    context_stack: list[str] = []
    pending_context: str | None = None
    rows: list[WriteRow] = []

    write_re = re.compile(r"\bWrite\s*\((.*)\)\s*;")

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not in_func:
            if re.match(r"void\s+SaveLevelData\s*\(", stripped):
                in_func = True
                brace_depth += line.count("{") - line.count("}")
            continue

        if stripped.startswith("#if PC_VERSION"):
            in_pc_branch = True
            continue
        if in_pc_branch and stripped.startswith("#else"):
            break

        if in_pc_branch:
            # The source uses a simple K&R-ish style: control line, then a brace
            # on the next line. Maintain a best-effort source context without
            # expanding runtime-dependent loops.
            leading_closes = len(stripped) - len(stripped.lstrip("}"))
            for _ in range(leading_closes):
                if context_stack:
                    context_stack.pop()

            if stripped == "{" and pending_context:
                context_stack.append(pending_context)
                pending_context = None
            elif "{" in stripped and pending_context:
                context_stack.append(pending_context)
                pending_context = None

            match = write_re.search(stripped)
            if match:
                split = _split_args(match.group(1))
                if split:
                    expression, size = split
                    rows.append(WriteRow(
                        index=len(rows) + 1,
                        line=lineno,
                        expression=expression,
                        size=size,
                        context=_context_from_stack(context_stack),
                    ))

            if stripped.startswith(("for", "if", "else if", "else")):
                pending_context = stripped.rstrip("{").strip()
                if "{" in stripped:
                    context_stack.append(pending_context)
                    pending_context = None

        brace_depth += line.count("{") - line.count("}")
        if in_func and brace_depth <= 0:
            break

    if not rows:
        raise ValueError(f"No SaveLevelData Write(...) rows parsed from {source}")
    return rows


def write_csv(rows: list[WriteRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["index", "line", "expression", "size", "context"], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "index": row.index,
                "line": row.line,
                "expression": row.expression,
                "size": row.size,
                "context": row.context,
            })


def write_markdown(rows: list[WriteRow], path: Path, source: Path, csv_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# SaveLevelData source-level stream schema",
        "",
        "Status: Generated",
        "Story: `docs/stories/RE-010-savegame-stream-schema.md`",
        "",
        "## Purpose",
        "",
        "This file captures the ordered `Write(expr, size)` calls from the current `PC_VERSION` branch of `SaveLevelData`.",
        "The PSX branch is still unimplemented, so this is a reconstruction aid, not proof of PSX equivalence.",
        "",
        "## Inputs and outputs",
        "",
        f"- Source: `{source}`",
        f"- CSV: `{csv_path}`",
        f"- Parsed write sites: `{len(rows)}`",
        "",
        "## How to use this schema",
        "",
        "- Treat the row order as the first field-order hypothesis for PSX `SaveLevelData`.",
        "- Preserve loop/conditional context; do not expand rows whose counts depend on runtime values.",
        "- Reconstruct `RestoreLevelData` as the inverse `ReadSG` stream only after checking each field against the original control flow.",
        "- Do not use this file to add `(F)`, `(D)`, or `(**)` markers by itself.",
        "",
        "## Rows",
        "",
    ]
    for row in rows:
        lines.extend([
            f"### {row.index}. `{row.expression}`",
            "",
            f"- source line: `{row.line}`",
            f"- size expression: `{row.size}`",
            f"- context: `{row.context}`",
            "",
        ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="TOMB5 repo root")
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="source file relative to repo")
    parser.add_argument("--csv", default=DEFAULT_OUT_CSV, help="CSV output relative to repo")
    parser.add_argument("--md", default=DEFAULT_OUT_MD, help="Markdown output relative to repo")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    source = repo / args.source
    csv_path = repo / args.csv
    md_path = repo / args.md
    rows = parse_save_level_data_writes(source)
    write_csv(rows, csv_path)
    write_markdown(rows, md_path, source.relative_to(repo), csv_path.relative_to(repo))
    print(f"parsed {len(rows)} SaveLevelData Write(...) rows")
    print(f"csv={csv_path}")
    print(f"md={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
