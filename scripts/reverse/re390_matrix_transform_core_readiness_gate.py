#!/usr/bin/env python3
"""Gate RE-389 matrix-transform-core candidates before reopening a proof domain."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE389_HANDOFF = "docs/reverse/generated/re389-ghidra-maths-render-cluster-narrow-handoff.csv"
RE389_CANDIDATES = "docs/reverse/generated/re389-ghidra-maths-render-cluster-narrow-candidates.csv"
CANDIDATES_CSV = "docs/reverse/generated/re390-matrix-transform-core-readiness-gate-candidates.csv"
GATES_CSV = "docs/reverse/generated/re390-matrix-transform-core-readiness-gate-gates.csv"
SUMMARY_CSV = "docs/reverse/generated/re390-matrix-transform-core-readiness-gate-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re390-matrix-transform-core-readiness-gate-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re390-matrix-transform-core-readiness-gate.md"
STORY = "docs/stories/RE-390-matrix-transform-core-readiness-gate.md"

SELECTED_SUBCLUSTER = "matrix-transform-core"
SELECTED_CANDIDATE_IDS = ("cc1a1b589426", "6e9ad2da9fce", "95467f3600d5")
NEXT_TICKET = "RE-391"
NEXT_TOPIC = "post-maths-render-next-ghidra-cluster-selection"
MATRIX_TOKENS = ("mPopMatrix", "mPushMatrix", "mPushUnitMatrix", "mCopyMatrix", "mTranslateXYZ")

FORBIDDEN_OUTPUT_FRAGMENTS = (
    "0x",
    "fun_",
    "word_le_hex",
    "payload_offset",
    "dump row",
    "opcode",
    "machine word",
    "call_address",
    "branch target",
    "call target",
    "hex-address-fragment",
    "raw_evidence",
    "ghidra_entry",
    "ghidra_name",
    "source_line_text",
    "unimplemented();",
)


@dataclass(frozen=True)
class MatrixCandidateGateRow:
    rank: int
    source_rank: int
    candidate_id: str
    selected_narrow_subcluster: str
    bridge_class: str
    body_size_bucket: str
    mapped_caller_count: int
    mapped_callee_count: int
    source_context_count: int
    matrix_context_count: int
    proof_signal_class: str
    candidate_level_proof: str
    readiness_gate: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    blocker_class: str
    next_probe: str
    stop_condition: str


@dataclass(frozen=True)
class MatrixReadinessGateRow:
    rank: int
    gate_class: str
    candidate_count: int
    representative_candidates: str
    candidate_level_proof_count: int
    gate_decision: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    next_ticket: str
    next_topic: str
    stop_condition: str


@dataclass(frozen=True)
class MatrixReadinessSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    selected_narrow_subcluster: str
    input_candidate_count: int
    candidate_gate_count: int
    candidate_level_proof_count: int
    ready_to_reopen_domain_count: int
    source_patch_authorized_count: int
    selected_domain: str
    selected_pivot: str
    selected_followup_candidate_id: str
    next_ticket: str
    next_topic: str
    metadata_work_readiness: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class MatrixReadinessBundle:
    candidate_rows: list[MatrixCandidateGateRow]
    gate_rows: list[MatrixReadinessGateRow]
    summary: MatrixReadinessSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def one_row(repo: Path, rel_path: str) -> dict[str, str]:
    rows = read_csv(repo / rel_path)
    if len(rows) != 1:
        raise ValueError(f"{rel_path} must contain exactly one row")
    return rows[0]


def validate_re389_handoff(repo: Path) -> None:
    row = one_row(repo, RE389_HANDOFF)
    expected = {
        "story_id": "RE-389",
        "next_ticket": "RE-390",
        "next_topic": "matrix-transform-core-readiness-gate",
        "selected_narrow_subcluster": SELECTED_SUBCLUSTER,
        "selected_narrow_candidate_count": "3",
        "selected_candidate_ids": ";".join(SELECTED_CANDIDATE_IDS),
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-389 handoff drift: {key}={row.get(key)!r}")


def split_symbols(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def count_matrix_context(value: str) -> int:
    symbols = split_symbols(value)
    return sum(1 for symbol in symbols if any(token.lower() in symbol.lower() for token in MATRIX_TOKENS))


def proof_signal_class(row: dict[str, str], matrix_count: int) -> str:
    caller_count = int(row["mapped_caller_count"])
    callee_count = int(row["mapped_callee_count"])
    if caller_count and callee_count and matrix_count:
        return "caller-callee-matrix-context-only"
    if callee_count and matrix_count:
        return "callee-matrix-context-only"
    return "broad-matrix-context-only"


def selected_candidate_rows(repo: Path) -> list[dict[str, str]]:
    rows = read_csv(repo / RE389_CANDIDATES)
    if [row.get("candidate_id") for row in rows] != list(SELECTED_CANDIDATE_IDS):
        raise ValueError("RE-389 matrix-transform-core candidate set drift")
    for row in rows:
        expected = {
            "narrow_subcluster": SELECTED_SUBCLUSTER,
            "readiness_gate": "blocked-needs-candidate-level-proof",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_probe": "readiness-gate",
        }
        for key, value in expected.items():
            if row.get(key) != value:
                raise ValueError(f"RE-389 candidate drift: {key}={row.get(key)!r}")
    return rows


def build_matrix_transform_core_readiness_gate(repo: Path) -> MatrixReadinessBundle:
    repo = Path(repo)
    validate_re389_handoff(repo)
    source_rows = selected_candidate_rows(repo)

    candidate_rows: list[MatrixCandidateGateRow] = []
    for rank, source in enumerate(source_rows, start=1):
        matrix_count = count_matrix_context(source["representative_source_context"])
        if matrix_count == 0:
            raise ValueError(f"Missing matrix context for {source['candidate_id']}")
        candidate_rows.append(
            MatrixCandidateGateRow(
                rank=rank,
                source_rank=int(source["source_rank"]),
                candidate_id=source["candidate_id"],
                selected_narrow_subcluster=SELECTED_SUBCLUSTER,
                bridge_class=source["bridge_class"],
                body_size_bucket=source["body_size_bucket"],
                mapped_caller_count=int(source["mapped_caller_count"]),
                mapped_callee_count=int(source["mapped_callee_count"]),
                source_context_count=int(source["source_context_count"]),
                matrix_context_count=matrix_count,
                proof_signal_class=proof_signal_class(source, matrix_count),
                candidate_level_proof="no",
                readiness_gate="blocked-no-candidate-level-proof",
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                blocker_class="source-symbolic-matrix-context-lacks-candidate-proof",
                next_probe="close-matrix-transform-core-subcluster",
                stop_condition="candidate-level source-symbolic proof is required before proof-domain selection",
            )
        )

    proof_count = sum(row.candidate_level_proof == "yes" for row in candidate_rows)
    gate_rows = [
        MatrixReadinessGateRow(
            rank=1,
            gate_class="candidate-level-source-symbolic-proof-missing",
            candidate_count=len(candidate_rows),
            representative_candidates=";".join(row.candidate_id for row in candidate_rows),
            candidate_level_proof_count=proof_count,
            gate_decision="close-subcluster-select-next-deferred-cluster",
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            next_ticket=NEXT_TICKET,
            next_topic=NEXT_TOPIC,
            stop_condition="matrix transform core candidate queue exhausted without candidate-level proof",
        )
    ]

    summary = MatrixReadinessSummary(
        story_id="RE-390",
        topic="matrix-transform-core-readiness-gate",
        upstream_handoff="RE-389",
        selected_narrow_subcluster=SELECTED_SUBCLUSTER,
        input_candidate_count=len(candidate_rows),
        candidate_gate_count=len(gate_rows),
        candidate_level_proof_count=proof_count,
        ready_to_reopen_domain_count=0,
        source_patch_authorized_count=0,
        selected_domain="none",
        selected_pivot="none",
        selected_followup_candidate_id="none",
        next_ticket=NEXT_TICKET,
        next_topic=NEXT_TOPIC,
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="matrix transform core candidate queue exhausted without candidate-level proof; select next deferred bridge cluster",
    )
    return MatrixReadinessBundle(candidate_rows=candidate_rows, gate_rows=gate_rows, summary=summary)


def require_metadata_only(text: str) -> None:
    lowered = text.lower()
    for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
        if fragment in lowered:
            raise ValueError(f"Forbidden raw-evidence fragment in generated output: {fragment}")


def write_csv(path: Path, rows: list[object], row_type: type[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(row_type)], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def render_md(bundle: MatrixReadinessBundle) -> str:
    s = bundle.summary
    text = f"""# RE-390 matrix transform core readiness gate

