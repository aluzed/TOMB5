#!/usr/bin/env python3
"""Generate RE-303 source-patch gate denial reduction artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from collections import defaultdict
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE302_HANDOFF = "docs/reverse/generated/re302-proof-audit-blocker-taxonomy-readiness-gate-handoff.csv"
RE296_CANDIDATES = "docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv"

TAXONOMY_CSV = "docs/reverse/generated/re303-source-patch-gate-denial-reduction.csv"
EVIDENCE_CSV = "docs/reverse/generated/re303-source-patch-gate-denial-reduction-evidence.csv"
SUMMARY_CSV = "docs/reverse/generated/re303-source-patch-gate-denial-reduction-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re303-source-patch-gate-denial-reduction-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re303-source-patch-gate-denial-reduction.md"
STORY = "docs/stories/RE-303-source-patch-gate-denial-reduction.md"

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

NEXT_TICKET = "RE-304"
NEXT_TOPIC = "source-patch-gate-denial-readiness-gate"
SOURCE_ID = "source-patch-gates"
SUPPORTED_DENIAL_FIELDS = ("blocker", "reason", "stop_reason", "dependency", "patch_gate_status", "decision")


@dataclass(frozen=True)
class DenialTaxonomyRow:
    normalized_class: str
    description: str
    evidence_count: int
    source_patch_gate_file_count: int
    unique_denial_count: int
    first_source_patch_gate_file: str
    metadata_reduction_ready: str
    domain_selection_ready: str
    source_patch_authorized: str
    next_action: str


@dataclass(frozen=True)
class DenialEvidenceRow:
    source_patch_gate_file: str
    row_number: int
    normalized_class: str
    denial_fingerprint: str


@dataclass(frozen=True)
class DenialSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    source_patch_gate_file_count: int
    evidence_row_count: int
    normalized_class_count: int
    metadata_reduction_ready_count: int
    domain_selection_ready_count: int
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
class DenialReductionBundle:
    rows: list[DenialTaxonomyRow]
    evidence_rows: list[DenialEvidenceRow]
    summary: DenialSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_re302_handoff(repo: Path) -> None:
    rows = read_csv(repo / RE302_HANDOFF)
    if len(rows) != 1:
        raise ValueError("RE-302 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "story_id": "RE-302",
        "next_ticket": "RE-303",
        "next_topic": "source-patch-gate-denial-reduction",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "raw_or_asset_source_count": "0",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-302 handoff drift: {key}={row.get(key)!r}")


def validate_re296_source_patch_candidate(repo: Path) -> None:
    rows = read_csv(repo / RE296_CANDIDATES)
    matches = [row for row in rows if row["source_id"] == SOURCE_ID]
    if len(matches) != 1:
        raise ValueError("RE-296 source-patch-gates candidate must contain exactly one row")
    row = matches[0]
    expected = {
        "selection_status": "candidate",
        "next_topic": "source-patch-gate-denial-reduction",
        "metadata_candidate_ready": "yes",
        "domain_selection_ready": "no",
        "source_patch_authorized": "no",
        "raw_or_asset_dependency": "no",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-296 source-patch-gates candidate drift: {key}={row.get(key)!r}")


def source_patch_gate_files(repo: Path) -> list[Path]:
    generated = repo / "docs/reverse/generated"
    files = []
    for path in generated.glob("*source-patch-gate*.csv"):
        if re.search(r"re30[3-9]|re3[1-9][0-9]|re[4-9][0-9]{2}", path.name):
            continue
        files.append(path)
    return sorted(files)


def choose_denial_text(row: dict[str, str]) -> str:
    for field in SUPPORTED_DENIAL_FIELDS:
        value = (row.get(field) or "").strip()
        if value:
            return value
    return "generic-source-patch-gate-denial"


def normalize_denial(value: str) -> str:
    low = value.lower()
    if "zero rows passed" in low:
        return "upstream-gate-zero-ready"
    if "symbolic-equivalence" in low:
        return "symbolic-equivalence-proof-missing"
    if "state-contract-and-non-raw" in low or "cross-platform-state-contract" in low:
        return "state-contract-and-non-raw-equivalence-missing"
    if "source-contract-and-non-raw" in low:
        return "source-contract-and-non-raw-equivalence-missing"
    if "non-raw-binary-equivalence" in low or "non-raw-nd-lifecycle-equivalence" in low or "non-raw equivalence" in low:
        return "non-raw-equivalence-proof-missing"
    if "missing-equivalence-proof" in low:
        return "equivalence-proof-missing"
    if ("source-patch" in low and "deny" in low) or "deny-source" in low:
        return "source-patch-denied"
    return "generic-source-patch-gate-denial"


def description_for_class(normalized_class: str) -> str:
    descriptions = {
        "non-raw-equivalence-proof-missing": "Source-patch gates denied by missing non-raw equivalence proof.",
        "upstream-gate-zero-ready": "Source-patch or marker gates denied because an upstream gate produced zero ready rows.",
        "symbolic-equivalence-proof-missing": "Source-patch gates denied by missing symbolic equivalence proof.",
        "state-contract-and-non-raw-equivalence-missing": "Source-patch gates denied by missing state contracts plus non-raw equivalence proof.",
        "source-contract-and-non-raw-equivalence-missing": "Source-patch gates denied by missing source contracts plus non-raw equivalence proof.",
        "equivalence-proof-missing": "Source-patch gates denied by missing equivalence proof metadata.",
        "source-patch-denied": "Source-patch gates explicitly denied source changes without a narrower blocker.",
        "generic-source-patch-gate-denial": "Source-patch gate denial rows reduced to a generic metadata class.",
    }
    return descriptions[normalized_class]


def build_source_patch_gate_denial_reduction(repo: Path) -> DenialReductionBundle:
    repo = Path(repo)
    validate_re302_handoff(repo)
    validate_re296_source_patch_candidate(repo)
    files = source_patch_gate_files(repo)
    if len(files) != 16:
        raise ValueError(f"source-patch gate file drift: expected 16 files, got {len(files)}")

    evidence: list[DenialEvidenceRow] = []
    raw_values_by_class: dict[str, set[str]] = defaultdict(set)
    files_by_class: dict[str, set[str]] = defaultdict(set)
    for path in files:
        rel = str(path.relative_to(repo))
        for row_number, row in enumerate(read_csv(path), start=2):
            denial_text = choose_denial_text(row)
            normalized = normalize_denial(denial_text)
            raw_values_by_class[normalized].add(denial_text)
            files_by_class[normalized].add(rel)
            fingerprint = hashlib.sha256(denial_text.encode("utf-8")).hexdigest()[:16]
            evidence.append(
                DenialEvidenceRow(
                    source_patch_gate_file=rel,
                    row_number=row_number,
                    normalized_class=normalized,
                    denial_fingerprint=fingerprint,
                )
            )
    if len(evidence) != 58:
        raise ValueError(f"source-patch denial row drift: expected 58 rows, got {len(evidence)}")

    counts: dict[str, int] = defaultdict(int)
    for row in evidence:
        counts[row.normalized_class] += 1
    rows = [
        DenialTaxonomyRow(
            normalized_class=normalized_class,
            description=description_for_class(normalized_class),
            evidence_count=count,
            source_patch_gate_file_count=len(files_by_class[normalized_class]),
            unique_denial_count=len(raw_values_by_class[normalized_class]),
            first_source_patch_gate_file=sorted(files_by_class[normalized_class])[0],
            metadata_reduction_ready="yes",
            domain_selection_ready="no",
            source_patch_authorized="no",
            next_action=f"feed {normalized_class} into the source-patch gate denial readiness gate",
        )
        for normalized_class, count in counts.items()
    ]
    rows = sorted(rows, key=lambda row: (-row.evidence_count, row.normalized_class))
    evidence = sorted(evidence, key=lambda row: (row.source_patch_gate_file, row.row_number, row.normalized_class))
    summary = DenialSummary(
        story_id="RE-303",
        topic="source-patch-gate-denial-reduction",
        upstream_handoff="RE-302",
        source_patch_gate_file_count=len(files),
        evidence_row_count=len(evidence),
        normalized_class_count=len(rows),
        metadata_reduction_ready_count=sum(1 for row in rows if row.metadata_reduction_ready == "yes"),
        domain_selection_ready_count=sum(1 for row in rows if row.domain_selection_ready == "yes"),
        source_patch_authorized_count=sum(1 for row in rows if row.source_patch_authorized == "yes"),
        raw_or_asset_source_count=0,
        next_ticket=NEXT_TICKET,
        next_topic=NEXT_TOPIC,
        selected_domain="none",
        selected_pivot="none",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="gate source-patch denial taxonomy before proof-domain selection can reopen",
    )
    return DenialReductionBundle(rows=rows, evidence_rows=evidence, summary=summary)


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


def write_markdown(path: Path, bundle: DenialReductionBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-303 source-patch gate denial reduction",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-302 source-patch denial handoff validated.",
        "- [x] RE-296 source-patch-gates candidate validated.",
        "- [x] Upstream source-patch gate CSVs scanned using supported denial metadata fields only.",
        "- [x] Source-patch denial evidence reduced to hashed metadata classes.",
        "- [x] Proof-domain selection kept blocked pending source-patch denial readiness gate.",
        "",
        "## Reduction summary",
        "",
        f"- Source-patch gate CSV files scanned: `{s.source_patch_gate_file_count}`",
        f"- Evidence rows reduced: `{s.evidence_row_count}`",
        f"- Normalized denial classes: `{s.normalized_class_count}`",
        f"- Metadata-ready classes: `{s.metadata_reduction_ready_count}`",
        f"- Domain-selection-ready classes: `{s.domain_selection_ready_count}`",
        f"- Source patch authorized rows: `{s.source_patch_authorized_count}`",
        "",
        "## Normalized classes",
        "",
    ]
    for row in bundle.rows:
        lines.extend(
            [
                f"### {row.normalized_class}",
                "",
                f"- Evidence count: `{row.evidence_count}`",
                f"- Source-patch gate files: `{row.source_patch_gate_file_count}`",
                f"- Unique denial fingerprints/classes: `{row.unique_denial_count}`",
                f"- Metadata reduction ready: `{row.metadata_reduction_ready}`",
                f"- Domain selection ready: `{row.domain_selection_ready}`",
                f"- Next action: {row.next_action}.",
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


def write_story(path: Path, bundle: DenialReductionBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-303 — source-patch gate denial reduction",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Reduce source-patch gate denial metadata into reusable classes before any source edit or proof-domain selection can reopen.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-302 source-patch denial handoff validated.",
        "- [x] RE-296 deferred source-patch-gates candidate validated.",
        "- [x] Source-patch gate CSV denial metadata normalized.",
        "- [x] Evidence emitted as fingerprints only, without raw denial text.",
        "- [x] Follow-up readiness gate identified.",
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
        f"- Source-patch gate CSV files scanned: `{s.source_patch_gate_file_count}`",
        f"- Evidence rows reduced: `{s.evidence_row_count}`",
        f"- Normalized denial classes: `{s.normalized_class_count}`",
        f"- Domain-selection-ready classes: `{s.domain_selection_ready_count}`",
        f"- Source patch authorized rows: `{s.source_patch_authorized_count}`",
        f"- Raw/asset sources admitted: `{s.raw_or_asset_source_count}`",
        "",
        "The source-patch gate denial taxonomy is metadata-only and keeps source/code readiness blocked until a dedicated readiness gate evaluates the reduced classes.",
        "",
        "## Follow-up ticket breakdown",
        "",
        f"### {s.next_ticket} — {s.next_topic}",
        "",
        "- Goal: gate the reduced source-patch denial taxonomy before proof-domain selection can reopen.",
        f"- Inputs: `{TAXONOMY_CSV}`, `{EVIDENCE_CSV}`, and the prior proof-audit gate artifacts.",
        "- Deliverables: readiness gate CSV, summary/handoff CSV, story file with progress tracker.",
        "- Validation: targeted pytest, reverse suite, metadata-only forbidden-fragment guard, asset staging guard.",
        "- Stop condition: keep selected domain/pivot empty unless non-raw source-patch authorization evidence exists.",
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


def write_all_artifacts(bundle: DenialReductionBundle, repo: Path) -> dict[str, Path]:
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
    write_rows(paths["evidence_csv"], bundle.evidence_rows)
    write_rows(paths["summary_csv"], [bundle.summary])
    write_rows(paths["handoff_csv"], [bundle.summary])
    write_markdown(paths["md"], bundle)
    write_story(paths["story"], bundle)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", type=Path)
    args = parser.parse_args()
    bundle = build_source_patch_gate_denial_reduction(args.repo)
    written = write_all_artifacts(bundle, args.repo)
    for name, path in written.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
