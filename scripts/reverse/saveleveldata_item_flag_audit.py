#!/usr/bin/env python3
"""Audit SaveLevelData item-serialization call groups against source flag cases.

This script consumes the versionable RE-013 call-group map plus current source
schema. It does not read the original disassembly dump and does not emit original
instructions or machine words.
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

DEFAULT_CALL_MAP_CSV = "docs/reverse/generated/saveleveldata-write-call-map.csv"
DEFAULT_SOURCE = "GAME/SAVEGAME.C"
DEFAULT_OUT_CSV = "docs/reverse/generated/saveleveldata-item-flag-audit.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/saveleveldata-item-flag-audit.md"


@dataclass(frozen=True)
class ItemGroupRow:
    original_group: int
    original_call_count: int
    first_call_index: int
    last_call_index: int
    first_call_address: str
    last_call_address: str
    candidate_source_rows: str
    candidate_context: str
    count_status: str
    matching_source_cases: str
    notes: str

    def versionable_lines(self) -> list[str]:
        return [
            f"original_group: {self.original_group}",
            f"original_call_count: {self.original_call_count}",
            f"first_call_index: {self.first_call_index}",
            f"last_call_index: {self.last_call_index}",
            f"first_call_address: {self.first_call_address}",
            f"last_call_address: {self.last_call_address}",
            f"candidate_source_rows: {self.candidate_source_rows}",
            f"count_status: {self.count_status}",
            f"matching_source_cases: {self.matching_source_cases}",
        ]


@dataclass(frozen=True)
class ItemFlagAudit:
    source: Path
    call_map_csv: Path
    total_item_groups: int
    total_item_group_calls: int
    active_control_word_written: bool
    save_flags_write_sites: int
    possible_active_branch_counts: tuple[int, ...]
    unrepresented_original_groups: tuple[int, ...]
    rows: tuple[ItemGroupRow, ...]
    status: str


def _relative_to_repo(path: Path, repo: Path) -> Path:
    try:
        return path.resolve().relative_to(repo.resolve())
    except ValueError:
        return path


def _function_body(source: Path, name: str) -> str:
    text = source.read_text(encoding="utf-8")
    signature = f"void {name}(int FullSave)"
    start = text.index(signature)
    brace = text.index("{", start)
    depth = 0
    for pos in range(brace, len(text)):
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
            if depth == 0:
                return text[brace + 1:pos]
    raise ValueError(f"function not closed: {name}")


def active_control_word_written(source: Path) -> bool:
    body = _function_body(source, "SaveLevelData")
    active_start = body.index("word = 0x8000;")
    branch_tail = body.index("if (obj->save_flags)", active_start)
    active_region = body[active_start:branch_tail]
    return bool(re.search(r"\bWrite\s*\(\s*&word\s*,\s*2\s*\)\s*;", active_region))


def _block_from_control(body: str, control_text: str) -> str:
    start = body.index(control_text)
    brace = body.index("{", start)
    depth = 0
    for pos in range(brace, len(body)):
        if body[pos] == "{":
            depth += 1
        elif body[pos] == "}":
            depth -= 1
            if depth == 0:
                return body[brace + 1:pos]
    raise ValueError(f"control block not closed: {control_text}")


def count_save_flags_write_sites(source: Path) -> int:
    body = _function_body(source, "SaveLevelData")
    region = _block_from_control(body, "if (obj->save_flags)")
    return len(re.findall(r"\bWrite\s*\(", region))


def possible_active_branch_counts(active_control_word_sites: int = 0, save_flags_write_sites: int = 0) -> tuple[int, ...]:
    # Source model:
    # - active_header: one control word write when the active/full-save branch serializes `word`.
    # - save_position: absent or five required writes plus four optional low-bit/speed writes.
    # - save_anim: absent or five writes (states, anim number/byte, frame).
    # - save_hitpoints: absent or one write.
    # - save_flags: absent or the current number of Write(...) sites in the save_flags block.
    active_header_counts = [active_control_word_sites]
    position_counts = [0, 5, 6, 7, 8, 9]
    anim_counts = [0, 5]
    hitpoint_counts = [0, 1]
    save_flags_counts = [0]
    if save_flags_write_sites:
        save_flags_counts.append(save_flags_write_sites)
    counts = {
        header + p + a + h + f
        for header in active_header_counts
        for p in position_counts
        for a in anim_counts
        for h in hitpoint_counts
        for f in save_flags_counts
    }
    return tuple(sorted(counts))


def _matching_cases(call_count: int, active_control_word_sites: int = 0, save_flags_write_sites: int = 0) -> str:
    cases: list[str] = []
    save_flags_counts = [0]
    if save_flags_write_sites:
        save_flags_counts.append(save_flags_write_sites)
    for position in [0, 5, 6, 7, 8, 9]:
        for anim in [0, 5]:
            for hitpoints in [0, 1]:
                for save_flags in save_flags_counts:
                    total = active_control_word_sites + position + anim + hitpoints + save_flags
                    if total == call_count:
                        parts = []
                        if active_control_word_sites:
                            parts.append(f"active_header={active_control_word_sites}")
                        if position:
                            parts.append(f"save_position={position}")
                        if anim:
                            parts.append("save_anim=5")
                        if hitpoints:
                            parts.append("save_hitpoints=1")
                        if save_flags:
                            parts.append(f"save_flags={save_flags}")
                        if not parts:
                            parts.append("no optional source writes")
                        cases.append(" + ".join(parts))
    return "; ".join(cases) if cases else "none"


def _read_item_group_rows(call_map_csv: Path) -> list[dict[str, str]]:
    with call_map_csv.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    # RE-013 identified groups 4-12 as repeated item-serialization candidates.
    return [row for row in rows if int(row["original_group"]) >= 4]


def build_item_flag_audit(repo: Path, call_map_csv: Path, source: Path) -> ItemFlagAudit:
    has_active_header = active_control_word_written(source)
    save_flags_writes = count_save_flags_write_sites(source)
    active_header_writes = 1 if has_active_header else 0
    source_counts = possible_active_branch_counts(
        active_control_word_sites=active_header_writes,
        save_flags_write_sites=save_flags_writes,
    )
    rows: list[ItemGroupRow] = []
    unrepresented: list[int] = []
    for raw in _read_item_group_rows(call_map_csv):
        group = int(raw["original_group"])
        call_count = int(raw["original_call_count"])
        representable = call_count in source_counts
        if representable:
            status = "representable-count-needs-control-flow-proof"
            notes = "Count can be produced by current source write-count model; branch conditions still need manual proof."
        else:
            status = "not-representable-by-current-source-count-model"
            unrepresented.append(group)
            if call_count > max(source_counts):
                notes = "Count exceeds current source maximum; likely missing active control word and/or save_flags writes."
            else:
                notes = "Count falls into a gap in current optional flag combinations; audit original branch boundaries."
        rows.append(ItemGroupRow(
            original_group=group,
            original_call_count=call_count,
            first_call_index=int(raw["first_call_index"]),
            last_call_index=int(raw["last_call_index"]),
            first_call_address=raw["first_call_address"],
            last_call_address=raw["last_call_address"],
            candidate_source_rows=raw["candidate_source_rows"],
            candidate_context=raw["candidate_context"],
            count_status=status,
            matching_source_cases=_matching_cases(
                call_count,
                active_control_word_sites=active_header_writes,
                save_flags_write_sites=save_flags_writes,
            ),
            notes=notes,
        ))
    status = "source-gaps-found" if unrepresented or not has_active_header or save_flags_writes == 0 else "counts-representable-needs-proof"
    return ItemFlagAudit(
        source=_relative_to_repo(source, repo),
        call_map_csv=_relative_to_repo(call_map_csv, repo),
        total_item_groups=len(rows),
        total_item_group_calls=sum(row.original_call_count for row in rows),
        active_control_word_written=has_active_header,
        save_flags_write_sites=save_flags_writes,
        possible_active_branch_counts=source_counts,
        unrepresented_original_groups=tuple(unrepresented),
        rows=tuple(rows),
        status=status,
    )


def write_csv(audit: ItemFlagAudit, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "original_group", "original_call_count", "first_call_index", "last_call_index",
        "first_call_address", "last_call_address", "candidate_source_rows",
        "candidate_context", "count_status", "matching_source_cases", "notes",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in audit.rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def write_markdown(audit: ItemFlagAudit, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    groups = ", ".join(str(group) for group in audit.unrepresented_original_groups) or "none"
    lines = [
        "# SaveLevelData item flag audit",
        "",
        "Status: Generated",
        "Story: `docs/stories/RE-015-saveleveldata-active-item-serialization.md`",
        "",
        "## Progress tracker",
        "",
        "- [x] Model source item serialization write-count cases.",
        "- [x] Compare RE-013 item call groups against the source count model.",
        "- [x] Identify source gaps without versioning original instructions or bytes.",
        "- [x] Preserve marker verdict limits.",
        "",
        "## Inputs",
        "",
        f"- Source: `{audit.source}`",
        f"- Call-group map CSV: `{audit.call_map_csv}`",
        "",
        "## Summary",
        "",
        f"- item candidate groups: `{audit.total_item_groups}`",
        f"- original item-group `WriteSG` calls: `{audit.total_item_group_calls}`",
        f"- possible current-source active branch counts: `{', '.join(str(v) for v in audit.possible_active_branch_counts)}`",
        f"- active control word written: `{'yes' if audit.active_control_word_written else 'no'}`",
        f"- save_flags write sites: `{audit.save_flags_write_sites}`",
        f"- unrepresented original item groups: `{groups}`",
        f"- status: `{audit.status}`",
        "",
        "## Source count model",
        "",
        "The active/full-save item branch is modeled as:",
        "",
        "- `save_position`: absent, or 5 required writes plus up to 4 optional writes (`x_rot`, `z_rot`, `speed`, `fallspeed`).",
        "- `save_anim`: absent, or 5 writes (`current`, `goal`, `required`, anim number/byte, frame).",
        "- `save_hitpoints`: absent, or 1 write.",
        "- `save_flags`: absent, or one packed 32-bit write (`flags` plus active/status bitfield low 15 bits).",
        "- active branch control word: written once after `word` is assembled and before optional payload fields.",
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
            f"- candidate source rows: `{row.candidate_source_rows}`",
            f"- candidate context: `{row.candidate_context}`",
            f"- count status: `{row.count_status}`",
            f"- matching source cases: `{row.matching_source_cases}`",
            f"- notes: {row.notes}",
            "",
        ])
    lines.extend([
        "## Verdict",
        "",
        "RE-015 resolves the source-level count gaps that RE-014 identified: the active item branch now writes the control word, and `obj->save_flags` now serializes one packed 32-bit flags word. The original item groups are therefore representable by source write counts, including groups `4` and `6`; this is still a count-level result, not a control-flow equivalence proof, so no `(F)`, `(D)`, or `(**)` marker is justified yet.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="TOMB5 repo root")
    parser.add_argument("--call-map-csv", default=DEFAULT_CALL_MAP_CSV, help="RE-013 call map CSV relative to repo")
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="source file relative to repo")
    parser.add_argument("--csv", default=DEFAULT_OUT_CSV, help="versionable CSV output relative to repo")
    parser.add_argument("--md", default=DEFAULT_OUT_MD, help="versionable markdown output relative to repo")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    audit = build_item_flag_audit(
        repo=repo,
        call_map_csv=repo / args.call_map_csv,
        source=repo / args.source,
    )
    csv_path = repo / args.csv
    md_path = repo / args.md
    write_csv(audit, csv_path)
    write_markdown(audit, md_path)
    groups = ",".join(str(group) for group in audit.unrepresented_original_groups) or "none"
    print(f"item_groups={audit.total_item_groups}")
    print(f"item_group_calls={audit.total_item_group_calls}")
    print(f"active_control_word_written={'yes' if audit.active_control_word_written else 'no'}")
    print(f"save_flags_write_sites={audit.save_flags_write_sites}")
    print(f"unrepresented_groups={groups}")
    print(f"status={audit.status}")
    print(f"csv={csv_path}")
    print(f"md={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