## Purpose

Gate the RE-389 `{s.selected_narrow_subcluster}` candidate queue before any proof-domain or source-patch decision.

## Inputs

- Upstream handoff: `{RE389_HANDOFF}`
- Candidate rows: `{RE389_CANDIDATES}`

## Decision

No proof-domain is reopened by this gate. The matrix-transform-core rows remain source-symbolic context only because candidate-level proof is still missing.

## Counts

- Input candidates: `{s.input_candidate_count}`
- Gate rows: `{s.candidate_gate_count}`
- Candidate-level proof rows: `{s.candidate_level_proof_count}`
- Ready to reopen domain: `{s.ready_to_reopen_domain_count}`
- Source patch authorized: `{s.source_patch_authorized_count}`

## Handoff

- Selected follow-up candidate: `{s.selected_followup_candidate_id}`
- Next ticket: `{s.next_ticket}`
- Next topic: `{s.next_topic}`
- Code readiness: `{s.code_change_readiness}`
- Stop condition: `{s.stop_condition}`
"""
    require_metadata_only(text)
    return text


def render_story(bundle: MatrixReadinessBundle) -> str:
    s = bundle.summary
    text = f"""# RE-390 matrix transform core readiness gate

## Goal

Gate the RE-389 `{s.selected_narrow_subcluster}` candidates and decide whether any can reopen proof-domain selection or authorize a source patch.

