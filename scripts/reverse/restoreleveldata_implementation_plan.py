#!/usr/bin/env python3
"""Build a metadata-only RestoreLevelData implementation plan from RE-022 blockers.

RE-023 deliberately remains a planning/audit artifact. It consumes the versioned
RE-022 field/predicate reconciliation and produces a group-by-group implementation
readiness matrix without reading original dumps or changing GAME/SAVEGAME.C.
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

DEFAULT_RECONCILIATION_CSV = "docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv"
DEFAULT_OUT_CSV = "docs/reverse/generated/restoreleveldata-implementation-plan.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/restoreleveldata-implementation-plan.md"
PRIORITY_GROUPS = (4, 5, 8, 10)


@dataclass(frozen=True)
class ImplementationPlanRow:
    save_original_group: int
    restore_groups: str
    implementation_phase: str
    missing_proof: str
    minimal_safe_action: str
    code_change_readiness: str
    recommended_next_ticket: str
    risk_level: str
    proof_source: str
    notes: str


@dataclass(frozen=True)
class RestoreLevelDataImplementationPlan:
    reconciliation_csv: Path
    save_groups_covered: tuple[int, ...]
    rows: tuple[ImplementationPlanRow, ...]
    patch_ready_count: int
    code_change_ready_count: int
    status: str


def _relative_to_repo(path: Path, repo: Path) -> Path:
    try:
        return path.resolve().relative_to(repo.resolve())
    except ValueError:
        return path


def _profile_for_group(group: int, unresolved_predicates: str, proof_status: str) -> tuple[str, str, str, str, str, str]:
    profiles = {
        4: (
            "prove-split-active-item-layout",
            unresolved_predicates,
            "derive source-level split predicate checklist for active item header and animation payloads",
            "RE-024",
            "high",
            "Prioritize only after split restore groups are explained by source predicates; repeated 2-byte fields make blind coding unsafe.",
        ),
        5: (
            "prove-object-extension-payloads",
            unresolved_predicates,
            "derive source-level payload predicate checklist",
            "RE-025",
            "high",
            "Packed flags alone are insufficient; each optional item flag, timer, trigger, and object extension payload needs a source predicate before code changes.",
        ),
        8: (
            "prove-object-subtype-layout-fanout",
            unresolved_predicates,
            "separate subtype/layout alternatives and identify extra restore bytes as source fields or non-source state rebuild",
            "RE-026",
            "high",
            "Layout fanout and extra restore bytes are the riskiest blockers; keep this behind proof work, not serializer edits.",
        ),
        10: (
            "prove-room-layout-window",
            unresolved_predicates,
            "prove room byte order/layout predicate from source-level field model",
            "RE-024",
            "medium",
            "This is the smallest blocker set and a good next proof target, but exact window size alone is still not enough for a patch.",
        ),
    }
    phase, missing, action, ticket, risk, notes = profiles[group]
    return phase, missing, action, ticket, risk, f"RE-022 proof_status={proof_status}. {notes}"


def build_restoreleveldata_implementation_plan(repo: Path, reconciliation_csv: Path) -> RestoreLevelDataImplementationPlan:
    rows: list[ImplementationPlanRow] = []
    with reconciliation_csv.open(newline="", encoding="utf-8") as f:
        for raw in csv.DictReader(f):
            group = int(raw["save_original_group"])
            if group not in PRIORITY_GROUPS:
                continue
            phase, missing, action, ticket, risk, notes = _profile_for_group(
                group,
                raw.get("unresolved_predicates", "unknown"),
                raw.get("proof_status", "unknown"),
            )
            rows.append(ImplementationPlanRow(
                save_original_group=group,
                restore_groups=raw.get("restore_groups", "none"),
                implementation_phase=phase,
                missing_proof=missing,
                minimal_safe_action=action,
                code_change_readiness="blocked",
                recommended_next_ticket=ticket,
                risk_level=risk,
                proof_source="RE-022 field/predicate reconciliation",
                notes=notes,
            ))

    rows.sort(key=lambda row: PRIORITY_GROUPS.index(row.save_original_group))
    code_ready = sum(1 for row in rows if row.code_change_readiness == "ready")
    patch_ready = 0
    status = "restoreleveldata-implementation-plan-blocked" if rows else "restoreleveldata-implementation-plan-missing"
    return RestoreLevelDataImplementationPlan(
        reconciliation_csv=_relative_to_repo(reconciliation_csv, repo),
        save_groups_covered=tuple(row.save_original_group for row in rows),
        rows=tuple(rows),
        patch_ready_count=patch_ready,
        code_change_ready_count=code_ready,
        status=status,
    )


def write_csv(plan: RestoreLevelDataImplementationPlan, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "save_original_group",
        "restore_groups",
        "implementation_phase",
        "missing_proof",
        "minimal_safe_action",
        "code_change_readiness",
        "recommended_next_ticket",
        "risk_level",
        "proof_source",
        "notes",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in plan.rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def write_markdown(plan: RestoreLevelDataImplementationPlan, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RestoreLevelData implementation plan",
        "",
        "Status: Generated",
        "Story: `docs/stories/RE-023-restoreleveldata-implementation-plan.md`",
        "",
        "## Progress tracker",
        "",
        "- [x] Load RE-022 field/predicate reconciliation metadata.",
        "- [x] Convert each priority save group into a restore implementation readiness row.",
        "- [x] Preserve blocked status for all code changes until missing proofs are resolved.",
        "- [x] Recommend proof-first follow-up tickets before touching `GAME/SAVEGAME.C`.",
        "- [x] Keep raw opcode text, machine words, payload coordinates, addresses, and branch/call targets out of versioned outputs.",
        "",
        "## Inputs",
        "",
        f"- RE-022 reconciliation CSV: `{plan.reconciliation_csv}`",
        "",
        "## Summary",
        "",
        f"- save groups covered: `{', '.join(str(g) for g in plan.save_groups_covered)}`",
        f"- plan rows: `{len(plan.rows)}`",
        f"- patch-ready groups: `{plan.patch_ready_count}`",
        f"- code-change-ready groups: `{plan.code_change_ready_count}`",
        f"- status: `{plan.status}`",
        "",
        "## Implementation readiness matrix",
    ]
    for row in plan.rows:
        lines.extend([
            "",
            f"### Save group {row.save_original_group}",
            "",
            f"- restore groups: `{row.restore_groups}`",
            f"- implementation phase: `{row.implementation_phase}`",
            f"- missing proof: `{row.missing_proof}`",
            f"- minimal safe action: `{row.minimal_safe_action}`",
            f"- code change readiness: `{row.code_change_readiness}`",
            f"- recommended next ticket: `{row.recommended_next_ticket}`",
            f"- risk level: `{row.risk_level}`",
            f"- proof source: `{row.proof_source}`",
            f"- notes: {row.notes}",
        ])
    lines.extend([
        "",
        "## Execution order",
        "",
        "1. Start with RE-024 because save group `10` has the smallest blocker set and can also validate the split proof pattern needed by save group `4`.",
        "2. Defer save group `5` until item flag, timer, trigger, and object extension payload predicates are source-backed.",
        "3. Defer save group `8` until subtype/layout fanout and extra restore bytes are explained without guessing.",
        "4. Only after a row becomes code-change-ready should a later ticket modify `GAME/SAVEGAME.C`.",
        "",
        "## Verdict",
        "",
        "RE-023 is a plan, not an implementation patch. All groups remain blocked for code changes.",
        "",
        "Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.",
        "",
        "Recommended next ticket: RE-024 — prove the room/layout predicate window for save group `10` and the active item split predicate path needed by save group `4`.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reconciliation-csv", default=DEFAULT_RECONCILIATION_CSV)
    parser.add_argument("--out-csv", default=DEFAULT_OUT_CSV)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    args = parser.parse_args(argv)

    plan = build_restoreleveldata_implementation_plan(
        repo=ROOT,
        reconciliation_csv=ROOT / args.reconciliation_csv,
    )
    write_csv(plan, ROOT / args.out_csv)
    write_markdown(plan, ROOT / args.out_md)
    print(f"wrote {args.out_csv} and {args.out_md}: {plan.status}; code-change-ready={plan.code_change_ready_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
