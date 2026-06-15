#!/usr/bin/env python3
"""Build a metadata-only RestoreLevelData field/predicate reconciliation.

RE-022 consumes the already-versioned metadata from RE-017, RE-020, and RE-021.
It does not read original dumps. The output reconciles candidate restore branch
regions with source-side field identities and optional predicate families while
keeping patch readiness blocked until both field identity and predicates are
proved.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_FIELD_WIDTH_CSV = "docs/reverse/generated/saveleveldata-item-field-width-audit.csv"
DEFAULT_FIELD_CONTROL_FLOW_CSV = "docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv"
DEFAULT_BRANCH_PREDICATE_CSV = "docs/reverse/generated/restoreleveldata-branch-predicate-map.csv"
DEFAULT_OUT_CSV = "docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/restoreleveldata-field-predicate-reconciliation.md"
PRIORITY_GROUPS = (4, 5, 8, 10)
MATCH_STATUSES = {"exact-field-width-match"}
UNRESOLVED_STATUSES = {
    "source-width-mismatch",
    "source-missing-field",
    "source-layout-mismatch",
    "branch-boundary-or-sentinel",
    "needs-manual-field-proof",
}


@dataclass(frozen=True)
class FieldWidthRow:
    original_group: int
    probable_source_field: str
    gap_status: str


@dataclass(frozen=True)
class ControlFlowRow:
    save_original_group: int
    restore_group_candidates: str
    proof_status: str
    proof_limit: str


@dataclass(frozen=True)
class BranchRow:
    restore_group: int
    branch_summary: str
    predicate_hypothesis: str
    proof_status: str


@dataclass(frozen=True)
class FieldPredicateRow:
    save_original_group: int
    restore_groups: str
    branch_predicate_hypotheses: str
    branch_summary: str
    matched_field_count: int
    unresolved_field_count: int
    unresolved_gap_summary: str
    source_predicate_summary: str
    unresolved_predicates: str
    proof_status: str
    patch_readiness: str
    proof_limit: str


@dataclass(frozen=True)
class RestoreFieldPredicateReconciliation:
    field_width_csv: Path
    field_control_flow_csv: Path
    branch_predicate_csv: Path
    save_groups_covered: tuple[int, ...]
    rows: tuple[FieldPredicateRow, ...]
    patch_ready_count: int
    status: str


def _relative_to_repo(path: Path, repo: Path) -> Path:
    try:
        return path.resolve().relative_to(repo.resolve())
    except ValueError:
        return path


def _read_field_width_rows(path: Path) -> dict[int, tuple[FieldWidthRow, ...]]:
    grouped: dict[int, list[FieldWidthRow]] = defaultdict(list)
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            group = int(row["original_group"])
            if group not in PRIORITY_GROUPS:
                continue
            grouped[group].append(FieldWidthRow(
                original_group=group,
                probable_source_field=row.get("probable_source_field", ""),
                gap_status=row.get("gap_status", ""),
            ))
    return {group: tuple(grouped[group]) for group in PRIORITY_GROUPS if group in grouped}


def _read_control_flow_rows(path: Path) -> dict[int, ControlFlowRow]:
    rows: dict[int, ControlFlowRow] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            group = int(row["save_original_group"])
            if group not in PRIORITY_GROUPS:
                continue
            rows[group] = ControlFlowRow(
                save_original_group=group,
                restore_group_candidates=row.get("restore_group_candidates", "none"),
                proof_status=row.get("proof_status", ""),
                proof_limit=row.get("proof_limit", ""),
            )
    return rows


def _read_branch_rows(path: Path) -> dict[int, BranchRow]:
    rows: dict[int, BranchRow] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            group = int(row["restore_group"])
            rows[group] = BranchRow(
                restore_group=group,
                branch_summary=row.get("branch_summary", "none"),
                predicate_hypothesis=row.get("predicate_hypothesis", ""),
                proof_status=row.get("proof_status", ""),
            )
    return rows


def _split_restore_groups(text: str) -> tuple[int, ...]:
    if not text or text == "none":
        return ()
    return tuple(int(part) for part in text.split(";") if part.strip())


def _count_fields(rows: tuple[FieldWidthRow, ...]) -> tuple[int, int, str]:
    counts = Counter(row.gap_status for row in rows)
    matched = sum(counts[status] for status in MATCH_STATUSES)
    unresolved = sum(count for status, count in counts.items() if status in UNRESOLVED_STATUSES or status not in MATCH_STATUSES)
    parts = [
        f"{status}={counts[status]}"
        for status in (
            "source-width-mismatch",
            "source-missing-field",
            "source-layout-mismatch",
            "branch-boundary-or-sentinel",
            "needs-manual-field-proof",
        )
        if counts.get(status)
    ]
    return matched, unresolved, ";".join(parts) if parts else "none"


def _group_profile(group: int) -> tuple[str, str, str, str]:
    profiles = {
        4: (
            "obj->save_position;obj->save_anim;word-bit optional x_rot/z_rot/speed/fallspeed;lara anim variant;obj->save_hitpoints",
            "anim-state byte-vs-word restore predicate;split restore groups 4+5",
            "field-identity-partial-predicate-blocked",
            "Most position/rotation/speed/anim fields have width matches, but anim-state byte-vs-word differences and split restore branch predicates still block a safe source patch.",
        ),
        5: (
            "obj->save_flags;word-bit item_flags/timer/trigger_flags;object extension payload",
            "item_flags[0..3] payload;timer payload;trigger_flags payload;object-specific 24/20-byte payload blocks",
            "payload-predicate-missing",
            "Only the packed flags word is source-backed; separate flag/timer/trigger and object payload predicates remain missing on the source side.",
        ),
        8: (
            "object subtype/layout fanout;item_flags payload;anim-state payload;speed/fallspeed payload",
            "subtype byte;20-byte layout block;room/rotation ordering;item_flags payload predicates;extra restore bytes",
            "layout-and-predicate-mismatch",
            "Field identity is mixed: speed/fallspeed/anim states match, but extra restore bytes, layout blocks, and item_flags predicates remain unresolved.",
        ),
        10: (
            "position/rotation room layout window;optional x_rot predicate",
            "room byte order/layout predicate",
            "exact-window-field-partial",
            "The size window and most field widths match, but exact size does not prove the room byte order/layout predicate.",
        ),
    }
    return profiles[group]


def _branch_evidence(restore_groups: tuple[int, ...], branches: dict[int, BranchRow]) -> tuple[str, str]:
    hypotheses: list[str] = []
    summaries: list[str] = []
    for group in restore_groups:
        branch = branches.get(group)
        if branch is None:
            continue
        hypotheses.append(f"restore_group={group}:{branch.predicate_hypothesis}/{branch.proof_status}")
        summaries.append(f"restore_group={group}:{branch.branch_summary}")
    return "; ".join(hypotheses) if hypotheses else "none", "; ".join(summaries) if summaries else "none"


def build_restore_field_predicate_reconciliation(repo: Path, field_width_csv: Path, field_control_flow_csv: Path, branch_predicate_csv: Path) -> RestoreFieldPredicateReconciliation:
    field_rows = _read_field_width_rows(field_width_csv)
    control_rows = _read_control_flow_rows(field_control_flow_csv)
    branch_rows = _read_branch_rows(branch_predicate_csv)

    rows: list[FieldPredicateRow] = []
    for group in PRIORITY_GROUPS:
        fields = field_rows[group]
        control = control_rows[group]
        restore_groups = _split_restore_groups(control.restore_group_candidates)
        branch_hypotheses, branch_summary = _branch_evidence(restore_groups, branch_rows)
        matched, unresolved, gap_summary = _count_fields(fields)
        source_predicates, unresolved_predicates, proof_status, group_limit = _group_profile(group)
        proof_limit = f"{group_limit} RE-020 limit: {control.proof_limit}"
        rows.append(FieldPredicateRow(
            save_original_group=group,
            restore_groups=";".join(str(candidate) for candidate in restore_groups) or "none",
            branch_predicate_hypotheses=branch_hypotheses,
            branch_summary=branch_summary,
            matched_field_count=matched,
            unresolved_field_count=unresolved,
            unresolved_gap_summary=gap_summary,
            source_predicate_summary=source_predicates,
            unresolved_predicates=unresolved_predicates,
            proof_status=proof_status,
            patch_readiness="blocked",
            proof_limit=proof_limit,
        ))

    patch_ready_count = sum(1 for row in rows if row.patch_readiness == "ready")
    status = "restore-field-predicate-reconciliation-partial" if rows else "restore-field-predicate-reconciliation-missing"
    return RestoreFieldPredicateReconciliation(
        field_width_csv=_relative_to_repo(field_width_csv, repo),
        field_control_flow_csv=_relative_to_repo(field_control_flow_csv, repo),
        branch_predicate_csv=_relative_to_repo(branch_predicate_csv, repo),
        save_groups_covered=tuple(row.save_original_group for row in rows),
        rows=tuple(rows),
        patch_ready_count=patch_ready_count,
        status=status,
    )


def write_csv(reconciliation: RestoreFieldPredicateReconciliation, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "save_original_group", "restore_groups", "branch_predicate_hypotheses", "branch_summary",
        "matched_field_count", "unresolved_field_count", "unresolved_gap_summary",
        "source_predicate_summary", "unresolved_predicates", "proof_status",
        "patch_readiness", "proof_limit",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in reconciliation.rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def write_markdown(reconciliation: RestoreFieldPredicateReconciliation, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RestoreLevelData field/predicate reconciliation",
        "",
        "Status: Generated",
        "Story: `docs/stories/RE-022-restoreleveldata-field-predicate-reconciliation.md`",
        "",
        "## Progress tracker",
        "",
        "- [x] Load RE-017 source/original field-width metadata.",
        "- [x] Load RE-020 restore candidate field/control-flow links.",
        "- [x] Load RE-021 branch/predicate hypotheses.",
        "- [x] Reconcile matched versus unresolved field counts per priority save group.",
        "- [x] Record source predicate families and unresolved predicate blockers.",
        "- [x] Keep raw opcode text, machine words, payload coordinates, addresses, and branch/call targets out of versioned outputs.",
        "- [x] Preserve marker verdict limits.",
        "",
        "## Inputs",
        "",
        f"- RE-017 field-width CSV: `{reconciliation.field_width_csv}`",
        f"- RE-020 field/control-flow CSV: `{reconciliation.field_control_flow_csv}`",
        f"- RE-021 branch/predicate CSV: `{reconciliation.branch_predicate_csv}`",
        "",
        "## Summary",
        "",
        f"- save groups covered: `{', '.join(str(g) for g in reconciliation.save_groups_covered)}`",
        f"- proof rows: `{len(reconciliation.rows)}`",
        f"- patch-ready groups: `{reconciliation.patch_ready_count}`",
        f"- status: `{reconciliation.status}`",
        "",
        "## Field/predicate matrix",
    ]
    for row in reconciliation.rows:
        lines.extend([
            "",
            f"### Save group {row.save_original_group}",
            "",
            f"- restore groups: `{row.restore_groups}`",
            f"- branch predicate hypotheses: `{row.branch_predicate_hypotheses}`",
            f"- branch summary: `{row.branch_summary}`",
            f"- matched field count: `{row.matched_field_count}`",
            f"- unresolved field count: `{row.unresolved_field_count}`",
            f"- unresolved gap summary: `{row.unresolved_gap_summary}`",
            f"- source predicate summary: `{row.source_predicate_summary}`",
            f"- unresolved predicates: `{row.unresolved_predicates}`",
            f"- proof status: `{row.proof_status}`",
            f"- patch readiness: `{row.patch_readiness}`",
            f"- proof limit: {row.proof_limit}",
        ])
    lines.extend([
        "",
        "## Verdict",
        "",
        "RE-022 makes the blockers more actionable, but it still does not prove exact restore-side field predicates. Patch readiness remains `0`.",
        "",
        "Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.",
        "",
        "Next step: build a restore implementation plan only after the missing payload predicates and layout blockers have source-level proof.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-width-csv", default=DEFAULT_FIELD_WIDTH_CSV)
    parser.add_argument("--field-control-flow-csv", default=DEFAULT_FIELD_CONTROL_FLOW_CSV)
    parser.add_argument("--branch-predicate-csv", default=DEFAULT_BRANCH_PREDICATE_CSV)
    parser.add_argument("--out-csv", default=DEFAULT_OUT_CSV)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    args = parser.parse_args(argv)

    reconciliation = build_restore_field_predicate_reconciliation(
        repo=ROOT,
        field_width_csv=ROOT / args.field_width_csv,
        field_control_flow_csv=ROOT / args.field_control_flow_csv,
        branch_predicate_csv=ROOT / args.branch_predicate_csv,
    )
    write_csv(reconciliation, ROOT / args.out_csv)
    write_markdown(reconciliation, ROOT / args.out_md)
    print(f"wrote {args.out_csv} and {args.out_md}: {reconciliation.status}; patch-ready={reconciliation.patch_ready_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
