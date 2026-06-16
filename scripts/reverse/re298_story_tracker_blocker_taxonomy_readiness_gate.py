#!/usr/bin/env python3
"""Generate RE-298 story-tracker blocker taxonomy readiness gate artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE297_HANDOFF = "docs/reverse/generated/re297-story-tracker-readiness-statement-reduction-handoff.csv"
RE297_TAXONOMY = "docs/reverse/generated/re297-story-tracker-readiness-statement-reduction.csv"
RE297_EVIDENCE = "docs/reverse/generated/re297-story-tracker-readiness-statement-reduction-evidence.csv"
RE296_CANDIDATES = "docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv"

GATE_CSV = "docs/reverse/generated/re298-story-tracker-blocker-taxonomy-readiness-gate.csv"
SUMMARY_CSV = "docs/reverse/generated/re298-story-tracker-blocker-taxonomy-readiness-gate-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re298-story-tracker-blocker-taxonomy-readiness-gate-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re298-story-tracker-blocker-taxonomy-readiness-gate.md"
STORY = "docs/stories/RE-298-story-tracker-blocker-taxonomy-readiness-gate.md"

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

NEXT_TOPIC = "generated-markdown-blocker-taxonomy-reduction"


@dataclass(frozen=True)
class ReadinessGateRow:
    normalized_class: str
    evidence_count: int
    story_count: int
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
    taxonomy_class_count: int
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


def validate_re297_handoff(repo: Path) -> dict[str, str]:
    rows = read_csv(repo / RE297_HANDOFF)
    if len(rows) != 1:
        raise ValueError("RE-297 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "story_id": "RE-297",
        "next_ticket": "RE-298",
        "next_topic": "story-tracker-blocker-taxonomy-readiness-gate",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
        "domain_selection_ready_count": "0",
        "raw_or_asset_source_count": "0",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-297 handoff drift: {key}={row.get(key)!r}")
    return row


def validate_re296_deferred_generated_markdown(repo: Path) -> None:
    rows = read_csv(repo / RE296_CANDIDATES)
    matches = [row for row in rows if row["source_id"] == "generated-markdown"]
    if len(matches) != 1:
        raise ValueError("RE-296 candidates must contain exactly one generated-markdown row")
    row = matches[0]
    expected = {
        "selection_status": "candidate",
        "next_topic": NEXT_TOPIC,
        "source_patch_authorized": "no",
        "raw_or_asset_dependency": "no",
        "domain_selection_ready": "no",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-296 generated-markdown candidate drift: {key}={row.get(key)!r}")


def validate_evidence_metadata_only(repo: Path) -> int:
    rows = read_csv(repo / RE297_EVIDENCE)
    if not rows:
        raise ValueError("RE-297 evidence must not be empty")
    forbidden_columns = {"line_text", "source_text", "raw_text"}
    if forbidden_columns & set(rows[0]):
        raise ValueError("RE-297 evidence leaked raw line text columns")
    required = {"story_file", "line_number", "normalized_class", "line_fingerprint"}
    if not required.issubset(rows[0]):
        raise ValueError("RE-297 evidence missing metadata columns")
    return len(rows)


def reason_for_class(normalized_class: str) -> str:
    if normalized_class == "generic-blocker-reference":
        return "generic story references are not specific enough to justify a proof-domain selection"
    if normalized_class == "no-production-source-authorization":
        return "authorization denials confirm source work is blocked rather than reopenable"
    if normalized_class == "source-or-code-readiness-blocked":
        return "source/code readiness blockers still dominate the tracker"
    if normalized_class == "blocked-readiness-status":
        return "blocked status labels need corroboration from another metadata source"
    if normalized_class == "domain-selection-still-blocked":
        return "domain-selection rows explicitly remain blocked"
    if normalized_class == "stop-condition-before-source-or-domain-work":
        return "stop conditions require another metadata gate before proof-domain work"
    if normalized_class == "metadata-work-readiness-only":
        return "metadata readiness alone is insufficient to select a proof domain"
    return "story-tracker taxonomy needs corroborating metadata before domain selection"


def build_rows(repo: Path) -> list[ReadinessGateRow]:
    taxonomy = read_csv(repo / RE297_TAXONOMY)
    if len(taxonomy) != 7:
        raise ValueError(f"RE-297 taxonomy drift: expected 7 rows, got {len(taxonomy)}")
    rows: list[ReadinessGateRow] = []
    for row in taxonomy:
        if row["domain_selection_ready"] != "no" or row["source_patch_authorized"] != "no":
            raise ValueError(f"taxonomy row unexpectedly ready: {row['normalized_class']}")
        rows.append(
            ReadinessGateRow(
                normalized_class=row["normalized_class"],
                evidence_count=int(row["evidence_count"]),
                story_count=int(row["story_count"]),
                gate_decision="needs-more-metadata",
                readiness_reason=reason_for_class(row["normalized_class"]),
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                next_metadata_source="generated-markdown",
                next_ticket="RE-299",
                next_topic=NEXT_TOPIC,
            )
        )
    return sorted(rows, key=lambda item: (-item.evidence_count, item.normalized_class))


def build_readiness_gate(repo: Path) -> ReadinessGateBundle:
    repo = Path(repo)
    validate_re297_handoff(repo)
    validate_re296_deferred_generated_markdown(repo)
    validate_evidence_metadata_only(repo)
    rows = build_rows(repo)
    summary = ReadinessGateSummary(
        story_id="RE-298",
        topic="story-tracker-blocker-taxonomy-readiness-gate",
        upstream_handoff="RE-297",
        taxonomy_class_count=len(rows),
        gate_row_count=len(rows),
        ready_to_reopen_domain_count=sum(1 for row in rows if row.ready_to_reopen_domain == "yes"),
        needs_more_metadata_count=sum(1 for row in rows if row.gate_decision == "needs-more-metadata"),
        raw_or_asset_source_count=0,
        next_ticket="RE-299",
        next_topic=NEXT_TOPIC,
        selected_domain="none",
        selected_pivot="none",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="reduce generated-markdown blockers before proof-domain selection can reopen",
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
        "# RE-298 story-tracker blocker taxonomy readiness gate",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-297 taxonomy handoff validated.",
        "- [x] RE-297 evidence schema checked for metadata-only fingerprints.",
        "- [x] Story-tracker taxonomy classes gated for proof-domain readiness.",
        "- [x] Next metadata source selected without reopening source or domain work.",
        "",
        "## Gate decision",
        "",
        f"- Taxonomy classes gated: `{s.gate_row_count}`",
        f"- Ready to reopen proof-domain selection: `{s.ready_to_reopen_domain_count}`",
        f"- Classes needing more metadata: `{s.needs_more_metadata_count}`",
        f"- Next metadata source: `generated-markdown`",
        f"- Next topic: `{s.next_topic}`",
        "",
        "The story-tracker taxonomy is useful metadata, but it is not enough by itself to justify a safe proof-domain selection. The next safe step is to reduce generated Markdown blockers for corroboration.",
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
                f"- Story count: `{row.story_count}`",
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
        "# RE-298 — story-tracker blocker taxonomy readiness gate",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Gate the normalized story-tracker blocker taxonomy and decide whether it can safely reopen proof-domain selection or must be corroborated by another metadata source.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-297 taxonomy handoff validated.",
        "- [x] Evidence CSV confirmed metadata-only and fingerprint-based.",
        "- [x] All taxonomy classes evaluated for proof-domain reopen readiness.",
        "- [x] Proof-domain selection kept blocked.",
        "- [x] Generated-Markdown blocker reduction emitted as next safe metadata step.",
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
        f"- Taxonomy classes gated: `{s.taxonomy_class_count}`",
        f"- Ready to reopen proof-domain selection: `{s.ready_to_reopen_domain_count}`",
        f"- Classes needing more metadata: `{s.needs_more_metadata_count}`",
        f"- Raw/asset sources admitted: `{s.raw_or_asset_source_count}`",
        "",
        "The story-tracker taxonomy is still too broad and tracker-local to select a proof domain. Generated Markdown blockers are the next safe metadata surface to reduce before domain selection can reopen.",
        "",
        "## Follow-up ticket breakdown",
        "",
        f"### {s.next_ticket} — {s.next_topic}",
        "",
        "- Goal: normalize generated reverse-function Markdown blockers and compare them with the story-tracker taxonomy.",
        f"- Inputs: `{GATE_CSV}`, `docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv`, generated Markdown under `docs/reverse/functions/`.",
        "- Deliverables: generated-Markdown blocker taxonomy CSV, summary/handoff CSV, story file with progress tracker.",
        "- Validation: targeted pytest, reverse suite, metadata-only forbidden-fragment guard, asset staging guard.",
        "- Stop condition: do not reopen proof-domain selection until generated-Markdown blockers are normalized and gated.",
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
