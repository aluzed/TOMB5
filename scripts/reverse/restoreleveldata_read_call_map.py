#!/usr/bin/env python3
"""Build a metadata-only RestoreLevelData ReadSG call map.

The input dump is the ignored CSV produced by `disasm_extract.py` and contains
original instructions/words. This script reads it only to derive safe metadata:
`ReadSG` call coordinates, integer size arguments, group size sequences, and
sequence-level comparisons against RE-017 item hypotheses. Outputs intentionally
omit instruction text, machine words, payload offsets, and raw branch targets.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.reverse.saveleveldata_call_map import DEFAULT_MAX_GAP

DEFAULT_ORIGINAL_DUMP = "build/reverse/re007/original/RestoreLevelData_80054f6c.csv"
DEFAULT_FIELD_WIDTH_CSV = "docs/reverse/generated/saveleveldata-item-field-width-audit.csv"
DEFAULT_OUT_CSV = "docs/reverse/generated/restoreleveldata-read-call-map.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/restoreleveldata-read-call-map.md"
DEFAULT_READ_SG_ADDRESS = "0x80053b44"
DEFAULT_ITEM_GROUP_RANGE = range(4, 12)


@dataclass(frozen=True)
class RestoreReadCall:
    index: int
    address: str
    size: int | None


@dataclass(frozen=True)
class RestoreReadGroup:
    group_id: int
    call_count: int
    first_call_index: int
    last_call_index: int
    first_call_address: str
    last_call_address: str
    size_sequence: str


@dataclass(frozen=True)
class RestoreComparisonRow:
    save_original_group: int
    save_call_count: int
    save_size_sequence: str
    restore_match_status: str
    restore_match_locations: str
    patch_readiness: str
    notes: str


@dataclass(frozen=True)
class RestoreReadCallMap:
    original_dump: Path
    field_width_csv: Path
    read_sg_address: str
    max_gap: int
    total_read_sg_calls: int
    restore_groups: tuple[RestoreReadGroup, ...]
    comparison_rows: tuple[RestoreComparisonRow, ...]
    matched_group_count: int
    patch_ready_count: int
    status: str


def _relative_to_repo(path: Path, repo: Path) -> Path:
    try:
        return path.resolve().relative_to(repo.resolve())
    except ValueError:
        return path


def _normalize_address(text: str) -> str:
    return text.strip().lower()


def _parse_a1_immediate(text: str) -> int | None:
    stripped = text.strip()
    for pattern in (
        r"addiu \$a1, \$zero, (-?\d+)",
        r"ori \$a1, \$zero, (0x[0-9a-fA-F]+|\d+)",
    ):
        match = re.match(pattern, stripped)
        if match:
            return int(match.group(1), 0)
    return None


def _sequence_text(sizes: tuple[int | None, ...]) -> str:
    return ",".join("unknown" if size is None else str(size) for size in sizes)


def extract_read_sg_size_groups(dump_csv: Path, read_sg_address: str, max_gap: int = DEFAULT_MAX_GAP) -> tuple[tuple[RestoreReadCall, ...], ...]:
    """Return ReadSG call groups with safe call metadata and size args only."""
    target = f"jal {_normalize_address(read_sg_address)}"
    with dump_csv.open(newline="", encoding="utf-8") as f:
        dump_rows = list(csv.DictReader(f))

    calls: list[RestoreReadCall] = []
    current_a1: int | None = None
    for idx, row in enumerate(dump_rows):
        current_text = (row.get("instruction") or "").strip().lower()
        if current_text == target:
            delay_size = None
            if idx + 1 < len(dump_rows):
                delay_size = _parse_a1_immediate(dump_rows[idx + 1].get("instruction") or "")
            calls.append(RestoreReadCall(
                index=int(row.get("index") or len(calls)),
                address=row.get("ram_address", ""),
                size=delay_size if delay_size is not None else current_a1,
            ))
        next_a1 = _parse_a1_immediate(row.get("instruction") or "")
        if next_a1 is not None:
            current_a1 = next_a1

    groups: list[tuple[RestoreReadCall, ...]] = []
    current: list[RestoreReadCall] = []
    previous_index: int | None = None
    for call in calls:
        if previous_index is not None and call.index - previous_index > max_gap:
            groups.append(tuple(current))
            current = []
        current.append(call)
        previous_index = call.index
    if current:
        groups.append(tuple(current))
    return tuple(groups)


def _restore_group_rows(groups: tuple[tuple[RestoreReadCall, ...], ...]) -> tuple[RestoreReadGroup, ...]:
    rows: list[RestoreReadGroup] = []
    for group_id, calls in enumerate(groups, start=1):
        first = calls[0]
        last = calls[-1]
        rows.append(RestoreReadGroup(
            group_id=group_id,
            call_count=len(calls),
            first_call_index=first.index,
            last_call_index=last.index,
            first_call_address=first.address,
            last_call_address=last.address,
            size_sequence=_sequence_text(tuple(call.size for call in calls)),
        ))
    return tuple(rows)


def _read_save_item_sequences(field_width_csv: Path) -> dict[int, tuple[int | None, ...]]:
    grouped: dict[int, list[int | None]] = {}
    with field_width_csv.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            group_id = int(row["original_group"])
            if group_id not in DEFAULT_ITEM_GROUP_RANGE:
                continue
            size_text = row.get("original_size") or ""
            size = int(size_text) if size_text else None
            grouped.setdefault(group_id, []).append(size)
    return {group_id: tuple(sizes) for group_id, sizes in sorted(grouped.items())}


def _find_subsequence_locations(needle: tuple[int | None, ...], haystacks: tuple[tuple[RestoreReadCall, ...], ...]) -> list[str]:
    if not needle:
        return []
    locations: list[str] = []
    for group_id, calls in enumerate(haystacks, start=1):
        sizes = tuple(call.size for call in calls)
        if len(needle) > len(sizes):
            continue
        for offset in range(0, len(sizes) - len(needle) + 1):
            if sizes[offset:offset + len(needle)] == needle:
                locations.append(f"restore_group={group_id}:call_ordinal={offset + 1}")
    return locations


def _comparison_status(sequence: tuple[int | None, ...], locations: list[str]) -> tuple[str, str, str]:
    if not locations:
        return (
            "no-exact-restore-size-sequence",
            "blocked",
            "No exact contiguous restore ReadSG size subsequence matches this RE-017 item group.",
        )
    if len(sequence) == 1:
        return (
            "ambiguous-single-byte-restore-matches",
            "blocked",
            "Single-byte groups match many restore locations and do not identify a field or branch by themselves.",
        )
    return (
        "exact-restore-size-subsequence-match",
        "blocked",
        "Size sequence exists on restore side, but this is not field/predicate proof and does not unlock a patch alone.",
    )


def build_restore_read_call_map(repo: Path, original_dump: Path, field_width_csv: Path, read_sg_address: str = DEFAULT_READ_SG_ADDRESS, max_gap: int = DEFAULT_MAX_GAP) -> RestoreReadCallMap:
    raw_groups = extract_read_sg_size_groups(original_dump, read_sg_address, max_gap=max_gap)
    restore_groups = _restore_group_rows(raw_groups)
    save_sequences = _read_save_item_sequences(field_width_csv)

    comparison_rows: list[RestoreComparisonRow] = []
    for save_group, sequence in save_sequences.items():
        locations = _find_subsequence_locations(sequence, raw_groups)
        status, readiness, notes = _comparison_status(sequence, locations)
        comparison_rows.append(RestoreComparisonRow(
            save_original_group=save_group,
            save_call_count=len(sequence),
            save_size_sequence=_sequence_text(sequence),
            restore_match_status=status,
            restore_match_locations="; ".join(locations) if locations else "none",
            patch_readiness=readiness,
            notes=notes,
        ))

    matched_group_count = sum(1 for row in comparison_rows if row.restore_match_status != "no-exact-restore-size-sequence")
    patch_ready_count = sum(1 for row in comparison_rows if row.patch_readiness == "ready")
    status = "restore-size-proof-partial" if matched_group_count else "restore-size-proof-missing"
    return RestoreReadCallMap(
        original_dump=_relative_to_repo(original_dump, repo),
        field_width_csv=_relative_to_repo(field_width_csv, repo),
        read_sg_address=_normalize_address(read_sg_address),
        max_gap=max_gap,
        total_read_sg_calls=sum(group.call_count for group in restore_groups),
        restore_groups=restore_groups,
        comparison_rows=tuple(comparison_rows),
        matched_group_count=matched_group_count,
        patch_ready_count=patch_ready_count,
        status=status,
    )


def write_csv(mapping: RestoreReadCallMap, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "record_kind", "restore_group", "call_count", "first_call_index", "last_call_index",
        "first_call_address", "last_call_address", "size_sequence", "save_original_group",
        "save_call_count", "save_size_sequence", "restore_match_status", "restore_match_locations",
        "patch_readiness", "notes",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for group in mapping.restore_groups:
            writer.writerow({
                "record_kind": "restore-read-group",
                "restore_group": group.group_id,
                "call_count": group.call_count,
                "first_call_index": group.first_call_index,
                "last_call_index": group.last_call_index,
                "first_call_address": group.first_call_address,
                "last_call_address": group.last_call_address,
                "size_sequence": group.size_sequence,
            })
        for row in mapping.comparison_rows:
            writer.writerow({
                "record_kind": "save-restore-comparison",
                "save_original_group": row.save_original_group,
                "save_call_count": row.save_call_count,
                "save_size_sequence": row.save_size_sequence,
                "restore_match_status": row.restore_match_status,
                "restore_match_locations": row.restore_match_locations,
                "patch_readiness": row.patch_readiness,
                "notes": row.notes,
            })


def write_markdown(mapping: RestoreReadCallMap, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RestoreLevelData ReadSG call-map audit",
        "",
        "Status: Generated",
        "Story: `docs/stories/RE-019-restoreleveldata-read-call-map.md`",
        "",
        "## Progress tracker",
        "",
        "- [x] Extract original `ReadSG` call coordinates and size metadata.",
        "- [x] Group restore-side read calls by row-index gaps.",
        "- [x] Compare RE-017 item size sequences against restore read size subsequences.",
        "- [x] Keep original opcode rows and machine words out of versioned outputs.",
        "- [x] Preserve marker verdict limits.",
        "",
        "## Inputs",
        "",
        f"- Original dump CSV: `{mapping.original_dump}` (ignored; not versioned)",
        f"- RE-017 field-width CSV: `{mapping.field_width_csv}`",
        "- ReadSG final PSX address: metadata target configured in the generator; raw call opcodes are not emitted.",
        f"- Grouping gap threshold: `{mapping.max_gap}` row indices",
        "",
        "## Summary",
        "",
        f"- original `ReadSG` calls: `{mapping.total_read_sg_calls}`",
        f"- restore read groups: `{len(mapping.restore_groups)}`",
        f"- RE-017 item groups compared: `{len(mapping.comparison_rows)}`",
        f"- groups with size-only restore match: `{mapping.matched_group_count}`",
        f"- patch-ready groups: `{mapping.patch_ready_count}`",
        f"- status: `{mapping.status}`",
        "",
        "## Restore ReadSG groups",
        "",
        "The call indices, addresses, and sizes below are metadata coordinates only. This report does not include original opcode text, machine words, payload offsets, or dump rows.",
        "",
    ]
    for group in mapping.restore_groups:
        lines.extend([
            f"### Restore read group {group.group_id}",
            "",
            f"- read call count: `{group.call_count}`",
            f"- call index range: `{group.first_call_index}` → `{group.last_call_index}`",
            f"- call address range: `{group.first_call_address}` → `{group.last_call_address}`",
            f"- size sequence: `{group.size_sequence}`",
            "",
        ])
    lines.extend([
        "## RE-017 / RE-018 comparison",
        "",
    ])
    for row in mapping.comparison_rows:
        lines.extend([
            f"### Save original item group {row.save_original_group}",
            "",
            f"- save call count: `{row.save_call_count}`",
            f"- save size sequence: `{row.save_size_sequence}`",
            f"- restore match status: `{row.restore_match_status}`",
            f"- restore match locations: `{row.restore_match_locations}`",
            f"- patch readiness: `{row.patch_readiness}`",
            f"- notes: {row.notes}",
            "",
        ])
    lines.extend([
        "## Verdict",
        "",
        "RE-019 finds only size-sequence evidence. Most RE-017 item groups do not have an exact contiguous restore-size match; the matching single-byte groups are ambiguous, and the group 10 size subsequence is not field/predicate proof. Patch readiness remains `0`.",
        "",
        "Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.",
        "",
        "Next step: derive stronger restore-side field/control-flow proof for the matched and mismatched regions, especially branch predicates around item groups 4, 5, 8, and 10.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="TOMB5 repo root")
    parser.add_argument("--original-dump", default=DEFAULT_ORIGINAL_DUMP, help="ignored original RestoreLevelData dump CSV, relative to repo")
    parser.add_argument("--field-width-csv", default=DEFAULT_FIELD_WIDTH_CSV, help="RE-017 field-width CSV, relative to repo")
    parser.add_argument("--read-sg-address", default=DEFAULT_READ_SG_ADDRESS, help="final PSX address for ReadSG")
    parser.add_argument("--max-gap", type=int, default=DEFAULT_MAX_GAP, help="start a new group when call indices differ by more than this")
    parser.add_argument("--csv", default=DEFAULT_OUT_CSV, help="versionable CSV output, relative to repo")
    parser.add_argument("--md", default=DEFAULT_OUT_MD, help="versionable markdown output, relative to repo")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    mapping = build_restore_read_call_map(
        repo=repo,
        original_dump=repo / args.original_dump,
        field_width_csv=repo / args.field_width_csv,
        read_sg_address=args.read_sg_address,
        max_gap=args.max_gap,
    )
    csv_path = repo / args.csv
    md_path = repo / args.md
    write_csv(mapping, csv_path)
    write_markdown(mapping, md_path)
    print(f"original_read_sg_calls={mapping.total_read_sg_calls}")
    print(f"restore_read_groups={len(mapping.restore_groups)}")
    print(f"re017_item_groups_compared={len(mapping.comparison_rows)}")
    print(f"matched_group_count={mapping.matched_group_count}")
    print(f"patch_ready_count={mapping.patch_ready_count}")
    print(f"status={mapping.status}")
    print(f"csv={csv_path}")
    print(f"md={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
