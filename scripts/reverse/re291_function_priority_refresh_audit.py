#!/usr/bin/env python3
"""Generate RE-291 function-priority upstream refresh audit artifacts."""

from __future__ import annotations

import argparse
import csv
import sys
import tempfile
from dataclasses import asdict, dataclass, fields
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.reverse.function_priority import priority_rows, read_rows, write_csv

SOURCE_MAP = "docs/reverse/generated/repo-function-map.csv"
CURRENT_PRIORITY = "docs/reverse/generated/function-priority.csv"
UPSTREAM_HANDOFF = "docs/reverse/generated/re290-final-function-priority-handoff.csv"

AUDIT_CSV = "docs/reverse/generated/re291-function-priority-refresh-audit.csv"
HANDOFF_CSV = "docs/reverse/generated/re291-function-priority-refresh-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re291-function-priority-upstream-refresh-audit.md"
STORY = "docs/stories/RE-291-function-priority-upstream-refresh-audit.md"

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


@dataclass(frozen=True)
class RefreshAudit:
    story_id: str
    topic: str
    upstream_handoff: str
    source_map: str
    current_priority: str
    source_map_rows: int
    current_priority_rows: int
    regenerated_priority_rows: int
    priority_delta_rows: int
    priority_changed: str
    next_ticket: str
    next_topic: str
    selected_domain: str
    selected_pivot: str
    code_change_readiness: str
    stop_condition: str


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_upstream(repo: Path) -> None:
    rows = read_csv(repo / UPSTREAM_HANDOFF)
    if len(rows) != 1:
        raise ValueError("RE-290 handoff must contain exactly one row")
    expected = {
        "next_ticket": "TBD",
        "next_topic": "function-priority-backlog-exhausted",
        "selected_domain": "none",
        "selected_pivot": "none",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if rows[0].get(key) != value:
            raise ValueError(f"RE-290 handoff drift: {key}={rows[0].get(key)!r}")


def regenerated_priority_csv_rows(repo: Path) -> list[dict[str, str]]:
    source_rows = read_rows(repo / SOURCE_MAP)
    priorities = priority_rows(source_rows)
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "function-priority.csv"
        write_csv(out, priorities)
        return read_csv(out)


def delta_count(current_rows: list[dict[str, str]], regenerated_rows: list[dict[str, str]]) -> int:
    max_len = max(len(current_rows), len(regenerated_rows))
    count = 0
    for index in range(max_len):
        left = current_rows[index] if index < len(current_rows) else None
        right = regenerated_rows[index] if index < len(regenerated_rows) else None
        if left != right:
            count += 1
    return count


def build_audit(repo: Path) -> RefreshAudit:
    repo = Path(repo)
    validate_upstream(repo)
    source_rows = read_rows(repo / SOURCE_MAP)
    current_rows = read_csv(repo / CURRENT_PRIORITY)
    regenerated_rows = regenerated_priority_csv_rows(repo)
    deltas = delta_count(current_rows, regenerated_rows)
    changed = "yes" if deltas else "no"
    next_topic = "function-priority-inputs-changed" if deltas else "function-priority-inputs-unchanged"
    return RefreshAudit(
        story_id="RE-291",
        topic="function-priority-upstream-refresh-audit",
        upstream_handoff="RE-290",
        source_map=SOURCE_MAP,
        current_priority=CURRENT_PRIORITY,
        source_map_rows=len(source_rows),
        current_priority_rows=len(current_rows),
        regenerated_priority_rows=len(regenerated_rows),
        priority_delta_rows=deltas,
        priority_changed=changed,
        next_ticket="TBD",
        next_topic=next_topic,
        selected_domain="none",
        selected_pivot="none",
        code_change_readiness="blocked",
        stop_condition="provide changed repo-function-map.csv or new non-raw proof evidence before opening another epic",
    )


def write_row(path: Path, row: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    names = [field.name for field in fields(row)]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=names, lineterminator="\n")
        writer.writeheader()
        writer.writerow(asdict(row))


def write_markdown(path: Path, audit: RefreshAudit) -> None:
    lines = [
        "# RE-291 function-priority upstream refresh audit",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-290 final handoff consumed.",
        "- [x] Current repo-function-map.csv consumed.",
        "- [x] function-priority.csv regenerated in an isolated temp output.",
        "- [x] Existing and regenerated priority rows compared.",
        "- [x] Handoff emitted without selecting a fake domain.",
        "",
        "## Refresh result",
        "",
        f"- Source map rows: `{audit.source_map_rows}`",
        f"- Current priority rows: `{audit.current_priority_rows}`",
        f"- Regenerated priority rows: `{audit.regenerated_priority_rows}`",
        f"- Priority delta rows: `{audit.priority_delta_rows}`",
        f"- Priority changed: `{audit.priority_changed}`",
        "",
        "## Readiness",
        "",
        f"- Readiness: `{audit.code_change_readiness}`",
        f"- Next ticket: `{audit.next_ticket}`",
        f"- Next topic: `{audit.next_topic}`",
        f"- Selected domain: `{audit.selected_domain}`",
        f"- Selected pivot: `{audit.selected_pivot}`",
        f"- Stop condition: `{audit.stop_condition}`",
        "",
        "No production source or marker change is authorized by this audit.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story(path: Path, audit: RefreshAudit) -> None:
    lines = [
        "# RE-291 — function-priority upstream refresh audit",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Refresh the upstream function-priority input pipeline after RE-290 and decide whether a new proof epic can be selected.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-290 terminal handoff validated.",
        "- [x] Current repo-function-map.csv consumed.",
        "- [x] Priority CSV regenerated from current inputs in temp output.",
        "- [x] Delta count recorded.",
        "- [x] Readiness and stop condition recorded.",
        "",
        "## Artifacts",
        "",
        f"- Audit CSV: `{AUDIT_CSV}`",
        f"- Handoff CSV: `{HANDOFF_CSV}`",
        f"- Markdown: `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- Regenerated priority rows: `{audit.regenerated_priority_rows}`",
        f"- Priority delta rows: `{audit.priority_delta_rows}`",
        f"- Priority changed: `{audit.priority_changed}`",
        "",
        "## Readiness",
        "",
        f"- Readiness: `{audit.code_change_readiness}`",
        f"- Next ticket: `{audit.next_ticket}`",
        f"- Next topic: `{audit.next_topic}`",
        f"- Selected domain: `{audit.selected_domain}`",
        f"- Selected pivot: `{audit.selected_pivot}`",
        f"- Stop condition: `{audit.stop_condition}`",
        "",
        "No production source or marker change is authorized by this story.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_all_artifacts(audit: RefreshAudit, base: Path) -> dict[str, Path]:
    base = Path(base)
    paths = {
        "audit_csv": base / AUDIT_CSV,
        "handoff_csv": base / HANDOFF_CSV,
        "md": base / MD_OUTPUT,
        "story": base / STORY,
    }
    write_row(paths["audit_csv"], audit)
    write_row(paths["handoff_csv"], audit)
    write_markdown(paths["md"], audit)
    write_story(paths["story"], audit)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    audit = build_audit(repo)
    write_all_artifacts(audit, repo)


if __name__ == "__main__":
    main()
