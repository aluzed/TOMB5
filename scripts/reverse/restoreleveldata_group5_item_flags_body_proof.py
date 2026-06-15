#!/usr/bin/env python3
"""Build the RE-029 RestoreLevelData group 5 item_flags body proof.

This proof narrows the RE-028 checklist to the `item_flags[0..3]` payload
family. It records source-visible header predicates and restore-side candidate
width context, but keeps the result blocked because no source write bodies or
restore assignment identities are present in versionable evidence.
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

DEFAULT_CHECKLIST_CSV = "docs/reverse/generated/restoreleveldata-group5-source-field-identity-checklist.csv"
DEFAULT_FIELD_WIDTH_CSV = "docs/reverse/generated/saveleveldata-item-field-width-audit.csv"
DEFAULT_READ_MAP_CSV = "docs/reverse/generated/restoreleveldata-read-call-map.csv"
DEFAULT_BRANCH_MAP_CSV = "docs/reverse/generated/restoreleveldata-branch-predicate-map.csv"
DEFAULT_SOURCE_FILE = "GAME/SAVEGAME.C"
DEFAULT_OUT_CSV = "docs/reverse/generated/restoreleveldata-group5-item-flags-body-proof.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/restoreleveldata-group5-item-flags-body-proof.md"
STORY_PATH = "docs/stories/RE-029-restoreleveldata-group5-item-flags-body-proof.md"
SOURCE_INPUTS = ("RE-017", "RE-021", "RE-028", "GAME/SAVEGAME.C")
TARGET_SAVE_GROUP = 5
RESTORE_GROUP = 6
PAYLOAD_FAMILY = "item_flags[0..3]"
MASK_BY_FLAG_INDEX = {0: "0x80", 1: "0x100", 2: "0x200", 3: "0x400"}


@dataclass(frozen=True)
class Group5ItemFlagsBodyProofRow:
    flag_index: int
    payload_field: str
    header_predicate: str
    source_body_evidence: str
    save_payload_width: int
    restore_candidate_width: int
    restore_candidate_context: str
    body_order_status: str
    proof_status: str
    code_change_readiness: str
    safe_next_action: str
    recommended_next_ticket: str


@dataclass(frozen=True)
class Group5ItemFlagsBodyProof:
    story_id: str
    checklist_csv: Path
    field_width_csv: Path
    read_map_csv: Path
    branch_map_csv: Path
    source_file: Path
    source_inputs: tuple[str, ...]
    target_save_group: int
    restore_group: int
    payload_family: str
    rows: tuple[Group5ItemFlagsBodyProofRow, ...]
    rows_count: int
    patch_ready_count: int
    status: str


def _relative_to_repo(path: Path, repo: Path) -> Path:
    try:
        return path.resolve().relative_to(repo.resolve())
    except ValueError:
        return path


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _source_has_header_predicate(source_text: str, index: int, mask: str) -> bool:
    pattern = rf"if\s*\(\s*item->item_flags\[{index}\]\s*\)\s*word\s*\|=\s*{re.escape(mask)}\s*;"
    return re.search(pattern, source_text, flags=re.MULTILINE) is not None


def _source_has_separate_write(source_text: str, index: int) -> bool:
    return f"Write(&item->item_flags[{index}]" in source_text or f"Write(item->item_flags + {index}" in source_text


def _save_payload_width(field_width_rows: list[dict[str, str]], index: int) -> int:
    field = f"item->item_flags[{index}] payload"
    for row in field_width_rows:
        if row.get("original_group") == str(TARGET_SAVE_GROUP) and row.get("probable_source_field") == field:
            return int(row["original_size"])
    raise ValueError(f"missing field-width row for {field}")


def _restore_candidate_width(read_map_rows: list[dict[str, str]], branch_map_rows: list[dict[str, str]]) -> tuple[int, str]:
    read_group = next(row for row in read_map_rows if row.get("record_kind") == "restore-read-group" and row.get("restore_group") == str(RESTORE_GROUP))
    branch_group = next(row for row in branch_map_rows if row.get("restore_group") == str(RESTORE_GROUP))
    widths = [int(part) for part in read_group["size_sequence"].split(",")]
    candidate_width = 2 if 2 in widths else 0
    context = f"restore group {RESTORE_GROUP} compact branch payload cluster"
    if branch_group.get("predicate_hypothesis") != "object-payload-anchor-compact-branch":
        context = f"restore group {RESTORE_GROUP} payload cluster"
    return candidate_width, context


def build_restoreleveldata_group5_item_flags_body_proof(
    repo: Path,
    checklist_csv: Path,
    field_width_csv: Path,
    read_map_csv: Path,
    branch_map_csv: Path,
    source_file: Path,
) -> Group5ItemFlagsBodyProof:
    checklist_rows = _read_csv(checklist_csv)
    checklist_row = next(row for row in checklist_rows if row.get("payload_family") == PAYLOAD_FAMILY)
    if checklist_row.get("code_change_readiness") != "blocked":
        raise ValueError("RE-029 expects RE-028 item_flags checklist row to remain blocked")

    field_width_rows = _read_csv(field_width_csv)
    read_map_rows = _read_csv(read_map_csv)
    branch_map_rows = _read_csv(branch_map_csv)
    source_text = source_file.read_text(encoding="utf-8")
    restore_width, restore_context = _restore_candidate_width(read_map_rows, branch_map_rows)

    rows: list[Group5ItemFlagsBodyProofRow] = []
    for index, mask in MASK_BY_FLAG_INDEX.items():
        if not _source_has_header_predicate(source_text, index, mask):
            raise ValueError(f"missing source header predicate for item_flags[{index}]")
        source_body_evidence = "separate Write site present" if _source_has_separate_write(source_text, index) else "no separate Write site in current source"
        rows.append(
            Group5ItemFlagsBodyProofRow(
                flag_index=index,
                payload_field=f"item->item_flags[{index}] payload",
                header_predicate=f"item->item_flags[{index}] -> word bit {mask}",
                source_body_evidence=source_body_evidence,
                save_payload_width=_save_payload_width(field_width_rows, index),
                restore_candidate_width=restore_width,
                restore_candidate_context=restore_context,
                body_order_status="candidate-width-only",
                proof_status="payload-body-identity-missing",
                code_change_readiness="blocked",
                safe_next_action="do not patch; recover source/restore assignment identity before serializer edit",
                recommended_next_ticket="RE-030",
            )
        )

    patch_ready = sum(1 for row in rows if row.code_change_readiness == "ready")
    return Group5ItemFlagsBodyProof(
        story_id="RE-029",
        checklist_csv=_relative_to_repo(checklist_csv, repo),
        field_width_csv=_relative_to_repo(field_width_csv, repo),
        read_map_csv=_relative_to_repo(read_map_csv, repo),
        branch_map_csv=_relative_to_repo(branch_map_csv, repo),
        source_file=_relative_to_repo(source_file, repo),
        source_inputs=SOURCE_INPUTS,
        target_save_group=TARGET_SAVE_GROUP,
        restore_group=RESTORE_GROUP,
        payload_family=PAYLOAD_FAMILY,
        rows=tuple(rows),
        rows_count=len(rows),
        patch_ready_count=patch_ready,
        status="restoreleveldata-group5-item-flags-body-proof-blocked",
    )


def write_csv(proof: Group5ItemFlagsBodyProof, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "flag_index",
        "payload_field",
        "header_predicate",
        "source_body_evidence",
        "save_payload_width",
        "restore_candidate_width",
        "restore_candidate_context",
        "body_order_status",
        "proof_status",
        "code_change_readiness",
        "safe_next_action",
        "recommended_next_ticket",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in proof.rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def write_markdown(proof: Group5ItemFlagsBodyProof, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RestoreLevelData group 5 item_flags body proof",
        "",
        "Status: Generated",
        f"Story: `{STORY_PATH}`",
        "",
        "## Progress tracker",
        "",
        "- [x] Select RE-028 payload family `item_flags[0..3]`.",
        "- [x] Load RE-017 save-side field-width metadata for the four item flag payloads.",
        "- [x] Load RE-021 restore group `6` branch context and RE-019 read-size context.",
        "- [x] Inspect current source text for header predicates and separate payload write sites.",
        "- [x] Publish per-flag body proof rows while keeping patch readiness blocked.",
        "- [x] Keep raw opcode text, machine words, payload coordinates, addresses, and branch/call targets out of versioned outputs.",
        "",
        "## Inputs",
        "",
        f"- RE-028 checklist CSV: `{proof.checklist_csv}`",
        f"- RE-017 field-width CSV: `{proof.field_width_csv}`",
        f"- RE-019 read map CSV: `{proof.read_map_csv}`",
        f"- RE-021 branch map CSV: `{proof.branch_map_csv}`",
        f"- Source file inspected: `{proof.source_file}`",
        "",
        "## Summary",
        "",
        f"- source inputs: `{', '.join(proof.source_inputs)}`",
        f"- target save group: `{proof.target_save_group}`",
        f"- restore group: `{proof.restore_group}`",
        f"- payload family: `{proof.payload_family}`",
        f"- proof rows: `{proof.rows_count}`",
        f"- patch-ready rows: `{proof.patch_ready_count}`",
        f"- status: `{proof.status}`",
        "",
        "## Item flag body rows",
    ]
    for row in proof.rows:
        lines.extend([
            "",
            f"### item_flags[{row.flag_index}]",
            "",
            f"- payload field: `{row.payload_field}`",
            f"- header predicate: `{row.header_predicate}`",
            f"- source body evidence: `{row.source_body_evidence}`",
            f"- save payload width: `{row.save_payload_width}`",
            f"- restore candidate width: `{row.restore_candidate_width}`",
            f"- restore candidate context: `{row.restore_candidate_context}`",
            f"- body order status: `{row.body_order_status}`",
            f"- proof status: `{row.proof_status}`",
            f"- code change readiness: `{row.code_change_readiness}`",
            f"- safe next action: `{row.safe_next_action}`",
            f"- recommended next ticket: `{row.recommended_next_ticket}`",
        ])
    lines.extend([
        "",
        "## Verdict",
        "",
        "RE-029 proves the current limit for the `item_flags[0..3]` payload family: all four header predicates are visible in source, and 2-byte payload widths are present in metadata, but there are no separate source write bodies or versioned restore assignment identities. The result is candidate-width-only, not source-field identity proof.",
        "",
        "Do not add `(F)`, `(D)`, or `(**)` markers; do not patch `GAME/SAVEGAME.C` from this proof alone.",
        "",
        "Recommended next ticket: RE-030 — recover a versionable restore assignment identity map for group `5` payload bodies, or defer group `5` from any source reconstruction scope.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checklist-csv", default=DEFAULT_CHECKLIST_CSV)
    parser.add_argument("--field-width-csv", default=DEFAULT_FIELD_WIDTH_CSV)
    parser.add_argument("--read-map-csv", default=DEFAULT_READ_MAP_CSV)
    parser.add_argument("--branch-map-csv", default=DEFAULT_BRANCH_MAP_CSV)
    parser.add_argument("--source-file", default=DEFAULT_SOURCE_FILE)
    parser.add_argument("--out-csv", default=DEFAULT_OUT_CSV)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    args = parser.parse_args(argv)

    proof = build_restoreleveldata_group5_item_flags_body_proof(
        repo=ROOT,
        checklist_csv=ROOT / args.checklist_csv,
        field_width_csv=ROOT / args.field_width_csv,
        read_map_csv=ROOT / args.read_map_csv,
        branch_map_csv=ROOT / args.branch_map_csv,
        source_file=ROOT / args.source_file,
    )
    write_csv(proof, ROOT / args.out_csv)
    write_markdown(proof, ROOT / args.out_md)
    print(f"wrote {args.out_csv} and {args.out_md}: {proof.status}; patch-ready={proof.patch_ready_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
