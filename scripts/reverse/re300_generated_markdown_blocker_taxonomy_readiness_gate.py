#!/usr/bin/env python3
"""Generate RE-300 generated-Markdown blocker taxonomy readiness gate artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE299_HANDOFF = "docs/reverse/generated/re299-generated-markdown-blocker-taxonomy-reduction-handoff.csv"
RE299_TAXONOMY = "docs/reverse/generated/re299-generated-markdown-blocker-taxonomy-reduction.csv"
RE299_EVIDENCE = "docs/reverse/generated/re299-generated-markdown-blocker-taxonomy-reduction-evidence.csv"
RE296_CANDIDATES = "docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv"

GATE_CSV = "docs/reverse/generated/re300-generated-markdown-blocker-taxonomy-readiness-gate.csv"
SUMMARY_CSV = "docs/reverse/generated/re300-generated-markdown-blocker-taxonomy-readiness-gate-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re300-generated-markdown-blocker-taxonomy-readiness-gate-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re300-generated-markdown-blocker-taxonomy-readiness-gate.md"
STORY = "docs/stories/RE-300-generated-markdown-blocker-taxonomy-readiness-gate.md"

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

NEXT_TOPIC = "proof-audit-blocker-taxonomy-reduction"
NEXT_SOURCE = "proof-audits"


@dataclass(frozen=True)
class ReadinessGateRow:
    normalized_class: str
    evidence_count: int
    markdown_file_count: int
    story_tracker_correlated: str
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
    generated_markdown_class_count: int
    story_tracker_correlated_count: int
    gate_row_count: int
    ready_to_reopen_domain_count: int
    needs_more_metadata_count: int
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


def validate_re299_handoff(repo: Path) -> None:
    rows = read_csv(repo / RE299_HANDOFF)
    if len(rows) != 1:
        raise ValueError("RE-299 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "story_id": "RE-299",
        "next_ticket": "RE-300",
        "next_topic": "generated-markdown-blocker-taxonomy-readiness-gate",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
        "domain_selection_ready_count": "0",
        "raw_or_asset_source_count": "0",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-299 handoff drift: {key}={row.get(key)!r}")


def validate_re296_next_candidate(repo: Path) -> None:
    rows = read_csv(repo / RE296_CANDIDATES)
    matches = [row for row in rows if row["source_id"] == NEXT_SOURCE]
    if len(matches) != 1:
        raise ValueError("RE-296 proof-audits candidate must contain exactly one row")
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
            raise ValueError(f"RE-296 proof-audits candidate drift: {key}={row.get(key)!r}")


def validate_evidence_metadata_only(repo: Path) -> None:
    rows = read_csv(repo / RE299_EVIDENCE)
    if not rows:
        raise ValueError("RE-299 evidence must not be empty")
    required = {"markdown_file", "line_number", "normalized_class", "line_fingerprint"}
    if set(rows[0]) != required:
        raise ValueError(f"RE-299 evidence schema drift: {set(rows[0])!r}")
    forbidden_columns = {"line_text", "source_text", "raw_text"}
    if forbidden_columns & set(rows[0]):
        raise ValueError("RE-299 evidence leaked raw text columns")


def reason_for_class(row: dict[str, str]) -> str:
    cls = row["normalized_class"]
    correlated = row["story_tracker_correlated"]
    if cls == "generic-blocker-reference":
        return "generated-Markdown blockers remain too generic to select a proof domain"
    if cls == "domain-selection-still-blocked":
        return "generated Markdown explicitly keeps domain selection blocked"
    if cls == "proof-or-marker-change-blocked":
        return "marker/proof blockers require proof-audit corroboration beyond partial story-tracker overlap"
    if cls == "source-or-code-readiness-blocked":
        return "source/code readiness remains blocked across generated Markdown"
    if cls == "no-production-source-authorization":
        return "source authorization denials confirm no source patch can proceed"
    if cls == "metadata-work-readiness-only":
        return "metadata readiness alone does not prove a domain or pivot"
    if cls == "stop-condition-before-source-or-domain-work":
        return "stop conditions require another metadata source before proof-domain work"
    return f"generated-Markdown taxonomy correlation is {correlated} and still needs proof-audit corroboration"


def build_rows(repo: Path) -> list[ReadinessGateRow]:
    taxonomy = read_csv(repo / RE299_TAXONOMY)
    if len(taxonomy) != 7:
        raise ValueError(f"RE-299 taxonomy drift: expected 7 rows, got {len(taxonomy)}")
    rows: list[ReadinessGateRow] = []
    for row in taxonomy:
        if row["domain_selection_ready"] != "no" or row["source_patch_authorized"] != "no":
            raise ValueError(f"taxonomy row unexpectedly ready: {row['normalized_class']}")
        rows.append(
            ReadinessGateRow(
                normalized_class=row["normalized_class"],
                evidence_count=int(row["evidence_count"]),
                markdown_file_count=int(row["markdown_file_count"]),
                story_tracker_correlated=row["story_tracker_correlated"],
                gate_decision="needs-more-metadata",
                readiness_reason=reason_for_class(row),
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                next_metadata_source=NEXT_SOURCE,
                next_ticket="RE-301",
                next_topic=NEXT_TOPIC,
            )
        )
    return sorted(rows, key=lambda row: (-row.evidence_count, row.normalized_class))


def build_readiness_gate(repo: Path) -> ReadinessGateBundle:
    repo = Path(repo)
    validate_re299_handoff(repo)
    validate_re296_next_candidate(repo)
    validate_evidence_metadata_only(repo)
    rows = build_rows(repo)
    summary = ReadinessGateSummary(
        story_id="RE-300",
        topic="generated-markdown-blocker-taxonomy-readiness-gate",
        upstream_handoff="RE-299",
        generated_markdown_class_count=len(rows),
        story_tracker_correlated_count=sum(1 for row in rows if row.story_tracker_correlated in {"yes", "partial"}),
        gate_row_count=len(rows),
        ready_to_reopen_domain_count=sum(1 for row in rows if row.ready_to_reopen_domain == "yes"),
        needs_more_metadata_count=sum(1 for row in rows if row.gate_decision == "needs-more-metadata"),
        raw_or_asset_source_count=0,
        next_ticket="RE-301",
        next_topic=NEXT_TOPIC,
        selected_domain="none",
        selected_pivot="none",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="reduce proof-audit blockers before proof-domain selection can reopen",
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
        "# RE-300 generated-Markdown blocker taxonomy readiness gate",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-299 generated-Markdown taxonomy handoff validated.",
        "- [x] RE-299 evidence schema checked for metadata-only fingerprints.",
        "- [x] Generated-Markdown taxonomy gated against story-tracker correlation.",
        "- [x] Proof-domain selection kept blocked pending proof-audit reduction.",
        "",
        "## Gate decision",
        "",
        f"- Generated-Markdown classes gated: `{s.gate_row_count}`",
        f"- Story-tracker-correlated classes: `{s.story_tracker_correlated_count}`",
        f"- Ready to reopen proof-domain selection: `{s.ready_to_reopen_domain_count}`",
        f"- Classes needing more metadata: `{s.needs_more_metadata_count}`",
        f"- Next metadata source: `{NEXT_SOURCE}`",
        f"- Next topic: `{s.next_topic}`",
        "",
        "Generated Markdown corroborates story-tracker blockers, but the evidence is still blocker taxonomy rather than non-raw proof-domain selection evidence. Proof-audit blockers are the next safe metadata source.",
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
                f"- Markdown files: `{row.markdown_file_count}`",
                f"- Story-tracker correlated: `{row.story_tracker_correlated}`",
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
        "# RE-300 — generated-Markdown blocker taxonomy readiness gate",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Gate the generated-Markdown blocker taxonomy against story-tracker correlation and decide whether proof-domain selection can reopen.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-299 generated-Markdown taxonomy handoff validated.",
        "- [x] RE-299 evidence CSV confirmed metadata-only and fingerprint-based.",
        "- [x] All generated-Markdown taxonomy classes evaluated for proof-domain reopen readiness.",
        "- [x] Proof-domain selection kept blocked.",
        "- [x] Proof-audit blocker reduction emitted as next safe metadata step.",
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
        f"- Generated-Markdown classes gated: `{s.generated_markdown_class_count}`",
        f"- Story-tracker-correlated classes: `{s.story_tracker_correlated_count}`",
        f"- Ready to reopen proof-domain selection: `{s.ready_to_reopen_domain_count}`",
        f"- Classes needing more metadata: `{s.needs_more_metadata_count}`",
        f"- Raw/asset sources admitted: `{s.raw_or_asset_source_count}`",
        "",
        "The generated-Markdown taxonomy corroborates blockers already seen in story tracking, but the gate still lacks proof-audit corroboration. Proof-domain selection remains blocked.",
        "",
        "## Follow-up ticket breakdown",
        "",
        f"### {s.next_ticket} — {s.next_topic}",
        "",
        "- Goal: normalize proof-audit blocker rows into reusable missing-evidence classes.",
        f"- Inputs: `{GATE_CSV}`, `docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv`, proof-audit generated CSV/Markdown artifacts.",
        "- Deliverables: proof-audit blocker taxonomy CSV, summary/handoff CSV, story file with progress tracker.",
        "- Validation: targeted pytest, reverse suite, metadata-only forbidden-fragment guard, asset staging guard.",
        "- Stop condition: do not reopen proof-domain selection until proof-audit blockers are normalized and gated.",
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
