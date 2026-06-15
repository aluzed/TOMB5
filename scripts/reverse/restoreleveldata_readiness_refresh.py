#!/usr/bin/env python3
"""Refresh RestoreLevelData implementation readiness from RE-024..RE-026 proofs.

RE-027 consolidates the proof-first follow-ups into a single metadata-only
readiness matrix. It does not read original dumps and does not make source patch
claims while any group remains blocked.
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
DEFAULT_ROOM_SPLIT_CSV = "docs/reverse/generated/restoreleveldata-room-split-predicate-proof.csv"
DEFAULT_GROUP5_PAYLOAD_CSV = "docs/reverse/generated/restoreleveldata-group5-payload-predicate-proof.csv"
DEFAULT_GROUP8_FANOUT_CSV = "docs/reverse/generated/restoreleveldata-group8-layout-fanout-proof.csv"
DEFAULT_OUT_CSV = "docs/reverse/generated/restoreleveldata-readiness-refresh.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/restoreleveldata-readiness-refresh.md"
TARGET_GROUPS = (4, 5, 8, 10)
SOURCE_PROOF_INPUTS = ("RE-024", "RE-025", "RE-026")


@dataclass(frozen=True)
class RestoreLevelDataReadinessRefreshRow:
    save_original_group: int
    restore_groups: str
    latest_evidence: str
    evidence_summary: str
    prior_plan_phase: str
    remaining_blockers: str
    readiness_phase: str
    safe_next_action: str
    code_change_readiness: str
    recommended_next_ticket: str


@dataclass(frozen=True)
class RestoreLevelDataReadinessRefresh:
    implementation_plan_csv: Path
    room_split_csv: Path
    group5_payload_csv: Path
    group8_fanout_csv: Path
    source_proof_inputs: tuple[str, ...]
    target_save_groups: tuple[int, ...]
    rows: tuple[RestoreLevelDataReadinessRefreshRow, ...]
    rows_count: int
    code_change_ready_count: int
    status: str


def _relative_to_repo(path: Path, repo: Path) -> Path:
    try:
        return path.resolve().relative_to(repo.resolve())
    except ValueError:
        return path


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _rows_by_int(path: Path, field: str) -> dict[int, dict[str, str]]:
    return {int(row[field]): row for row in _read_csv(path)}


def _blocked_count(rows: list[dict[str, str]]) -> int:
    return sum(1 for row in rows if row.get("code_change_readiness") == "blocked")


def _build_group4(room_rows: dict[int, dict[str, str]], plan_rows: dict[int, dict[str, str]]) -> RestoreLevelDataReadinessRefreshRow:
    row = room_rows[4]
    plan = plan_rows[4]
    return RestoreLevelDataReadinessRefreshRow(
        save_original_group=4,
        restore_groups=row["restore_groups"],
        latest_evidence="RE-024 room/split predicate proof",
        evidence_summary=f"proof-focus={row['proof_focus']};verdict={row['proof_verdict']}",
        prior_plan_phase=plan["implementation_phase"],
        remaining_blockers=row["blocking_predicates"],
        readiness_phase="continue-source-field-proof",
        safe_next_action="prove split active-item restore predicates before source reconstruction",
        code_change_readiness="blocked",
        recommended_next_ticket="RE-028",
    )


def _build_group10(room_rows: dict[int, dict[str, str]], plan_rows: dict[int, dict[str, str]]) -> RestoreLevelDataReadinessRefreshRow:
    row = room_rows[10]
    plan = plan_rows[10]
    return RestoreLevelDataReadinessRefreshRow(
        save_original_group=10,
        restore_groups=row["restore_groups"],
        latest_evidence="RE-024 room/split predicate proof",
        evidence_summary=f"proof-focus={row['proof_focus']};verdict={row['proof_verdict']}",
        prior_plan_phase=plan["implementation_phase"],
        remaining_blockers=row["blocking_predicates"],
        readiness_phase="continue-source-field-proof",
        safe_next_action="prove room byte placement before source reconstruction",
        code_change_readiness="blocked",
        recommended_next_ticket="RE-028",
    )


def _build_group5(group5_rows: list[dict[str, str]], plan_rows: dict[int, dict[str, str]]) -> RestoreLevelDataReadinessRefreshRow:
    verdict_counts = Counter(row.get("proof_verdict", "unknown") for row in group5_rows)
    anchor_count = verdict_counts.get("source-backed-anchor-only", 0)
    return RestoreLevelDataReadinessRefreshRow(
        save_original_group=5,
        restore_groups=plan_rows[5]["restore_groups"],
        latest_evidence="RE-025 group 5 payload predicate proof",
        evidence_summary=f"payload-families={len(group5_rows)};blocked={_blocked_count(group5_rows)};source-backed-anchor-only={anchor_count}",
        prior_plan_phase=plan_rows[5]["implementation_phase"],
        remaining_blockers="item_flags[0..3] payload bodies;timer payload body;trigger_flags payload body;object-extension field identity",
        readiness_phase="continue-source-field-proof",
        safe_next_action="prove payload body field identities or keep group out of source patch scope",
        code_change_readiness="blocked",
        recommended_next_ticket="RE-028",
    )


def _build_group8(group8_rows: list[dict[str, str]], plan_rows: dict[int, dict[str, str]]) -> RestoreLevelDataReadinessRefreshRow:
    deps = sorted({row.get("prior_group5_dependency", "none") for row in group8_rows if row.get("prior_group5_dependency") != "none"})
    dep = ";".join(deps) if deps else "none"
    return RestoreLevelDataReadinessRefreshRow(
        save_original_group=8,
        restore_groups=plan_rows[8]["restore_groups"],
        latest_evidence="RE-026 group 8 layout/fanout proof",
        evidence_summary=f"fanout-families={len(group8_rows)};blocked={_blocked_count(group8_rows)};group5-dependency={dep}",
        prior_plan_phase=plan_rows[8]["implementation_phase"],
        remaining_blockers="subtype/extra byte predicate;layout block 20;room/rotation ordering;item data word;item flag payload bodies",
        readiness_phase="continue-source-field-proof",
        safe_next_action="prove subtype/layout fanout field identities or keep group out of source patch scope",
        code_change_readiness="blocked",
        recommended_next_ticket="RE-028",
    )


def build_restoreleveldata_readiness_refresh(
    repo: Path,
    implementation_plan_csv: Path,
    room_split_csv: Path,
    group5_payload_csv: Path,
    group8_fanout_csv: Path,
) -> RestoreLevelDataReadinessRefresh:
    plan_rows = _rows_by_int(implementation_plan_csv, "save_original_group")
    room_rows = _rows_by_int(room_split_csv, "save_original_group")
    group5_rows = _read_csv(group5_payload_csv)
    group8_rows = _read_csv(group8_fanout_csv)

    rows = (
        _build_group4(room_rows, plan_rows),
        _build_group5(group5_rows, plan_rows),
        _build_group8(group8_rows, plan_rows),
        _build_group10(room_rows, plan_rows),
    )
    code_ready = sum(1 for row in rows if row.code_change_readiness == "ready")
    return RestoreLevelDataReadinessRefresh(
        implementation_plan_csv=_relative_to_repo(implementation_plan_csv, repo),
        room_split_csv=_relative_to_repo(room_split_csv, repo),
        group5_payload_csv=_relative_to_repo(group5_payload_csv, repo),
        group8_fanout_csv=_relative_to_repo(group8_fanout_csv, repo),
        source_proof_inputs=SOURCE_PROOF_INPUTS,
        target_save_groups=tuple(row.save_original_group for row in rows),
        rows=rows,
        rows_count=len(rows),
        code_change_ready_count=code_ready,
        status="restoreleveldata-readiness-refresh-blocked",
    )


def write_csv(refresh: RestoreLevelDataReadinessRefresh, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "save_original_group",
        "restore_groups",
        "latest_evidence",
        "evidence_summary",
        "prior_plan_phase",
        "remaining_blockers",
        "readiness_phase",
        "safe_next_action",
        "code_change_readiness",
        "recommended_next_ticket",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in refresh.rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def write_markdown(refresh: RestoreLevelDataReadinessRefresh, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RestoreLevelData readiness refresh",
        "",
        "Status: Generated",
        "Story: `docs/stories/RE-027-restoreleveldata-readiness-refresh.md`",
        "",
        "## Progress tracker",
        "",
        "- [x] Load RE-023 implementation plan metadata.",
        "- [x] Load RE-024 room/split predicate proof.",
        "- [x] Load RE-025 group 5 payload predicate proof.",
        "- [x] Load RE-026 group 8 layout/fanout proof.",
        "- [x] Refresh readiness rows for save groups `4`, `5`, `8`, and `10`.",
        "- [x] Keep source patch readiness blocked while blockers remain.",
        "- [x] Keep raw opcode text, machine words, payload coordinates, addresses, and branch/call targets out of versioned outputs.",
        "",
        "## Inputs",
        "",
        f"- RE-023 plan CSV: `{refresh.implementation_plan_csv}`",
        f"- RE-024 room/split CSV: `{refresh.room_split_csv}`",
        f"- RE-025 group 5 payload CSV: `{refresh.group5_payload_csv}`",
        f"- RE-026 group 8 fanout CSV: `{refresh.group8_fanout_csv}`",
        "",
        "## Summary",
        "",
        f"- source proof inputs: `{', '.join(refresh.source_proof_inputs)}`",
        f"- target save groups: `{', '.join(str(g) for g in refresh.target_save_groups)}`",
        f"- readiness rows: `{refresh.rows_count}`",
        f"- code-change-ready groups: `{refresh.code_change_ready_count}`",
        f"- status: `{refresh.status}`",
        "",
        "## Readiness matrix",
    ]
    for row in refresh.rows:
        lines.extend([
            "",
            f"### Save group {row.save_original_group}",
            "",
            f"- restore groups: `{row.restore_groups}`",
            f"- latest evidence: `{row.latest_evidence}`",
            f"- evidence summary: `{row.evidence_summary}`",
            f"- prior plan phase: `{row.prior_plan_phase}`",
            f"- remaining blockers: `{row.remaining_blockers}`",
            f"- readiness phase: `{row.readiness_phase}`",
            f"- safe next action: `{row.safe_next_action}`",
            f"- code change readiness: `{row.code_change_readiness}`",
            f"- recommended next ticket: `{row.recommended_next_ticket}`",
        ])
    lines.extend([
        "",
        "## Verdict",
        "",
        "RE-027 confirms that all priority `RestoreLevelData` groups remain blocked after RE-024, RE-025, and RE-026. The safe path is additional source-field identity proof or a later patch scope that explicitly excludes blocked families.",
        "",
        "Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.",
        "",
        "Recommended next ticket: RE-028 — build a source-field identity checklist for the highest-value blocked family, or define a deliberately limited reconstruction scope that excludes every still-blocked predicate.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--implementation-plan-csv", default=DEFAULT_IMPLEMENTATION_PLAN_CSV)
    parser.add_argument("--room-split-csv", default=DEFAULT_ROOM_SPLIT_CSV)
    parser.add_argument("--group5-payload-csv", default=DEFAULT_GROUP5_PAYLOAD_CSV)
    parser.add_argument("--group8-fanout-csv", default=DEFAULT_GROUP8_FANOUT_CSV)
    parser.add_argument("--out-csv", default=DEFAULT_OUT_CSV)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    args = parser.parse_args(argv)

    refresh = build_restoreleveldata_readiness_refresh(
        repo=ROOT,
        implementation_plan_csv=ROOT / args.implementation_plan_csv,
        room_split_csv=ROOT / args.room_split_csv,
        group5_payload_csv=ROOT / args.group5_payload_csv,
        group8_fanout_csv=ROOT / args.group8_fanout_csv,
    )
    write_csv(refresh, ROOT / args.out_csv)
    write_markdown(refresh, ROOT / args.out_md)
    print(f"wrote {args.out_csv} and {args.out_md}: {refresh.status}; code-change-ready={refresh.code_change_ready_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
