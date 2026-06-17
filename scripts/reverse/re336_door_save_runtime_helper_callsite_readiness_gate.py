#!/usr/bin/env python3
"""Generate RE-336 callsite-family readiness gate metadata for the door-save-runtime helper candidate."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE335_HANDOFF = "docs/reverse/generated/re335-door-save-runtime-helper-candidate-callsite-handoff.csv"
RE335_FUNCTIONS = "docs/reverse/generated/re335-door-save-runtime-helper-candidate-callsite-functions.csv"
RE335_CALLSITES = "docs/reverse/generated/re335-door-save-runtime-helper-candidate-callsite-map.csv"
RE333_CANDIDATES = "docs/reverse/generated/re333-door-save-runtime-helper-readiness-gate-candidates.csv"
FAMILIES_CSV = "docs/reverse/generated/re336-door-save-runtime-helper-callsite-readiness-families.csv"
DECISION_CSV = "docs/reverse/generated/re336-door-save-runtime-helper-callsite-readiness-decision.csv"
SUMMARY_CSV = "docs/reverse/generated/re336-door-save-runtime-helper-callsite-readiness-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re336-door-save-runtime-helper-callsite-readiness-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re336-door-save-runtime-helper-callsite-readiness-gate.md"
STORY = "docs/stories/RE-336-door-save-runtime-helper-callsite-readiness-gate.md"

SELECTED_CANDIDATE_ID = "f457f2772655"
NEXT_CANDIDATE_ID = "none"
FAMILY_ORDER = (
    "platform-cd-helper",
    "camera-runtime-helper",
    "savegame-memory-helper",
    "platform-file-helper",
    "lara-state-helper",
    "collision-trigger-helper",
    "level-runtime-helper",
    "frontend-runtime-helper",
    "gameflow-load-helper",
    "audio-helper",
    "address-derived-symbol-omitted",
    "stub-marker",
    "other",
)
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
class CallsiteFamilyGateRow:
    rank: int
    candidate_id: str
    callsite_family: str
    source_backed_callsite_count: int
    implemented_callsite_count: int
    stub_callsite_count: int
    caller_count: int
    implemented_caller_count: int
    candidate_level_proof: str
    readiness_gate: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    blocker_class: str
    next_probe: str


@dataclass(frozen=True)
class CallsiteReadinessDecisionRow:
    rank: int
    candidate_id: str
    callsite_family_count: int
    implemented_callsite_family_count: int
    candidate_level_proof_count: int
    readiness_gate: str
    decision: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    selected_domain: str
    selected_pivot: str
    next_ticket: str
    next_topic: str
    next_candidate_id: str
    stop_condition: str


@dataclass(frozen=True)
class CallsiteReadinessSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    selected_candidate_id: str
    source_context_function_count: int
    source_backed_callsite_count: int
    callsite_family_count: int
    implemented_callsite_family_count: int
    stub_only_callsite_family_count: int
    candidate_level_proof_count: int
    ready_to_reopen_domain_count: int
    source_patch_authorized_count: int
    selected_domain: str
    selected_pivot: str
    next_ticket: str
    next_topic: str
    next_candidate_id: str
    metadata_work_readiness: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class CallsiteReadinessBundle:
    family_rows: list[CallsiteFamilyGateRow]
    decision_rows: list[CallsiteReadinessDecisionRow]
    summary: CallsiteReadinessSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def one_row(repo: Path, rel_path: str) -> dict[str, str]:
    rows = read_csv(repo / rel_path)
    if len(rows) != 1:
        raise ValueError(f"{rel_path} must contain exactly one row")
    return rows[0]


def validate_re335_handoff(repo: Path) -> None:
    row = one_row(repo, RE335_HANDOFF)
    expected = {
        "story_id": "RE-335",
        "next_ticket": "RE-336",
        "next_topic": "door-save-runtime-helper-callsite-readiness-gate",
        "selected_candidate_id": SELECTED_CANDIDATE_ID,
        "source_context_function_count": "14",
        "source_backed_callsite_count": "185",
        "implemented_context_function_count": "13",
        "stub_context_function_count": "1",
        "no_callsite_context_function_count": "0",
        "candidate_level_proof_count": "0",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-335 handoff drift: {key}={row.get(key)!r}")


def validate_single_candidate_queue(repo: Path) -> None:
    rows = read_csv(repo / RE333_CANDIDATES)
    candidate_ids = [row.get("candidate_id") for row in rows]
    if candidate_ids != [SELECTED_CANDIDATE_ID]:
        raise ValueError(f"RE-333 door-save-runtime candidate queue drift: {candidate_ids!r}")
    row = rows[0]
    expected = {
        "selected_narrow_subcluster": "door-save-runtime-helper",
        "ready_to_reopen_domain": "no",
        "source_patch_authorized": "no",
        "next_probe": "candidate-proof-export",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-333 candidate queue drift: {key}={row.get(key)!r}")


def build_family_rows(callsite_rows: list[dict[str, str]]) -> list[CallsiteFamilyGateRow]:
    by_family: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in callsite_rows:
        if row.get("candidate_id") != SELECTED_CANDIDATE_ID:
            raise ValueError("RE-335 callsite candidate set drift")
        by_family[row["callsite_family"]].append(row)

    if set(by_family) != set(FAMILY_ORDER):
        raise ValueError(f"Unexpected callsite families: {sorted(by_family)}")

    family_rows: list[CallsiteFamilyGateRow] = []
    for rank, family in enumerate(FAMILY_ORDER, start=1):
        rows = by_family.get(family, [])
        if not rows:
            raise ValueError(f"Missing callsite family {family}")
        statuses = Counter(row["function_status"] for row in rows)
        unexpected_statuses = sorted(set(statuses) - {"source-with-calls", "stub-unimplemented"})
        if unexpected_statuses:
            raise ValueError(f"Unexpected function statuses for {family}: {unexpected_statuses!r}")
        callers = {row["caller_symbol"] for row in rows}
        implemented_callers = {row["caller_symbol"] for row in rows if row["function_status"] == "source-with-calls"}
        implemented_count = statuses.get("source-with-calls", 0)
        stub_count = statuses.get("stub-unimplemented", 0)
        if implemented_count and stub_count:
            raise ValueError(f"Mixed implemented/stub callsite family {family}")
        if implemented_count:
            readiness_gate = "blocked-no-candidate-level-proof"
            blocker_class = "implemented-family-lacks-candidate-level-proof"
        else:
            readiness_gate = "blocked-stub-only-family"
            blocker_class = "stub-only-callsite-family"
        family_rows.append(
            CallsiteFamilyGateRow(
                rank=rank,
                candidate_id=SELECTED_CANDIDATE_ID,
                callsite_family=family,
                source_backed_callsite_count=len(rows),
                implemented_callsite_count=implemented_count,
                stub_callsite_count=stub_count,
                caller_count=len(callers),
                implemented_caller_count=len(implemented_callers),
                candidate_level_proof="no",
                readiness_gate=readiness_gate,
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                blocker_class=blocker_class,
                next_probe="candidate-queue-exhausted",
            )
        )
    return family_rows


def build_door_save_runtime_helper_callsite_readiness_gate(repo: Path) -> CallsiteReadinessBundle:
    repo = Path(repo)
    validate_re335_handoff(repo)
    validate_single_candidate_queue(repo)
    function_rows = read_csv(repo / RE335_FUNCTIONS)
    callsite_rows = read_csv(repo / RE335_CALLSITES)
    if len(function_rows) != 14:
        raise ValueError(f"Expected 14 RE-335 function rows, got {len(function_rows)}")
    if len(callsite_rows) != 185:
        raise ValueError(f"Expected 185 RE-335 callsite rows, got {len(callsite_rows)}")
    if any(row.get("candidate_id") != SELECTED_CANDIDATE_ID for row in function_rows + callsite_rows):
        raise ValueError("RE-335 candidate set drift")

    family_rows = build_family_rows(callsite_rows)
    implemented_family_count = sum(row.implemented_callsite_count > 0 for row in family_rows)
    stub_only_family_count = sum(row.implemented_callsite_count == 0 for row in family_rows)
    candidate_level_proof_count = sum(row.candidate_level_proof == "yes" for row in family_rows)
    ready_count = sum(row.ready_to_reopen_domain == "yes" for row in family_rows)
    source_patch_count = sum(row.source_patch_authorized == "yes" for row in family_rows)

    decision_rows = [
        CallsiteReadinessDecisionRow(
            rank=1,
            candidate_id=SELECTED_CANDIDATE_ID,
            callsite_family_count=len(family_rows),
            implemented_callsite_family_count=implemented_family_count,
            candidate_level_proof_count=candidate_level_proof_count,
            readiness_gate="blocked-single-candidate-queue-exhausted",
            decision="deny-domain-reopen-and-exhaust-candidate-queue",
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            selected_domain="none",
            selected_pivot="none",
            next_ticket="TBD",
            next_topic="door-save-runtime-helper-candidate-queue-exhausted",
            next_candidate_id=NEXT_CANDIDATE_ID,
            stop_condition="single door-save-runtime helper candidate has source-backed callsites but no candidate-level proof; candidate queue exhausted",
        )
    ]

    summary = CallsiteReadinessSummary(
        story_id="RE-336",
        topic="door-save-runtime-helper-callsite-readiness-gate",
        upstream_handoff="RE-335",
        selected_candidate_id=SELECTED_CANDIDATE_ID,
        source_context_function_count=len(function_rows),
        source_backed_callsite_count=len(callsite_rows),
        callsite_family_count=len(family_rows),
        implemented_callsite_family_count=implemented_family_count,
        stub_only_callsite_family_count=stub_only_family_count,
        candidate_level_proof_count=candidate_level_proof_count,
        ready_to_reopen_domain_count=ready_count,
        source_patch_authorized_count=source_patch_count,
        selected_domain="none",
        selected_pivot="none",
        next_ticket="TBD",
        next_topic="door-save-runtime-helper-candidate-queue-exhausted",
        next_candidate_id=NEXT_CANDIDATE_ID,
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="door-save-runtime helper callsite readiness gate denied the single candidate; candidate queue exhausted",
    )
    return CallsiteReadinessBundle(family_rows=family_rows, decision_rows=decision_rows, summary=summary)


def write_csv(path: Path, rows: list[object], row_type: type[object]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(row_type)], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
    return path


def assert_metadata_only(paths: list[Path]) -> None:
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            if fragment in text:
                raise ValueError(f"Forbidden output fragment {fragment!r} in {path}")


def render_markdown(bundle: CallsiteReadinessBundle) -> str:
    rows = "\n".join(
        f"- `{row.callsite_family}`: `{row.source_backed_callsite_count}` rows, gate `{row.readiness_gate}`."
        for row in bundle.family_rows
    )
    return f"""# RE-336 door-save-runtime helper callsite readiness gate

