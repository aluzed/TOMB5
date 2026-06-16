#!/usr/bin/env python3
"""Generate RE-268..RE-274 camera epic artifacts."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import asdict, dataclass, fields
from pathlib import Path

UPSTREAM_HANDOFF = "docs/reverse/generated/re267-post-input-handoff.csv"
UPSTREAM_SELECTION = "docs/reverse/generated/re267-post-input-domain-selection.csv"
FUNCTION_PRIORITY = "docs/reverse/generated/function-priority.csv"

AUDIT_CSV = "docs/reverse/generated/re268-camera-proof-first-audit.csv"
SUBCLUSTERS_CSV = "docs/reverse/generated/re268-camera-subclusters.csv"
EPIC_CSV = "docs/reverse/generated/re268-re274-camera-epic.csv"
GATE_CSV = "docs/reverse/generated/re273-camera-source-patch-gates.csv"
EXHAUSTION_CSV = "docs/reverse/generated/re274-post-camera-domain-exhaustion.csv"
HANDOFF_CSV = "docs/reverse/generated/re274-post-camera-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re268-re274-camera-epic.md"
STORY_INDEX = "docs/stories/RE-268-RE-274-camera-epic.md"

FORBIDDEN = (
    "word_le_hex", "payload_offset", "dump row", "opcode", "machine word",
    "call_address", "branch target", "call target", "0x800",
)
STALE_FRAGMENTS = (
    "input closed", "post-input", "s_updateinput", "open re-268 camera proof-first audit", "inventory",
)
BLOCKER = "missing-camera-state-contract-and-non-raw-equivalence-proof"

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
CLOSED_DOMAINS = {"camera"}


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
class ExhaustionRow:
    next_ticket: str
    remaining_domain_count: int
    status: str
    reason: str
    dependency: str


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
class CameraEpic:
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
    subcluster_rows: tuple[SubclusterRow, ...]
    story_rows: tuple[StoryRow, ...]
    gate_rows: tuple[GateRow, ...]
    exhaustion: ExhaustionRow
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
    if function == "CalculateSpotCams":
        return "spotcam"
    if function in {"CalculateCamera", "CombatCamera"}:
        return "camera-core"
    if function == "mgLOS":
        return "line-of-sight"
    raise ValueError(f"unclassified camera row: {function} {row.get('file', '')}")


def validate_upstream(repo: Path) -> None:
    handoff = read_csv(repo / UPSTREAM_HANDOFF)
    if len(handoff) != 1:
        raise ValueError("RE-267 handoff must contain exactly one row")
    expected = {
        "next_ticket": "RE-268",
        "next_topic": "camera-proof-first-audit",
        "selected_domain": "camera",
        "selected_pivot": "CalculateSpotCams",
    }
    for key, value in expected.items():
        if handoff[0].get(key) != value:
            raise ValueError(f"RE-267 handoff drift: {key}={handoff[0].get(key)!r}")
    selection = read_csv(repo / UPSTREAM_SELECTION)
    if not selection or selection[0].get("domain_id") != "camera":
        raise ValueError("RE-267 selection must rank camera first")
    if selection[0].get("top_function") != "CalculateSpotCams" or parse_int(selection[0].get("candidate_count")) != 4:
        raise ValueError("RE-267 selected camera scope drifted")


def camera_priority_rows(repo: Path) -> list[dict[str, str]]:
    rows = [row for row in read_csv(repo / FUNCTION_PRIORITY) if classify_domain(row) == "camera"]
    expected = ["CalculateSpotCams", "CalculateCamera", "CombatCamera", "mgLOS"]
    observed = [row["repo_function"] for row in rows]
    if observed != expected:
        raise ValueError(f"camera scope drifted: {observed!r}")
    return rows


def build_epic(repo: Path) -> CameraEpic:
    validate_upstream(repo)
    rows = camera_priority_rows(repo)
    audit_rows = tuple(
        AuditRow(
            rank=i,
            domain_id="camera",
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
    grouped: dict[str, list[AuditRow]] = defaultdict(list)
    for row in audit_rows:
        grouped[row.subcluster].append(row)
    order = ["spotcam", "camera-core", "line-of-sight"]
    story_for = {"spotcam": "RE-269", "camera-core": "RE-270", "line-of-sight": "RE-271"}
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
        StoryRow("RE-268", "camera-proof-first-audit", "camera domain scope from RE-267 handoff", 4, "blocked", "no", "no", BLOCKER, AUDIT_CSV),
        StoryRow("RE-269", "camera-spotcam-chain", "CalculateSpotCams", 1, "blocked", "no", "no", BLOCKER, SUBCLUSTERS_CSV),
        StoryRow("RE-270", "camera-core-chain", "CalculateCamera, CombatCamera", 2, "blocked", "no", "no", BLOCKER, SUBCLUSTERS_CSV),
        StoryRow("RE-271", "camera-line-of-sight-chain", "mgLOS", 1, "blocked", "no", "no", BLOCKER, SUBCLUSTERS_CSV),
        StoryRow("RE-272", "camera-state-equivalence-gate", "camera state/equivalence proof", 4, "blocked", "no", "no", BLOCKER, GATE_CSV),
        StoryRow("RE-273", "camera-source-patch-gate", "source patch and marker readiness", 4, "blocked", "no", "no", BLOCKER, GATE_CSV),
        StoryRow("RE-274", "post-camera-domain-exhaustion", "remaining ranked domains after camera closure", 0, "blocked", "no", "no", BLOCKER, EXHAUSTION_CSV),
    )
    gate_rows = (
        GateRow("equivalence", "RE-272", "all camera candidates", 0, len(audit_rows), "deny", BLOCKER),
        GateRow("source-patch", "RE-273", "all camera candidates", 0, len(audit_rows), "deny", BLOCKER),
        GateRow("marker", "RE-273", "all camera candidates", 0, len(audit_rows), "deny", BLOCKER),
    )
    exhaustion = ExhaustionRow(
        next_ticket="TBD",
        remaining_domain_count=0,
        status="exhausted",
        reason="RE-267 ranked selection contained only camera; camera closed with no remaining ranked domain rows",
        dependency="RE-268..RE-274 camera epic",
    )
    handoff = HandoffRow(
        next_ticket="TBD",
        next_topic="post-re267-domain-backlog-exhausted",
        selected_domain="none",
        selected_pivot="none",
        outcome="camera-closed-domain-backlog-exhausted",
        reason=exhaustion.reason,
        dependency="RE-268..RE-274 camera epic",
        code_change_readiness="blocked",
        stop_condition="no ranked remaining domain in RE-267 selection",
    )
    return CameraEpic(
        story_range="RE-268..RE-274",
        upstream_ticket="RE-267",
        domain_id="camera",
        selected_pivot="CalculateSpotCams",
        raw_priority_count=len(rows),
        parser_artifact_count=0,
        candidate_count=len(rows),
        closed_candidate_count=len(rows),
        runtime_count=sum(1 for row in audit_rows if row.runtime_focus == "yes"),
        nd_count=sum(1 for row in audit_rows if row.nd == "yes"),
        code_change_ready_count=0,
        marker_ready_count=0,
        domain_outcome="documentation-only-terminal-blocker",
        blocker=BLOCKER,
        audit_rows=audit_rows,
        subcluster_rows=subcluster_rows,
        story_rows=story_rows,
        gate_rows=gate_rows,
        exhaustion=exhaustion,
        handoff=handoff,
    )


def write_csv(path: Path, rows: tuple[object, ...]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        if not rows:
            raise ValueError(f"no rows for {path}")
        writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(rows[0])], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
    return path


def write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def render_md(epic: CameraEpic) -> str:
    lines = [
        "# RE-268..RE-274 camera epic",
        "", "Domain: `camera`", "Pivot: `CalculateSpotCams`",
        "Outcome: `documentation-only-terminal-blocker`", f"Blocker: `{epic.blocker}`",
        f"Raw priority rows: `{epic.raw_priority_count}`", f"Remaining domains: `{epic.exhaustion.remaining_domain_count}`",
        f"Candidates closed/documented: `{epic.closed_candidate_count}` / `{epic.candidate_count}`",
        "", "## Progress tracker", "",
        "- [x] RE-267 handoff consumed.",
        "- [x] Proof-first audit emitted.",
        "- [x] Spotcam, camera-core, and line-of-sight subclusters documented.",
        "- [x] State/equivalence and patch gates denied with zero ready rows.",
        "- [x] Ranked domain backlog exhaustion recorded.",
        "", "## Subcluster closures", "",
    ]
    for row in epic.subcluster_rows:
        lines.append(f"- `{row.closed_by_story}` `{row.subcluster}`: {row.candidate_count} candidate(s), top `{row.top_function}`, outcome `{row.outcome}`.")
    lines.extend([
        "", "## Terminal decision", "",
        "This is a documentation-only terminal blocker for camera. No production source or marker change is authorized.",
        "", "## Next domain", "",
        "Next proof domain: `none`",
        "Selected pivot: `none`",
        "Recommended next ticket: `TBD`",
        "",
    ])
    return "\n".join(lines)


def render_story_index(epic: CameraEpic) -> str:
    return "\n".join([
        "# RE-268..RE-274 camera epic", "", "## Progress tracker", "",
        "- [x] Upstream handoff validated.",
        "- [x] Camera scope generated.",
        "- [x] Source patch gate denied.",
        "- [x] Ranked domain backlog exhaustion recorded.", "",
        f"Readiness: `{epic.domain_outcome}`",
        "No production source or marker change is authorized.", "",
    ])


def render_story(row: StoryRow) -> str:
    return "\n".join([
        f"# {row.story_id} {row.topic}", "", "## Progress tracker", "",
        "- [x] Inputs consumed.", "- [x] Metadata-only artifact generated.", "- [x] Readiness recorded.", "",
        f"Scope: `{row.scope}`", f"Readiness: `{row.readiness}`", f"Source patch ready: `{row.source_patch_ready}`",
        f"Marker ready: `{row.marker_ready}`", f"Blocker: `{row.blocker}`", f"Artifact: `{row.artifact}`", "",
        "No production source or marker change is authorized.", "",
    ])


def assert_metadata_only(paths: list[Path]) -> None:
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN + STALE_FRAGMENTS:
            if fragment in text:
                raise ValueError(f"forbidden or stale fragment {fragment!r} in {path}")


def write_all_artifacts(epic: CameraEpic, repo: Path) -> dict[str, object]:
    written: dict[str, object] = {}
    written["audit_csv"] = write_csv(repo / AUDIT_CSV, epic.audit_rows)
    written["subclusters_csv"] = write_csv(repo / SUBCLUSTERS_CSV, epic.subcluster_rows)
    written["epic_csv"] = write_csv(repo / EPIC_CSV, epic.story_rows)
    written["gate_csv"] = write_csv(repo / GATE_CSV, epic.gate_rows)
    written["exhaustion_csv"] = write_csv(repo / EXHAUSTION_CSV, (epic.exhaustion,))
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
    write_all_artifacts(build_epic(args.repo), args.repo)


if __name__ == "__main__":
    main()
