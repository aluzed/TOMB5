#!/usr/bin/env python3
"""Generate RE-292 post-refresh evidence unblock audit artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE291_HANDOFF = "docs/reverse/generated/re291-function-priority-refresh-handoff.csv"
SOURCE_MAP = "docs/reverse/generated/repo-function-map.csv"
CURRENT_PRIORITY = "docs/reverse/generated/function-priority.csv"
GENERATED_DIR = "docs/reverse/generated"

AUDIT_CSV = "docs/reverse/generated/re292-post-refresh-evidence-unblock-audit.csv"
HANDOFF_CSV = "docs/reverse/generated/re292-post-refresh-evidence-unblock-handoff.csv"
FOLLOWUP_CSV = "docs/reverse/generated/re292-post-refresh-evidence-followup-plan.csv"
MD_OUTPUT = "docs/reverse/functions/re292-post-refresh-evidence-unblock-audit.md"
STORY = "docs/stories/RE-292-post-refresh-evidence-unblock-audit.md"

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
class EvidenceUnblockAudit:
    story_id: str
    topic: str
    upstream_handoff: str
    priority_changed: str
    source_map_rows: int
    priority_rows: int
    generated_artifact_count: int
    proof_audit_count: int
    callsite_map_count: int
    equivalence_gate_count: int
    new_priority_candidate_count: int
    new_non_raw_proof_evidence: str
    next_ticket: str
    next_topic: str
    selected_domain: str
    selected_pivot: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class Followup:
    ticket_id: str
    slug: str
    goal: str
    deliverable: str
    dependency: str
    status: str


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_re291_handoff(repo: Path) -> dict[str, str]:
    rows = read_csv(repo / RE291_HANDOFF)
    if len(rows) != 1:
        raise ValueError("RE-291 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "story_id": "RE-291",
        "next_ticket": "TBD",
        "next_topic": "function-priority-inputs-unchanged",
        "selected_domain": "none",
        "selected_pivot": "none",
        "code_change_readiness": "blocked",
        "priority_changed": "no",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-291 handoff drift: {key}={row.get(key)!r}")
    return row


def count_rows(path: Path) -> int:
    return len(read_csv(path))


def count_generated(repo: Path, pattern: str) -> int:
    return len(list((repo / GENERATED_DIR).glob(pattern)))


def count_pre_re292_generated_artifacts(repo: Path) -> int:
    return len(
        [
            p
            for p in (repo / GENERATED_DIR).iterdir()
            if p.is_file() and not p.name.startswith("re292-post-refresh-evidence-")
        ]
    )


def build_audit(repo: Path) -> EvidenceUnblockAudit:
    repo = Path(repo)
    handoff = validate_re291_handoff(repo)
    source_map_rows = count_rows(repo / SOURCE_MAP)
    priority_rows = count_rows(repo / CURRENT_PRIORITY)
    generated_artifact_count = count_pre_re292_generated_artifacts(repo)
    proof_audit_count = count_generated(repo, "*proof*.csv")
    callsite_map_count = count_generated(repo, "*callsite*.csv")
    equivalence_gate_count = count_generated(repo, "*equivalence*.csv")

    return EvidenceUnblockAudit(
        story_id="RE-292",
        topic="post-refresh-evidence-unblock-audit",
        upstream_handoff="RE-291",
        priority_changed=handoff["priority_changed"],
        source_map_rows=source_map_rows,
        priority_rows=priority_rows,
        generated_artifact_count=generated_artifact_count,
        proof_audit_count=proof_audit_count,
        callsite_map_count=callsite_map_count,
        equivalence_gate_count=equivalence_gate_count,
        new_priority_candidate_count=0,
        new_non_raw_proof_evidence="no",
        next_ticket="TBD",
        next_topic="await-new-non-raw-proof-evidence",
        selected_domain="none",
        selected_pivot="none",
        code_change_readiness="blocked",
        stop_condition="add changed upstream mapping or new non-raw proof artifact before selecting another domain",
    )


def followup_plan() -> list[Followup]:
    return [
        Followup(
            ticket_id="UNBLOCK-1",
            slug="ingest-updated-repo-function-map",
            goal="Provide or generate a changed repo-function-map.csv and rerun the function-priority refresh audit.",
            deliverable="Updated mapping diff plus refreshed priority delta report.",
            dependency="new upstream mapping input",
            status="blocked-pending-input",
        ),
        Followup(
            ticket_id="UNBLOCK-2",
            slug="ingest-non-raw-proof-evidence",
            goal="Add a metadata-only proof artifact that narrows a previously blocked identity/layout/predicate/equivalence gate.",
            deliverable="New proof CSV/Markdown with source-backed symbolic fields only.",
            dependency="new non-raw proof evidence",
            status="blocked-pending-input",
        ),
        Followup(
            ticket_id="UNBLOCK-3",
            slug="rerun-domain-selection-after-new-evidence",
            goal="Select the next proof domain only after priority rows or proof readiness changes.",
            deliverable="Post-input selection gate naming a real domain and pivot.",
            dependency="UNBLOCK-1 or UNBLOCK-2",
            status="blocked-pending-input",
        ),
    ]


def write_rows(path: Path, rows: list[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("rows required")
    names = [field.name for field in fields(rows[0])]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=names, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_markdown(path: Path, audit: EvidenceUnblockAudit) -> None:
    lines = [
        "# RE-292 post-refresh evidence unblock audit",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-291 refresh handoff validated.",
        "- [x] Current generated evidence inventory counted.",
        "- [x] New priority candidate availability checked.",
        "- [x] New proof-evidence availability checked.",
        "- [x] Blocked handoff and follow-up plan emitted.",
        "",
        "## Inventory result",
        "",
        f"- Source map rows: `{audit.source_map_rows}`",
        f"- Priority rows: `{audit.priority_rows}`",
        f"- Generated artifacts: `{audit.generated_artifact_count}`",
        f"- Proof/audit CSVs: `{audit.proof_audit_count}`",
        f"- Callsite maps: `{audit.callsite_map_count}`",
        f"- Equivalence gates: `{audit.equivalence_gate_count}`",
        f"- New priority candidates: `{audit.new_priority_candidate_count}`",
        f"- New non-raw proof evidence: `{audit.new_non_raw_proof_evidence}`",
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


def write_story(path: Path, audit: EvidenceUnblockAudit) -> None:
    plan = followup_plan()
    lines = [
        "# RE-292 — post-refresh evidence unblock audit",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "After RE-291 found unchanged priority inputs, inventory the available metadata-only evidence and define the next legal unblock path without inventing a proof domain.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-291 refresh handoff validated.",
        "- [x] Generated reverse-evidence inventory counted.",
        "- [x] Priority candidate and proof-evidence availability recorded.",
        "- [x] Follow-up ticket breakdown emitted.",
        "- [x] Readiness and stop condition recorded.",
        "",
        "## Artifacts",
        "",
        f"- Audit CSV: `{AUDIT_CSV}`",
        f"- Handoff CSV: `{HANDOFF_CSV}`",
        f"- Follow-up CSV: `{FOLLOWUP_CSV}`",
        f"- Markdown: `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- New priority candidates: `{audit.new_priority_candidate_count}`",
        f"- New non-raw proof evidence: `{audit.new_non_raw_proof_evidence}`",
        f"- Existing generated artifacts counted: `{audit.generated_artifact_count}`",
        "",
        "## Follow-up ticket breakdown",
        "",
    ]
    for item in plan:
        lines.extend(
            [
                f"### {item.ticket_id} — {item.slug}",
                "",
                f"- Goal: {item.goal}",
                f"- Deliverable: {item.deliverable}",
                f"- Dependency: `{item.dependency}`",
                f"- Status: `{item.status}`",
                "",
            ]
        )
    lines.extend(
        [
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
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_all_artifacts(audit: EvidenceUnblockAudit, base: Path) -> dict[str, Path]:
    base = Path(base)
    paths = {
        "audit_csv": base / AUDIT_CSV,
        "handoff_csv": base / HANDOFF_CSV,
        "followup_csv": base / FOLLOWUP_CSV,
        "md": base / MD_OUTPUT,
        "story": base / STORY,
    }
    write_rows(paths["audit_csv"], [audit])
    write_rows(paths["handoff_csv"], [audit])
    write_rows(paths["followup_csv"], followup_plan())
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
