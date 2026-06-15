#!/usr/bin/env python3
"""Generate RE-044 post-RestoreLevelData domain reprioritization artifacts.

The output intentionally consumes the metadata-only function priority CSV and
publishes domain-level next-work candidates without raw addresses/opcodes or
savegame source-patch claims.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


INPUT_PRIORITY = "docs/reverse/generated/function-priority.csv"
CSV_OUTPUT = "docs/reverse/generated/re044-domain-reprioritization.csv"
MD_OUTPUT = "docs/reverse/functions/re044-post-restoreleveldata-reprioritization.md"
STORY_OUTPUT = "docs/stories/RE-044-post-restoreleveldata-domain-reprioritization.md"

CLOSED_CHAIN_FUNCTIONS = {"RestoreLevelData", "SaveLevelData"}
CLOSED_CHAIN_FILES = {"GAME/SAVEGAME.C"}

DOMAIN_RULES = (
    ("audio-effects", "Audio/effects hubs", ("EFFECT", "SFX", "SOUND")),
    ("collision", "Collision and spatial queries", ("COLLIDE", "COLLISION")),
    ("inventory", "Inventory/frontend item UI", ("NEWINV", "INVENTORY", "REQUEST")),
    ("camera", "Camera and spotcam control", ("CAMERA", "SPOTCAM")),
    ("input", "Runtime input handling", ("INPUT", "PSXINPUT")),
    ("lara-combat", "Lara combat and weapon detection", ("LARAFIRE", "WEAPON", "MISSILE")),
    ("traps-switches-doors", "Traps, switches, and doors", ("TRAPS", "SWITCH", "DOOR")),
    ("animation-items", "Animated item runtime", ("ANIMITEM", "ANIM")),
    ("maths-render-support", "Maths/render support", ("MATHS", "DRAW", "GPU")),
)


@dataclass(frozen=True)
class FunctionCandidate:
    name: str
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
    next_step: str
    address: str = ""


@dataclass(frozen=True)
class DomainCandidate:
    rank: int
    domain_id: str
    label: str
    status: str
    score: int
    candidate_count: int
    mapped_count: int
    nd_count: int
    runtime_count: int
    top_function: str
    top_file: str
    functions: tuple[FunctionCandidate, ...]
    rationale: str
    next_action: str


@dataclass(frozen=True)
class ReprioritizationPlan:
    story_id: str
    status: str
    restoreleveldata_chain_status: str
    code_change_readiness: str
    next_ticket: str
    source_csv: str
    excluded_closed_chain_count: int
    domains: tuple[DomainCandidate, ...]


def parse_int(text: str | None) -> int:
    try:
        return int(text or "0")
    except ValueError:
        return 0


def read_priority_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def is_closed_chain(row: dict[str, str]) -> bool:
    return row.get("repo_function", "") in CLOSED_CHAIN_FUNCTIONS or row.get("file", "") in CLOSED_CHAIN_FILES


def classify_domain(row: dict[str, str]) -> tuple[str, str]:
    haystack = f"{row.get('file', '')} {row.get('repo_function', '')}".upper()
    for domain_id, label, terms in DOMAIN_RULES:
        if any(term in haystack for term in terms):
            return domain_id, label
    module = row.get("file", ".").split("/", 1)[0]
    return f"module-{module.lower()}", f"Module {module} follow-up"


def to_function(row: dict[str, str]) -> FunctionCandidate:
    return FunctionCandidate(
        name=row.get("repo_function", ""),
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
        next_step=row.get("next_step", ""),
        address="",
    )


def domain_rationale(domain: str, functions: list[FunctionCandidate]) -> str:
    top = functions[0]
    if domain == "audio-effects":
        return "high fan-in effects/audio hub; good impact and separated from closed savegame work"
    if domain == "collision":
        return "gameplay collision queries have many callers and clear validation boundaries"
    if domain == "inventory":
        return "inventory/frontend routines form an isolatable UI-domain proof chain"
    if domain == "camera":
        return "camera/spotcam routines are large but domain-local enough for a focused audit"
    if domain == "input":
        return "runtime input is high-priority but cross-platform, so scope must be narrow"
    if top.nd == "yes":
        return "contains ND markers that can be audited without source reconstruction"
    return "remaining mapped non-final domain after savegame closure"


def build_reprioritization(repo: Path) -> ReprioritizationPlan:
    repo = Path(repo)
    input_path = repo / INPUT_PRIORITY
    rows = read_priority_rows(input_path)

    excluded_count = sum(1 for row in rows if is_closed_chain(row))
    remaining = [row for row in rows if not is_closed_chain(row)]

    grouped: dict[str, dict[str, object]] = {}
    bucketed: dict[str, list[FunctionCandidate]] = defaultdict(list)
    for row in remaining:
        domain_id, label = classify_domain(row)
        grouped.setdefault(domain_id, {"label": label})
        bucketed[domain_id].append(to_function(row))

    domains: list[DomainCandidate] = []
    for domain_id, functions in bucketed.items():
        functions.sort(key=lambda item: (-item.score, item.file, item.line, item.name))
        top_functions = tuple(functions[:5])
        score = sum(function.score for function in functions[:8]) + len(functions) * 25
        mapped_count = sum(1 for function in functions if function.file and function.bucket in {"P0", "P1", "P2"})
        nd_count = sum(1 for function in functions if function.nd == "yes")
        runtime_count = sum(1 for function in functions if function.runtime_focus == "yes")
        top = functions[0]
        domains.append(
            DomainCandidate(
                rank=0,
                domain_id=domain_id,
                label=str(grouped[domain_id]["label"]),
                status="candidate",
                score=score,
                candidate_count=len(functions),
                mapped_count=mapped_count,
                nd_count=nd_count,
                runtime_count=runtime_count,
                top_function=top.name,
                top_file=top.file,
                functions=top_functions,
                rationale=domain_rationale(domain_id, functions),
                next_action="defer until higher-ranked domain is selected",
            )
        )

    domains.sort(key=lambda item: (-item.score, item.domain_id))
    required_domains = {"audio-effects", "collision", "inventory", "camera", "input"}
    selected_domains = domains[:10]
    selected_ids = {domain.domain_id for domain in selected_domains}
    for domain in domains[10:]:
        if domain.domain_id in required_domains and domain.domain_id not in selected_ids:
            selected_domains.append(domain)
            selected_ids.add(domain.domain_id)
    selected_domains.sort(key=lambda item: (-item.score, item.domain_id))

    ranked: list[DomainCandidate] = []
    for index, domain in enumerate(selected_domains, start=1):
        next_action = (
            f"create RE-045 for {domain.domain_id} proof-first audit"
            if index == 1
            else "defer until higher-ranked domain is selected"
        )
        ranked.append(
            DomainCandidate(
                rank=index,
                domain_id=domain.domain_id,
                label=domain.label,
                status=domain.status,
                score=domain.score,
                candidate_count=domain.candidate_count,
                mapped_count=domain.mapped_count,
                nd_count=domain.nd_count,
                runtime_count=domain.runtime_count,
                top_function=domain.top_function,
                top_file=domain.top_file,
                functions=domain.functions,
                rationale=domain.rationale,
                next_action=next_action,
            )
        )

    return ReprioritizationPlan(
        story_id="RE-044",
        status="post-restoreleveldata-domain-reprioritization-ready",
        restoreleveldata_chain_status="closed-by-RE-043",
        code_change_readiness="documentation-only-selection-gate",
        next_ticket="RE-045",
        source_csv=INPUT_PRIORITY,
        excluded_closed_chain_count=excluded_count,
        domains=tuple(ranked),
    )


def write_csv(path: Path, plan: ReprioritizationPlan) -> None:
    fields = [
        "domain_id",
        "rank",
        "status",
        "score",
        "candidate_count",
        "mapped_count",
        "nd_count",
        "runtime_count",
        "top_function",
        "top_file",
        "rationale",
        "next_action",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for domain in plan.domains:
            writer.writerow({field: getattr(domain, field) for field in fields})


def domain_lines(domain: DomainCandidate) -> list[str]:
    lines = [
        f"- `#{domain.rank}` `{domain.domain_id}` — {domain.label}",
        f"  - status: `{domain.status}`; score: `{domain.score}`; candidates: `{domain.candidate_count}`; ND: `{domain.nd_count}`; runtime: `{domain.runtime_count}`",
        f"  - top: `{domain.top_function}` in `{domain.top_file}`",
        f"  - rationale: {domain.rationale}",
        f"  - next action: `{domain.next_action}`",
        "  - representative functions:",
    ]
    for function in domain.functions[:3]:
        lines.append(
            f"    - `{function.name}` — `{function.file}:{function.line}`; bucket `{function.bucket}`; status `{function.status}`; score `{function.score}`"
        )
    return lines


def write_markdown(path: Path, plan: ReprioritizationPlan) -> None:
    lines = [
        "# RE-044 — Post-RestoreLevelData domain reprioritization",
        "",
        f"Source: `{plan.source_csv}`",
        f"RestoreLevelData chain: `{plan.restoreleveldata_chain_status}`",
        f"Excluded closed-chain candidates: `{plan.excluded_closed_chain_count}`",
        f"Code-change readiness: `{plan.code_change_readiness}`",
        f"Recommended next ticket: `{plan.next_ticket}`",
        "",
        "## Progress tracker",
        "",
        "- [x] Closed RestoreLevelData chain excluded.",
        "- [x] Existing priority CSV consumed without raw evidence expansion.",
        "- [x] Domain-level shortlist generated.",
        "- [x] Next ticket selected as a proof-first audit gate.",
        "",
        "## Domain shortlist",
        "",
    ]
    for domain in plan.domains:
        lines.extend(domain_lines(domain))
    lines.extend([
        "",
        "## Selection rule",
        "",
        "Domains are ranked from existing metadata-only priority rows after excluding the closed savegame chain. Scores aggregate top candidate weights plus small breadth bonuses; the result is a selection gate, not a source-patch authorization.",
        "",
        "## Safety decision",
        "",
        "No production source patch is implied by RE-044. The selected RE-045 domain must start with metadata-only proof artifacts and its own readiness tracker.",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_story(path: Path, plan: ReprioritizationPlan) -> None:
    selected = plan.domains[0]
    lines = [
        "# RE-044 — Post-RestoreLevelData domain reprioritization",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Choose the next reverse-engineering domain after RE-043 closed the RestoreLevelData source reconstruction chain.",
        "",
        "## Scope",
        "",
        "- depends on: `RE-043`, `RE-004`",
        f"- source priority input: `{plan.source_csv}`",
        "- safety contract: `metadata-only; no opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records; no raw addresses in generated outputs`",
        "",
        "## Progress",
        "",
        "- [x] Closed RestoreLevelData chain excluded.",
        "- [x] Existing backlog metadata consumed.",
        "- [x] New domain shortlist generated.",
        "- [x] Source patch authorization withheld pending domain-specific proof.",
        "",
        "## Generated artifacts",
        "",
        "- `docs/reverse/generated/re044-domain-reprioritization.csv`",
        "- `docs/reverse/functions/re044-post-restoreleveldata-reprioritization.md`",
        "",
        "## Findings",
        "",
        f"- RestoreLevelData chain status: `{plan.restoreleveldata_chain_status}`",
        f"- excluded closed-chain candidates: `{plan.excluded_closed_chain_count}`",
        f"- top selected domain: `{selected.domain_id}`",
        f"- top selected function: `{selected.top_function}` in `{selected.top_file}`",
        f"- code-change readiness: `{plan.code_change_readiness}`",
        "",
        "## Selection decision",
        "",
        f"- decision: `start-new-domain-proof-chain`",
        f"- selected domain: `{selected.domain_id}`",
        f"- safe next action: `{selected.next_action}`",
        f"- Recommended next ticket: `{plan.next_ticket}`",
        "",
        "Do not patch production source or add `(F)`, `(D)`, or `(**)` markers from RE-044 alone.",
        "",
        "## Validation",
        "",
        "- `python3 -m pytest tests/reverse/test_re044_post_restoreleveldata_reprioritization.py -q`",
        "- metadata-only guard over RE-044 outputs",
        "",
        "## Next step",
        "",
        f"{plan.next_ticket}: open a proof-first metadata-only audit for `{selected.domain_id}` before any source reconstruction or status marker change.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_all_artifacts(plan: ReprioritizationPlan, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    csv_path = repo / CSV_OUTPUT
    md_path = repo / MD_OUTPUT
    story_path = repo / STORY_OUTPUT
    write_csv(csv_path, plan)
    write_markdown(md_path, plan)
    write_story(story_path, plan)
    return {"csv": csv_path, "md": md_path, "story": story_path}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="TOMB5 repo root; default: current directory")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    plan = build_reprioritization(repo)
    written = write_all_artifacts(plan, repo)
    print(f"wrote RE-044 domain reprioritization to {written['csv']}")
    print(f"wrote RE-044 markdown to {written['md']}")
    print(f"wrote RE-044 story to {written['story']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
