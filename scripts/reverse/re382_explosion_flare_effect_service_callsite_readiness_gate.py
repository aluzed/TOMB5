#!/usr/bin/env python3
"""Generate RE-382 callsite readiness gate metadata for explosion/flare service."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE381_HANDOFF = "docs/reverse/generated/re381-explosion-flare-effect-service-candidate-callsite-handoff.csv"
RE381_FUNCTIONS = "docs/reverse/generated/re381-explosion-flare-effect-service-candidate-callsite-functions.csv"
RE381_CALLSITES = "docs/reverse/generated/re381-explosion-flare-effect-service-candidate-callsite-map.csv"
RE379_CANDIDATES = "docs/reverse/generated/re379-explosion-flare-effect-service-readiness-gate-candidates.csv"
RE370_SUBCLUSTERS = "docs/reverse/generated/re370-ghidra-effects-lighting-narrow-subclusters.csv"
FAMILIES_CSV = "docs/reverse/generated/re382-explosion-flare-effect-service-callsite-readiness-families.csv"
DECISION_CSV = "docs/reverse/generated/re382-explosion-flare-effect-service-callsite-readiness-decision.csv"
SUMMARY_CSV = "docs/reverse/generated/re382-explosion-flare-effect-service-callsite-readiness-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re382-explosion-flare-effect-service-callsite-readiness-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re382-explosion-flare-effect-service-callsite-readiness-gate.md"
STORY = "docs/stories/RE-382-explosion-flare-effect-service-callsite-readiness-gate.md"

SELECTED_CANDIDATE_ID = "87d9c8a62335"
EXHAUSTED_SUBCLUSTER = "explosion-flare-effect-service"
NEXT_SUBCLUSTER = "spotcam-projectile-effect-service"
FAMILY_ORDER = (
    "control-flow-helper",
    "explosion-flare-effect-helper",
    "joint-position-helper",
    "audio-camera-helper",
    "runtime-effect-support",
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
class CallsiteDecisionRow:
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
    next_deferred_candidate_id: str
    next_subcluster: str
    next_ticket: str
    next_topic: str
    stop_condition: str


@dataclass(frozen=True)
class CallsiteReadinessSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    selected_candidate_id: str
    exhausted_subcluster: str
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
    next_deferred_candidate_id: str
    next_subcluster: str
    next_ticket: str
    next_topic: str
    metadata_work_readiness: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class CallsiteReadinessBundle:
    family_rows: list[CallsiteFamilyGateRow]
    decision_rows: list[CallsiteDecisionRow]
    summary: CallsiteReadinessSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def one_row(repo: Path, rel_path: str) -> dict[str, str]:
    rows = read_csv(repo / rel_path)
    if len(rows) != 1:
        raise ValueError(f"{rel_path} must contain exactly one row")
    return rows[0]


def validate_re381_handoff(repo: Path) -> None:
    row = one_row(repo, RE381_HANDOFF)
    expected = {
        "story_id": "RE-381",
        "next_ticket": "RE-382",
        "next_topic": "explosion-flare-effect-service-callsite-readiness-gate",
        "selected_candidate_id": SELECTED_CANDIDATE_ID,
        "source_context_function_count": "18",
        "source_backed_callsite_count": "121",
        "implemented_context_function_count": "12",
        "stub_context_function_count": "6",
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
            raise ValueError(f"RE-381 handoff drift: {key}={row.get(key)!r}")


def validate_candidate_queue_exhaustion(repo: Path) -> None:
    rows = read_csv(repo / RE379_CANDIDATES)
    candidate_ids = [row.get("candidate_id") for row in rows]
    if candidate_ids != [SELECTED_CANDIDATE_ID]:
        raise ValueError(f"RE-379 candidate order drift: {candidate_ids!r}")
    row = rows[0]
    expected = {
        "selected_narrow_subcluster": EXHAUSTED_SUBCLUSTER,
        "ready_to_reopen_domain": "no",
        "source_patch_authorized": "no",
        "readiness_gate": "blocked-needs-candidate-level-proof",
        "next_probe": "candidate-proof-export",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-379 candidate drift: {key}={row.get(key)!r}")


def validate_parent_subcluster_queue(repo: Path) -> None:
    rows = read_csv(repo / RE370_SUBCLUSTERS)
    names = [row.get("narrow_subcluster") for row in rows]
    expected_names = ["dynamic-lighting-service", EXHAUSTED_SUBCLUSTER, NEXT_SUBCLUSTER]
    if names != expected_names:
        raise ValueError(f"RE-370 subcluster queue drift: {names!r}")
    selected = rows[1]
    next_row = rows[2]
    if selected.get("selection_status") != "deferred-after-selected-subcluster":
        raise ValueError("RE-370 explosion/flare row is not the deferred parent row")
    if next_row.get("selection_status") != "deferred-after-selected-subcluster":
        raise ValueError("RE-370 spotcam/projectile row is not still deferred")
    for row in rows:
        if row.get("ready_to_reopen_domain") != "no" or row.get("source_patch_authorized") != "no":
            raise ValueError(f"RE-370 subcluster readiness drift: {row.get('narrow_subcluster')}")


def build_family_rows(callsite_rows: list[dict[str, str]]) -> list[CallsiteFamilyGateRow]:
    by_family: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in callsite_rows:
        if row.get("candidate_id") != SELECTED_CANDIDATE_ID:
            continue
        by_family[row["callsite_family"]].append(row)
    if set(by_family) != set(FAMILY_ORDER):
        raise ValueError(f"Unexpected RE-382 callsite families: {sorted(by_family)}")

    family_rows: list[CallsiteFamilyGateRow] = []
    for rank, family in enumerate(FAMILY_ORDER, start=1):
        rows = by_family[family]
        statuses = Counter(row["function_status"] for row in rows)
        unexpected_statuses = sorted(set(statuses) - {"source-with-calls", "stub-unimplemented"})
        if unexpected_statuses:
            raise ValueError(f"Unexpected function statuses for {family}: {unexpected_statuses!r}")
        implemented_count = statuses.get("source-with-calls", 0)
        stub_count = statuses.get("stub-unimplemented", 0)
        callers = {row["caller_symbol"] for row in rows}
        implemented_callers = {row["caller_symbol"] for row in rows if row["function_status"] == "source-with-calls"}
        is_stub_only = implemented_count == 0
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
                readiness_gate="blocked-stub-only-family" if is_stub_only else "blocked-no-candidate-level-proof",
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                blocker_class="stub-only-callsite-family" if is_stub_only else "source-callsite-family-lacks-candidate-proof",
                next_probe="close-explosion-flare-subcluster",
            )
        )
    return family_rows


def build_explosion_flare_effect_service_callsite_readiness_gate(repo: Path) -> CallsiteReadinessBundle:
    repo = Path(repo)
    validate_re381_handoff(repo)
    validate_candidate_queue_exhaustion(repo)
    validate_parent_subcluster_queue(repo)
    function_rows = read_csv(repo / RE381_FUNCTIONS)
    callsite_rows = read_csv(repo / RE381_CALLSITES)
    if len(function_rows) != 18:
        raise ValueError(f"Expected 18 RE-381 function rows, got {len(function_rows)}")
    if len(callsite_rows) != 121:
        raise ValueError(f"Expected 121 RE-381 callsite rows, got {len(callsite_rows)}")
    if any(row.get("candidate_id") != SELECTED_CANDIDATE_ID for row in function_rows + callsite_rows):
        raise ValueError("RE-381 candidate set drift")

    family_rows = build_family_rows(callsite_rows)
    implemented_family_count = sum(row.implemented_callsite_count > 0 for row in family_rows)
    stub_only_family_count = sum(row.implemented_callsite_count == 0 for row in family_rows)
    candidate_level_proof_count = sum(row.candidate_level_proof == "yes" for row in family_rows)
    ready_count = sum(row.ready_to_reopen_domain == "yes" for row in family_rows)
    source_patch_count = sum(row.source_patch_authorized == "yes" for row in family_rows)

    decision_rows = [
        CallsiteDecisionRow(
            rank=1,
            candidate_id=SELECTED_CANDIDATE_ID,
            callsite_family_count=len(family_rows),
            implemented_callsite_family_count=implemented_family_count,
            candidate_level_proof_count=candidate_level_proof_count,
            readiness_gate="blocked-no-callsite-family-proves-candidate",
            decision="deny-domain-reopen-and-close-subcluster",
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            selected_domain="none",
            selected_pivot="none",
            next_deferred_candidate_id="none",
            next_subcluster=NEXT_SUBCLUSTER,
            next_ticket="RE-383",
            next_topic="effects-lighting-cluster-post-explosion-flare-next-subcluster-selection",
            stop_condition="the only explosion/flare service candidate lacks candidate-level proof; close this subcluster and select the next deferred parent subcluster",
        )
    ]
    summary = CallsiteReadinessSummary(
        story_id="RE-382",
        topic="explosion-flare-effect-service-callsite-readiness-gate",
        upstream_handoff="RE-381",
        selected_candidate_id=SELECTED_CANDIDATE_ID,
        exhausted_subcluster=EXHAUSTED_SUBCLUSTER,
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
        next_deferred_candidate_id="none",
        next_subcluster=NEXT_SUBCLUSTER,
        next_ticket="RE-383",
        next_topic="effects-lighting-cluster-post-explosion-flare-next-subcluster-selection",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="explosion/flare service candidate queue exhausted; transition to the next deferred effects/lighting subcluster",
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
    return f"""# RE-382 explosion/flare effect service callsite readiness gate

