#!/usr/bin/env python3
"""Build a metadata-only SaveLevelData item field/width reconciliation table."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.reverse.saveleveldata_call_map import DEFAULT_MAX_GAP, DEFAULT_WRITE_SG_ADDRESS
from scripts.reverse.saveleveldata_item_control_flow_audit import extract_write_sg_size_groups

DEFAULT_ORIGINAL_DUMP = "build/reverse/re007/original/SaveLevelData_80053f10.csv"
DEFAULT_CONTROL_FLOW_CSV = "docs/reverse/generated/saveleveldata-item-control-flow-audit.csv"
DEFAULT_OUT_CSV = "docs/reverse/generated/saveleveldata-item-field-width-audit.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/saveleveldata-item-field-width-audit.md"


@dataclass(frozen=True)
class FieldHypothesis:
    probable_source_field: str
    source_size: int | None
    gap_status: str
    evidence: str


@dataclass(frozen=True)
class ItemFieldWidthRow:
    original_group: int
    call_ordinal: int
    call_index: int
    call_address: str
    original_size: int | None
    probable_source_field: str
    source_size: int | None
    gap_status: str
    evidence: str

    def versionable_lines(self) -> list[str]:
        return [
            f"original_group: {self.original_group}",
            f"call_ordinal: {self.call_ordinal}",
            f"call_index: {self.call_index}",
            f"call_address: {self.call_address}",
            f"original_size: {self.original_size}",
            f"probable_source_field: {self.probable_source_field}",
            f"source_size: {self.source_size}",
            f"gap_status: {self.gap_status}",
        ]


@dataclass(frozen=True)
class ItemFieldWidthAudit:
    original_dump: Path
    control_flow_csv: Path
    write_sg_address: str
    mismatch_groups: tuple[int, ...]
    total_original_calls: int
    gap_counts: dict[str, int]
    priority_findings: tuple[str, ...]
    rows: tuple[ItemFieldWidthRow, ...]
    status: str


def _relative_to_repo(path: Path, repo: Path) -> Path:
    try:
        return path.resolve().relative_to(repo.resolve())
    except ValueError:
        return path


def _read_mismatch_groups(control_flow_csv: Path) -> tuple[int, ...]:
    with control_flow_csv.open(newline="", encoding="utf-8") as f:
        rows = csv.DictReader(f)
        return tuple(
            int(row["original_group"])
            for row in rows
            if row.get("control_flow_status") == "size-sequence-mismatch"
        )


def _field_map() -> dict[tuple[int, int], FieldHypothesis]:
    exact = "exact-field-width-match"
    width = "source-width-mismatch"
    missing = "source-missing-field"
    layout = "source-layout-mismatch"
    boundary = "branch-boundary-or-sentinel"
    unknown = "needs-manual-field-proof"
    return {
        # Group 4: active header + position + anim/hitpoint region. The three
        # anim state payloads are byte-sized in the original metadata but 2-byte
        # writes in the current source.
        (4, 1): FieldHypothesis("active control header", 2, exact, "header coordinate matches current source"),
        (4, 2): FieldHypothesis("item->pos.x_pos packed", 2, exact, "position payload width matches"),
        (4, 3): FieldHypothesis("item->pos.y_pos packed", 2, exact, "position payload width matches"),
        (4, 4): FieldHypothesis("item->pos.z_pos packed", 2, exact, "position payload width matches"),
        (4, 5): FieldHypothesis("item->room_number", 1, exact, "room byte width matches"),
        (4, 6): FieldHypothesis("item->pos.y_rot", 2, exact, "rotation width matches"),
        (4, 7): FieldHypothesis("item->pos.x_rot", 2, exact, "optional rotation width matches"),
        (4, 8): FieldHypothesis("item->pos.z_rot", 2, exact, "optional rotation width matches"),
        (4, 9): FieldHypothesis("item->speed", 2, exact, "optional speed width matches"),
        (4, 10): FieldHypothesis("item->fallspeed", 2, exact, "optional fallspeed width matches"),
        (4, 11): FieldHypothesis("item->current_anim_state", 2, width, "original metadata has byte write where current source writes 2"),
        (4, 12): FieldHypothesis("item->goal_anim_state", 2, width, "original metadata has byte write where current source writes 2"),
        (4, 13): FieldHypothesis("item->required_anim_state", 2, width, "original metadata has byte write where current source writes 2"),
        (4, 14): FieldHypothesis("item->anim_number", 2, exact, "Lara anim-number variant width matches"),
        (4, 15): FieldHypothesis("item->anim_number - obj->anim_index", 1, exact, "non-Lara anim-number variant width matches"),
        (4, 16): FieldHypothesis("item->frame_number", 2, exact, "frame width matches"),
        (4, 17): FieldHypothesis("item->hit_points", 2, exact, "hitpoint width matches"),
        # Group 5: current source only records these as header bits or a packed
        # save_flags word; the original metadata exposes separate payload regions.
        (5, 1): FieldHypothesis("packed active/status flags", 4, exact, "packed flag payload width matches RE-015 source addition"),
        (5, 2): FieldHypothesis("item->item_flags[0] payload", None, missing, "current source sets a header bit but has no separate payload write"),
        (5, 3): FieldHypothesis("item->item_flags[1] payload", None, missing, "current source sets a header bit but has no separate payload write"),
        (5, 4): FieldHypothesis("item->item_flags[2] payload", None, missing, "current source sets a header bit but has no separate payload write"),
        (5, 5): FieldHypothesis("item->item_flags[3] payload", None, missing, "current source sets a header bit but has no separate payload write"),
        (5, 6): FieldHypothesis("item->timer payload", None, missing, "current source sets a header bit but has no separate payload write"),
        (5, 7): FieldHypothesis("item->trigger_flags payload", None, missing, "current source sets a header bit but has no separate payload write"),
        (5, 8): FieldHypothesis("object-specific short payload", None, missing, "probable object extension not represented by source branch"),
        (5, 9): FieldHypothesis("object-specific payload block", None, missing, "24-byte original metadata block has no current source equivalent"),
        (5, 10): FieldHypothesis("object-specific short payload", None, missing, "probable object extension not represented by source branch"),
        (5, 11): FieldHypothesis("object-specific short payload", None, missing, "probable object extension not represented by source branch"),
        (5, 12): FieldHypothesis("object-specific short payload", None, missing, "probable object extension not represented by source branch"),
        (5, 13): FieldHypothesis("object-specific short payload", None, missing, "probable object extension not represented by source branch"),
        (5, 14): FieldHypothesis("object-specific short payload", None, missing, "probable object extension not represented by source branch"),
        (5, 15): FieldHypothesis("object-specific payload block", None, missing, "20-byte original metadata block has no current source equivalent"),
        (6, 1): FieldHypothesis("packed byte status/control payload", None, missing, "byte payload is not modeled by current source"),
        (6, 2): FieldHypothesis("item flag/data word payload", 4, layout, "4-byte original payload is separate from current packed source flags"),
        (6, 3): FieldHypothesis("item auxiliary word payload", None, missing, "4-byte original payload has no current source equivalent"),
        (7, 1): FieldHypothesis("item loop sentinel/control byte", None, boundary, "single byte group likely marks branch/loop boundary, not current source header"),
        (8, 1): FieldHypothesis("item branch subtype byte", None, missing, "byte subtype payload is not represented by current source"),
        (8, 2): FieldHypothesis("position vector/block payload", None, layout, "20-byte original block conflicts with current split position writes"),
        (8, 3): FieldHypothesis("room/rotation payload", None, layout, "2-byte original payload does not align with current room byte ordering"),
        (8, 4): FieldHypothesis("item->speed", 2, exact, "speed width matches"),
        (8, 5): FieldHypothesis("item->fallspeed", 2, exact, "fallspeed width matches"),
        (8, 6): FieldHypothesis("item data pointer/word payload", None, missing, "4-byte original payload has no current source equivalent"),
        (8, 7): FieldHypothesis("item->item_flags[3] payload", None, missing, "separate item flag payload not modeled"),
        (8, 8): FieldHypothesis("item->item_flags[0] payload", None, missing, "separate item flag payload not modeled"),
        (8, 9): FieldHypothesis("item->item_flags[1] payload", None, missing, "separate item flag payload not modeled"),
        (8, 10): FieldHypothesis("item->current_anim_state", 2, exact, "anim state width matches in this branch"),
        (8, 11): FieldHypothesis("item->goal_anim_state", 2, exact, "anim state width matches in this branch"),
        (8, 12): FieldHypothesis("item->required_anim_state", 2, exact, "anim state width matches in this branch"),
        (9, 1): FieldHypothesis("item list/sentinel byte", None, boundary, "single byte group likely marks branch/loop boundary"),
        (10, 1): FieldHypothesis("active control header", 2, exact, "header width matches"),
        (10, 2): FieldHypothesis("item->pos.x_pos packed", 2, exact, "position payload width matches"),
        (10, 3): FieldHypothesis("item->pos.y_pos packed", 2, exact, "position payload width matches"),
        (10, 4): FieldHypothesis("item->pos.z_pos packed", 2, exact, "position payload width matches"),
        (10, 5): FieldHypothesis("item->pos.y_rot", 2, exact, "rotation width matches"),
        (10, 6): FieldHypothesis("item->pos.x_rot", 2, exact, "optional rotation width matches"),
        (10, 7): FieldHypothesis("item->room_number", 1, layout, "room byte appears after position/rotation in original metadata but earlier in current source"),
        (11, 1): FieldHypothesis("item list/sentinel byte", None, boundary, "single byte group likely marks branch/loop boundary"),
    }


def _priority_findings(rows: tuple[ItemFieldWidthRow, ...]) -> tuple[str, ...]:
    findings: list[str] = []
    anim_width = [row for row in rows if row.gap_status == "source-width-mismatch" and "anim_state" in row.probable_source_field]
    if anim_width:
        groups = sorted({row.original_group for row in anim_width})
        findings.append(f"anim-state-byte-width: {len(anim_width)} writes in groups {', '.join(map(str, groups))} are byte-sized original metadata vs 2-byte current source")
    large_missing = [row for row in rows if row.gap_status in {"source-missing-field", "source-layout-mismatch"} and row.original_size in {4, 20, 24}]
    if large_missing:
        sizes = sorted({row.original_size for row in large_missing if row.original_size is not None})
        findings.append(f"unmodeled-large-payloads: original sizes {', '.join(map(str, sizes))} require source field reconciliation")
    separate_flags = [row for row in rows if "item_flags" in row.probable_source_field and row.gap_status == "source-missing-field"]
    if separate_flags:
        findings.append(f"separate-item-flag-payloads: {len(separate_flags)} probable item_flags payload writes are not modeled as source writes")
    return tuple(findings)


def build_item_field_width_audit(repo: Path, original_dump: Path, control_flow_csv: Path, write_sg_address: str, max_gap: int = DEFAULT_MAX_GAP) -> ItemFieldWidthAudit:
    mismatch_groups = _read_mismatch_groups(control_flow_csv)
    grouped_calls = extract_write_sg_size_groups(original_dump, write_sg_address, max_gap=max_gap)
    field_map = _field_map()
    rows: list[ItemFieldWidthRow] = []
    for group_id in mismatch_groups:
        calls = grouped_calls[group_id - 1]
        for ordinal, call in enumerate(calls, 1):
            hypothesis = field_map.get(
                (group_id, ordinal),
                FieldHypothesis("unmapped original payload", None, "needs-manual-field-proof", "no conservative field hypothesis assigned"),
            )
            rows.append(ItemFieldWidthRow(
                original_group=group_id,
                call_ordinal=ordinal,
                call_index=call.index,
                call_address=call.address,
                original_size=call.size,
                probable_source_field=hypothesis.probable_source_field,
                source_size=hypothesis.source_size,
                gap_status=hypothesis.gap_status,
                evidence=hypothesis.evidence,
            ))
    row_tuple = tuple(rows)
    gap_counts = dict(Counter(row.gap_status for row in row_tuple))
    status = "field-width-gaps-found" if any(status != "exact-field-width-match" for status in gap_counts) else "field-widths-covered"
    return ItemFieldWidthAudit(
        original_dump=_relative_to_repo(original_dump, repo),
        control_flow_csv=_relative_to_repo(control_flow_csv, repo),
        write_sg_address=write_sg_address.lower(),
        mismatch_groups=mismatch_groups,
        total_original_calls=len(row_tuple),
        gap_counts=gap_counts,
        priority_findings=_priority_findings(row_tuple),
        rows=row_tuple,
        status=status,
    )


def write_csv(audit: ItemFieldWidthAudit, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "original_group", "call_ordinal", "call_index", "call_address", "original_size",
        "probable_source_field", "source_size", "gap_status", "evidence",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in audit.rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def _groups_text(groups: tuple[int, ...]) -> str:
    return ", ".join(str(group) for group in groups) or "none"


def write_markdown(audit: ItemFieldWidthAudit, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# SaveLevelData item field/width reconciliation",
        "",
        "Status: Generated",
        "Story: `docs/stories/RE-017-saveleveldata-item-field-width-reconciliation.md`",
        "",
        "## Progress tracker",
        "",
        "- [x] Load RE-016 mismatch groups.",
        "- [x] Derive call-size metadata for the mismatch groups.",
        "- [x] Assign conservative probable source fields and gap statuses.",
        "- [x] Keep raw original rows, binary words, and payload coordinates out of versioned outputs.",
        "- [x] Preserve marker verdict limits.",
        "",
        "## Inputs",
        "",
        f"- Original dump CSV: `{audit.original_dump}` (ignored; not versioned)",
        f"- RE-016 control-flow CSV: `{audit.control_flow_csv}`",
        f"- WriteSG final PSX address: `{audit.write_sg_address}`",
        "",
        "## Summary",
        "",
        f"- mismatch groups covered: `{_groups_text(audit.mismatch_groups)}`",
        f"- original calls classified: `{audit.total_original_calls}`",
        f"- status: `{audit.status}`",
        "",
        "### Gap counts",
        "",
    ]
    for status, count in sorted(audit.gap_counts.items()):
        lines.append(f"- `{status}`: `{count}`")
    lines.extend(["", "### Priority findings", ""])
    for finding in audit.priority_findings:
        lines.append(f"- {finding}")
    lines.extend([
        "",
        "## Field/width table",
        "",
        "The table below is a field hypothesis matrix. It is not an equivalence proof and does not justify `(F)`, `(D)`, or `(**)` markers.",
        "",
    ])
    current_group: int | None = None
    for row in audit.rows:
        if row.original_group != current_group:
            current_group = row.original_group
            lines.extend([f"### Original item group {current_group}", ""])
        lines.extend([
            f"- call {row.call_ordinal} @ `{row.call_address}`",
            f"  - call index: `{row.call_index}`",
            f"  - original size: `{row.original_size}`",
            f"  - probable source field: `{row.probable_source_field}`",
            f"  - source size: `{row.source_size}`",
            f"  - gap status: `{row.gap_status}`",
            f"  - evidence: {row.evidence}",
        ])
    lines.extend([
        "",
        "## Verdict",
        "",
        "RE-017 identifies concrete field/width gaps rather than a serializer patch. The highest-priority gap is that the original metadata shows byte-sized anim-state writes in group `4` while the current source writes those states as 2-byte fields. Additional gaps include separate item flag/timer/trigger payloads and object-specific payload blocks of sizes `4`, `20`, and `24` that are not represented by the current source branch.",
        "",
        "Do not add `(F)`, `(D)`, or `(**)` markers until these field hypotheses are reconciled against restore-side behavior and source changes are proven with tests.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="TOMB5 repo root")
    parser.add_argument("--original-dump", default=DEFAULT_ORIGINAL_DUMP, help="ignored original dump CSV relative to repo")
    parser.add_argument("--control-flow-csv", default=DEFAULT_CONTROL_FLOW_CSV, help="RE-016 control-flow CSV relative to repo")
    parser.add_argument("--write-sg-address", default=DEFAULT_WRITE_SG_ADDRESS, help="final PSX address for WriteSG")
    parser.add_argument("--max-gap", type=int, default=DEFAULT_MAX_GAP, help="start a new group when call indices differ by more than this")
    parser.add_argument("--csv", default=DEFAULT_OUT_CSV, help="versionable CSV output relative to repo")
    parser.add_argument("--md", default=DEFAULT_OUT_MD, help="versionable Markdown output relative to repo")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    audit = build_item_field_width_audit(
        repo=repo,
        original_dump=repo / args.original_dump,
        control_flow_csv=repo / args.control_flow_csv,
        write_sg_address=args.write_sg_address,
        max_gap=args.max_gap,
    )
    csv_path = repo / args.csv
    md_path = repo / args.md
    write_csv(audit, csv_path)
    write_markdown(audit, md_path)
    print(f"mismatch_groups={_groups_text(audit.mismatch_groups)}")
    print(f"classified_original_calls={audit.total_original_calls}")
    print(f"status={audit.status}")
    print(f"priority_findings={len(audit.priority_findings)}")
    print(f"csv={csv_path}")
    print(f"md={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
