#!/usr/bin/env python3
"""Build a metadata-only RestoreLevelData save-group-8 layout/fanout proof.

RE-026 narrows the proof-first plan to save group 8: subtype/extra restore bytes,
20-byte layout block, room/rotation ordering, item data word, item flag payloads,
and source-visible speed/fallspeed/anim-state fields that still sit inside an
unproved object subtype fanout. It consumes only versioned metadata summaries and
keeps raw original dump details out of generated outputs.
"""

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

DEFAULT_IMPLEMENTATION_PLAN_CSV = "docs/reverse/generated/restoreleveldata-implementation-plan.csv"
DEFAULT_RECONCILIATION_CSV = "docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv"
DEFAULT_FIELD_WIDTH_CSV = "docs/reverse/generated/saveleveldata-item-field-width-audit.csv"
DEFAULT_CONTROL_FLOW_CSV = "docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv"
DEFAULT_BRANCH_PREDICATE_CSV = "docs/reverse/generated/restoreleveldata-branch-predicate-map.csv"
DEFAULT_GROUP5_PAYLOAD_CSV = "docs/reverse/generated/restoreleveldata-group5-payload-predicate-proof.csv"
DEFAULT_OUT_CSV = "docs/reverse/generated/restoreleveldata-group8-layout-fanout-proof.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/restoreleveldata-group8-layout-fanout-proof.md"
TARGET_SAVE_GROUP = 8


@dataclass(frozen=True)
class Group8LayoutFanoutProofRow:
    save_original_group: int
    restore_group: str
    fanout_family: str
    save_payload_profile: str
    restore_layout_profile: str
    source_predicate_profile: str
    branch_profile: str
    prior_group5_dependency: str
    blocking_predicates: str
    proof_verdict: str
    next_action: str
    code_change_readiness: str
    recommended_next_ticket: str


@dataclass(frozen=True)
class RestoreLevelDataGroup8LayoutFanoutProof:
    implementation_plan_csv: Path
    reconciliation_csv: Path
    field_width_csv: Path
    control_flow_csv: Path
    branch_predicate_csv: Path
    group5_payload_csv: Path
    target_save_group: int
    restore_group: str
    rows: tuple[Group8LayoutFanoutProofRow, ...]
    fanout_rows: int
    code_change_ready_count: int
    status: str


def _relative_to_repo(path: Path, repo: Path) -> Path:
    try:
        return path.resolve().relative_to(repo.resolve())
    except ValueError:
        return path


def _rows_by_group(path: Path, group_field: str) -> dict[int, dict[str, str]]:
    rows: dict[int, dict[str, str]] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows[int(row[group_field])] = row
    return rows