## Inputs

- Upstream handoff: `{RE389_HANDOFF}`
- Candidate rows: `{RE389_CANDIDATES}`

## Progress tracker

- [x] RE-389 matrix-transform-core handoff validated.
- [x] Three matrix-transform-core candidates checked for drift.
- [x] Candidate-level proof requirement evaluated.
- [x] Domain/source-patch authorization denied.
- [x] Next deferred bridge-cluster selection handoff emitted.

## Generated artifacts

- `{CANDIDATES_CSV}`
- `{GATES_CSV}`
- `{SUMMARY_CSV}`
- `{HANDOFF_CSV}`
- `{MD_OUTPUT}`

## Findings

- Selected narrow subcluster: `{s.selected_narrow_subcluster}`
- Input candidates: `{s.input_candidate_count}`
- Gate rows: `{s.candidate_gate_count}`
- Candidate-level proof rows: `{s.candidate_level_proof_count}`
- Ready to reopen domain selection: `{s.ready_to_reopen_domain_count}`
- Source patch authorized rows: `{s.source_patch_authorized_count}`

## Readiness decision

The `{s.selected_narrow_subcluster}` rows remain source-symbolic. Domain and pivot stay `{s.selected_domain}` / `{s.selected_pivot}`, and code readiness remains `{s.code_change_readiness}`.

## Follow-up ticket breakdown

- `{s.next_ticket}` / `{s.next_topic}`: close the maths/render branch and select the next deferred parent bridge cluster.
  - Inputs: RE-390 candidate/gate CSVs plus the parent cluster queue.
  - Deliverables: next-cluster selection rows, summary/handoff, story.
  - Stop condition: if the selected cluster also lacks proof-domain readiness, keep source/code readiness blocked and continue via a narrow export.

## Validation commands

- `python -m pytest tests/reverse/test_re390_matrix_transform_core_readiness_gate.py -q`
- `python scripts/reverse/re390_matrix_transform_core_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
"""
    require_metadata_only(text)
    return text


def write_all_artifacts(bundle: MatrixReadinessBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    outputs = {
        "candidates_csv": repo / CANDIDATES_CSV,
        "gates_csv": repo / GATES_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_csv(outputs["candidates_csv"], bundle.candidate_rows, MatrixCandidateGateRow)
    write_csv(outputs["gates_csv"], bundle.gate_rows, MatrixReadinessGateRow)
    write_csv(outputs["summary_csv"], [bundle.summary], MatrixReadinessSummary)
    write_csv(outputs["handoff_csv"], [bundle.summary], MatrixReadinessSummary)
    outputs["md"].parent.mkdir(parents=True, exist_ok=True)
    outputs["md"].write_text(render_md(bundle), encoding="utf-8")
    outputs["story"].parent.mkdir(parents=True, exist_ok=True)
    outputs["story"].write_text(render_story(bundle), encoding="utf-8")
    for path in outputs.values():
        require_metadata_only(path.read_text(encoding="utf-8"))
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()
    bundle = build_matrix_transform_core_readiness_gate(repo)
    outputs = write_all_artifacts(bundle, repo)
    for label, path in outputs.items():
        print(f"{label}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
