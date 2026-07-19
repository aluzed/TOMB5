#!/usr/bin/env python3
"""Gate RE-392 lara-control-service candidate before selecting the next deferred subcluster."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE392_HANDOFF = "docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-handoff.csv"
RE392_CANDIDATES = "docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-candidates.csv"
CANDIDATES_CSV = "docs/reverse/generated/re393-lara-control-service-readiness-gate-candidates.csv"
GATES_CSV = "docs/reverse/generated/re393-lara-control-service-readiness-gate-gates.csv"
SUMMARY_CSV = "docs/reverse/generated/re393-lara-control-service-readiness-gate-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re393-lara-control-service-readiness-gate-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re393-lara-control-service-readiness-gate.md"
STORY = "docs/stories/RE-393-lara-control-service-readiness-gate.md"

SELECTED_SUBCLUSTER = "lara-control-service"
FOLLOWUP_CANDIDATE_ID = "4a632b41837e"
NEXT_TICKET = "RE-394"
NEXT_TOPIC = "lara-combat-camera-post-lara-control-next-subcluster-selection"
LARA_CONTROL_TOKENS = (
    "DelAlignLara",
    "LaraAboveWater",
    "LaraCollide",
    "LaraControl",
    "LaraDoClimb",
    "LaraSurface",
)

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
class LaraControlCandidateGateRow:
    rank: int
    source_rank: int
    candidate_id: str
    selected_narrow_subcluster: str
    bridge_class: str
    body_size_bucket: str
    mapped_caller_count: int
    mapped_callee_count: int
    source_context_count: int
    lara_control_context_count: int
    proof_signal_class: str
    candidate_level_proof: str
    readiness_gate: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    blocker_class: str
    next_probe: str
    stop_condition: str


@dataclass(frozen=True)
class LaraControlReadinessGateRow:
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
class LaraControlReadinessSummary:
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
class LaraControlReadinessBundle:
    candidate_rows: list[LaraControlCandidateGateRow]
    gate_rows: list[LaraControlReadinessGateRow]
    summary: LaraControlReadinessSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def one_row(repo: Path, rel_path: str) -> dict[str, str]:
    rows = read_csv(repo / rel_path)
    if len(rows) != 1:
        raise ValueError(f"{rel_path} must contain exactly one row")
    return rows[0]


def validate_re392_handoff(repo: Path) -> None:
    row = one_row(repo, RE392_HANDOFF)
    expected = {
        "story_id": "RE-392",
        "next_ticket": "RE-393",
        "next_topic": "lara-control-service-readiness-gate",
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
            raise ValueError(f"RE-392 handoff drift: {key}={row.get(key)!r}")


def split_symbols(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def count_lara_control_context(value: str) -> int:
    symbols = split_symbols(value)
    return sum(1 for symbol in symbols if any(token.lower() in symbol.lower() for token in LARA_CONTROL_TOKENS))


def proof_signal_class(row: dict[str, str], lara_count: int) -> str:
    caller_count = int(row["mapped_caller_count"])
    callee_count = int(row["mapped_callee_count"])
    if caller_count and callee_count and lara_count:
        return "caller-callee-lara-control-context-only"
    if caller_count and lara_count:
        return "caller-lara-control-context-only"
    return "broad-lara-control-context-only"


def selected_candidate_rows(repo: Path) -> list[dict[str, str]]:
    rows = read_csv(repo / RE392_CANDIDATES)
    selected = [row for row in rows if row.get("narrow_subcluster") == SELECTED_SUBCLUSTER]
    if [row.get("candidate_id") for row in selected] != [FOLLOWUP_CANDIDATE_ID]:
        raise ValueError("RE-392 lara-control-service candidate set drift")
    for row in selected:
        expected = {
            "readiness_gate": "blocked-needs-candidate-level-proof",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "next_probe": "readiness-gate",
        }
        for key, value in expected.items():
            if row.get(key) != value:
                raise ValueError(f"RE-392 candidate drift: {key}={row.get(key)!r}")
    deferred = [row for row in rows if row.get("narrow_subcluster") != SELECTED_SUBCLUSTER]
    if [row.get("narrow_subcluster") for row in deferred] != ["combat-camera-service"]:
        raise ValueError("RE-392 deferred lara/combat/camera subcluster drift")
    return selected


def build_lara_control_service_readiness_gate(repo: Path) -> LaraControlReadinessBundle:
    repo = Path(repo)
    validate_re392_handoff(repo)
    source_rows = selected_candidate_rows(repo)

    candidate_rows: list[LaraControlCandidateGateRow] = []
    for rank, source in enumerate(source_rows, start=1):
        lara_count = count_lara_control_context(source["representative_source_context"])
        if lara_count == 0:
            raise ValueError(f"Missing lara-control context for {source['candidate_id']}")
        candidate_rows.append(
            LaraControlCandidateGateRow(
                rank=rank,
                source_rank=int(source["source_rank"]),
                candidate_id=source["candidate_id"],
                selected_narrow_subcluster=SELECTED_SUBCLUSTER,
                bridge_class=source["bridge_class"],
                body_size_bucket=source["body_size_bucket"],
                mapped_caller_count=int(source["mapped_caller_count"]),
                mapped_callee_count=int(source["mapped_callee_count"]),
                source_context_count=int(source["source_context_count"]),
                lara_control_context_count=lara_count,
                proof_signal_class=proof_signal_class(source, lara_count),
                candidate_level_proof="no",
                readiness_gate="blocked-no-candidate-level-proof",
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                blocker_class="source-symbolic-lara-control-context-lacks-candidate-proof",
                next_probe="close-lara-control-service-select-next-subcluster",
                stop_condition="candidate-level source-symbolic proof is required before proof-domain selection",
            )
        )

    proof_count = sum(row.candidate_level_proof == "yes" for row in candidate_rows)
    gate_rows = [
        LaraControlReadinessGateRow(
            rank=1,
            gate_class="candidate-level-source-symbolic-proof-missing",
            candidate_count=len(candidate_rows),
            representative_candidates=";".join(row.candidate_id for row in candidate_rows),
            candidate_level_proof_count=proof_count,
            gate_decision="close-subcluster-select-next-deferred-subcluster",
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            next_ticket=NEXT_TICKET,
            next_topic=NEXT_TOPIC,
            stop_condition="lara control service candidate queue exhausted without candidate-level proof",
        )
    ]

    summary = LaraControlReadinessSummary(
        story_id="RE-393",
        topic="lara-control-service-readiness-gate",
        upstream_handoff="RE-392",
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
        stop_condition="lara control service candidate queue exhausted without candidate-level proof; select next deferred lara/combat/camera subcluster",
    )
    return LaraControlReadinessBundle(candidate_rows=candidate_rows, gate_rows=gate_rows, summary=summary)


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


def render_md(bundle: LaraControlReadinessBundle) -> str:
    s = bundle.summary
    text = f"""# RE-393 lara control service readiness gate