def _group8_field_rows(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if int(row["original_group"]) == TARGET_SAVE_GROUP:
                rows.append(row)
    return rows


def _bytes(rows: list[dict[str, str]]) -> int:
    return sum(int(row["original_size"]) for row in rows)


def _profile(rows: list[dict[str, str]]) -> str:
    counts = Counter(row.get("gap_status", "unknown") for row in rows)
    order = ("exact-field-width-match", "source-layout-mismatch", "source-missing-field")
    status_text = ";".join(f"{status}={counts[status]}" for status in order if counts.get(status)) or "none"
    return f"{status_text};bytes={_bytes(rows)}"


def _select(rows: list[dict[str, str]], predicate) -> list[dict[str, str]]:
    return [row for row in rows if predicate(row.get("probable_source_field", ""))]


def _branch_profile(branch_row: dict[str, str]) -> str:
    return (
        f"restore_group={branch_row.get('restore_group', 'unknown')}:"
        f"{branch_row.get('predicate_hypothesis', 'unknown')}/"
        f"{branch_row.get('proof_status', 'unknown')}/"
        f"branch_total={branch_row.get('branch_total', 'unknown')}"
    )


def _restore_layout_profile(control_row: dict[str, str]) -> str:
    sequence = control_row.get("restore_size_sequences", "unknown").replace("restore_group=8:", "")
    return (
        f"{control_row.get('proof_status', 'unknown')};"
        f"restore-size-sequence={sequence};"
        "extra-restore-byte-candidate=1"
    )


def _group5_dependency(group5_payload_csv: Path) -> str:
    if not group5_payload_csv.exists():
        return "group5-payload-proof-missing"
    with group5_payload_csv.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    item_flag_rows = [row for row in rows if row.get("payload_family") == "item_flags[0..3]"]
    if item_flag_rows and item_flag_rows[0].get("code_change_readiness") == "blocked":
        return "group5-item-flag-payloads-blocked"
    return "group5-item-flag-payloads-not-blocking"


def _build_rows(
    field_rows: list[dict[str, str]],
    control_row: dict[str, str],
    branch_row: dict[str, str],
    reconciliation_row: dict[str, str],
    group5_dependency: str,
) -> tuple[Group8LayoutFanoutProofRow, ...]:
    restore_group = reconciliation_row.get("restore_groups", "8")
    branch_profile = _branch_profile(branch_row)
    restore_profile = _restore_layout_profile(control_row)

    subtype = _select(field_rows, lambda field: "subtype" in field)
    position_block = _select(field_rows, lambda field: "position vector/block" in field)
    room_rotation = _select(field_rows, lambda field: "room/rotation" in field)
    speed_fallspeed = _select(field_rows, lambda field: field in {"item->speed", "item->fallspeed"})
    item_data = _select(field_rows, lambda field: "item data pointer/word" in field)
    item_flags = _select(field_rows, lambda field: "item->item_flags" in field)
    anim_state = _select(field_rows, lambda field: "anim_state" in field)

    specs = [
        (
            "subtype-extra-byte",
            _profile(subtype),
            "no current source predicate for subtype byte or the extra restore byte candidate",
            "subtype byte plus extra restore byte candidate are branch/fanout clues, not source field identity",
            "subtype-and-extra-byte-predicate-unproven",
            "prove subtype dispatch and explain the extra restore byte as source field or rebuilt state before patching",
            "none",
        ),
        (
            "position-layout-block",
            _profile(position_block),
            "current source uses split position writes, not a proved twenty-byte block",
            "twenty-byte layout block conflicts with current split position representation",
            "layout-block-predicate-unproven",
            "split the twenty-byte block into source fields or prove it is an object-specific payload body",
            "none",
        ),
        (
            "room-rotation-ordering",
            _profile(room_rotation),
            "current source room byte and rotation ordering does not match this compact payload shape",
            "room/rotation payload ordering remains unresolved inside the fanout branch",
            "room-rotation-ordering-unproven",
            "prove room/rotation field order for this subtype branch before source edits",
            "none",
        ),
        (
            "speed-fallspeed",
            _profile(speed_fallspeed),
            "speed and fallspeed widths are source-visible",
            "field widths match but subtype fanout and surrounding layout are still not predicate proof",
            "field-width-match-fanout-still-blocked",
            "keep as matched subfields while proving the enclosing fanout/layout predicate",
            "none",
        ),
        (
            "item-data-word",
            _profile(item_data),
            "no current source predicate for item data pointer/word payload",
            "item data pointer/word payload has no source field identity",
            "item-data-pointer-predicate-unproven",
            "identify the item data word as a concrete source field or non-source rebuilt state",
            "none",
        ),
        (
            "item_flags[3,0,1]",
            _profile(item_flags),
            "item flag payload bodies remain absent from current source",
            "group 8 repeats item flag payload blockers already visible in group 5",
            "item-flag-payload-predicate-unproven",
            "reuse the group 5 item-flag payload proof blocker before attempting group 8 source edits",
            group5_dependency,
        ),
        (
            "anim-state-payload",
            _profile(anim_state),
            "anim-state widths are source-visible in this branch",
            "field widths match but branch fanout/layout identity remains unresolved",
            "field-width-match-fanout-still-blocked",
            "keep anim-state fields as matched subfields while proving the enclosing object subtype fanout",
            "none",
        ),
    ]

    return tuple(
        Group8LayoutFanoutProofRow(
            save_original_group=TARGET_SAVE_GROUP,
            restore_group=restore_group,
            fanout_family=family,
            save_payload_profile=save_profile,
            restore_layout_profile=restore_profile,
            source_predicate_profile=source_profile,
            branch_profile=branch_profile,
            prior_group5_dependency=dependency,
            blocking_predicates=blocker,
            proof_verdict=verdict,
            next_action=next_action,
            code_change_readiness="blocked",
            recommended_next_ticket="RE-027",
        )
        for family, save_profile, source_profile, blocker, verdict, next_action, dependency in specs
    )


def build_restoreleveldata_group8_layout_fanout_proof(
    repo: Path,
    implementation_plan_csv: Path,
    reconciliation_csv: Path,
    field_width_csv: Path,
    control_flow_csv: Path,
    branch_predicate_csv: Path,
    group5_payload_csv: Path,
) -> RestoreLevelDataGroup8LayoutFanoutProof:
    _rows_by_group(implementation_plan_csv, "save_original_group")[TARGET_SAVE_GROUP]
    reconciliation_row = _rows_by_group(reconciliation_csv, "save_original_group")[TARGET_SAVE_GROUP]
    control_row = _rows_by_group(control_flow_csv, "save_original_group")[TARGET_SAVE_GROUP]
    branch_row = _rows_by_group(branch_predicate_csv, "restore_group")[8]
    field_rows = _group8_field_rows(field_width_csv)
    rows = _build_rows(
        field_rows=field_rows,
        control_row=control_row,
        branch_row=branch_row,
        reconciliation_row=reconciliation_row,
        group5_dependency=_group5_dependency(group5_payload_csv),
    )
    code_ready = sum(1 for row in rows if row.code_change_readiness == "ready")

    return RestoreLevelDataGroup8LayoutFanoutProof(
        implementation_plan_csv=_relative_to_repo(implementation_plan_csv, repo),
        reconciliation_csv=_relative_to_repo(reconciliation_csv, repo),
        field_width_csv=_relative_to_repo(field_width_csv, repo),
        control_flow_csv=_relative_to_repo(control_flow_csv, repo),
        branch_predicate_csv=_relative_to_repo(branch_predicate_csv, repo),
        group5_payload_csv=_relative_to_repo(group5_payload_csv, repo),
        target_save_group=TARGET_SAVE_GROUP,
        restore_group=reconciliation_row.get("restore_groups", "8"),
        rows=rows,
        fanout_rows=len(rows),
        code_change_ready_count=code_ready,
        status="restoreleveldata-group8-layout-fanout-proof-blocked",
    )


def write_csv(proof: RestoreLevelDataGroup8LayoutFanoutProof, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "save_original_group",
        "restore_group",
        "fanout_family",
        "save_payload_profile",
        "restore_layout_profile",
        "source_predicate_profile",
        "branch_profile",
        "prior_group5_dependency",
        "blocking_predicates",
        "proof_verdict",
        "next_action",
        "code_change_readiness",
        "recommended_next_ticket",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in proof.rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def write_markdown(proof: RestoreLevelDataGroup8LayoutFanoutProof, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RestoreLevelData group 8 layout/fanout proof",
        "",
        "Status: Generated",
        "Story: `docs/stories/RE-026-restoreleveldata-group8-layout-fanout-proof.md`",
        "",
        "## Progress tracker",
        "",
        "- [x] Load RE-023 implementation plan metadata.",
        "- [x] Load RE-022 save group `8` field/predicate blockers.",
        "- [x] Load RE-017 field-width rows for subtype, layout block, room/rotation, item data, item flags, speed/fallspeed, and anim-state payloads.",
        "- [x] Load RE-020/RE-021 restore group `8` payload anchor and branch-fanout summaries.",
        "- [x] Carry forward the RE-025 group `5` item-flag payload dependency.",
        "- [x] Keep code-change readiness blocked and raw original details out of versioned outputs.",
        "",
        "## Inputs",
        "",
        f"- RE-023 plan CSV: `{proof.implementation_plan_csv}`",
        f"- RE-022 reconciliation CSV: `{proof.reconciliation_csv}`",
        f"- RE-017 field-width CSV: `{proof.field_width_csv}`",
        f"- RE-020 control-flow CSV: `{proof.control_flow_csv}`",
        f"- RE-021 branch predicate CSV: `{proof.branch_predicate_csv}`",
        f"- RE-025 group 5 payload CSV: `{proof.group5_payload_csv}`",
        "",
        "## Summary",
        "",
        f"- target save group: `{proof.target_save_group}`",
        f"- restore group: `{proof.restore_group}`",
        f"- fanout rows: `{proof.fanout_rows}`",
        f"- code-change-ready fanout families: `{proof.code_change_ready_count}`",
        f"- status: `{proof.status}`",
        "",
        "## Layout/fanout predicate matrix",
    ]
    for row in proof.rows:
        lines.extend([
            "",
            f"### {row.fanout_family}",
            "",
            f"- save original group: `{row.save_original_group}`",
            f"- restore group: `{row.restore_group}`",
            f"- save payload profile: `{row.save_payload_profile}`",
            f"- restore layout profile: `{row.restore_layout_profile}`",
            f"- source predicate profile: `{row.source_predicate_profile}`",
            f"- branch profile: `{row.branch_profile}`",
            f"- prior group 5 dependency: `{row.prior_group5_dependency}`",
            f"- blocking predicates: `{row.blocking_predicates}`",
            f"- proof verdict: `{row.proof_verdict}`",
            f"- next action: `{row.next_action}`",
            f"- code change readiness: `{row.code_change_readiness}`",
            f"- recommended next ticket: `{row.recommended_next_ticket}`",
        ])
    lines.extend([
        "",
        "## Verdict",
        "",
        "RE-026 shows that save group `8` contains some source-visible width matches, but the subtype byte, extra restore byte candidate, layout block, room/rotation ordering, item data word, and item-flag payload bodies remain unresolved inside an object subtype fanout.",
        "",
        "Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.",
        "",
        "Recommended next ticket: RE-027 — derive a source-level RestoreLevelData implementation readiness refresh from RE-024, RE-025, and RE-026, keeping all blocked predicates explicit before any source patch.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--implementation-plan-csv", default=DEFAULT_IMPLEMENTATION_PLAN_CSV)
    parser.add_argument("--reconciliation-csv", default=DEFAULT_RECONCILIATION_CSV)
    parser.add_argument("--field-width-csv", default=DEFAULT_FIELD_WIDTH_CSV)
    parser.add_argument("--control-flow-csv", default=DEFAULT_CONTROL_FLOW_CSV)
    parser.add_argument("--branch-predicate-csv", default=DEFAULT_BRANCH_PREDICATE_CSV)
    parser.add_argument("--group5-payload-csv", default=DEFAULT_GROUP5_PAYLOAD_CSV)
    parser.add_argument("--out-csv", default=DEFAULT_OUT_CSV)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    args = parser.parse_args(argv)

    proof = build_restoreleveldata_group8_layout_fanout_proof(
        repo=ROOT,
        implementation_plan_csv=ROOT / args.implementation_plan_csv,
        reconciliation_csv=ROOT / args.reconciliation_csv,
        field_width_csv=ROOT / args.field_width_csv,
        control_flow_csv=ROOT / args.control_flow_csv,
        branch_predicate_csv=ROOT / args.branch_predicate_csv,
        group5_payload_csv=ROOT / args.group5_payload_csv,
    )
    write_csv(proof, ROOT / args.out_csv)
    write_markdown(proof, ROOT / args.out_md)
    print(f"wrote {args.out_csv} and {args.out_md}: {proof.status}; code-change-ready={proof.code_change_ready_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
