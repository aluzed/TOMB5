#!/usr/bin/env python3
"""Generate RE-288..RE-290 global function-priority exhaustion artifacts."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import asdict, dataclass, fields
from pathlib import Path

UPSTREAM_HANDOFF = "docs/reverse/generated/re287-post-module-spec-pc-n-handoff.csv"
FUNCTION_PRIORITY = "docs/reverse/generated/function-priority.csv"

DOMAINS_CSV = "docs/reverse/generated/re288-global-function-priority-exhaustion.csv"
PARSER_CSV = "docs/reverse/generated/re289-global-parser-artifacts.csv"
EPIC_CSV = "docs/reverse/generated/re288-re290-global-exhaustion-epic.csv"
HANDOFF_CSV = "docs/reverse/generated/re290-final-function-priority-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re288-re290-global-function-priority-exhaustion.md"
STORY_INDEX = "docs/stories/RE-288-RE-290-global-function-priority-exhaustion.md"

FORBIDDEN = (
    "word_le_hex", "payload_offset", "dump row", "opcode", "machine word",
    "call_address", "branch target", "call target", "0x800",
)
STALE_FRAGMENTS = (
    "open re-276", "calc animatingitem", "selected domain: `module-spec_pc_n`",
    "next topic: `post-animation-items-domain-selection-needed`",
)
KEYWORDS = {"if", "for", "while", "switch"}

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
EXPECTED_ORDER = (
    "maths-render-support",
    "module-game",
    "collision",
    "animation-items",
    "module-spec_psxpc",
    "module-spec_psxpc_n",
    "traps-switches-doors",
    "audio-effects",
    "module-spec_psx",
    "inventory",
    "lara-combat",
    "camera",
    "savegame",
    "input",
    "module-spec_pc_n",
)


@dataclass(frozen=True)
class DomainRow:
    rank: int
    domain_id: str
    priority_count: int
    parser_artifact_count: int
    remaining_candidates: int
    status: str
    closure_reference: str


@dataclass(frozen=True)
class ParserArtifactRow:
    rank: int
    domain_id: str
    function: str
    file: str
    line: int
    classification: str
    disposition: str


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
class GlobalExhaustionEpic:
    story_range: str
    upstream_ticket: str
    total_priority_rows: int
    closed_domain_count: int
    remaining_domain_count: int
    remaining_candidate_count: int
    parser_artifact_count: int
    code_change_ready_count: int
    marker_ready_count: int
    outcome: str
    domain_rows: tuple[DomainRow, ...]
    parser_rows: tuple[ParserArtifactRow, ...]
    story_rows: tuple[StoryRow, ...]
    handoff: HandoffRow


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_int(value: str | None) -> int:
    return int(value or 0)


def classify_domain(row: dict[str, str]) -> str:
    if row.get("file") == "GAME/SAVEGAME.C":
        return "savegame"
    haystack = f"{row.get('file', '')} {row.get('repo_function', '')}".upper()
    for domain_id, terms in DOMAIN_RULES:
        if any(term in haystack for term in terms):
            return domain_id
    return "module-" + (row.get("file") or "unknown").split("/", 1)[0].lower()


def validate_upstream(repo: Path) -> None:
    rows = read_csv(repo / UPSTREAM_HANDOFF)
    if len(rows) != 1:
        raise ValueError("RE-287 handoff must contain exactly one row")
    expected = {
        "next_ticket": "TBD",
        "next_topic": "post-animation-items-domain-backlog-exhausted",
        "selected_domain": "none",
        "selected_pivot": "none",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if rows[0].get(key) != value:
            raise ValueError(f"RE-287 handoff drift: {key}={rows[0].get(key)!r}")


def closure_reference(domain_id: str) -> str:
    references = {
        "savegame": "RE-001..RE-043 savegame closure chain",
        "audio-effects": "RE-045..RE-052 audio-effects chain",
        "collision": "RE-053..RE-060 collision chain",
        "module-game": "RE-061..RE-161 module-game chain",
        "module-spec_psxpc_n": "RE-163..RE-212 module-spec_psxpc_n chain",
        "maths-render-support": "RE-214..RE-221 maths-render-support epic",
        "traps-switches-doors": "RE-222..RE-228 traps-switches-doors epic",
        "module-spec_psxpc": "RE-229..RE-236 module-spec_psxpc epic",
        "module-spec_psx": "RE-237..RE-244 module-spec_psx epic",
        "lara-combat": "RE-245..RE-252 lara-combat epic",
        "inventory": "RE-253..RE-260 inventory epic",
        "input": "RE-261..RE-267 input epic",
        "camera": "RE-268..RE-274 camera epic",
        "animation-items": "RE-275..RE-282 animation-items epic",
        "module-spec_pc_n": "RE-283..RE-287 module-spec_pc_n epic",
    }
    return references[domain_id]


def build_epic(repo: Path) -> GlobalExhaustionEpic:
    repo = Path(repo)
    validate_upstream(repo)
    rows = read_csv(repo / FUNCTION_PRIORITY)
    counts = Counter(classify_domain(row) for row in rows)
    parser_counts = Counter(classify_domain(row) for row in rows if row.get("repo_function") in KEYWORDS)
    observed_order = tuple(domain for domain, _ in sorted(counts.items(), key=lambda item: (-item[1], EXPECTED_ORDER.index(item[0]) if item[0] in EXPECTED_ORDER else 99)))
    if observed_order != EXPECTED_ORDER:
        raise ValueError(f"global domain scope drifted: {observed_order!r}")
    domain_rows = tuple(
        DomainRow(
            rank=index,
            domain_id=domain,
            priority_count=counts[domain],
            parser_artifact_count=parser_counts[domain],
            remaining_candidates=0,
            status="closed-or-proof-blocked",
            closure_reference=closure_reference(domain),
        )
        for index, domain in enumerate(EXPECTED_ORDER, 1)
    )
    parser_rows = tuple(
        ParserArtifactRow(
            rank=index,
            domain_id=classify_domain(row),
            function=row["repo_function"],
            file=row["file"],
            line=parse_int(row.get("line")),
            classification="parser-artifact",
            disposition="excluded-from-source-patch-scopes",
        )
        for index, row in enumerate((row for row in rows if row.get("repo_function") in KEYWORDS), 1)
    )
    if len(rows) != 348 or len(domain_rows) != 15 or len(parser_rows) != 16:
        raise ValueError("function-priority exhaustion counts drifted")
    story_rows = (
        StoryRow("RE-288", "global-function-priority-exhaustion-audit", "all function-priority rows and closed domains", 348, "blocked", "no", "no", "function-priority-backlog-exhausted", DOMAINS_CSV),
        StoryRow("RE-289", "global-parser-artifact-reconciliation", "all parser-artifact keyword rows across closed scopes", 16, "blocked", "no", "no", "function-priority-backlog-exhausted", PARSER_CSV),
        StoryRow("RE-290", "final-function-priority-handoff", "remaining candidate rows after all known closures", 0, "blocked", "no", "no", "function-priority-backlog-exhausted", HANDOFF_CSV),
    )
    handoff = HandoffRow(
        next_ticket="TBD",
        next_topic="function-priority-backlog-exhausted",
        selected_domain="none",
        selected_pivot="none",
        outcome="all-ranked-function-priority-domains-closed-or-proof-blocked",
        reason="all 348 function-priority rows are covered by closed or proof-blocked RE chains; no remaining ranked domain candidate exists",
        dependency="RE-288..RE-290 global function-priority exhaustion epic",
        code_change_readiness="blocked",
        stop_condition="refresh upstream function-priority inputs or add new non-raw proof evidence before opening another epic",
    )
    return GlobalExhaustionEpic(
        story_range="RE-288..RE-290",
        upstream_ticket="RE-287",
        total_priority_rows=len(rows),
        closed_domain_count=len(domain_rows),
        remaining_domain_count=0,
        remaining_candidate_count=sum(row.remaining_candidates for row in domain_rows),
        parser_artifact_count=len(parser_rows),
        code_change_ready_count=0,
        marker_ready_count=0,
        outcome="function-priority-backlog-exhausted",
        domain_rows=domain_rows,
        parser_rows=parser_rows,
        story_rows=story_rows,
        handoff=handoff,
    )


def write_rows(path: Path, rows: tuple[object, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    row_fields = [field.name for field in fields(rows[0])]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row_fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_markdown(path: Path, epic: GlobalExhaustionEpic) -> None:
    lines = [
        "# RE-288..RE-290 global function-priority exhaustion epic",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-287 final domain handoff consumed.",
        "- [x] All function-priority rows classified into closed or proof-blocked domains.",
        "- [x] Parser-artifact keyword rows reconciled globally.",
        "- [x] Final no-next-domain handoff emitted.",
        "",
        "## Decision",
        "",
        f"- Total priority rows: `{epic.total_priority_rows}`",
        f"- Closed/proof-blocked domains: `{epic.closed_domain_count}`",
        f"- Parser artifacts reconciled: `{epic.parser_artifact_count}`",
        f"- Remaining candidate rows: `{epic.remaining_candidate_count}`",
        f"- Outcome: `{epic.outcome}`",
        f"- Recommended next ticket: `{epic.handoff.next_ticket}`",
        "",
        "No production source or marker change is authorized by this epic.",
        "",
        "## Domain coverage",
        "",
    ]
    for row in epic.domain_rows:
        lines.append(f"- `{row.domain_id}`: {row.priority_count} rows; status `{row.status}`; remaining `{row.remaining_candidates}`.")
    lines.extend(["", "## Handoff", "", f"- Next topic: `{epic.handoff.next_topic}`", f"- Stop condition: `{epic.handoff.stop_condition}`", ""])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def story_text(row: StoryRow, epic: GlobalExhaustionEpic) -> str:
    return "\n".join([
        f"# {row.story_id} — {row.topic}",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        f"Advance `{row.topic}` for the final function-priority backlog without source or marker changes.",
        "",
        "## Progress tracker",
        "",
        "- [x] Upstream handoff consumed.",
        "- [x] Metadata-only function-priority rows reviewed.",
        "- [x] Generated artifacts emitted.",
        "- [x] Readiness and blocker state recorded.",
        "",
        "## Scope",
        "",
        f"- Scope: `{row.scope}`",
        f"- Candidate count: `{row.candidate_count}`",
        f"- Artifact: `{row.artifact}`",
        "",
        "## Readiness",
        "",
        f"- Readiness: `{row.readiness}`",
        f"- Source patch ready: `{row.source_patch_ready}`",
        f"- Marker ready: `{row.marker_ready}`",
        f"- Blocker: `{row.blocker}`",
        "",
        "No production source or marker change is authorized by this story.",
        "",
    ])


def write_stories(base: Path, epic: GlobalExhaustionEpic) -> dict[str, Path]:
    out: dict[str, Path] = {}
    for row in epic.story_rows:
        path = base / f"docs/stories/{row.story_id}-{row.topic}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(story_text(row, epic), encoding="utf-8")
        out[row.story_id] = path
    return out


def write_story_index(path: Path, epic: GlobalExhaustionEpic) -> None:
    lines = [
        "# RE-288..RE-290 global function-priority exhaustion epic",
        "",
        "Status: Done",
        "",
        "## Progress tracker",
        "",
        "- [x] Final domain handoff consumed.",
        "- [x] Domain coverage matrix emitted.",
        "- [x] Parser-artifact matrix emitted.",
        "- [x] Backlog exhaustion handoff emitted.",
        "",
        "## Stories",
        "",
    ]
    for row in epic.story_rows:
        lines.append(f"- `{row.story_id}` — `{row.topic}`: Readiness: `{row.readiness}`; candidates `{row.candidate_count}`.")
    lines.extend(["", "No production source or marker change is authorized by this epic.", ""])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_all_artifacts(epic: GlobalExhaustionEpic, base: Path) -> dict[str, object]:
    base = Path(base)
    paths = {
        "domains_csv": base / DOMAINS_CSV,
        "parser_csv": base / PARSER_CSV,
        "epic_csv": base / EPIC_CSV,
        "handoff_csv": base / HANDOFF_CSV,
        "md": base / MD_OUTPUT,
        "story_index": base / STORY_INDEX,
    }
    write_rows(paths["domains_csv"], epic.domain_rows)
    write_rows(paths["parser_csv"], epic.parser_rows)
    write_rows(paths["epic_csv"], epic.story_rows)
    write_rows(paths["handoff_csv"], (epic.handoff,))
    write_markdown(paths["md"], epic)
    write_story_index(paths["story_index"], epic)
    paths["stories"] = write_stories(base, epic)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    epic = build_epic(repo)
    write_all_artifacts(epic, repo)


if __name__ == "__main__":
    main()
