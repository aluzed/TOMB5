#!/usr/bin/env python3
"""Gate RE-378 explosion/flare effect service candidate before reopening a proof domain."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE378_HANDOFF = "docs/reverse/generated/re378-effects-lighting-cluster-post-dynamic-lighting-next-subcluster-selection-handoff.csv"
RE378_CANDIDATES = "docs/reverse/generated/re378-effects-lighting-cluster-post-dynamic-lighting-next-subcluster-selection-candidates.csv"
RE370_CANDIDATES = "docs/reverse/generated/re370-ghidra-effects-lighting-narrow-candidates.csv"
CANDIDATES_CSV = "docs/reverse/generated/re379-explosion-flare-effect-service-readiness-gate-candidates.csv"
GATES_CSV = "docs/reverse/generated/re379-explosion-flare-effect-service-readiness-gate-gates.csv"
SUMMARY_CSV = "docs/reverse/generated/re379-explosion-flare-effect-service-readiness-gate-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re379-explosion-flare-effect-service-readiness-gate-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re379-explosion-flare-effect-service-readiness-gate.md"
STORY = "docs/stories/RE-379-explosion-flare-effect-service-readiness-gate.md"

SELECTED_SUBCLUSTER = "explosion-flare-effect-service"
FOLLOWUP_CANDIDATE_ID = "87d9c8a62335"
EXPLOSION_FLARE_TOKENS = ("Explosion", "Flare", "Flame", "Bubble")
NEXT_TICKET = "RE-380"
NEXT_TOPIC = "explosion-flare-effect-service-candidate-proof-export"

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
class ReadinessCandidateRow:
    rank: int
    source_rank: int
    candidate_id: str
    selected_narrow_subcluster: str
    bridge_class: str
    body_size_bucket: str
    mapped_caller_count: int
    mapped_callee_count: int
    source_context_count: int
    explosion_flare_context_count: int
    proof_signal_class: str
    readiness_gate: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    next_probe: str
    stop_condition: str


@dataclass(frozen=True)
class ReadinessGateRow:
    rank: int
    gate_class: str
    candidate_count: int
    representative_candidates: str
    gate_decision: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    next_ticket: str
    next_topic: str
    stop_condition: str


@dataclass(frozen=True)
class ReadinessSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    selected_narrow_subcluster: str
    input_candidate_count: int
    candidate_gate_count: int
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
class ReadinessBundle:
    candidate_rows: list[ReadinessCandidateRow]
    gate_rows: list[ReadinessGateRow]
    summary: ReadinessSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def one_row(repo: Path, rel_path: str) -> dict[str, str]:
    rows = read_csv(repo / rel_path)
    if len(rows) != 1:
        raise ValueError(f"{rel_path} must contain exactly one row")
    return rows[0]


def validate_re378_handoff(repo: Path) -> None:
    row = one_row(repo, RE378_HANDOFF)
    expected = {
        "story_id": "RE-378",
        "next_ticket": "RE-379",
        "next_topic": SELECTED_SUBCLUSTER + "-readiness-gate",
        "parent_scope": "effects-lighting-cluster",
        "closed_subclusters": "dynamic-lighting-service",
        "selected_narrow_subcluster": SELECTED_SUBCLUSTER,
        "selected_narrow_candidate_count": "1",
        "selected_candidate_ids": FOLLOWUP_CANDIDATE_ID,
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-378 handoff drift: {key}={row.get(key)!r}")


def split_symbols(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def count_explosion_flare_context(value: str) -> int:
    symbols = split_symbols(value)
    return sum(1 for symbol in symbols if any(token.lower() in symbol.lower() for token in EXPLOSION_FLARE_TOKENS))


def proof_signal_class(source_context: str) -> str:
    if count_explosion_flare_context(source_context):
        return "caller-explosion-flare-context-only"
    return "broad-explosion-flare-context-only"


def selected_candidate_rows(repo: Path) -> list[dict[str, str]]:
    rows = read_csv(repo / RE378_CANDIDATES)
    if [row.get("candidate_id") for row in rows] != [FOLLOWUP_CANDIDATE_ID]:
        raise ValueError("RE-378 explosion/flare candidate set drift")
    for row in rows:
        expected = {
            "narrow_subcluster": SELECTED_SUBCLUSTER,
            "readiness_gate": "blocked-needs-candidate-level-proof",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_probe": "candidate-proof-export",
        }
        for key, value in expected.items():
            if row.get(key) != value:
                raise ValueError(f"RE-378 candidate drift: {key}={row.get(key)!r}")
    return rows


def representative_context_by_candidate(repo: Path) -> dict[str, str]:
    rows = read_csv(repo / RE370_CANDIDATES)
    return {row["candidate_id"]: row.get("representative_source_context", "") for row in rows}


def build_explosion_flare_effect_service_readiness_gate(repo: Path) -> ReadinessBundle:
    repo = Path(repo)
    validate_re378_handoff(repo)
    source_rows = selected_candidate_rows(repo)
    context_rows = representative_context_by_candidate(repo)

    candidate_rows: list[ReadinessCandidateRow] = []
    for rank, source in enumerate(source_rows, start=1):
        context = context_rows.get(source["candidate_id"], "")
        if not context:
            raise ValueError(f"Missing source context for {source['candidate_id']}")
        candidate_rows.append(
            ReadinessCandidateRow(
                rank=rank,
                source_rank=int(source["source_rank"]),
                candidate_id=source["candidate_id"],
                selected_narrow_subcluster=SELECTED_SUBCLUSTER,
                bridge_class=source["bridge_class"],
                body_size_bucket=source["body_size_bucket"],
                mapped_caller_count=int(source["mapped_caller_count"]),
                mapped_callee_count=int(source["mapped_callee_count"]),
                source_context_count=int(source["source_context_count"]),
                explosion_flare_context_count=count_explosion_flare_context(context),
                proof_signal_class=proof_signal_class(context),
                readiness_gate="blocked-needs-candidate-level-proof",
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                next_probe="candidate-proof-export",
                stop_condition="candidate-level source-symbolic proof is required before proof-domain selection",
            )
        )

    gate_rows = [
        ReadinessGateRow(
            rank=1,
            gate_class="candidate-level-source-symbolic-proof-missing",
            candidate_count=len(candidate_rows),
            representative_candidates=";".join(row.candidate_id for row in candidate_rows),
            gate_decision="request-still-narrower-export",
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            next_ticket=NEXT_TICKET,
            next_topic=NEXT_TOPIC,
            stop_condition="candidate-level source-symbolic proof is required before proof-domain selection",
        )
    ]

    summary = ReadinessSummary(
        story_id="RE-379",
        topic="explosion-flare-effect-service-readiness-gate",
        upstream_handoff="RE-378",
        selected_narrow_subcluster=SELECTED_SUBCLUSTER,
        input_candidate_count=len(candidate_rows),
        candidate_gate_count=len(gate_rows),
        ready_to_reopen_domain_count=0,
        source_patch_authorized_count=0,
        selected_domain="none",
        selected_pivot="none",
        selected_followup_candidate_id=FOLLOWUP_CANDIDATE_ID,
        next_ticket=NEXT_TICKET,
        next_topic=NEXT_TOPIC,
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="explosion/flare effect candidate lacks candidate-level proof; export still narrower proof context before proof-domain selection",
    )
    return ReadinessBundle(candidate_rows=candidate_rows, gate_rows=gate_rows, summary=summary)


def require_metadata_only(text: str) -> None:
    lowered = text.lower()
    for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
        if fragment in lowered:
            raise ValueError(f"Forbidden raw-evidence fragment in generated output: {fragment}")


def write_csv(path: Path, rows: list[object], row_type: type) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(row_type)], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def render_md(bundle: ReadinessBundle) -> str:
    s = bundle.summary
    text = f"""# RE-379 explosion/flare effect service readiness gate

