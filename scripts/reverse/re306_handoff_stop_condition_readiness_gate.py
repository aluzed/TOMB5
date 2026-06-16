#!/usr/bin/env python3
"""Generate RE-306 handoff stop-condition readiness gate artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE305_HANDOFF = "docs/reverse/generated/re305-handoff-stop-condition-reduction-handoff.csv"
RE305_TAXONOMY = "docs/reverse/generated/re305-handoff-stop-condition-reduction.csv"
RE305_EVIDENCE = "docs/reverse/generated/re305-handoff-stop-condition-reduction-evidence.csv"
RE296_CANDIDATES = "docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv"

GATE_CSV = "docs/reverse/generated/re306-handoff-stop-condition-readiness-gate.csv"
SUMMARY_CSV = "docs/reverse/generated/re306-handoff-stop-condition-readiness-gate-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re306-handoff-stop-condition-readiness-gate-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re306-handoff-stop-condition-readiness-gate.md"
STORY = "docs/stories/RE-306-handoff-stop-condition-readiness-gate.md"

FORBIDDEN = (
    "word_le_hex",
    "payload_offset",
    "dump row",
    "opcode",
    "machine word",
    "call_address",
    "branch target",
    "call target",
    "hex-address-fragment",
    "stop_condition_text",
)

NEXT_SOURCE = "blocker-reduction-source-exhaustion-audit"
NEXT_TICKET = "RE-307"
NEXT_TOPIC = "blocker-reduction-source-exhaustion-audit"


@dataclass(frozen=True)
class ReadinessGateRow:
    normalized_class: str
    evidence_count: int
    handoff_file_count: int
    unique_stop_condition_count: int
    gate_decision: str
    readiness_reason: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    next_metadata_source: str
    next_ticket: str
    next_topic: str


@dataclass(frozen=True)
class ReadinessGateSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    handoff_stop_condition_class_count: int
    gate_row_count: int
    ready_to_reopen_domain_count: int
    needs_new_evidence_count: int
    source_patch_authorized_count: int
    raw_or_asset_source_count: int
    next_ticket: str
    next_topic: str
    selected_domain: str
    selected_pivot: str
    metadata_work_readiness: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class ReadinessGateBundle:
    rows: list[ReadinessGateRow]
    summary: ReadinessGateSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_re305_handoff(repo: Path) -> None:
    rows = read_csv(repo / RE305_HANDOFF)
    if len(rows) != 1:
        raise ValueError("RE-305 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "story_id": "RE-305",
        "next_ticket": "RE-306",
        "next_topic": "handoff-stop-condition-readiness-gate",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
        "domain_selection_ready_count": "0",
        "source_patch_authorized_count": "0",
        "raw_or_asset_source_count": "0",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-305 handoff drift: {key}={row.get(key)!r}")


def validate_re296_handoff_candidate(repo: Path) -> None:
    rows = read_csv(repo / RE296_CANDIDATES)
    matches = [row for row in rows if row["source_id"] == "handoff-csvs"]
    if len(matches) != 1:
        raise ValueError("RE-296 handoff-csvs candidate must contain exactly one row")
    row = matches[0]
    expected = {
        "selection_status": "candidate",
        "next_topic": "handoff-stop-condition-reduction",
        "metadata_candidate_ready": "yes",
        "domain_selection_ready": "no",
        "source_patch_authorized": "no",
        "raw_or_asset_dependency": "no",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-296 handoff-csvs candidate drift: {key}={row.get(key)!r}")


def validate_evidence_metadata_only(repo: Path) -> None:
    rows = read_csv(repo / RE305_EVIDENCE)
    if not rows:
        raise ValueError("RE-305 evidence must not be empty")
    required = {"handoff_file", "row_number", "source_field", "normalized_class", "stop_condition_fingerprint"}
    if set(rows[0]) != required:
        raise ValueError(f"RE-305 evidence schema drift: {set(rows[0])!r}")
    forbidden_columns = {"stop_condition_text", "reason_text", "blocker_text", "source_text", "raw_text"}
    if forbidden_columns & set(rows[0]):
        raise ValueError("RE-305 evidence leaked raw stop-condition columns")


def gate_decision_for_class(normalized_class: str) -> str:
    if normalized_class == "upstream-input-refresh-or-change-needed":
        return "needs-upstream-input-change"
    return "needs-new-non-raw-proof-evidence"


def reason_for_class(row: dict[str, str]) -> str:
    cls = row["normalized_class"]
    if cls == "proof-blocked-or-no-marker-patch":
        return "handoff stop conditions still end in proof blockers or no-marker/no-source-patch states"
    if cls == "metadata-reduction-before-domain-selection":
        return "handoff stop conditions request more metadata reduction before domain selection, not a ready domain"
    if cls == "generic-handoff-stop-condition":
        return "generic handoff stop conditions need exhaustion audit rather than domain selection"
    if cls == "upstream-input-refresh-or-change-needed":
        return "upstream inputs or new non-raw evidence must change before any proof domain can reopen"
    if cls == "readiness-gate-before-domain-selection":
        return "readiness gates remain prerequisites and do not themselves authorize source or marker changes"
    return "handoff stop-condition taxonomy is not sufficient to reopen proof-domain selection"


def build_rows(repo: Path) -> list[ReadinessGateRow]:
    taxonomy = read_csv(repo / RE305_TAXONOMY)
    if len(taxonomy) != 5:
        raise ValueError(f"RE-305 taxonomy drift: expected 5 rows, got {len(taxonomy)}")
    rows: list[ReadinessGateRow] = []
    for row in taxonomy:
        if row["metadata_reduction_ready"] != "yes":
            raise ValueError(f"taxonomy row not metadata-ready: {row['normalized_class']}")
        if row["domain_selection_ready"] != "no" or row["source_patch_authorized"] != "no":
            raise ValueError(f"taxonomy row unexpectedly ready: {row['normalized_class']}")
        rows.append(
            ReadinessGateRow(
                normalized_class=row["normalized_class"],
                evidence_count=int(row["evidence_count"]),
                handoff_file_count=int(row["handoff_file_count"]),
                unique_stop_condition_count=int(row["unique_stop_condition_count"]),
                gate_decision=gate_decision_for_class(row["normalized_class"]),
                readiness_reason=reason_for_class(row),
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                next_metadata_source=NEXT_SOURCE,
                next_ticket=NEXT_TICKET,
                next_topic=NEXT_TOPIC,
            )
        )
    return sorted(rows, key=lambda row: (-row.evidence_count, row.normalized_class))


def build_handoff_stop_condition_readiness_gate(repo: Path) -> ReadinessGateBundle:
    repo = Path(repo)
    validate_re305_handoff(repo)
    validate_re296_handoff_candidate(repo)
    validate_evidence_metadata_only(repo)
    rows = build_rows(repo)
    summary = ReadinessGateSummary(
        story_id="RE-306",
        topic="handoff-stop-condition-readiness-gate",
        upstream_handoff="RE-305",
        handoff_stop_condition_class_count=len(rows),
        gate_row_count=len(rows),
        ready_to_reopen_domain_count=sum(1 for row in rows if row.ready_to_reopen_domain == "yes"),
        needs_new_evidence_count=sum(1 for row in rows if row.gate_decision.startswith("needs-")),
        source_patch_authorized_count=sum(1 for row in rows if row.source_patch_authorized == "yes"),
        raw_or_asset_source_count=0,
        next_ticket=NEXT_TICKET,
        next_topic=NEXT_TOPIC,
        selected_domain="none",
        selected_pivot="none",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="audit blocker-reduction metadata source exhaustion before selecting another proof domain",
    )
    return ReadinessGateBundle(rows=rows, summary=summary)


def write_rows(path: Path, rows: list[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("rows required")
    names = [field.name for field in fields(rows[0])]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=names, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_markdown(path: Path, bundle: ReadinessGateBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-306 handoff stop-condition readiness gate",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-305 handoff stop-condition reduction handoff validated.",
        "- [x] RE-305 fingerprint-only evidence schema checked.",
        "- [x] Handoff stop-condition classes gated for proof-domain reopen readiness.",
        "- [x] Proof-domain selection kept blocked pending blocker-reduction source exhaustion audit.",
        "",
        "## Gate decision",
        "",
        f"- Handoff stop-condition classes gated: `{s.handoff_stop_condition_class_count}`",
        f"- Ready to reopen proof-domain selection: `{s.ready_to_reopen_domain_count}`",
        f"- Classes needing new evidence/input changes: `{s.needs_new_evidence_count}`",
        f"- Source patch authorized rows: `{s.source_patch_authorized_count}`",
        f"- Next metadata source: `{NEXT_SOURCE}`",
        f"- Next topic: `{s.next_topic}`",
        "",
        "Handoff stop-condition classes do not reopen proof-domain selection. They consolidate prior stop reasons, but they do not provide new non-raw proof evidence, changed upstream mapping, a selected domain, or source authorization.",
        "",
        "## Gate rows",
        "",
    ]
    for row in bundle.rows:
        lines.extend(
            [
                f"### `{row.normalized_class}`",
                "",
                f"- Evidence rows: `{row.evidence_count}`",
                f"- Handoff files: `{row.handoff_file_count}`",
                f"- Unique stop-condition fingerprints: `{row.unique_stop_condition_count}`",
                f"- Gate decision: `{row.gate_decision}`",
                f"- Reason: {row.readiness_reason}",
                f"- Ready to reopen domain: `{row.ready_to_reopen_domain}`",
                f"- Source patch authorized: `{row.source_patch_authorized}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Readiness decision",
            "",
            "No production source or marker change is authorized by this gate.",
            "The next safe step is to audit exhaustion of the blocker-reduction metadata sources before selecting another proof domain.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story(path: Path, bundle: ReadinessGateBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-306 handoff stop-condition readiness gate",
        "",
        "## Goal",
        "",
        "Gate the RE-305 handoff stop-condition taxonomy to decide whether proof-domain selection can reopen.",
        "",
        "## Inputs",
        "",
        f"- Upstream handoff: `{RE305_HANDOFF}`",
        f"- Taxonomy: `{RE305_TAXONOMY}`",
        f"- Evidence: `{RE305_EVIDENCE}`",
        f"- Candidate source: `{RE296_CANDIDATES}` / `handoff-csvs`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-305 handoff stop-condition reduction handoff validated.",
        "- [x] RE-305 taxonomy readiness flags verified as metadata-only/non-authorizing.",
        "- [x] RE-305 evidence schema verified as fingerprint-only.",
        "- [x] Readiness gate CSV, summary, handoff, Markdown, and story generated.",
        "- [x] Source/code readiness remains blocked.",
        "",
        "## Generated artifacts",
        "",
        f"- `{GATE_CSV}`",
        f"- `{SUMMARY_CSV}`",
        f"- `{HANDOFF_CSV}`",
        f"- `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- Handoff stop-condition classes gated: `{s.handoff_stop_condition_class_count}`",
        f"- Ready to reopen proof-domain selection: `{s.ready_to_reopen_domain_count}`",
        f"- Classes needing new evidence/input changes: `{s.needs_new_evidence_count}`",
        f"- Source patch authorized rows: `{s.source_patch_authorized_count}`",
        "",
    ]
    for row in bundle.rows:
        lines.append(f"- `{row.normalized_class}`: `{row.gate_decision}`, evidence `{row.evidence_count}`.")
    lines.extend(
        [
            "",
            "## Readiness decision",
            "",
            "The handoff stop-condition taxonomy is not proof-domain-selection-ready. It points to new non-raw proof evidence, changed upstream inputs, or a source-exhaustion audit rather than a safe source/marker patch.",
            "",
            "## Follow-up ticket breakdown",
            "",
            f"- `{s.next_ticket}` / `{s.next_topic}`: audit whether all blocker-reduction metadata sources from RE-296 have been reduced/gated and whether any safe source remains before another proof-domain selection attempt.",
            "  - Inputs: RE-296 candidate list and RE-297..RE-306 reduction/gate handoffs.",
            "  - Deliverables: exhaustion matrix, summary, handoff, generated Markdown, and story tracker.",
            "  - Stop condition: if no safe metadata source or non-raw proof evidence remains, keep selected domain/pivot `none` and request changed upstream mapping or new non-raw evidence.",
            "",
            "## Validation commands",
            "",
            "- `python -m pytest tests/reverse/test_re306_handoff_stop_condition_readiness_gate.py -q`",
            "- `python scripts/reverse/re306_handoff_stop_condition_readiness_gate.py --repo .`",
            "- `python -m pytest tests/reverse -q`",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_all_artifacts(bundle: ReadinessGateBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "gate_csv": repo / GATE_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_rows(paths["gate_csv"], bundle.rows)
    write_rows(paths["summary_csv"], [bundle.summary])
    write_rows(paths["handoff_csv"], [bundle.summary])
    write_markdown(paths["md"], bundle)
    write_story(paths["story"], bundle)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    bundle = build_handoff_stop_condition_readiness_gate(args.repo)
    written = write_all_artifacts(bundle, args.repo)
    for key, path in written.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
