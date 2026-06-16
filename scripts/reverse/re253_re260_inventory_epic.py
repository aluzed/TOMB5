#!/usr/bin/env python3
"""Generate RE-253..RE-260 inventory epic artifacts."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass, fields, asdict
from pathlib import Path

UPSTREAM_HANDOFF = "docs/reverse/generated/re252-post-lara-combat-handoff.csv"
UPSTREAM_SELECTION = "docs/reverse/generated/re252-post-lara-combat-domain-selection.csv"
FUNCTION_PRIORITY = "docs/reverse/generated/function-priority.csv"

AUDIT_CSV = "docs/reverse/generated/re253-inventory-proof-first-audit.csv"
SUBCLUSTERS_CSV = "docs/reverse/generated/re253-inventory-subclusters.csv"
PARSER_ARTIFACTS_CSV = "docs/reverse/generated/re257-inventory-parser-artifacts.csv"
EPIC_CSV = "docs/reverse/generated/re253-re260-inventory-epic.csv"
GATE_CSV = "docs/reverse/generated/re259-inventory-source-patch-gates.csv"
NEXT_SELECTION_CSV = "docs/reverse/generated/re260-post-inventory-domain-selection.csv"
HANDOFF_CSV = "docs/reverse/generated/re260-post-inventory-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re253-re260-inventory-epic.md"
STORY_INDEX = "docs/stories/RE-253-RE-260-inventory-epic.md"

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
    "lara-combat closed",
    "post-lara-combat",
    "do proper detection",
    "DoProperDetection".lower(),
    "open re-253 inventory proof-first audit",
    "module-spec_psx",
)
PARSER_ARTIFACTS = frozenset({"if", "for", "while", "switch", "else"})
BLOCKER = "missing-inventory-source-contract-and-non-raw-equivalence-proof"

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
CLOSED_DOMAINS = {"lara-combat", "inventory"}


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
class InventoryEpic:
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
    haystack = f"{row.get('file', '')} {row.get('repo_function', '')} {row.get('top_file', '')} {row.get('top_function', '')}".upper()
    for domain_id, terms in DOMAIN_RULES:
        if any(term in haystack for term in terms):
            return domain_id
    return "module-" + (row.get("file") or row.get("top_file") or "unknown").split("/", 1)[0].lower()


def subcluster_for(row: dict[str, str]) -> str:
    function = row.get("repo_function", "")
    if function in {"S_CallInventory2", "use_current_item", "do_keypad_mode"}:
        return "menu-flow"
    if function == "draw_current_object_list":
        return "object-list"
    if function == "Requester":
        return "requester-service"
    raise ValueError(f"unclassified inventory row: {function} {row.get('file', '')}")


def validate_upstream(repo: Path) -> None:
    handoff = read_csv(repo / UPSTREAM_HANDOFF)
    if len(handoff) != 1:
        raise ValueError("RE-252 handoff must contain exactly one row")
    expected = {
        "next_ticket": "RE-253",
        "next_topic": "inventory-proof-first-audit",
        "selected_domain": "inventory",
        "selected_pivot": "S_CallInventory2",
    }
    for key, value in expected.items():
        if handoff[0].get(key) != value:
            raise ValueError(f"RE-252 handoff drift: {key}={handoff[0].get(key)!r}")
    selection = read_csv(repo / UPSTREAM_SELECTION)
    if not selection or selection[0].get("domain_id") != "inventory":
        raise ValueError("RE-252 selection must rank inventory first")
    if selection[0].get("top_function") != "S_CallInventory2" or parse_int(selection[0].get("candidate_count")) != 11:
        raise ValueError("RE-252 selected inventory scope drifted")


def inventory_priority_rows(repo: Path) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    rows: list[dict[str, str]] = []
    artifacts: list[dict[str, str]] = []
    for row in read_csv(repo / FUNCTION_PRIORITY):
        if classify_domain(row) != "inventory":
            continue
        if row.get("repo_function") in PARSER_ARTIFACTS:
            artifacts.append(row)
        else:
            rows.append(row)
    expected = ["S_CallInventory2", "draw_current_object_list", "Requester", "do_keypad_mode", "use_current_item"]
    if [row["repo_function"] for row in rows] != expected:
        raise ValueError(f"inventory scope drifted: {[row['repo_function'] for row in rows]!r}")
    if len(artifacts) != 6 or {row["repo_function"] for row in artifacts} != {"if"}:
        raise ValueError("inventory parser-artifact scope drifted")
    return rows, artifacts


def build_next_domain_rows(repo: Path) -> tuple[NextDomainRow, ...]:
    source_rows = read_csv(repo / UPSTREAM_SELECTION)
    out: list[NextDomainRow] = []
    for row in source_rows:
        if row.get("domain_id") in CLOSED_DOMAINS:
            continue
        rank = len(out) + 1
        domain = row["domain_id"]
        is_next = rank == 1
        out.append(
            NextDomainRow(
                rank=rank,
                domain_id=domain,
                status=row.get("status", "candidate"),
                score=parse_int(row.get("score")),
                candidate_count=parse_int(row.get("candidate_count")),
                mapped_count=parse_int(row.get("mapped_count")),
                nd_count=parse_int(row.get("nd_count")),
                runtime_count=parse_int(row.get("runtime_count")),
                top_function=row.get("top_function", ""),
                top_file=row.get("top_file", ""),
                next_ticket="RE-261" if is_next else "TBD",
                next_action=(
                    f"open RE-261 {domain} proof-first audit"
                    if is_next
                    else "defer until higher-ranked post-inventory domain is selected"
                ),
                code_change_readiness="blocked",
            )
        )
    if not out or out[0].domain_id != "input" or out[0].top_function != "S_UpdateInput":
        raise ValueError("post-inventory next-domain selection drifted")
    return tuple(out)


def build_epic(repo: Path) -> InventoryEpic:
    validate_upstream(repo)
    rows, artifacts = inventory_priority_rows(repo)
    audit_rows = tuple(
        AuditRow(
            rank=i,
            domain_id="inventory",
            subcluster=subcluster_for(row),
            function=row["repo_function"],
            file=row["file"],
            line=parse_int(row.get("line")),
            status=row.get("status", ""),
            mapped=row.get("mapping_status", ""),
            runtime_focus=row.get("runtime_focus", "no"),
            nd=row.get("nd", "no"),
            caller_count=parse_int(row.get("caller_count")),
            callee_count=parse_int(row.get("callee_count")),
            readiness="blocked",
            source_patch_ready="no",
            marker_ready="no",
            blocker=BLOCKER,
        )
        for i, row in enumerate(rows, 1)
    )
    parser_artifact_rows = tuple(
        ParserArtifactRow(
            rank=parse_int(row.get("priority_rank")),
            domain_id="inventory",
            function=row["repo_function"],
            file=row["file"],
            line=parse_int(row.get("line")),
            reason="c-keyword-parser-artifact-not-a-function",
            action="excluded-from-function-scope",
        )
        for row in artifacts
    )
    grouped: dict[str, list[AuditRow]] = defaultdict(list)
    for row in audit_rows:
        grouped[row.subcluster].append(row)
    order = ["menu-flow", "object-list", "requester-service"]
    story_for = {"menu-flow": "RE-254", "object-list": "RE-255", "requester-service": "RE-256"}
    subcluster_rows = tuple(
        SubclusterRow(
            subcluster=name,
            rank=i,
            candidate_count=len(grouped[name]),
            mapped_count=sum(1 for row in grouped[name] if row.mapped == "mapped"),
            nd_count=sum(1 for row in grouped[name] if row.nd == "yes"),
            runtime_count=sum(1 for row in grouped[name] if row.runtime_focus == "yes"),
            top_function=grouped[name][0].function,
            outcome="blocked-no-patch",
            code_change_ready="no",
            marker_ready="no",
            blocker=BLOCKER,
            closed_by_story=story_for[name],
        )
        for i, name in enumerate(order, 1)
    )
    story_rows = (
        StoryRow("RE-253", "inventory-proof-first-audit", "inventory domain scope from RE-252 handoff", 5, "blocked", "no", "no", BLOCKER, AUDIT_CSV),
        StoryRow("RE-254", "inventory-menu-flow-chain", "S_CallInventory2, use_current_item, do_keypad_mode", 3, "blocked", "no", "no", BLOCKER, SUBCLUSTERS_CSV),
        StoryRow("RE-255", "inventory-object-list-chain", "draw_current_object_list", 1, "blocked", "no", "no", BLOCKER, SUBCLUSTERS_CSV),
        StoryRow("RE-256", "inventory-requester-chain", "Requester", 1, "blocked", "no", "no", BLOCKER, SUBCLUSTERS_CSV),
        StoryRow("RE-257", "inventory-parser-artifact-reconciliation", "excluded C keyword parser artifacts", 6, "blocked", "no", "no", BLOCKER, PARSER_ARTIFACTS_CSV),
        StoryRow("RE-258", "inventory-state-equivalence-gate", "inventory state/equivalence proof", 5, "blocked", "no", "no", BLOCKER, GATE_CSV),
        StoryRow("RE-259", "inventory-source-patch-gate", "source patch and marker readiness", 5, "blocked", "no", "no", BLOCKER, GATE_CSV),
        StoryRow("RE-260", "post-inventory-domain-selection", "remaining ranked domains after inventory closure", 0, "blocked", "no", "no", BLOCKER, NEXT_SELECTION_CSV),
    )
    gate_rows = (
        GateRow("equivalence", "RE-258", "all inventory candidates", 0, len(audit_rows), "deny", BLOCKER),
        GateRow("source-patch", "RE-259", "all inventory candidates", 0, len(audit_rows), "deny", BLOCKER),
        GateRow("marker", "RE-259", "all inventory candidates", 0, len(audit_rows), "deny", BLOCKER),
    )
    next_rows = build_next_domain_rows(repo)
    handoff = HandoffRow(
        next_ticket="RE-261",
        next_topic="input-proof-first-audit",
        selected_domain=next_rows[0].domain_id,
        selected_pivot=next_rows[0].top_function,
        outcome="inventory-closed-next-domain-selected",
        reason="inventory closed as a documentation-only terminal blocker after parser artifacts were excluded; next ranked remaining domain selected",
        dependency="RE-253..RE-260 inventory epic",
        code_change_readiness="blocked",
        stop_condition="input proof-first audit emitted",
    )
    return InventoryEpic(
        story_range="RE-253..RE-260",
        upstream_ticket="RE-252",
        domain_id="inventory",
        selected_pivot="S_CallInventory2",
        raw_priority_count=len(rows) + len(artifacts),
        parser_artifact_count=len(artifacts),
        candidate_count=len(rows),
        closed_candidate_count=len(rows),
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
        next_domain_rows=next_rows,
        handoff=handoff,
    )


def write_csv(path: Path, rows: tuple[object, ...]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        if not rows:
            raise ValueError(f"no rows for {path}")
        writer = csv.DictWriter(
            f,
            fieldnames=[field.name for field in fields(rows[0])],
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
    return path


def write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def render_md(epic: InventoryEpic) -> str:
    lines = [
        "# RE-253..RE-260 inventory epic",
        "",
        "Domain: `inventory`",
        "Pivot: `S_CallInventory2`",
        "Outcome: `documentation-only-terminal-blocker`",
        f"Blocker: `{epic.blocker}`",
        f"Raw priority rows: `{epic.raw_priority_count}`",
        f"Parser artifacts excluded: `{epic.parser_artifact_count}`",
        f"Candidates closed/documented: `{epic.closed_candidate_count}` / `{epic.candidate_count}`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-252 handoff consumed.",
        "- [x] Proof-first audit emitted.",
        "- [x] Parser artifacts excluded before function-scope closure.",
        "- [x] Menu-flow, object-list, and requester-service subclusters documented.",
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
        "This is a documentation-only terminal blocker for inventory. No production source or marker change is authorized.",
        "",
        "## Next domain",
        "",
        "Next proof domain: `input`",
        "Selected pivot: `S_UpdateInput`",
        "Recommended next ticket: `RE-261`",
        "",
    ])
    return "\n".join(lines)


def render_story_index(epic: InventoryEpic) -> str:
    return "\n".join([
        "# RE-253..RE-260 inventory epic",
        "",
        "## Progress tracker",
        "",
        "- [x] Upstream handoff validated.",
        "- [x] Inventory scope generated.",
        "- [x] Parser artifacts reconciled.",
        "- [x] Source patch gate denied.",
        "- [x] Next domain selected.",
        "",
        f"Readiness: `{epic.domain_outcome}`",
        "No production source or marker change is authorized.",
        "",
    ])


def render_story(row: StoryRow) -> str:
    return "\n".join([
        f"# {row.story_id} {row.topic}",
        "",
        "## Progress tracker",
        "",
        "- [x] Inputs consumed.",
        "- [x] Metadata-only artifact generated.",
        "- [x] Readiness recorded.",
        "",
        f"Scope: `{row.scope}`",
        f"Readiness: `{row.readiness}`",
        f"Source patch ready: `{row.source_patch_ready}`",
        f"Marker ready: `{row.marker_ready}`",
        f"Blocker: `{row.blocker}`",
        f"Artifact: `{row.artifact}`",
        "",
        "No production source or marker change is authorized.",
        "",
    ])


def assert_metadata_only(paths: list[Path]) -> None:
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN + STALE_FRAGMENTS:
            if fragment in text:
                raise ValueError(f"forbidden or stale fragment {fragment!r} in {path}")


def write_all_artifacts(epic: InventoryEpic, repo: Path) -> dict[str, object]:
    written: dict[str, object] = {}
    written["audit_csv"] = write_csv(repo / AUDIT_CSV, epic.audit_rows)
    written["subclusters_csv"] = write_csv(repo / SUBCLUSTERS_CSV, epic.subcluster_rows)
    written["parser_artifacts_csv"] = write_csv(repo / PARSER_ARTIFACTS_CSV, epic.parser_artifact_rows)
    written["epic_csv"] = write_csv(repo / EPIC_CSV, epic.story_rows)
    written["gate_csv"] = write_csv(repo / GATE_CSV, epic.gate_rows)
    written["next_selection_csv"] = write_csv(repo / NEXT_SELECTION_CSV, epic.next_domain_rows)
    written["handoff_csv"] = write_csv(repo / HANDOFF_CSV, (epic.handoff,))
    written["md"] = write_text(repo / MD_OUTPUT, render_md(epic))
    written["story_index"] = write_text(repo / STORY_INDEX, render_story_index(epic))
    story_paths: dict[str, Path] = {}
    for row in epic.story_rows:
        story_paths[row.story_id] = write_text(repo / f"docs/stories/{row.story_id}-{row.topic}.md", render_story(row))
    written["stories"] = story_paths
    all_paths = [p for key, value in written.items() if key != "stories" for p in [value]] + list(story_paths.values())
    assert_metadata_only(all_paths)
    return written


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    epic = build_epic(args.repo)
    write_all_artifacts(epic, args.repo)


if __name__ == "__main__":
    main()