## Summary

Gated `{bundle.summary.callsite_family_count}` source-backed callsite families for candidate `{bundle.summary.selected_candidate_id}`.
No door-save-runtime callsite family proves candidate-level behavior, so the proof domain and pivot remain `none`.

## Family gates

{rows}

## Readiness decision

- candidate-level proof rows: `{bundle.summary.candidate_level_proof_count}`
- ready-to-reopen rows: `{bundle.summary.ready_to_reopen_domain_count}`
- source-patch authorized rows: `{bundle.summary.source_patch_authorized_count}`
- next candidate: `{bundle.summary.next_candidate_id}`
- next ticket: `{bundle.summary.next_ticket}` / `{bundle.summary.next_topic}`

Code readiness remains `blocked`.
"""


def render_story(bundle: CallsiteReadinessBundle) -> str:
    return f"""# RE-336 door-save-runtime helper callsite readiness gate

## Goal

Gate the RE-335 source-backed callsite map and decide whether any door-save-runtime callsite family can reopen a proof domain or authorize a source patch.

## Inputs

- Upstream handoff: `{RE335_HANDOFF}`
- Source-backed callsite map: `{RE335_CALLSITES}`
- Source context functions: `{RE335_FUNCTIONS}`
- Candidate queue: `{RE333_CANDIDATES}`

