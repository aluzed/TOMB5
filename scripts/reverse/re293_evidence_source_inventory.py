#!/usr/bin/env python3
"""Generate RE-293 metadata-only evidence source inventory artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE292_HANDOFF = "docs/reverse/generated/re292-post-refresh-evidence-unblock-handoff.csv"
GENERATED_DIR = "docs/reverse/generated"
SOURCE_MAP = "docs/reverse/generated/repo-function-map.csv"
PRIORITY = "docs/reverse/generated/function-priority.csv"

INVENTORY_CSV = "docs/reverse/generated/re293-evidence-source-inventory.csv"
SUMMARY_CSV = "docs/reverse/generated/re293-evidence-source-inventory-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re293-evidence-source-inventory-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re293-evidence-source-inventory.md"
STORY = "docs/stories/RE-293-evidence-source-inventory.md"

FORBIDDEN = (
    "word_le_hex",
    "payload_offset",
    "dump row",
    "opcode",
    "machine word",
    "call_address",
    "branch target",
    "call target",
    "0x800",
)

SOURCE_DIRS = ("GAME", "SPEC_PSXPC", "SPEC_PSXPC_N", "SPEC_PSX", "SPEC_PC_N", "TOOLS")
SOURCE_SUFFIXES = {".C", ".H", ".CPP", ".RC"}


@dataclass(frozen=True)
class EvidenceSource:
    source_id: str
    source_type: str
    path_pattern: str
    row_or_file_count: int
    safety_class: str
    progression_status: str
    use_for: str
    current_gap: str


@dataclass(frozen=True)
class InventorySummary:
    story_id: str
    topic: str
    upstream_handoff: str
    source_count: int
    metadata_only_sources: int
    source_symbolic_sources: int
    raw_or_asset_sources: int
    candidate_gap_count: int
    next_ticket: str
    next_topic: str
    selected_domain: str
    selected_pivot: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class InventoryBundle:
    sources: list[EvidenceSource]
    summary: InventorySummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def count_csv_rows(path: Path) -> int:
    return len(read_csv(path))


def count_generated(repo: Path, pattern: str) -> int:
    return len([p for p in (repo / GENERATED_DIR).glob(pattern) if not p.name.startswith("re293-evidence-source-")])


def count_reverse_markdown(repo: Path) -> int:
    return len([p for p in (repo / "docs/reverse").glob("**/*.md") if not p.name.startswith("re293-evidence-source-")])


def count_story_markdown(repo: Path) -> int:
    return len([p for p in (repo / "docs/stories").glob("RE-*.md") if not p.name.startswith("RE-293-evidence-source-")])


def count_source_corpus_files(repo: Path) -> int:
    count = 0
    for dirname in SOURCE_DIRS:
        base = repo / dirname
        if not base.exists():
            continue
        count += sum(1 for p in base.glob("**/*") if p.is_file() and p.suffix.upper() in SOURCE_SUFFIXES)
    return count


def validate_re292_handoff(repo: Path) -> dict[str, str]:
    rows = read_csv(repo / RE292_HANDOFF)
    if len(rows) != 1:
        raise ValueError("RE-292 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "story_id": "RE-292",
        "next_ticket": "TBD",
        "next_topic": "await-new-non-raw-proof-evidence",
        "selected_domain": "none",
        "selected_pivot": "none",
        "code_change_readiness": "blocked",
        "new_priority_candidate_count": "0",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-292 handoff drift: {key}={row.get(key)!r}")
    return row


def _source(source_id: str, source_type: str, path_pattern: str, count: int, safety_class: str, use_for: str, gap: str) -> EvidenceSource:
    return EvidenceSource(
        source_id=source_id,
        source_type=source_type,
        path_pattern=path_pattern,
        row_or_file_count=count,
        safety_class=safety_class,
        progression_status="available" if count > 0 else "missing",
        use_for=use_for,
        current_gap=gap,
    )


def build_sources(repo: Path) -> list[EvidenceSource]:
    repo = Path(repo)
    sources = [
        _source(
            "argument-taxonomies",
            "generated-csv",
            "docs/reverse/generated/*argument*taxonomy*.csv",
            count_generated(repo, "*argument*taxonomy*.csv"),
            "metadata-only",
            "symbolic argument and state grouping",
            "needs cross-ticket gap ranking before reuse",
        ),
        _source(
            "callsite-maps",
            "generated-csv",
            "docs/reverse/generated/*callsite*.csv",
            count_generated(repo, "*callsite*.csv"),
            "metadata-only",
            "source-backed caller/callee context",
            "needs stale-domain coverage comparison",
        ),
        _source(
            "caller-maps",
            "generated-csv",
            "docs/reverse/generated/*caller-map*.csv",
            count_generated(repo, "*caller-map*.csv"),
            "metadata-only",
            "legacy caller mapping context",
            "needs normalization with newer callsite maps",
        ),
        _source(
            "comparison-gates",
            "generated-csv",
            "docs/reverse/generated/*comparison-gate*.csv",
            count_generated(repo, "*comparison-gate*.csv"),
            "metadata-only",
            "blocked comparison readiness decisions",
            "needs source-gap ranking",
        ),
        _source(
            "equivalence-gates",
            "generated-csv",
            "docs/reverse/generated/*equivalence-gate*.csv",
            count_generated(repo, "*equivalence-gate*.csv"),
            "metadata-only",
            "blocked equivalence readiness decisions",
            "needs proof-evidence gap ranking",
        ),
        _source(
            "function-priority",
            "generated-csv",
            PRIORITY,
            count_csv_rows(repo / PRIORITY),
            "metadata-only",
            "closed priority backlog baseline",
            "contains no remaining candidate row",
        ),
        _source(
            "generated-markdown",
            "generated-md",
            "docs/reverse/**/*.md",
            count_reverse_markdown(repo),
            "metadata-only",
            "human-readable proof summaries and blockers",
            "needs machine-readable gap extraction",
        ),
        _source(
            "handoff-csvs",
            "generated-csv",
            "docs/reverse/generated/*handoff*.csv",
            count_generated(repo, "*handoff*.csv"),
            "metadata-only",
            "ticket-to-ticket readiness and closure state",
            "needs consolidated next-input ranking",
        ),
        _source(
            "proof-audits",
            "generated-csv",
            "docs/reverse/generated/*proof*.csv",
            count_generated(repo, "*proof*.csv"),
            "metadata-only",
            "proof-first domain openings and blockers",
            "needs gap severity ranking",
        ),
        _source(
            "repo-function-map",
            "generated-csv",
            SOURCE_MAP,
            count_csv_rows(repo / SOURCE_MAP),
            "metadata-only",
            "authoritative function/domain mapping input",
            "unchanged after RE-291 refresh",
        ),
        _source(
            "selection-gates",
            "generated-csv",
            "docs/reverse/generated/*selection*.csv",
            count_generated(repo, "*selection*.csv"),
            "metadata-only",
            "previous domain and cluster selection decisions",
            "needs re-run only after a new input changes",
        ),
        _source(
            "source-corpus",
            "checked-in-source",
            "GAME|SPEC_*|TOOLS source files",
            count_source_corpus_files(repo),
            "source-symbolic",
            "function names, files, and source-level control context",
            "insufficient alone for binary equivalence readiness",
        ),
        _source(
            "source-patch-gates",
            "generated-csv",
            "docs/reverse/generated/*source-patch-gate*.csv",
            count_generated(repo, "*source-patch-gate*.csv"),
            "metadata-only",
            "source and marker patch denials",
            "needs evidence source ranking before any patch gate can reopen",
        ),
        _source(
            "state-contracts",
            "generated-csv",
            "docs/reverse/generated/*state-contract*.csv",
            count_generated(repo, "*state-contract*.csv"),
            "metadata-only",
            "symbolic state contracts",
            "needs non-raw proof narrowing",
        ),
        _source(
            "story-tracker",
            "story-md",
            "docs/stories/RE-*.md",
            count_story_markdown(repo),
            "metadata-only",
            "progression history and explicit blockers",
            "needs gap extraction into ranked work items",
        ),
    ]
    return sorted(sources, key=lambda row: row.source_id)


def build_inventory(repo: Path) -> InventoryBundle:
    repo = Path(repo)
    validate_re292_handoff(repo)
    sources = build_sources(repo)
    metadata_only = sum(1 for row in sources if row.safety_class == "metadata-only")
    source_symbolic = sum(1 for row in sources if row.safety_class == "source-symbolic")
    raw_or_asset = sum(1 for row in sources if row.safety_class == "raw-or-asset")
    gaps = sum(1 for row in sources if "needs" in row.current_gap or "insufficient" in row.current_gap or "unchanged" in row.current_gap)
    summary = InventorySummary(
        story_id="RE-293",
        topic="evidence-source-inventory",
        upstream_handoff="RE-292",
        source_count=len(sources),
        metadata_only_sources=metadata_only,
        source_symbolic_sources=source_symbolic,
        raw_or_asset_sources=raw_or_asset,
        candidate_gap_count=gaps,
        next_ticket="RE-294",
        next_topic="evidence-source-gap-ranking",
        selected_domain="none",
        selected_pivot="none",
        code_change_readiness="blocked",
        stop_condition="rank existing safe evidence sources before opening a new proof domain",
    )
    return InventoryBundle(sources=sources, summary=summary)


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


def write_markdown(path: Path, bundle: InventoryBundle) -> None:
    summary = bundle.summary
    lines = [
        "# RE-293 evidence source inventory",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-292 blocked handoff validated.",
        "- [x] Safe metadata/source-symbolic evidence sources enumerated.",
        "- [x] Unsafe binary/asset source classes excluded from the inventory.",
        "- [x] Inventory summary and blocked handoff emitted.",
        "",
        "## Summary",
        "",
        f"- Evidence sources inventoried: `{summary.source_count}`",
        f"- Metadata-only sources: `{summary.metadata_only_sources}`",
        f"- Source-symbolic sources: `{summary.source_symbolic_sources}`",
        f"- Raw/asset sources admitted: `{summary.raw_or_asset_sources}`",
        f"- Candidate evidence gaps: `{summary.candidate_gap_count}`",
        "",
        "## Evidence source inventory",
        "",
    ]
    for row in bundle.sources:
        lines.extend(
            [
                f"### {row.source_id}",
                "",
                f"- Type: `{row.source_type}`",
                f"- Pattern: `{row.path_pattern}`",
                f"- Count: `{row.row_or_file_count}`",
                f"- Safety: `{row.safety_class}`",
                f"- Status: `{row.progression_status}`",
                f"- Use: {row.use_for}.",
                f"- Gap: {row.current_gap}.",
                "",
            ]
        )
    lines.extend(
        [
            "## Readiness",
            "",
            f"- Readiness: `{summary.code_change_readiness}`",
            f"- Next ticket: `{summary.next_ticket}`",
            f"- Next topic: `{summary.next_topic}`",
            f"- Selected domain: `{summary.selected_domain}`",
            f"- Selected pivot: `{summary.selected_pivot}`",
            f"- Stop condition: `{summary.stop_condition}`",
            "",
            "No production source or marker change is authorized by this inventory.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story(path: Path, bundle: InventoryBundle) -> None:
    summary = bundle.summary
    lines = [
        "# RE-293 — evidence source inventory",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Inventory the safe source classes that can feed future non-raw proof work after RE-292 left domain selection blocked.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-292 blocked handoff validated.",
        "- [x] Safe evidence sources counted and classified.",
        "- [x] Binary/asset evidence classes excluded from committed outputs.",
        "- [x] Inventory artifacts generated.",
        "- [x] Next gap-ranking objective emitted.",
        "",
        "## Artifacts",
        "",
        f"- Inventory CSV: `{INVENTORY_CSV}`",
        f"- Summary CSV: `{SUMMARY_CSV}`",
        f"- Handoff CSV: `{HANDOFF_CSV}`",
        f"- Markdown: `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- Evidence sources inventoried: `{summary.source_count}`",
        f"- Metadata-only sources: `{summary.metadata_only_sources}`",
        f"- Source-symbolic sources: `{summary.source_symbolic_sources}`",
        f"- Raw/asset sources admitted: `{summary.raw_or_asset_sources}`",
        f"- Candidate evidence gaps: `{summary.candidate_gap_count}`",
        "",
        "The inventory identifies reusable safe inputs, but it does not by itself create new proof readiness or select a domain.",
        "",
        "## Next objective",
        "",
        f"- Next ticket: `{summary.next_ticket}`",
        f"- Topic: `{summary.next_topic}`",
        "- Goal: rank the existing safe evidence sources by which blocker classes they can narrow, then decide whether any follow-up can be testable now without new binary/asset material.",
        "",
        "## Readiness",
        "",
        f"- Readiness: `{summary.code_change_readiness}`",
        f"- Selected domain: `{summary.selected_domain}`",
        f"- Selected pivot: `{summary.selected_pivot}`",
        f"- Stop condition: `{summary.stop_condition}`",
        "",
        "No production source or marker change is authorized by this story.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_all_artifacts(bundle: InventoryBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "inventory_csv": repo / INVENTORY_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_rows(paths["inventory_csv"], bundle.sources)
    write_rows(paths["summary_csv"], [bundle.summary])
    write_rows(paths["handoff_csv"], [bundle.summary])
    write_markdown(paths["md"], bundle)
    write_story(paths["story"], bundle)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", type=Path)
    args = parser.parse_args()
    bundle = build_inventory(args.repo)
    written = write_all_artifacts(bundle, args.repo)
    for name, path in written.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