## Purpose

Gate the RE-392 `{s.selected_narrow_subcluster}` candidate before any proof-domain or source-patch decision.

## Inputs

- Upstream handoff: `{RE392_HANDOFF}`
- Candidate rows: `{RE392_CANDIDATES}`

## Decision

No proof-domain is reopened by this gate. The selected candidate has source-symbolic lara-control context, but no candidate-level proof rows.

## Counts

- Input candidates: `{s.input_candidate_count}`
- Candidate-level proof rows: `{s.candidate_level_proof_count}`
- Ready to reopen domain: `{s.ready_to_reopen_domain_count}`
- Source patch authorized: `{s.source_patch_authorized_count}`

## Handoff

- Next ticket: `{s.next_ticket}`
- Next topic: `{s.next_topic}`
- Stop condition: `{s.stop_condition}`
"""
    require_metadata_only(text)
    return text


def render_story(bundle: LaraControlReadinessBundle) -> str:
    s = bundle.summary
    text = f"""# RE-393 lara control service readiness gate

## Goal

Gate the RE-392 lara-control-service candidate and decide whether source-symbolic context can reopen a proof domain.

## Inputs

- Upstream handoff: `{RE392_HANDOFF}`
- Candidate rows: `{RE392_CANDIDATES}`

## Progress tracker

- [x] RE-392 lara-control-service handoff validated.
- [x] Selected candidate queue gated fail-closed.
- [x] Source-symbolic lara-control context counted as prioritization signal only.
- [x] Domain and pivot selection kept blocked.
- [x] Source/code patch authorization denied.
- [x] Next deferred lara/combat/camera subcluster selection queued.

## Generated artifacts

- `{CANDIDATES_CSV}`
- `{GATES_CSV}`
- `{SUMMARY_CSV}`
- `{HANDOFF_CSV}`
- `{MD_OUTPUT}`

## Findings

- Selected narrow subcluster: `{s.selected_narrow_subcluster}`
- Input candidate count: `{s.input_candidate_count}`
- Candidate-level proof rows: `{s.candidate_level_proof_count}`
- Ready to reopen domain selection: `{s.ready_to_reopen_domain_count}`
- Source patch authorized rows: `{s.source_patch_authorized_count}`

## Readiness decision

The lara-control-service queue is source-symbolic only. Domain and pivot stay `{s.selected_domain}` / `{s.selected_pivot}`, and code readiness remains `{s.code_change_readiness}` pending candidate-level proof in a later queue.

## Follow-up ticket breakdown

- `{s.next_ticket}` / `{s.next_topic}`: close `{s.selected_narrow_subcluster}` and select the next deferred RE-392 lara/combat/camera subcluster.
  - Inputs: RE-393 handoff and RE-392 narrowed subcluster/candidate CSVs.
  - Deliverables: transition selection rows, summary/handoff, story.
  - Stop condition: select the next deferred subcluster without reopening domain/source/code readiness.

## Validation commands

- `python -m pytest tests/reverse/test_re393_lara_control_service_readiness_gate.py -q`
- `python scripts/reverse/re393_lara_control_service_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
"""
    require_metadata_only(text)
    return text


def write_all_artifacts(bundle: LaraControlReadinessBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    outputs = {
        "candidates_csv": repo / CANDIDATES_CSV,
        "gates_csv": repo / GATES_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_csv(outputs["candidates_csv"], bundle.candidate_rows, LaraControlCandidateGateRow)
    write_csv(outputs["gates_csv"], bundle.gate_rows, LaraControlReadinessGateRow)
    write_csv(outputs["summary_csv"], [bundle.summary], LaraControlReadinessSummary)
    write_csv(outputs["handoff_csv"], [bundle.summary], LaraControlReadinessSummary)
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
    bundle = build_lara_control_service_readiness_gate(args.repo)
    outputs = write_all_artifacts(bundle, args.repo)
    for key, path in outputs.items():
        print(f"{key}: {path.relative_to(args.repo)}")


if __name__ == "__main__":
    main()
