#!/usr/bin/env python3
"""Build a metadata-only RestoreLevelData field/control-flow proof table.

RE-019 proved that exact size-subsequence matching is too weak for serializer
patches. This follow-up keeps the evidence versionable by using only prior
metadata CSVs: SaveLevelData field hypotheses and RestoreLevelData read-group
size sequences. It records candidate restore regions, rare payload anchors, and
remaining proof limits without emitting original opcode text or binary-derived
rows.
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

DEFAULT_FIELD_WIDTH_CSV = "docs/reverse/generated/saveleveldata-item-field-width-audit.csv"
DEFAULT_RESTORE_CALL_MAP_CSV = "docs/reverse/generated/restoreleveldata-read-call-map.csv"
DEFAULT_OUT_CSV = "docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/restoreleveldata-field-control-flow-proof.md"
PRIORITY_GROUPS = (4, 5, 8, 10)
GAP_STATUS_ORDER = (
    "source-missing-field",
    "exact-field-width-match",
    "source-layout-mismatch",
    "source-width-mismatch",
    "branch-boundary-or-sentinel",
    "needs-manual-field-proof",
)


@dataclass(frozen=True)
class SaveFieldRow:
    original_group: int
    call_ordinal: int
    original_size: int | None
    probable_source_field: str
    source_size: int | None
    gap_status: str


@dataclass(frozen=True)
class RestoreGroup:
    group_id: int
    call_count: int
    size_sequence: tuple[int | None, ...]


@dataclass(frozen=True)
class RestoreFieldControlFlowRow:
    save_original_group: int
    save_call_count: int
    save_size_sequence: str
    gap_summary: str
    rare_payload_anchors: str
    restore_group_candidates: str
    restore_size_sequences: str
    proof_status: str
    patch_readiness: str
    proof_limit: str


@dataclass(frozen=True)
class RestoreFieldControlFlowProof:
    field_width_csv: Path
    restore_call_map_csv: Path
    priority_groups: tuple[int, ...]
    rows: tuple[RestoreFieldControlFlowRow, ...]
    patch_ready_count: int
    status: str


def _relative_to_repo(path: Path, repo: Path) -> Path:
    try:
        return path.resolve().relative_to(repo.resolve())
    except ValueError:
        return path


def _parse_size(text: str | None) -> int | None:
    if text is None or text == "" or text == "unknown":
        return None
    return int(text)


def _sequence_text(sizes: tuple[int | None, ...]) -> str:
    return ",".join("unknown" if size is None else str(size) for size in sizes)


def _read_field_rows(path: Path) -> dict[int, tuple[SaveFieldRow, ...]]:
    grouped: dict[int, list[SaveFieldRow]] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            group = int(row["original_group"])
            if group not in PRIORITY_GROUPS:
                continue
            grouped.setdefault(group, []).append(SaveFieldRow(
                original_group=group,
                call_ordinal=int(row["call_ordinal"]),
                original_size=_parse_size(row.get("original_size")),
                probable_source_field=row.get("probable_source_field", ""),
                source_size=_parse_size(row.get("source_size")),
                gap_status=row.get("gap_status", ""),
            ))
    return {group: tuple(rows) for group, rows in sorted(grouped.items())}


def _read_restore_groups(path: Path) -> dict[int, RestoreGroup]:
    groups: dict[int, RestoreGroup] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("record_kind") != "restore-read-group":
                continue
            sizes = tuple(_parse_size(part) for part in row["size_sequence"].split(","))
            group_id = int(row["restore_group"])
            groups[group_id] = RestoreGroup(
                group_id=group_id,
                call_count=int(row["call_count"]),
                size_sequence=sizes,
            )
    return groups


def _read_exact_restore_locations(path: Path) -> dict[int, tuple[int, ...]]:
    locations: dict[int, tuple[int, ...]] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("record_kind") != "save-restore-comparison":
                continue
            group_text = row.get("save_original_group") or ""
            if not group_text:
                continue
            group = int(group_text)
            raw_locations = row.get("restore_match_locations") or ""
            candidates: list[int] = []
            if raw_locations and raw_locations != "none":
                for part in raw_locations.split(";"):
                    part = part.strip()
                    if part.startswith("restore_group="):
                        candidates.append(int(part.split(":", 1)[0].split("=", 1)[1]))
            locations[group] = tuple(sorted(set(candidates)))
    return locations


def _gap_summary(rows: tuple[SaveFieldRow, ...]) -> str:
    counts = Counter(row.gap_status for row in rows)
    ordered = [status for status in GAP_STATUS_ORDER if counts.get(status)]
    ordered.extend(sorted(status for status in counts if status not in ordered))
    return ";".join(f"{status}={counts[status]}" for status in ordered)


def _rare_anchors(group: int, rows: tuple[SaveFieldRow, ...]) -> tuple[int, ...]:
    sizes = tuple(row.original_size for row in rows if row.original_size is not None)
    if group == 5:
        # Exclude the leading packed flag word: RE-020 cares about object payload
        # anchors that can identify a restore region beyond repeated 2-byte fields.
        return tuple(size for size in sizes if size in {20, 24})
    if group == 8:
        return tuple(size for size in sizes if size in {20, 4})
    return tuple(size for size in sizes if size and size > 4)


def _groups_with_ordered_anchors(groups: dict[int, RestoreGroup], anchors: tuple[int, ...]) -> tuple[int, ...]:
    if not anchors:
        return ()
    matches: list[int] = []
    for group_id, group in groups.items():
        pos = 0
        for size in group.size_sequence:
            if pos < len(anchors) and size == anchors[pos]:
                pos += 1
        if pos == len(anchors):
            matches.append(group_id)
    return tuple(matches)


def _candidate_groups(group: int, anchors: tuple[int, ...], restore_groups: dict[int, RestoreGroup], exact_locations: dict[int, tuple[int, ...]]) -> tuple[int, ...]:
    if group == 4:
        return (4, 5)
    if anchors:
        return _groups_with_ordered_anchors(restore_groups, anchors)
    return exact_locations.get(group, ())


def _proof_status(group: int, anchors: tuple[int, ...], candidates: tuple[int, ...], exact_locations: dict[int, tuple[int, ...]]) -> str:
    if group == 4 and candidates:
        return "control-flow-split-candidate"
    if anchors and candidates:
        return "rare-payload-anchor"
    if exact_locations.get(group):
        return "exact-size-window"
    if candidates:
        return "ambiguous-size-only"
    return "missing-restore-proof"


def _proof_limit(group: int, proof_status: str, anchors: tuple[int, ...]) -> str:
    if group == 4:
        return "restore read regions are split across candidate groups 4 and 5; repeated 2-byte fields prevent field/predicate proof."
    if group == 5:
        return "object payload anchors exist on restore side, but leading packed flags and separate item flag/timer/trigger payload predicates remain unproved."
    if group == 8:
        return "object payload anchors exist on restore side, but extra restore bytes and layout mismatches still block field equivalence."
    if group == 10:
        return "exact size window is not predicate proof; room/control-flow layout still needs restore-side field proof."
    if proof_status == "rare-payload-anchor":
        return f"rare anchors {_sequence_text(anchors)} identify a candidate region but not branch predicates."
    return "no sufficient restore-side field/control-flow proof."


def build_restore_field_control_flow_proof(repo: Path, field_width_csv: Path, restore_call_map_csv: Path) -> RestoreFieldControlFlowProof:
    save_rows = _read_field_rows(field_width_csv)
    restore_groups = _read_restore_groups(restore_call_map_csv)
    exact_locations = _read_exact_restore_locations(restore_call_map_csv)

    proof_rows: list[RestoreFieldControlFlowRow] = []
    for group in PRIORITY_GROUPS:
        rows = save_rows[group]
        save_sequence = tuple(row.original_size for row in rows)
        anchors = _rare_anchors(group, rows)
        candidates = _candidate_groups(group, anchors, restore_groups, exact_locations)
        status = _proof_status(group, anchors, candidates, exact_locations)
        restore_sequences = "; ".join(
            f"restore_group={candidate}:{_sequence_text(restore_groups[candidate].size_sequence)}"
            for candidate in candidates
            if candidate in restore_groups
        ) or "none"
        proof_rows.append(RestoreFieldControlFlowRow(
            save_original_group=group,
            save_call_count=len(rows),
            save_size_sequence=_sequence_text(save_sequence),
            gap_summary=_gap_summary(rows),
            rare_payload_anchors=_sequence_text(anchors) if anchors else "none",
            restore_group_candidates=";".join(str(candidate) for candidate in candidates) if candidates else "none",
            restore_size_sequences=restore_sequences,
            proof_status=status,
            patch_readiness="blocked",
            proof_limit=_proof_limit(group, status, anchors),
        ))

    patch_ready_count = sum(1 for row in proof_rows if row.patch_readiness == "ready")
    informative = sum(1 for row in proof_rows if row.proof_status != "missing-restore-proof")
    status = "restore-field-control-flow-proof-partial" if informative else "restore-field-control-flow-proof-missing"
    return RestoreFieldControlFlowProof(
        field_width_csv=_relative_to_repo(field_width_csv, repo),
        restore_call_map_csv=_relative_to_repo(restore_call_map_csv, repo),
        priority_groups=PRIORITY_GROUPS,
        rows=tuple(proof_rows),
        patch_ready_count=patch_ready_count,
        status=status,
    )


def write_csv(proof: RestoreFieldControlFlowProof, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "save_original_group", "save_call_count", "save_size_sequence", "gap_summary",
        "rare_payload_anchors", "restore_group_candidates", "restore_size_sequences",
        "proof_status", "patch_readiness", "proof_limit",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in proof.rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def write_markdown(proof: RestoreFieldControlFlowProof, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RestoreLevelData field/control-flow proof",
        "",
        "Status: Generated",
        "Story: `docs/stories/RE-020-restoreleveldata-field-control-flow-proof.md`",
        "",
        "## Progress tracker",
        "",
        "- [x] Load RE-017 field/width hypotheses.",
        "- [x] Load RE-019 restore read-group size metadata.",
        "- [x] Classify priority item groups by restore evidence strength.",
        "- [x] Keep raw original rows, opcode text, machine words, and payload coordinates out of versioned outputs.",
        "- [x] Preserve marker verdict limits.",
        "",
        "## Inputs",
        "",
        f"- RE-017 field-width CSV: `{proof.field_width_csv}`",
        f"- RE-019 restore call-map CSV: `{proof.restore_call_map_csv}`",
        "",
        "## Summary",
        "",
        f"- priority groups covered: `{', '.join(map(str, proof.priority_groups))}`",
        f"- proof rows: `{len(proof.rows)}`",
        f"- patch-ready groups: `{proof.patch_ready_count}`",
        f"- status: `{proof.status}`",
        "",
        "## Priority group matrix",
        "",
    ]
    for row in proof.rows:
        lines.extend([
            f"### Save original item group {row.save_original_group}",
            "",
            f"- save call count: `{row.save_call_count}`",
            f"- save size sequence: `{row.save_size_sequence}`",
            f"- gap summary: `{row.gap_summary}`",
            f"- rare payload anchors: `{row.rare_payload_anchors}`",
            f"- restore group candidates: `{row.restore_group_candidates}`",
            f"- restore size sequences: `{row.restore_size_sequences}`",
            f"- proof status: `{row.proof_status}`",
            f"- patch readiness: `{row.patch_readiness}`",
            f"- proof limit: {row.proof_limit}",
            "",
        ])
    lines.extend([
        "## Verdict",
        "",
        "RE-020 improves the triage map by identifying candidate restore regions and rare payload anchors, but it still does not prove field predicates or full control-flow equivalence. Patch readiness remains `0`.",
        "",
        "Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.",
        "",
        "Next step: derive branch-predicate metadata around the candidate restore regions before any serializer source modification.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="TOMB5 repo root")
    parser.add_argument("--field-width-csv", default=DEFAULT_FIELD_WIDTH_CSV, help="RE-017 field-width CSV, relative to repo")
    parser.add_argument("--restore-call-map-csv", default=DEFAULT_RESTORE_CALL_MAP_CSV, help="RE-019 restore call-map CSV, relative to repo")
    parser.add_argument("--csv", default=DEFAULT_OUT_CSV, help="versionable CSV output, relative to repo")
    parser.add_argument("--md", default=DEFAULT_OUT_MD, help="versionable markdown output, relative to repo")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    proof = build_restore_field_control_flow_proof(
        repo=repo,
        field_width_csv=repo / args.field_width_csv,
        restore_call_map_csv=repo / args.restore_call_map_csv,
    )
    csv_path = repo / args.csv
    md_path = repo / args.md
    write_csv(proof, csv_path)
    write_markdown(proof, md_path)
    print(f"priority_groups={','.join(map(str, proof.priority_groups))}")
    print(f"proof_rows={len(proof.rows)}")
    print(f"patch_ready_count={proof.patch_ready_count}")
    print(f"status={proof.status}")
    print(f"csv={csv_path}")
    print(f"md={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
