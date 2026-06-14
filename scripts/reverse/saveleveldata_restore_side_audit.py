#!/usr/bin/env python3
"""Audit RE-017 SaveLevelData item hypotheses against restore-side source state.

This stage intentionally does not patch serializers. It records whether the
current source-side RestoreLevelData implementation can support, reject, or not
verify RE-017 field/width hypotheses.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_SOURCE = "GAME/SAVEGAME.C"
DEFAULT_FIELD_WIDTH_CSV = "docs/reverse/generated/saveleveldata-item-field-width-audit.csv"
DEFAULT_OUT_CSV = "docs/reverse/generated/saveleveldata-restore-side-audit.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/saveleveldata-restore-side-audit.md"


@dataclass(frozen=True)
class RestoreSideRow:
    original_group: int
    call_ordinal: int
    call_index: int
    call_address: str
    original_size: int | None
    probable_source_field: str
    save_gap_status: str
    restore_side_status: str
    patch_readiness: str
    next_action: str


@dataclass(frozen=True)
class RestoreSideAudit:
    source: Path
    field_width_csv: Path
    restore_function_status: str
    total_hypotheses: int
    priority_hypotheses: int
    patch_ready_count: int
    restore_status_counts: dict[str, int]
    rows: tuple[RestoreSideRow, ...]
    status: str


def _relative_to_repo(path: Path, repo: Path) -> Path:
    try:
        return path.resolve().relative_to(repo.resolve())
    except ValueError:
        return path


def _restore_function_status(source: Path) -> str:
    text = source.read_text(encoding="utf-8", errors="replace")
    start = text.find("void RestoreLevelData")
    if start == -1:
        return "source-missing"
    brace = text.find("{", start)
    if brace == -1:
        return "source-missing"
    depth = 0
    end = len(text)
    for pos in range(brace, len(text)):
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
            if depth == 0:
                end = pos
                break
    body = text[brace:end]
    if "UNIMPLEMENTED()" in body:
        return "source-unimplemented"
    if "Read(" not in body:
        return "source-no-read-sites"
    return "source-has-read-sites"


def _read_field_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _int_or_none(text: str) -> int | None:
    return int(text) if text not in {"", "None", None} else None


def _restore_status(field: str, gap_status: str, original_size: int | None, restore_function_status: str) -> tuple[str, str, str]:
    if restore_function_status != "source-unimplemented":
        return "needs-restore-source-audit", "blocked", "audit implemented restore-side read sites before patching"

    if gap_status == "source-width-mismatch":
        return "restore-width-unverifiable", "blocked", "derive original RestoreLevelData read width before changing source"
    if gap_status == "source-layout-mismatch":
        if original_size in {20, 24} or "block" in field:
            return "needs-original-restore-proof", "blocked", "prove original restore consumes this layout block before changing source"
        return "restore-layout-unverifiable", "blocked", "derive restore-side ordering/layout before changing source"
    if gap_status == "branch-boundary-or-sentinel":
        return "needs-original-restore-proof", "blocked", "locate matching original RestoreLevelData control byte before source changes"
    if gap_status == "source-missing-field":
        if original_size in {4, 20, 24} or "object-specific" in field or "payload block" in field:
            return "needs-original-restore-proof", "blocked", "prove original restore consumes this payload block before implementing writes"
        return "restore-source-absent", "blocked", "RestoreLevelData is unimplemented; add read-side design/proof before serializer patch"
    if gap_status == "exact-field-width-match":
        return "restore-source-absent", "blocked", "RestoreLevelData is unimplemented; exact save-side width alone is insufficient"
    return "needs-original-restore-proof", "blocked", "manual restore-side proof required"


def build_restore_side_audit(repo: Path, source: Path, field_width_csv: Path) -> RestoreSideAudit:
    restore_status = _restore_function_status(source)
    rows: list[RestoreSideRow] = []
    for row in _read_field_rows(field_width_csv):
        field = row["probable_source_field"]
        gap_status = row["gap_status"]
        original_size = _int_or_none(row.get("original_size"))
        status, readiness, action = _restore_status(field, gap_status, original_size, restore_status)
        rows.append(RestoreSideRow(
            original_group=int(row["original_group"]),
            call_ordinal=int(row["call_ordinal"]),
            call_index=int(row["call_index"]),
            call_address=row["call_address"],
            original_size=original_size,
            probable_source_field=field,
            save_gap_status=gap_status,
            restore_side_status=status,
            patch_readiness=readiness,
            next_action=action,
        ))

    counts = dict(Counter(row.restore_side_status for row in rows))
    patch_ready = sum(1 for row in rows if row.patch_readiness == "ready")
    priority = min(
        len(rows),
        sum(1 for row in rows if row.save_gap_status != "exact-field-width-match")
        + sum(1 for row in rows if row.probable_source_field == "active control header")
        + sum(1 for row in rows if row.probable_source_field == "item->room_number" and row.save_gap_status == "source-layout-mismatch"),
    )
    status = "restore-side-supported" if patch_ready and patch_ready == len(rows) else "restore-side-proof-missing"
    return RestoreSideAudit(
        source=_relative_to_repo(source, repo),
        field_width_csv=_relative_to_repo(field_width_csv, repo),
        restore_function_status=restore_status,
        total_hypotheses=len(rows),
        priority_hypotheses=priority,
        patch_ready_count=patch_ready,
        restore_status_counts=counts,
        rows=tuple(rows),
        status=status,
    )


def write_csv(audit: RestoreSideAudit, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "original_group", "call_ordinal", "call_index", "call_address", "original_size",
        "probable_source_field", "save_gap_status", "restore_side_status", "patch_readiness", "next_action",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in audit.rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def write_markdown(audit: RestoreSideAudit, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# SaveLevelData restore-side field proof audit",
        "",
        "Status: Generated",
        "Story: `docs/stories/RE-018-saveleveldata-restore-side-field-proof.md`",
        "",
        "## Progress tracker",
        "",
        "- [x] Load RE-017 field/width hypotheses.",
        "- [x] Inspect current source RestoreLevelData implementation status.",
        "- [x] Classify each hypothesis against restore-side proof availability.",
        "- [x] Keep outputs metadata-only.",
        "- [x] Preserve marker verdict limits.",
        "",
        "## Inputs",
        "",
        f"- Source: `{audit.source}`",
        f"- RE-017 field-width CSV: `{audit.field_width_csv}`",
        "",
        "## Summary",
        "",
        f"- RestoreLevelData source status: `{audit.restore_function_status}`",
        f"- hypotheses audited: `{audit.total_hypotheses}`",
        f"- priority hypotheses: `{audit.priority_hypotheses}`",
        f"- patch-ready hypotheses: `{audit.patch_ready_count}`",
        f"- status: `{audit.status}`",
        "",
        "### Restore-side status counts",
        "",
    ]
    for status, count in sorted(audit.restore_status_counts.items()):
        lines.append(f"- `{status}`: `{count}`")
    lines.extend([
        "",
        "## Findings",
        "",
        "Current source `RestoreLevelData` is unimplemented, so RE-017 hypotheses cannot be promoted to serializer patches from source evidence alone. Byte/word, layout, separate payload, and object-specific block hypotheses all require restore-side proof first.",
        "",
        "## Hypothesis matrix",
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
            f"  - RE-017 save gap status: `{row.save_gap_status}`",
            f"  - restore-side status: `{row.restore_side_status}`",
            f"  - patch readiness: `{row.patch_readiness}`",
            f"  - next action: {row.next_action}",
        ])
    lines.extend([
        "",
        "## Verdict",
        "",
        "RE-018 blocks serializer patching from RE-017 alone: current source `RestoreLevelData` is unimplemented and no restore-side source read sequence can support the field/width hypotheses yet. Do not add `(F)`, `(D)`, or `(**)` markers.",
        "",
        "Next step: extract or reconstruct a metadata-only original `RestoreLevelData` read-call map, then compare restore read sizes/order against the RE-017 hypotheses before patching source serialization.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="TOMB5 repo root")
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="source file relative to repo")
    parser.add_argument("--field-width-csv", default=DEFAULT_FIELD_WIDTH_CSV, help="RE-017 CSV relative to repo")
    parser.add_argument("--csv", default=DEFAULT_OUT_CSV, help="versionable CSV output relative to repo")
    parser.add_argument("--md", default=DEFAULT_OUT_MD, help="versionable Markdown output relative to repo")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    audit = build_restore_side_audit(repo, repo / args.source, repo / args.field_width_csv)
    csv_path = repo / args.csv
    md_path = repo / args.md
    write_csv(audit, csv_path)
    write_markdown(audit, md_path)
    print(f"restore_function_status={audit.restore_function_status}")
    print(f"hypotheses={audit.total_hypotheses}")
    print(f"patch_ready={audit.patch_ready_count}")
    print(f"status={audit.status}")
    print(f"csv={csv_path}")
    print(f"md={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
