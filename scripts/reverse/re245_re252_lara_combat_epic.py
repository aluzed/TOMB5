#!/usr/bin/env python3
"""Generate RE-245..RE-252 lara-combat epic artifacts."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

UPSTREAM_HANDOFF = "docs/reverse/generated/re244-post-module-spec-psx-handoff.csv"
UPSTREAM_SELECTION = "docs/reverse/generated/re244-post-module-spec-psx-domain-selection.csv"
FUNCTION_PRIORITY = "docs/reverse/generated/function-priority.csv"

AUDIT_CSV = "docs/reverse/generated/re245-lara-combat-proof-first-audit.csv"
SUBCLUSTERS_CSV = "docs/reverse/generated/re245-lara-combat-subclusters.csv"
PARSER_ARTIFACTS_CSV = "docs/reverse/generated/re249-lara-combat-parser-artifacts.csv"
EPIC_CSV = "docs/reverse/generated/re245-re252-lara-combat-epic.csv"
GATE_CSV = "docs/reverse/generated/re251-lara-combat-source-patch-gates.csv"
NEXT_SELECTION_CSV = "docs/reverse/generated/re252-post-lara-combat-domain-selection.csv"
HANDOFF_CSV = "docs/reverse/generated/re252-post-lara-combat-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re245-re252-lara-combat-epic.md"
STORY_INDEX = "docs/stories/RE-245-RE-252-lara-combat-epic.md"

FORBIDDEN = (
    "word_le_hex",
    "payload_offset",
    "dump row",
    "opcode",
    "machine word",
    "call_address",
    "branch target",
    "call target",
    "0x800",
)
STALE_FRAGMENTS = (
    "module-spec_psx closed",
    "post-module-spec-psx",
    "platform-main-lifecycle",
    "frontend-loadsave-flow",
    "platform-memory",
    "open re-245 lara-combat proof-first audit",
)
PARSER_ARTIFACTS = frozenset({"if", "for", "while", "switch", "else"})
BLOCKER = "missing-lara-combat-source-contract-and-non-raw-equivalence-proof"

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
CLOSED_CHAIN_FUNCTIONS = {"RestoreLevelData", "SaveLevelData"}
CLOSED_CHAIN_FILES = {"GAME/SAVEGAME.C"}


@dataclass(frozen=True)
class AuditRow:
    rank: int
    domain_id: str
    subcluster: str
    function: str
    file: str
    line: int
    status: str
    mapped: str
    runtime_focus: str
    nd: str
    caller_count: int
    callee_count: int
    readiness: str
    source_patch_ready: str
    marker_ready: str
    blocker: str


@dataclass(frozen=True)
class ParserArtifactRow:
    rank: int
    domain_id: str
    function: str
    file: str
    line: int
    reason: str
    action: str


@dataclass(frozen=True)
class SubclusterRow:
    subcluster: str
    rank: int
    candidate_count: int
    mapped_count: int
    nd_count: int
    runtime_count: int
    top_function: str
    outcome: str
    code_change_ready: str
    marker_ready: str
    blocker: str
    closed_by_story: str


@dataclass(frozen=True)
class StoryRow:
    story_id: str
    topic: str
    scope: str
    candidate_count: int
    readiness: str
    source_patch_ready: str
    marker_ready: str
    blocker: str
    artifact: str


@dataclass(frozen=True)
class GateRow:
    gate: str
    story_id: str
    scope: str
    ready_count: int
    blocked_count: int
    decision: str
    blocker: str


@dataclass(frozen=True)
class NextDomainRow:
    rank: int
    domain_id: str
    status: str
    score: int
    candidate_count: int
    mapped_count: int
    nd_count: int
    runtime_count: int
    top_function: str
    top_file: str
    next_ticket: str
    next_action: str
    code_change_readiness: str


@dataclass(frozen=True)
class HandoffRow:
    next_ticket: str
    next_topic: str
    selected_domain: str
    selected_pivot: str
    outcome: str
    reason: str
    dependency: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class LaraCombatEpic:
    story_range: str
    upstream_ticket: str
    domain_id: str
    selected_pivot: str
    raw_priority_count: int
    parser_artifact_count: int
    candidate_count: int
    closed_candidate_count: int
    runtime_count: int
    nd_count: int
    code_change_ready_count: int
    marker_ready_count: int
    domain_outcome: str
    blocker: str
    audit_rows: tuple[AuditRow, ...]
    parser_artifact_rows: tuple[ParserArtifactRow, ...]
    subcluster_rows: tuple[SubclusterRow, ...]
    story_rows: tuple[StoryRow, ...]
    gate_rows: tuple[GateRow, ...]
    next_domain_rows: tuple[NextDomainRow, ...]
    handoff: HandoffRow


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_int(value: str | None) -> int:
    return int(value or 0)


def classify_domain(row: dict[str, str]) -> str:
    haystack = f"{row.get('file', '')} {row.get('repo_function', '')}".upper()
    for domain_id, terms in DOMAIN_RULES:
        if any(term in haystack for term in terms):
            return domain_id
    return "module-" + row.get("file", "unknown").split("/", 1)[0].lower()


def subcluster_for(row: dict[str, str]) -> str:
    function = row.get("repo_function", "")
    if function in {"DoProperDetection", "find_target_point"}:
        return "target-detection"
    if function in {"LaraGetNewTarget", "LaraTargetInfo", "AimWeapon"}:
        return "target-acquisition"
    if function in {"FireWeapon", "LaraGun"}:
        return "weapon-fire-control"
    raise ValueError(f"unclassified lara-combat row: {function} {row.get('file', '')}")


def validate_upstream(repo: Path) -> None:
    handoff = read_csv(repo / UPSTREAM_HANDOFF)
    if len(handoff) != 1:
        raise ValueError("RE-244 handoff must contain exactly one row")
    expected = {
        "next_ticket": "RE-245",
        "next_topic": "lara-combat-proof-first-audit",
        "selected_domain": "lara-combat",
        "selected_pivot": "DoProperDetection",
    }
    for key, value in expected.items():
        if handoff[0].get(key) != value:
            raise ValueError(f"RE-244 handoff drift: {key}={handoff[0].get(key)!r}")
    selection = read_csv(repo / UPSTREAM_SELECTION)
    if not selection or selection[0].get("domain_id") != "lara-combat":
        raise ValueError("RE-244 selection must rank lara-combat first")
    if selection[0].get("top_function") != "DoProperDetection" or parse_int(selection[0].get("candidate_count")) != 10:
        raise ValueError("RE-244 selected lara-combat scope drifted")


def lara_priority_rows(repo: Path) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    rows: list[dict[str, str]] = []
    artifacts: list[dict[str, str]] = []
    for row in read_csv(repo / FUNCTION_PRIORITY):
        if row.get("repo_function") in CLOSED_CHAIN_FUNCTIONS or row.get("file") in CLOSED_CHAIN_FILES:
            continue
        if classify_domain(row) != "lara-combat":
            continue
        if row.get("repo_function", "") in PARSER_ARTIFACTS:
            artifacts.append(row)
        else:
            rows.append(row)
    key = lambda item: (-parse_int(item.get("score")), item.get("file", ""), parse_int(item.get("line")), item.get("repo_function", ""))
    rows.sort(key=key)
    artifacts.sort(key=key)
    selected = [row.get("repo_function") for row in rows]
    expected = ["DoProperDetection", "LaraGetNewTarget", "FireWeapon", "LaraGun", "LaraTargetInfo", "find_target_point", "AimWeapon"]
    if selected != expected or len(artifacts) != 3:
        raise ValueError(f"lara-combat function scope drifted: selected={selected!r} artifacts={len(artifacts)}")
    return rows, artifacts


def build_audit_and_artifact_rows(repo: Path) -> tuple[tuple[AuditRow, ...], tuple[ParserArtifactRow, ...]]:
    rows, artifacts = lara_priority_rows(repo)
    audit: list[AuditRow] = []
    for rank, row in enumerate(rows, start=1):
        audit.append(AuditRow(
            rank=rank,
            domain_id="lara-combat",
            subcluster=subcluster_for(row),
            function=row.get("repo_function", ""),
            file=row.get("file", ""),
            line=parse_int(row.get("line")),
            status=row.get("status", ""),
            mapped=row.get("mapped", ""),
            runtime_focus=row.get("runtime_focus", ""),
            nd=row.get("nd", ""),
            caller_count=parse_int(row.get("caller_count")),
            callee_count=parse_int(row.get("callee_count")),
            readiness="blocked",
            source_patch_ready="no",
            marker_ready="no",
            blocker=BLOCKER,
        ))
    parser_rows = tuple(ParserArtifactRow(
        rank=index,
        domain_id="lara-combat",
        function=row.get("repo_function", ""),
        file=row.get("file", ""),
        line=parse_int(row.get("line")),
        reason="C keyword/parser artifact from source scanner, not a function scope",
        action="excluded-from-function-scope",
    ) for index, row in enumerate(artifacts, start=1))
    return tuple(audit), parser_rows


def build_subcluster_rows(audit_rows: tuple[AuditRow, ...]) -> tuple[SubclusterRow, ...]:
    order = ("target-detection", "target-acquisition", "weapon-fire-control")
    story_by_subcluster = {
        "target-detection": "RE-246",
        "target-acquisition": "RE-247",
        "weapon-fire-control": "RE-248",
    }
    grouped: dict[str, list[AuditRow]] = defaultdict(list)
    for row in audit_rows:
        grouped[row.subcluster].append(row)
    result: list[SubclusterRow] = []
    for rank, subcluster in enumerate(order, start=1):
        rows = grouped[subcluster]
        result.append(SubclusterRow(
            subcluster=subcluster,
            rank=rank,
            candidate_count=len(rows),
            mapped_count=sum(1 for row in rows if row.mapped == "yes"),
            nd_count=sum(1 for row in rows if row.nd == "yes"),
            runtime_count=sum(1 for row in rows if row.runtime_focus == "yes"),
            top_function=rows[0].function,
            outcome="blocked-no-patch",
            code_change_ready="no",
            marker_ready="no",
            blocker=BLOCKER,
            closed_by_story=story_by_subcluster[subcluster],
        ))
    return tuple(result)


def build_story_rows() -> tuple[StoryRow, ...]:
    specs = (
        ("RE-245", "lara-combat-proof-first-audit", "all lara-combat candidates plus parser-artifact suppression", 10, "opening-audit"),
        ("RE-246", "lara-combat-target-detection-chain", "target-detection candidates", 2, "documentation-only"),
        ("RE-247", "lara-combat-target-acquisition-chain", "target-acquisition candidates", 3, "documentation-only"),
        ("RE-248", "lara-combat-weapon-fire-control-chain", "weapon-fire-control candidates", 2, "documentation-only"),
        ("RE-249", "lara-combat-parser-artifact-reconciliation", "parser-artifact rows excluded from function scope", 3, "documentation-only"),
        ("RE-250", "lara-combat-state-equivalence-gate", "all scoped lara-combat rows", 7, "documentation-only"),
        ("RE-251", "lara-combat-source-patch-gate", "ready lara-combat rows", 7, "documentation-only"),
        ("RE-252", "post-lara-combat-domain-selection", "remaining domain backlog after lara-combat", 0, "next-domain-selected"),
    )
    return tuple(StoryRow(
        story_id=story_id,
        topic=topic,
        scope=scope,
        candidate_count=count,
        readiness="blocked",
        source_patch_ready="no",
        marker_ready="no",
        blocker=BLOCKER,
        artifact=artifact,
    ) for story_id, topic, scope, count, artifact in specs)


def build_gate_rows() -> tuple[GateRow, ...]:
    return (
        GateRow("equivalence", "RE-250", "all scoped lara-combat rows", 0, 7, "deny", BLOCKER),
        GateRow("source-patch", "RE-251", "ready lara-combat rows", 0, 7, "deny", "zero rows passed the equivalence gate"),
        GateRow("marker", "RE-251", "ready lara-combat rows", 0, 7, "deny", "zero rows passed the source-patch gate"),
    )


def build_next_domain_rows(repo: Path) -> tuple[NextDomainRow, ...]:
    source_rows = read_csv(repo / UPSTREAM_SELECTION)
    remaining = [row for row in source_rows if row.get("domain_id") != "lara-combat"]
    if not remaining or remaining[0].get("domain_id") != "inventory":
        raise ValueError("post-lara-combat next-domain selection drifted")
    result: list[NextDomainRow] = []
    for rank, row in enumerate(remaining, start=1):
        selected = rank == 1
        result.append(NextDomainRow(
            rank=rank,
            domain_id=row["domain_id"],
            status=row["status"],
            score=parse_int(row["score"]),
            candidate_count=parse_int(row["candidate_count"]),
            mapped_count=parse_int(row["mapped_count"]),
            nd_count=parse_int(row["nd_count"]),
            runtime_count=parse_int(row["runtime_count"]),
            top_function=row["top_function"],
            top_file=row["top_file"],
            next_ticket="RE-253" if selected else "TBD",
            next_action="open RE-253 inventory proof-first audit" if selected else "defer until higher-ranked post-lara-combat domain is selected",
            code_change_readiness="blocked",
        ))
    return tuple(result)


def build_epic(repo: Path) -> LaraCombatEpic:
    repo = Path(repo)
    validate_upstream(repo)
    audit_rows, parser_artifact_rows = build_audit_and_artifact_rows(repo)
    subcluster_rows = build_subcluster_rows(audit_rows)
    story_rows = build_story_rows()
    gate_rows = build_gate_rows()
    next_domain_rows = build_next_domain_rows(repo)
    selected = next_domain_rows[0]
    handoff = HandoffRow(
        next_ticket="RE-253",
        next_topic="inventory-proof-first-audit",
        selected_domain=selected.domain_id,
        selected_pivot=selected.top_function,
        outcome="lara-combat-closed-next-domain-selected",
        reason="lara-combat closed as a documentation-only terminal blocker after parser artifacts were excluded; next ranked remaining domain selected",
        dependency="RE-245..RE-252 lara-combat epic",
        code_change_readiness="blocked",
        stop_condition="inventory proof-first audit emitted",
    )
    return LaraCombatEpic(
        story_range="RE-245..RE-252",
        upstream_ticket="RE-244",
        domain_id="lara-combat",
        selected_pivot="DoProperDetection",
        raw_priority_count=len(audit_rows) + len(parser_artifact_rows),
        parser_artifact_count=len(parser_artifact_rows),
        candidate_count=len(audit_rows),
        closed_candidate_count=sum(row.candidate_count for row in subcluster_rows),
        runtime_count=sum(1 for row in audit_rows if row.runtime_focus == "yes"),
        nd_count=sum(1 for row in audit_rows if row.nd == "yes"),
        code_change_ready_count=0,
        marker_ready_count=0,
        domain_outcome="documentation-only-terminal-blocker",
        blocker=BLOCKER,
        audit_rows=audit_rows,
        parser_artifact_rows=parser_artifact_rows,
        subcluster_rows=subcluster_rows,
        story_rows=story_rows,
        gate_rows=gate_rows,
        next_domain_rows=next_domain_rows,
        handoff=handoff,
    )


def write_rows(path: Path, cls: type, rows: list[dict[str, object]]) -> None:
    fields = list(cls.__dataclass_fields__)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_md(path: Path, epic: LaraCombatEpic) -> None:
    lines = [
        "# RE-245..RE-252 lara-combat epic",
        "",
        f"Domain: `{epic.domain_id}`",
        f"Pivot: `{epic.selected_pivot}`",
        f"Outcome: `{epic.domain_outcome}`",
        f"Blocker: `{epic.blocker}`",
        f"Raw priority rows: `{epic.raw_priority_count}`",
        f"Parser artifacts excluded: `{epic.parser_artifact_count}`",
        f"Candidates closed/documented: `{epic.closed_candidate_count}` / `{epic.candidate_count}`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-244 handoff consumed.",
        "- [x] Proof-first audit emitted.",
        "- [x] Parser artifacts excluded before function-scope closure.",
        "- [x] Target detection, target acquisition, and weapon fire-control subclusters documented.",
        "- [x] State/equivalence and patch gates denied with zero ready rows.",
        "- [x] Next proof domain selected from the remaining ranked backlog.",
        "",
        "## Subcluster closures",
        "",
    ]
    for row in epic.subcluster_rows:
        lines.append(f"- `{row.closed_by_story}` `{row.subcluster}`: {row.candidate_count} candidate(s), top `{row.top_function}`, outcome `{row.outcome}`.")
    lines.extend([
        "",
        "## Terminal decision",
        "",
        "This is a documentation-only terminal blocker for lara-combat. No production source or marker change is authorized.",
        "",
        "## Next domain",
        "",
        f"Next proof domain: `{epic.handoff.selected_domain}`",
        f"Selected pivot: `{epic.handoff.selected_pivot}`",
        f"Recommended next ticket: `{epic.handoff.next_ticket}`",
        "",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story_index(path: Path, epic: LaraCombatEpic) -> None:
    lines = [
        "# RE-245..RE-252 — lara-combat epic",
        "",
        "Status: Done",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-245..RE-252 range generated as a bounded epic.",
        "- [x] Parser artifacts separated from function candidates.",
        "- [x] All lara-combat subclusters documented.",
        "- [x] Source-patch and marker gates denied safely.",
        "- [x] Post-domain selection handoff emitted.",
        "",
        "## Readiness",
        "",
        "Readiness: `blocked`",
        f"Blocker: `{epic.blocker}`",
        "No production source or marker change is authorized by this epic.",
        "",
        "## Stories",
        "",
    ]
    for row in epic.story_rows:
        lines.append(f"- `{row.story_id}` — `{row.topic}` / readiness `{row.readiness}`")
    lines.extend([
        "",
        "## Next step",
        "",
        f"{epic.handoff.next_ticket}: `{epic.handoff.next_topic}` / pivot `{epic.handoff.selected_pivot}`.",
        "",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story(path: Path, row: StoryRow, epic: LaraCombatEpic) -> None:
    lines = [
        f"# {row.story_id} — {row.topic}",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        f"Advance `{row.topic}` within the lara-combat epic using metadata-only proof artifacts.",
        "",
        "## Scope",
        "",
        f"- scope: `{row.scope}`",
        f"- candidates: `{row.candidate_count}`",
        "- source contract: generated metadata only; no source or marker edit",
        "",
        "## Progress tracker",
        "",
        "- [x] Upstream handoff consumed.",
        "- [x] Story outcome generated deterministically.",
        "- [x] Readiness and blocker recorded.",
        "- [x] No production source or marker change is authorized.",
        "",
        "## Readiness",
        "",
        f"Readiness: `{row.readiness}`",
        f"Source patch ready: `{row.source_patch_ready}`",
        f"Marker ready: `{row.marker_ready}`",
        f"Blocker: `{row.blocker}`",
        "",
        "## Validation",
        "",
        "- `python3 -m pytest tests/reverse/test_re245_re252_lara_combat_epic.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over RE-245..RE-252 outputs",
        "",
        "## Next step",
        "",
        f"Epic handoff: `{epic.handoff.next_ticket}` / `{epic.handoff.next_topic}`.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_all_artifacts(epic: LaraCombatEpic, repo: Path) -> dict[str, object]:
    repo = Path(repo)
    paths: dict[str, object] = {
        "audit_csv": repo / AUDIT_CSV,
        "subclusters_csv": repo / SUBCLUSTERS_CSV,
        "parser_artifacts_csv": repo / PARSER_ARTIFACTS_CSV,
        "epic_csv": repo / EPIC_CSV,
        "gate_csv": repo / GATE_CSV,
        "next_selection_csv": repo / NEXT_SELECTION_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story_index": repo / STORY_INDEX,
    }
    write_rows(paths["audit_csv"], AuditRow, [row.__dict__ for row in epic.audit_rows])
    write_rows(paths["subclusters_csv"], SubclusterRow, [row.__dict__ for row in epic.subcluster_rows])
    write_rows(paths["parser_artifacts_csv"], ParserArtifactRow, [row.__dict__ for row in epic.parser_artifact_rows])
    write_rows(paths["epic_csv"], StoryRow, [row.__dict__ for row in epic.story_rows])
    write_rows(paths["gate_csv"], GateRow, [row.__dict__ for row in epic.gate_rows])
    write_rows(paths["next_selection_csv"], NextDomainRow, [row.__dict__ for row in epic.next_domain_rows])
    write_rows(paths["handoff_csv"], HandoffRow, [epic.handoff.__dict__])
    write_md(paths["md"], epic)
    write_story_index(paths["story_index"], epic)
    story_paths: dict[str, Path] = {}
    for row in epic.story_rows:
        story_path = repo / "docs" / "stories" / f"{row.story_id}-{row.topic}.md"
        write_story(story_path, row, epic)
        story_paths[row.story_id] = story_path
    paths["stories"] = story_paths
    return paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    args = parser.parse_args()
    epic = build_epic(Path(args.repo))
    write_all_artifacts(epic, Path(args.repo))
    print("generated RE-245..RE-252 lara-combat artifacts")
    print(f"next_ticket={epic.handoff.next_ticket}")
    print(f"next_domain={epic.handoff.selected_domain}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
