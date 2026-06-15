#!/usr/bin/env python3
"""Build a metadata-only RestoreLevelData branch/predicate map.

This RE-021 audit reads the ignored original RestoreLevelData dump locally to
count nearby branch shapes around restore read groups selected by RE-020. The
versioned outputs contain only relative zones, branch classes, size sequences,
predicate hypotheses, and proof limits. Raw opcode text, machine words, payload
coordinates, and branch/call targets are intentionally not emitted.
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

DEFAULT_ORIGINAL_DUMP = "build/reverse/re007/original/RestoreLevelData_80054f6c.csv"
DEFAULT_RESTORE_CALL_MAP_CSV = "docs/reverse/generated/restoreleveldata-read-call-map.csv"
DEFAULT_FIELD_CONTROL_FLOW_CSV = "docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv"
DEFAULT_OUT_CSV = "docs/reverse/generated/restoreleveldata-branch-predicate-map.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/restoreleveldata-branch-predicate-map.md"
DEFAULT_WINDOW = 16
ZONE_ORDER = ("before", "inside", "after")
BRANCH_CLASS_ORDER = ("conditional-compare", "conditional-sign", "unconditional-jump")


@dataclass(frozen=True)
class RestoreGroupMeta:
    restore_group: int
    first_call_index: int
    last_call_index: int
    call_count: int
    size_sequence: str


@dataclass(frozen=True)
class BranchPredicateRow:
    restore_group: int
    linked_save_groups: str
    call_count: int
    size_sequence: str
    branch_window: str
    branch_summary: str
    branch_total: int
    nearest_branch_zone: str
    predicate_hypothesis: str
    confidence: str
    proof_status: str
    patch_readiness: str
    proof_limit: str


@dataclass(frozen=True)
class RestoreBranchPredicateMap:
    original_dump: Path
    restore_call_map_csv: Path
    field_control_flow_csv: Path
    window: int
    restore_groups_covered: tuple[int, ...]
    rows: tuple[BranchPredicateRow, ...]
    patch_ready_count: int
    status: str


def _relative_to_repo(path: Path, repo: Path) -> Path:
    try:
        return path.resolve().relative_to(repo.resolve())
    except ValueError:
        return path


def _read_restore_groups(path: Path) -> dict[int, RestoreGroupMeta]:
    groups: dict[int, RestoreGroupMeta] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("record_kind") != "restore-read-group":
                continue
            group_id = int(row["restore_group"])
            groups[group_id] = RestoreGroupMeta(
                restore_group=group_id,
                first_call_index=int(row["first_call_index"]),
                last_call_index=int(row["last_call_index"]),
                call_count=int(row["call_count"]),
                size_sequence=row["size_sequence"],
            )
    return groups


def _read_candidate_links(path: Path) -> dict[int, list[int]]:
    links: dict[int, list[int]] = defaultdict(list)
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            save_group = int(row["save_original_group"])
            raw_candidates = row.get("restore_group_candidates") or ""
            if raw_candidates == "none":
                continue
            for part in raw_candidates.split(";"):
                part = part.strip()
                if not part:
                    continue
                links[int(part)].append(save_group)
    return {group: sorted(set(save_groups)) for group, save_groups in links.items()}


def _branch_class(opcode_text: str) -> str | None:
    text = opcode_text.strip().lower()
    if text.startswith(("beq", "bne")):
        return "conditional-compare"
    if text.startswith(("blez", "bgtz", "bltz", "bgez")):
        return "conditional-sign"
    if text.startswith("j "):
        return "unconditional-jump"
    return None


def _branch_summary(original_dump: Path, group: RestoreGroupMeta, window: int) -> tuple[str, int, str]:
    counts: Counter[tuple[str, str]] = Counter()
    nearest: tuple[int, str] | None = None
    with original_dump.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            idx = int(row["index"])
            if idx < group.first_call_index - window or idx > group.last_call_index + window:
                continue
            branch_class = _branch_class(row.get("instruction") or "")
            if branch_class is None:
                continue
            if idx < group.first_call_index:
                zone = "before"
                distance = group.first_call_index - idx
            elif idx > group.last_call_index:
                zone = "after"
                distance = idx - group.last_call_index
            else:
                zone = "inside"
                distance = 0
            counts[(zone, branch_class)] += 1
            candidate = (distance, zone)
            if nearest is None or candidate[0] < nearest[0]:
                nearest = candidate

    parts: list[str] = []
    for zone in ZONE_ORDER:
        for branch_class in BRANCH_CLASS_ORDER:
            count = counts.get((zone, branch_class), 0)
            if count:
                parts.append(f"{zone}:{branch_class}={count}")
    return ";".join(parts) if parts else "none", sum(counts.values()), nearest[1] if nearest else "none"


def _predicate_hypothesis(group_id: int) -> tuple[str, str, str, str]:
    mapping = {
        4: (
            "active-item-header-and-animation-split",
            "medium",
            "split-branch-candidate",
            "branch-rich region aligns with save group 4 but repeated small fields prevent predicate identity.",
        ),
        5: (
            "active-item-optional-payload-fanout",
            "medium",
            "branch-fanout-candidate",
            "branch fanout suggests optional active-item payloads but field predicates are not individually proven.",
        ),
        6: (
            "object-payload-anchor-compact-branch",
            "medium",
            "rare-anchor-branch-candidate",
            "rare object payload anchors sit in a compact branch envelope but source predicates are still unknown.",
        ),
        8: (
            "object-subtype-layout-fanout",
            "medium",
            "branch-fanout-candidate",
            "object/layout payload anchors sit inside branch fanout with extra restore bytes and unresolved field identity.",
        ),
        9: (
            "exact-window-room-sentinel-candidate",
            "low",
            "exact-window-needs-predicate-proof",
            "exact read-size window still lacks field predicate identity.",
        ),
    }
    return mapping.get(group_id, (
        "unclassified-restore-branch-region",
        "low",
        "needs-manual-proof",
        "no conservative predicate hypothesis assigned.",
    ))


def build_restore_branch_predicate_map(repo: Path, original_dump: Path, restore_call_map_csv: Path, field_control_flow_csv: Path, window: int = DEFAULT_WINDOW) -> RestoreBranchPredicateMap:
    restore_groups = _read_restore_groups(restore_call_map_csv)
    links = _read_candidate_links(field_control_flow_csv)
    selected_groups = tuple(sorted(group for group in links if group in restore_groups))
    rows: list[BranchPredicateRow] = []
    for group_id in selected_groups:
        group = restore_groups[group_id]
        summary, total, nearest_zone = _branch_summary(original_dump, group, window)
        hypothesis, confidence, proof_status, proof_limit = _predicate_hypothesis(group_id)
        rows.append(BranchPredicateRow(
            restore_group=group_id,
            linked_save_groups=";".join(str(group) for group in links[group_id]),
            call_count=group.call_count,
            size_sequence=group.size_sequence,
            branch_window=f"call-range±{window}",
            branch_summary=summary,
            branch_total=total,
            nearest_branch_zone=nearest_zone,
            predicate_hypothesis=hypothesis,
            confidence=confidence,
            proof_status=proof_status,
            patch_readiness="blocked",
            proof_limit=proof_limit,
        ))

    patch_ready_count = sum(1 for row in rows if row.patch_readiness == "ready")
    informative = sum(1 for row in rows if row.proof_status != "needs-manual-proof")
    status = "restore-branch-predicate-map-partial" if informative else "restore-branch-predicate-map-missing"
    return RestoreBranchPredicateMap(
        original_dump=_relative_to_repo(original_dump, repo),
        restore_call_map_csv=_relative_to_repo(restore_call_map_csv, repo),
        field_control_flow_csv=_relative_to_repo(field_control_flow_csv, repo),
        window=window,
        restore_groups_covered=selected_groups,
        rows=tuple(rows),
        patch_ready_count=patch_ready_count,
        status=status,
    )


def write_csv(branch_map: RestoreBranchPredicateMap, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "restore_group", "linked_save_groups", "call_count", "size_sequence",
        "branch_window", "branch_summary", "branch_total", "nearest_branch_zone",
        "predicate_hypothesis", "confidence", "proof_status", "patch_readiness", "proof_limit",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in branch_map.rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def write_markdown(branch_map: RestoreBranchPredicateMap, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RestoreLevelData branch/predicate map",
        "",
        "Status: Generated",
        "Story: `docs/stories/RE-021-restoreleveldata-branch-predicate-map.md`",
        "",
        "## Progress tracker",
        "",
        "- [x] Load RE-019 restore read-group metadata.",
        "- [x] Load RE-020 candidate restore/save links.",
        "- [x] Count nearby branch classes in relative zones only.",
        "- [x] Assign conservative predicate hypotheses and proof limits.",
        "- [x] Keep raw opcode text, machine words, payload coordinates, and branch/call targets out of versioned outputs.",
        "- [x] Preserve marker verdict limits.",
        "",
        "## Inputs",
        "",
        f"- Original dump CSV: `{branch_map.original_dump}` (ignored; not versioned)",
        f"- RE-019 restore call-map CSV: `{branch_map.restore_call_map_csv}`",
        f"- RE-020 field/control-flow CSV: `{branch_map.field_control_flow_csv}`",
        f"- Branch scan window: `{branch_map.window}` rows around each read-call range",
        "",
        "## Summary",
        "",
        f"- restore groups covered: `{', '.join(map(str, branch_map.restore_groups_covered))}`",
        f"- proof rows: `{len(branch_map.rows)}`",
        f"- patch-ready groups: `{branch_map.patch_ready_count}`",
        f"- status: `{branch_map.status}`",
        "",
        "## Branch/predicate matrix",
        "",
    ]
    for row in branch_map.rows:
        lines.extend([
            f"### Restore group {row.restore_group}",
            "",
            f"- linked save groups: `{row.linked_save_groups}`",
            f"- read call count: `{row.call_count}`",
            f"- size sequence: `{row.size_sequence}`",
            f"- branch window: `{row.branch_window}`",
            f"- branch summary: `{row.branch_summary}`",
            f"- branch total: `{row.branch_total}`",
            f"- nearest branch zone: `{row.nearest_branch_zone}`",
            f"- predicate hypothesis: `{row.predicate_hypothesis}`",
            f"- confidence: `{row.confidence}`",
            f"- proof status: `{row.proof_status}`",
            f"- patch readiness: `{row.patch_readiness}`",
            f"- proof limit: {row.proof_limit}",
            "",
        ])
    lines.extend([
        "## Verdict",
        "",
        "RE-021 identifies branch-rich candidate regions and compact rare-anchor regions, but it still does not prove exact field predicates. Patch readiness remains `0`.",
        "",
        "Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.",
        "",
        "Next step: reconcile branch-region hypotheses with source field identities and optional payload predicates before any serializer modification.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="TOMB5 repo root")
    parser.add_argument("--original-dump", default=DEFAULT_ORIGINAL_DUMP, help="ignored original RestoreLevelData dump CSV, relative to repo")
    parser.add_argument("--restore-call-map-csv", default=DEFAULT_RESTORE_CALL_MAP_CSV, help="RE-019 restore call-map CSV, relative to repo")
    parser.add_argument("--field-control-flow-csv", default=DEFAULT_FIELD_CONTROL_FLOW_CSV, help="RE-020 field/control-flow CSV, relative to repo")
    parser.add_argument("--window", type=int, default=DEFAULT_WINDOW, help="rows around each read-call range to classify")
    parser.add_argument("--csv", default=DEFAULT_OUT_CSV, help="versionable CSV output, relative to repo")
    parser.add_argument("--md", default=DEFAULT_OUT_MD, help="versionable markdown output, relative to repo")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    branch_map = build_restore_branch_predicate_map(
        repo=repo,
        original_dump=repo / args.original_dump,
        restore_call_map_csv=repo / args.restore_call_map_csv,
        field_control_flow_csv=repo / args.field_control_flow_csv,
        window=args.window,
    )
    csv_path = repo / args.csv
    md_path = repo / args.md
    write_csv(branch_map, csv_path)
    write_markdown(branch_map, md_path)
    print(f"restore_groups={','.join(map(str, branch_map.restore_groups_covered))}")
    print(f"proof_rows={len(branch_map.rows)}")
    print(f"patch_ready_count={branch_map.patch_ready_count}")
    print(f"status={branch_map.status}")
    print(f"csv={csv_path}")
    print(f"md={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
