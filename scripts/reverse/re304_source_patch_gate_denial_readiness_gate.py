#!/usr/bin/env python3
"""Generate RE-304 source-patch gate denial readiness gate artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE303_HANDOFF = "docs/reverse/generated/re303-source-patch-gate-denial-reduction-handoff.csv"
RE303_TAXONOMY = "docs/reverse/generated/re303-source-patch-gate-denial-reduction.csv"
RE303_EVIDENCE = "docs/reverse/generated/re303-source-patch-gate-denial-reduction-evidence.csv"
RE296_CANDIDATES = "docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv"

GATE_CSV = "docs/reverse/generated/re304-source-patch-gate-denial-readiness-gate.csv"
SUMMARY_CSV = "docs/reverse/generated/re304-source-patch-gate-denial-readiness-gate-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re304-source-patch-gate-denial-readiness-gate-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re304-source-patch-gate-denial-readiness-gate.md"
STORY = "docs/stories/RE-304-source-patch-gate-denial-readiness-gate.md"

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
)

NEXT_SOURCE = "handoff-csvs"
NEXT_TICKET = "RE-305"
NEXT_TOPIC = "handoff-stop-condition-reduction"


@dataclass(frozen=True)
class ReadinessGateRow:
    normalized_class: str
    evidence_count: int
    source_patch_gate_file_count: int
    unique_denial_count: int
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
    source_patch_denial_class_count: int
    gate_row_count: int
    ready_to_reopen_domain_count: int
    needs_more_metadata_count: int
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


def validate_re303_handoff(repo: Path) -> None:
    rows = read_csv(repo / RE303_HANDOFF)
    if len(rows) != 1:
        raise ValueError("RE-303 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "story_id": "RE-303",
        "next_ticket": "RE-304",
        "next_topic": "source-patch-gate-denial-readiness-gate",
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
            raise ValueError(f"RE-303 handoff drift: {key}={row.get(key)!r}")


def validate_re296_next_candidate(repo: Path) -> None:
    rows = read_csv(repo / RE296_CANDIDATES)
    matches = [row for row in rows if row["source_id"] == NEXT_SOURCE]
    if len(matches) != 1:
        raise ValueError("RE-296 handoff-csvs candidate must contain exactly one row")
    row = matches[0]
    expected = {
        "selection_status": "candidate",
        "next_topic": NEXT_TOPIC,
        "metadata_candidate_ready": "yes",
        "domain_selection_ready": "no",
        "source_patch_authorized": "no",
        "raw_or_asset_dependency": "no",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-296 handoff-csvs candidate drift: {key}={row.get(key)!r}")


def validate_evidence_metadata_only(repo: Path) -> None:
    rows = read_csv(repo / RE303_EVIDENCE)
    if not rows:
        raise ValueError("RE-303 evidence must not be empty")
    required = {"source_patch_gate_file", "row_number", "normalized_class", "denial_fingerprint"}
    if set(rows[0]) != required:
        raise ValueError(f"RE-303 evidence schema drift: {set(rows[0])!r}")
    forbidden_columns = {"denial_text", "blocker_text", "source_text", "raw_text"}
    if forbidden_columns & set(rows[0]):
        raise ValueError("RE-303 evidence leaked raw denial columns")


def reason_for_class(row: dict[str, str]) -> str:
    cls = row["normalized_class"]
    if cls == "non-raw-equivalence-proof-missing":
        return "source-patch denials still require non-raw equivalence proof before any domain can reopen"
    if cls == "upstream-gate-zero-ready":
        return "source-patch gates inherit zero-ready upstream decisions rather than creating patch authorization"
    if cls == "symbolic-equivalence-proof-missing":
        return "source-patch denials still require symbolic equivalence proof before marker or source work"
    if cls == "state-contract-and-non-raw-equivalence-missing":
        return "state contracts and non-raw equivalence are still missing from denied source-patch paths"
    if cls == "source-contract-and-non-raw-equivalence-missing":
        return "source contracts and non-raw equivalence are still missing from denied source-patch paths"
    return "source-patch denial taxonomy is not sufficient to reopen proof-domain selection"


def build_rows(repo: Path) -> list[ReadinessGateRow]:
    taxonomy = read_csv(repo / RE303_TAXONOMY)
    if len(taxonomy) != 5:
        raise ValueError(f"RE-303 taxonomy drift: expected 5 rows, got {len(taxonomy)}")
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
                source_patch_gate_file_count=int(row["source_patch_gate_file_count"]),
                unique_denial_count=int(row["unique_denial_count"]),
                gate_decision="needs-handoff-stop-condition-metadata",
                readiness_reason=reason_for_class(row),
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                next_metadata_source=NEXT_SOURCE,
                next_ticket=NEXT_TICKET,
                next_topic=NEXT_TOPIC,
            )
        )
    return sorted(rows, key=lambda row: (-row.evidence_count, row.normalized_class))


def build_readiness_gate(repo: Path) -> ReadinessGateBundle:
    repo = Path(repo)
    validate_re303_handoff(repo)
    validate_re296_next_candidate(repo)
    validate_evidence_metadata_only(repo)
    rows = build_rows(repo)
    summary = ReadinessGateSummary(
        story_id="RE-304",
        topic="source-patch-gate-denial-readiness-gate",
        upstream_handoff="RE-303",
        source_patch_denial_class_count=len(rows),
        gate_row_count=len(rows),
        ready_to_reopen_domain_count=sum(1 for row in rows if row.ready_to_reopen_domain == "yes"),
        needs_more_metadata_count=sum(1 for row in rows if row.gate_decision == "needs-handoff-stop-condition-metadata"),
        source_patch_authorized_count=sum(1 for row in rows if row.source_patch_authorized == "yes"),
        raw_or_asset_source_count=0,
        next_ticket=NEXT_TICKET,
        next_topic=NEXT_TOPIC,
        selected_domain="none",
        selected_pivot="none",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="reduce handoff stop conditions before proof-domain selection can reopen",
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
        "# RE-304 source-patch gate denial readiness gate",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-303 source-patch denial taxonomy handoff validated.",
        "- [x] RE-303 evidence schema checked for metadata-only fingerprints.",
        "- [x] Source-patch denial taxonomy gated for proof-domain reopen readiness.",
        "- [x] Proof-domain selection kept blocked pending handoff stop-condition reduction.",
        "",
        "## Gate decision",
        "",
        f"- Source-patch denial classes gated: `{s.source_patch_denial_class_count}`",
        f"- Ready to reopen proof-domain selection: `{s.ready_to_reopen_domain_count}`",
        f"- Classes needing more metadata: `{s.needs_more_metadata_count}`",
        f"- Source patch authorized rows: `{s.source_patch_authorized_count}`",
        f"- Next metadata source: `{NEXT_SOURCE}`",
        f"- Next topic: `{s.next_topic}`",
        "",
        "Source-patch denial blockers confirm why source/marker work is denied, but they do not identify a safe domain/pivot. handoff stop conditions are the next safe metadata source.",
        "",
        "## Gate rows",
        "",
    ]
    for row in bundle.rows:
        lines.extend(
            [
                f"### {row.normalized_class}",
                "",
                f"- Evidence count: `{row.evidence_count}`",
                f"- Source-patch gate files: `{row.source_patch_gate_file_count}`",
                f"- Unique denials: `{row.unique_denial_count}`",
                f"- Decision: `{row.gate_decision}`",
                f"- Reason: {row.readiness_reason}.",
                f"- Ready to reopen domain: `{row.ready_to_reopen_domain}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Readiness",
            "",
            f"- Metadata work readiness: `{s.metadata_work_readiness}`",
            f"- Code/source readiness: `{s.code_change_readiness}`",
            f"- Next ticket: `{s.next_ticket}`",
            f"- Next topic: `{s.next_topic}`",
            f"- Selected domain: `{s.selected_domain}`",
            f"- Selected pivot: `{s.selected_pivot}`",
            f"- Stop condition: `{s.stop_condition}`",
            "",
            "No production source or marker change is authorized by this gate.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story(path: Path, bundle: ReadinessGateBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-304 — source-patch gate denial readiness gate",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Gate the source-patch denial taxonomy and decide whether proof-domain selection can reopen.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-303 source-patch denial taxonomy handoff validated.",
        "- [x] RE-303 evidence CSV confirmed metadata-only and fingerprint-based.",
        "- [x] All source-patch denial classes evaluated for proof-domain reopen readiness.",
        "- [x] Proof-domain selection kept blocked.",
        "- [x] Handoff stop-condition reduction emitted as next safe metadata step.",
        "",
        "## Artifacts",
        "",
        f"- Gate CSV: `{GATE_CSV}`",
        f"- Summary CSV: `{SUMMARY_CSV}`",
        f"- Handoff CSV: `{HANDOFF_CSV}`",
        f"- Markdown: `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- Source-patch denial classes gated: `{s.source_patch_denial_class_count}`",
        f"- Ready to reopen proof-domain selection: `{s.ready_to_reopen_domain_count}`",
        f"- Classes needing more metadata: `{s.needs_more_metadata_count}`",
        f"- Source patch authorized rows: `{s.source_patch_authorized_count}`",
        f"- Raw/asset sources admitted: `{s.raw_or_asset_source_count}`",
        "",
        "The source-patch denial taxonomy is metadata-only and confirms blocked patch paths, not proof-domain readiness or source authorization.",
        "",
        "## Follow-up ticket breakdown",
        "",
        f"### {s.next_ticket} — {s.next_topic}",
        "",
        "- Goal: normalize handoff stop conditions before any proof-domain selection can reopen.",
        f"- Inputs: `{GATE_CSV}`, `docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv`, upstream handoff CSV artifacts.",
        "- Deliverables: handoff stop-condition taxonomy CSV, metadata-only evidence CSV, summary/handoff CSV, story file with progress tracker.",
        "- Validation: targeted pytest, reverse suite, metadata-only forbidden-fragment guard, asset staging guard.",
        "- Stop condition: do not reopen proof-domain selection until handoff stop conditions are reduced and gated.",
        "",
        "## Readiness",
        "",
        f"- Metadata work readiness: `{s.metadata_work_readiness}`",
        f"- Code/source readiness: `{s.code_change_readiness}`",
        f"- Selected domain: `{s.selected_domain}`",
        f"- Selected pivot: `{s.selected_pivot}`",
        f"- Stop condition: `{s.stop_condition}`",
        "",
        "No production source or marker change is authorized by this story.",
        "",
    ]
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", type=Path)
    args = parser.parse_args()
    bundle = build_readiness_gate(args.repo)
    written = write_all_artifacts(bundle, args.repo)
    for name, path in written.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
