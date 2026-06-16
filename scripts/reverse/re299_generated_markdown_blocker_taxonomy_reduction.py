#!/usr/bin/env python3
"""Generate RE-299 generated-Markdown blocker taxonomy reduction artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE298_HANDOFF = "docs/reverse/generated/re298-story-tracker-blocker-taxonomy-readiness-gate-handoff.csv"
RE298_GATE = "docs/reverse/generated/re298-story-tracker-blocker-taxonomy-readiness-gate.csv"
RE297_TAXONOMY = "docs/reverse/generated/re297-story-tracker-readiness-statement-reduction.csv"
RE296_CANDIDATES = "docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv"

TAXONOMY_CSV = "docs/reverse/generated/re299-generated-markdown-blocker-taxonomy-reduction.csv"
EVIDENCE_CSV = "docs/reverse/generated/re299-generated-markdown-blocker-taxonomy-reduction-evidence.csv"
SUMMARY_CSV = "docs/reverse/generated/re299-generated-markdown-blocker-taxonomy-reduction-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re299-generated-markdown-blocker-taxonomy-reduction-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re299-generated-markdown-blocker-taxonomy-reduction.md"
STORY = "docs/stories/RE-299-generated-markdown-blocker-taxonomy-reduction.md"

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

NEXT_TOPIC = "generated-markdown-blocker-taxonomy-readiness-gate"


@dataclass(frozen=True)
class EvidenceRow:
    markdown_file: str
    line_number: int
    normalized_class: str
    line_fingerprint: str


@dataclass(frozen=True)
class MarkdownTaxonomyRow:
    normalized_class: str
    description: str
    evidence_count: int
    markdown_file_count: int
    first_markdown_file: str
    story_tracker_correlated: str
    metadata_reduction_ready: str
    domain_selection_ready: str
    source_patch_authorized: str
    next_action: str


@dataclass(frozen=True)
class MarkdownReductionSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    generated_markdown_file_count: int
    evidence_line_count: int
    normalized_class_count: int
    metadata_reduction_ready_count: int
    domain_selection_ready_count: int
    raw_or_asset_source_count: int
    story_tracker_correlated_count: int
    next_ticket: str
    next_topic: str
    selected_domain: str
    selected_pivot: str
    metadata_work_readiness: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class MarkdownReductionBundle:
    rows: list[MarkdownTaxonomyRow]
    evidence: list[EvidenceRow]
    summary: MarkdownReductionSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_re298_handoff(repo: Path) -> None:
    rows = read_csv(repo / RE298_HANDOFF)
    if len(rows) != 1:
        raise ValueError("RE-298 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "story_id": "RE-298",
        "next_ticket": "RE-299",
        "next_topic": "generated-markdown-blocker-taxonomy-reduction",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
        "ready_to_reopen_domain_count": "0",
        "raw_or_asset_source_count": "0",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-298 handoff drift: {key}={row.get(key)!r}")


def validate_re298_gate(repo: Path) -> None:
    rows = read_csv(repo / RE298_GATE)
    if not rows:
        raise ValueError("RE-298 gate rows required")
    if any(row["next_metadata_source"] != "generated-markdown" for row in rows):
        raise ValueError("RE-298 gate must point every row at generated-markdown")
    if any(row["ready_to_reopen_domain"] != "no" for row in rows):
        raise ValueError("RE-298 gate unexpectedly reopened a proof domain")


def validate_re296_candidate(repo: Path) -> None:
    rows = read_csv(repo / RE296_CANDIDATES)
    matches = [row for row in rows if row["candidate_id"] == "generated-markdown-blocked-readiness-statements"]
    if len(matches) != 1:
        raise ValueError("RE-296 generated-markdown candidate missing")
    row = matches[0]
    expected = {
        "source_id": "generated-markdown",
        "selection_status": "candidate",
        "metadata_candidate_ready": "yes",
        "domain_selection_ready": "no",
        "source_patch_authorized": "no",
        "raw_or_asset_dependency": "no",
        "next_topic": "generated-markdown-blocker-taxonomy-reduction",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-296 generated-markdown candidate drift: {key}={row.get(key)!r}")


def generated_markdown_files(repo: Path) -> list[Path]:
    files: list[Path] = []
    for path in (repo / "docs/reverse/functions").glob("*.md"):
        match = re.match(r"re(\d+)-", path.name)
        if match and int(match.group(1)) >= 299:
            continue
        files.append(path)
    return sorted(files)


def normalize_line(line: str) -> str | None:
    low = line.lower()
    if not any(token in low for token in ("blocked", "readiness", "source patch", "marker", "proof", "domain", "stop condition", "no production")):
        return None
    if "no production" in low or "no source" in low or "not authorize" in low or "not authorized" in low:
        return "no-production-source-authorization"
    if "source patch" in low or "code change" in low or "code-change" in low or "source/code" in low:
        return "source-or-code-readiness-blocked"
    if "marker" in low or "proof marker" in low:
        return "proof-or-marker-change-blocked"
    if "domain" in low or "pivot" in low:
        return "domain-selection-still-blocked"
    if "metadata" in low and "readiness" in low:
        return "metadata-work-readiness-only"
    if "stop condition" in low or "stop-condition" in low:
        return "stop-condition-before-source-or-domain-work"
    if "blocked" in low or "readiness" in low or "proof" in low:
        return "generic-blocker-reference"
    return None


def description_for_class(normalized_class: str) -> str:
    descriptions = {
        "source-or-code-readiness-blocked": "Generated Markdown statements that keep source or code-change readiness blocked.",
        "no-production-source-authorization": "Generated Markdown statements that deny production source changes.",
        "proof-or-marker-change-blocked": "Generated Markdown statements that deny proof-marker or marker patch readiness.",
        "domain-selection-still-blocked": "Generated Markdown statements that keep domain or pivot selection unavailable.",
        "metadata-work-readiness-only": "Generated Markdown statements where metadata work is ready but proof/source work remains blocked.",
        "stop-condition-before-source-or-domain-work": "Generated Markdown stop conditions before source or proof-domain work can resume.",
        "generic-blocker-reference": "Other generated Markdown blocker, proof, or readiness references.",
    }
    return descriptions[normalized_class]


def story_tracker_classes(repo: Path) -> set[str]:
    return {row["normalized_class"] for row in read_csv(repo / RE297_TAXONOMY)}


def correlation_for(normalized_class: str, story_classes: set[str]) -> str:
    if normalized_class in story_classes:
        return "yes"
    if normalized_class == "proof-or-marker-change-blocked":
        return "partial"
    return "no"


def scan_markdown(repo: Path) -> tuple[list[EvidenceRow], int]:
    evidence: list[EvidenceRow] = []
    files = generated_markdown_files(repo)
    for path in files:
        rel = path.relative_to(repo).as_posix()
        for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
            normalized = normalize_line(line)
            if normalized is None:
                continue
            fingerprint = hashlib.sha256(f"{rel}:{line_number}:{line.strip()}".encode("utf-8")).hexdigest()[:16]
            evidence.append(EvidenceRow(rel, line_number, normalized, fingerprint))
    evidence.sort(key=lambda row: (row.normalized_class, row.markdown_file, row.line_number))
    return evidence, len(files)


def build_rows(repo: Path, evidence: list[EvidenceRow]) -> list[MarkdownTaxonomyRow]:
    story_classes = story_tracker_classes(repo)
    counts = Counter(row.normalized_class for row in evidence)
    files_by_class: dict[str, set[str]] = defaultdict(set)
    for row in evidence:
        files_by_class[row.normalized_class].add(row.markdown_file)
    rows: list[MarkdownTaxonomyRow] = []
    for normalized_class, count in counts.items():
        first_file = sorted(files_by_class[normalized_class])[0]
        rows.append(
            MarkdownTaxonomyRow(
                normalized_class=normalized_class,
                description=description_for_class(normalized_class),
                evidence_count=count,
                markdown_file_count=len(files_by_class[normalized_class]),
                first_markdown_file=first_file,
                story_tracker_correlated=correlation_for(normalized_class, story_classes),
                metadata_reduction_ready="yes",
                domain_selection_ready="no",
                source_patch_authorized="no",
                next_action=f"feed {normalized_class} into the generated-Markdown blocker taxonomy readiness gate",
            )
        )
    return sorted(rows, key=lambda row: (-row.evidence_count, row.normalized_class))


def build_generated_markdown_reduction(repo: Path) -> MarkdownReductionBundle:
    repo = Path(repo)
    validate_re298_handoff(repo)
    validate_re298_gate(repo)
    validate_re296_candidate(repo)
    evidence, file_count = scan_markdown(repo)
    if not evidence:
        raise ValueError("generated Markdown evidence required")
    rows = build_rows(repo, evidence)
    summary = MarkdownReductionSummary(
        story_id="RE-299",
        topic="generated-markdown-blocker-taxonomy-reduction",
        upstream_handoff="RE-298",
        generated_markdown_file_count=file_count,
        evidence_line_count=len(evidence),
        normalized_class_count=len(rows),
        metadata_reduction_ready_count=sum(1 for row in rows if row.metadata_reduction_ready == "yes"),
        domain_selection_ready_count=sum(1 for row in rows if row.domain_selection_ready == "yes"),
        raw_or_asset_source_count=0,
        story_tracker_correlated_count=sum(1 for row in rows if row.story_tracker_correlated in {"yes", "partial"}),
        next_ticket="RE-300",
        next_topic=NEXT_TOPIC,
        selected_domain="none",
        selected_pivot="none",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="gate generated-markdown taxonomy before proof-domain selection can reopen",
    )
    return MarkdownReductionBundle(rows=rows, evidence=evidence, summary=summary)


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


def write_markdown(path: Path, bundle: MarkdownReductionBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-299 generated-Markdown blocker taxonomy reduction",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-298 readiness-gate handoff validated.",
        "- [x] Deferred generated-Markdown candidate from RE-296 validated.",
        "- [x] Generated Markdown files scanned with RE-299+ outputs excluded for stable reruns.",
        "- [x] Evidence reduced to hashed metadata rows without storing source line text.",
        "",
        "## Findings",
        "",
        f"- Generated Markdown files scanned: `{s.generated_markdown_file_count}`",
        f"- Evidence lines reduced: `{s.evidence_line_count}`",
        f"- Normalized classes: `{s.normalized_class_count}`",
        f"- Domain-selection-ready classes: `{s.domain_selection_ready_count}`",
        "",
        "## Story-tracker correlation",
        "",
        "Generated Markdown blockers overlap the story-tracker taxonomy, but this reduction still does not reopen proof-domain selection. It prepares the generated-Markdown taxonomy for a dedicated readiness gate.",
        "",
        "## Taxonomy rows",
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
                f"- Domain selection ready: `{row.domain_selection_ready}`",
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
            "No production source or marker change is authorized by this reduction.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story(path: Path, bundle: MarkdownReductionBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-299 — generated-Markdown blocker taxonomy reduction",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Normalize generated reverse-function Markdown blocker and readiness statements into reusable metadata classes, then hand off to a gate before proof-domain selection can reopen.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-298 readiness-gate handoff validated.",
        "- [x] RE-296 generated-Markdown candidate validated as safe metadata work.",
        "- [x] Generated Markdown evidence reduced to hashed metadata rows.",
        "- [x] Story-tracker taxonomy correlation recorded.",
        "- [x] Code/source readiness remains blocked.",
        "",
        "## Artifacts",
        "",
        f"- Taxonomy CSV: `{TAXONOMY_CSV}`",
        f"- Evidence CSV: `{EVIDENCE_CSV}`",
        f"- Summary CSV: `{SUMMARY_CSV}`",
        f"- Handoff CSV: `{HANDOFF_CSV}`",
        f"- Markdown: `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- Generated Markdown files scanned: `{s.generated_markdown_file_count}`",
        f"- Evidence lines reduced: `{s.evidence_line_count}`",
        f"- Normalized classes: `{s.normalized_class_count}`",
        f"- Metadata-ready classes: `{s.metadata_reduction_ready_count}`",
        f"- Domain-selection-ready classes: `{s.domain_selection_ready_count}`",
        f"- Story-tracker-correlated classes: `{s.story_tracker_correlated_count}`",
        f"- Raw/asset sources admitted: `{s.raw_or_asset_source_count}`",
        "",
        "The reduction confirms that generated Markdown carries corroborating blocker taxonomy, but it does not by itself authorize proof-domain selection, source patches, or marker patches.",
        "",
        "## Follow-up ticket breakdown",
        "",
        f"### {s.next_ticket} — {s.next_topic}",
        "",
        "- Goal: gate the generated-Markdown taxonomy against story-tracker classes and decide whether another metadata source is required.",
        f"- Inputs: `{TAXONOMY_CSV}`, `{EVIDENCE_CSV}`, `docs/reverse/generated/re298-story-tracker-blocker-taxonomy-readiness-gate.csv`.",
        "- Deliverables: readiness-gate CSV, summary/handoff CSV, story file with progress tracker.",
        "- Validation: targeted pytest, reverse suite, metadata-only forbidden-fragment guard, asset staging guard.",
        "- Stop condition: keep proof-domain selection blocked unless the gate can justify a non-raw metadata selection step.",
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


def write_all_artifacts(bundle: MarkdownReductionBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "taxonomy_csv": repo / TAXONOMY_CSV,
        "evidence_csv": repo / EVIDENCE_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_rows(paths["taxonomy_csv"], bundle.rows)
    write_rows(paths["evidence_csv"], bundle.evidence)
    write_rows(paths["summary_csv"], [bundle.summary])
    write_rows(paths["handoff_csv"], [bundle.summary])
    write_markdown(paths["md"], bundle)
    write_story(paths["story"], bundle)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", type=Path)
    args = parser.parse_args()
    bundle = build_generated_markdown_reduction(args.repo)
    written = write_all_artifacts(bundle, args.repo)
    for name, path in written.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
