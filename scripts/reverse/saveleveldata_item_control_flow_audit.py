#!/usr/bin/env python3
"""Audit SaveLevelData item call-group control-flow by WriteSG size sequences.

The script reads the ignored original dump only to derive safe metadata: WriteSG
call groups and the integer size argument passed in `a1`. It never emits original
instruction text, machine words, payload offsets, or binary-derived rows.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.reverse.saveleveldata_call_map import DEFAULT_MAX_GAP, DEFAULT_WRITE_SG_ADDRESS

DEFAULT_ORIGINAL_DUMP = "build/reverse/re007/original/SaveLevelData_80053f10.csv"
DEFAULT_ITEM_FLAG_CSV = "docs/reverse/generated/saveleveldata-item-flag-audit.csv"
DEFAULT_OUT_CSV = "docs/reverse/generated/saveleveldata-item-control-flow-audit.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/saveleveldata-item-control-flow-audit.md"


@dataclass(frozen=True)
class OriginalCall:
    index: int
    address: str
    size: int | None


@dataclass(frozen=True)
class SourceSizeCase:
    label: str
    sizes: tuple[int, ...]


@dataclass(frozen=True)
class ItemControlFlowRow:
    original_group: int
    original_call_count: int
    first_call_index: int
    last_call_index: int
    first_call_address: str
    last_call_address: str
    original_size_sequence: str
    source_count_cases: str
    matching_source_cases: str
    control_flow_status: str
    notes: str

    def versionable_lines(self) -> list[str]:
        return [
            f"original_group: {self.original_group}",
            f"original_call_count: {self.original_call_count}",
            f"first_call_index: {self.first_call_index}",
            f"last_call_index: {self.last_call_index}",
            f"first_call_address: {self.first_call_address}",
            f"last_call_address: {self.last_call_address}",
            f"original_size_sequence: {self.original_size_sequence}",
            f"control_flow_status: {self.control_flow_status}",
            f"matching_source_cases: {self.matching_source_cases}",
        ]


@dataclass(frozen=True)
class ItemControlFlowAudit:
    original_dump: Path
    item_flag_csv: Path
    write_sg_address: str
    total_item_groups: int
    exact_match_groups: tuple[int, ...]
    mismatch_groups: tuple[int, ...]
    rows: tuple[ItemControlFlowRow, ...]
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


def extract_write_sg_size_groups(dump_csv: Path, write_sg_address: str, max_gap: int = DEFAULT_MAX_GAP) -> tuple[tuple[OriginalCall, ...], ...]:
    """Return WriteSG call groups with safe call metadata and size args only."""
    target = f"jal {_normalize_address(write_sg_address)}"
    with dump_csv.open(newline="", encoding="utf-8") as f:
        dump_rows = list(csv.DictReader(f))

    calls: list[OriginalCall] = []
    current_a1: int | None = None
    for idx, row in enumerate(dump_rows):
        current_text = (row.get("instruction") or "").strip().lower()
        if current_text == target:
            delay_size = None
            if idx + 1 < len(dump_rows):
                delay_size = _parse_a1_immediate(dump_rows[idx + 1].get("instruction") or "")
            calls.append(OriginalCall(
                index=int(row.get("index") or len(calls)),
                address=row.get("ram_address", ""),
                size=delay_size if delay_size is not None else current_a1,
            ))
        next_a1 = _parse_a1_immediate(row.get("instruction") or "")
        if next_a1 is not None:
            current_a1 = next_a1

    groups: list[tuple[OriginalCall, ...]] = []
    current: list[OriginalCall] = []
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


def _source_size_cases() -> tuple[SourceSizeCase, ...]:
    """Enumerate current source item active/full-save branch size sequences."""
    cases: list[SourceSizeCase] = []
    optional_position_bits = ("x_rot", "z_rot", "speed", "fallspeed")
    position_variants: list[tuple[str, tuple[int, ...]]] = [("save_position=absent", ())]
    for bits in itertools.product((False, True), repeat=len(optional_position_bits)):
        labels = [name for enabled, name in zip(bits, optional_position_bits) if enabled]
        suffix = "+".join(labels) if labels else "required-only"
        sizes = (2, 2, 2, 1, 2) + tuple(2 for enabled in bits if enabled)
        position_variants.append((f"save_position={suffix}", sizes))

    anim_variants = [
        ("save_anim=absent", ()),
        ("save_anim=lara", (2, 2, 2, 2, 2)),
        ("save_anim=non_lara", (2, 2, 2, 1, 2)),
    ]
    hitpoint_variants = [("save_hitpoints=absent", ()), ("save_hitpoints=1", (2,))]
    flags_variants = [("save_flags=absent", ()), ("save_flags=1", (4,))]

    for position_label, position_sizes in position_variants:
        for anim_label, anim_sizes in anim_variants:
            for hitpoint_label, hitpoint_sizes in hitpoint_variants:
                for flags_label, flags_sizes in flags_variants:
                    labels = ["active_header=1"]
                    labels.extend(label for label in (position_label, anim_label, hitpoint_label, flags_label) if not label.endswith("=absent"))
                    sizes = (2,) + position_sizes + anim_sizes + hitpoint_sizes + flags_sizes
                    cases.append(SourceSizeCase(label=" + ".join(labels), sizes=sizes))
    return tuple(cases)


def _sequence_text(sizes: tuple[int | None, ...]) -> str:
    return ",".join("unknown" if size is None else str(size) for size in sizes)


def _read_item_flag_rows(item_flag_csv: Path) -> dict[int, dict[str, str]]:
    with item_flag_csv.open(newline="", encoding="utf-8") as f:
        return {int(row["original_group"]): row for row in csv.DictReader(f)}


def build_item_control_flow_audit(repo: Path, original_dump: Path, item_flag_csv: Path, write_sg_address: str, max_gap: int = DEFAULT_MAX_GAP) -> ItemControlFlowAudit:
    groups = extract_write_sg_size_groups(original_dump, write_sg_address, max_gap=max_gap)
    item_rows = _read_item_flag_rows(item_flag_csv)
    source_cases = _source_size_cases()

    rows: list[ItemControlFlowRow] = []
    exact: list[int] = []
    mismatch: list[int] = []
    for group_id in sorted(item_rows):
        calls = groups[group_id - 1]
        first = calls[0]
        last = calls[-1]
        original_sizes = tuple(call.size for call in calls)
        source_count_cases = item_rows[group_id]["matching_source_cases"]
        matching = [case.label for case in source_cases if case.sizes == original_sizes]
        if matching:
            status = "exact-size-sequence-match"
            notes = "Original size sequence has at least one exact current-source branch case; semantic branch predicates still need review."
            exact.append(group_id)
        else:
            status = "size-sequence-mismatch"
            notes = "Count is representable, but no exact source size sequence matches the original group; inspect field widths and branch boundaries before any marker claim."
            mismatch.append(group_id)
        rows.append(ItemControlFlowRow(
            original_group=group_id,
            original_call_count=len(calls),
            first_call_index=first.index,
            last_call_index=last.index,
            first_call_address=first.address,
            last_call_address=last.address,
            original_size_sequence=_sequence_text(original_sizes),
            source_count_cases=source_count_cases,
            matching_source_cases="; ".join(matching) if matching else "none",
            control_flow_status=status,
            notes=notes,
        ))

    status = "control-flow-proven-by-size-sequences" if not mismatch else "control-flow-gaps-found"
    return ItemControlFlowAudit(
        original_dump=_relative_to_repo(original_dump, repo),
        item_flag_csv=_relative_to_repo(item_flag_csv, repo),
        write_sg_address=_normalize_address(write_sg_address),
        total_item_groups=len(rows),
        exact_match_groups=tuple(exact),
        mismatch_groups=tuple(mismatch),
        rows=tuple(rows),
        status=status,
    )


def _groups_text(groups: tuple[int, ...]) -> str:
    return ", ".join(str(group) for group in groups) or "none"


def write_csv(audit: ItemControlFlowAudit, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "original_group", "original_call_count", "first_call_index", "last_call_index",
        "first_call_address", "last_call_address", "original_size_sequence",
        "source_count_cases", "matching_source_cases", "control_flow_status", "notes",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in audit.rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def write_markdown(audit: ItemControlFlowAudit, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# SaveLevelData item control-flow audit",
        "",
        "Status: Generated",
        "Story: `docs/stories/RE-016-saveleveldata-item-control-flow-proof.md`",
        "",
        "## Progress tracker",
        "",
        "- [x] Derive original `WriteSG` call size metadata from the ignored dump.",
        "- [x] Enumerate current-source item active/full-save size sequences.",
        "- [x] Compare item groups `4` to `12` by exact size sequence.",
        "- [x] Keep original rows and binary words out of versioned outputs.",
        "- [x] Preserve marker verdict limits.",
        "",
        "## Inputs",
        "",
        f"- Original dump CSV: `{audit.original_dump}` (ignored; not versioned)",
        f"- Item count audit CSV: `{audit.item_flag_csv}`",
        f"- `WriteSG` final PSX address: `{audit.write_sg_address}`",
        "",
        "## Summary",
        "",
        f"- item candidate groups: `{audit.total_item_groups}`",
        f"- exact-match groups: `{_groups_text(audit.exact_match_groups)}`",
        f"- mismatch groups: `{_groups_text(audit.mismatch_groups)}`",
        f"- status: `{audit.status}`",
        "",
        "## Method",
        "",
        "This report records only call coordinates and size arguments. The original dump remains ignored and no original row text or machine word is emitted here.",
        "",
        "A match means the whole grouped size sequence is exactly reproducible by at least one current-source item branch case. It is still weaker than semantic equivalence because predicate identity and field provenance are not proven.",
        "",
        "## Item group comparison",
        "",
    ]
    for row in audit.rows:
        lines.extend([
            f"### Original item group {row.original_group}",
            "",
            f"- original call count: `{row.original_call_count}`",
            f"- call index range: `{row.first_call_index}` → `{row.last_call_index}`",
            f"- call address range: `{row.first_call_address}` → `{row.last_call_address}`",
            f"- original size sequence: `{row.original_size_sequence}`",
            f"- count-level source cases: `{row.source_count_cases}`",
            f"- exact matching source cases: `{row.matching_source_cases}`",
            f"- control-flow status: `{row.control_flow_status}`",
            f"- notes: {row.notes}",
            "",
        ])
    lines.extend([
        "## Verdict",
        "",
        "RE-016 does not prove item control-flow equivalence. It finds exact size-sequence coverage only for group `12`; groups `4, 5, 6, 7, 8, 9, 10, 11` remain mismatched even though their call counts became representable in RE-015. Do not add `(F)`, `(D)`, or `(**)` markers from this evidence.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="TOMB5 repo root")
    parser.add_argument("--original-dump", default=DEFAULT_ORIGINAL_DUMP, help="ignored original dump CSV relative to repo")
    parser.add_argument("--item-flag-csv", default=DEFAULT_ITEM_FLAG_CSV, help="RE-015 item flag CSV relative to repo")
    parser.add_argument("--write-sg-address", default=DEFAULT_WRITE_SG_ADDRESS, help="final PSX address for WriteSG")
    parser.add_argument("--max-gap", type=int, default=DEFAULT_MAX_GAP, help="start a new group when call indices differ by more than this")
    parser.add_argument("--csv", default=DEFAULT_OUT_CSV, help="versionable CSV output relative to repo")
    parser.add_argument("--md", default=DEFAULT_OUT_MD, help="versionable Markdown output relative to repo")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    audit = build_item_control_flow_audit(
        repo=repo,
        original_dump=repo / args.original_dump,
        item_flag_csv=repo / args.item_flag_csv,
        write_sg_address=args.write_sg_address,
        max_gap=args.max_gap,
    )
    csv_path = repo / args.csv
    md_path = repo / args.md
    write_csv(audit, csv_path)
    write_markdown(audit, md_path)
    print(f"item_groups={audit.total_item_groups}")
    print(f"exact_match_groups={_groups_text(audit.exact_match_groups)}")
    print(f"mismatch_groups={_groups_text(audit.mismatch_groups)}")
    print(f"status={audit.status}")
    print(f"csv={csv_path}")
    print(f"md={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