## Progress tracker

- [x] RE-335 callsite handoff validated.
- [x] RE-333 single-candidate queue verified fail-closed.
- [x] Door-save-runtime callsite families grouped and readiness-gated.
- [x] Candidate-level proof and source-patch authorization denied for every family.
- [x] Candidate queue exhaustion handoff emitted.

## Generated artifacts

- `{FAMILIES_CSV}`
- `{DECISION_CSV}`
- `{SUMMARY_CSV}`
- `{HANDOFF_CSV}`
- `{MD_OUTPUT}`

## Findings

- Source context functions: `{bundle.summary.source_context_function_count}`
- Source-backed callsite rows: `{bundle.summary.source_backed_callsite_count}`
- Callsite families: `{bundle.summary.callsite_family_count}`
- Implemented callsite families: `{bundle.summary.implemented_callsite_family_count}`
- Stub-only callsite families: `{bundle.summary.stub_only_callsite_family_count}`
- Candidate-level proof rows: `{bundle.summary.candidate_level_proof_count}`
- Ready to reopen domain selection: `{bundle.summary.ready_to_reopen_domain_count}`
- Source patch authorized rows: `{bundle.summary.source_patch_authorized_count}`

## Readiness decision

No RE-335 door-save-runtime callsite family proves candidate-level behavior. Domain and pivot stay `none`; source/code readiness remains `blocked`, and the candidate queue is exhausted.

