#!/usr/bin/env python3
"""Gate RE-343 cd/load/audio service candidates before reopening a proof domain."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE343_HANDOFF = "docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-handoff.csv"
RE343_CANDIDATES = "docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-candidates.csv"
CANDIDATES_CSV = "docs/reverse/generated/re344-cd-load-audio-service-readiness-gate-candidates.csv"
GATES_CSV = "docs/reverse/generated/re344-cd-load-audio-service-readiness-gate-gates.csv"
SUMMARY_CSV = "docs/reverse/generated/re344-cd-load-audio-service-readiness-gate-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re344-cd-load-audio-service-readiness-gate-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re344-cd-load-audio-service-readiness-gate.md"
STORY = "docs/stories/RE-344-cd-load-audio-service-readiness-gate.md"

SELECTED_SUBCLUSTER = "cd-load-audio-service"
FOLLOWUP_CANDIDATE_ID = "1e35f3f4fb97"
FOLLOWUP_CANDIDATE_IDS = ("1e35f3f4fb97", "653df7c5909b")
CD_LOAD_AUDIO_TOKENS = ("CDFS", "CD", "LOAD", "Play", "Stop")

FORBIDDEN_OUTPUT_FRAGMENTS = (
    "0x",
    "fun_",
    "sub_",
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
    cd_load_audio_context_count: int
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


def validate_re343_handoff(repo: Path) -> None:
    row = one_row(repo, RE343_HANDOFF)
    expected = {
        "story_id": "RE-343",
        "next_ticket": "RE-344",
        "next_topic": "cd-load-audio-service-readiness-gate",
        "selected_narrow_subcluster": SELECTED_SUBCLUSTER,
        "selected_narrow_candidate_count": "2",
        "selected_candidate_ids": ";".join(FOLLOWUP_CANDIDATE_IDS),
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "selected_domain": "none",
        "selected_pivot": "none",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-343 handoff drift: {key}={row.get(key)!r}")


def split_symbols(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def count_cd_load_audio_context(value: str) -> int:
    symbols = split_symbols(value)
    return sum(1 for symbol in symbols if any(token.lower() in symbol.lower() for token in CD_LOAD_AUDIO_TOKENS))


def proof_signal_class(row: dict[str, str]) -> str:
    caller_hits = count_cd_load_audio_context(row.get("representative_source_context", ""))
    if caller_hits:
        return "caller-cd-load-audio-context-only"
    return "broad-cd-load-audio-context-only"


def selected_candidate_rows(repo: Path) -> list[dict[str, str]]:
    rows = [
        row
        for row in read_csv(repo / RE343_CANDIDATES)
        if row.get("narrow_subcluster") == SELECTED_SUBCLUSTER
    ]
    rows.sort(key=lambda row: int(row["rank"]))
    if [row.get("candidate_id") for row in rows] != list(FOLLOWUP_CANDIDATE_IDS):
        raise ValueError("RE-343 cd-load-audio candidate set drift")
    for row in rows:
        expected = {
            "readiness_gate": "blocked-needs-candidate-level-proof",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
        }
        for key, value in expected.items():
            if row.get(key) != value:
                raise ValueError(f"RE-343 candidate drift: {row.get('candidate_id')} {key}={row.get(key)!r}")
    return rows


def build_cd_load_audio_service_readiness_gate(repo: Path) -> ReadinessBundle:
    repo = Path(repo)
    validate_re343_handoff(repo)
    source_rows = selected_candidate_rows(repo)

    candidate_rows: list[ReadinessCandidateRow] = []
    for rank, source in enumerate(source_rows, start=1):
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
                cd_load_audio_context_count=count_cd_load_audio_context(source.get("representative_source_context", "")),
                proof_signal_class=proof_signal_class(source),
                readiness_gate="blocked-needs-candidate-level-proof",
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                next_probe="candidate-proof-export" if source["candidate_id"] == FOLLOWUP_CANDIDATE_ID else "defer-after-re345",
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
            next_ticket="RE-345",
            next_topic="cd-load-audio-service-candidate-proof-export",
            stop_condition="candidate-level source-symbolic proof is required before proof-domain selection",
        )
    ]

    summary = ReadinessSummary(
        story_id="RE-344",
        topic="cd-load-audio-service-readiness-gate",
        upstream_handoff="RE-343",
        selected_narrow_subcluster=SELECTED_SUBCLUSTER,
        input_candidate_count=len(candidate_rows),
        candidate_gate_count=len(gate_rows),
        ready_to_reopen_domain_count=0,
        source_patch_authorized_count=0,
        selected_domain="none",
        selected_pivot="none",
        selected_followup_candidate_id=FOLLOWUP_CANDIDATE_ID,
        next_ticket="RE-345",
        next_topic="cd-load-audio-service-candidate-proof-export",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="cd/load/audio candidates lack candidate-level proof; export still narrower proof context before proof-domain selection",
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
    text = f"""# RE-344 cd-load-audio service readiness gate

## Purpose

Gate the RE-343 `{s.selected_narrow_subcluster}` candidate set before any proof-domain or source-patch decision.

## Inputs

- Upstream handoff: `{RE343_HANDOFF}`
- Candidate rows: `{RE343_CANDIDATES}`

## Decision

No proof-domain is reopened by this gate. The candidates remain source-symbolic context only because candidate-level proof is still missing.

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
    text = f"""# RE-344 cd-load-audio service readiness gate

## Goal

Gate the RE-343 `{s.selected_narrow_subcluster}` candidates and decide whether any row can reopen proof-domain selection or authorize a source patch.

## Inputs

- Upstream handoff: `{RE343_HANDOFF}`
- Candidate rows: `{RE343_CANDIDATES}`

## Progress tracker

- [x] RE-343 cd-load-audio service handoff validated.
- [x] Selected candidate set checked for drift.
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

The `{s.selected_narrow_subcluster}` rows remain source-symbolic. Domain and pivot stay `{s.selected_domain}` / `{s.selected_pivot}`, and code readiness remains `{s.code_change_readiness}`.

## Follow-up ticket breakdown

- `{s.next_ticket}` / `{s.next_topic}`: export still-narrower candidate proof context for `{s.selected_followup_candidate_id}`.
  - Inputs: RE-344 candidate/gate CSVs plus RE-343 context.
  - Deliverables: metadata-only proof export, summary/handoff, story.
  - Stop condition: if no candidate-level proof exists, keep source/code readiness blocked and propose the next deferred hypothesis.

## Validation commands

- `python -m pytest tests/reverse/test_re344_cd_load_audio_service_readiness_gate.py -q`
- `python scripts/reverse/re344_cd_load_audio_service_readiness_gate.py --repo .`
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
    bundle = build_cd_load_audio_service_readiness_gate(args.repo)
    outputs = write_all_artifacts(bundle, args.repo)
    for key, path in outputs.items():
        print(f"{key}: {path.relative_to(args.repo)}")


if __name__ == "__main__":
    main()
