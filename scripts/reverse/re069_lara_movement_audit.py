#!/usr/bin/env python3
"""Generate RE-069 lara-movement proof-first audit artifacts.

Consumes the RE-068 handoff and the RE-061 module-game candidate audit. Outputs
metadata-only scope, subcluster, and follow-up ticket plan for the next bounded
module-game proof chain.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


RE068_HANDOFF_CSV = "docs/reverse/generated/re068-module-game-handoff.csv"
RE061_AUDIT_CSV = "docs/reverse/generated/re061-module-game-proof-first-audit.csv"
AUDIT_CSV = "docs/reverse/generated/re069-lara-movement-proof-first-audit.csv"
SUBCLUSTER_CSV = "docs/reverse/generated/re069-lara-movement-subclusters.csv"
PLAN_CSV = "docs/reverse/generated/re069-lara-movement-ticket-plan.csv"
MD_OUTPUT = "docs/reverse/functions/re069-lara-movement-proof-first-audit.md"
STORY_OUTPUT = "docs/stories/RE-069-lara-movement-proof-first-audit.md"
C_KEYWORD_ARTIFACTS = {"if", "for", "while", "switch", "else", "do"}
FORBIDDEN_FRAGMENTS = ("0x", "payload", "opcode", "machine word", "raw call target")


@dataclass(frozen=True)
class AuditSummary:
    candidate_count: int
    source_backed_count: int
    runtime_count: int
    subcluster_count: int
    selected_subcluster: str
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
    subcluster: str
    role: str
    readiness: str
    code_change_ready: str
    marker_ready: str
    blocker: str
    next_probe: str


@dataclass(frozen=True)
class Subcluster:
    subcluster: str
    candidate_count: int
    source_backed_count: int
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
class LaraMovementAudit:
    story_id: str
    domain_id: str
    cluster: str
    pivot_function: str
    status: str
    depends_on: tuple[str, ...]
    decision: str
    code_change_readiness: str
    next_ticket: str
    progress: tuple[str, ...]
    summary: AuditSummary
    candidates: tuple[Candidate, ...]
    subclusters: tuple[Subcluster, ...]
    ticket_plan: tuple[TicketPlanItem, ...]


def parse_int(text: str | None) -> int:
    try:
        return int(text or "0")
    except ValueError:
        return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def subcluster_for(function: str, file: str) -> str:
    haystack = f"{file} {function}".upper()
    if "SLIDE" in haystack or "VAULT" in haystack or "HANG" in haystack or "CLIMB" in haystack or "CORNER" in haystack:
        return "ledge-and-vault-tests"
    if "FLARE" in haystack:
        return "flare-movement-support"
    if "SWIM" in haystack or "WATER" in haystack or "SURF" in haystack:
        return "water-movement-support"
    if "LARA" in haystack:
        return "lara-control-context"
    return "movement-mixed-support"


def role_for(function: str, subcluster: str) -> str:
    if function == "TestLaraSlide":
        return "pivot"
    if subcluster == "ledge-and-vault-tests":
        return "ledge-vault-support"
    if subcluster == "flare-movement-support":
        return "flare-support"
    if subcluster == "water-movement-support":
        return "water-movement-support"
    return "supporting-candidate"


def readiness_for(role: str, subcluster: str) -> tuple[str, str, str]:
    if role == "pivot":
        return (
            "proof-first-audit-needed",
            "top handoff candidate, but caller intent, state writes, and binary equivalence are not proven",
            "RE-070 lara movement caller and side-effect map",
        )
    if subcluster == "ledge-and-vault-tests":
        return (
            "cluster-support-proof-needed",
            "ledge/vault/hang predicates need grouped source contract and equivalence proof",
            "include in RE-070 caller/side-effect map",
        )
    return (
        "backlog-candidate-proof-needed",
        "useful movement support row but not selected as first subcluster proof target",
        "defer until ledge/vault proof gate closes",
    )


def build_candidates(audit_rows: list[dict[str, str]]) -> list[Candidate]:
    rows: list[Candidate] = []
    for row in audit_rows:
        if row.get("cluster") != "lara-movement-support":
            continue
        function = row.get("function", "")
        if function in C_KEYWORD_ARTIFACTS:
            continue
        subcluster = subcluster_for(function, row.get("file", ""))
        role = role_for(function, subcluster)
        readiness, blocker, next_probe = readiness_for(role, subcluster)
        rows.append(
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
                subcluster=subcluster,
                role=role,
                readiness=readiness,
                code_change_ready="no",
                marker_ready="no",
                blocker=blocker,
                next_probe=next_probe,
            )
        )
    rows.sort(key=lambda item: (0 if item.function == "TestLaraSlide" else 1, -item.score, item.file, item.line, item.function))
    return rows


def build_subclusters(candidates: list[Candidate]) -> list[Subcluster]:
    grouped: dict[str, list[Candidate]] = defaultdict(list)
    for row in candidates:
        grouped[row.subcluster].append(row)
    output: list[Subcluster] = []
    for subcluster, rows in grouped.items():
        rows.sort(key=lambda item: (-item.score, item.file, item.line, item.function))
        readiness = "proof-needed"
        blocker = "subcluster needs source-level contract and non-raw binary equivalence proof"
        next_ticket = "defer"
        if subcluster == "ledge-and-vault-tests":
            readiness = "best-initial-proof-subcluster"
            blocker = "TestLaraSlide/TestLaraVault/ledge predicates need caller/state/equivalence map before source or marker changes"
            next_ticket = "RE-070"
        output.append(
            Subcluster(
                subcluster=subcluster,
                candidate_count=len(rows),
                source_backed_count=sum(1 for row in rows if row.status in {"decompiled", "debugged", "final", "binary_matched"}),
                runtime_count=sum(1 for row in rows if row.runtime_focus == "yes"),
                top_function=rows[0].function,
                representative_functions=tuple(row.function for row in rows[:5]),
                readiness=readiness,
                blocker=blocker,
                recommended_next_ticket=next_ticket,
            )
        )
    output.sort(key=lambda item: (0 if item.subcluster == "ledge-and-vault-tests" else 1, -item.candidate_count, item.subcluster))
    return output


def build_ticket_plan() -> tuple[TicketPlanItem, ...]:
    specs = (
        ("RE-070", "lara-movement-caller-side-effect-map", "Map TestLaraSlide/TestLaraVault/ledge-hang callers, callees, state writes, and predicate surfaces.", "ledge-and-vault-tests initial subcluster", "blocked-until-proof", "caller/side-effect matrix published or terminal proof blocker recorded"),
        ("RE-071", "lara-movement-argument-state-taxonomy", "Classify movement predicate arguments, Lara state fields, item/collision dependencies, and write targets.", "selected lara movement source contract", "blocked-until-proof", "taxonomy separates source-backed fields from candidate-only fields"),
        ("RE-072", "lara-movement-comparison-gate", "Decide whether non-raw binary/source equivalence evidence is sufficient for any source or marker change.", "comparison readiness gate", "blocked-until-proof", "patch-ready rows identified or explicit no-patch blocker published"),
        ("RE-073", "lara-movement-reconstruction-plan", "Convert ready rows into a minimal reconstruction plan with tests, guards, and rollback boundaries.", "only rows admitted by RE-072", "blocked-until-proof", "source patch plan exists or chain remains documentation-only"),
        ("RE-074", "lara-movement-source-patch-gate", "Apply the smallest safe source/marker patch only if RE-072/RE-073 made rows patch-ready; otherwise publish denial gate.", "conditional source patch gate", "blocked-until-proof", "patch validated or no-source-change decision recorded"),
        ("RE-075", "lara-movement-validation-regression", "Run build/tests/guards for the selected movement subcluster and record validation status.", "validation and regression evidence", "blocked-until-proof", "validation log published with pass/fail and remaining blockers"),
        ("RE-076", "lara-movement-closure-or-handoff", "Close the lara movement subcluster or hand off to the next module-game cluster with a refreshed plan.", "closure and reprioritization", "blocked-until-proof", "domain closure, next-subcluster handoff, or terminal blocker recorded"),
    )
    return tuple(TicketPlanItem(*spec) for spec in specs)


def verify_handoff(repo: Path) -> None:
    rows = read_csv(repo / RE068_HANDOFF_CSV)
    if not rows or rows[0].get("next_ticket") != "RE-069":
        raise ValueError("RE-068 handoff to RE-069 is missing")
    if rows[0].get("next_cluster") != "lara-movement-support":
        raise ValueError("RE-068 handoff is no longer lara-movement-support")


def build_lara_movement_audit(repo: Path) -> LaraMovementAudit:
    repo = Path(repo)
    verify_handoff(repo)
    candidates = tuple(build_candidates(read_csv(repo / RE061_AUDIT_CSV)))
    subclusters = tuple(build_subclusters(list(candidates)))
    summary = AuditSummary(
        candidate_count=len(candidates),
        source_backed_count=sum(1 for row in candidates if row.status in {"decompiled", "debugged", "final", "binary_matched"}),
        runtime_count=sum(1 for row in candidates if row.runtime_focus == "yes"),
        subcluster_count=len(subclusters),
        selected_subcluster=subclusters[0].subcluster if subclusters else "ledge-and-vault-tests",
        patch_ready_count=0,
        marker_ready_count=0,
    )
    return LaraMovementAudit(
        story_id="RE-069",
        domain_id="module-game",
        cluster="lara-movement-support",
        pivot_function="TestLaraSlide",
        status="lara-movement-proof-first-audit-published",
        depends_on=("RE-068", "RE-061"),
        decision="lara-movement-cluster-scoped-for-proof-chain",
        code_change_readiness="blocked",
        next_ticket="RE-070",
        progress=(
            "re068-handoff-consumed",
            "re061-lara-movement-candidates-loaded",
            "lara-movement-subclusters-classified",
            "proof-first-blockers-recorded",
            "follow-up-ticket-plan-published",
            "forbidden-raw-evidence-excluded",
        ),
        summary=summary,
        candidates=candidates,
        subclusters=subclusters,
        ticket_plan=build_ticket_plan(),
    )


def write_dict_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_audit_csv(path: Path, audit: LaraMovementAudit) -> None:
    fields = ["function", "file", "line", "status", "markers", "bucket", "score", "caller_count", "callee_count", "runtime_focus", "nd", "subcluster", "role", "readiness", "code_change_ready", "marker_ready", "blocker", "next_probe"]
    write_dict_csv(path, fields, [row.__dict__ for row in audit.candidates])


def write_subcluster_csv(path: Path, audit: LaraMovementAudit) -> None:
    fields = ["subcluster", "candidate_count", "source_backed_count", "runtime_count", "top_function", "representative_functions", "readiness", "blocker", "recommended_next_ticket"]
    rows = [{**row.__dict__, "representative_functions": ";".join(row.representative_functions)} for row in audit.subclusters]
    write_dict_csv(path, fields, rows)


def write_plan_csv(path: Path, audit: LaraMovementAudit) -> None:
    fields = ["story_id", "topic", "goal", "scope", "code_change_readiness", "exit_condition"]
    write_dict_csv(path, fields, [row.__dict__ for row in audit.ticket_plan])


def write_markdown(path: Path, audit: LaraMovementAudit) -> None:
    lines = [
        "# RE-069 — Lara movement proof-first audit",
        "",
        f"Domain: `{audit.domain_id}`",
        f"Cluster: `{audit.cluster}`",
        f"Pivot: `{audit.pivot_function}`",
        f"Status: `{audit.status}`",
        f"Decision: `{audit.decision}`",
        f"Code-change readiness: `{audit.code_change_readiness}`",
        f"Recommended next ticket: `{audit.next_ticket}`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-068 handoff consumed.",
        "- [x] RE-061 lara movement candidates loaded.",
        "- [x] Lara movement subclusters classified.",
        "- [x] Proof-first blockers recorded.",
        "- [x] Follow-up ticket plan published.",
        "- [x] Forbidden raw evidence excluded.",
        "",
        "## Summary",
        "",
        f"- candidates: `{audit.summary.candidate_count}`",
        f"- source-backed candidates: `{audit.summary.source_backed_count}`",
        f"- runtime-focus candidates: `{audit.summary.runtime_count}`",
        f"- subclusters: `{audit.summary.subcluster_count}`",
        f"- selected subcluster: `{audit.summary.selected_subcluster}`",
        f"- code-change-ready rows: `{audit.summary.patch_ready_count}`",
        f"- marker-ready rows: `{audit.summary.marker_ready_count}`",
        "",
        "## Subclusters",
        "",
    ]
    for row in audit.subclusters:
        lines.append(f"- `{row.subcluster}` — candidates `{row.candidate_count}`, top `{row.top_function}`, readiness `{row.readiness}`")
    lines.extend(["", "## Ticket plan", ""])
    for ticket in audit.ticket_plan:
        lines.append(f"- `{ticket.story_id}` `{ticket.topic}` — {ticket.goal}")
    lines.extend([
        "",
        "## Readiness decision",
        "",
        f"- decision: `{audit.decision}`",
        "- source/marker patch: `blocked`",
        "- blocker: `caller intent, Lara state writes, and non-raw equivalence proof are not yet established`",
        "",
        "No production source or proof marker change is made by this audit.",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_story(path: Path, audit: LaraMovementAudit) -> None:
    lines = [
        "# RE-069 — Lara movement proof-first audit",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Open the next module-game proof chain from the RE-068 handoff by scoping the lara movement support cluster.",
        "",
        "## Scope",
        "",
        "- depends on: `RE-068`, `RE-061`",
        "- upstream handoff input: `docs/reverse/generated/re068-module-game-handoff.csv`",
        "- upstream candidate input: `docs/reverse/generated/re061-module-game-proof-first-audit.csv`",
        "- safety contract: `metadata-only symbolic classifications; forbidden raw evidence excluded`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-068 handoff consumed.",
        "- [x] RE-061 lara movement candidates loaded.",
        "- [x] Lara movement subclusters classified.",
        "- [x] Proof-first blockers recorded.",
        "- [x] Follow-up ticket plan published.",
        "- [x] Forbidden raw evidence excluded.",
        "",
        "## Generated artifacts",
        "",
        f"- `{AUDIT_CSV}`",
        f"- `{SUBCLUSTER_CSV}`",
        f"- `{PLAN_CSV}`",
        f"- `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- selected cluster: `{audit.cluster}`",
        f"- selected subcluster: `{audit.summary.selected_subcluster}`",
        f"- pivot function: `{audit.pivot_function}`",
        f"- candidates: `{audit.summary.candidate_count}`",
        f"- code-change-ready candidates: `{audit.summary.patch_ready_count}`",
        f"- marker-ready candidates: `{audit.summary.marker_ready_count}`",
        "",
        "## Multi-ticket plan",
        "",
    ]
    for ticket in audit.ticket_plan:
        lines.extend([
            f"- `{ticket.story_id}` `{ticket.topic}`",
            f"  - goal: {ticket.goal}",
            f"  - scope: `{ticket.scope}`",
            f"  - readiness: `{ticket.code_change_readiness}`",
            f"  - exit: {ticket.exit_condition}",
        ])
    lines.extend([
        "",
        "## Readiness decision",
        "",
        f"- decision: `{audit.decision}`",
        f"- code change readiness: `{audit.code_change_readiness}`",
        f"- next ticket: `{audit.next_ticket}`",
        "",
        "Do not patch production source or add/remove proof markers from this story alone.",
        "",
        "## Validation",
        "",
        "- `python3 -m pytest tests/reverse/test_re069_lara_movement_audit.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over generated RE-069 artifacts",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def assert_metadata_only(path: Path) -> None:
    text = path.read_text(encoding="utf-8").lower()
    hits = [fragment for fragment in FORBIDDEN_FRAGMENTS if fragment in text]
    if hits:
        raise ValueError(f"forbidden raw evidence fragments in {path}: {hits}")


def write_all_artifacts(audit: LaraMovementAudit, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "audit_csv": repo / AUDIT_CSV,
        "subcluster_csv": repo / SUBCLUSTER_CSV,
        "plan_csv": repo / PLAN_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY_OUTPUT,
    }
    write_audit_csv(paths["audit_csv"], audit)
    write_subcluster_csv(paths["subcluster_csv"], audit)
    write_plan_csv(paths["plan_csv"], audit)
    write_markdown(paths["md"], audit)
    write_story(paths["story"], audit)
    for path in paths.values():
        assert_metadata_only(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    audit = build_lara_movement_audit(args.repo)
    written = write_all_artifacts(audit, args.repo)
    for key, path in written.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