## Summary

Gated `{bundle.summary.callsite_family_count}` source-backed callsite families for explosion/flare candidate `{bundle.summary.selected_candidate_id}`.
No explosion/flare callsite family proves candidate-level behavior, so the proof domain and pivot remain `none`.

## Family gates

{rows}

## Readiness decision

- candidate-level proof rows: `{bundle.summary.candidate_level_proof_count}`
- ready-to-reopen rows: `{bundle.summary.ready_to_reopen_domain_count}`
- source-patch authorized rows: `{bundle.summary.source_patch_authorized_count}`
- next deferred candidate: `{bundle.summary.next_deferred_candidate_id}`
- next subcluster: `{bundle.summary.next_subcluster}`
- next ticket: `{bundle.summary.next_ticket}` / `{bundle.summary.next_topic}`

Code readiness remains `blocked`.
"""


def render_story(bundle: CallsiteReadinessBundle) -> str:
    return f"""# RE-382 explosion/flare effect service callsite readiness gate

## Goal

Gate the RE-381 source-backed callsite map, close the explosion/flare effect service queue if no family proves candidate-level behavior, and hand off to the next deferred parent subcluster.

## Inputs

- Upstream handoff: `{RE381_HANDOFF}`
- Source-backed callsite map: `{RE381_CALLSITES}`
- Source context functions: `{RE381_FUNCTIONS}`
- explosion/flare candidate queue: `{RE379_CANDIDATES}`
- Parent effects/lighting subcluster queue: `{RE370_SUBCLUSTERS}`

