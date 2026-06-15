#!/usr/bin/env python3
"""Build the RE-030 RestoreLevelData group 5 restore assignment identity map.

RE-030 asks whether group 5 payload bodies have versionable restore assignment
identities. The answer remains blocked: versioned metadata gives a restore group
6 candidate payload cluster, but the current `RestoreLevelData` source body is
absent and no generated evidence names restore target fields.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_CHECKLIST_CSV = "docs/reverse/generated/restoreleveldata-group5-source-field-identity-checklist.csv"
DEFAULT_ITEM_FLAGS_CSV = "docs/reverse/generated/restoreleveldata-group5-item-flags-body-proof.csv"
DEFAULT_PAYLOAD_CSV = "docs/reverse/generated/restoreleveldata-group5-payload-predicate-proof.csv"
DEFAULT_READ_MAP_CSV = "docs/reverse/generated/restoreleveldata-read-call-map.csv"
DEFAULT_RECONCILIATION_CSV = "docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv"
DEFAULT_SOURCE_FILE = "GAME/SAVEGAME.C"
DEFAULT_OUT_CSV = "docs/reverse/generated/restoreleveldata-group5-restore-assignment-identity-map.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/restoreleveldata-group5-restore-assignment-identity-map.md"
STORY_PATH = "docs/stories/RE-030-restoreleveldata-group5-restore-assignment-identity-map.md"
SOURCE_INPUTS = ("RE-019", "RE-022", "RE-025", "RE-028", "RE-029", "GAME/SAVEGAME.C")
TARGET_SAVE_GROUP = 5
RESTORE_GROUP = 6


@dataclass(frozen=True)
class Group5RestoreAssignmentIdentityRow:
    payload_family: str
    prior_body_proof: str
    restore_candidate_profile: str
    restore_assignment_evidence: str
    assignment_identity_state: str
    required_assignment_evidence: str
    assignment_identity_readiness: str
    code_change_readiness: str
    safe_next_action: str
    recommended_next_ticket: str


@dataclass(frozen=True)
class Group5RestoreAssignmentIdentityMap:
    story_id: str
    checklist_csv: Path
    item_flags_csv: Path
    payload_csv: Path
    read_map_csv: Path
    reconciliation_csv: Path
    source_file: Path
    source_inputs: tuple[str, ...]
    target_save_group: int
    restore_group: int
    restore_source_state: str
    group5_decision: str
    rows: tuple[Group5RestoreAssignmentIdentityRow, ...]
    rows_count: int
    assignment_identity_ready_count: int
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


def _restore_source_state(source_text: str) -> str:
    match = re.search(r"void\s+RestoreLevelData\s*\([^)]*\)[^{]*\{(?P<body>.*?)\n\}", source_text, re.S)
    if not match:
        return "RestoreLevelData source body not found"
    body = match.group("body")
    if "UNIMPLEMENTED();" in body:
        return "RestoreLevelData source body is UNIMPLEMENTED"
    return "RestoreLevelData source body exists but assignment identity still requires proof"


def _restore_candidate_profile(read_map_rows: list[dict[str, str]], family: str) -> str:
    group = next(row for row in read_map_rows if row.get("record_kind") == "restore-read-group" and row.get("restore_group") == str(RESTORE_GROUP))
    widths = [int(part) for part in group["size_sequence"].split(",")]
    if 24 in widths and 20 in widths and widths.count(2) >= 5:
        return "restore group 6 compact branch payload cluster; rare anchor widths present"
    return f"restore group {RESTORE_GROUP} candidate payload cluster"


def _prior_body_proof(family: str, item_flags_rows: list[dict[str, str]], payload_rows: list[dict[str, str]]) -> str:
    if family == "item_flags[0..3]":
        patch_ready = sum(1 for row in item_flags_rows if row.get("code_change_readiness") == "ready")
        return f"candidate-width-only; {len(item_flags_rows)} rows; patch-ready={patch_ready}"
    payload = next(row for row in payload_rows if row.get("payload_family") == family)
    return f"{payload['proof_verdict']}; readiness={payload['code_change_readiness']}"


def _required_assignment_evidence(family: str) -> str:
    return {
        "packed-status-flags": "named restore assignment for packed status word and independence proof for following payload bodies",
        "item_flags[0..3]": "four named restore assignments; per-flag body order; source/restore field identity",
        "timer": "named restore timer assignment and predicate identity",
        "trigger_flags": "named restore trigger_flags assignment and predicate identity",
        "object-extension": "object-specific restore target fields; object predicate map; block assignment order",
    }[family]


def build_restoreleveldata_group5_restore_assignment_identity_map(
    repo: Path,
    checklist_csv: Path,
    item_flags_csv: Path,
    payload_csv: Path,
    read_map_csv: Path,
    reconciliation_csv: Path,
    source_file: Path,
) -> Group5RestoreAssignmentIdentityMap:
    checklist_rows = _read_csv(checklist_csv)
    item_flags_rows = _read_csv(item_flags_csv)
    payload_rows = _read_csv(payload_csv)
    read_map_rows = _read_csv(read_map_csv)
    reconciliation_rows = _read_csv(reconciliation_csv)
    source_text = source_file.read_text(encoding="utf-8")

    group5_reconciliation = next(row for row in reconciliation_rows if row.get("save_original_group") == str(TARGET_SAVE_GROUP))
    if group5_reconciliation.get("patch_readiness") != "blocked":
        raise ValueError("RE-030 expects group 5 reconciliation to remain blocked")

    source_state = _restore_source_state(source_text)
    rows: list[Group5RestoreAssignmentIdentityRow] = []
    for checklist in checklist_rows:
        family = checklist["payload_family"]
        rows.append(
            Group5RestoreAssignmentIdentityRow(
                payload_family=family,
                prior_body_proof=_prior_body_proof(family, item_flags_rows, payload_rows),
                restore_candidate_profile=_restore_candidate_profile(read_map_rows, family),
                restore_assignment_evidence="no versioned restore assignment identity; current source restore body absent",
                assignment_identity_state="missing-restore-assignment-map",
                required_assignment_evidence=_required_assignment_evidence(family),
                assignment_identity_readiness="blocked",
                code_change_readiness="blocked",
                safe_next_action="defer group 5 or recover assignment identities before source reconstruction",
                recommended_next_ticket="RE-031",
            )
        )

    ready = sum(1 for row in rows if row.assignment_identity_readiness == "ready")
    patch_ready = sum(1 for row in rows if row.code_change_readiness == "ready")
    return Group5RestoreAssignmentIdentityMap(
        story_id="RE-030",
        checklist_csv=_relative_to_repo(checklist_csv, repo),
        item_flags_csv=_relative_to_repo(item_flags_csv, repo),
        payload_csv=_relative_to_repo(payload_csv, repo),
        read_map_csv=_relative_to_repo(read_map_csv, repo),
        reconciliation_csv=_relative_to_repo(reconciliation_csv, repo),
        source_file=_relative_to_repo(source_file, repo),
        source_inputs=SOURCE_INPUTS,
        target_save_group=TARGET_SAVE_GROUP,
        restore_group=RESTORE_GROUP,
        restore_source_state=source_state,
        group5_decision="defer-group5-from-source-reconstruction",
        rows=tuple(rows),
        rows_count=len(rows),
        assignment_identity_ready_count=ready,
        patch_ready_count=patch_ready,
        status="restoreleveldata-group5-restore-assignment-identity-map-blocked",
    )


def write_csv(identity_map: Group5RestoreAssignmentIdentityMap, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "payload_family",
        "prior_body_proof",
        "restore_candidate_profile",
        "restore_assignment_evidence",
        "assignment_identity_state",
        "required_assignment_evidence",
        "assignment_identity_readiness",
        "code_change_readiness",
        "safe_next_action",
        "recommended_next_ticket",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in identity_map.rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def write_markdown(identity_map: Group5RestoreAssignmentIdentityMap, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RestoreLevelData group 5 restore assignment identity map",
        "",
        "Status: Generated",
        f"Story: `{STORY_PATH}`",
        "",
        "## Progress tracker",
        "",
        "- [x] Load RE-028 group 5 source-field checklist.",
        "- [x] Load RE-029 item_flags body proof.",
        "- [x] Load RE-025 payload-family metadata and RE-022 reconciliation status.",
        "- [x] Load RE-019 restore group `6` size context without publishing raw coordinates.",
        "- [x] Inspect current source for `RestoreLevelData` body availability.",
        "- [x] Publish restore assignment identity state per group 5 payload family.",
        "- [x] Keep raw opcode text, machine words, payload coordinates, addresses, and branch/call targets out of versioned outputs.",
        "",
        "## Inputs",
        "",
        f"- RE-028 checklist CSV: `{identity_map.checklist_csv}`",
        f"- RE-029 item flags CSV: `{identity_map.item_flags_csv}`",
        f"- RE-025 payload CSV: `{identity_map.payload_csv}`",
        f"- RE-019 read map CSV: `{identity_map.read_map_csv}`",
        f"- RE-022 reconciliation CSV: `{identity_map.reconciliation_csv}`",
        f"- Source file inspected: `{identity_map.source_file}`",
        "",
        "## Summary",
        "",
        f"- source inputs: `{', '.join(identity_map.source_inputs)}`",
        f"- target save group: `{identity_map.target_save_group}`",
        f"- restore group: `{identity_map.restore_group}`",
        f"- restore source state: `{identity_map.restore_source_state}`",
        f"- group 5 decision: `{identity_map.group5_decision}`",
        f"- map rows: `{identity_map.rows_count}`",
        f"- assignment-identity-ready rows: `{identity_map.assignment_identity_ready_count}`",
        f"- patch-ready rows: `{identity_map.patch_ready_count}`",
        f"- status: `{identity_map.status}`",
        "",
        "## Assignment identity rows",
    ]
    for row in identity_map.rows:
        lines.extend([
            "",
            f"### {row.payload_family}",
            "",
            f"- prior body proof: `{row.prior_body_proof}`",
            f"- restore candidate profile: `{row.restore_candidate_profile}`",
            f"- restore assignment evidence: `{row.restore_assignment_evidence}`",
            f"- assignment identity state: `{row.assignment_identity_state}`",
            f"- required assignment evidence: `{row.required_assignment_evidence}`",
            f"- assignment identity readiness: `{row.assignment_identity_readiness}`",
            f"- code change readiness: `{row.code_change_readiness}`",
            f"- safe next action: `{row.safe_next_action}`",
            f"- recommended next ticket: `{row.recommended_next_ticket}`",
        ])
    lines.extend([
        "",
        "## Verdict",
        "",
        "RE-030 does not recover a versionable restore assignment identity map for group `5`. The restore group `6` metadata remains a candidate payload cluster only, and the current `RestoreLevelData` source body is absent. Group `5` should therefore be deferred from source reconstruction scope unless a future proof can name restore target fields without publishing raw dump payloads.",
        "",
        "Do not add `(F)`, `(D)`, or `(**)` markers; do not patch `GAME/SAVEGAME.C` from this map alone.",
        "",
        "Recommended next ticket: RE-031 — define a limited RestoreLevelData reconstruction scope that explicitly excludes group `5`, or produce a non-raw assignment extraction method that can unlock group `5` safely.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checklist-csv", default=DEFAULT_CHECKLIST_CSV)
    parser.add_argument("--item-flags-csv", default=DEFAULT_ITEM_FLAGS_CSV)
    parser.add_argument("--payload-csv", default=DEFAULT_PAYLOAD_CSV)
    parser.add_argument("--read-map-csv", default=DEFAULT_READ_MAP_CSV)
    parser.add_argument("--reconciliation-csv", default=DEFAULT_RECONCILIATION_CSV)
    parser.add_argument("--source-file", default=DEFAULT_SOURCE_FILE)
    parser.add_argument("--out-csv", default=DEFAULT_OUT_CSV)
    parser.add_argument("--out-md", default=DEFAULT_OUT_MD)
    args = parser.parse_args(argv)

    identity_map = build_restoreleveldata_group5_restore_assignment_identity_map(
        repo=ROOT,
        checklist_csv=ROOT / args.checklist_csv,
        item_flags_csv=ROOT / args.item_flags_csv,
        payload_csv=ROOT / args.payload_csv,
        read_map_csv=ROOT / args.read_map_csv,
        reconciliation_csv=ROOT / args.reconciliation_csv,
        source_file=ROOT / args.source_file,
    )
    write_csv(identity_map, ROOT / args.out_csv)
    write_markdown(identity_map, ROOT / args.out_md)
    print(f"wrote {args.out_csv} and {args.out_md}: {identity_map.status}; patch-ready={identity_map.patch_ready_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
