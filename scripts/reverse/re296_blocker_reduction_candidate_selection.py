#!/usr/bin/env python3
"""Generate RE-296 blocker reduction candidate selection artifacts."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE295_HANDOFF = "docs/reverse/generated/re295-metadata-blocker-extraction-handoff.csv"
RE295_EXTRACTION = "docs/reverse/generated/re295-metadata-blocker-extraction.csv"

CANDIDATE_CSV = "docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv"
SUMMARY_CSV = "docs/reverse/generated/re296-blocker-reduction-candidate-selection-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re296-blocker-reduction-candidate-selection-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re296-blocker-reduction-candidate-selection.md"
STORY = "docs/stories/RE-296-blocker-reduction-candidate-selection.md"

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

NEXT_BY_SOURCE = {
    "story-tracker": (
        "story-tracker-readiness-statement-reduction",
        "normalize story readiness blocker statements before any proof-domain selection",
    ),
    "generated-markdown": (
        "generated-markdown-blocker-taxonomy-reduction",
        "normalize function Markdown blocker taxonomy into reusable metadata classes",
    ),
    "proof-audits": (
        "proof-audit-blocker-taxonomy-reduction",
        "cluster proof-audit blockers by reusable missing-evidence class",
    ),
    "source-patch-gates": (
        "source-patch-gate-denial-reduction",
        "cluster source-patch denial blockers before any source edit",
    ),
    "handoff-csvs": (
        "handoff-stop-condition-reduction",
        "normalize handoff stop conditions before any proof-domain selection",
    ),
}


@dataclass(frozen=True)
class CandidateSelectionRow:
    candidate_id: str
    source_id: str
    source_type: str
    safety_class: str
    blocker_class: str
    dominant_blocker: str
    evidence_count: int
    unique_blocker_count: int
    inherited_reduction_score: int
    selection_score: int
    selection_status: str
    domain_scope: str
    pivot_scope: str
    raw_or_asset_dependency: str
    source_patch_authorized: str
    metadata_candidate_ready: str
    domain_selection_ready: str
    reduction_action: str
    next_ticket: str
    next_topic: str


@dataclass(frozen=True)
class CandidateSelectionSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    source_count: int
    candidate_row_count: int
    selected_candidate_id: str
    selected_source_id: str
    selected_blocker: str
    metadata_candidate_ready_count: int
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
class CandidateSelectionBundle:
    rows: list[CandidateSelectionRow]
    summary: CandidateSelectionSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_re295_handoff(repo: Path) -> dict[str, str]:
    rows = read_csv(repo / RE295_HANDOFF)
    if len(rows) != 1:
        raise ValueError("RE-295 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "story_id": "RE-295",
        "next_ticket": "RE-296",
        "next_topic": "blocker-reduction-candidate-selection",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
        "domain_selection_ready_count": "0",
        "raw_or_asset_source_count": "0",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-295 handoff drift: {key}={row.get(key)!r}")
    return row


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "none"


def score_row(row: dict[str, str]) -> int:
    evidence = int(row["evidence_count"])
    unique = int(row["unique_blocker_count"])
    inherited = int(row["reduction_score"])
    source_bias = {
        "story-tracker": 50,
        "generated-markdown": 40,
        "proof-audits": 30,
        "source-patch-gates": 20,
        "handoff-csvs": 10,
    }.get(row["source_id"], 0)
    return inherited + evidence + unique + source_bias


def candidate_from_re295(row: dict[str, str]) -> CandidateSelectionRow:
    source_id = row["source_id"]
    next_topic, action = NEXT_BY_SOURCE[source_id]
    candidate_id = f"{slugify(source_id)}-{slugify(row['dominant_blocker'])}"
    return CandidateSelectionRow(
        candidate_id=candidate_id,
        source_id=source_id,
        source_type=row["source_type"],
        safety_class=row["safety_class"],
        blocker_class=row["blocker_class"],
        dominant_blocker=row["dominant_blocker"],
        evidence_count=int(row["evidence_count"]),
        unique_blocker_count=int(row["unique_blocker_count"]),
        inherited_reduction_score=int(row["reduction_score"]),
        selection_score=score_row(row),
        selection_status="candidate",
        domain_scope="none",
        pivot_scope="none",
        raw_or_asset_dependency="no",
        source_patch_authorized="no",
        metadata_candidate_ready="yes" if row["metadata_reduction_ready"] == "yes" else "no",
        domain_selection_ready="no",
        reduction_action=action,
        next_ticket="RE-297" if source_id == "story-tracker" else "deferred",
        next_topic=next_topic,
    )


def build_rows(repo: Path) -> list[CandidateSelectionRow]:
    extraction_rows = read_csv(repo / RE295_EXTRACTION)
    if len(extraction_rows) != 5:
        raise ValueError(f"RE-295 extraction drift: expected 5 rows, got {len(extraction_rows)}")
    candidates = [candidate_from_re295(row) for row in extraction_rows]
    if any(row.safety_class == "raw-or-asset" for row in candidates):
        raise ValueError("raw or asset source cannot become a candidate")
    candidates = sorted(candidates, key=lambda row: (-row.selection_score, row.candidate_id))
    selected = candidates[0]
    finalized = []
    for row in candidates:
        if row.candidate_id == selected.candidate_id:
            finalized.append(
                CandidateSelectionRow(
                    **{
                        **asdict(row),
                        "selection_status": "selected",
                        "domain_selection_ready": "no",
                        "next_ticket": "RE-297",
                    }
                )
            )
        else:
            finalized.append(row)
    return finalized


def build_candidate_selection(repo: Path) -> CandidateSelectionBundle:
    repo = Path(repo)
    validate_re295_handoff(repo)
    rows = build_rows(repo)
    selected = rows[0]
    if selected.selection_status != "selected":
        raise ValueError("top candidate must be selected")
    summary = CandidateSelectionSummary(
        story_id="RE-296",
        topic="blocker-reduction-candidate-selection",
        upstream_handoff="RE-295",
        source_count=len(rows),
        candidate_row_count=len(rows),
        selected_candidate_id=selected.candidate_id,
        selected_source_id=selected.source_id,
        selected_blocker=selected.dominant_blocker,
        metadata_candidate_ready_count=sum(1 for row in rows if row.metadata_candidate_ready == "yes"),
        domain_selection_ready_count=sum(1 for row in rows if row.domain_selection_ready == "yes"),
        raw_or_asset_source_count=sum(1 for row in rows if row.safety_class == "raw-or-asset"),
        next_ticket="RE-297",
        next_topic=selected.next_topic,
        selected_domain="none",
        selected_pivot="none",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="reduce selected metadata blocker candidate before reopening any proof domain",
    )
    return CandidateSelectionBundle(rows=rows, summary=summary)


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


def write_markdown(path: Path, bundle: CandidateSelectionBundle) -> None:
    s = bundle.summary
    selected = bundle.rows[0]
    lines = [
        "# RE-296 blocker reduction candidate selection",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-295 blocker extraction handoff validated.",
        "- [x] Metadata-only candidates scored without raw or asset inputs.",
        "- [x] One blocker-reduction candidate selected while proof-domain selection remains blocked.",
        "- [x] Source and marker patch readiness kept blocked.",
        "",
        "## Summary",
        "",
        f"- Candidate rows: `{s.candidate_row_count}`",
        f"- Metadata-ready candidates: `{s.metadata_candidate_ready_count}`",
        f"- Domain-selection-ready candidates: `{s.domain_selection_ready_count}`",
        f"- Raw/asset sources admitted: `{s.raw_or_asset_source_count}`",
        "",
        "## Selected candidate",
        "",
        f"- Candidate ID: `{selected.candidate_id}`",
        f"- Source: `{selected.source_id}`",
        f"- Blocker class: `{selected.blocker_class}`",
        f"- Dominant blocker: `{selected.dominant_blocker}`",
        f"- Evidence count: `{selected.evidence_count}`",
        f"- Unique blocker count: `{selected.unique_blocker_count}`",
        f"- Selection score: `{selected.selection_score}`",
        f"- Reduction action: {selected.reduction_action}.",
        "",
        "## Candidate ranking",
        "",
    ]
    for row in bundle.rows:
        lines.extend(
            [
                f"### {row.candidate_id}",
                "",
                f"- Status: `{row.selection_status}`",
                f"- Score: `{row.selection_score}`",
                f"- Metadata candidate ready: `{row.metadata_candidate_ready}`",
                f"- Domain selection ready: `{row.domain_selection_ready}`",
                f"- Next topic: `{row.next_topic}`",
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
            "No production source or marker change is authorized by this selection.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story(path: Path, bundle: CandidateSelectionBundle) -> None:
    s = bundle.summary
    selected = bundle.rows[0]
    lines = [
        "# RE-296 — blocker reduction candidate selection",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Select the safest metadata-only blocker-reduction candidate from RE-295 before reopening any proof domain or considering source and marker changes.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-295 blocker extraction handoff validated.",
        "- [x] Candidate rows scored from metadata-only extraction rows.",
        "- [x] Selected candidate keeps domain and pivot scope at none.",
        "- [x] Follow-up blocker-reduction ticket emitted.",
        "- [x] Code/source readiness remains blocked.",
        "",
        "## Artifacts",
        "",
        f"- Candidate CSV: `{CANDIDATE_CSV}`",
        f"- Summary CSV: `{SUMMARY_CSV}`",
        f"- Handoff CSV: `{HANDOFF_CSV}`",
        f"- Markdown: `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- Candidate rows: `{s.candidate_row_count}`",
        f"- Selected candidate: `{s.selected_candidate_id}`",
        f"- Selected source: `{s.selected_source_id}`",
        f"- Selected blocker: `{s.selected_blocker}`",
        f"- Metadata-ready candidates: `{s.metadata_candidate_ready_count}`",
        f"- Domain-selection-ready candidates: `{s.domain_selection_ready_count}`",
        f"- Raw/asset sources admitted: `{s.raw_or_asset_source_count}`",
        "",
        "The selected work is intentionally still metadata-only: it narrows repeated readiness language in story trackers, but it does not make domain selection, pivot selection, or source patching ready.",
        "",
        "## Follow-up ticket breakdown",
        "",
        f"### {s.next_ticket} — {s.next_topic}",
        "",
        f"- Goal: {selected.reduction_action}.",
        f"- Inputs: `{CANDIDATE_CSV}`, `{RE295_EXTRACTION}`, story tracker Markdown under `docs/stories/`.",
        "- Deliverables: normalized blocker taxonomy CSV, summary/handoff CSV, story file with progress tracker.",
        "- Validation: targeted pytest, reverse suite, metadata-only forbidden-fragment guard, asset staging guard.",
        "- Stop condition: do not reopen proof-domain selection until the selected metadata blocker has been reduced into reusable classes.",
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


def write_all_artifacts(bundle: CandidateSelectionBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "candidate_csv": repo / CANDIDATE_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_rows(paths["candidate_csv"], bundle.rows)
    write_rows(paths["summary_csv"], [bundle.summary])
    write_rows(paths["handoff_csv"], [bundle.summary])
    write_markdown(paths["md"], bundle)
    write_story(paths["story"], bundle)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", type=Path)
    args = parser.parse_args()
    bundle = build_candidate_selection(args.repo)
    written = write_all_artifacts(bundle, args.repo)
    for name, path in written.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