## Progress tracker

- [x] RE-381 callsite-map handoff validated.
- [x] RE-379 explosion/flare candidate queue verified exhausted after the selected candidate.
- [x] Parent RE-370 deferred subcluster queue checked.
- [x] Explosion/flare callsite families grouped and readiness-gated.
- [x] Candidate-level proof and source-patch authorization denied for every family.
- [x] Next parent subcluster selection follow-up emitted.

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
- Next deferred candidate: `{bundle.summary.next_deferred_candidate_id}`
- Next deferred subcluster: `{bundle.summary.next_subcluster}`

## Readiness decision

The only explosion/flare candidate's source-backed callsite map still does not prove candidate-level behavior. Domain and pivot remain `none`; code readiness remains `blocked`. The explosion/flare candidate queue is exhausted.

## Follow-up ticket breakdown

- `RE-383` / `effects-lighting-cluster-post-explosion-flare-next-subcluster-selection`: close `explosion-flare-effect-service` and select `spotcam-projectile-effect-service` from the parent RE-370 deferred subcluster queue.
  - Inputs: RE-382 handoff plus RE-370 subcluster queue.
  - Deliverables: metadata-only selected subcluster/candidate rows, summary, and handoff to that subcluster readiness gate.
  - Stop condition: keep source/code readiness blocked until the next selected subcluster has candidate-level proof.

## Validation commands

- `python -m pytest tests/reverse/test_re382_explosion_flare_effect_service_callsite_readiness_gate.py -q`
- `python scripts/reverse/re382_explosion_flare_effect_service_callsite_readiness_gate.py --repo .`
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
    write_csv(paths["decision_csv"], bundle.decision_rows, CallsiteDecisionRow)
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
    bundle = build_explosion_flare_effect_service_callsite_readiness_gate(repo)
    written = write_all_artifacts(bundle, repo)
    for key, path in written.items():
        print(f"{key}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
