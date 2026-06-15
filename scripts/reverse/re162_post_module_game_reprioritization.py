#!/usr/bin/env python3
"""Generate RE-162 post-module-game domain reprioritization artifacts.

This is a metadata-only selection gate after RE-161 emitted a parent-level
`module-game-exhausted` handoff. It reuses the earlier domain-priority shortlist,
excludes already closed/exhausted domains, and selects the next proof-first audit
without authorizing source or marker changes.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


UPSTREAM_HANDOFF = "docs/reverse/generated/re161-ui-text-support-handoff.csv"
SOURCE_REPRIORITIZATION = "docs/reverse/generated/re044-domain-reprioritization.csv"
CSV_OUTPUT = "docs/reverse/generated/re162-post-module-game-domain-reprioritization.csv"
MD_OUTPUT = "docs/reverse/functions/re162-post-module-game-domain-reprioritization.md"
STORY_OUTPUT = "docs/stories/RE-162-post-module-game-domain-reprioritization.md"

CLOSED_DOMAINS = {"audio-effects", "collision", "module-game"}
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
class DomainRow:
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
    rationale: str
    next_action: str
    next_ticket: str
    code_change_readiness: str


@dataclass(frozen=True)
class ReprioritizationPlan:
    story_id: str
    upstream_ticket: str
    upstream_status: str
    status: str
    selected_domain: str
    selected_pivot: str
    next_ticket: str
    code_change_readiness: str
    excluded_domains: tuple[str, ...]
    rows: tuple[DomainRow, ...]


def parse_int(value: str | None) -> int:
    try:
        return int(value or "0")
    except ValueError:
        return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_upstream_handoff(rows: list[dict[str, str]]) -> None:
    if len(rows) != 1:
        raise ValueError("RE-161 handoff must contain exactly one row")
    row = rows[0]
    expected = {
        "next_ticket": "TBD",
        "next_cluster": "module-game-exhausted",
        "next_subcluster": "module-game-exhausted",
        "pivot": "TBD",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-161 handoff drift: expected {key}={value!r}, got {row.get(key)!r}")


def build_reprioritization(repo: Path) -> ReprioritizationPlan:
    repo = Path(repo)
    validate_upstream_handoff(read_csv(repo / UPSTREAM_HANDOFF))
    source_rows = read_csv(repo / SOURCE_REPRIORITIZATION)

    candidates = [row for row in source_rows if row.get("domain_id") not in CLOSED_DOMAINS]
    if not candidates:
        raise ValueError("No candidate domains remain after module-game exhaustion")

    ranked: list[DomainRow] = []
    for index, row in enumerate(candidates, start=1):
        domain_id = row.get("domain_id", "")
        next_ticket = "RE-163" if index == 1 else "TBD"
        if index == 1:
            next_action = f"open RE-163 {domain_id} proof-first audit"
            rationale = (
                "next-ranked domain after module-game exhaustion; "
                + row.get("rationale", "")
            )
        else:
            next_action = "defer until higher-ranked post-module-game domain is selected"
            rationale = row.get("rationale", "")
        ranked.append(
            DomainRow(
                rank=index,
                domain_id=domain_id,
                status=row.get("status", "candidate"),
                score=parse_int(row.get("score")),
                candidate_count=parse_int(row.get("candidate_count")),
                mapped_count=parse_int(row.get("mapped_count")),
                nd_count=parse_int(row.get("nd_count")),
                runtime_count=parse_int(row.get("runtime_count")),
                top_function=row.get("top_function", ""),
                top_file=row.get("top_file", ""),
                rationale=rationale,
                next_action=next_action,
                next_ticket=next_ticket,
                code_change_readiness="blocked",
            )
        )

    selected = ranked[0]
    return ReprioritizationPlan(
        story_id="RE-162",
        upstream_ticket="RE-161",
        upstream_status="module-game-exhausted",
        status="post-module-game-domain-reprioritization-ready",
        selected_domain=selected.domain_id,
        selected_pivot=selected.top_function,
        next_ticket="RE-163",
        code_change_readiness="documentation-only-selection-gate",
        excluded_domains=tuple(sorted(CLOSED_DOMAINS)),
        rows=tuple(ranked),
    )


def write_csv(path: Path, plan: ReprioritizationPlan) -> None:
    fields = [
        "rank",
        "domain_id",
        "status",
        "score",
        "candidate_count",
        "mapped_count",
        "nd_count",
        "runtime_count",
        "top_function",
        "top_file",
        "rationale",
        "next_action",
        "next_ticket",
        "code_change_readiness",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in plan.rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def write_markdown(path: Path, plan: ReprioritizationPlan) -> None:
    lines = [
        "# RE-162 post-module-game domain reprioritization",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-161 module-game exhaustion handoff consumed.",
        "- [x] Closed domains excluded from the next-domain shortlist.",
        "- [x] Ranked metadata-only next-domain rows emitted.",
        "- [x] Proof-first next ticket selected without source or marker changes.",
        "",
        "## Decision",
        "",
        f"- Upstream status: `{plan.upstream_status}`",
        f"- Closed domains excluded: `{', '.join(plan.excluded_domains)}`",
        f"- Selected next domain: `{plan.selected_domain}`",
        f"- Selected pivot: `{plan.selected_pivot}`",
        f"- Recommended next ticket: `{plan.next_ticket}`",
        f"- Code-change readiness: `{plan.code_change_readiness}`",
        "",
        "No production source or marker change is authorized by this selection gate.",
        "",
        "## Ranked candidates",
        "",
    ]
    for row in plan.rows:
        lines.append(
            f"- #{row.rank} `{row.domain_id}` / `{row.top_function}` "
            f"({row.candidate_count} candidates): {row.next_action}; readiness `{row.code_change_readiness}`."
        )
    lines.extend([
        "",
        "## Next proof",
        "",
        f"Open `{plan.next_ticket}` as a proof-first audit for `{plan.selected_domain}` before any source reconstruction or marker update.",
        "",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_story(path: Path, plan: ReprioritizationPlan) -> None:
    lines = [
        "# RE-162 — Post-module-game domain reprioritization",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Select the next reverse-engineering backlog outside the exhausted RE-061 module-game parent domain.",
        "",
        "## Scope",
        "",
        "- depends on: `RE-161`, `RE-044`",
        "- safety contract: metadata-only generated rows; binary instruction text, proprietary dump records, and raw address literals stay out of versioned outputs",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-161 module-game exhaustion handoff consumed.",
        "- [x] Closed domains excluded.",
        "- [x] Next-domain shortlist generated.",
        "- [x] Readiness decision recorded.",
        "- [x] Forbidden raw evidence excluded.",
        "",
        "## Generated artifacts",
        "",
        f"- `{CSV_OUTPUT}`",
        f"- `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- selected next domain: `{plan.selected_domain}`",
        f"- selected pivot: `{plan.selected_pivot}`",
        f"- excluded closed domains: `{', '.join(plan.excluded_domains)}`",
        "- all rows remain blocked for source or marker changes until a domain-specific proof-first audit runs",
        "",
        "## Selection decision",
        "",
        f"Recommended next ticket: `{plan.next_ticket}`",
        f"Code-change readiness: `{plan.code_change_readiness}`",
        "No production source or marker change is authorized by this selection gate.",
        "",
        "## Validation",
        "",
        "- `python3 -m pytest tests/reverse/test_re162_post_module_game_reprioritization.py -q`",
        "- metadata-only guard over RE-162 outputs",
        "",
        "## Next step",
        "",
        f"{plan.next_ticket}: open a proof-first audit for `{plan.selected_domain}` / `{plan.selected_pivot}`.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_all_artifacts(plan: ReprioritizationPlan, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "csv": repo / CSV_OUTPUT,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY_OUTPUT,
    }
    write_csv(paths["csv"], plan)
    write_markdown(paths["md"], plan)
    write_story(paths["story"], plan)
    return paths


def assert_metadata_only(paths: dict[str, Path]) -> None:
    for path in paths.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            if fragment in text:
                raise ValueError(f"forbidden metadata fragment {fragment!r} in {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="repository root")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    plan = build_reprioritization(repo)
    written = write_all_artifacts(plan, repo)
    assert_metadata_only(written)
    print(f"selected_domain={plan.selected_domain}")
    print(f"selected_pivot={plan.selected_pivot}")
    print(f"next_ticket={plan.next_ticket}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
