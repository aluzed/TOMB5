#!/usr/bin/env python3
"""Generate RE-297 story-tracker readiness statement reduction artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE296_HANDOFF = "docs/reverse/generated/re296-blocker-reduction-candidate-selection-handoff.csv"
RE296_CANDIDATES = "docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv"

TAXONOMY_CSV = "docs/reverse/generated/re297-story-tracker-readiness-statement-reduction.csv"
EVIDENCE_CSV = "docs/reverse/generated/re297-story-tracker-readiness-statement-reduction-evidence.csv"
SUMMARY_CSV = "docs/reverse/generated/re297-story-tracker-readiness-statement-reduction-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re297-story-tracker-readiness-statement-reduction-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re297-story-tracker-readiness-statement-reduction.md"
STORY = "docs/stories/RE-297-story-tracker-readiness-statement-reduction.md"

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

LINE_TERMS = (
    "blocked",
    "readiness:",
    "readiness`",
    "readiness: `",
    "stop condition",
    "stop-condition",
    "no production source",
    "no source",
    "selected domain",
    "domain selection",
    "source readiness",
    "code/source readiness",
    "code change readiness",
)

CLASS_DESCRIPTIONS = {
    "source-or-code-readiness-blocked": "Rows that explicitly keep production source, marker, or code-change readiness blocked.",
    "blocked-readiness-status": "Status and readiness labels that encode a blocked or terminal-blocked state.",
    "no-production-source-authorization": "Statements that deny production source or marker changes.",
    "domain-selection-still-blocked": "Statements that keep domain or pivot selection unavailable.",
    "stop-condition-before-source-or-domain-work": "Stop conditions that must be satisfied before source or proof-domain work resumes.",
    "metadata-work-readiness-only": "Statements where only metadata work is ready while proof/source work remains blocked.",
    "generic-blocker-reference": "Other blocker mentions in story tracker prose or validation command text.",
}

CLASS_ORDER = {
    "source-or-code-readiness-blocked": 0,
    "blocked-readiness-status": 1,
    "no-production-source-authorization": 2,
    "domain-selection-still-blocked": 3,
    "stop-condition-before-source-or-domain-work": 4,
    "metadata-work-readiness-only": 5,
    "generic-blocker-reference": 6,
}


@dataclass(frozen=True)
class StoryEvidenceRow:
    story_file: str
    line_number: int
    normalized_class: str
    line_fingerprint: str


@dataclass(frozen=True)
class ReadinessTaxonomyRow:
    normalized_class: str
    description: str
    evidence_count: int
    story_count: int
    first_story: str
    metadata_reduction_ready: str
    domain_selection_ready: str
    source_patch_authorized: str
    next_action: str


@dataclass(frozen=True)
class ReadinessReductionSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    selected_candidate_id: str
    selected_source_id: str
    selected_blocker: str
    story_file_count: int
    evidence_line_count: int
    normalized_class_count: int
    metadata_reduction_ready_count: int
    domain_selection_ready_count: int
    raw_or_asset_source_count: int
    next_ticket: str
    next_topic: str
    selected_domain: str
    selected_pivot: str
    metadata_work_readiness: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class ReadinessReductionBundle:
    rows: list[ReadinessTaxonomyRow]
    evidence: list[StoryEvidenceRow]
    summary: ReadinessReductionSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_re296_handoff(repo: Path) -> dict[str, str]:
    rows = read_csv(repo / RE296_HANDOFF)
    if len(rows) != 1:
        raise ValueError("RE-296 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "story_id": "RE-296",
        "next_ticket": "RE-297",
        "next_topic": "story-tracker-readiness-statement-reduction",
        "selected_candidate_id": "story-tracker-blocked-readiness-statements",
        "selected_source_id": "story-tracker",
        "selected_blocker": "blocked-readiness-statements",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
        "domain_selection_ready_count": "0",
        "raw_or_asset_source_count": "0",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-296 handoff drift: {key}={row.get(key)!r}")
    return row


def selected_candidate(repo: Path) -> dict[str, str]:
    candidates = read_csv(repo / RE296_CANDIDATES)
    selected = [row for row in candidates if row["selection_status"] == "selected"]
    if len(selected) != 1:
        raise ValueError("RE-296 candidates must contain exactly one selected row")
    row = selected[0]
    if row["candidate_id"] != "story-tracker-blocked-readiness-statements":
        raise ValueError(f"unexpected selected candidate: {row['candidate_id']}")
    if row["source_id"] != "story-tracker" or row["source_patch_authorized"] != "no":
        raise ValueError("selected candidate must remain story-tracker metadata-only work")
    return row


def story_number(path: Path) -> int | None:
    match = re.match(r"RE-(\d+)-", path.name)
    return int(match.group(1)) if match else None


def upstream_story_files(story_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in story_dir.glob("RE-*.md"):
        number = story_number(path)
        if number is not None and number >= 297:
            continue
        files.append(path)
    return sorted(files)


def is_relevant_line(line: str) -> bool:
    low = line.lower()
    return any(term in low for term in LINE_TERMS)


def normalize_line(line: str) -> str:
    low = line.lower()
    if "metadata work readiness" in low:
        return "metadata-work-readiness-only"
    if "stop condition" in low or "stop-condition" in low:
        return "stop-condition-before-source-or-domain-work"
    if "selected domain" in low or "domain selection" in low or "domain-selection" in low or "selected pivot" in low:
        return "domain-selection-still-blocked"
    if "no production source" in low or "no source" in low or "source or marker" in low or "source/marker" in low:
        return "no-production-source-authorization"
    if "code/source readiness" in low or "code change readiness" in low or "code-change readiness" in low or "source readiness" in low:
        return "source-or-code-readiness-blocked"
    if "readiness" in low and "blocked" in low:
        return "blocked-readiness-status"
    if "blocked" in low:
        return "generic-blocker-reference"
    return "generic-blocker-reference"


def fingerprint(line: str) -> str:
    normalized = re.sub(r"\s+", " ", line.strip().lower())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def collect_evidence(repo: Path) -> tuple[list[StoryEvidenceRow], int]:
    stories = upstream_story_files(repo / "docs/stories")
    evidence: list[StoryEvidenceRow] = []
    for path in stories:
        for idx, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
            if not is_relevant_line(line):
                continue
            evidence.append(
                StoryEvidenceRow(
                    story_file=str(path.relative_to(repo)),
                    line_number=idx,
                    normalized_class=normalize_line(line),
                    line_fingerprint=fingerprint(line),
                )
            )
    return sorted(evidence, key=lambda row: (row.story_file, row.line_number, row.normalized_class)), len(stories)


def build_taxonomy(evidence: list[StoryEvidenceRow]) -> list[ReadinessTaxonomyRow]:
    counts = Counter(row.normalized_class for row in evidence)
    stories_by_class: dict[str, set[str]] = defaultdict(set)
    for row in evidence:
        stories_by_class[row.normalized_class].add(row.story_file)
    rows: list[ReadinessTaxonomyRow] = []
    for normalized_class, count in counts.items():
        first_story = sorted(stories_by_class[normalized_class])[0]
        rows.append(
            ReadinessTaxonomyRow(
                normalized_class=normalized_class,
                description=CLASS_DESCRIPTIONS[normalized_class],
                evidence_count=count,
                story_count=len(stories_by_class[normalized_class]),
                first_story=first_story,
                metadata_reduction_ready="yes",
                domain_selection_ready="no",
                source_patch_authorized="no",
                next_action=f"feed {normalized_class} into the story-tracker blocker taxonomy readiness gate",
            )
        )
    return sorted(rows, key=lambda row: (-row.evidence_count, row.normalized_class))


def build_readiness_reduction(repo: Path) -> ReadinessReductionBundle:
    repo = Path(repo)
    handoff = validate_re296_handoff(repo)
    selected_candidate(repo)
    evidence, story_count = collect_evidence(repo)
    rows = build_taxonomy(evidence)
    if not rows:
        raise ValueError("story tracker evidence is empty")
    raw_count = 0
    summary = ReadinessReductionSummary(
        story_id="RE-297",
        topic="story-tracker-readiness-statement-reduction",
        upstream_handoff="RE-296",
        selected_candidate_id=handoff["selected_candidate_id"],
        selected_source_id=handoff["selected_source_id"],
        selected_blocker=handoff["selected_blocker"],
        story_file_count=story_count,
        evidence_line_count=len(evidence),
        normalized_class_count=len(rows),
        metadata_reduction_ready_count=sum(1 for row in rows if row.metadata_reduction_ready == "yes"),
        domain_selection_ready_count=sum(1 for row in rows if row.domain_selection_ready == "yes"),
        raw_or_asset_source_count=raw_count,
        next_ticket="RE-298",
        next_topic="story-tracker-blocker-taxonomy-readiness-gate",
        selected_domain="none",
        selected_pivot="none",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="run taxonomy readiness gate before reopening proof-domain selection",
    )
    return ReadinessReductionBundle(rows=rows, evidence=evidence, summary=summary)


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


def write_markdown(path: Path, bundle: ReadinessReductionBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-297 story-tracker readiness statement reduction",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-296 candidate-selection handoff validated.",
        "- [x] Story tracker readiness/blocker lines inventoried without raw or asset inputs.",
        "- [x] Repeated readiness statements normalized into reusable blocker classes.",
        "- [x] Domain selection and source patch readiness kept blocked.",
        "",
        "## Summary",
        "",
        f"- Story files scanned: `{s.story_file_count}`",
        f"- Evidence lines reduced: `{s.evidence_line_count}`",
        f"- Normalized classes: `{s.normalized_class_count}`",
        f"- Metadata-ready classes: `{s.metadata_reduction_ready_count}`",
        f"- Domain-selection-ready classes: `{s.domain_selection_ready_count}`",
        f"- Raw/asset sources admitted: `{s.raw_or_asset_source_count}`",
        "",
        "## Normalized blocker taxonomy",
        "",
    ]
    for row in bundle.rows:
        lines.extend(
            [
                f"### {row.normalized_class}",
                "",
                f"- Evidence count: `{row.evidence_count}`",
                f"- Story count: `{row.story_count}`",
                f"- First story: `{row.first_story}`",
                f"- Description: {row.description}",
                f"- Domain selection ready: `{row.domain_selection_ready}`",
                f"- Source patch authorized: `{row.source_patch_authorized}`",
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


def write_story(path: Path, bundle: ReadinessReductionBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-297 — story-tracker readiness statement reduction",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Normalize repeated story-tracker readiness and blocker statements into reusable metadata classes before reopening proof-domain selection.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-296 candidate-selection handoff validated.",
        "- [x] Upstream story files scanned with RE-297+ outputs excluded for stable reruns.",
        "- [x] Evidence lines reduced to hashed metadata rows without storing source line text.",
        "- [x] Normalized taxonomy and follow-up readiness gate emitted.",
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
        f"- Story files scanned: `{s.story_file_count}`",
        f"- Evidence lines reduced: `{s.evidence_line_count}`",
        f"- Normalized classes: `{s.normalized_class_count}`",
        f"- Metadata-ready classes: `{s.metadata_reduction_ready_count}`",
        f"- Domain-selection-ready classes: `{s.domain_selection_ready_count}`",
        f"- Raw/asset sources admitted: `{s.raw_or_asset_source_count}`",
        "",
        "The reduction converts repeated story readiness language into reusable metadata classes. It still does not select a proof domain, pivot, source patch, or marker patch.",
        "",
        "## Follow-up ticket breakdown",
        "",
        f"### {s.next_ticket} — {s.next_topic}",
        "",
        "- Goal: decide whether the normalized story-tracker blocker taxonomy is sufficient to reopen safe proof-domain selection or whether another metadata source must be reduced first.",
        f"- Inputs: `{TAXONOMY_CSV}`, `{EVIDENCE_CSV}`, `{RE296_CANDIDATES}`.",
        "- Deliverables: readiness-gate CSV, summary/handoff CSV, story file with progress tracker.",
        "- Validation: targeted pytest, reverse suite, metadata-only forbidden-fragment guard, asset staging guard.",
        "- Stop condition: keep proof-domain selection blocked unless the gate can justify a non-raw, metadata-only next selection step.",
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


def write_all_artifacts(bundle: ReadinessReductionBundle, repo: Path) -> dict[str, Path]:
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
    bundle = build_readiness_reduction(args.repo)
    written = write_all_artifacts(bundle, args.repo)
    for name, path in written.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
