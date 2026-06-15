#!/usr/bin/env python3
"""Generate RE-163 module SPEC_PSXPC_N proof-first audit artifacts.

The audit consumes the RE-162 post-module-game selection gate plus the older
RE-044 domain priority snapshot. It publishes only metadata: symbolic function
names, source paths, counts, clusters, blockers, and follow-up ticket IDs. Raw
binary evidence, instruction words, branch/call targets, payload coordinates,
and copied dump records are intentionally excluded from versioned outputs.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

PRIORITY_CSV = "docs/reverse/generated/function-priority.csv"
RE044_CSV = "docs/reverse/generated/re044-domain-reprioritization.csv"
RE162_CSV = "docs/reverse/generated/re162-post-module-game-domain-reprioritization.csv"
AUDIT_CSV = "docs/reverse/generated/re163-module-spec-psxpc-n-proof-first-audit.csv"
CLUSTER_CSV = "docs/reverse/generated/re163-module-spec-psxpc-n-clusters.csv"
PLAN_CSV = "docs/reverse/generated/re163-module-spec-psxpc-n-ticket-plan.csv"
MD_OUTPUT = "docs/reverse/functions/re163-module-spec-psxpc-n-proof-first-audit.md"
STORY_OUTPUT = "docs/stories/RE-163-module-spec-psxpc-n-proof-first-audit.md"

DOMAIN_ID = "module-spec_psxpc_n"
PIVOT_FUNCTION = "PrintString"
SELECTED_CLUSTER = "ui-text-rendering"
C_KEYWORD_ARTIFACTS = {"if", "for", "while", "switch", "else", "do"}
FORBIDDEN = (
    "word_" + "le_hex",
    "payload_" + "offset",
    "dump" + " row",
    "jal " + "0x",
    "call_" + "address",
    "0x" + "800",
)

DOMAIN_RULES = (
    ("audio-effects", ("EFFECT", "SFX", "SOUND")),
    ("collision", ("COLLIDE", "COLLISION")),
    ("inventory", ("NEWINV", "INVENTORY", "REQUEST")),
    ("camera", ("CAMERA", "SPOTCAM")),
    ("input", ("INPUT", "PSXINPUT")),
    ("lara-combat", ("LARAFIRE", "WEAPON", "MISSILE")),
    ("traps-switches-doors", ("TRAPS", "SWITCH", "DOOR")),
    ("animation-items", ("ANIMITEM", "ANIM")),
    ("maths-render-support", ("MATHS", "DRAW", "GPU")),
)


@dataclass(frozen=True)
class AuditSummary:
    candidate_count: int
    mapped_count: int
    nd_count: int
    runtime_count: int
    cluster_count: int
    selected_cluster: str
    patch_ready_count: int
    marker_ready_count: int


@dataclass(frozen=True)
class Candidate:
    function: str
    file: str
    line: int
    status: str
    markers: str
    bucket: str
    score: int
    caller_count: int
    callee_count: int
    runtime_focus: str
    nd: str
    cluster: str
    role: str
    readiness: str
    code_change_ready: str
    marker_ready: str
    blocker: str
    next_probe: str


@dataclass(frozen=True)
class Cluster:
    cluster: str
    candidate_count: int
    mapped_count: int
    nd_count: int
    runtime_count: int
    top_function: str
    representative_functions: tuple[str, ...]
    readiness: str
    blocker: str
    recommended_next_ticket: str


@dataclass(frozen=True)
class TicketPlanItem:
    story_id: str
    topic: str
    goal: str
    scope: str
    code_change_readiness: str
    exit_condition: str


@dataclass(frozen=True)
class Audit:
    story_id: str
    domain_id: str
    pivot_function: str
    status: str
    depends_on: tuple[str, ...]
    decision: str
    code_change_readiness: str
    next_ticket: str
    source_priority_csv: str
    upstream_reprioritization_csv: str
    upstream_selection_csv: str
    progress: tuple[str, ...]
    summary: AuditSummary
    candidates: tuple[Candidate, ...]
    clusters: tuple[Cluster, ...]
    ticket_plan: tuple[TicketPlanItem, ...]


def parse_int(text: str | None) -> int:
    try:
        return int(text or "0")
    except ValueError:
        return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def classify_domain(row: dict[str, str]) -> str:
    haystack = f"{row.get('file', '')} {row.get('repo_function', '')}".upper()
    for domain_id, terms in DOMAIN_RULES:
        if any(term in haystack for term in terms):
            return domain_id
    module = row.get("file", ".").split("/", 1)[0]
    return f"module-{module.lower()}"


def candidate_cluster(function: str, file: str) -> str:
    haystack = f"{file} {function}".upper()
    if "TEXT" in haystack or function in {"PrintString", "GetStringLength"}:
        return "ui-text-rendering"
    if "PSXMAIN" in haystack or "CD" in haystack or "ROOMLOAD" in haystack:
        return "platform-main-lifecycle"
    if "MALLOC" in haystack:
        return "platform-memory"
    if "MISC" in haystack or "SPECIFIC" in haystack or "SHADOWS" in haystack or "LIGHT" in haystack:
        return "platform-gpu-display"
    if "LOADSAVE" in haystack:
        return "frontend-loadsave"
    if "MOVIE" in haystack or "TITSEQ" in haystack:
        return "frontend-sequence"
    if "CALC" in haystack or "CONTROL" in haystack or "BUBBLES" in haystack or "DELTAPAK" in haystack:
        return "geometry-support"
    return "module-support-mixed"


def candidate_role(row: dict[str, str], cluster: str) -> str:
    function = row.get("repo_function", "")
    if function == PIVOT_FUNCTION:
        return "pivot"
    if row.get("nd") == "yes":
        return "nd-marker-audit-target"
    if cluster == SELECTED_CLUSTER:
        return "cluster-support"
    if row.get("runtime_focus") == "yes":
        return "runtime-context"
    return "supporting-candidate"


def readiness_for(row: dict[str, str], cluster: str, role: str) -> tuple[str, str, str]:
    if role == "pivot":
        return (
            "proof-first-audit-needed",
            "symbolic top candidate from RE-162, but caller side effects and non-raw equivalence proof are not established",
            "RE-164 ui-text-rendering caller and side-effect map",
        )
    if role == "nd-marker-audit-target":
        return (
            "nd-marker-proof-needed",
            "ND marker needs behavior proof before source or marker changes",
            "dedicated ND marker proof after the initial ui text rendering map",
        )
    if cluster == SELECTED_CLUSTER:
        return (
            "cluster-support-proof-needed",
            "ui text support row still lacks callsite/state contract and non-raw equivalence proof",
            "include in RE-164 ui text rendering call/data map",
        )
    return (
        "backlog-candidate-proof-needed",
        "module SPEC_PSXPC_N row is useful context but not the first proof cluster",
        "defer until ui text rendering proof gate closes",
    )


def build_candidates(priority_rows: list[dict[str, str]]) -> list[Candidate]:
    candidates: list[Candidate] = []
    for row in priority_rows:
        function = row.get("repo_function", "")
        if function in C_KEYWORD_ARTIFACTS or classify_domain(row) != DOMAIN_ID:
            continue
        cluster = candidate_cluster(function, row.get("file", ""))
        role = candidate_role(row, cluster)
        readiness, blocker, next_probe = readiness_for(row, cluster, role)
        candidates.append(
            Candidate(
                function=function,
                file=row.get("file", ""),
                line=parse_int(row.get("line")),
                status=row.get("status", ""),
                markers=row.get("markers", "") or "none",
                bucket=row.get("bucket", ""),
                score=parse_int(row.get("score")),
                caller_count=parse_int(row.get("caller_count")),
                callee_count=parse_int(row.get("callee_count")),
                runtime_focus=row.get("runtime_focus", ""),
                nd=row.get("nd", ""),
                cluster=cluster,
                role=role,
                readiness=readiness,
                code_change_ready="no",
                marker_ready="no",
                blocker=blocker,
                next_probe=next_probe,
            )
        )
    candidates.sort(key=lambda item: (item.function != PIVOT_FUNCTION, -item.score, item.file, item.line, item.function))
    return candidates


def build_clusters(candidates: list[Candidate]) -> list[Cluster]:
    grouped: dict[str, list[Candidate]] = defaultdict(list)
    for candidate in candidates:
        grouped[candidate.cluster].append(candidate)

    clusters: list[Cluster] = []
    for cluster, rows in grouped.items():
        rows.sort(key=lambda item: (item.function != PIVOT_FUNCTION, -item.score, item.file, item.line, item.function))
        readiness = "proof-needed"
        blocker = "cluster needs source-level state contract and non-raw binary equivalence proof"
        next_ticket = "defer"
        if cluster == SELECTED_CLUSTER:
            readiness = "best-initial-proof-cluster"
            blocker = "PrintString callers, text buffer state, font flags, and draw side effects need metadata-only proof before source or marker changes"
            next_ticket = "RE-164"
        elif any(row.nd == "yes" for row in rows):
            readiness = "nd-marker-audit-later"
            blocker = "ND marker rows require dedicated behavior proof after the initial ui text rendering cluster"
            next_ticket = "after-RE-164"
        clusters.append(
            Cluster(
                cluster=cluster,
                candidate_count=len(rows),
                mapped_count=sum(1 for row in rows if row.status in {"decompiled", "debugged"}),
                nd_count=sum(1 for row in rows if row.nd == "yes"),
                runtime_count=sum(1 for row in rows if row.runtime_focus == "yes"),
                top_function=rows[0].function,
                representative_functions=tuple(row.function for row in rows[:5]),
                readiness=readiness,
                blocker=blocker,
                recommended_next_ticket=next_ticket,
            )
        )
    clusters.sort(key=lambda item: (item.cluster != SELECTED_CLUSTER, -item.candidate_count, item.cluster))
    return clusters


def ticket_plan() -> tuple[TicketPlanItem, ...]:
    rows = (
        ("RE-164", "ui-text-rendering-caller-side-effect-map", "Map PrintString/GetStringLength callsites, callers, flags, text sources, and visible side-effect categories.", "PrintString plus immediate ui text rendering support rows", "Caller/state map published with source-backed callsite rows only."),
        ("RE-165", "ui-text-rendering-argument-taxonomy", "Classify PrintString coordinate, colour, string source, and flag argument shapes into stable metadata categories.", "PrintString callsite argument families", "Taxonomy distinguishes source-backed shapes from unproven runtime payload assumptions."),
        ("RE-166", "ui-text-rendering-state-contract", "Document text/font/global state dependencies and blockers for safe reconstruction or marker decisions.", "font buffers, string tables, flags, draw queues", "State-contract matrix either unblocks a comparison gate or records exact remaining blockers."),
        ("RE-167", "ui-text-rendering-equivalence-gate", "Compare source-level semantics against non-raw binary metadata without versioning instruction text or addresses.", "PrintString and selected support rows", "Readiness matrix names any code-change-ready or marker-ready rows, otherwise remains blocked."),
        ("RE-168", "ui-text-rendering-source-patch-gate", "Apply a minimal source or marker patch only if RE-167 marks rows ready.", "patch-ready ui text rows only", "Patch/build/tests pass, or a no-patch blocker is published."),
        ("RE-169", "module-spec-psxpc-n-next-cluster-selection", "Select the next SPEC_PSXPC_N cluster after ui text rendering closes or blocks.", "remaining SPEC_PSXPC_N clusters", "Next cluster/handoff artifact names the smallest useful proof gate."),
        ("RE-170", "module-spec-psxpc-n-closure-or-handoff", "Close the module SPEC_PSXPC_N domain when clusters are proved or terminally blocked, then hand off to the next domain.", "module SPEC_PSXPC_N domain", "Closure or exhausted handoff is emitted with next objective."),
    )
    return tuple(
        TicketPlanItem(
            story_id=story_id,
            topic=topic,
            goal=goal,
            scope=scope,
            code_change_readiness="blocked-until-proof",
            exit_condition=exit_condition,
        )
        for story_id, topic, goal, scope, exit_condition in rows
    )


def require_upstream(rows: list[dict[str, str]], source: str) -> dict[str, str]:
    matches = [row for row in rows if row.get("domain_id") == DOMAIN_ID]
    if not matches:
        raise ValueError(f"{source} does not contain {DOMAIN_ID}")
    row = matches[0]
    if row.get("top_function") != PIVOT_FUNCTION:
        raise ValueError(f"{source} drifted: expected pivot {PIVOT_FUNCTION}, got {row.get('top_function')}")
    return row


def build_module_spec_psxpc_n_audit(repo: Path) -> Audit:
    priority_rows = read_csv(repo / PRIORITY_CSV)
    re162_row = require_upstream(read_csv(repo / RE162_CSV), RE162_CSV)
    re044_row = require_upstream(read_csv(repo / RE044_CSV), RE044_CSV)
    if re162_row.get("next_ticket") != "RE-163" or re162_row.get("code_change_readiness") != "blocked":
        raise ValueError("RE-162 selection is not the blocked RE-163 handoff expected by RE-163")

    candidates = build_candidates(priority_rows)
    if not candidates or candidates[0].function != PIVOT_FUNCTION:
        raise ValueError("candidate selection drifted: PrintString is not the selected pivot")
    clusters = build_clusters(candidates)
    summary = AuditSummary(
        candidate_count=parse_int(re044_row.get("candidate_count")),
        mapped_count=parse_int(re044_row.get("mapped_count")),
        nd_count=parse_int(re044_row.get("nd_count")),
        runtime_count=parse_int(re044_row.get("runtime_count")),
        cluster_count=len(clusters),
        selected_cluster=SELECTED_CLUSTER,
        patch_ready_count=0,
        marker_ready_count=0,
    )
    return Audit(
        story_id="RE-163",
        domain_id=DOMAIN_ID,
        pivot_function=PIVOT_FUNCTION,
        status="module-spec-psxpc-n-proof-first-audit-published",
        depends_on=("RE-162", "RE-044"),
        decision="module-spec-psxpc-n-domain-scoped-for-proof-chain",
        code_change_readiness="blocked",
        next_ticket="RE-164",
        source_priority_csv=PRIORITY_CSV,
        upstream_reprioritization_csv=RE044_CSV,
        upstream_selection_csv=RE162_CSV,
        progress=(
            "re162-selection-loaded",
            "re044-module-spec-psxpc-n-row-consumed",
            "module-spec-psxpc-n-candidates-classified",
            "proof-first-blockers-recorded",
            "forbidden-raw-evidence-excluded",
        ),
        summary=summary,
        candidates=tuple(candidates),
        clusters=tuple(clusters),
        ticket_plan=ticket_plan(),
    )


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def render_markdown(audit: Audit) -> str:
    s = audit.summary
    cluster_lines = "\n".join(
        f"- `{cluster.cluster}`: {cluster.candidate_count} candidate(s), readiness `{cluster.readiness}`, next `{cluster.recommended_next_ticket}`."
        for cluster in audit.clusters
    )
    plan_lines = "\n".join(
        f"- `{item.story_id}` `{item.topic}` — {item.goal} Exit: {item.exit_condition}"
        for item in audit.ticket_plan
    )
    return f"""# RE-163 — Module SPEC_PSXPC_N proof-first audit

