#!/usr/bin/env python3
"""Build RE-031..RE-037 RestoreLevelData reconstruction backlog artifacts.

The tickets produced here deliberately remain metadata-only. They consolidate the
current RestoreLevelData blockers into a sequential proof backlog without
publishing raw binary evidence or claiming source patch readiness.
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

DEFAULT_OUT_CSV = "docs/reverse/generated/restoreleveldata-reconstruction-backlog-re031-re037.csv"
DEFAULT_OUT_MD = "docs/reverse/functions/restoreleveldata-reconstruction-backlog-re031-re037.md"
STORY_DIR = "docs/stories"
PROGRESS = (
    "input-artifacts-loaded",
    "metadata-only-decision-published",
    "source-patch-readiness-evaluated",
    "forbidden-raw-evidence-excluded",
)
SAFETY_CONTRACT = "metadata-only; no raw opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records"


@dataclass(frozen=True)
class ReconstructionBacklogTicket:
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
class ReconstructionBacklog:
    tickets: tuple[ReconstructionBacklogTicket, ...]
    status: str
    patch_scope_decision: str
    code_change_ready_count: int


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _split_blockers(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.split(";") if part.strip())


def build_restoreleveldata_reconstruction_backlog(repo: Path = ROOT) -> ReconstructionBacklog:
    readiness_rows = {int(row["save_original_group"]): row for row in _read_csv(repo / "docs/reverse/generated/restoreleveldata-readiness-refresh.csv")}
    group5_rows = _read_csv(repo / "docs/reverse/generated/restoreleveldata-group5-restore-assignment-identity-map.csv")
    group8_rows = _read_csv(repo / "docs/reverse/generated/restoreleveldata-group8-layout-fanout-proof.csv")

    group5_blockers = tuple(row["required_assignment_evidence"] for row in group5_rows)
    group8_blockers = tuple(row["fanout_family"].replace("-", " ") for row in group8_rows)

    tickets = (
        ReconstructionBacklogTicket(
            story_id="RE-031",
            title="Limited RestoreLevelData reconstruction scope",
            topic="limited-restoreleveldata-reconstruction-scope",
            depends_on=("RE-027", "RE-030"),
            target_save_groups=(4, 5, 8, 10),
            blockers=tuple(readiness_rows[group]["remaining_blockers"] for group in (4, 5, 8, 10)),
            decision="exclude-blocked-groups-from-source-scope",
            safe_next_action="publish explicit ready/blocked/excluded scope before any source patch",
            code_change_readiness="blocked",
            next_ticket="RE-032",
            status="Done",
            progress=PROGRESS,
            safety_contract=SAFETY_CONTRACT,
        ),
        ReconstructionBacklogTicket(
            story_id="RE-032",
            title="RestoreLevelData group 10 room byte order/layout predicate",
            topic="group10-room-byte-order-layout-predicate",
            depends_on=("RE-024", "RE-027", "RE-031"),
            target_save_groups=(10,),
            blockers=_split_blockers(readiness_rows[10]["remaining_blockers"]),
            decision="group10-remains-blocked-until-room-placement-proof",
            safe_next_action="prove room byte placement/order as metadata-only rows before source reconstruction",
            code_change_readiness="blocked",
            next_ticket="RE-033",
            status="Done",
            progress=PROGRESS,
            safety_contract=SAFETY_CONTRACT,
        ),
        ReconstructionBacklogTicket(
            story_id="RE-033",
            title="RestoreLevelData group 4 active-item split restore predicates",
            topic="group4-active-item-split-restore-predicates",
            depends_on=("RE-024", "RE-027", "RE-031"),
            target_save_groups=(4,),
            blockers=_split_blockers(readiness_rows[4]["remaining_blockers"]),
            decision="group4-remains-blocked-by-split-and-width-predicate",
            safe_next_action="prove active-item split restore groups and anim-state width before source reconstruction",
            code_change_readiness="blocked",
            next_ticket="RE-034",
            status="Done",
            progress=PROGRESS,
            safety_contract=SAFETY_CONTRACT,
        ),
        ReconstructionBacklogTicket(
            story_id="RE-034",
            title="Non-raw RestoreLevelData assignment identity method",
            topic="non-raw-restore-assignment-identity-method",
            depends_on=("RE-030", "RE-031"),
            target_save_groups=(5,),
            blockers=("restore target names absent", "source restore body unavailable", "raw-evidence publication forbidden"),
            decision="method-defined-but-no-identities-recovered",
            safe_next_action="allow only symbolic field names, counts, statuses, and dependency labels in assignment proofs",
            code_change_readiness="blocked",
            next_ticket="RE-035",
            status="Done",
            progress=PROGRESS,
            safety_contract=SAFETY_CONTRACT,
        ),
        ReconstructionBacklogTicket(
            story_id="RE-035",
            title="RestoreLevelData group 5 safe assignment identity retry",
            topic="group5-safe-assignment-identity-retry",
            depends_on=("RE-028", "RE-029", "RE-030", "RE-034"),
            target_save_groups=(5,),
            blockers=(
                "packed-status-flags assignment identity",
                "item_flags[0..3] assignment identity and body order",
                "timer assignment identity",
                "trigger_flags assignment identity",
                "object-extension target fields and assignment order",
            ),
            decision="group5-still-excluded-from-source-scope",
            safe_next_action="retry only if RE-034 can name assignments without raw evidence leakage",
            code_change_readiness="blocked",
            next_ticket="RE-036",
            status="Done",
            progress=PROGRESS,
            safety_contract=SAFETY_CONTRACT,
        ),
        ReconstructionBacklogTicket(
            story_id="RE-036",
            title="RestoreLevelData group 8 subtype/layout/fanout readiness",
            topic="group8-subtype-layout-fanout-readiness",
            depends_on=("RE-026", "RE-031", "RE-035"),
            target_save_groups=(8,),
            blockers=group8_blockers + ("group5 item flag payload dependency",),
            decision="group8-remains-blocked-by-fanout-layout-and-group5-dependency",
            safe_next_action="prove subtype fanout and layout field identities after group5 dependency is resolved or excluded",
            code_change_readiness="blocked",
            next_ticket="RE-037",
            status="Done",
            progress=PROGRESS,
            safety_contract=SAFETY_CONTRACT,
        ),
        ReconstructionBacklogTicket(
            story_id="RE-037",
            title="RestoreLevelData partial patch readiness matrix",
            topic="partial-patch-readiness-matrix",
            depends_on=("RE-031", "RE-032", "RE-033", "RE-035", "RE-036"),
            target_save_groups=(4, 5, 8, 10),
            blockers=("no target save group has code-change-ready evidence", "source RestoreLevelData patch remains unsafe"),
            decision="no-partial-patch-ready",
            safe_next_action="defer RE-038 source patch until at least one proof row becomes code-change-ready",
            code_change_readiness="blocked",
            next_ticket="RE-038",
            status="Done",
            progress=PROGRESS,
            safety_contract=SAFETY_CONTRACT,
        ),
    )
    ready = sum(1 for ticket in tickets if ticket.code_change_readiness == "ready")
    return ReconstructionBacklog(
        tickets=tickets,
        status="restoreleveldata-reconstruction-backlog-blocked",
        patch_scope_decision="documentation-only-no-source-patch",
        code_change_ready_count=ready,
    )


def write_csv(backlog: ReconstructionBacklog, path: Path) -> None:
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
        for ticket in backlog.tickets:
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


def write_markdown(backlog: ReconstructionBacklog, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RestoreLevelData reconstruction backlog RE-031..RE-037",
        "",
        "Status: Generated",
        "Stories: `docs/stories/RE-031` through `docs/stories/RE-037`",
        "",
        "## Progress tracker",
        "",
        "- [x] Input artifacts loaded.",
        "- [x] Metadata-only decisions published.",
        "- [x] Source patch readiness evaluated.",
        "- [x] Forbidden raw evidence excluded.",
        "",
        "## Summary",
        "",
        f"- status: `{backlog.status}`",
        f"- patch scope decision: `{backlog.patch_scope_decision}`",
        f"- tickets covered: `{len(backlog.tickets)}`",
        f"- code-change-ready tickets: `{backlog.code_change_ready_count}`",
        "",
        "## Ticket matrix",
    ]
    for ticket in backlog.tickets:
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
        "Do not patch `GAME/SAVEGAME.C` from this backlog. No RE-031..RE-037 ticket makes a code-change-ready claim; all outputs are documentation/proof scope only.",
        "",
        "Recommended next ticket: RE-038 — source patch only after a later proof row becomes code-change-ready; otherwise continue proof-first blocker reduction.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _story_slug(ticket: ReconstructionBacklogTicket) -> str:
    return ticket.topic.replace("_", "-")


def _write_story(ticket: ReconstructionBacklogTicket, story_dir: Path) -> Path:
    story_dir.mkdir(parents=True, exist_ok=True)
    path = story_dir / f"{ticket.story_id}-{_story_slug(ticket)}.md"
    lines = [
        f"# {ticket.story_id} — {ticket.title}",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        f"Publish a metadata-only decision for `{ticket.topic}` without source patch claims or raw reverse-engineering evidence.",
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
        "- [x] Metadata-only decision published.",
        "- [x] Source patch readiness evaluated.",
        "- [x] Forbidden raw evidence excluded.",
        "",
        "## Findings",
        "",
    ]
    for blocker in ticket.blockers:
        lines.append(f"- blocker: `{blocker}`")
    lines.extend([
        "",
        "## Readiness decision",
        "",
        f"- decision: `{ticket.decision}`",
        f"- safe next action: `{ticket.safe_next_action}`",
        f"- code change readiness: `{ticket.code_change_readiness}`",
        "",
        "Do not patch `GAME/SAVEGAME.C` or add `(F)`, `(D)`, or `(**)` markers from this story alone.",
        "",
        "## Validation",
        "",
        "- `pytest tests/reverse/test_restoreleveldata_reconstruction_backlog.py -q`",
        "- metadata-only guard over generated/story outputs",
        "",
        "## Next step",
        "",
        f"{ticket.next_ticket}: continue proof-first blocker reduction before any source reconstruction.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_all_artifacts(backlog: ReconstructionBacklog, base_dir: Path = ROOT) -> dict[str, object]:
    csv_path = base_dir / DEFAULT_OUT_CSV
    md_path = base_dir / DEFAULT_OUT_MD
    story_dir = base_dir / STORY_DIR
    write_csv(backlog, csv_path)
    write_markdown(backlog, md_path)
    story_paths = [_write_story(ticket, story_dir) for ticket in backlog.tickets]
    return {"csv": csv_path, "md": md_path, "stories": story_paths}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    backlog = build_restoreleveldata_reconstruction_backlog(args.repo)
    write_all_artifacts(backlog, args.repo)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
