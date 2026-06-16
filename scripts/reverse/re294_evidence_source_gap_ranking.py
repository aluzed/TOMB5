#!/usr/bin/env python3
"""Generate RE-294 evidence source gap ranking artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE293_HANDOFF = "docs/reverse/generated/re293-evidence-source-inventory-handoff.csv"
RE293_INVENTORY = "docs/reverse/generated/re293-evidence-source-inventory.csv"

RANKING_CSV = "docs/reverse/generated/re294-evidence-source-gap-ranking.csv"
SUMMARY_CSV = "docs/reverse/generated/re294-evidence-source-gap-ranking-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re294-evidence-source-gap-ranking-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re294-evidence-source-gap-ranking.md"
STORY = "docs/stories/RE-294-evidence-source-gap-ranking.md"

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
)

RANKING_RULES: dict[str, dict[str, object]] = {
    "generated-markdown": {
        "score": 100,
        "blocker_class": "human-summary-blockers",
        "actionability": "testable-now",
        "recommended_use": "extract explicit blocker statements into a machine-readable matrix",
        "next_step": "parse RE markdown sections for readiness and stop-condition language",
    },
    "story-tracker": {
        "score": 96,
        "blocker_class": "progression-blockers",
        "actionability": "testable-now",
        "recommended_use": "normalize story progress trackers and blocked follow-up items",
        "next_step": "extract open blocker classes and dependency phrases from story files",
    },
    "handoff-csvs": {
        "score": 92,
        "blocker_class": "handoff-readiness",
        "actionability": "testable-now",
        "recommended_use": "merge next_topic and readiness outcomes across closed chains",
        "next_step": "rank repeated handoff blockers by frequency and recency",
    },
    "source-patch-gates": {
        "score": 88,
        "blocker_class": "patch-gate-denials",
        "actionability": "testable-now",
        "recommended_use": "identify why source or marker patches were denied",
        "next_step": "cluster denial reasons by evidence type needed",
    },
    "proof-audits": {
        "score": 84,
        "blocker_class": "proof-first-gaps",
        "actionability": "testable-now",
        "recommended_use": "recover proof-first blocker wording from prior domain openings",
        "next_step": "extract proof gap classes from audit CSVs",
    },
    "equivalence-gates": {
        "score": 76,
        "blocker_class": "equivalence-readiness",
        "actionability": "testable-with-existing-metadata",
        "recommended_use": "rank equivalence gates by what symbolic evidence is missing",
        "next_step": "compare gate blockers against available state contracts and taxonomies",
    },
    "state-contracts": {
        "score": 72,
        "blocker_class": "state-contract-coverage",
        "actionability": "testable-with-existing-metadata",
        "recommended_use": "map contracts to equivalence gates that still need narrowing",
        "next_step": "join contract names to gate topics where possible",
    },
    "argument-taxonomies": {
        "score": 68,
        "blocker_class": "argument-state-coverage",
        "actionability": "supporting-only",
        "recommended_use": "support blocker extraction with symbolic argument group names",
        "next_step": "link taxonomy topics to proof audit domains",
    },
    "callsite-maps": {
        "score": 64,
        "blocker_class": "callsite-coverage",
        "actionability": "supporting-only",
        "recommended_use": "support source-context claims for already mapped callsite chains",
        "next_step": "compare map topics with blocked gate topics",
    },
    "selection-gates": {
        "score": 60,
        "blocker_class": "selection-history",
        "actionability": "supporting-only",
        "recommended_use": "trace how prior domain selections were exhausted",
        "next_step": "use only after blocker extraction names a plausible domain",
    },
    "comparison-gates": {
        "score": 56,
        "blocker_class": "comparison-readiness",
        "actionability": "supporting-only",
        "recommended_use": "preserve earlier comparison gate blockers",
        "next_step": "fold into unified gate blocker matrix",
    },
    "caller-maps": {
        "score": 52,
        "blocker_class": "legacy-caller-context",
        "actionability": "supporting-only",
        "recommended_use": "normalize older caller maps with newer callsite records",
        "next_step": "deduplicate with callsite maps before domain selection",
    },
    "source-corpus": {
        "score": 40,
        "blocker_class": "source-symbol-context",
        "actionability": "supporting-only",
        "recommended_use": "provide symbolic names and source-level context only",
        "next_step": "do not use alone to reopen binary equivalence or patch readiness",
    },
    "repo-function-map": {
        "score": 24,
        "blocker_class": "unchanged-upstream-map",
        "actionability": "blocked-no-candidate",
        "recommended_use": "baseline function/domain map after unchanged refresh",
        "next_step": "wait for changed upstream mapping before reselection",
    },
    "function-priority": {
        "score": 20,
        "blocker_class": "exhausted-priority-backlog",
        "actionability": "blocked-no-candidate",
        "recommended_use": "document exhausted ranked backlog",
        "next_step": "do not select a fake priority row",
    },
}


@dataclass(frozen=True)
class GapRankingRow:
    rank: int
    source_id: str
    source_type: str
    source_count: int
    safety_class: str
    blocker_class: str
    actionability: str
    priority_score: int
    recommended_use: str
    next_step: str


@dataclass(frozen=True)
class GapRankingSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    ranked_source_count: int
    testable_now_count: int
    testable_with_existing_metadata_count: int
    supporting_only_count: int
    blocked_no_candidate_count: int
    raw_or_asset_source_count: int
    top_source_id: str
    next_ticket: str
    next_topic: str
    selected_domain: str
    selected_pivot: str
    metadata_work_readiness: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class GapRankingBundle:
    rows: list[GapRankingRow]
    summary: GapRankingSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_re293_handoff(repo: Path) -> dict[str, str]:
    rows = read_csv(repo / RE293_HANDOFF)
    if len(rows) != 1:
        raise ValueError("RE-293 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "story_id": "RE-293",
        "next_ticket": "RE-294",
        "next_topic": "evidence-source-gap-ranking",
        "selected_domain": "none",
        "selected_pivot": "none",
        "code_change_readiness": "blocked",
        "raw_or_asset_sources": "0",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-293 handoff drift: {key}={row.get(key)!r}")
    return row


def build_rows(repo: Path) -> list[GapRankingRow]:
    inventory = read_csv(repo / RE293_INVENTORY)
    rows: list[GapRankingRow] = []
    for source in inventory:
        source_id = source["source_id"]
        if source_id not in RANKING_RULES:
            raise ValueError(f"missing ranking rule for {source_id}")
        rule = RANKING_RULES[source_id]
        if source["safety_class"] == "raw-or-asset":
            raise ValueError(f"unsafe source cannot be ranked: {source_id}")
        rows.append(
            GapRankingRow(
                rank=0,
                source_id=source_id,
                source_type=source["source_type"],
                source_count=int(source["row_or_file_count"]),
                safety_class=source["safety_class"],
                blocker_class=str(rule["blocker_class"]),
                actionability=str(rule["actionability"]),
                priority_score=int(rule["score"]),
                recommended_use=str(rule["recommended_use"]),
                next_step=str(rule["next_step"]),
            )
        )
    ranked = sorted(rows, key=lambda row: (-row.priority_score, row.source_id))
    return [row.__class__(rank=i + 1, **{k: v for k, v in asdict(row).items() if k != "rank"}) for i, row in enumerate(ranked)]


def build_gap_ranking(repo: Path) -> GapRankingBundle:
    repo = Path(repo)
    validate_re293_handoff(repo)
    rows = build_rows(repo)
    testable = sum(1 for row in rows if row.actionability == "testable-now")
    existing_metadata = sum(1 for row in rows if row.actionability == "testable-with-existing-metadata")
    supporting = sum(1 for row in rows if row.actionability == "supporting-only")
    blocked = sum(1 for row in rows if row.actionability == "blocked-no-candidate")
    raw = sum(1 for row in rows if row.safety_class == "raw-or-asset")
    summary = GapRankingSummary(
        story_id="RE-294",
        topic="evidence-source-gap-ranking",
        upstream_handoff="RE-293",
        ranked_source_count=len(rows),
        testable_now_count=testable,
        testable_with_existing_metadata_count=existing_metadata,
        supporting_only_count=supporting,
        blocked_no_candidate_count=blocked,
        raw_or_asset_source_count=raw,
        top_source_id=rows[0].source_id,
        next_ticket="RE-295",
        next_topic="metadata-blocker-extraction",
        selected_domain="none",
        selected_pivot="none",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="extract machine-readable blockers from top-ranked metadata sources before selecting a proof domain",
    )
    return GapRankingBundle(rows=rows, summary=summary)


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


def write_markdown(path: Path, bundle: GapRankingBundle) -> None:
    s = bundle.summary
    lines = [
        "# RE-294 evidence source gap ranking",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-293 source inventory handoff validated.",
        "- [x] Safe evidence sources ranked by blocker-reduction potential.",
        "- [x] Raw/binary/asset source classes excluded from ranking.",
        "- [x] Metadata-ready next ticket emitted without selecting a fake proof domain.",
        "",
        "## Summary",
        "",
        f"- Ranked sources: `{s.ranked_source_count}`",
        f"- Testable now: `{s.testable_now_count}`",
        f"- Testable with existing metadata: `{s.testable_with_existing_metadata_count}`",
        f"- Supporting-only sources: `{s.supporting_only_count}`",
        f"- Blocked/no-candidate baselines: `{s.blocked_no_candidate_count}`",
        f"- Raw/asset sources admitted: `{s.raw_or_asset_source_count}`",
        f"- Top source: `{s.top_source_id}`",
        "",
        "## Ranked evidence sources",
        "",
    ]
    for row in bundle.rows:
        lines.extend(
            [
                f"### {row.rank}. {row.source_id}",
                "",
                f"- Score: `{row.priority_score}`",
                f"- Count: `{row.source_count}`",
                f"- Safety: `{row.safety_class}`",
                f"- Actionability: `{row.actionability}`",
                f"- Blocker class: `{row.blocker_class}`",
                f"- Recommended use: {row.recommended_use}.",
                f"- Next step: {row.next_step}.",
                "",
            ]
        )
    lines.extend(
        [
            "## Readiness",
            "",
            f"- Metadata work readiness: `{s.metadata_work_readiness}`",
            f"- Code/source readiness: `{s.code_change_readiness}`",
            f"- Next ticket: `{s.next_ticket}`",
            f"- Next topic: `{s.next_topic}`",
            f"- Selected domain: `{s.selected_domain}`",
            f"- Selected pivot: `{s.selected_pivot}`",
            f"- Stop condition: `{s.stop_condition}`",
            "",
            "No production source or marker change is authorized by this ranking.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story(path: Path, bundle: GapRankingBundle) -> None:
    s = bundle.summary
    top = bundle.rows[:5]
    lines = [
        "# RE-294 — evidence source gap ranking",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Rank the safe evidence sources inventoried by RE-293 by their ability to reduce current blocker classes without using raw/binary/asset material.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-293 source inventory handoff validated.",
        "- [x] Source classes scored for blocker-reduction potential.",
        "- [x] Testable-now metadata sources separated from supporting-only sources.",
        "- [x] Proof-domain selection kept blocked until blockers are extracted.",
        "- [x] Next metadata-only extraction ticket emitted.",
        "",
        "## Artifacts",
        "",
        f"- Ranking CSV: `{RANKING_CSV}`",
        f"- Summary CSV: `{SUMMARY_CSV}`",
        f"- Handoff CSV: `{HANDOFF_CSV}`",
        f"- Markdown: `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- Ranked sources: `{s.ranked_source_count}`",
        f"- Testable now: `{s.testable_now_count}`",
        f"- Raw/asset sources admitted: `{s.raw_or_asset_source_count}`",
        f"- Top source: `{s.top_source_id}`",
        "",
        "Top testable-now sources:",
        "",
    ]
    for row in top:
        lines.append(f"- `{row.source_id}` — `{row.blocker_class}` — score `{row.priority_score}`")
    lines.extend(
        [
            "",
            "The ranking makes metadata work ready, but it still does not authorize production source or marker changes.",
            "",
            "## Next objective",
            "",
            f"- Next ticket: `{s.next_ticket}`",
            f"- Topic: `{s.next_topic}`",
            "- Goal: extract machine-readable blocker classes from the top-ranked metadata sources and determine whether any blocker can be reduced without new external evidence.",
            "",
            "## Readiness",
            "",
            f"- Metadata work readiness: `{s.metadata_work_readiness}`",
            f"- Code/source readiness: `{s.code_change_readiness}`",
            f"- Selected domain: `{s.selected_domain}`",
            f"- Selected pivot: `{s.selected_pivot}`",
            f"- Stop condition: `{s.stop_condition}`",
            "",
            "No production source or marker change is authorized by this story.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_all_artifacts(bundle: GapRankingBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "ranking_csv": repo / RANKING_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_rows(paths["ranking_csv"], bundle.rows)
    write_rows(paths["summary_csv"], [bundle.summary])
    write_rows(paths["handoff_csv"], [bundle.summary])
    write_markdown(paths["md"], bundle)
    write_story(paths["story"], bundle)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", type=Path)
    args = parser.parse_args()
    bundle = build_gap_ranking(args.repo)
    written = write_all_artifacts(bundle, args.repo)
    for name, path in written.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
