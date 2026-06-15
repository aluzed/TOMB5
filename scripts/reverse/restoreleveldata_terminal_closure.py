#!/usr/bin/env python3
"""Build RE-038..RE-043 terminal RestoreLevelData closure artifacts.

This is the stop report for the current RestoreLevelData proof chain. It does
not attempt a source patch: RE-031..RE-037 established that no target group has
code-change-ready evidence under the metadata-only safety rules.
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_OUT_CSV = "docs/reverse/generated/restoreleveldata-terminal-closure-re038-re043.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/restoreleveldata-terminal-closure-re038-re043.md"
STORY_DIR = "docs/stories"
PROGRESS = (
    "input-artifacts-loaded",
    "terminal-decision-published",
    "source-patch-rejected-or-deferred",
    "forbidden-raw-evidence-excluded",
)
SAFETY_CONTRACT = "metadata-only; symbolic blocker labels only; no opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records"


@dataclass(frozen=True)
class TerminalClosureTicket:
    story_id: str
    title: str
    topic: str
    depends_on: tuple[str, ...]
    target_save_groups: tuple[int, ...]
    blockers: tuple[str, ...]
    decision: str
    safe_next_action: str
    code_change_readiness: str
    next_ticket: str
    status: str
    progress: tuple[str, ...]
    safety_contract: str


@dataclass(frozen=True)
class TerminalClosure:
    tickets: tuple[TerminalClosureTicket, ...]
    status: str
    final_decision: str
    code_change_ready_count: int
    next_ticket: str


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _split(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.split(";") if part.strip())


def build_restoreleveldata_terminal_closure(repo: Path = ROOT) -> TerminalClosure:
    backlog_rows = {row["story_id"]: row for row in _read_csv(repo / "docs/reverse/generated/restoreleveldata-reconstruction-backlog-re031-re037.csv")}

    tickets = (
        TerminalClosureTicket(
            story_id="RE-038",
            title="RestoreLevelData source patch gate",
            topic="source-patch-gate",
            depends_on=("RE-037",),
            target_save_groups=(4, 5, 8, 10),
            blockers=("zero code-change-ready rows", "all candidate patch scopes remain blocked"),
            decision="source-patch-denied-no-ready-rows",
            safe_next_action="do not create a RestoreLevelData source patch from the current proof set",
            code_change_readiness="blocked",
            next_ticket="RE-039",
            status="Done",
            progress=PROGRESS,
            safety_contract=SAFETY_CONTRACT,
        ),
        TerminalClosureTicket(
            story_id="RE-039",
            title="RestoreLevelData group 10 terminal blocker",
            topic="group10-terminal-blocker",
            depends_on=("RE-032", "RE-038"),
            target_save_groups=(10,),
            blockers=_split(backlog_rows["RE-032"]["blockers"]),
            decision="terminal-blocked-without-new-non-raw-evidence",
            safe_next_action="pause group 10 until a new metadata-only room placement proof exists",
            code_change_readiness="blocked",
            next_ticket="RE-040",
            status="Done",
            progress=PROGRESS,
            safety_contract=SAFETY_CONTRACT,
        ),
        TerminalClosureTicket(
            story_id="RE-040",
            title="RestoreLevelData group 4 terminal blocker",
            topic="group4-terminal-blocker",
            depends_on=("RE-033", "RE-038"),
            target_save_groups=(4,),
            blockers=_split(backlog_rows["RE-033"]["blockers"]),
            decision="terminal-blocked-without-new-non-raw-evidence",
            safe_next_action="pause group 4 until split active-item and anim width proofs exist",
            code_change_readiness="blocked",
            next_ticket="RE-041",
            status="Done",
            progress=PROGRESS,
            safety_contract=SAFETY_CONTRACT,
        ),
        TerminalClosureTicket(
            story_id="RE-041",
            title="RestoreLevelData group 5 terminal blocker",
            topic="group5-terminal-blocker",
            depends_on=("RE-035", "RE-038"),
            target_save_groups=(5,),
            blockers=_split(backlog_rows["RE-035"]["blockers"]),
            decision="terminal-excluded-no-assignment-identities",
            safe_next_action="keep group 5 excluded unless future evidence names restore assignments safely",
            code_change_readiness="blocked",
            next_ticket="RE-042",
            status="Done",
            progress=PROGRESS,
            safety_contract=SAFETY_CONTRACT,
        ),
        TerminalClosureTicket(
            story_id="RE-042",
            title="RestoreLevelData group 8 terminal blocker",
            topic="group8-terminal-blocker",
            depends_on=("RE-036", "RE-038", "RE-041"),
            target_save_groups=(8,),
            blockers=_split(backlog_rows["RE-036"]["blockers"]),
            decision="terminal-blocked-by-layout-and-group5-dependency",
            safe_next_action="pause group 8 until subtype/layout proofs and group 5 dependency are safe",
            code_change_readiness="blocked",
            next_ticket="RE-043",
            status="Done",
            progress=PROGRESS,
            safety_contract=SAFETY_CONTRACT,
        ),
        TerminalClosureTicket(
            story_id="RE-043",
            title="RestoreLevelData final stop report",
            topic="restoreleveldata-final-stop-report",
            depends_on=("RE-038", "RE-039", "RE-040", "RE-041", "RE-042"),
            target_save_groups=(4, 5, 8, 10),
            blockers=("no safe source patch target remains", "future work requires new non-raw evidence outside the current chain"),
            decision="no-safe-remaining-restoreleveldata-source-work",
            safe_next_action="stop this RestoreLevelData reconstruction chain and switch domains or obtain new safe evidence",
            code_change_readiness="blocked",
            next_ticket="none",
            status="Done",
            progress=PROGRESS,
            safety_contract=SAFETY_CONTRACT,
        ),
    )
    ready = sum(1 for ticket in tickets if ticket.code_change_readiness == "ready")
    return TerminalClosure(
        tickets=tickets,
        status="restoreleveldata-terminal-closure-no-safe-source-patch",
        final_decision="stop-restoreleveldata-source-reconstruction-chain",
        code_change_ready_count=ready,
        next_ticket="none",
    )


def write_csv(closure: TerminalClosure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "story_id",
        "topic",
        "title",
        "depends_on",
        "target_save_groups",
        "blockers",
        "decision",
        "safe_next_action",
        "code_change_readiness",
        "next_ticket",
        "status",
        "safety_contract",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for ticket in closure.tickets:
            writer.writerow({
                "story_id": ticket.story_id,
                "topic": ticket.topic,
                "title": ticket.title,
                "depends_on": ";".join(ticket.depends_on),
                "target_save_groups": ";".join(str(group) for group in ticket.target_save_groups),
                "blockers": ";".join(ticket.blockers),
                "decision": ticket.decision,
                "safe_next_action": ticket.safe_next_action,
                "code_change_readiness": ticket.code_change_readiness,
                "next_ticket": ticket.next_ticket,
                "status": ticket.status,
                "safety_contract": ticket.safety_contract,
            })


def write_markdown(closure: TerminalClosure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RestoreLevelData terminal closure RE-038..RE-043",
        "",
        "Status: Generated",
        "Stories: `docs/stories/RE-038` through `docs/stories/RE-043`",
        "",
        "## Progress tracker",
        "",
        "- [x] Input artifacts loaded.",
        "- [x] Terminal decisions published.",
        "- [x] Source patch rejected/deferred.",
        "- [x] Forbidden raw evidence excluded.",
        "",
        "## Summary",
        "",
        f"- status: `{closure.status}`",
        f"- final decision: `{closure.final_decision}`",
        f"- tickets covered: `{len(closure.tickets)}`",
        f"- code-change-ready tickets: `{closure.code_change_ready_count}`",
        f"- next ticket: `{closure.next_ticket}`",
        "",
        "## Terminal matrix",
    ]
    for ticket in closure.tickets:
        lines.extend([
            "",
            f"### {ticket.story_id} — {ticket.title}",
            "",
            f"- topic: `{ticket.topic}`",
            f"- depends on: `{', '.join(ticket.depends_on)}`",
            f"- target save groups: `{', '.join(str(group) for group in ticket.target_save_groups)}`",
            f"- blockers: `{'; '.join(ticket.blockers)}`",
            f"- decision: `{ticket.decision}`",
            f"- safe next action: `{ticket.safe_next_action}`",
            f"- code change readiness: `{ticket.code_change_readiness}`",
            f"- next ticket: `{ticket.next_ticket}`",
        ])
    lines.extend([
        "",
        "## Verdict",
        "",
        "Do not patch `GAME/SAVEGAME.C` from the current RestoreLevelData chain. The chain is closed because every source-patch path is still blocked under the metadata-only safety contract.",
        "",
        "Recommended next ticket: none — resume only if new non-raw evidence becomes available, or switch to a different reverse-engineering domain.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _story_slug(ticket: TerminalClosureTicket) -> str:
    return ticket.topic.replace("_", "-")


def _write_story(ticket: TerminalClosureTicket, story_dir: Path) -> Path:
    story_dir.mkdir(parents=True, exist_ok=True)
    path = story_dir / f"{ticket.story_id}-{_story_slug(ticket)}.md"
    lines = [
        f"# {ticket.story_id} — {ticket.title}",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        f"Publish the terminal metadata-only decision for `{ticket.topic}`.",
        "",
        "## Scope",
        "",
        f"- depends on: `{', '.join(ticket.depends_on)}`",
        f"- target save groups: `{', '.join(str(group) for group in ticket.target_save_groups)}`",
        f"- safety contract: `{ticket.safety_contract}`",
        "",
        "## Progress",
        "",
        "- [x] Input artifacts loaded.",
        "- [x] Terminal decision published.",
        "- [x] Source patch rejected or deferred.",
        "- [x] Forbidden raw evidence excluded.",
        "",
        "## Findings",
        "",
    ]
    for blocker in ticket.blockers:
        lines.append(f"- blocker: `{blocker}`")
    lines.extend([
        "",
        "## Terminal decision",
        "",
        f"- decision: `{ticket.decision}`",
        f"- safe next action: `{ticket.safe_next_action}`",
        f"- code change readiness: `{ticket.code_change_readiness}`",
        "",
        "Do not patch `GAME/SAVEGAME.C` or add `(F)`, `(D)`, or `(**)` markers from this story.",
        "",
        "## Validation",
        "",
        "- `pytest tests/reverse/test_restoreleveldata_terminal_closure.py -q`",
        "- metadata-only guard over terminal closure outputs",
        "",
        "## Next step",
        "",
        f"{ticket.next_ticket}: {'no next RestoreLevelData ticket in this chain' if ticket.next_ticket == 'none' else 'continue terminal closure sequencing' }.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_all_artifacts(closure: TerminalClosure, base_dir: Path = ROOT) -> dict[str, object]:
    csv_path = base_dir / DEFAULT_OUT_CSV
    md_path = base_dir / DEFAULT_OUT_MD
    story_dir = base_dir / STORY_DIR
    write_csv(closure, csv_path)
    write_markdown(closure, md_path)
    story_paths = [_write_story(ticket, story_dir) for ticket in closure.tickets]
    return {"csv": csv_path, "md": md_path, "stories": story_paths}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    closure = build_restoreleveldata_terminal_closure(args.repo)
    write_all_artifacts(closure, args.repo)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
