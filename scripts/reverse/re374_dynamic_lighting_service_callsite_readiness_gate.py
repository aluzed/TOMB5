#!/usr/bin/env python3
"""Generate RE-374 callsite-family readiness gate metadata for the dynamic-lighting service candidate."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE373_HANDOFF = "docs/reverse/generated/re373-dynamic-lighting-service-candidate-callsite-handoff.csv"
RE373_FUNCTIONS = "docs/reverse/generated/re373-dynamic-lighting-service-candidate-callsite-functions.csv"
RE373_CALLSITES = "docs/reverse/generated/re373-dynamic-lighting-service-candidate-callsite-map.csv"
RE371_CANDIDATES = "docs/reverse/generated/re371-dynamic-lighting-service-readiness-gate-candidates.csv"
FAMILIES_CSV = "docs/reverse/generated/re374-dynamic-lighting-service-callsite-readiness-families.csv"
DECISION_CSV = "docs/reverse/generated/re374-dynamic-lighting-service-callsite-readiness-decision.csv"
SUMMARY_CSV = "docs/reverse/generated/re374-dynamic-lighting-service-callsite-readiness-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re374-dynamic-lighting-service-callsite-readiness-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re374-dynamic-lighting-service-callsite-readiness-gate.md"
STORY = "docs/stories/RE-374-dynamic-lighting-service-callsite-readiness-gate.md"

SELECTED_CANDIDATE_ID = "f5d0099b5511"
NEXT_CANDIDATE_ID = "3a208e2bf745"
FAMILY_ORDER = (
    "control-flow-helper",
    "dynamic-light-trigger",
    "joint-position-helper",
    "effect-state-helper",
    "effects-lighting-trigger",
    "room-floor-helper",
    "stub-marker",
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


def validate_re373_handoff(repo: Path) -> None:
    row = one_row(repo, RE373_HANDOFF)
    expected = {
        "story_id": "RE-373",
        "next_ticket": "RE-374",
        "next_topic": "dynamic-lighting-service-callsite-readiness-gate",
        "selected_candidate_id": SELECTED_CANDIDATE_ID,
        "source_context_function_count": "23",
        "source_backed_callsite_count": "129",
        "implemented_context_function_count": "16",
        "stub_context_function_count": "7",
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
            raise ValueError(f"RE-373 handoff drift: {key}={row.get(key)!r}")


def validate_next_candidate(repo: Path) -> None:
    rows = read_csv(repo / RE371_CANDIDATES)
    candidate_ids = [row.get("candidate_id") for row in rows]
    if candidate_ids != [SELECTED_CANDIDATE_ID, NEXT_CANDIDATE_ID]:
        raise ValueError(f"RE-371 candidate order drift: {candidate_ids!r}")
    selected_row, next_row = rows
    if selected_row.get("next_probe") != "candidate-proof-export":
        raise ValueError("RE-371 selected candidate is not the completed proof-export candidate")
    if next_row.get("next_probe") != "defer-after-re372":
        raise ValueError("RE-371 next candidate is not deferred after the selected candidate")
    for row in rows:
        expected = {
            "selected_narrow_subcluster": "dynamic-lighting-service",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "readiness_gate": "blocked-needs-candidate-level-proof",
        }
        for key, value in expected.items():
            if row.get(key) != value:
                raise ValueError(f"RE-371 candidate drift: {row.get('candidate_id')} {key}={row.get(key)!r}")


def build_family_rows(callsite_rows: list[dict[str, str]]) -> list[CallsiteFamilyGateRow]:
    by_family: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in callsite_rows:
        if row.get("candidate_id") != SELECTED_CANDIDATE_ID:
            continue
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
        is_stub_only = implemented_count == 0
        readiness_gate = "blocked-stub-only-family" if is_stub_only else "blocked-no-candidate-level-proof"
        blocker_class = "stub-only-callsite-family" if is_stub_only else "source-callsite-family-lacks-candidate-proof"
        next_probe = "defer-selected-candidate" if is_stub_only else "needs-non-raw-candidate-equivalence-proof"
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
                next_probe=next_probe,
            )
        )
    return family_rows


def build_dynamic_lighting_service_callsite_readiness_gate(repo: Path) -> CallsiteReadinessBundle:
    repo = Path(repo)
    validate_re373_handoff(repo)
    validate_next_candidate(repo)
    function_rows = read_csv(repo / RE373_FUNCTIONS)
    callsite_rows = read_csv(repo / RE373_CALLSITES)
    if len(function_rows) != 23:
        raise ValueError(f"Expected 23 RE-373 function rows, got {len(function_rows)}")
    if len(callsite_rows) != 129:
        raise ValueError(f"Expected 129 RE-373 callsite rows, got {len(callsite_rows)}")
    if any(row.get("candidate_id") != SELECTED_CANDIDATE_ID for row in function_rows + callsite_rows):
        raise ValueError("RE-373 candidate set drift")

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
            readiness_gate="blocked-no-callsite-family-proves-candidate",
            decision="deny-domain-reopen",
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            selected_domain="none",
            selected_pivot="none",
            next_ticket="RE-375",
            next_topic="dynamic-lighting-service-next-candidate-proof-export",
            next_candidate_id=NEXT_CANDIDATE_ID,
            stop_condition="source-backed dynamic-lighting callsite families do not prove candidate-level behavior",
        )
    ]

    summary = CallsiteReadinessSummary(
        story_id="RE-374",
        topic="dynamic-lighting-service-callsite-readiness-gate",
        upstream_handoff="RE-373",
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
        next_ticket="RE-375",
        next_topic="dynamic-lighting-service-next-candidate-proof-export",
        next_candidate_id=NEXT_CANDIDATE_ID,
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="callsite readiness gate denied the selected candidate; continue with the next deferred dynamic-lighting candidate export",
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
    return f"""# RE-374 dynamic-lighting service callsite readiness gate

