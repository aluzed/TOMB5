#!/usr/bin/env python3
"""Generate RE-295 metadata blocker extraction artifacts."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE294_HANDOFF = "docs/reverse/generated/re294-evidence-source-gap-ranking-handoff.csv"
RE294_RANKING = "docs/reverse/generated/re294-evidence-source-gap-ranking.csv"

EXTRACTION_CSV = "docs/reverse/generated/re295-metadata-blocker-extraction.csv"
SUMMARY_CSV = "docs/reverse/generated/re295-metadata-blocker-extraction-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re295-metadata-blocker-extraction-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re295-metadata-blocker-extraction.md"
STORY = "docs/stories/RE-295-metadata-blocker-extraction.md"

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

TOP_TESTABLE_SOURCES = {
    "generated-markdown",
    "story-tracker",
    "handoff-csvs",
    "source-patch-gates",
    "proof-audits",
}

LINE_BLOCKER_TERMS = (
    "blocked",
    "readiness:",
    "stop condition",
    "stop-condition",
    "no production source",
    "selected domain",
    "source readiness",
)


@dataclass(frozen=True)
class BlockerExtractionRow:
    source_id: str
    source_type: str
    safety_class: str
    blocker_class: str
    evidence_count: int
    unique_blocker_count: int
    dominant_blocker: str
    metadata_reduction_ready: str
    domain_selection_ready: str
    reduction_score: int
    next_step: str


@dataclass(frozen=True)
class BlockerExtractionSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    source_count: int
    extraction_row_count: int
    metadata_reduction_ready_count: int
    domain_selection_ready_count: int
    raw_or_asset_source_count: int
    top_source_id: str
    next_ticket: str
    next_topic: str
    selected_domain: str
    selected_pivot: str
    metadata_work_readiness: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class BlockerExtractionBundle:
    rows: list[BlockerExtractionRow]
    summary: BlockerExtractionSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_re294_handoff(repo: Path) -> dict[str, str]:
    rows = read_csv(repo / RE294_HANDOFF)
    if len(rows) != 1:
        raise ValueError("RE-294 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "story_id": "RE-294",
        "next_ticket": "RE-295",
        "next_topic": "metadata-blocker-extraction",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
        "raw_or_asset_source_count": "0",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-294 handoff drift: {key}={row.get(key)!r}")
    return row


def top_ranked_sources(repo: Path) -> dict[str, dict[str, str]]:
    rows = read_csv(repo / RE294_RANKING)
    selected = {
        row["source_id"]: row
        for row in rows
        if row["source_id"] in TOP_TESTABLE_SOURCES and row["actionability"] == "testable-now"
    }
    missing = TOP_TESTABLE_SOURCES - set(selected)
    if missing:
        raise ValueError(f"missing top testable sources: {sorted(missing)}")
    for source_id, row in selected.items():
        if row["safety_class"] == "raw-or-asset":
            raise ValueError(f"unsafe source cannot be extracted: {source_id}")
    return selected


def iter_relevant_lines(base: Path) -> list[str]:
    lines: list[str] = []
    for p in sorted(base.glob("**/*.md")):
        if p.name.startswith("re295-metadata-blocker-extraction") or p.name.startswith("RE-295-metadata-blocker-extraction"):
            continue
        text = p.read_text(errors="ignore", encoding="utf-8")
        for line in text.splitlines():
            low = line.lower()
            if any(term in low for term in LINE_BLOCKER_TERMS):
                lines.append(line.strip())
    return lines


def text_dominant_blocker(lines: list[str]) -> str:
    lowered = "\n".join(lines).lower()
    if "readiness" in lowered and "blocked" in lowered:
        return "blocked-readiness-statements"
    if "no production source" in lowered:
        return "no-production-source-authorization"
    return "metadata-blocker-lines"


def csv_blocker_counter(paths: list[Path], fields_to_try: tuple[str, ...]) -> tuple[int, Counter[str]]:
    count = 0
    blockers: Counter[str] = Counter()
    for path in sorted(paths):
        for row in read_csv(path):
            count += 1
            blocker = ""
            for field in fields_to_try:
                if row.get(field):
                    blocker = row[field].strip()
                    break
            if blocker:
                blockers[blocker] += 1
    return count, blockers


def upstream_generated_files(generated_dir: Path, pattern: str) -> list[Path]:
    return [p for p in generated_dir.glob(pattern) if not p.name.startswith("re295-metadata-blocker-extraction")]


def row_for_text_source(source: dict[str, str], source_id: str, base: Path, blocker_class: str, next_step: str) -> BlockerExtractionRow:
    lines = iter_relevant_lines(base)
    evidence_count = len(lines)
    dominant = text_dominant_blocker(lines)
    unique = len(set(lines))
    return BlockerExtractionRow(
        source_id=source_id,
        source_type=source["source_type"],
        safety_class=source["safety_class"],
        blocker_class=blocker_class,
        evidence_count=evidence_count,
        unique_blocker_count=unique,
        dominant_blocker=dominant,
        metadata_reduction_ready="yes" if evidence_count > 0 else "no",
        domain_selection_ready="no",
        reduction_score=evidence_count,
        next_step=next_step,
    )


def row_for_csv_source(
    source: dict[str, str],
    source_id: str,
    paths: list[Path],
    fields_to_try: tuple[str, ...],
    blocker_class: str,
    next_step: str,
) -> BlockerExtractionRow:
    evidence_count, blockers = csv_blocker_counter(paths, fields_to_try)
    dominant = blockers.most_common(1)[0][0] if blockers else "none"
    return BlockerExtractionRow(
        source_id=source_id,
        source_type=source["source_type"],
        safety_class=source["safety_class"],
        blocker_class=blocker_class,
        evidence_count=evidence_count,
        unique_blocker_count=len(blockers),
        dominant_blocker=dominant,
        metadata_reduction_ready="yes" if evidence_count > 0 else "no",
        domain_selection_ready="no",
        reduction_score=evidence_count,
        next_step=next_step,
    )


def build_rows(repo: Path) -> list[BlockerExtractionRow]:
    sources = top_ranked_sources(repo)
    generated = repo / "docs/reverse/functions"
    stories = repo / "docs/stories"
    generated_dir = repo / "docs/reverse/generated"
    rows = [
        row_for_text_source(
            sources["generated-markdown"],
            "generated-markdown",
            generated,
            "human-summary-blockers",
            "extract normalized blocker phrases from reverse function Markdown",
        ),
        row_for_text_source(
            sources["story-tracker"],
            "story-tracker",
            stories,
            "progression-blockers",
            "extract blocked progress tracker and next-objective dependencies from stories",
        ),
        row_for_csv_source(
            sources["handoff-csvs"],
            "handoff-csvs",
            upstream_generated_files(generated_dir, "*handoff*.csv"),
            ("blocker", "stop_condition", "reason"),
            "handoff-readiness",
            "consolidate repeated handoff blockers and terminal stop conditions",
        ),
        row_for_csv_source(
            sources["source-patch-gates"],
            "source-patch-gates",
            upstream_generated_files(generated_dir, "*source-patch-gate*.csv"),
            ("blocker", "stop_reason", "decision", "dependency"),
            "patch-gate-denials",
            "cluster patch denial reasons by missing proof class",
        ),
        row_for_csv_source(
            sources["proof-audits"],
            "proof-audits",
            upstream_generated_files(generated_dir, "*proof*.csv"),
            ("blocker", "readiness", "next_probe"),
            "proof-first-gaps",
            "cluster proof-first blockers by domain and missing evidence class",
        ),
    ]
    return sorted(rows, key=lambda row: (-row.reduction_score, row.source_id))


def build_blocker_extraction(repo: Path) -> BlockerExtractionBundle:
    repo = Path(repo)
    validate_re294_handoff(repo)
    rows = build_rows(repo)
    metadata_ready = sum(1 for row in rows if row.metadata_reduction_ready == "yes")
    domain_ready = sum(1 for row in rows if row.domain_selection_ready == "yes")
    raw = sum(1 for row in rows if row.safety_class == "raw-or-asset")
    summary = BlockerExtractionSummary(
        story_id="RE-295",
        topic="metadata-blocker-extraction",
        upstream_handoff="RE-294",
        source_count=len(rows),
        extraction_row_count=len(rows),
        metadata_reduction_ready_count=metadata_ready,
        domain_selection_ready_count=domain_ready,
        raw_or_asset_source_count=raw,
        top_source_id=rows[0].source_id,
        next_ticket="RE-296",
        next_topic="blocker-reduction-candidate-selection",
        selected_domain="none",
        selected_pivot="none",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="select a metadata blocker-reduction candidate before reopening any proof domain",
    )
    return BlockerExtractionBundle(rows=rows, summary=summary)


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


def write_markdown(path: Path, bundle: BlockerExtractionBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-295 metadata blocker extraction",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-294 ranking handoff validated.",
        "- [x] Top testable metadata sources consumed.",
        "- [x] Blocker evidence counts and dominant blockers extracted.",
        "- [x] Domain selection kept blocked until a reduction candidate is selected.",
        "",
        "## Summary",
        "",
        f"- Sources extracted: `{s.source_count}`",
        f"- Extraction rows: `{s.extraction_row_count}`",
        f"- Metadata reduction ready rows: `{s.metadata_reduction_ready_count}`",
        f"- Domain selection ready rows: `{s.domain_selection_ready_count}`",
        f"- Raw/asset sources admitted: `{s.raw_or_asset_source_count}`",
        f"- Top source: `{s.top_source_id}`",
        "",
        "## Extracted blocker sources",
        "",
    ]
    for row in bundle.rows:
        lines.extend(
            [
                f"### {row.source_id}",
                "",
                f"- Blocker class: `{row.blocker_class}`",
                f"- Evidence count: `{row.evidence_count}`",
                f"- Unique blocker count: `{row.unique_blocker_count}`",
                f"- Dominant blocker: `{row.dominant_blocker}`",
                f"- Metadata reduction ready: `{row.metadata_reduction_ready}`",
                f"- Domain selection ready: `{row.domain_selection_ready}`",
                f"- Next step: {row.next_step}.",
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
            "No production source or marker change is authorized by this extraction.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story(path: Path, bundle: BlockerExtractionBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-295 — metadata blocker extraction",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Extract machine-readable blocker classes from the top-ranked metadata sources produced by RE-294 without selecting a proof domain or using raw/binary/asset material.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-294 ranking handoff validated.",
        "- [x] Top testable-now metadata sources consumed.",
        "- [x] Evidence counts and dominant blockers extracted.",
        "- [x] Domain selection readiness kept at zero.",
        "- [x] Next blocker-reduction candidate ticket emitted.",
        "",
        "## Artifacts",
        "",
        f"- Extraction CSV: `{EXTRACTION_CSV}`",
        f"- Summary CSV: `{SUMMARY_CSV}`",
        f"- Handoff CSV: `{HANDOFF_CSV}`",
        f"- Markdown: `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- Sources extracted: `{s.source_count}`",
        f"- Metadata reduction ready rows: `{s.metadata_reduction_ready_count}`",
        f"- Domain selection ready rows: `{s.domain_selection_ready_count}`",
        f"- Raw/asset sources admitted: `{s.raw_or_asset_source_count}`",
        f"- Top source: `{s.top_source_id}`",
        "",
        "The extraction converts existing metadata blockers into a ranking surface. It does not make any production source or marker patch ready.",
        "",
        "## Next objective",
        "",
        f"- Next ticket: `{s.next_ticket}`",
        f"- Topic: `{s.next_topic}`",
        "- Goal: choose the best metadata-only blocker-reduction candidate and define the next testable narrowing step before any proof-domain selection.",
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


def write_all_artifacts(bundle: BlockerExtractionBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "extraction_csv": repo / EXTRACTION_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_rows(paths["extraction_csv"], bundle.rows)
    write_rows(paths["summary_csv"], [bundle.summary])
    write_rows(paths["handoff_csv"], [bundle.summary])
    write_markdown(paths["md"], bundle)
    write_story(paths["story"], bundle)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", type=Path)
    args = parser.parse_args()
    bundle = build_blocker_extraction(args.repo)
    written = write_all_artifacts(bundle, args.repo)
    for name, path in written.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
