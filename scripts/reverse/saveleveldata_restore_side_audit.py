#!/usr/bin/env python3
"""Audit RE-017 SaveLevelData item hypotheses against restore-side source state.

RE-018 was originally produced when ``RestoreLevelData`` was unimplemented. The
current source has read sites, so this audit now combines:

- RE-017 save-side field/width hypotheses (versioned metadata)
- RE-019 original restore ``ReadSG`` size-comparison metadata, when available
- implemented restore/read capability evidence extracted from ``GAME/SAVEGAME.C``

This remains metadata-only and does not prove original PSX restore equivalence.
It does not patch serializers and does not justify ``(F)``, ``(D)`` or ``(**)``
markers.
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
DEFAULT_RESTORE_READ_MAP_CSV = "docs/reverse/generated/restoreleveldata-read-call-map.csv"
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
    implemented_evidence: str
    re019_restore_match_status: str


@dataclass(frozen=True)
class RestoreSideAudit:
    source: Path
    field_width_csv: Path
    restore_read_map_csv: Path | None
    restore_function_status: str
    total_hypotheses: int
    priority_hypotheses: int
    patch_ready_count: int
    restore_status_counts: dict[str, int]
    rows: tuple[RestoreSideRow, ...]
    status: str


@dataclass(frozen=True)
class ImplementedRestoreEvidence:
    has_read_sites: bool
    has_save_leveldata: bool
    # item-loop capabilities (best-effort, source-text evidence)
    reads_item_header_word: bool
    reads_packed_pos_xyz: bool
    reads_room_byte: bool
    reads_y_rot: bool
    reads_optional_x_rot: bool
    reads_optional_z_rot: bool
    reads_optional_speed: bool
    reads_optional_fallspeed: bool
    reads_anim_states_word: bool  # 2-byte current/goal/required
    reads_lara_anim_word: bool
    reads_nonlara_anim_byte: bool
    reads_frame_word: bool
    reads_hitpoints_word: bool
    reads_packed_flags_dword: bool
    reads_item_flag_payloads: bool  # item_flags[0-3]/timer/trigger_flags 2-byte payloads
    saves_item_flag_payloads: bool
    has_portsave_level_format_gate: bool
    has_object_specific_payload_reads: bool


def _relative_to_repo(path: Path, repo: Path) -> Path:
    try:
        return path.resolve().relative_to(repo.resolve())
    except ValueError:
        return path


def _function_body(text: str, name: str) -> str | None:
    start = text.find(f"void {name}")
    if start == -1:
        return None
    brace = text.find("{", start)
    if brace == -1:
        return None
    depth = 0
    for pos in range(brace, len(text)):
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
            if depth == 0:
                return text[brace : pos + 1]
    return text[brace:]


def _restore_function_status(source: Path) -> str:
    text = source.read_text(encoding="utf-8", errors="replace")
    body = _function_body(text, "RestoreLevelData")
    if body is None:
        return "source-missing"
    if "UNIMPLEMENTED()" in body:
        return "source-unimplemented"
    if "ReadSG(" not in body and "Read(" not in body:
        return "source-no-read-sites"
    return "source-has-read-sites"


def _has(body: str | None, pattern: str) -> bool:
    return bool(body and re.search(pattern, body, re.S))


def _extract_implemented_evidence(source: Path) -> ImplementedRestoreEvidence:
    text = source.read_text(encoding="utf-8", errors="replace")
    restore = _function_body(text, "RestoreLevelData") or ""
    save = _function_body(text, "SaveLevelData") or ""
    has_read = "ReadSG(" in restore or "Read(" in restore
    payload_save = _has(save, r"item->item_flags\[0\].*Write|Write\(.*item->item_flags\[0\].*,\s*2\).*Write\(.*item->timer.*,\s*2\)|Write\(.*item->trigger_flags.*,\s*2\)") or _has(save, r"Write\(.*&item->timer,\s*2\)")
    payload_restore = _has(restore, r"ReadSG\(.*&item->item_flags\[0\],\s*2\)") and _has(restore, r"ReadSG\(.*&item->timer,\s*2\)|ReadSG\(.*&item->trigger_flags,\s*2\)")
    return ImplementedRestoreEvidence(
        has_read_sites=has_read,
        has_save_leveldata=bool(save),
        reads_item_header_word=_has(restore, r'ReadSG\(\(char\*\)&word,\s*2\).*(0x2000|0x8000)'),
        reads_packed_pos_xyz=_has(restore, r'packed.*ReadSG\(\(char\*\)&packed,\s*2\).*item->pos\.x_pos') and _has(restore, r'item->pos\.z_pos'),
        reads_room_byte=_has(restore, r'ReadSG\(\(char\*\)&byte,\s*1\).*new_room\s*=\s*byte'),
        reads_y_rot=_has(restore, r'ReadSG\(\(char\*\)&item->pos\.y_rot,\s*2\)'),
        reads_optional_x_rot=_has(restore, r'word\s*&\s*1.*ReadSG\(\(char\*\)&item->pos\.x_rot,\s*2\)'),
        reads_optional_z_rot=_has(restore, r'word\s*&\s*2.*ReadSG\(\(char\*\)&item->pos\.z_rot,\s*2\)'),
        reads_optional_speed=_has(restore, r'0x20.*ReadSG\(\(char\*\)&item->speed,\s*2\)'),
        reads_optional_fallspeed=_has(restore, r'0x40.*ReadSG\(\(char\*\)&item->fallspeed,\s*2\)'),
        reads_anim_states_word=_has(restore, r'ReadSG\(\(char\*\)&item->current_anim_state,\s*2\).*ReadSG\(\(char\*\)&item->goal_anim_state,\s*2\).*ReadSG\(\(char\*\)&item->required_anim_state,\s*2\)'),
        reads_lara_anim_word=_has(restore, r'LARA.*ReadSG\(\(char\*\)&item->anim_number,\s*2\)'),
        reads_nonlara_anim_byte=_has(restore, r'ReadSG\(\(char\*\)&byte,\s*1\).*item->anim_number\s*=\s*obj->anim_index\s*\+\s*byte'),
        reads_frame_word=_has(restore, r'ReadSG\(\(char\*\)&item->frame_number,\s*2\)'),
        reads_hitpoints_word=_has(restore, r'0x4000.*ReadSG\(\(char\*\)&item->hit_points,\s*2\)'),
        reads_packed_flags_dword=_has(restore, r'ReadSG\(\(char\*\)&flags,\s*4\)'),
        reads_item_flag_payloads=payload_restore,
        saves_item_flag_payloads=payload_save,
        has_portsave_level_format_gate=_has(restore, r'PortSave_LevelFormat\s*>=\s*4'),
        has_object_specific_payload_reads=_has(restore, r'ReadSG\([^\n]+,\s*24\s*\)') or _has(restore, r'ReadSG\([^\n]+,\s*20\s*\)'),
    )


def _read_field_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _load_re019_comparisons(path: Path | None) -> dict[int, dict[str, str]]:
    if path is None or not path.exists():
        return {}
    out: dict[int, dict[str, str]] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("record_kind") != "save-restore-comparison":
                continue
            group = row.get("save_original_group")
            if group:
                out[int(group)] = row
    return out


def _int_or_none(text: str | None) -> int | None:
    if text in {"", "None", None}:
        return None
    return int(text)


def _field_impl_match(field: str, original_size: int | None, impl: ImplementedRestoreEvidence) -> tuple[bool, str | None, str]:
    """Return (implemented read present, implemented size note, evidence)."""
    if field == "active control header":
        return impl.reads_item_header_word, "2", "implemented restore reads item header word (2 bytes)"
    if field == "item->pos.x_pos packed":
        return impl.reads_packed_pos_xyz, "2", "implemented restore reads packed x/y/z words (2 bytes each)"
    if field == "item->pos.y_pos packed":
        return impl.reads_packed_pos_xyz, "2", "implemented restore reads packed x/y/z words (2 bytes each)"
    if field == "item->pos.z_pos packed":
        return impl.reads_packed_pos_xyz, "2", "implemented restore reads packed x/y/z words (2 bytes each)"
    if field == "item->room_number":
        return impl.reads_room_byte, "1", "implemented restore reads room byte (1 byte)"
    if field == "item->pos.y_rot":
        return impl.reads_y_rot, "2", "implemented restore reads y_rot (2 bytes)"
    if field == "item->pos.x_rot":
        return impl.reads_optional_x_rot, "2", "implemented restore conditionally reads x_rot (2 bytes, header bit)"
    if field == "item->pos.z_rot":
        return impl.reads_optional_z_rot, "2", "implemented restore conditionally reads z_rot (2 bytes, header bit)"
    if field == "item->speed":
        return impl.reads_optional_speed, "2", "implemented restore conditionally reads speed (2 bytes, header bit)"
    if field == "item->fallspeed":
        return impl.reads_optional_fallspeed, "2", "implemented restore conditionally reads fallspeed (2 bytes, header bit)"
    if field in {"item->current_anim_state", "item->goal_anim_state", "item->required_anim_state"}:
        return impl.reads_anim_states_word, "2", "implemented restore reads anim states as words (2 bytes each), matching current save"
    if field == "item->anim_number":
        return impl.reads_lara_anim_word, "2", "implemented restore reads Lara anim_number as word (2 bytes)"
    if field == "item->anim_number - obj->anim_index":
        return impl.reads_nonlara_anim_byte, "1", "implemented restore reads non-Lara anim index delta as byte (1 byte)"
    if field == "item->frame_number":
        return impl.reads_frame_word, "2", "implemented restore reads frame_number (2 bytes)"
    if field == "item->hit_points":
        return impl.reads_hitpoints_word, "2", "implemented restore reads hit_points (2 bytes, header bit)"
    if field == "packed active/status flags":
        return impl.reads_packed_flags_dword, "4", "implemented restore reads packed flags dword (4 bytes) in save_flags path"
    if field in {
        "item->item_flags[0] payload", "item->item_flags[1] payload",
        "item->item_flags[2] payload", "item->item_flags[3] payload",
        "item->timer payload", "item->trigger_flags payload",
    }:
        ev = "implemented restore reads 2-byte payload when header bit set"
        if impl.has_portsave_level_format_gate:
            ev += " (PortSave_LevelFormat >= 4 gate)"
        if impl.saves_item_flag_payloads:
            ev += "; implemented save writes matching payloads"
        return impl.reads_item_flag_payloads, "2", ev
    # object-specific/blocks/sentinels/unknown layout payloads
    if original_size in {20, 24} or "payload block" in field or "object-specific" in field:
        present = impl.has_object_specific_payload_reads
        return present, str(original_size) if present else None, (
            "implemented restore has block-sized reads" if present
            else "no implemented restore read for this object-specific/block payload in active item loop"
        )
    return False, None, "no implemented restore read identified for this hypothesis"


def _classify(
    field: str,
    gap_status: str,
    original_size: int | None,
    restore_function_status: str,
    impl: ImplementedRestoreEvidence,
    re019: dict[str, str] | None,
) -> tuple[str, str, str, str, str]:
    re019_status = (re019 or {}).get("restore_match_status", "no-re019-comparison")
    re019_note = (re019 or {}).get("notes", "")

    if restore_function_status == "source-unimplemented":
        # preserve old behavior shape
        if gap_status == "source-width-mismatch":
            return "restore-width-unverifiable", "blocked", "derive original RestoreLevelData read width before changing source", "no implemented restore", re019_status
        if gap_status == "source-layout-mismatch":
            if original_size in {20, 24} or "block" in field:
                return "needs-original-restore-proof", "blocked", "prove original restore consumes this layout block before changing source", "no implemented restore", re019_status
            return "restore-layout-unverifiable", "blocked", "derive restore-side ordering/layout before changing source", "no implemented restore", re019_status
        if gap_status == "branch-boundary-or-sentinel":
            return "needs-original-restore-proof", "blocked", "locate matching original RestoreLevelData control byte before source changes", "no implemented restore", re019_status
        if gap_status == "source-missing-field":
            if original_size in {4, 20, 24} or "object-specific" in field or "payload block" in field:
                return "needs-original-restore-proof", "blocked", "prove original restore consumes this payload block before implementing writes", "no implemented restore", re019_status
            return "restore-source-absent", "blocked", "RestoreLevelData is unimplemented; add read-side design/proof before serializer patch", "no implemented restore", re019_status
        if gap_status == "exact-field-width-match":
            return "restore-source-absent", "blocked", "RestoreLevelData is unimplemented; exact save-side width alone is insufficient", "no implemented restore", re019_status
        return "needs-original-restore-proof", "blocked", "manual restore-side proof required", "no implemented restore", re019_status

    present, impl_size, evidence = _field_impl_match(field, original_size, impl)
    re019_suffix = f" RE-019={re019_status}." if re019 else ""

    if gap_status == "branch-boundary-or-sentinel":
        return "needs-original-restore-proof", "blocked", "locate matching original RestoreLevelData control byte before source changes", evidence + re019_suffix, re019_status

    if not present:
        status = "needs-original-restore-proof" if original_size in {20, 24} or "object-specific" in field or "payload block" in field else "needs-original-restore-proof"
        action = "prove original restore consumes this payload/field before implementing or changing source"
        if "item_flags" in field and impl.saves_item_flag_payloads:
            evidence += "; current save has payload writes but implemented restore read path for this original group/field identity is unproven"
        return status, "blocked", action, evidence + re019_suffix, re019_status

    # implemented read exists
    if gap_status == "source-width-mismatch":
        if impl_size and original_size is not None and str(original_size) != impl_size:
            action = "implemented restore/save use a different width than RE-017 original hypothesis; prove original restore width before changing source"
            return "implemented-restore-width-differs-from-original-hypothesis", "blocked", action, f"{evidence}; RE-017 original hypothesis size={original_size}" + re019_suffix, re019_status
        return "implemented-restore-present-needs-original-proof", "blocked", "implemented restore reads field, but original width/predicate equivalence remains unproven", evidence + re019_suffix, re019_status

    if gap_status == "source-layout-mismatch":
        return "implemented-restore-layout-differs-from-original-hypothesis", "blocked", "implemented restore order/layout differs from RE-017 original hypothesis; prove original restore layout before changing source", evidence + re019_suffix, re019_status

    if gap_status == "source-missing-field":
        # RE-017 may be stale relative to current implementation (e.g. item flag payloads now present)
        return "implemented-restore-payload-present-needs-original-proof", "blocked", "implemented save/restore contain payload sites, but original restore field identity/predicate/order remains unproven", evidence + re019_suffix, re019_status

    if gap_status == "exact-field-width-match":
        return "implemented-restore-read-present-needs-original-proof", "blocked", "implemented restore read width matches hypothesis, but original restore predicate/ordering/control-flow equivalence remains unproven", evidence + re019_suffix, re019_status

    return "implemented-restore-present-needs-original-proof", "blocked", "manual original restore proof required", evidence + re019_suffix, re019_status


def build_restore_side_audit(
    repo: Path,
    source: Path,
    field_width_csv: Path,
    restore_read_map_csv: Path | None = None,
) -> RestoreSideAudit:
    restore_status = _restore_function_status(source)
    impl = _extract_implemented_evidence(source)
    re019_map = _load_re019_comparisons(restore_read_map_csv)
    rows: list[RestoreSideRow] = []
    for row in _read_field_rows(field_width_csv):
        field = row["probable_source_field"]
        gap_status = row["gap_status"]
        original_size = _int_or_none(row.get("original_size"))
        group = int(row["original_group"])
        status, readiness, action, evidence, re019_status = _classify(
            field, gap_status, original_size, restore_status, impl, re019_map.get(group),
        )
        rows.append(
            RestoreSideRow(
                original_group=group,
                call_ordinal=int(row["call_ordinal"]),
                call_index=int(row["call_index"]),
                call_address=row["call_address"],
                original_size=original_size,
                probable_source_field=field,
                save_gap_status=gap_status,
                restore_side_status=status,
                patch_readiness=readiness,
                next_action=action,
                implemented_evidence=evidence,
                re019_restore_match_status=re019_status,
            )
        )

    counts = dict(Counter(row.restore_side_status for row in rows))
    patch_ready = sum(1 for row in rows if row.patch_readiness == "ready")
    priority = min(
        len(rows),
        sum(1 for row in rows if row.save_gap_status != "exact-field-width-match")
        + sum(1 for row in rows if row.probable_source_field == "active control header")
        + sum(1 for row in rows if row.probable_source_field == "item->room_number" and row.save_gap_status == "source-layout-mismatch"),
    )
    # status remains proof-missing unless fully ready (it should not be)
    overall_status = "restore-side-proof-missing"
    return RestoreSideAudit(
        source=_relative_to_repo(source, repo),
        field_width_csv=_relative_to_repo(field_width_csv, repo),
        restore_read_map_csv=_relative_to_repo(restore_read_map_csv, repo) if restore_read_map_csv and restore_read_map_csv.exists() else None,
        restore_function_status=restore_status,
        total_hypotheses=len(rows),
        priority_hypotheses=priority,
        patch_ready_count=patch_ready,
        restore_status_counts=counts,
        rows=tuple(rows),
        status=overall_status,
    )


def write_csv(audit: RestoreSideAudit, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "original_group", "call_ordinal", "call_index", "call_address", "original_size",
        "probable_source_field", "save_gap_status", "restore_side_status", "patch_readiness",
        "next_action", "implemented_evidence", "re019_restore_match_status",
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
        "- [x] Extract implemented restore read/write evidence from source (best-effort).",
        "- [x] Incorporate RE-019 original restore read-call comparison metadata when available.",
        "- [x] Classify each hypothesis against implemented evidence and original-proof availability.",
        "- [x] Keep outputs metadata-only.",
        "- [x] Preserve marker verdict limits.",
        "",
        "## Inputs",
        "",
        f"- Source: `{audit.source}`",
        f"- RE-017 field-width CSV: `{audit.field_width_csv}`",
        f"- RE-019 restore read-call map CSV: `{audit.restore_read_map_csv}`" if audit.restore_read_map_csv else "- RE-019 restore read-call map CSV: `not found`",
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

    if audit.restore_function_status == "source-unimplemented":
        findings = (
            "Current source `RestoreLevelData` is unimplemented, so RE-017 hypotheses cannot be "
            "promoted to serializer patches from source evidence alone. Byte/word, layout, separate "
            "payload, and object-specific block hypotheses all require restore-side proof first."
        )
    else:
        findings = (
            "Current source `RestoreLevelData` contains read sites. RE-018 now records implemented "
            "read/write evidence and RE-019 original restore comparison metadata where available, but "
            "implemented source symmetry is not proof of original PSX restore equivalence. "
            "RE-017 hypotheses remain blocked for patching unless original restore field identity, "
            "predicates, order, widths, payload semantics, and control flow are proved."
        )
    lines.extend([
        "",
        "## Findings",
        "",
        findings,
        "",
        "Key refresh notes (implemented source, not original equivalence proof):",
        "- Save group 4 anim-state calls 11-13: RE-017 hypothesized 1-byte original writes; implemented restore/save read/write anim states as 2 bytes. Width differs from the RE-017 original hypothesis and still requires original restore proof.",
        "- Save group 5 calls 2-7 (item_flags/timer/trigger payloads): implemented save and restore now contain 2-byte payload sites (restore gated by PortSave_LevelFormat >= 4). RE-017's save-gap status may be stale for current source shape, but original restore predicate/ordering/field identity remains unproven (RE-019: no exact restore size sequence for save group 5).",
        "- Save group 10: RE-019 reports an exact restore size subsequence match for the group size window, but RE-019/RE-022 explicitly state size match is not predicate/layout proof. Implemented restore keeps room before y_rot in the save_position block, while RE-017 flags original room-byte ordering as a layout question.",
        "- Object-specific payload blocks (e.g. 20/24-byte hypotheses) and sentinel/control-byte groups still require original restore proof.",
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
            f"  - RE-019 restore match status: `{row.re019_restore_match_status}`",
            f"  - implemented evidence: {row.implemented_evidence}",
            f"  - next action: {row.next_action}",
        ])

    if audit.restore_function_status == "source-unimplemented":
        verdict = (
            "RE-018 blocks serializer patching from RE-017 alone: current source `RestoreLevelData` "
            "is unimplemented and no restore-side source read sequence can support the field/width "
            "hypotheses yet. Do not add `(F)`, `(D)`, or `(**)` markers."
        )
        next_step = (
            "Next step: extract or reconstruct a metadata-only original `RestoreLevelData` read-call "
            "map, then compare restore read sizes/order against the RE-017 hypotheses before patching "
            "source serialization."
        )
    else:
        verdict = (
            f"RE-018 refresh records restore-side source status `{audit.restore_function_status}` and "
            "implemented read/write evidence. This is stronger context than the original "
            "source-unimplemented state, but it still does not prove original PSX equivalence. "
            "Do not add `(F)`, `(D)`, or `(**)` markers without proof against original restore behavior."
        )
        next_step = (
            "Next step: use RE-019–RE-043 original restore evidence chains for any remaining claims; "
            "RE-043 already reports no safe remaining RestoreLevelData source work in that chain. "
            "Treat this refresh as documentation/context reconciliation, not a new patch gate."
        )
    lines.extend([
        "",
        "## Verdict",
        "",
        verdict,
        "",
        next_step,
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="TOMB5 repo root")
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="source file relative to repo")
    parser.add_argument("--field-width-csv", default=DEFAULT_FIELD_WIDTH_CSV, help="RE-017 CSV relative to repo")
    parser.add_argument("--restore-read-map-csv", default=DEFAULT_RESTORE_READ_MAP_CSV, help="RE-019 CSV relative to repo")
    parser.add_argument("--csv", default=DEFAULT_OUT_CSV, help="versionable CSV output relative to repo")
    parser.add_argument("--md", default=DEFAULT_OUT_MD, help="versionable Markdown output relative to repo")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    audit = build_restore_side_audit(
        repo,
        repo / args.source,
        repo / args.field_width_csv,
        restore_read_map_csv=repo / args.restore_read_map_csv,
    )
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
