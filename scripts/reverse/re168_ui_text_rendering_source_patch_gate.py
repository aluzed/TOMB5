#!/usr/bin/env python3
"""Generate RE-168 UI text rendering source-patch/no-patch gate artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

RE163_PLAN_CSV = "docs/reverse/generated/re163-module-spec-psxpc-n-ticket-plan.csv"
RE167_READINESS_CSV = "docs/reverse/generated/re167-ui-text-rendering-equivalence-gate.csv"
PATCH_CSV = "docs/reverse/generated/re168-ui-text-rendering-source-patch-gate.csv"
HANDOFF_CSV = "docs/reverse/generated/re168-ui-text-rendering-source-patch-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re168-ui-text-rendering-source-patch-gate.md"
STORY_OUTPUT = "docs/stories/RE-168-ui-text-rendering-source-patch-gate.md"

FORBIDDEN_FRAGMENTS = ("0x", "pay" + "load", "op" + "code", "machine" + " word", "raw" + " call target")
EXPECTED_PLAN_IDS = ("RE-164", "RE-165", "RE-166", "RE-167", "RE-168", "RE-169", "RE-170")
EXPECTED_RE167_CONTRACT_IDS = (
    "ui-text-printstring-scale-flag-lifecycle",
    "ui-text-printstring-blink-frame-gate",
    "ui-text-printstring-alignment-bounds-contract",
    "ui-text-printstring-glyph-table-contract",
    "ui-text-getstringlength-scale-read-contract",
    "ui-text-getstringlength-font-metric-contract",
    "ui-text-getstringlength-bounds-output-contract",
    "ui-text-getstringlength-control-character-contract",
    "ui-text-drawchar-draw-buffer-contract",
)


@dataclass(frozen=True)
class PatchGateRow:
    contract_id: str
    function: str
    state_surface: str
    required_symbolic_proof: str
    upstream_equivalence_status: str
    patch_gate_status: str
    source_patch_decision: str
    marker_change_decision: str
    production_source_modified: str
    marker_modified: str
    stop_reason: str
    blocker: str
    next_action: str


@dataclass(frozen=True)
class HandoffRow:
    next_ticket: str
    next_topic: str
    current_cluster: str
    outcome: str
    reason: str
    dependency: str
    stop_condition: str


@dataclass(frozen=True)
class UiTextRenderingSourcePatchGate:
    story_id: str
    upstream_ticket: str
    cluster: str
    final_decision: str
    next_ticket: str
    readiness_row_count: int
    source_patch_allowed_count: int
    marker_change_allowed_count: int
    patch_rows: tuple[PatchGateRow, ...]
    handoff: HandoffRow


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_dict_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def verify_re163_plan(repo: Path) -> None:
    rows = read_csv(repo / RE163_PLAN_CSV)
    ids = tuple(row.get("story_id", "") for row in rows)
    if ids != EXPECTED_PLAN_IDS:
        raise ValueError(f"RE-163 plan drifted before RE-168: {ids}")
    re168 = rows[4]
    if re168.get("topic") != "ui-text-rendering-source-patch-gate":
        raise ValueError("RE-163 plan no longer names RE-168 as the source-patch gate")
    if re168.get("code_change_readiness") != "blocked-until-proof":
        raise ValueError("RE-168 plan no longer starts from blocked-until-proof readiness")


def verify_re167_readiness(repo: Path) -> list[dict[str, str]]:
    rows = read_csv(repo / RE167_READINESS_CSV)
    ids = tuple(row.get("contract_id", "") for row in rows)
    if ids != EXPECTED_RE167_CONTRACT_IDS:
        raise ValueError(f"RE-167 readiness rows drifted before RE-168: {ids}")
    required = {
        "contract_id", "function", "state_surface", "binary_evidence", "required_symbolic_proof",
        "equivalence_status", "code_change_ready", "marker_ready", "source_patch_allowed",
        "marker_change_allowed", "blocker", "next_action",
    }
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"RE-167 readiness missing columns: {sorted(missing)}")
    for row in rows:
        if row["binary_evidence"] != "non-raw-symbolic-evidence-missing":
            raise ValueError(f"RE-168 refuses unexpected proof evidence without a new patch test: {row}")
        if row["equivalence_status"] != "blocked-missing-ui-text-rendering-non-raw-symbolic-equivalence-proof":
            raise ValueError(f"RE-168 refuses drifted equivalence status: {row}")
        for field in ("code_change_ready", "marker_ready", "source_patch_allowed", "marker_change_allowed"):
            if row[field] != "no":
                raise ValueError(f"RE-168 refuses ready row without a patch-ready test: {field} {row}")
        if row["blocker"] != "missing-ui-text-rendering-non-raw-symbolic-equivalence-proof":
            raise ValueError(f"RE-168 blocker drifted: {row}")
    return rows


def build_patch_rows(readiness_rows: list[dict[str, str]]) -> tuple[PatchGateRow, ...]:
    rows: list[PatchGateRow] = []
    for row in readiness_rows:
        rows.append(PatchGateRow(
            contract_id=row["contract_id"],
            function=row["function"],
            state_surface=row["state_surface"],
            required_symbolic_proof=row["required_symbolic_proof"],
            upstream_equivalence_status=row["equivalence_status"],
            patch_gate_status="blocked-by-missing-equivalence-proof",
            source_patch_decision="denied",
            marker_change_decision="denied",
            production_source_modified="no",
            marker_modified="no",
            stop_reason="no-re167-ready-row",
            blocker=row["blocker"],
            next_action="handoff-to-re169-next-cluster-selection",
        ))
    return tuple(rows)


def build_handoff() -> HandoffRow:
    return HandoffRow(
        next_ticket="RE-169",
        next_topic="module-spec-psxpc-n-next-cluster-selection",
        current_cluster="ui-text-rendering",
        outcome="ui-text-rendering-source-patch-denied",
        reason="RE-167 produced zero source-patch-ready or marker-ready rows",
        dependency="RE-168 no-patch gate",
        stop_condition="next SPEC_PSXPC_N cluster selected or module handoff emitted",
    )


def build_ui_text_rendering_source_patch_gate(repo: Path) -> UiTextRenderingSourcePatchGate:
    repo = Path(repo)
    verify_re163_plan(repo)
    readiness_rows = verify_re167_readiness(repo)
    patch_rows = build_patch_rows(readiness_rows)
    return UiTextRenderingSourcePatchGate(
        story_id="RE-168",
        upstream_ticket="RE-167",
        cluster="ui-text-rendering",
        final_decision="source-and-marker-patch-denied-no-ready-rows",
        next_ticket="RE-169",
        readiness_row_count=len(readiness_rows),
        source_patch_allowed_count=0,
        marker_change_allowed_count=0,
        patch_rows=patch_rows,
        handoff=build_handoff(),
    )


def assert_clean(path: Path) -> None:
    text = path.read_text(encoding="utf-8").lower()
    hits = [item for item in FORBIDDEN_FRAGMENTS if item in text]
    if hits:
        raise ValueError(f"forbidden metadata fragments in {path}: {hits}")


def write_all_artifacts(gate: UiTextRenderingSourcePatchGate, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "patch_csv": repo / PATCH_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY_OUTPUT,
    }
    write_dict_csv(paths["patch_csv"], list(PatchGateRow.__dataclass_fields__), [row.__dict__ for row in gate.patch_rows])
    write_dict_csv(paths["handoff_csv"], list(HandoffRow.__dataclass_fields__), [gate.handoff.__dict__])

    md_lines = [
        "# RE-168 — UI text rendering source-patch gate",
        "",
        "Cluster: `ui-text-rendering`",
        f"Decision: `{gate.final_decision}`",
        "Next: `RE-169`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-167 readiness gate consumed.",
        "- [x] No-patch source gate emitted.",
        "- [x] Source and marker modifications denied.",
        "- [x] RE-169 handoff emitted.",
        "- [x] Forbidden evidence excluded from generated artifacts.",
        "",
        "## Summary",
        "",
        f"- readiness rows consumed: `{gate.readiness_row_count}`",
        f"- source-patch-ready rows: `{gate.source_patch_allowed_count}`",
        f"- marker-ready rows: `{gate.marker_change_allowed_count}`",
        "- production source modified: `no`",
        "- marker modified: `no`",
        "",
        "## Patch gate rows",
        "",
    ]
    for row in gate.patch_rows:
        md_lines.append(f"- `{row.contract_id}`: `{row.function}` / `{row.patch_gate_status}` / source patch `{row.source_patch_decision}` / marker `{row.marker_change_decision}`")
    md_lines.extend([
        "",
        "No production source or marker change was made by this gate.",
    ])
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    story_lines = [
        "# RE-168 — UI text rendering source-patch gate",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Apply a minimal source or marker patch only if RE-167 marks rows ready; otherwise publish a no-patch gate.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-167 readiness gate consumed.",
        "- [x] No-patch source gate emitted.",
        "- [x] Source patch and marker change decisions recorded.",
        "- [x] RE-169 handoff emitted.",
        "- [x] Forbidden evidence excluded from generated artifacts.",
        "",
        "## Generated artifacts",
        "",
        f"- `{PATCH_CSV}`",
        f"- `{HANDOFF_CSV}`",
        f"- `{MD_OUTPUT}`",
        "",
        "## Readiness decision",
        "",
        f"- decision: `{gate.final_decision}`",
        "- source patch readiness: `blocked`",
        "- marker change readiness: `blocked`",
        "- source-patch-ready rows: `0`",
        "- marker-ready rows: `0`",
        "- next ticket: `RE-169`",
        "- blocker: `missing-ui-text-rendering-non-raw-symbolic-equivalence-proof`",
        "",
        "## Follow-up breakdown",
        "",
        "- `RE-169`: select the next SPEC_PSXPC_N cluster after this UI text rendering no-patch gate.",
        "- `RE-170`: close or hand off the broader module SPEC_PSXPC_N domain after cluster selection.",
        "",
        "## Validation",
        "",
        "- `python3 -m pytest tests/reverse/test_re168_ui_text_rendering_source_patch_gate.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over RE-168 artifacts",
        "",
        "No production source or marker change was made by this gate.",
        "",
    ]
    paths["story"].parent.mkdir(parents=True, exist_ok=True)
    paths["story"].write_text("\n".join(story_lines), encoding="utf-8")

    for path in paths.values():
        assert_clean(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    gate = build_ui_text_rendering_source_patch_gate(args.repo)
    for key, path in write_all_artifacts(gate, args.repo).items():
        print(f"{key}: {path}")
    print(f"patch_gate_rows={len(gate.patch_rows)}")
    print(f"next_ticket={gate.next_ticket}")


if __name__ == "__main__":
    main()
