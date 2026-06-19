#!/usr/bin/env python3
"""Generate RE-355 callsite-family readiness gate metadata for the frontend display/menu service candidate."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE354_HANDOFF = "docs/reverse/generated/re354-frontend-display-menu-service-candidate-callsite-handoff.csv"
RE354_FUNCTIONS = "docs/reverse/generated/re354-frontend-display-menu-service-candidate-callsite-functions.csv"
RE354_CALLSITES = "docs/reverse/generated/re354-frontend-display-menu-service-candidate-callsite-map.csv"
RE352_CANDIDATES = "docs/reverse/generated/re352-frontend-display-menu-service-readiness-gate-candidates.csv"
FAMILIES_CSV = "docs/reverse/generated/re355-frontend-display-menu-service-callsite-readiness-families.csv"
DECISION_CSV = "docs/reverse/generated/re355-frontend-display-menu-service-callsite-readiness-decision.csv"
SUMMARY_CSV = "docs/reverse/generated/re355-frontend-display-menu-service-callsite-readiness-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re355-frontend-display-menu-service-callsite-readiness-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re355-frontend-display-menu-service-callsite-readiness-gate.md"
STORY = "docs/stories/RE-355-frontend-display-menu-service-callsite-readiness-gate.md"

SELECTED_CANDIDATE_ID = "de919274685f"
NEXT_CANDIDATE_ID = "4c90c6af8f9d"
FAMILY_ORDER = (
    "gpu-display-helper",
    "level-load-service-helper",
    "inventory-menu-helper",
    "audio-sound-helper",
    "platform-lifecycle-helper",
    "text-ui-helper",
    "input-pad-helper",
    "memory-card-helper",
    "diagnostic-helper",
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


def validate_re354_handoff(repo: Path) -> None:
    row = one_row(repo, RE354_HANDOFF)
    expected = {
        "story_id": "RE-354",
        "next_ticket": "RE-355",
        "next_topic": "frontend-display-menu-service-callsite-readiness-gate",
        "selected_candidate_id": SELECTED_CANDIDATE_ID,
        "source_context_function_count": "25",
        "source_backed_callsite_count": "326",
        "implemented_context_function_count": "23",
        "stub_context_function_count": "0",
        "no_callsite_context_function_count": "2",
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
            raise ValueError(f"RE-354 handoff drift: {key}={row.get(key)!r}")


def validate_next_candidate(repo: Path) -> None:
    rows = read_csv(repo / RE352_CANDIDATES)
    candidate_ids = [row.get("candidate_id") for row in rows]
    if candidate_ids != [SELECTED_CANDIDATE_ID, NEXT_CANDIDATE_ID]:
        raise ValueError(f"RE-352 candidate order drift: {candidate_ids!r}")
    selected_row, next_row = rows
    if selected_row.get("next_probe") != "candidate-proof-export":
        raise ValueError("RE-352 selected candidate is not the completed proof-export candidate")
    if next_row.get("next_probe") != "defer-after-re353":
        raise ValueError("RE-352 next candidate is not deferred after the selected candidate")
    for row in rows:
        expected = {
            "selected_narrow_subcluster": "frontend-display-menu-service",
            "ready_to_reopen_domain": "no",
            "source_patch_authorized": "no",
            "readiness_gate": "blocked-needs-candidate-level-proof",
        }
        for key, value in expected.items():
            if row.get(key) != value:
                raise ValueError(f"RE-352 candidate drift: {row.get('candidate_id')} {key}={row.get(key)!r}")


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


def build_frontend_display_menu_service_callsite_readiness_gate(repo: Path) -> CallsiteReadinessBundle:
    repo = Path(repo)
    validate_re354_handoff(repo)
    validate_next_candidate(repo)
    function_rows = read_csv(repo / RE354_FUNCTIONS)
    callsite_rows = read_csv(repo / RE354_CALLSITES)
    if len(function_rows) != 25:
        raise ValueError(f"Expected 25 RE-354 function rows, got {len(function_rows)}")
    if len(callsite_rows) != 326:
        raise ValueError(f"Expected 326 RE-354 callsite rows, got {len(callsite_rows)}")
    if any(row.get("candidate_id") != SELECTED_CANDIDATE_ID for row in function_rows + callsite_rows):
        raise ValueError("RE-354 candidate set drift")

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
            next_ticket="RE-356",
            next_topic="frontend-display-menu-service-next-candidate-proof-export",
            next_candidate_id=NEXT_CANDIDATE_ID,
            stop_condition="source-backed frontend display/menu callsite families do not prove candidate-level behavior",
        )
    ]

    summary = CallsiteReadinessSummary(
        story_id="RE-355",
        topic="frontend-display-menu-service-callsite-readiness-gate",
        upstream_handoff="RE-354",
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
        next_ticket="RE-356",
        next_topic="frontend-display-menu-service-next-candidate-proof-export",
        next_candidate_id=NEXT_CANDIDATE_ID,
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="callsite readiness gate denied the selected candidate; continue with the next deferred frontend display/menu candidate export",
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
    return f"""# RE-355 frontend display/menu service callsite readiness gate

## Summary

Gated `{bundle.summary.callsite_family_count}` source-backed callsite families for candidate `{bundle.summary.selected_candidate_id}`.
No frontend display/menu callsite family proves candidate-level behavior, so the proof domain and pivot remain `none`.

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
    return f"""# RE-355 frontend display/menu service callsite readiness gate

## Goal

Gate the RE-354 source-backed callsite map and decide whether any frontend display/menu callsite family can reopen a proof domain or authorize a source patch.

## Inputs

- Upstream handoff: `{RE354_HANDOFF}`
- Source-backed callsite map: `{RE354_CALLSITES}`
- Source context functions: `{RE354_FUNCTIONS}`
- Deferred candidate order: `{RE352_CANDIDATES}`

## Progress tracker

- [x] RE-354 callsite handoff validated.
- [x] RE-352 deferred candidate order verified fail-closed.
- [x] Callsite families grouped from metadata-only rows.
- [x] Domain/pivot/source-patch readiness denied because candidate-level proof rows remain absent.
- [x] Next deferred frontend display/menu candidate selected.

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

- `RE-356` / `frontend-display-menu-service-next-candidate-proof-export`: reconstruct candidate `{bundle.summary.next_candidate_id}` and export source-symbolic proof context for the deferred frontend display/menu candidate.
  - Inputs: RE-355 decision/handoff plus RE-352 candidate queue.
  - Deliverables: next-candidate context/proof rows and a handoff to either source-backed callsite mapping or queue exhaustion.
  - Stop condition: if the next candidate also lacks candidate-level proof, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re355_frontend_display_menu_service_callsite_readiness_gate.py -q`
- `python scripts/reverse/re355_frontend_display_menu_service_callsite_readiness_gate.py --repo .`
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
    bundle = build_frontend_display_menu_service_callsite_readiness_gate(repo)
    written = write_all_artifacts(bundle, repo)
    for key, path in written.items():
        print(f"{key}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
