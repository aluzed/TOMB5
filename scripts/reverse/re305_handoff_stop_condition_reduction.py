#!/usr/bin/env python3
"""Generate RE-305 handoff stop-condition reduction artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from collections import defaultdict
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE304_HANDOFF = "docs/reverse/generated/re304-source-patch-gate-denial-readiness-gate-handoff.csv"
RE296_CANDIDATES = "docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv"

TAXONOMY_CSV = "docs/reverse/generated/re305-handoff-stop-condition-reduction.csv"
EVIDENCE_CSV = "docs/reverse/generated/re305-handoff-stop-condition-reduction-evidence.csv"
SUMMARY_CSV = "docs/reverse/generated/re305-handoff-stop-condition-reduction-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re305-handoff-stop-condition-reduction-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re305-handoff-stop-condition-reduction.md"
STORY = "docs/stories/RE-305-handoff-stop-condition-reduction.md"

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

NEXT_TICKET = "RE-306"
NEXT_TOPIC = "handoff-stop-condition-readiness-gate"
SOURCE_ID = "handoff-csvs"
SUPPORTED_STOP_FIELDS = ("stop_condition", "reason", "blocker", "dependency", "outcome")


@dataclass(frozen=True)
class StopConditionTaxonomyRow:
    normalized_class: str
    description: str
    evidence_count: int
    handoff_file_count: int
    unique_stop_condition_count: int
    first_handoff_file: str
    metadata_reduction_ready: str
    domain_selection_ready: str
    source_patch_authorized: str
    next_action: str


@dataclass(frozen=True)
class StopConditionEvidenceRow:
    handoff_file: str
    row_number: int
    source_field: str
    normalized_class: str
    stop_condition_fingerprint: str


@dataclass(frozen=True)
class StopConditionSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    handoff_file_count: int
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
class StopConditionReductionBundle:
    rows: list[StopConditionTaxonomyRow]
    evidence_rows: list[StopConditionEvidenceRow]
    summary: StopConditionSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_re304_handoff(repo: Path) -> None:
    rows = read_csv(repo / RE304_HANDOFF)
    if len(rows) != 1:
        raise ValueError("RE-304 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "story_id": "RE-304",
        "next_ticket": "RE-305",
        "next_topic": "handoff-stop-condition-reduction",
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
            raise ValueError(f"RE-304 handoff drift: {key}={row.get(key)!r}")


def validate_re296_handoff_candidate(repo: Path) -> None:
    rows = read_csv(repo / RE296_CANDIDATES)
    matches = [row for row in rows if row["source_id"] == SOURCE_ID]
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


def handoff_csv_files(repo: Path) -> list[Path]:
    files: list[Path] = []
    for path in (repo / "docs/reverse/generated").glob("*handoff*.csv"):
        match = re.match(r"re(\d+)-", path.name)
        if match and int(match.group(1)) >= 305:
            continue
        files.append(path)
    return sorted(files)


def choose_stop_condition(row: dict[str, str]) -> tuple[str, str]:
    for field in SUPPORTED_STOP_FIELDS:
        value = (row.get(field) or "").strip()
        if value:
            return value, field
    return "generic-handoff-stop-condition", "generic"


def normalize_stop_condition(value: str) -> str:
    low = value.lower()
    if (
        "refresh upstream" in low
        or "changed upstream mapping" in low
        or "changed repo-function-map" in low
        or "function-priority inputs" in low
    ):
        return "upstream-input-refresh-or-change-needed"
    if (
        "before proof-domain selection can reopen" in low
        or "before reopening proof-domain selection" in low
        or "before reopening any proof domain" in low
        or "before selecting a proof domain" in low
        or "before opening a new proof domain" in low
    ):
        return "metadata-reduction-before-domain-selection"
    if "gate " in low or "readiness gate" in low or "taxonomy readiness gate" in low:
        return "readiness-gate-before-domain-selection"
    if "source-patch" in low or "source patch" in low or "source/code readiness" in low or "code-change" in low:
        return "source-patch-or-code-readiness-blocked"
    if "selected by next-cluster gate" in low or "next cluster" in low or "next proof-first audit" in low or "handoff to" in low:
        return "next-domain-or-cluster-handoff"
    if "no source/marker patch" in low or "blocked" in low or "proof" in low:
        return "proof-blocked-or-no-marker-patch"
    return "generic-handoff-stop-condition"


def description_for_class(normalized_class: str) -> str:
    return {
        "proof-blocked-or-no-marker-patch": "Handoff rows closed by proof blockers or no-marker/no-source-patch states.",
        "metadata-reduction-before-domain-selection": "Handoff rows requiring further safe metadata reduction before proof-domain selection.",
        "generic-handoff-stop-condition": "Handoff rows with nonstandard stop-condition wording reduced to a generic metadata class.",
        "upstream-input-refresh-or-change-needed": "Handoff rows requiring changed upstream mapping or new non-raw evidence before a domain can reopen.",
        "readiness-gate-before-domain-selection": "Handoff rows requiring an explicit readiness/selection gate before source changes.",
        "source-patch-or-code-readiness-blocked": "Handoff rows whose stop condition blocks source patch or code-change readiness.",
        "next-domain-or-cluster-handoff": "Handoff rows that route to another proof-first domain or cluster before code changes.",
    }[normalized_class]


def fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def collect_evidence(repo: Path) -> tuple[list[StopConditionEvidenceRow], dict[str, set[str]], dict[str, set[str]]]:
    evidence: list[StopConditionEvidenceRow] = []
    files_by_class: dict[str, set[str]] = defaultdict(set)
    values_by_class: dict[str, set[str]] = defaultdict(set)
    for path in handoff_csv_files(repo):
        rel = path.relative_to(repo).as_posix()
        for row_number, row in enumerate(read_csv(path), start=2):
            value, source_field = choose_stop_condition(row)
            normalized = normalize_stop_condition(value)
            files_by_class[normalized].add(rel)
            values_by_class[normalized].add(value)
            evidence.append(
                StopConditionEvidenceRow(
                    handoff_file=rel,
                    row_number=row_number,
                    source_field=source_field,
                    normalized_class=normalized,
                    stop_condition_fingerprint=fingerprint(value),
                )
            )
    return evidence, files_by_class, values_by_class


def build_handoff_stop_condition_reduction(repo: Path) -> StopConditionReductionBundle:
    repo = Path(repo)
    validate_re304_handoff(repo)
    validate_re296_handoff_candidate(repo)
    files = handoff_csv_files(repo)
    if len(files) != 50:
        raise ValueError(f"handoff file drift: expected 50 files, got {len(files)}")
    evidence, files_by_class, values_by_class = collect_evidence(repo)
    if len(evidence) != 50:
        raise ValueError(f"handoff stop-condition row drift: expected 50 rows, got {len(evidence)}")
    counts: dict[str, int] = defaultdict(int)
    for row in evidence:
        counts[row.normalized_class] += 1
    rows = [
        StopConditionTaxonomyRow(
            normalized_class=normalized_class,
            description=description_for_class(normalized_class),
            evidence_count=count,
            handoff_file_count=len(files_by_class[normalized_class]),
            unique_stop_condition_count=len(values_by_class[normalized_class]),
            first_handoff_file=sorted(files_by_class[normalized_class])[0],
            metadata_reduction_ready="yes",
            domain_selection_ready="no",
            source_patch_authorized="no",
            next_action=f"feed {normalized_class} into the handoff stop-condition readiness gate",
        )
        for normalized_class, count in counts.items()
    ]
    rows = sorted(rows, key=lambda row: (-row.evidence_count, row.normalized_class))
    evidence = sorted(evidence, key=lambda row: (row.handoff_file, row.row_number, row.normalized_class))
    summary = StopConditionSummary(
        story_id="RE-305",
        topic="handoff-stop-condition-reduction",
        upstream_handoff="RE-304",
        handoff_file_count=len(files),
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
        stop_condition="gate handoff stop-condition taxonomy before proof-domain selection can reopen",
    )
    return StopConditionReductionBundle(rows=rows, evidence_rows=evidence, summary=summary)


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


def write_markdown(path: Path, bundle: StopConditionReductionBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-305 handoff stop-condition reduction",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-304 source-patch denial readiness gate handoff validated.",
        "- [x] RE-296 handoff-csvs metadata candidate validated.",
        "- [x] Upstream handoff CSV stop-condition fields reduced to metadata classes.",
        "- [x] Proof-domain selection kept blocked pending handoff stop-condition readiness gate.",
        "",
        "## Reduction decision",
        "",
        f"- Handoff CSV files scanned: `{s.handoff_file_count}`",
        f"- Stop-condition evidence rows: `{s.evidence_row_count}`",
        f"- Normalized stop-condition classes: `{s.normalized_class_count}`",
        f"- Metadata-reduction-ready classes: `{s.metadata_reduction_ready_count}`",
        f"- Ready to reopen proof-domain selection: `{s.domain_selection_ready_count}`",
        f"- Source patch authorized rows: `{s.source_patch_authorized_count}`",
        f"- Next topic: `{s.next_topic}`",
        "",
        "Handoff stop conditions remain metadata-only blockers. They explain why prior epics stopped, but the reduction does not provide non-raw equivalence proof, a selected domain, or source authorization.",
        "",
        "## Taxonomy rows",
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
                f"- First handoff file: `{row.first_handoff_file}`",
                f"- Domain selection ready: `{row.domain_selection_ready}`",
                f"- Source patch authorized: `{row.source_patch_authorized}`",
                f"- Next action: {row.next_action}",
                "",
            ]
        )
    lines.extend(
        [
            "## Readiness decision",
            "",
            "No production source or marker change is authorized by this reduction.",
            "The next safe step is a readiness gate over these handoff stop-condition classes before proof-domain selection can reopen.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story(path: Path, bundle: StopConditionReductionBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-305 handoff stop-condition reduction",
        "",
        "## Goal",
        "",
        "Reduce safe handoff CSV stop-condition metadata into reusable classes before any proof-domain selection can reopen.",
        "",
        "## Inputs",
        "",
        f"- Upstream handoff: `{RE304_HANDOFF}`",
        f"- Candidate source: `{RE296_CANDIDATES}` / `{SOURCE_ID}`",
        "- Scanned source: `docs/reverse/generated/*handoff*.csv` with RE-305+ outputs excluded.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-304 source-patch denial readiness gate handoff validated.",
        "- [x] RE-296 handoff-csvs metadata candidate validated.",
        "- [x] Handoff stop-condition fields normalized without raw text columns.",
        "- [x] Taxonomy, evidence, summary, and handoff artifacts generated.",
        "- [x] Source/code readiness remains blocked.",
        "",
        "## Generated artifacts",
        "",
        f"- `{TAXONOMY_CSV}`",
        f"- `{EVIDENCE_CSV}`",
        f"- `{SUMMARY_CSV}`",
        f"- `{HANDOFF_CSV}`",
        f"- `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- Handoff files scanned: `{s.handoff_file_count}`",
        f"- Stop-condition evidence rows: `{s.evidence_row_count}`",
        f"- Normalized classes: `{s.normalized_class_count}`",
        f"- Domain-selection-ready classes: `{s.domain_selection_ready_count}`",
        f"- Source-patch-authorized classes: `{s.source_patch_authorized_count}`",
        "",
    ]
    for row in bundle.rows:
        lines.append(f"- `{row.normalized_class}`: `{row.evidence_count}` rows, readiness `{row.domain_selection_ready}`.")
    lines.extend(
        [
            "",
            "## Readiness decision",
            "",
            "The handoff stop-condition taxonomy is metadata-reduction-ready but not proof-domain-selection-ready. It does not introduce a selected domain/pivot, non-raw equivalence proof, or source patch authorization.",
            "",
            "## Follow-up ticket breakdown",
            "",
            f"- `{s.next_ticket}` / `{s.next_topic}`: gate the handoff stop-condition taxonomy and decide whether any class can reopen proof-domain selection.",
            "  - Inputs: RE-305 taxonomy, evidence, summary, and handoff artifacts.",
            "  - Deliverables: readiness-gate CSV, summary, handoff, generated Markdown, and story tracker.",
            "  - Stop condition: if all classes remain non-authorizing metadata, keep selected domain/pivot `none` and route to the next safe metadata source or evidence refresh.",
            "",
            "## Validation commands",
            "",
            "- `python -m pytest tests/reverse/test_re305_handoff_stop_condition_reduction.py -q`",
            "- `python scripts/reverse/re305_handoff_stop_condition_reduction.py --repo .`",
            "- `python -m pytest tests/reverse -q`",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_all_artifacts(bundle: StopConditionReductionBundle, repo: Path) -> dict[str, Path]:
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    bundle = build_handoff_stop_condition_reduction(args.repo)
    written = write_all_artifacts(bundle, args.repo)
    for key, path in written.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
