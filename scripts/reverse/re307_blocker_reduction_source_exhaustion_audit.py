#!/usr/bin/env python3
"""Generate RE-307 blocker-reduction source exhaustion audit artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE296_CANDIDATES = "docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv"
RE306_HANDOFF = "docs/reverse/generated/re306-handoff-stop-condition-readiness-gate-handoff.csv"

AUDIT_CSV = "docs/reverse/generated/re307-blocker-reduction-source-exhaustion-audit.csv"
SUMMARY_CSV = "docs/reverse/generated/re307-blocker-reduction-source-exhaustion-audit-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re307-blocker-reduction-source-exhaustion-audit-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re307-blocker-reduction-source-exhaustion-audit.md"
STORY = "docs/stories/RE-307-blocker-reduction-source-exhaustion-audit.md"

FORBIDDEN = (
    "word_le_hex",
    "payload_offset",
    "dump row",
    "opcode",
    "machine word",
    "call_address",
    "branch target",
    "call target",
    "hex-address-fragment",
    "raw_evidence",
)

SOURCE_CHAIN = {
    "story-tracker": {
        "selection_rank": 1,
        "reduction_story": "RE-297",
        "reduction_topic": "story-tracker-readiness-statement-reduction",
        "reduction_handoff": "docs/reverse/generated/re297-story-tracker-readiness-statement-reduction-handoff.csv",
        "reduction_ready_field": "metadata_reduction_ready_count",
        "gate_story": "RE-298",
        "gate_topic": "story-tracker-blocker-taxonomy-readiness-gate",
        "gate_handoff": "docs/reverse/generated/re298-story-tracker-blocker-taxonomy-readiness-gate-handoff.csv",
        "gate_ready_field": "ready_to_reopen_domain_count",
    },
    "generated-markdown": {
        "selection_rank": 2,
        "reduction_story": "RE-299",
        "reduction_topic": "generated-markdown-blocker-taxonomy-reduction",
        "reduction_handoff": "docs/reverse/generated/re299-generated-markdown-blocker-taxonomy-reduction-handoff.csv",
        "reduction_ready_field": "metadata_reduction_ready_count",
        "gate_story": "RE-300",
        "gate_topic": "generated-markdown-blocker-taxonomy-readiness-gate",
        "gate_handoff": "docs/reverse/generated/re300-generated-markdown-blocker-taxonomy-readiness-gate-handoff.csv",
        "gate_ready_field": "ready_to_reopen_domain_count",
    },
    "proof-audits": {
        "selection_rank": 3,
        "reduction_story": "RE-301",
        "reduction_topic": "proof-audit-blocker-taxonomy-reduction",
        "reduction_handoff": "docs/reverse/generated/re301-proof-audit-blocker-taxonomy-reduction-handoff.csv",
        "reduction_ready_field": "metadata_reduction_ready_count",
        "gate_story": "RE-302",
        "gate_topic": "proof-audit-blocker-taxonomy-readiness-gate",
        "gate_handoff": "docs/reverse/generated/re302-proof-audit-blocker-taxonomy-readiness-gate-handoff.csv",
        "gate_ready_field": "ready_to_reopen_domain_count",
    },
    "source-patch-gates": {
        "selection_rank": 4,
        "reduction_story": "RE-303",
        "reduction_topic": "source-patch-gate-denial-reduction",
        "reduction_handoff": "docs/reverse/generated/re303-source-patch-gate-denial-reduction-handoff.csv",
        "reduction_ready_field": "metadata_reduction_ready_count",
        "gate_story": "RE-304",
        "gate_topic": "source-patch-gate-denial-readiness-gate",
        "gate_handoff": "docs/reverse/generated/re304-source-patch-gate-denial-readiness-gate-handoff.csv",
        "gate_ready_field": "ready_to_reopen_domain_count",
    },
    "handoff-csvs": {
        "selection_rank": 5,
        "reduction_story": "RE-305",
        "reduction_topic": "handoff-stop-condition-reduction",
        "reduction_handoff": "docs/reverse/generated/re305-handoff-stop-condition-reduction-handoff.csv",
        "reduction_ready_field": "metadata_reduction_ready_count",
        "gate_story": "RE-306",
        "gate_topic": "handoff-stop-condition-readiness-gate",
        "gate_handoff": RE306_HANDOFF,
        "gate_ready_field": "ready_to_reopen_domain_count",
    },
}


@dataclass(frozen=True)
class ExhaustionAuditRow:
    selection_rank: int
    source_id: str
    candidate_id: str
    candidate_status: str
    safety_class: str
    reduction_story: str
    reduction_topic: str
    reduction_ready_count: int
    gate_story: str
    gate_topic: str
    ready_to_reopen_domain_count: int
    source_patch_authorized_count: int
    exhaustion_status: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    next_required_input: str


@dataclass(frozen=True)
class ExhaustionSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    candidate_source_count: int
    reduction_complete_count: int
    readiness_gate_complete_count: int
    remaining_metadata_source_count: int
    ready_to_reopen_domain_count: int
    source_patch_authorized_count: int
    raw_or_asset_source_count: int
    next_ticket: str
    next_topic: str
    selected_domain: str
    selected_pivot: str
    metadata_work_readiness: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class ExhaustionBundle:
    rows: list[ExhaustionAuditRow]
    summary: ExhaustionSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def one_row(repo: Path, rel_path: str) -> dict[str, str]:
    rows = read_csv(repo / rel_path)
    if len(rows) != 1:
        raise ValueError(f"{rel_path} must contain exactly one row")
    return rows[0]


def validate_re306_handoff(repo: Path) -> None:
    row = one_row(repo, RE306_HANDOFF)
    expected = {
        "story_id": "RE-306",
        "next_ticket": "RE-307",
        "next_topic": "blocker-reduction-source-exhaustion-audit",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "raw_or_asset_source_count": "0",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-306 handoff drift: {key}={row.get(key)!r}")


def validate_candidate_rows(rows: list[dict[str, str]]) -> None:
    source_ids = [row["source_id"] for row in rows]
    if source_ids != ["story-tracker", "generated-markdown", "proof-audits", "source-patch-gates", "handoff-csvs"]:
        raise ValueError(f"RE-296 candidate source order drift: {source_ids!r}")
    for row in rows:
        expected = {
            "safety_class": "metadata-only",
            "raw_or_asset_dependency": "no",
            "source_patch_authorized": "no",
            "metadata_candidate_ready": "yes",
            "domain_selection_ready": "no",
        }
        for key, value in expected.items():
            if row.get(key) != value:
                raise ValueError(f"RE-296 candidate drift for {row['source_id']}: {key}={row.get(key)!r}")


def int_field(row: dict[str, str], field: str) -> int:
    value = row.get(field)
    if value is None or value == "":
        raise ValueError(f"missing field {field}")
    return int(value)


def build_row(repo: Path, candidate: dict[str, str]) -> ExhaustionAuditRow:
    source_id = candidate["source_id"]
    chain = SOURCE_CHAIN[source_id]
    reduction_handoff = one_row(repo, str(chain["reduction_handoff"]))
    gate_handoff = one_row(repo, str(chain["gate_handoff"]))
    if reduction_handoff.get("story_id") != chain["reduction_story"] or reduction_handoff.get("topic") != chain["reduction_topic"]:
        raise ValueError(f"reduction handoff drift for {source_id}")
    if gate_handoff.get("story_id") != chain["gate_story"] or gate_handoff.get("topic") != chain["gate_topic"]:
        raise ValueError(f"gate handoff drift for {source_id}")
    if gate_handoff.get("selected_domain") != "none" or gate_handoff.get("selected_pivot") != "none":
        raise ValueError(f"gate unexpectedly selected a domain for {source_id}")
    if gate_handoff.get("code_change_readiness") != "blocked":
        raise ValueError(f"gate unexpectedly changed code readiness for {source_id}")
    source_patch_authorized = int(gate_handoff.get("source_patch_authorized_count", "0"))
    ready_count = int_field(gate_handoff, str(chain["gate_ready_field"]))
    if ready_count or source_patch_authorized:
        status = "ready"
        ready = "yes"
    else:
        status = "exhausted-blocked"
        ready = "no"
    return ExhaustionAuditRow(
        selection_rank=int(chain["selection_rank"]),
        source_id=source_id,
        candidate_id=candidate["candidate_id"],
        candidate_status=candidate["selection_status"],
        safety_class=candidate["safety_class"],
        reduction_story=str(chain["reduction_story"]),
        reduction_topic=str(chain["reduction_topic"]),
        reduction_ready_count=int_field(reduction_handoff, str(chain["reduction_ready_field"])),
        gate_story=str(chain["gate_story"]),
        gate_topic=str(chain["gate_topic"]),
        ready_to_reopen_domain_count=ready_count,
        source_patch_authorized_count=source_patch_authorized,
        exhaustion_status=status,
        ready_to_reopen_domain=ready,
        source_patch_authorized="yes" if source_patch_authorized else "no",
        next_required_input="changed-upstream-mapping-or-new-non-raw-proof-evidence",
    )


def build_blocker_reduction_source_exhaustion_audit(repo: Path) -> ExhaustionBundle:
    repo = Path(repo)
    validate_re306_handoff(repo)
    candidates = read_csv(repo / RE296_CANDIDATES)
    validate_candidate_rows(candidates)
    rows = [build_row(repo, candidate) for candidate in candidates]
    rows = sorted(rows, key=lambda row: row.selection_rank)
    summary = ExhaustionSummary(
        story_id="RE-307",
        topic="blocker-reduction-source-exhaustion-audit",
        upstream_handoff="RE-306",
        candidate_source_count=len(rows),
        reduction_complete_count=sum(1 for row in rows if row.reduction_ready_count > 0),
        readiness_gate_complete_count=len(rows),
        remaining_metadata_source_count=sum(1 for row in rows if row.exhaustion_status != "exhausted-blocked"),
        ready_to_reopen_domain_count=sum(row.ready_to_reopen_domain_count for row in rows),
        source_patch_authorized_count=sum(row.source_patch_authorized_count for row in rows),
        raw_or_asset_source_count=0,
        next_ticket="TBD",
        next_topic="blocker-reduction-sources-exhausted",
        selected_domain="none",
        selected_pivot="none",
        metadata_work_readiness="blocked",
        code_change_readiness="blocked",
        stop_condition="provide changed upstream mapping or new non-raw proof evidence before selecting another proof domain",
    )
    return ExhaustionBundle(rows=rows, summary=summary)


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


def write_markdown(path: Path, bundle: ExhaustionBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-307 blocker-reduction source exhaustion audit",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-306 handoff stop-condition readiness gate validated.",
        "- [x] RE-296 blocker-reduction source list validated.",
        "- [x] RE-297 through RE-306 reduction/gate handoffs audited.",
        "- [x] Proof-domain selection kept blocked because every metadata source is exhausted or gated blocked.",
        "",
        "## Exhaustion decision",
        "",
        f"- Candidate metadata sources: `{s.candidate_source_count}`",
        f"- Reduction-complete sources: `{s.reduction_complete_count}`",
        f"- Readiness-gate-complete sources: `{s.readiness_gate_complete_count}`",
        f"- Remaining metadata sources: `{s.remaining_metadata_source_count}`",
        f"- Ready to reopen proof-domain selection: `{s.ready_to_reopen_domain_count}`",
        f"- Source patch authorized rows: `{s.source_patch_authorized_count}`",
        "",
        "All blocker-reduction metadata sources are exhausted or gated blocked. The safe next input is changed upstream mapping or new non-raw proof evidence, not another invented proof domain.",
        "",
        "## Source matrix",
        "",
    ]
    for row in bundle.rows:
        lines.extend(
            [
                f"### `{row.source_id}`",
                "",
                f"- Candidate: `{row.candidate_id}`",
                f"- Reduction: `{row.reduction_story}` / `{row.reduction_topic}`",
                f"- Gate: `{row.gate_story}` / `{row.gate_topic}`",
                f"- Exhaustion status: `{row.exhaustion_status}`",
                f"- Ready to reopen domain: `{row.ready_to_reopen_domain}`",
                f"- Source patch authorized: `{row.source_patch_authorized}`",
                f"- Next required input: `{row.next_required_input}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Readiness decision",
            "",
            "No production source or marker change is authorized by this audit.",
            "Proof-domain selection remains blocked until changed upstream mapping or new non-raw proof evidence is supplied.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story(path: Path, bundle: ExhaustionBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-307 blocker-reduction source exhaustion audit",
        "",
        "## Goal",
        "",
        "Audit whether the RE-296 blocker-reduction metadata sources have all been reduced and gated, and whether any safe source remains before selecting another proof domain.",
        "",
        "## Inputs",
        "",
        f"- Upstream handoff: `{RE306_HANDOFF}`",
        f"- Candidate source list: `{RE296_CANDIDATES}`",
        "- Reduction/gate handoffs: RE-297 through RE-306.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-306 handoff stop-condition readiness gate validated.",
        "- [x] RE-296 candidate source ordering and safety flags validated.",
        "- [x] Each candidate source matched to its reduction and readiness gate handoff.",
        "- [x] Exhaustion matrix, summary, handoff, Markdown, and story generated.",
        "- [x] Source/code readiness remains blocked.",
        "",
        "## Generated artifacts",
        "",
        f"- `{AUDIT_CSV}`",
        f"- `{SUMMARY_CSV}`",
        f"- `{HANDOFF_CSV}`",
        f"- `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- Candidate metadata sources: `{s.candidate_source_count}`",
        f"- Reduction-complete sources: `{s.reduction_complete_count}`",
        f"- Readiness-gate-complete sources: `{s.readiness_gate_complete_count}`",
        f"- Remaining metadata sources: `{s.remaining_metadata_source_count}`",
        f"- Ready to reopen proof-domain selection: `{s.ready_to_reopen_domain_count}`",
        f"- Source patch authorized rows: `{s.source_patch_authorized_count}`",
        "",
    ]
    for row in bundle.rows:
        lines.append(f"- `{row.source_id}`: `{row.exhaustion_status}` via `{row.reduction_story}` -> `{row.gate_story}`.")
    lines.extend(
        [
            "",
            "## Readiness decision",
            "",
            "All blocker-reduction metadata sources have been reduced and gated without reopening a proof domain. Metadata work is now blocked until changed upstream mapping or new non-raw proof evidence appears.",
            "",
            "## Follow-up ticket breakdown",
            "",
            "- `TBD` / `changed-upstream-mapping-refresh`: if `repo-function-map.csv` or equivalent upstream mapping changes, rerun the function-priority refresh/selection chain.",
            "  - Inputs: changed upstream mapping artifact.",
            "  - Stop condition: no mapping delta keeps selected domain/pivot `none`.",
            "- `TBD` / `new-non-raw-proof-evidence-intake`: if a new safe proof artifact appears, inventory and rank it before selecting a proof domain.",
            "  - Inputs: metadata-only or source-symbolic proof evidence; no raw/binary/asset dumps.",
            "  - Stop condition: no actionable non-raw evidence keeps source/code readiness blocked.",
            "",
            "## Validation commands",
            "",
            "- `python -m pytest tests/reverse/test_re307_blocker_reduction_source_exhaustion_audit.py -q`",
            "- `python scripts/reverse/re307_blocker_reduction_source_exhaustion_audit.py --repo .`",
            "- `python -m pytest tests/reverse -q`",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_all_artifacts(bundle: ExhaustionBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "audit_csv": repo / AUDIT_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_rows(paths["audit_csv"], bundle.rows)
    write_rows(paths["summary_csv"], [bundle.summary])
    write_rows(paths["handoff_csv"], [bundle.summary])
    write_markdown(paths["md"], bundle)
    write_story(paths["story"], bundle)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    bundle = build_blocker_reduction_source_exhaustion_audit(args.repo)
    written = write_all_artifacts(bundle, args.repo)
    for key, path in written.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