## Purpose

Gate the RE-378 `{s.selected_narrow_subcluster}` candidate before any proof-domain or source-patch decision.

## Inputs

- Upstream handoff: `{RE378_HANDOFF}`
- Candidate rows: `{RE378_CANDIDATES}`

## Decision

No proof-domain is reopened by this gate. The candidate remains source-symbolic context only because candidate-level proof is still missing.

## Counts

- Input candidates: `{s.input_candidate_count}`
- Gate rows: `{s.candidate_gate_count}`
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


def render_story(bundle: ReadinessBundle) -> str:
    s = bundle.summary
    text = f"""# RE-379 explosion/flare effect service readiness gate

## Goal

Gate the RE-378 `{s.selected_narrow_subcluster}` candidate and decide whether it can reopen proof-domain selection or authorize a source patch.

## Inputs

- Upstream handoff: `{RE378_HANDOFF}`
- Candidate rows: `{RE378_CANDIDATES}`
- Source-context baseline: `{RE370_CANDIDATES}`

## Progress tracker

- [x] RE-378 explosion/flare effect service handoff validated.
- [x] Selected candidate checked for drift.
- [x] Candidate-level proof requirement evaluated.
- [x] Domain/source-patch authorization denied.
- [x] Still-narrower proof export handoff emitted.

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
- Ready to reopen domain selection: `{s.ready_to_reopen_domain_count}`
- Source patch authorized rows: `{s.source_patch_authorized_count}`

## Readiness decision

The `{s.selected_narrow_subcluster}` row remains source-symbolic. Domain and pivot stay `{s.selected_domain}` / `{s.selected_pivot}`, and code readiness remains `{s.code_change_readiness}`.

## Follow-up ticket breakdown

- `{s.next_ticket}` / `{s.next_topic}`: export still-narrower candidate proof context for `{s.selected_followup_candidate_id}`.
  - Inputs: RE-379 candidate/gate CSVs plus RE-370 context.
  - Deliverables: metadata-only proof export, summary/handoff, story.
  - Stop condition: if no candidate-level proof exists, keep source/code readiness blocked and propose the next deferred hypothesis.

## Validation commands

- `python -m pytest tests/reverse/test_re379_explosion_flare_effect_service_readiness_gate.py -q`
- `python scripts/reverse/re379_explosion_flare_effect_service_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
"""
    require_metadata_only(text)
    return text


def write_all_artifacts(bundle: ReadinessBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    outputs = {
        "candidates_csv": repo / CANDIDATES_CSV,
        "gates_csv": repo / GATES_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_csv(outputs["candidates_csv"], bundle.candidate_rows, ReadinessCandidateRow)
    write_csv(outputs["gates_csv"], bundle.gate_rows, ReadinessGateRow)
    write_csv(outputs["summary_csv"], [bundle.summary], ReadinessSummary)
    write_csv(outputs["handoff_csv"], [bundle.summary], ReadinessSummary)
    outputs["md"].parent.mkdir(parents=True, exist_ok=True)
    outputs["md"].write_text(render_md(bundle), encoding="utf-8")
    outputs["story"].parent.mkdir(parents=True, exist_ok=True)
    outputs["story"].write_text(render_story(bundle), encoding="utf-8")
    for path in outputs.values():
        require_metadata_only(path.read_text(encoding="utf-8"))
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".", type=Path)
    args = parser.parse_args()
    bundle = build_explosion_flare_effect_service_readiness_gate(args.repo)
    outputs = write_all_artifacts(bundle, args.repo)
    for key, path in outputs.items():
        print(f"{key}: {path.relative_to(args.repo)}")


if __name__ == "__main__":
    main()