## Scope

- Domain: `{audit.domain_id}`
- Selected pivot: `{audit.pivot_function}`
- Selected initial cluster: `{s.selected_cluster}`
- Inputs: `{audit.upstream_selection_csv}`, `{audit.upstream_reprioritization_csv}`, `{audit.source_priority_csv}`

## Summary

- candidates from upstream domain row: `{s.candidate_count}`
- mapped candidates from upstream domain row: `{s.mapped_count}`
- ND candidates from upstream domain row: `{s.nd_count}`
- runtime candidates from upstream domain row: `{s.runtime_count}`
- classified non-keyword candidates emitted: `{len(audit.candidates)}`
- clusters: `{s.cluster_count}`
- code-change-ready candidates: `{s.patch_ready_count}`
- marker-ready candidates: `{s.marker_ready_count}`
- Recommended next ticket: `{audit.next_ticket}`

## Cluster classification

{cluster_lines}

## Readiness decision

This is a proof-first audit gate. No production source or marker change is authorized until caller/state contracts and non-raw equivalence evidence are published. Current code change readiness: `{audit.code_change_readiness}`.

## Multi-ticket plan

{plan_lines}

## Safety contract

Generated rows are metadata-only: symbolic function names, source paths, counts, clusters, blockers, and ticket IDs. Raw binary evidence, instruction text, machine words, raw branch/call targets, payload coordinates, and copied dump records are excluded.
"""


def render_story(audit: Audit) -> str:
    plan_lines = "\n".join(
        f"- [ ] `{item.story_id}` `{item.topic}`: {item.goal}"
        for item in audit.ticket_plan
    )
    artifact_lines = "\n".join(
        f"- `{path}`"
        for path in (AUDIT_CSV, CLUSTER_CSV, PLAN_CSV, MD_OUTPUT)
    )
    return f"""# RE-163 — Module SPEC_PSXPC_N proof-first audit

