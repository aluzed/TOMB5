#!/usr/bin/env python3
"""Generate RE-061 module-game proof-first audit artifacts.

The audit consumes existing metadata-only priority and domain handoff CSVs. It
publishes a safe module-level shortlist and proof blockers only: no raw Ghidra
addresses, opcodes, machine words, branch/call targets, payload coordinates, or
copied binary dump records.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


PRIORITY_CSV = "docs/reverse/generated/function-priority.csv"
RE044_CSV = "docs/reverse/generated/re044-domain-reprioritization.csv"
RE060_CSV = "docs/reverse/generated/re053-re060-collision-chain.csv"
AUDIT_CSV = "docs/reverse/generated/re061-module-game-proof-first-audit.csv"
CLUSTER_CSV = "docs/reverse/generated/re061-module-game-clusters.csv"
PLAN_CSV = "docs/reverse/generated/re061-module-game-ticket-plan.csv"
MD_OUTPUT = "docs/reverse/functions/re061-module-game-proof-first-audit.md"
STORY_OUTPUT = "docs/stories/RE-061-module-game-proof-first-audit.md"

CLOSED_CHAIN_FUNCTIONS = {"RestoreLevelData", "SaveLevelData"}
CLOSED_CHAIN_FILES = {"GAME/SAVEGAME.C"}
C_KEYWORD_ARTIFACTS = {"if", "for", "while", "switch", "else", "do"}

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
class ModuleGameCandidate:
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
class ModuleGameCluster:
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
class ModuleGameAudit:
    story_id: str
    domain_id: str
    pivot_function: str
    status: str
    depends_on: tuple[str, ...]
    decision: str
    code_change_readiness: str
    next_ticket: str
    source_priority_csv: str
    upstream_handoff_csv: str
    upstream_reprioritization_csv: str
    progress: tuple[str, ...]
    summary: AuditSummary
    candidates: tuple[ModuleGameCandidate, ...]
    clusters: tuple[ModuleGameCluster, ...]
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


def is_closed_chain(row: dict[str, str]) -> bool:
    return row.get("repo_function", "") in CLOSED_CHAIN_FUNCTIONS or row.get("file", "") in CLOSED_CHAIN_FILES


def candidate_cluster(function: str, file: str) -> str:
    haystack = f"{file} {function}".upper()
    if "DEBRIS" in haystack or "SHATTER" in haystack or "EXPLOD" in haystack:
        return "debris-object-breakage"
    if "GAMEFLOW" in haystack or "TITLE" in haystack or "CONTROL" in haystack:
        return "gameflow-runtime-control"
    if "LARA" in haystack or "SWIM" in haystack or "CLIMB" in haystack or "VAULT" in haystack:
        return "lara-movement-support"
    if "FLARE" in haystack or "FLMTORCH" in haystack or "LIGHT" in haystack:
        return "item-lighting-interaction"
    if "PICKUP" in haystack or "OBJECT" in haystack:
        return "object-interaction"
    if "TEXT" in haystack or "FONT" in haystack:
        return "ui-text-support"
    return "gameplay-mixed"


def candidate_role(row: dict[str, str], cluster: str) -> str:
    function = row.get("repo_function", "")
    if function == "ShatterObject":
        return "pivot"
    if row.get("nd") == "yes":
        return "nd-marker-audit-target"
    if cluster == "debris-object-breakage":
        return "domain-entry-or-support"
    if row.get("runtime_focus") == "yes":
        return "runtime-context"
    return "supporting-candidate"


def readiness_for(row: dict[str, str], cluster: str, role: str) -> tuple[str, str, str]:
    if role == "pivot":
        return (
            "proof-first-audit-needed",
            "symbolic top candidate from RE-044, but source/binary equivalence and side effects are not proven",
            "RE-062 debris/object-breakage caller and side-effect map",
        )
    if role == "nd-marker-audit-target":
        return (
            "nd-marker-proof-needed",
            "ND marker needs behavior proof before removal or marker upgrade",
            "ND marker audit after the initial module-game cluster map",
        )
    if cluster == "debris-object-breakage":
        return (
            "cluster-support-proof-needed",
            "cluster support row still lacks non-raw equivalence proof",
            "include in RE-062 cluster call/data map",
        )
    return (
        "backlog-candidate-proof-needed",
        "module-game row is useful backlog context but not the first proof cluster",
        "defer until debris/object-breakage proof gate closes",
    )


def build_candidates(priority_rows: list[dict[str, str]]) -> list[ModuleGameCandidate]:
    candidates: list[ModuleGameCandidate] = []
    for row in priority_rows:
        function = row.get("repo_function", "")
        if function in C_KEYWORD_ARTIFACTS or is_closed_chain(row) or classify_domain(row) != "module-game":
            continue
        cluster = candidate_cluster(function, row.get("file", ""))
        role = candidate_role(row, cluster)
        readiness, blocker, next_probe = readiness_for(row, cluster, role)
        candidates.append(
            ModuleGameCandidate(
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
    candidates.sort(key=lambda item: (-item.score, item.file, item.line, item.function))
    return candidates


def build_clusters(candidates: list[ModuleGameCandidate]) -> list[ModuleGameCluster]:
    grouped: dict[str, list[ModuleGameCandidate]] = defaultdict(list)
    for candidate in candidates:
        grouped[candidate.cluster].append(candidate)

    clusters: list[ModuleGameCluster] = []
    for cluster, rows in grouped.items():
        rows.sort(key=lambda item: (-item.score, item.file, item.line, item.function))
        readiness = "proof-needed"
        blocker = "cluster needs source-level contract and non-raw binary equivalence proof"
        next_ticket = "defer"
        if cluster == "debris-object-breakage":
            readiness = "best-initial-proof-cluster"
            blocker = "ShatterObject/TriggerDebris side effects and callers need metadata-only proof before source or marker changes"
            next_ticket = "RE-062"
        elif any(row.nd == "yes" for row in rows):
            readiness = "nd-marker-audit-later"
            blocker = "ND marker rows require dedicated behavior proof after the initial module-game cluster"
            next_ticket = "after-RE-062"
        clusters.append(
            ModuleGameCluster(
                cluster=cluster,
                candidate_count=len(rows),
                mapped_count=sum(1 for row in rows if row.bucket in {"P0", "P1", "P2"}),
                nd_count=sum(1 for row in rows if row.nd == "yes"),
                runtime_count=sum(1 for row in rows if row.runtime_focus == "yes"),
                top_function=rows[0].function,
                representative_functions=tuple(row.function for row in rows[:5]),
                readiness=readiness,
                blocker=blocker,
                recommended_next_ticket=next_ticket,
            )
        )
    clusters.sort(key=lambda item: (0 if item.cluster == "debris-object-breakage" else 1, -item.candidate_count, item.cluster))
    return clusters


def build_ticket_plan() -> tuple[TicketPlanItem, ...]:
    specs = (
        (
            "RE-062",
            "debris-object-breakage-caller-side-effect-map",
            "Map ShatterObject/TriggerDebris callers, callees, globals, and side-effect surfaces as metadata only.",
            "debris-object-breakage initial cluster",
            "blocked-until-proof",
            "caller/side-effect matrix published or terminal proof blocker recorded",
        ),
        (
            "RE-063",
            "debris-object-breakage-argument-data-taxonomy",
            "Classify source-level argument shapes, structure fields, object/item dependencies, and write targets for the selected cluster.",
            "ShatterObject/TriggerDebris source contract",
            "blocked-until-proof",
            "taxonomy distinguishes source-backed fields from candidate-only fields",
        ),
        (
            "RE-064",
            "debris-object-breakage-comparison-gate",
            "Decide whether non-raw binary/source equivalence evidence is sufficient for any source or marker change.",
            "comparison readiness gate",
            "blocked-until-proof",
            "patch-ready rows identified or explicit no-patch blocker published",
        ),
        (
            "RE-065",
            "debris-object-breakage-reconstruction-plan",
            "Convert any ready rows into a minimal reconstruction plan with tests, guards, and rollback boundaries.",
            "only rows admitted by RE-064",
            "blocked-until-proof",
            "source patch plan exists or chain remains documentation-only",
        ),
        (
            "RE-066",
            "debris-object-breakage-source-patch-gate",
            "Apply the smallest safe source/marker patch only if RE-064/RE-065 made rows patch-ready; otherwise publish the denial gate.",
            "conditional source patch gate",
            "blocked-until-proof",
            "patch validated or no-source-change decision recorded",
        ),
        (
            "RE-067",
            "debris-object-breakage-validation-regression",
            "Run build/tests/guards for the selected cluster and record exact validation status.",
            "validation and regression evidence",
            "blocked-until-proof",
            "validation log published with pass/fail and remaining blockers",
        ),
        (
            "RE-068",
            "module-game-closure-or-next-cluster-handoff",
            "Close the initial module-game cluster or hand off to the next best module-game cluster with a refreshed plan.",
            "closure and reprioritization",
            "blocked-until-proof",
            "domain closure, next-cluster handoff, or terminal blocker recorded",
        ),
    )
    return tuple(TicketPlanItem(*spec) for spec in specs)


def verify_upstream_handoff(repo: Path) -> dict[str, str]:
    re044_rows = read_csv(repo / RE044_CSV)
    module_rows = [row for row in re044_rows if row.get("domain_id") == "module-game"]
    if not module_rows:
        raise ValueError("RE-044 module-game row is missing")
    module_row = module_rows[0]
    if module_row.get("top_function") != "ShatterObject":
        raise ValueError("RE-044 module-game top function changed; refresh RE-061 expectations")

    re060_rows = read_csv(repo / RE060_CSV)
    handoff_rows = [row for row in re060_rows if row.get("story_id") == "RE-060"]
    if not handoff_rows or handoff_rows[0].get("next_ticket") != "RE-061":
        raise ValueError("RE-060 handoff to RE-061 is missing")
    return module_row


def build_module_game_audit(repo: Path) -> ModuleGameAudit:
    repo = Path(repo)
    module_row = verify_upstream_handoff(repo)
    priority_rows = read_csv(repo / PRIORITY_CSV)
    candidates = tuple(build_candidates(priority_rows))
    clusters = tuple(build_clusters(list(candidates)))
    selected_cluster = clusters[0].cluster if clusters else "debris-object-breakage"
    pivot = module_row.get("top_function", "") or (candidates[0].function if candidates else "ShatterObject")
    summary = AuditSummary(
        candidate_count=len(candidates),
        mapped_count=sum(1 for row in candidates if row.bucket in {"P0", "P1", "P2"}),
        nd_count=sum(1 for row in candidates if row.nd == "yes"),
        runtime_count=sum(1 for row in candidates if row.runtime_focus == "yes"),
        cluster_count=len(clusters),
        selected_cluster=selected_cluster,
        patch_ready_count=0,
        marker_ready_count=0,
    )
    return ModuleGameAudit(
        story_id="RE-061",
        domain_id="module-game",
        pivot_function=pivot,
        status="module-game-proof-first-audit-published",
        depends_on=("RE-060", "RE-044"),
        decision="module-game-domain-scoped-for-proof-chain",
        code_change_readiness="blocked",
        next_ticket="RE-062",
        source_priority_csv=PRIORITY_CSV,
        upstream_handoff_csv=RE060_CSV,
        upstream_reprioritization_csv=RE044_CSV,
        progress=(
            "re060-handoff-loaded",
            "re044-module-game-row-consumed",
            "module-game-candidates-classified",
            "proof-first-blockers-recorded",
            "forbidden-raw-evidence-excluded",
        ),
        summary=summary,
        candidates=candidates,
        clusters=clusters,
        ticket_plan=build_ticket_plan(),
    )


def write_dict_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_audit_csv(path: Path, audit: ModuleGameAudit) -> None:
    fields = [
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
    ]
    write_dict_csv(path, fields, [candidate.__dict__ for candidate in audit.candidates])


def write_cluster_csv(path: Path, audit: ModuleGameAudit) -> None:
    fields = [
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
    ]
    rows = []
    for cluster in audit.clusters:
        rows.append({**cluster.__dict__, "representative_functions": ";".join(cluster.representative_functions)})
    write_dict_csv(path, fields, rows)


def write_plan_csv(path: Path, audit: ModuleGameAudit) -> None:
    fields = ["story_id", "topic", "goal", "scope", "code_change_readiness", "exit_condition"]
    write_dict_csv(path, fields, [ticket.__dict__ for ticket in audit.ticket_plan])


def write_markdown(path: Path, audit: ModuleGameAudit) -> None:
    lines = [
        "# RE-061 — Module-game proof-first audit",
        "",
        f"Domain: `{audit.domain_id}`",
        f"Pivot: `{audit.pivot_function}`",
        f"Status: `{audit.status}`",
        f"Decision: `{audit.decision}`",
        f"Code-change readiness: `{audit.code_change_readiness}`",
        f"Recommended next ticket: `{audit.next_ticket}`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-060 handoff loaded.",
        "- [x] RE-044 module-game row consumed.",
        "- [x] Module-game candidates classified.",
        "- [x] Proof-first blockers recorded.",
        "- [x] Forbidden raw evidence excluded.",
        "",
        "## Summary",
        "",
        f"- candidates: `{audit.summary.candidate_count}`",
        f"- mapped candidates: `{audit.summary.mapped_count}`",
        f"- ND candidates: `{audit.summary.nd_count}`",
        f"- runtime-focus candidates: `{audit.summary.runtime_count}`",
        f"- clusters: `{audit.summary.cluster_count}`",
        f"- Selected initial cluster: `{audit.summary.selected_cluster}`",
        f"- code-change-ready candidates: `{audit.summary.patch_ready_count}`",
        f"- marker-ready candidates: `{audit.summary.marker_ready_count}`",
        "",
        "## Cluster shortlist",
        "",
    ]
    for cluster in audit.clusters:
        lines.extend(
            [
                f"- `{cluster.cluster}`",
                f"  - candidates: `{cluster.candidate_count}`; mapped: `{cluster.mapped_count}`; ND: `{cluster.nd_count}`; runtime: `{cluster.runtime_count}`",
                f"  - top: `{cluster.top_function}`",
                f"  - representative functions: `{'; '.join(cluster.representative_functions)}`",
                f"  - readiness: `{cluster.readiness}`",
                f"  - blocker: {cluster.blocker}",
                f"  - recommended next ticket: `{cluster.recommended_next_ticket}`",
            ]
        )
    lines.extend(["", "## Multi-ticket plan", ""])
    for ticket in audit.ticket_plan:
        lines.extend(
            [
                f"- `{ticket.story_id}` `{ticket.topic}`",
                f"  - goal: {ticket.goal}",
                f"  - scope: `{ticket.scope}`",
                f"  - readiness: `{ticket.code_change_readiness}`",
                f"  - exit: {ticket.exit_condition}",
            ]
        )
    lines.extend(
        [
            "",
            "## Readiness decision",
            "",
            "RE-061 is a proof-first audit gate. It selects `debris-object-breakage` as the first module-game cluster because `ShatterObject` is the RE-044 top module-game candidate and `TriggerDebris` gives a compact adjacent support row. No source patch or completion-marker change is safe until a caller/side-effect map and non-raw equivalence proof exist.",
            "",
            "## Generated artifacts",
            "",
            f"- `{AUDIT_CSV}`",
            f"- `{CLUSTER_CSV}`",
            f"- `{PLAN_CSV}`",
            f"- `{MD_OUTPUT}`",
            "",
            "## Next step",
            "",
            "RE-062: build the debris/object-breakage caller and side-effect map for `ShatterObject`/`TriggerDebris` before any source reconstruction or marker update.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_story(path: Path, audit: ModuleGameAudit) -> None:
    lines = [
        "# RE-061 — Module-game proof-first audit",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Open the module-game reconstruction chain after the collision handoff by scoping a metadata-only proof-first audit.",
        "",
        "## Scope",
        "",
        "- depends on: " + ", ".join(f"`{dep}`" for dep in audit.depends_on),
        f"- source priority input: `{audit.source_priority_csv}`",
        f"- upstream handoff input: `{audit.upstream_handoff_csv}`",
        f"- upstream domain gate: `{audit.upstream_reprioritization_csv}`",
        "- safety contract: `metadata-only; no opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records; no raw addresses in generated outputs`",
        "",
        "## Progress",
        "",
    ]
    labels = {
        "re060-handoff-loaded": "RE-060 handoff loaded",
        "re044-module-game-row-consumed": "RE-044 module-game row consumed",
        "module-game-candidates-classified": "Module-game candidates classified",
        "proof-first-blockers-recorded": "Proof-first blockers recorded",
        "forbidden-raw-evidence-excluded": "Forbidden raw evidence excluded",
    }
    for item in audit.progress:
        lines.append(f"- [x] {labels[item]}.")
    lines.extend(
        [
            "",
            "## Generated artifacts",
            "",
            f"- `{AUDIT_CSV}`",
            f"- `{CLUSTER_CSV}`",
            f"- `{PLAN_CSV}`",
            f"- `{MD_OUTPUT}`",
            "",
            "## Findings",
            "",
            f"- module-game candidates: `{audit.summary.candidate_count}`",
            f"- selected initial cluster: `{audit.summary.selected_cluster}`",
            f"- pivot function: `{audit.pivot_function}`",
            f"- code-change-ready candidates: `{audit.summary.patch_ready_count}`",
            f"- marker-ready candidates: `{audit.summary.marker_ready_count}`",
            "",
            "## Multi-ticket plan",
            "",
        ]
    )
    for ticket in audit.ticket_plan:
        lines.extend(
            [
                f"- `{ticket.story_id}` `{ticket.topic}`",
                f"  - goal: {ticket.goal}",
                f"  - scope: `{ticket.scope}`",
                f"  - readiness: `{ticket.code_change_readiness}`",
                f"  - exit: {ticket.exit_condition}",
            ]
        )
    lines.extend(
        [
            "",
            "## Readiness decision",
            "",
            f"- decision: `{audit.decision}`",
            "- safe next action: `open RE-062 debris/object-breakage caller and side-effect map`",
            f"- code change readiness: `{audit.code_change_readiness}`",
            f"- next ticket: `{audit.next_ticket}`",
            "",
            "Do not patch production source or add `(F)`, `(D)`, or `(**)` markers from this story alone.",
            "",
            "## Validation",
            "",
            "- `python3 -m pytest tests/reverse/test_re061_module_game_audit.py -q`",
            "- metadata-only guard over RE-061 outputs",
            "",
            "## Next step",
            "",
            "RE-062: build a metadata-only caller/side-effect map for `ShatterObject` and `TriggerDebris` before any source reconstruction or marker update.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_all_artifacts(audit: ModuleGameAudit, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    audit_csv = repo / AUDIT_CSV
    cluster_csv = repo / CLUSTER_CSV
    plan_csv = repo / PLAN_CSV
    md = repo / MD_OUTPUT
    story = repo / STORY_OUTPUT
    write_audit_csv(audit_csv, audit)
    write_cluster_csv(cluster_csv, audit)
    write_plan_csv(plan_csv, audit)
    write_markdown(md, audit)
    write_story(story, audit)
    return {"audit_csv": audit_csv, "cluster_csv": cluster_csv, "plan_csv": plan_csv, "md": md, "story": story}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="TOMB5 repo root; default: current directory")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    audit = build_module_game_audit(repo)
    written = write_all_artifacts(audit, repo)
    print(f"wrote RE-061 audit to {written['audit_csv']}")
    print(f"wrote RE-061 clusters to {written['cluster_csv']}")
    print(f"wrote RE-061 ticket plan to {written['plan_csv']}")
    print(f"wrote RE-061 markdown to {written['md']}")
    print(f"wrote RE-061 story to {written['story']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
