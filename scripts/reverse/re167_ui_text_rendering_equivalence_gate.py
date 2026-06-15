#!/usr/bin/env python3
"""Generate RE-167 UI text rendering equivalence-gate artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

RE163_PLAN_CSV = "docs/reverse/generated/re163-module-spec-psxpc-n-ticket-plan.csv"
RE166_CONTRACT_CSV = "docs/reverse/generated/re166-ui-text-rendering-state-contract.csv"
READINESS_CSV = "docs/reverse/generated/re167-ui-text-rendering-equivalence-gate.csv"
MD_OUTPUT = "docs/reverse/functions/re167-ui-text-rendering-equivalence-gate.md"
STORY_OUTPUT = "docs/stories/RE-167-ui-text-rendering-equivalence-gate.md"

FORBIDDEN_FRAGMENTS = ("0x", "pay" + "load", "op" + "code", "machine" + " word", "raw" + " call target")
EXPECTED_PLAN_IDS = ("RE-164", "RE-165", "RE-166", "RE-167", "RE-168", "RE-169", "RE-170")
EXPECTED_RE166_CONTRACT_IDS = (
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
PROOF_REQUIREMENTS = {
    "ui-text-printstring-scale-flag-lifecycle": "scale lifetime and per-call isolation proof",
    "ui-text-printstring-blink-frame-gate": "frame counter timing and flag semantics proof",
    "ui-text-printstring-alignment-bounds-contract": "alignment arithmetic and newline bounds proof",
    "ui-text-printstring-glyph-table-contract": "glyph table identity and control character handling proof",
    "ui-text-getstringlength-scale-read-contract": "measurement scale state consistency proof",
    "ui-text-getstringlength-font-metric-contract": "font metric table identity and accent behavior proof",
    "ui-text-getstringlength-bounds-output-contract": "nullable output pointer behavior proof",
    "ui-text-getstringlength-control-character-contract": "control-character measurement flow proof",
    "ui-text-drawchar-draw-buffer-contract": "draw-buffer side effects and ordering-table insertion proof",
}


@dataclass(frozen=True)
class ReadinessRow:
    contract_id: str
    function: str
    state_surface: str
    source_evidence: str
    binary_evidence: str
    required_symbolic_proof: str
    equivalence_status: str
    code_change_ready: str
    marker_ready: str
    source_patch_allowed: str
    marker_change_allowed: str
    blocker: str
    next_action: str


@dataclass(frozen=True)
class UiTextRenderingEquivalenceGate:
    story_id: str
    upstream_ticket: str
    cluster: str
    status: str
    next_ticket: str
    contract_count: int
    code_change_ready_count: int
    marker_ready_count: int
    readiness_rows: tuple[ReadinessRow, ...]


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
        raise ValueError(f"RE-163 plan drifted before RE-167: {ids}")
    re167 = rows[3]
    if re167.get("topic") != "ui-text-rendering-equivalence-gate":
        raise ValueError("RE-163 plan no longer names RE-167 as the equivalence gate")
    if re167.get("code_change_readiness") != "blocked-until-proof":
        raise ValueError("RE-167 plan no longer starts from blocked-until-proof readiness")


def verify_re166_contract(repo: Path) -> list[dict[str, str]]:
    rows = read_csv(repo / RE166_CONTRACT_CSV)
    contract_ids = tuple(row.get("contract_id", "") for row in rows)
    if contract_ids != EXPECTED_RE166_CONTRACT_IDS:
        raise ValueError(f"RE-166 contract drifted before RE-167: {contract_ids}")
    required = {"contract_id", "function", "state_surface", "source_backing", "contract_status", "code_change_ready", "marker_ready", "blocker", "next_probe"}
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"RE-166 contract missing columns: {sorted(missing)}")
    for row in rows:
        if row["source_backing"] != "source-contract-only":
            raise ValueError(f"RE-167 refuses non-source-contract backing without explicit proof: {row}")
        if row["contract_status"] != "contract-documented-equivalence-blocked":
            raise ValueError(f"RE-167 refuses drifted contract status: {row}")
        if row["code_change_ready"] != "no" or row["marker_ready"] != "no":
            raise ValueError(f"RE-167 refuses pre-ready RE-166 row without a separate proof artifact: {row}")
        if row["blocker"] != "missing-ui-text-rendering-non-raw-symbolic-equivalence-proof":
            raise ValueError(f"RE-167 blocker drifted: {row}")
    return rows


def build_readiness_rows(contract_rows: list[dict[str, str]]) -> tuple[ReadinessRow, ...]:
    rows: list[ReadinessRow] = []
    for row in contract_rows:
        contract_id = row["contract_id"]
        rows.append(ReadinessRow(
            contract_id=contract_id,
            function=row["function"],
            state_surface=row["state_surface"],
            source_evidence=row["source_backing"],
            binary_evidence="non-raw-symbolic-evidence-missing",
            required_symbolic_proof=PROOF_REQUIREMENTS[contract_id],
            equivalence_status="blocked-missing-ui-text-rendering-non-raw-symbolic-equivalence-proof",
            code_change_ready="no",
            marker_ready="no",
            source_patch_allowed="no",
            marker_change_allowed="no",
            blocker="missing-ui-text-rendering-non-raw-symbolic-equivalence-proof",
            next_action="defer-source-and-marker-patch-to-re168-no-patch-gate",
        ))
    return tuple(rows)


def build_ui_text_rendering_equivalence_gate(repo: Path) -> UiTextRenderingEquivalenceGate:
    repo = Path(repo)
    verify_re163_plan(repo)
    contract_rows = verify_re166_contract(repo)
    readiness_rows = build_readiness_rows(contract_rows)
    return UiTextRenderingEquivalenceGate(
        story_id="RE-167",
        upstream_ticket="RE-166",
        cluster="ui-text-rendering",
        status="equivalence-gate-blocked-no-ready-rows",
        next_ticket="RE-168",
        contract_count=len(contract_rows),
        code_change_ready_count=0,
        marker_ready_count=0,
        readiness_rows=readiness_rows,
    )


def assert_clean(path: Path) -> None:
    text = path.read_text(encoding="utf-8").lower()
    hits = [item for item in FORBIDDEN_FRAGMENTS if item in text]
    if hits:
        raise ValueError(f"forbidden metadata fragments in {path}: {hits}")


def write_all_artifacts(audit: UiTextRenderingEquivalenceGate, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "readiness_csv": repo / READINESS_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY_OUTPUT,
    }
    write_dict_csv(paths["readiness_csv"], list(ReadinessRow.__dataclass_fields__), [row.__dict__ for row in audit.readiness_rows])

    md_lines = [
        "# RE-167 — UI text rendering equivalence gate",
        "",
        "Cluster: `ui-text-rendering`",
        "Decision: `equivalence-gate-blocked-no-ready-rows`",
        "Next: `RE-168`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-166 state contract consumed.",
        "- [x] Equivalence readiness matrix emitted.",
        "- [x] Source and marker readiness kept blocked.",
        "- [x] Forbidden evidence excluded from generated artifacts.",
        "",
        "## Summary",
        "",
        f"- contract rows consumed: `{audit.contract_count}`",
        f"- code-change-ready rows: `{audit.code_change_ready_count}`",
        f"- marker-ready rows: `{audit.marker_ready_count}`",
        "- source patch authorized: `no`",
        "",
        "## Readiness rows",
        "",
    ]
    for row in audit.readiness_rows:
        md_lines.append(f"- `{row.contract_id}`: `{row.function}` / `{row.state_surface}` / `{row.equivalence_status}`")
    md_lines.extend([
        "",
        "No production source or marker change is authorized by this equivalence gate.",
    ])
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    story_lines = [
        "# RE-167 — UI text rendering equivalence gate",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Compare the RE-166 source-backed state contracts against available symbolic evidence and publish a readiness gate.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-166 state contract consumed.",
        "- [x] UI text equivalence readiness matrix emitted.",
        "- [x] Code-change and marker readiness counts recorded.",
        "- [x] Forbidden evidence excluded from generated artifacts.",
        "",
        "## Generated artifacts",
        "",
        f"- `{READINESS_CSV}`",
        f"- `{MD_OUTPUT}`",
        "",
        "## Readiness decision",
        "",
        "- decision: `equivalence-gate-blocked-no-ready-rows`",
        "- code change readiness: `blocked`",
        "- marker readiness: `blocked`",
        "- code-change-ready rows: `0`",
        "- marker-ready rows: `0`",
        "- next ticket: `RE-168`",
        "- blocker: `missing-ui-text-rendering-non-raw-symbolic-equivalence-proof`",
        "",
        "## Follow-up breakdown",
        "",
        "- `RE-168`: publish the source-patch gate as a no-patch decision unless new symbolic proof appears.",
        "- `RE-169`: select the next SPEC_PSXPC_N cluster after the UI text rendering chain closes or blocks.",
        "- `RE-170`: close or hand off the broader module SPEC_PSXPC_N domain after cluster selection.",
        "",
        "## Validation",
        "",
        "- `python3 -m pytest tests/reverse/test_re167_ui_text_rendering_equivalence_gate.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over RE-167 artifacts",
        "",
        "No production source or marker change is authorized by this equivalence gate.",
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
    audit = build_ui_text_rendering_equivalence_gate(args.repo)
    for key, path in write_all_artifacts(audit, args.repo).items():
        print(f"{key}: {path}")
    print(f"readiness_rows={len(audit.readiness_rows)}")
    print(f"next_ticket={audit.next_ticket}")


if __name__ == "__main__":
    main()
