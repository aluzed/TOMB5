#!/usr/bin/env python3
"""Build the RE-028 RestoreLevelData group 5 source-field identity checklist.

The checklist stays metadata-only: it consumes versioned proof summaries and source
text only to classify whether source-level field identities are present. It does
not read original dumps, publish raw machine words, or authorize source patches.
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

DEFAULT_PAYLOAD_CSV = "docs/reverse/generated/restoreleveldata-group5-payload-predicate-proof.csv"
DEFAULT_FIELD_WIDTH_CSV = "docs/reverse/generated/saveleveldata-item-field-width-audit.csv"
DEFAULT_SOURCE_FILE = "GAME/SAVEGAME.C"
DEFAULT_OUT_CSV = "docs/reverse/generated/restoreleveldata-group5-source-field-identity-checklist.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/restoreleveldata-group5-source-field-identity-checklist.md"
STORY_PATH = "docs/stories/RE-028-restoreleveldata-group5-source-field-identity-checklist.md"
SOURCE_INPUTS = ("RE-017", "RE-025", "GAME/SAVEGAME.C")
TARGET_SAVE_GROUP = 5
RESTORE_GROUP = 6


@dataclass(frozen=True)
class Group5SourceFieldIdentityRow:
    payload_family: str
    field_width_summary: str
    source_identity_state: str
    restore_identity_state: str
    required_evidence: str
    current_blocker: str
    checklist_status: str
    safe_next_action: str
    code_change_readiness: str
    recommended_next_ticket: str


@dataclass(frozen=True)
class Group5SourceFieldIdentityChecklist:
    story_id: str
    payload_csv: Path
    field_width_csv: Path
    source_file: Path
    source_inputs: tuple[str, ...]
    target_save_group: int
    restore_group: int
    rows: tuple[Group5SourceFieldIdentityRow, ...]
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


def _field_width_summary(rows: list[dict[str, str]], family: str) -> str:
    group5 = [row for row in rows if row.get("original_group") == str(TARGET_SAVE_GROUP)]
    if family == "packed-status-flags":
        return "exact-field-width-match=1;bytes=4"
    if family == "item_flags[0..3]":
        return "source-missing-field=4;bytes=8"
    if family in {"timer", "trigger_flags"}:
        return "source-missing-field=1;bytes=2"
    if family == "object-extension":
        extension_rows = [row for row in group5 if row.get("probable_source_field", "").startswith("object-specific")]
        total_bytes = sum(int(row["original_size"]) for row in extension_rows)
        rare_blocks = sorted({row["original_size"] for row in extension_rows if int(row["original_size"]) > 2}, key=int, reverse=True)
        return f"source-missing-field={len(extension_rows)};bytes={total_bytes};rare-blocks={','.join(rare_blocks)}"
    raise ValueError(f"unsupported family: {family}")


def _source_has_tokens(source_text: str, tokens: tuple[str, ...]) -> bool:
    return all(token in source_text for token in tokens)


def _source_identity_state(family: str, source_text: str) -> str:
    if family == "packed-status-flags":
        if _source_has_tokens(source_text, ("obj->save_flags", "Write(&flags, 4)")):
            return "source-backed packed word; payload cluster anchor only"
        return "packed word source support missing"
    if family == "item_flags[0..3]":
        if _source_has_tokens(source_text, ("item->item_flags[0]", "item->item_flags[1]", "item->item_flags[2]", "item->item_flags[3]")):
            return "header predicates present; separate payload writes absent"
        return "header predicates missing"
    if family == "timer":
        if "item->timer" in source_text:
            return "header predicate present; separate payload write absent"
        return "header predicate missing"
    if family == "trigger_flags":
        if "item->trigger_flags" in source_text:
            return "header predicate present; separate payload write absent"
        return "header predicate missing"
    if family == "object-extension":
        return "no named source field identities for object-specific short/block payloads"
    raise ValueError(f"unsupported family: {family}")


def _required_evidence(family: str) -> str:
    return {
        "packed-status-flags": "restore packed-word assignment map; proof that following payload bodies are independent",
        "item_flags[0..3]": "four source write sites; four restore assignments; body order predicate",
        "timer": "source write site; restore assignment; timer predicate identity",
        "trigger_flags": "source write site; restore assignment; trigger_flags predicate identity",
        "object-extension": "object predicate map; named source fields for short/24-byte/20-byte payloads; restore assignment order",
    }[family]


def _safe_next_action(family: str) -> str:
    return {
        "packed-status-flags": "do not patch; use packed flags only as an anchor while proving dependent payload bodies",
        "item_flags[0..3]": "do not patch; prove item_flags[0..3] payload bodies from source identity first",
        "timer": "do not patch; prove timer payload body and restore assignment from source identity first",
        "trigger_flags": "do not patch; prove trigger_flags payload body and restore assignment from source identity first",
        "object-extension": "do not patch; map object-specific predicates and fields before reconstruction scope",
    }[family]


def _checklist_status(family: str) -> str:
    if family == "packed-status-flags":
        return "anchor-only"
    if family == "object-extension":
        return "source-field-identity-missing"
    return "payload-body-identity-missing"


def build_restoreleveldata_group5_source_field_identity_checklist(
    repo: Path,
    payload_csv: Path,
    field_width_csv: Path,
    source_file: Path,
) -> Group5SourceFieldIdentityChecklist:
    payload_rows = _read_csv(payload_csv)
    field_rows = _read_csv(field_width_csv)
    source_text = source_file.read_text(encoding="utf-8")

    rows: list[Group5SourceFieldIdentityRow] = []
    for payload in payload_rows:
        family = payload["payload_family"]
        rows.append(
            Group5SourceFieldIdentityRow(
                payload_family=family,
                field_width_summary=_field_width_summary(field_rows, family),
                source_identity_state=_source_identity_state(family, source_text),
                restore_identity_state="restore group 6 has compact branch/payload anchor but no versioned assignment identity",
                required_evidence=_required_evidence(family),
                current_blocker=payload["blocking_predicates"],
                checklist_status=_checklist_status(family),
                safe_next_action=_safe_next_action(family),
                code_change_readiness="blocked",
                recommended_next_ticket="RE-029",
            )
        )

    patch_ready = sum(1 for row in rows if row.code_change_readiness == "ready")
    return Group5SourceFieldIdentityChecklist(
        story_id="RE-028",
        payload_csv=_relative_to_repo(payload_csv, repo),
        field_width_csv=_relative_to_repo(field_width_csv, repo),
        source_file=_relative_to_repo(source_file, repo),
        source_inputs=SOURCE_INPUTS,
        target_save_group=TARGET_SAVE_GROUP,
        restore_group=RESTORE_GROUP,
        rows=tuple(rows),
        rows_count=len(rows),
        patch_ready_count=patch_ready,
        status="restoreleveldata-group5-source-field-identity-checklist-blocked",
    )


def write_csv(checklist: Group5SourceFieldIdentityChecklist, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "payload_family",
        "field_width_summary",
        "source_identity_state",
        "restore_identity_state",
        "required_evidence",
        "current_blocker",
        "checklist_status",
        "safe_next_action",
        "code_change_readiness",
        "recommended_next_ticket",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in checklist.rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def write_markdown(checklist: Group5SourceFieldIdentityChecklist, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RestoreLevelData group 5 source-field identity checklist",
        "",
        "Status: Generated",
        f"Story: `{STORY_PATH}`",
        "",
        "## Progress tracker",
        "",
        "- [x] Select save group `5` as the highest-value blocked family from RE-027.",
        "- [x] Load RE-025 payload predicate metadata.",
        "- [x] Load RE-017 field-width reconciliation metadata for save group `5`.",
        "- [x] Inspect current source text only for named field/predicate presence.",
        "- [x] Publish required source-field identity evidence per payload family.",
        "- [x] Keep all rows blocked until restore assignment identity and source write bodies exist.",
        "- [x] Keep raw opcode text, machine words, payload coordinates, addresses, and branch/call targets out of versioned outputs.",
        "",
        "## Inputs",
        "",
        f"- RE-025 payload CSV: `{checklist.payload_csv}`",
        f"- RE-017 field-width CSV: `{checklist.field_width_csv}`",
        f"- Source file inspected: `{checklist.source_file}`",
        "",
        "## Summary",
        "",
        f"- source inputs: `{', '.join(checklist.source_inputs)}`",
        f"- target save group: `{checklist.target_save_group}`",
        f"- restore group: `{checklist.restore_group}`",
        f"- checklist rows: `{checklist.rows_count}`",
        f"- patch-ready checklist rows: `{checklist.patch_ready_count}`",
        f"- status: `{checklist.status}`",
        "",
        "## Checklist rows",
    ]
    for row in checklist.rows:
        lines.extend([
            "",
            f"### {row.payload_family}",
            "",
            f"- field-width summary: `{row.field_width_summary}`",
            f"- source identity state: `{row.source_identity_state}`",
            f"- restore identity state: `{row.restore_identity_state}`",
            f"- required evidence: `{row.required_evidence}`",
            f"- current blocker: `{row.current_blocker}`",
            f"- checklist status: `{row.checklist_status}`",
            f"- safe next action: `{row.safe_next_action}`",
            f"- code change readiness: `{row.code_change_readiness}`",
            f"- recommended next ticket: `{row.recommended_next_ticket}`",
        ])
    lines.extend([
        "",
        "## Verdict",
        "",
        "RE-028 defines the source-field identity checklist for the save group `5` payload cluster. The packed status word is only an anchor. The item flag, timer, trigger flag, and object-extension bodies still lack enough source write and restore assignment identity for a source reconstruction patch.",
        "",
        "Do not add `(F)`, `(D)`, or `(**)` markers; do not patch `GAME/SAVEGAME.C` from this checklist alone.",
        "",
        "Recommended next ticket: RE-029 — prove one group 5 payload-body family end-to-end, starting with `item_flags[0..3]` if source identities can be recovered without publishing raw dump payloads.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--payload-csv", default=DEFAULT_PAYLOAD_CSV)
    parser.add_argument("--field-width-csv", default=DEFAULT_FIELD_WIDTH_CSV)
    parser.add_argument("--source-file", default=DEFAULT_SOURCE_FILE)
    parser.add_argument("--out-csv", default=DEFAULT_OUT_CSV)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    args = parser.parse_args(argv)

    checklist = build_restoreleveldata_group5_source_field_identity_checklist(
        repo=ROOT,
        payload_csv=ROOT / args.payload_csv,
        field_width_csv=ROOT / args.field_width_csv,
        source_file=ROOT / args.source_file,
    )
    write_csv(checklist, ROOT / args.out_csv)
    write_markdown(checklist, ROOT / args.out_md)
    print(f"wrote {args.out_csv} and {args.out_md}: {checklist.status}; patch-ready={checklist.patch_ready_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
