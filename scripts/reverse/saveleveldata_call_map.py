#!/usr/bin/env python3
"""Build a versionable candidate map from original SaveLevelData WriteSG call groups to source Write sites.

The input dump is the ignored CSV produced by `disasm_extract.py` and contains
original instructions/words. This script reads it only to locate `WriteSG` call
indices and addresses. Outputs intentionally omit instruction text and machine
words so they can be committed as reverse metadata.
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
DEFAULT_OUT_CSV = "docs/reverse/generated/saveleveldata-write-call-map.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/saveleveldata-write-call-map.md"
DEFAULT_WRITE_SG_ADDRESS = "0x80053b04"
DEFAULT_MAX_GAP = 24


@dataclass(frozen=True)
class CallGroup:
    group_id: int
    call_count: int
    first_call_index: int
    last_call_index: int
    first_call_address: str
    last_call_address: str

    def versionable_lines(self) -> list[str]:
        return [
            f"group_id: {self.group_id}",
            f"call_count: {self.call_count}",
            f"first_call_index: {self.first_call_index}",
            f"last_call_index: {self.last_call_index}",
            f"first_call_address: {self.first_call_address}",
            f"last_call_address: {self.last_call_address}",
        ]


@dataclass(frozen=True)
class MappingRow:
    original_group: int
    original_call_count: int
    first_call_index: int
    last_call_index: int
    first_call_address: str
    last_call_address: str
    candidate_source_rows: str
    candidate_context: str
    confidence: str
    notes: str


@dataclass(frozen=True)
class CallGroupMap:
    source: Path
    original_dump: Path
    write_sg_address: str
    max_gap: int
    total_original_calls: int
    total_source_sites: int
    status: str
    rows: tuple[MappingRow, ...]
    source_rows: tuple[WriteRow, ...]


def _normalize_address(text: str) -> str:
    return text.strip().lower()


def _relative_to_repo(path: Path, repo: Path) -> Path:
    try:
        return path.resolve().relative_to(repo.resolve())
    except ValueError:
        return path


def extract_write_sg_call_groups(dump_csv: Path, write_sg_address: str, max_gap: int = DEFAULT_MAX_GAP) -> tuple[CallGroup, ...]:
    target = _normalize_address(write_sg_address)
    calls: list[tuple[int, str]] = []
    with dump_csv.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            instruction = (row.get("instruction") or "").strip().lower()
            if instruction == f"jal {target}":
                calls.append((int(row.get("index") or len(calls)), row.get("ram_address", "")))

    groups: list[CallGroup] = []
    current: list[tuple[int, str]] = []
    previous_index: int | None = None
    for call in calls:
        index, _address = call
        if previous_index is not None and index - previous_index > max_gap:
            groups.append(_group_from_calls(len(groups) + 1, current))
            current = []
        current.append(call)
        previous_index = index
    if current:
        groups.append(_group_from_calls(len(groups) + 1, current))
    return tuple(groups)


def _group_from_calls(group_id: int, calls: list[tuple[int, str]]) -> CallGroup:
    first_index, first_address = calls[0]
    last_index, last_address = calls[-1]
    return CallGroup(
        group_id=group_id,
        call_count=len(calls),
        first_call_index=first_index,
        last_call_index=last_index,
        first_call_address=first_address,
        last_call_address=last_address,
    )


def _candidate_source_rows(source_rows: tuple[WriteRow, ...]) -> list[tuple[str, str, str, str]]:
    """Return conservative candidate source spans for grouped original calls.

    These are not equivalence claims. They are triage buckets that keep the next
    manual audit focused without copying original instructions.
    """
    return [
        ("1-9", "global state, flipmap loop, flip status, cd flags, atmosphere", "medium", "front-loaded top-level serializer fields"),
        ("10-15", "room static flags, sequence byte, camera flags, spotcam flags", "low", "contains runtime-count loops; verify control-flow boundaries"),
        ("16", "level item killed marker", "low", "single killed-item branch candidate"),
        ("17-26", "item header/position block and optional speed/fallspeed writes", "low", "candidate item save_position branch after RE-015 header insertion"),
        ("17-34", "item active/full-save branch variant", "low", "same source rows can compile into several original call regions"),
        ("27-34", "item animation, hitpoint, and flags fields", "low", "candidate save_anim/save_hitpoints/save_flags branch"),
        ("17-34", "item serialization alternate control-flow region", "low", "requires size-sequence/control-flow audit"),
        ("17-34", "item serialization dense call region", "low", "largest repeated candidate item region"),
        ("30-34", "lara/non-lara anim-number, frame, hitpoint, flags tail", "low", "tail branch candidate"),
        ("17-34", "item serialization second variant", "low", "requires mapping against item/object flags"),
        ("32-34", "frame number / hit points / flags tail", "low", "late item tail candidate"),
        ("17-34", "item serialization final variant", "low", "final original call group before function return"),
    ]


def build_call_group_map(repo: Path, original_dump: Path, source: Path, write_sg_address: str, max_gap: int = DEFAULT_MAX_GAP) -> CallGroupMap:
    source_rows = tuple(parse_save_level_data_writes(source))
    groups = extract_write_sg_call_groups(original_dump, write_sg_address, max_gap=max_gap)
    candidates = _candidate_source_rows(source_rows)
    rows: list[MappingRow] = []
    for group in groups:
        if group.group_id <= len(candidates):
            candidate_rows, context, confidence, notes = candidates[group.group_id - 1]
        else:
            candidate_rows, context, confidence, notes = "unassigned", "unassigned", "none", "more original groups than candidate buckets"
        rows.append(MappingRow(
            original_group=group.group_id,
            original_call_count=group.call_count,
            first_call_index=group.first_call_index,
            last_call_index=group.last_call_index,
            first_call_address=group.first_call_address,
            last_call_address=group.last_call_address,
            candidate_source_rows=candidate_rows,
            candidate_context=context,
            confidence=confidence,
            notes=notes,
        ))
    return CallGroupMap(
        source=_relative_to_repo(source, repo),
        original_dump=_relative_to_repo(original_dump, repo),
        write_sg_address=_normalize_address(write_sg_address),
        max_gap=max_gap,
        total_original_calls=sum(group.call_count for group in groups),
        total_source_sites=len(source_rows),
        status="candidate-map-needs-manual-audit",
        rows=tuple(rows),
        source_rows=source_rows,
    )


def write_csv(mapping: CallGroupMap, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "original_group", "original_call_count", "first_call_index", "last_call_index",
        "first_call_address", "last_call_address", "candidate_source_rows",
        "candidate_context", "confidence", "notes",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in mapping.rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def write_markdown(mapping: CallGroupMap, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# SaveLevelData WriteSG call-group map",
        "",
        "Status: Generated",
        "Story: `docs/stories/RE-013-saveleveldata-write-call-map.md`",
        "",
        "## Progress tracker",
        "",
        "- [x] Group original `WriteSG` calls by instruction-index gaps.",
        "- [x] Attach conservative source `Write(...)` candidate row spans.",
        "- [x] Keep original instruction rows and machine words out of versioned outputs.",
        "- [x] State that this is not an equivalence marker proof.",
        "",
        "## Inputs",
        "",
        f"- Source: `{mapping.source}`",
        f"- Original dump CSV: `{mapping.original_dump}` (ignored; not versioned)",
        f"- `WriteSG` final PSX address: `{mapping.write_sg_address}`",
        f"- Grouping gap threshold: `{mapping.max_gap}` instruction indices",
        "",
        "## Summary",
        "",
        f"- original `WriteSG` calls: `{mapping.total_original_calls}`",
        f"- original call groups: `{len(mapping.rows)}`",
        f"- source `Write(...)` sites: `{mapping.total_source_sites}`",
        f"- status: `{mapping.status}`",
        "",
        "## Candidate map",
        "",
        "The `first/last_call_*` columns are metadata coordinates only. This report does not include the original instruction text or machine words.",
        "",
    ]
    for row in mapping.rows:
        lines.extend([
            f"### Original call group {row.original_group}",
            "",
            f"- original call count: `{row.original_call_count}`",
            f"- call index range: `{row.first_call_index}` → `{row.last_call_index}`",
            f"- call address range: `{row.first_call_address}` → `{row.last_call_address}`",
            f"- candidate source rows: `{row.candidate_source_rows}`",
            f"- candidate context: `{row.candidate_context}`",
            f"- confidence: `{row.confidence}`",
            f"- notes: {row.notes}",
            "",
        ])
    lines.extend([
        "## Verdict",
        "",
        "This map is a triage artifact, not an equivalence proof. The repeated item-serialization regions need manual control-flow audit before `SaveLevelData` can receive `(F)`, `(D)`, or `(**)`.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="TOMB5 repo root")
    parser.add_argument("--original-dump", default=DEFAULT_ORIGINAL_DUMP, help="ignored original dump CSV, relative to repo")
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="source file relative to repo")
    parser.add_argument("--write-sg-address", default=DEFAULT_WRITE_SG_ADDRESS, help="final PSX address for WriteSG")
    parser.add_argument("--max-gap", type=int, default=DEFAULT_MAX_GAP, help="start a new group when call indices differ by more than this")
    parser.add_argument("--csv", default=DEFAULT_OUT_CSV, help="versionable CSV output, relative to repo")
    parser.add_argument("--md", default=DEFAULT_OUT_MD, help="versionable markdown output, relative to repo")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    mapping = build_call_group_map(
        repo=repo,
        original_dump=repo / args.original_dump,
        source=repo / args.source,
        write_sg_address=args.write_sg_address,
        max_gap=args.max_gap,
    )
    csv_path = repo / args.csv
    md_path = repo / args.md
    write_csv(mapping, csv_path)
    write_markdown(mapping, md_path)
    print(f"original_write_sg_calls={mapping.total_original_calls}")
    print(f"original_call_groups={len(mapping.rows)}")
    print(f"source_write_sites={mapping.total_source_sites}")
    print(f"status={mapping.status}")
    print(f"csv={csv_path}")
    print(f"md={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