## Follow-up ticket breakdown

- `TBD` / `door-save-runtime-helper-candidate-queue-exhausted`: no remaining deferred door-save-runtime helper candidate exists after `{bundle.summary.selected_candidate_id}`.
  - Inputs: RE-333 candidate queue and RE-336 denial handoff.
  - Deliverables: await next parent-subcluster selection or changed non-raw candidate-level proof evidence before reopening domain selection.
  - Stop condition: candidate queue is exhausted and source/code readiness remains blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re336_door_save_runtime_helper_callsite_readiness_gate.py -q`
- `python scripts/reverse/re336_door_save_runtime_helper_callsite_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
"""


def write_all_artifacts(bundle: CallsiteReadinessBundle, repo: Path) -> dict[str, Path]:
    written = {
        "families_csv": write_csv(repo / FAMILIES_CSV, bundle.family_rows, CallsiteFamilyGateRow),
        "decision_csv": write_csv(repo / DECISION_CSV, bundle.decision_rows, CallsiteReadinessDecisionRow),
        "summary_csv": write_csv(repo / SUMMARY_CSV, [bundle.summary], CallsiteReadinessSummary),
        "handoff_csv": write_csv(repo / HANDOFF_CSV, [bundle.summary], CallsiteReadinessSummary),
    }
    md = repo / MD_OUTPUT
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text(render_markdown(bundle), encoding="utf-8")
    written["md"] = md
    story = repo / STORY
    story.parent.mkdir(parents=True, exist_ok=True)
    story.write_text(render_story(bundle), encoding="utf-8")
    written["story"] = story
    assert_metadata_only(list(written.values()))
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()
    bundle = build_door_save_runtime_helper_callsite_readiness_gate(repo)
    written = write_all_artifacts(bundle, repo)
    for label, path in written.items():
        print(f"{label}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