## Summary

Gated `{bundle.summary.callsite_family_count}` source-backed callsite families for candidate `{bundle.summary.selected_candidate_id}`.
No dynamic-lighting callsite family proves candidate-level behavior, so the proof domain and pivot remain `none`.

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
    return f"""# RE-374 dynamic-lighting service callsite readiness gate

## Goal

Gate the RE-373 source-backed callsite map and decide whether any dynamic-lighting callsite family can reopen a proof domain or authorize a source patch.

## Inputs

- Upstream handoff: `{RE373_HANDOFF}`
- Source-backed callsite map: `{RE373_CALLSITES}`
- Source context functions: `{RE373_FUNCTIONS}`
- Deferred candidate order: `{RE371_CANDIDATES}`

## Progress tracker

- [x] RE-373 callsite handoff validated.
- [x] RE-371 deferred candidate order verified fail-closed.
- [x] Callsite families grouped from metadata-only rows.
- [x] Domain/pivot/source-patch readiness denied because candidate-level proof rows remain absent.
- [x] Next deferred dynamic-lighting candidate selected.

## Generated artifacts

- `{FAMILIES_CSV}`
- `{DECISION_CSV}`
- `{SUMMARY_CSV}`
- `{HANDOFF_CSV}`
- `{MD_OUTPUT}`

## Findings

- Selected candidate id: `{bundle.summary.selected_candidate_id}`
- Source context functions: `{bundle.summary.source_context_function_count}`
- Source-backed callsite rows: `{bundle.summary.source_backed_callsite_count}`
- Callsite families: `{bundle.summary.callsite_family_count}`
- Implemented callsite families: `{bundle.summary.implemented_callsite_family_count}`
- Stub-only callsite families: `{bundle.summary.stub_only_callsite_family_count}`
- Candidate-level proof rows: `{bundle.summary.candidate_level_proof_count}`
- Ready to reopen domain selection: `{bundle.summary.ready_to_reopen_domain_count}`
- Source patch authorized rows: `{bundle.summary.source_patch_authorized_count}`

## Readiness decision

The callsite families are source-backed and useful prioritization evidence, but they do not prove candidate-level behavior for the unmapped selected candidate. Domain and pivot stay `none`; code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-375` / `dynamic-lighting-service-next-candidate-proof-export`: reconstruct candidate `{bundle.summary.next_candidate_id}` and export source-symbolic proof context for the deferred dynamic-lighting candidate.
  - Inputs: RE-374 decision/handoff plus RE-371 candidate queue.
  - Deliverables: next-candidate context/proof rows and a handoff to either source-backed callsite mapping or queue exhaustion.
  - Stop condition: if the next candidate also lacks candidate-level proof, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re374_dynamic_lighting_service_callsite_readiness_gate.py -q`
- `python scripts/reverse/re374_dynamic_lighting_service_callsite_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
"""


def write_all_artifacts(bundle: CallsiteReadinessBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "families_csv": repo / FAMILIES_CSV,
        "decision_csv": repo / DECISION_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_csv(paths["families_csv"], bundle.family_rows, CallsiteFamilyGateRow)
    write_csv(paths["decision_csv"], bundle.decision_rows, CallsiteReadinessDecisionRow)
    write_csv(paths["summary_csv"], [bundle.summary], CallsiteReadinessSummary)
    write_csv(paths["handoff_csv"], [bundle.summary], CallsiteReadinessSummary)
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text(render_markdown(bundle), encoding="utf-8")
    paths["story"].parent.mkdir(parents=True, exist_ok=True)
    paths["story"].write_text(render_story(bundle), encoding="utf-8")
    assert_metadata_only(list(paths.values()))
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository root")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    bundle = build_dynamic_lighting_service_callsite_readiness_gate(repo)
    written = write_all_artifacts(bundle, repo)
    for key, path in written.items():
        print(f"{key}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