Status: Done

## Goal

Open the `module-spec_psxpc_n` proof chain selected by RE-162 and scope the `PrintString` pivot without changing production source or completion markers.

## Progress

- [x] RE-162 selection loaded.
- [x] RE-044 domain row consumed.
- [x] SPEC_PSXPC_N candidates classified into proof clusters.
- [x] Blockers and follow-up ticket plan recorded.
- [x] Forbidden raw evidence excluded from generated outputs.

## Generated artifacts

{artifact_lines}

## Readiness decision

- code change readiness: `{audit.code_change_readiness}`
- marker readiness: `blocked`
- selected cluster: `{audit.summary.selected_cluster}`
- next ticket: `{audit.next_ticket}`

No production source or marker change is authorized by RE-163. The next step is a metadata-only caller/side-effect map for `PrintString` and related ui text rendering support rows.

## Follow-up ticket plan

{plan_lines}

## Validation

- `python3 -m pytest tests/reverse/test_re163_module_spec_psxpc_n_audit.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over RE-163 generated outputs
"""


def write_all_artifacts(audit: Audit, repo: Path) -> dict[str, Path]:
    audit_path = repo / AUDIT_CSV
    cluster_path = repo / CLUSTER_CSV
    plan_path = repo / PLAN_CSV
    md_path = repo / MD_OUTPUT
    story_path = repo / STORY_OUTPUT

    write_csv(
        audit_path,
        [candidate.__dict__ for candidate in audit.candidates],
        [
            "function",
            "file",
            "line",
            "status",
            "markers",
            "bucket",
            "score",
            "caller_count",
            "callee_count",
            "runtime_focus",
            "nd",
            "cluster",
            "role",
            "readiness",
            "code_change_ready",
            "marker_ready",
            "blocker",
            "next_probe",
        ],
    )
    write_csv(
        cluster_path,
        [
            {
                **cluster.__dict__,
                "representative_functions": ";".join(cluster.representative_functions),
            }
            for cluster in audit.clusters
        ],
        [
            "cluster",
            "candidate_count",
            "mapped_count",
            "nd_count",
            "runtime_count",
            "top_function",
            "representative_functions",
            "readiness",
            "blocker",
            "recommended_next_ticket",
        ],
    )
    write_csv(
        plan_path,
        [item.__dict__ for item in audit.ticket_plan],
        ["story_id", "topic", "goal", "scope", "code_change_readiness", "exit_condition"],
    )
    md_path.parent.mkdir(parents=True, exist_ok=True)
    story_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(render_markdown(audit), encoding="utf-8")
    story_path.write_text(render_story(audit), encoding="utf-8")
    return {
        "audit_csv": audit_path,
        "cluster_csv": cluster_path,
        "plan_csv": plan_path,
        "md": md_path,
        "story": story_path,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    audit = build_module_spec_psxpc_n_audit(args.repo)
    write_all_artifacts(audit, args.repo)
    print(f"selected_domain={audit.domain_id}")
    print(f"selected_pivot={audit.pivot_function}")
    print(f"selected_cluster={audit.summary.selected_cluster}")
    print(f"next_ticket={audit.next_ticket}")


if __name__ == "__main__":
    main()
