#!/usr/bin/env python3
"""Generate RE-301 proof-audit blocker taxonomy reduction artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from collections import defaultdict
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE300_HANDOFF = "docs/reverse/generated/re300-generated-markdown-blocker-taxonomy-readiness-gate-handoff.csv"
RE296_CANDIDATES = "docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv"

TAXONOMY_CSV = "docs/reverse/generated/re301-proof-audit-blocker-taxonomy-reduction.csv"
EVIDENCE_CSV = "docs/reverse/generated/re301-proof-audit-blocker-taxonomy-reduction-evidence.csv"
SUMMARY_CSV = "docs/reverse/generated/re301-proof-audit-blocker-taxonomy-reduction-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re301-proof-audit-blocker-taxonomy-reduction-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re301-proof-audit-blocker-taxonomy-reduction.md"
STORY = "docs/stories/RE-301-proof-audit-blocker-taxonomy-reduction.md"

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

NEXT_TOPIC = "proof-audit-blocker-taxonomy-readiness-gate"


@dataclass(frozen=True)
class TaxonomyRow:
    normalized_class: str
    description: str
    evidence_count: int
    proof_csv_file_count: int
    unique_blocker_count: int
    first_proof_csv_file: str
    metadata_reduction_ready: str
    domain_selection_ready: str
    source_patch_authorized: str
    next_action: str


@dataclass(frozen=True)
class EvidenceRow:
    proof_csv_file: str
    row_number: int
    normalized_class: str
    blocker_fingerprint: str


@dataclass(frozen=True)
class ReductionSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    proof_csv_file_count: int
    evidence_row_count: int
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
class ReductionBundle:
    rows: list[TaxonomyRow]
    evidence_rows: list[EvidenceRow]
    summary: ReductionSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_re300_handoff(repo: Path) -> None:
    rows = read_csv(repo / RE300_HANDOFF)
    if len(rows) != 1:
        raise ValueError("RE-300 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "story_id": "RE-300",
        "next_ticket": "RE-301",
        "next_topic": "proof-audit-blocker-taxonomy-reduction",
        "selected_domain": "none",
        "selected_pivot": "none",
        "ready_to_reopen_domain_count": "0",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
        "raw_or_asset_source_count": "0",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-300 handoff drift: {key}={row.get(key)!r}")


def validate_re296_candidate(repo: Path) -> None:
    rows = read_csv(repo / RE296_CANDIDATES)
    matches = [row for row in rows if row["source_id"] == "proof-audits"]
    if len(matches) != 1:
        raise ValueError("proof-audits candidate must contain exactly one row")
    row = matches[0]
    expected = {
        "candidate_id": "proof-audits-missing-maths-render-source-contract-and-non-raw-equivalence-proof",
        "selection_status": "candidate",
        "metadata_candidate_ready": "yes",
        "domain_selection_ready": "no",
        "source_patch_authorized": "no",
        "raw_or_asset_dependency": "no",
        "next_topic": "proof-audit-blocker-taxonomy-reduction",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-296 proof-audits candidate drift: {key}={row.get(key)!r}")


def upstream_proof_csvs(repo: Path) -> list[Path]:
    generated = repo / "docs/reverse/generated"
    files: list[Path] = []
    for path in generated.glob("*proof*.csv"):
        match = re.match(r"re(\d+)-", path.name)
        if match and int(match.group(1)) >= 301:
            continue
        files.append(path)
    return sorted(files)


def blocker_value(row: dict[str, str]) -> str:
    for field in ("blocker", "readiness", "next_probe"):
        value = row.get(field, "").strip()
        if value:
            return value
    return "generic-proof-audit-blocker"


def normalize_blocker(value: str) -> str:
    low = value.lower()
    if low == "generic-proof-audit-blocker":
        return "generic-proof-audit-blocker"
    if "row is useful" in low or "support row" in low or "backlog context" in low or "not selected" in low:
        return "backlog-context-not-selected"
    if "nd marker" in low:
        return "marker-behavior-proof-needed"
    if ("source-contract" in low or "source contract" in low) and "non-raw" in low:
        return "source-contract-and-non-raw-equivalence-missing"
    if "state contract" in low and ("symbolic equivalence proof" in low or "equivalence proof" in low):
        return "state-contract-and-symbolic-equivalence-missing"
    if "non-raw equivalence proof" in low:
        return "non-raw-equivalence-proof-missing"
    if (
        "symbolic equivalence proof" in low
        or "source/binary equivalence" in low
        or "behavior/equivalence proof" in low
        or "caller side effects" in low
    ):
        return "symbolic-equivalence-proof-missing"
    if "proof" in low:
        return "proof-evidence-missing"
    return "generic-proof-audit-blocker"


def description_for_class(normalized_class: str) -> str:
    return {
        "source-contract-and-non-raw-equivalence-missing": "Proof-audit rows needing source-contract and non-raw equivalence evidence.",
        "backlog-context-not-selected": "Proof-audit rows retained as backlog/support context rather than selected proof pivots.",
        "proof-evidence-missing": "Proof-audit rows with generic missing proof or proof-first readiness blockers.",
        "state-contract-and-symbolic-equivalence-missing": "Rows needing state contracts plus symbolic equivalence proof.",
        "generic-proof-audit-blocker": "Rows with nonstandard or empty blocker fields reduced to a generic proof-audit class for later gating.",
        "marker-behavior-proof-needed": "Rows where ND marker or marker changes need behavior proof first.",
        "non-raw-equivalence-proof-missing": "Rows specifically blocked on missing non-raw equivalence proof.",
        "symbolic-equivalence-proof-missing": "Rows specifically blocked on symbolic equivalence proof.",
    }[normalized_class]


def fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def collect_evidence(repo: Path) -> tuple[list[EvidenceRow], dict[str, set[str]], dict[str, set[str]]]:
    evidence: list[EvidenceRow] = []
    files_by_class: dict[str, set[str]] = defaultdict(set)
    blockers_by_class: dict[str, set[str]] = defaultdict(set)
    for path in upstream_proof_csvs(repo):
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row_number, row in enumerate(reader, start=2):
                blocker = blocker_value(row)
                normalized = normalize_blocker(blocker)
                rel = path.relative_to(repo).as_posix()
                files_by_class[normalized].add(rel)
                blockers_by_class[normalized].add(blocker)
                evidence.append(
                    EvidenceRow(
                        proof_csv_file=rel,
                        row_number=row_number,
                        normalized_class=normalized,
                        blocker_fingerprint=fingerprint(blocker),
                    )
                )
    return evidence, files_by_class, blockers_by_class


def build_proof_audit_reduction(repo: Path) -> ReductionBundle:
    repo = Path(repo)
    validate_re300_handoff(repo)
    validate_re296_candidate(repo)
    proof_files = upstream_proof_csvs(repo)
    evidence, files_by_class, blockers_by_class = collect_evidence(repo)
    count_by_class: dict[str, int] = defaultdict(int)
    for row in evidence:
        count_by_class[row.normalized_class] += 1
    rows = [
        TaxonomyRow(
            normalized_class=normalized_class,
            description=description_for_class(normalized_class),
            evidence_count=count,
            proof_csv_file_count=len(files_by_class[normalized_class]),
            unique_blocker_count=len(blockers_by_class[normalized_class]),
            first_proof_csv_file=sorted(files_by_class[normalized_class])[0],
            metadata_reduction_ready="yes",
            domain_selection_ready="no",
            source_patch_authorized="no",
            next_action=f"feed {normalized_class} into the proof-audit blocker taxonomy readiness gate",
        )
        for normalized_class, count in count_by_class.items()
    ]
    rows.sort(key=lambda row: (-row.evidence_count, row.normalized_class))
    summary = ReductionSummary(
        story_id="RE-301",
        topic="proof-audit-blocker-taxonomy-reduction",
        upstream_handoff="RE-300",
        proof_csv_file_count=len(proof_files),
        evidence_row_count=len(evidence),
        normalized_class_count=len(rows),
        metadata_reduction_ready_count=sum(1 for row in rows if row.metadata_reduction_ready == "yes"),
        domain_selection_ready_count=sum(1 for row in rows if row.domain_selection_ready == "yes"),
        raw_or_asset_source_count=0,
        next_ticket="RE-302",
        next_topic=NEXT_TOPIC,
        selected_domain="none",
        selected_pivot="none",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="gate proof-audit taxonomy before proof-domain selection can reopen",
    )
    return ReductionBundle(rows=rows, evidence_rows=evidence, summary=summary)


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


def write_markdown(path: Path, bundle: ReductionBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-301 proof-audit blocker taxonomy reduction",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-300 proof-audit handoff validated.",
        "- [x] RE-296 proof-audits candidate validated as safe metadata work.",
        "- [x] Proof-audit CSV blockers normalized into reusable metadata classes.",
        "- [x] Evidence rows emitted as fingerprints only, with no blocker text.",
        "- [x] Code/source readiness remains blocked.",
        "",
        "## Summary",
        "",
        f"- Proof CSV files scanned: `{s.proof_csv_file_count}`",
        f"- Evidence rows reduced: `{s.evidence_row_count}`",
        f"- Normalized classes: `{s.normalized_class_count}`",
        f"- Metadata-ready classes: `{s.metadata_reduction_ready_count}`",
        f"- Domain-selection-ready classes: `{s.domain_selection_ready_count}`",
        f"- Raw/asset sources admitted: `{s.raw_or_asset_source_count}`",
        "",
        "## Taxonomy rows",
        "",
    ]
    for row in bundle.rows:
        lines.extend([
            f"### {row.normalized_class}",
            "",
            f"- Evidence count: `{row.evidence_count}`",
            f"- Proof CSV files: `{row.proof_csv_file_count}`",
            f"- Unique blocker fingerprints/classes: `{row.unique_blocker_count}`",
            f"- Description: {row.description}",
            f"- Domain selection ready: `{row.domain_selection_ready}`",
            "",
        ])
    lines.extend([
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
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story(path: Path, bundle: ReductionBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-301 — proof-audit blocker taxonomy reduction",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Normalize proof-audit blocker rows into reusable metadata classes without reopening proof-domain selection.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-300 proof-audit handoff validated.",
        "- [x] RE-296 proof-audits candidate validated.",
        "- [x] Upstream proof CSV rows reduced to hashed metadata evidence.",
        "- [x] Normalized proof-audit blocker taxonomy emitted.",
        "- [x] Proof-domain selection kept blocked until a readiness gate runs.",
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
        f"- Proof CSV files scanned: `{s.proof_csv_file_count}`",
        f"- Evidence rows reduced: `{s.evidence_row_count}`",
        f"- Normalized classes: `{s.normalized_class_count}`",
        f"- Metadata-ready classes: `{s.metadata_reduction_ready_count}`",
        f"- Domain-selection-ready classes: `{s.domain_selection_ready_count}`",
        f"- Raw/asset sources admitted: `{s.raw_or_asset_source_count}`",
        "",
        "The reduction consolidates proof-audit blockers, but the taxonomy remains a missing-evidence inventory rather than proof-domain readiness.",
        "",
        "## Follow-up ticket breakdown",
        "",
        f"### {s.next_ticket} — {s.next_topic}",
        "",
        "- Goal: gate the proof-audit blocker taxonomy and decide whether any non-raw metadata can reopen proof-domain selection.",
        f"- Inputs: `{TAXONOMY_CSV}`, `{EVIDENCE_CSV}`, `{HANDOFF_CSV}`.",
        "- Deliverables: readiness-gate CSV, summary/handoff CSV, story file with progress tracker.",
        "- Validation: targeted pytest, reverse suite, metadata-only forbidden-fragment guard, asset staging guard.",
        "- Stop condition: keep proof-domain selection blocked unless a non-raw proof-domain selection step is justified.",
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


def write_all_artifacts(bundle: ReductionBundle, repo: Path) -> dict[str, Path]:
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
    bundle = build_proof_audit_reduction(args.repo)
    written = write_all_artifacts(bundle, args.repo)
    for name, path in written.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
