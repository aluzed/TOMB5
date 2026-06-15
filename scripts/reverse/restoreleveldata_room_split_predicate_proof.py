#!/usr/bin/env python3
"""Build a metadata-only RestoreLevelData room/split predicate proof matrix.

RE-024 narrows the RE-023 proof-first plan to the two groups assigned to RE-024:
save group 10 (room/layout window) and save group 4 (active item split). It does
not read original dumps and does not make source patch readiness claims.
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
DEFAULT_OUT_CSV = "docs/reverse/generated/restoreleveldata-room-split-predicate-proof.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/restoreleveldata-room-split-predicate-proof.md"
TARGET_GROUPS = (10, 4)


@dataclass(frozen=True)
class RoomSplitPredicateProofRow:
    save_original_group: int
    restore_groups: str
    proof_focus: str
    field_width_profile: str
    restore_shape: str
    branch_profile: str
    blocking_predicates: str
    source_safe_hypothesis: str
    proof_verdict: str
    next_action: str
    code_change_readiness: str
    recommended_next_ticket: str


@dataclass(frozen=True)
class RestoreLevelDataRoomSplitPredicateProof:
    implementation_plan_csv: Path
    reconciliation_csv: Path
    field_width_csv: Path
    control_flow_csv: Path
    branch_predicate_csv: Path
    target_save_groups: tuple[int, ...]
    rows: tuple[RoomSplitPredicateProofRow, ...]
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
            group = int(row[group_field])
            rows[group] = row
    return rows


def _field_width_profiles(path: Path) -> dict[int, str]:
    grouped: dict[int, Counter[str]] = {group: Counter() for group in TARGET_GROUPS}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            group = int(row["original_group"])
            if group in grouped:
                grouped[group][row.get("gap_status", "unknown")] += 1
    order = (
        "exact-field-width-match",
        "source-width-mismatch",
        "source-layout-mismatch",
        "source-missing-field",
        "branch-boundary-or-sentinel",
        "needs-manual-field-proof",
    )
    return {
        group: ";".join(f"{status}={counts[status]}" for status in order if counts.get(status)) or "none"
        for group, counts in grouped.items()
    }


def _branch_profile(branch_rows: dict[int, dict[str, str]], restore_groups: str) -> str:
    parts: list[str] = []
    if not restore_groups or restore_groups == "none":
        return "none"
    for text_group in restore_groups.split(";"):
        if not text_group:
            continue
        branch = branch_rows.get(int(text_group))
        if branch is None:
            continue
        parts.append(
            f"restore_group={text_group}:"
            f"{branch.get('predicate_hypothesis', 'unknown')}/"
            f"{branch.get('proof_status', 'unknown')}/"
            f"branch_total={branch.get('branch_total', 'unknown')}"
        )
    return "; ".join(parts) if parts else "none"


def _profile(group: int, plan_row: dict[str, str], reconciliation_row: dict[str, str], control_row: dict[str, str]) -> tuple[str, str, str, str, str, str]:
    if group == 10:
        return (
            "room-layout-window",
            reconciliation_row.get("unresolved_predicates", "room byte order/layout predicate"),
            "room byte is source-visible but its restore placement/order is still not predicate proof",
            "room-layout-predicate-unproven",
            "model room byte placement and optional rotation predicate before source patch",
            "RE-025",
        )
    if group == 4:
        return (
            "active-item-split-predicate",
            reconciliation_row.get("unresolved_predicates", "active item split predicate"),
            "active item fields are source-visible but split restore regions and anim-state width differences remain unproved",
            "split-predicate-and-anim-width-unproven",
            "derive split active-item predicate checklist and anim-state width decision",
            "RE-025",
        )
    raise ValueError(f"unsupported group {group}")


def build_restoreleveldata_room_split_predicate_proof(
    repo: Path,
    implementation_plan_csv: Path,
    reconciliation_csv: Path,
    field_width_csv: Path,
    control_flow_csv: Path,
    branch_predicate_csv: Path,
) -> RestoreLevelDataRoomSplitPredicateProof:
    plan_rows = _rows_by_group(implementation_plan_csv, "save_original_group")
    reconciliation_rows = _rows_by_group(reconciliation_csv, "save_original_group")
    control_rows = _rows_by_group(control_flow_csv, "save_original_group")
    branch_rows = _rows_by_group(branch_predicate_csv, "restore_group")
    width_profiles = _field_width_profiles(field_width_csv)

    rows: list[RoomSplitPredicateProofRow] = []
    for group in TARGET_GROUPS:
        plan_row = plan_rows[group]
        reconciliation_row = reconciliation_rows[group]
        control_row = control_rows[group]
        proof_focus, blockers, source_hypothesis, verdict, next_action, next_ticket = _profile(
            group, plan_row, reconciliation_row, control_row
        )
        restore_groups = reconciliation_row.get("restore_groups", "none")
        rows.append(RoomSplitPredicateProofRow(
            save_original_group=group,
            restore_groups=restore_groups,
            proof_focus=proof_focus,
            field_width_profile=width_profiles[group],
            restore_shape=control_row.get("proof_status", "unknown"),
            branch_profile=_branch_profile(branch_rows, restore_groups),
            blocking_predicates=blockers,
            source_safe_hypothesis=source_hypothesis,
            proof_verdict=verdict,
            next_action=next_action,
            code_change_readiness="blocked",
            recommended_next_ticket=next_ticket,
        ))

    code_ready = sum(1 for row in rows if row.code_change_readiness == "ready")
    return RestoreLevelDataRoomSplitPredicateProof(
        implementation_plan_csv=_relative_to_repo(implementation_plan_csv, repo),
        reconciliation_csv=_relative_to_repo(reconciliation_csv, repo),
        field_width_csv=_relative_to_repo(field_width_csv, repo),
        control_flow_csv=_relative_to_repo(control_flow_csv, repo),
        branch_predicate_csv=_relative_to_repo(branch_predicate_csv, repo),
        target_save_groups=tuple(row.save_original_group for row in rows),
        rows=tuple(rows),
        code_change_ready_count=code_ready,
        status="restoreleveldata-room-split-proof-partial" if rows else "restoreleveldata-room-split-proof-missing",
    )


def write_csv(proof: RestoreLevelDataRoomSplitPredicateProof, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "save_original_group",
        "restore_groups",
        "proof_focus",
        "field_width_profile",
        "restore_shape",
        "branch_profile",
        "blocking_predicates",
        "source_safe_hypothesis",
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


def write_markdown(proof: RestoreLevelDataRoomSplitPredicateProof, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RestoreLevelData room/split predicate proof",
        "",
        "Status: Generated",
        "Story: `docs/stories/RE-024-restoreleveldata-room-split-predicate-proof.md`",
        "",
        "## Progress tracker",
        "",
        "- [x] Load RE-023 implementation plan metadata.",
        "- [x] Load RE-022 field/predicate blockers.",
        "- [x] Load field-width, restore control-flow, and branch predicate summaries.",
        "- [x] Build proof rows for save groups `10` and `4`.",
        "- [x] Keep code-change readiness blocked until predicates are proved more strongly.",
        "- [x] Keep raw opcode text, machine words, payload coordinates, addresses, and branch/call targets out of versioned outputs.",
        "",
        "## Inputs",
        "",
        f"- RE-023 plan CSV: `{proof.implementation_plan_csv}`",
        f"- RE-022 reconciliation CSV: `{proof.reconciliation_csv}`",
        f"- RE-017 field-width CSV: `{proof.field_width_csv}`",
        f"- RE-020 control-flow CSV: `{proof.control_flow_csv}`",
        f"- RE-021 branch predicate CSV: `{proof.branch_predicate_csv}`",
        "",
        "## Summary",
        "",
        f"- target save groups: `{', '.join(str(g) for g in proof.target_save_groups)}`",
        f"- proof rows: `{len(proof.rows)}`",
        f"- code-change-ready groups: `{proof.code_change_ready_count}`",
        f"- status: `{proof.status}`",
        "",
        "## Proof matrix",
    ]
    for row in proof.rows:
        lines.extend([
            "",
            f"### Save group {row.save_original_group}",
            "",
            f"- restore groups: `{row.restore_groups}`",
            f"- proof focus: `{row.proof_focus}`",
            f"- field-width profile: `{row.field_width_profile}`",
            f"- restore shape: `{row.restore_shape}`",
            f"- branch profile: `{row.branch_profile}`",
            f"- blocking predicates: `{row.blocking_predicates}`",
            f"- source-safe hypothesis: `{row.source_safe_hypothesis}`",
            f"- proof verdict: `{row.proof_verdict}`",
            f"- next action: `{row.next_action}`",
            f"- code change readiness: `{row.code_change_readiness}`",
            f"- recommended next ticket: `{row.recommended_next_ticket}`",
        ])
    lines.extend([
        "",
        "## Verdict",
        "",
        "RE-024 narrows the proof work but still does not make any restore group safe to implement in source.",
        "",
        "Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.",
        "",
        "Recommended next ticket: RE-025 — prove the payload predicates for save group `5` while keeping the group `10` and group `4` predicate blockers visible.",
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
    parser.add_argument("--out-csv", default=DEFAULT_OUT_CSV)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    args = parser.parse_args(argv)

    proof = build_restoreleveldata_room_split_predicate_proof(
        repo=ROOT,
        implementation_plan_csv=ROOT / args.implementation_plan_csv,
        reconciliation_csv=ROOT / args.reconciliation_csv,
        field_width_csv=ROOT / args.field_width_csv,
        control_flow_csv=ROOT / args.control_flow_csv,
        branch_predicate_csv=ROOT / args.branch_predicate_csv,
    )
    write_csv(proof, ROOT / args.out_csv)
    write_markdown(proof, ROOT / args.out_md)
    print(f"wrote {args.out_csv} and {args.out_md}: {proof.status}; code-change-ready={proof.code_change_ready_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
