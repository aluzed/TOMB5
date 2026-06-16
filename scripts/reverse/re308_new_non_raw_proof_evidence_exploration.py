#!/usr/bin/env python3
"""Generate RE-308 new non-raw proof evidence exploration artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE307_HANDOFF = "docs/reverse/generated/re307-blocker-reduction-source-exhaustion-audit-handoff.csv"
EXPLORATION_CSV = "docs/reverse/generated/re308-new-non-raw-proof-evidence-exploration.csv"
SUMMARY_CSV = "docs/reverse/generated/re308-new-non-raw-proof-evidence-exploration-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re308-new-non-raw-proof-evidence-exploration-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re308-new-non-raw-proof-evidence-exploration.md"
STORY = "docs/stories/RE-308-new-non-raw-proof-evidence-exploration.md"

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

SOURCE_DIRS = ("GAME", "SPEC_PSXPC", "SPEC_PSXPC_N", "SPEC_PSX", "SPEC_PC_N", "TOOLS")
SOURCE_SUFFIXES = {".C", ".H", ".CPP", ".RC"}


@dataclass(frozen=True)
class ExplorationVector:
    vector_rank: int
    vector_id: str
    evidence_class: str
    input_status: str
    actionability: str
    safe_to_inventory: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    observed_count: int
    next_required_input: str
    stop_condition: str


@dataclass(frozen=True)
class ExplorationSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    exploration_vector_count: int
    testable_now_count: int
    needs_new_export_count: int
    exhausted_metadata_count: int
    unsafe_raw_only_count: int
    missing_user_input_count: int
    ready_to_reopen_domain_count: int
    source_patch_authorized_count: int
    next_ticket: str
    next_topic: str
    selected_domain: str
    selected_pivot: str
    metadata_work_readiness: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class ExplorationBundle:
    rows: list[ExplorationVector]
    summary: ExplorationSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def one_row(repo: Path, rel_path: str) -> dict[str, str]:
    rows = read_csv(repo / rel_path)
    if len(rows) != 1:
        raise ValueError(f"{rel_path} must contain exactly one row")
    return rows[0]


def validate_re307_handoff(repo: Path) -> dict[str, str]:
    row = one_row(repo, RE307_HANDOFF)
    expected = {
        "story_id": "RE-307",
        "next_ticket": "TBD",
        "next_topic": "blocker-reduction-sources-exhausted",
        "selected_domain": "none",
        "selected_pivot": "none",
        "remaining_metadata_source_count": "0",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "raw_or_asset_source_count": "0",
        "metadata_work_readiness": "blocked",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-307 handoff drift: {key}={row.get(key)!r}")
    return row


def count_generated_csvs(repo: Path) -> int:
    return len([p for p in (repo / "docs/reverse/generated").glob("*.csv") if not p.name.startswith("re308-")])


def count_taxonomy_docs(repo: Path) -> int:
    generated_md = [p for p in (repo / "docs/reverse/functions").glob("*.md") if not p.name.startswith("re308-")]
    story_md = [p for p in (repo / "docs/stories").glob("RE-*.md") if not p.name.startswith("RE-308-")]
    return len(generated_md) + len(story_md)


def count_source_symbolic_files(repo: Path) -> int:
    count = 0
    for dirname in SOURCE_DIRS:
        base = repo / dirname
        if not base.exists():
            continue
        count += sum(1 for p in base.glob("**/*") if p.is_file() and p.suffix.upper() in SOURCE_SUFFIXES)
    return count


def _vector(
    rank: int,
    vector_id: str,
    evidence_class: str,
    input_status: str,
    actionability: str,
    safe_to_inventory: str,
    observed_count: int,
    next_required_input: str,
    stop_condition: str,
) -> ExplorationVector:
    return ExplorationVector(
        vector_rank=rank,
        vector_id=vector_id,
        evidence_class=evidence_class,
        input_status=input_status,
        actionability=actionability,
        safe_to_inventory=safe_to_inventory,
        ready_to_reopen_domain="no",
        source_patch_authorized="no",
        observed_count=observed_count,
        next_required_input=next_required_input,
        stop_condition=stop_condition,
    )


def build_vectors(repo: Path) -> list[ExplorationVector]:
    return [
        _vector(
            1,
            "changed-upstream-mapping",
            "metadata-only",
            "not-present",
            "needs-new-export",
            "yes",
            0,
            "changed repo-function-map or function-priority export",
            "no mapping delta keeps selected domain and pivot none",
        ),
        _vector(
            2,
            "new-user-supplied-proof-artifact",
            "metadata-only-or-source-symbolic",
            "not-present",
            "missing-input",
            "yes-if-non-raw",
            0,
            "user-provided safe proof artifact or pointer",
            "no provided safe artifact keeps code readiness blocked",
        ),
        _vector(
            3,
            "safe-source-symbolic-export",
            "source-symbolic",
            "available-but-not-new-proof",
            "needs-new-export",
            "yes",
            count_source_symbolic_files(repo),
            "new structured source-symbolic export with proof linkage",
            "source corpus alone is context, not proof-domain readiness",
        ),
        _vector(
            4,
            "existing-generated-metadata",
            "metadata-only",
            "available-exhausted",
            "exhausted-metadata",
            "yes",
            count_generated_csvs(repo),
            "changed generated metadata or newly derived safe evidence",
            "already reduced blocker metadata does not reopen selection",
        ),
        _vector(
            5,
            "existing-story-and-markdown-taxonomies",
            "metadata-only",
            "available-exhausted",
            "exhausted-metadata",
            "yes",
            count_taxonomy_docs(repo),
            "new taxonomy evidence not already gated blocked",
            "existing story and markdown blockers remain non-authorizing",
        ),
        _vector(
            6,
            "raw-binary-or-asset-evidence",
            "unsafe-input-class",
            "rejected",
            "unsafe-raw-only",
            "no",
            0,
            "replace with metadata-only or source-symbolic evidence",
            "unsafe evidence class cannot enter committed artifacts",
        ),
    ]


def build_new_non_raw_proof_evidence_exploration(repo: Path) -> ExplorationBundle:
    repo = Path(repo)
    validate_re307_handoff(repo)
    rows = build_vectors(repo)
    rows = sorted(rows, key=lambda row: row.vector_rank)
    summary = ExplorationSummary(
        story_id="RE-308",
        topic="new-non-raw-proof-evidence-exploration",
        upstream_handoff="RE-307",
        exploration_vector_count=len(rows),
        testable_now_count=sum(1 for row in rows if row.actionability == "testable-now"),
        needs_new_export_count=sum(1 for row in rows if row.actionability == "needs-new-export"),
        exhausted_metadata_count=sum(1 for row in rows if row.actionability == "exhausted-metadata"),
        unsafe_raw_only_count=sum(1 for row in rows if row.actionability == "unsafe-raw-only"),
        missing_user_input_count=sum(1 for row in rows if row.actionability == "missing-input"),
        ready_to_reopen_domain_count=0,
        source_patch_authorized_count=0,
        next_ticket="TBD",
        next_topic="await-new-safe-evidence-input",
        selected_domain="none",
        selected_pivot="none",
        metadata_work_readiness="blocked",
        code_change_readiness="blocked",
        stop_condition="provide changed upstream mapping or a new safe proof artifact before reopening domain selection",
    )
    return ExplorationBundle(rows=rows, summary=summary)


def write_csv(path: Path, rows: list[object], row_type: type) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(row_type)], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def render_markdown(bundle: ExplorationBundle) -> str:
    lines = [
        "# RE-308 new non-raw proof evidence exploration",
        "",
        "## Summary",
        "",
        "The RE-307 exhaustion handoff is valid: no blocker-reduction metadata source remains ready, no proof domain is selected, and no source patch is authorized.",
        "",
        "No current vector is testable now. The safe continuation requires either a changed upstream mapping export or a newly supplied metadata-only/source-symbolic proof artifact.",
        "",
        "## Exploration vectors",
        "",
    ]
    for row in bundle.rows:
        lines.append(
            f"- `{row.vector_id}`: `{row.actionability}`; observed count `{row.observed_count}`; next input `{row.next_required_input}`."
        )
    lines.extend(
        [
            "",
            "## Readiness decision",
            "",
            "No production source or marker change is authorized. Domain selection stays blocked until a new safe input appears.",
            "",
        ]
    )
    return "\n".join(lines)


def render_story(bundle: ExplorationBundle) -> str:
    summary = bundle.summary
    lines = [
        "# RE-308 new non-raw proof evidence exploration",
        "",
        "## Goal",
        "",
        "Explore the safe continuation path requested after RE-307 by checking whether a changed upstream mapping or new non-raw proof evidence is available before any domain selection.",
        "",
        "## Inputs",
        "",
        f"- Upstream handoff: `{RE307_HANDOFF}`",
        "- Existing generated metadata and story/Markdown taxonomies, counted only as exhausted context.",
        "- Checked-in source-symbolic corpus, counted as context rather than proof readiness.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-307 exhaustion handoff validated.",
        "- [x] Safe exploration vectors enumerated.",
        "- [x] Existing metadata-only context classified as exhausted, not testable-now.",
        "- [x] Unsafe evidence class rejected from committed outputs.",
        "- [x] Source/code readiness remains blocked.",
        "",
        "## Generated artifacts",
        "",
        f"- `{EXPLORATION_CSV}`",
        f"- `{SUMMARY_CSV}`",
        f"- `{HANDOFF_CSV}`",
        f"- `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- Exploration vectors: `{summary.exploration_vector_count}`",
        f"- Testable now: `{summary.testable_now_count}`",
        f"- Need new export: `{summary.needs_new_export_count}`",
        f"- Exhausted metadata: `{summary.exhausted_metadata_count}`",
        f"- Missing user input: `{summary.missing_user_input_count}`",
        f"- Unsafe input class: `{summary.unsafe_raw_only_count}`",
        f"- Ready to reopen proof-domain selection: `{summary.ready_to_reopen_domain_count}`",
        f"- Source patch authorized rows: `{summary.source_patch_authorized_count}`",
        "",
        "## Readiness decision",
        "",
        "The exploration did not find a current testable-now vector. Existing metadata remains exhausted/gated blocked, the source-symbolic corpus is context only, and unsafe evidence classes are rejected. Domain and source readiness remain blocked.",
        "",
        "## Follow-up ticket breakdown",
        "",
        "- `TBD` / `changed-upstream-mapping-refresh`: run only after a changed `repo-function-map.csv` or equivalent priority export is available.",
        "  - Inputs: changed safe mapping/export artifact.",
        "  - Stop condition: no mapping delta keeps selected domain/pivot `none`.",
        "- `TBD` / `new-safe-proof-evidence-intake`: run only after a new metadata-only or source-symbolic proof artifact is supplied.",
        "  - Inputs: safe proof artifact, path, or generated export; no unsafe binary/asset-derived payloads.",
        "  - Stop condition: artifact does not establish an actionable non-raw proof vector.",
        "",
        "## Validation commands",
        "",
        "- `python -m pytest tests/reverse/test_re308_new_non_raw_proof_evidence_exploration.py -q`",
        "- `python scripts/reverse/re308_new_non_raw_proof_evidence_exploration.py --repo .`",
        "- `python -m pytest tests/reverse -q`",
        "",
    ]
    return "\n".join(lines)


def write_all_artifacts(bundle: ExplorationBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "exploration_csv": repo / EXPLORATION_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_csv(paths["exploration_csv"], bundle.rows, ExplorationVector)
    write_csv(paths["summary_csv"], [bundle.summary], ExplorationSummary)
    write_csv(paths["handoff_csv"], [bundle.summary], ExplorationSummary)
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text(render_markdown(bundle), encoding="utf-8")
    paths["story"].parent.mkdir(parents=True, exist_ok=True)
    paths["story"].write_text(render_story(bundle), encoding="utf-8")
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository root")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    bundle = build_new_non_raw_proof_evidence_exploration(repo)
    written = write_all_artifacts(bundle, repo)
    for key, path in written.items():
        print(f"{key}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
