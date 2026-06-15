#!/usr/bin/env python3
"""Build a metadata-only RestoreLevelData save-group-5 payload predicate proof.

RE-025 narrows the RE-023/RE-024 proof-first plan to save group 5: packed
status flags, item flag payloads, timer, trigger flags, and object extension
payload anchors. It consumes only versioned metadata summaries and does not read
or publish raw original dumps, opcodes, machine words, payload coordinates, or
raw branch/call targets.
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
DEFAULT_OUT_CSV = "docs/reverse/generated/restoreleveldata-group5-payload-predicate-proof.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/restoreleveldata-group5-payload-predicate-proof.md"
TARGET_SAVE_GROUP = 5


@dataclass(frozen=True)
class Group5PayloadPredicateProofRow:
    save_original_group: int
    restore_group: str
    payload_family: str
    save_payload_profile: str
    restore_payload_profile: str
    source_predicate_profile: str
    branch_profile: str
    blocking_predicates: str
    proof_verdict: str
    next_action: str
    code_change_readiness: str
    recommended_next_ticket: str


@dataclass(frozen=True)
class RestoreLevelDataGroup5PayloadPredicateProof:
    implementation_plan_csv: Path
    reconciliation_csv: Path
    field_width_csv: Path
    control_flow_csv: Path
    branch_predicate_csv: Path
    target_save_group: int
    restore_group: str
    rows: tuple[Group5PayloadPredicateProofRow, ...]
    payload_rows: int
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


def _group5_field_rows(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if int(row["original_group"]) == TARGET_SAVE_GROUP:
                rows.append(row)
    return rows


def _bytes(rows: list[dict[str, str]]) -> int:
    return sum(int(row["original_size"]) for row in rows)


def _profile(rows: list[dict[str, str]]) -> str:
    statuses = Counter(row.get("gap_status", "unknown") for row in rows)
    status_text = ";".join(f"{status}={count}" for status, count in sorted(statuses.items()))
    return f"{status_text};bytes={_bytes(rows)}"


def _branch_profile(branch_row: dict[str, str]) -> str:
    return (
        f"restore_group={branch_row.get('restore_group', 'unknown')}:"
        f"{branch_row.get('predicate_hypothesis', 'unknown')}/"
        f"{branch_row.get('proof_status', 'unknown')}/"
        f"branch_total={branch_row.get('branch_total', 'unknown')}"
    )


def _select(rows: list[dict[str, str]], needle: str) -> list[dict[str, str]]:
    return [row for row in rows if needle in row.get("probable_source_field", "")]


def _build_rows(
    field_rows: list[dict[str, str]],
    control_row: dict[str, str],
    branch_row: dict[str, str],
    reconciliation_row: dict[str, str],
) -> tuple[Group5PayloadPredicateProofRow, ...]:
    restore_group = reconciliation_row.get("restore_groups", "6")
    branch_profile = _branch_profile(branch_row)
    restore_profile = (
        f"{control_row.get('proof_status', 'unknown')};"
        f"restore-size-sequence={control_row.get('restore_size_sequences', 'unknown').replace('restore_group=6:', '')}"
    )

    packed = _select(field_rows, "packed active/status flags")
    item_flags = _select(field_rows, "item->item_flags")
    timer = _select(field_rows, "timer payload")
    trigger = _select(field_rows, "trigger_flags payload")
    object_extension = [
        row for row in field_rows
        if row.get("probable_source_field", "").startswith("object-specific")
    ]

    row_specs = [
        (
            "packed-status-flags",
            f"{_profile(packed)}" if packed else "none",
            "obj->save_flags guarded packed status word",
            "packed status word exists, but it is only an anchor for this payload cluster",
            "source-backed-anchor-only",
            "keep packed status word as the group anchor and prove following payload predicates separately",
            "RE-026",
        ),
        (
            "item_flags[0..3]",
            _profile(item_flags),
            "header-bit predicates visible; separate payload writes absent",
            "item flag header bits do not prove the four item flag payload words or restore body order",
            "payload-body-predicate-unproven",
            "derive source-backed predicates and restore reads for four item flag payload words",
            "RE-026",
        ),
        (
            "timer",
            _profile(timer),
            "header-bit predicate visible; separate timer payload write absent",
            "timer header bit does not prove a separate timer payload body or restore assignment",
            "payload-body-predicate-unproven",
            "derive a source-backed timer payload predicate and restore assignment before serializer edits",
            "RE-026",
        ),
        (
            "trigger_flags",
            _profile(trigger),
            "header-bit predicate visible; separate trigger_flags payload write absent",
            "trigger_flags header bit does not prove a separate trigger_flags payload body or restore assignment",
            "payload-body-predicate-unproven",
            "derive a source-backed trigger_flags payload predicate and restore assignment before serializer edits",
            "RE-026",
        ),
        (
            "object-extension",
            f"{_profile(object_extension)};rare-blocks={control_row.get('rare_payload_anchors', 'none')}",
            "no current source predicate for object-specific short and block payloads",
            "object-specific short and block payloads lack source field identity and object predicate mapping",
            "object-extension-predicate-unproven",
            "map object-specific short, twenty-four-byte, and twenty-byte payload predicates before any source patch",
            "RE-026",
        ),
    ]

    return tuple(
        Group5PayloadPredicateProofRow(
            save_original_group=TARGET_SAVE_GROUP,
            restore_group=restore_group,
            payload_family=family,
            save_payload_profile=save_profile,
            restore_payload_profile=restore_profile,
            source_predicate_profile=source_profile,
            branch_profile=branch_profile,
            blocking_predicates=blocking,
            proof_verdict=verdict,
            next_action=next_action,
            code_change_readiness="blocked",
            recommended_next_ticket=next_ticket,
        )
        for family, save_profile, source_profile, blocking, verdict, next_action, next_ticket in row_specs
    )


def build_restoreleveldata_group5_payload_predicate_proof(
    repo: Path,
    implementation_plan_csv: Path,
    reconciliation_csv: Path,
    field_width_csv: Path,
    control_flow_csv: Path,
    branch_predicate_csv: Path,
) -> RestoreLevelDataGroup5PayloadPredicateProof:
    plan_rows = _rows_by_group(implementation_plan_csv, "save_original_group")
    reconciliation_rows = _rows_by_group(reconciliation_csv, "save_original_group")
    control_rows = _rows_by_group(control_flow_csv, "save_original_group")
    branch_rows = _rows_by_group(branch_predicate_csv, "restore_group")
    field_rows = _group5_field_rows(field_width_csv)

    plan_row = plan_rows[TARGET_SAVE_GROUP]
    reconciliation_row = reconciliation_rows[TARGET_SAVE_GROUP]
    control_row = control_rows[TARGET_SAVE_GROUP]
    restore_group = reconciliation_row.get("restore_groups", plan_row.get("restore_groups", "6"))
    branch_row = branch_rows[int(restore_group)]
    rows = _build_rows(field_rows, control_row, branch_row, reconciliation_row)
    code_ready = sum(1 for row in rows if row.code_change_readiness == "ready")

    return RestoreLevelDataGroup5PayloadPredicateProof(
        implementation_plan_csv=_relative_to_repo(implementation_plan_csv, repo),
        reconciliation_csv=_relative_to_repo(reconciliation_csv, repo),
        field_width_csv=_relative_to_repo(field_width_csv, repo),
        control_flow_csv=_relative_to_repo(control_flow_csv, repo),
        branch_predicate_csv=_relative_to_repo(branch_predicate_csv, repo),
        target_save_group=TARGET_SAVE_GROUP,
        restore_group=restore_group,
        rows=rows,
        payload_rows=len(rows),
        code_change_ready_count=code_ready,
        status="restoreleveldata-group5-payload-proof-blocked",
    )


def write_csv(proof: RestoreLevelDataGroup5PayloadPredicateProof, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "save_original_group",
        "restore_group",
        "payload_family",
        "save_payload_profile",
        "restore_payload_profile",
        "source_predicate_profile",
        "branch_profile",
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


def write_markdown(proof: RestoreLevelDataGroup5PayloadPredicateProof, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RestoreLevelData group 5 payload predicate proof",
        "",
        "Status: Generated",
        "Story: `docs/stories/RE-025-restoreleveldata-group5-payload-predicate-proof.md`",
        "",
        "## Progress tracker",
        "",
        "- [x] Load RE-023 implementation plan metadata.",
        "- [x] Load RE-022 save group `5` field/predicate blockers.",
        "- [x] Load RE-017 field-width rows for packed flags, item flags, timer, trigger flags, and object payload blocks.",
        "- [x] Load RE-020/RE-021 restore group `6` payload anchor and branch summaries.",
        "- [x] Build payload-family proof rows while keeping code-change readiness blocked.",
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
        f"- target save group: `{proof.target_save_group}`",
        f"- restore group: `{proof.restore_group}`",
        f"- payload rows: `{proof.payload_rows}`",
        f"- code-change-ready payload families: `{proof.code_change_ready_count}`",
        f"- status: `{proof.status}`",
        "",
        "## Payload predicate matrix",
    ]
    for row in proof.rows:
        lines.extend([
            "",
            f"### {row.payload_family}",
            "",
            f"- save original group: `{row.save_original_group}`",
            f"- restore group: `{row.restore_group}`",
            f"- save payload profile: `{row.save_payload_profile}`",
            f"- restore payload profile: `{row.restore_payload_profile}`",
            f"- source predicate profile: `{row.source_predicate_profile}`",
            f"- branch profile: `{row.branch_profile}`",
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
        "RE-025 proves only that save group `5` has a packed status-flags anchor plus source-visible header-bit predicates for item flags, timer, and trigger flags. It does not prove the separate payload bodies, restore assignment order, or object-extension predicates.",
        "",
        "Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.",
        "",
        "Recommended next ticket: RE-026 — prove object subtype/layout fanout and extra restore bytes for save group `8`, while keeping save group `5` payload-body predicates blocked until source-backed field identities exist.",
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

    proof = build_restoreleveldata_group5_payload_predicate_proof(
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
