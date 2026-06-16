#!/usr/bin/env python3
"""Generate RE-309 safe Ghidra unmapped bridge candidate artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE308_HANDOFF = "docs/reverse/generated/re308-new-non-raw-proof-evidence-exploration-handoff.csv"
GHIDRA_FUNCTIONS = "docs/reverse/generated/ghidra-functions.csv"
REPO_FUNCTION_MAP = "docs/reverse/generated/repo-function-map.csv"
FUNCTION_MAP_SUMMARY = "docs/reverse/generated/function-map-summary.json"

CANDIDATES_CSV = "docs/reverse/generated/re309-ghidra-unmapped-bridge-candidates.csv"
SUMMARY_CSV = "docs/reverse/generated/re309-ghidra-unmapped-bridge-candidates-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re309-ghidra-unmapped-bridge-candidates-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re309-ghidra-unmapped-bridge-candidates.md"
STORY = "docs/stories/RE-309-ghidra-unmapped-bridge-candidates.md"
TOP_LIMIT = 25

FORBIDDEN_OUTPUT_FRAGMENTS = (
    "0x",
    "fun_",
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

PARSER_ARTIFACT_NAMES = {"if", "for", "while", "switch"}


@dataclass(frozen=True)
class BridgeCandidate:
    rank: int
    candidate_id: str
    bridge_class: str
    actionability: str
    body_size_bucket: str
    caller_count: int
    callee_count: int
    mapped_caller_count: int
    mapped_callee_count: int
    source_file_count: int
    source_context_count: int
    safe_source_context: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    next_gate: str
    stop_condition: str


@dataclass(frozen=True)
class BridgeSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    ghidra_function_count: int
    repo_function_count: int
    mapped_function_count: int
    ghidra_only_function_count: int
    bridge_candidate_count: int
    testable_now_count: int
    top_candidate_count: int
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
class BridgeBundle:
    rows: list[BridgeCandidate]
    summary: BridgeSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def one_row(repo: Path, rel_path: str) -> dict[str, str]:
    rows = read_csv(repo / rel_path)
    if len(rows) != 1:
        raise ValueError(f"{rel_path} must contain exactly one row")
    return rows[0]


def validate_re308_handoff(repo: Path) -> None:
    row = one_row(repo, RE308_HANDOFF)
    expected = {
        "story_id": "RE-308",
        "next_ticket": "TBD",
        "next_topic": "await-new-safe-evidence-input",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "blocked",
        "code_change_readiness": "blocked",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-308 handoff drift: {key}={row.get(key)!r}")


def body_bucket(size_text: str) -> str:
    size = int(size_text or "0")
    if size < 128:
        return "tiny"
    if size < 512:
        return "small"
    if size < 1536:
        return "medium"
    return "large"


def candidate_hash(entry: str, name: str) -> str:
    return hashlib.sha1(f"{entry}|{name}".encode("utf-8")).hexdigest()[:12]


def split_symbols(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def safe_repo_symbol(row: dict[str, str]) -> str | None:
    name = row.get("repo_function", "")
    if not name or name.lower() in PARSER_ARTIFACT_NAMES:
        return None
    file = row.get("file", "")
    module = file.split("/", 1)[0] if "/" in file else file
    return f"{module}:{name}" if module else name


def unique_sorted(values: list[str]) -> list[str]:
    return sorted(dict.fromkeys(values))


def bridge_class(mapped_callers: int, mapped_callees: int) -> str:
    if mapped_callers >= 10:
        return "mapped-caller-heavy"
    if mapped_callers >= 1 and mapped_callees >= 1:
        return "mapped-caller-callee-bridge"
    if mapped_callers >= 1:
        return "mapped-caller-bridge"
    return "mapped-callee-bridge"


def build_bridge_candidates(repo: Path) -> tuple[list[BridgeCandidate], dict[str, int]]:
    ghidra_rows = read_csv(repo / GHIDRA_FUNCTIONS)
    map_rows = read_csv(repo / REPO_FUNCTION_MAP)
    summary_json = json.loads((repo / FUNCTION_MAP_SUMMARY).read_text(encoding="utf-8"))

    mapped_by_entry = {row["ghidra_entry"].lower(): row for row in map_rows if row.get("mapping_status") == "mapped" and row.get("ghidra_entry")}
    mapped_by_name: dict[str, list[dict[str, str]]] = {}
    for row in map_rows:
        if row.get("mapping_status") == "mapped" and row.get("ghidra_name"):
            mapped_by_name.setdefault(row["ghidra_name"], []).append(row)

    all_candidates: list[tuple[tuple[int, int, int, str], BridgeCandidate]] = []
    for ghidra in ghidra_rows:
        if ghidra["entry"].lower() in mapped_by_entry:
            continue
        callers = split_symbols(ghidra.get("callers", ""))
        callees = split_symbols(ghidra.get("called_functions", ""))
        mapped_callers = [row for symbol in callers for row in mapped_by_name.get(symbol, [])]
        mapped_callees = [row for symbol in callees for row in mapped_by_name.get(symbol, [])]
        if not mapped_callers and not mapped_callees:
            continue
        safe_context_values = unique_sorted(
            [value for row in mapped_callers + mapped_callees for value in [safe_repo_symbol(row)] if value]
        )
        source_files = unique_sorted([row.get("file", "") for row in mapped_callers + mapped_callees if row.get("file")])
        if not safe_context_values:
            continue
        mapped_caller_count = len(mapped_callers)
        mapped_callee_count = len(mapped_callees)
        caller_count = len(callers)
        callee_count = len(callees)
        body_size = int(ghidra.get("body_size", "0") or "0")
        candidate = BridgeCandidate(
            rank=0,
            candidate_id=candidate_hash(ghidra["entry"], ghidra["name"]),
            bridge_class=bridge_class(mapped_caller_count, mapped_callee_count),
            actionability="testable-now",
            body_size_bucket=body_bucket(ghidra.get("body_size", "0")),
            caller_count=caller_count,
            callee_count=callee_count,
            mapped_caller_count=mapped_caller_count,
            mapped_callee_count=mapped_callee_count,
            source_file_count=len(source_files),
            source_context_count=len(safe_context_values),
            safe_source_context=";".join(safe_context_values[:8]),
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            next_gate="ghidra-bridge-candidate-readiness-gate",
            stop_condition="gate candidate before selecting domain or patching source",
        )
        bridge_score = mapped_caller_count + mapped_callee_count
        all_candidates.append(((-bridge_score, -body_size, -len(source_files), candidate.candidate_id), candidate))

    all_candidates.sort(key=lambda item: item[0])
    rows = []
    for index, (_, candidate) in enumerate(all_candidates[:TOP_LIMIT], start=1):
        rows.append(BridgeCandidate(rank=index, **{field.name: getattr(candidate, field.name) for field in fields(BridgeCandidate) if field.name != "rank"}))
    counts = {
        "ghidra_function_count": int(summary_json["ghidra_functions"]),
        "repo_function_count": int(summary_json["repo_functions"]),
        "mapped_function_count": int(summary_json["mapped_functions"]),
        "ghidra_only_function_count": int(summary_json["ghidra_only_functions"]),
        "bridge_candidate_count": len(all_candidates),
    }
    return rows, counts


def build_ghidra_unmapped_bridge_candidates(repo: Path) -> BridgeBundle:
    repo = Path(repo)
    validate_re308_handoff(repo)
    rows, counts = build_bridge_candidates(repo)
    summary = BridgeSummary(
        story_id="RE-309",
        topic="ghidra-unmapped-bridge-candidates",
        upstream_handoff="RE-308",
        ghidra_function_count=counts["ghidra_function_count"],
        repo_function_count=counts["repo_function_count"],
        mapped_function_count=counts["mapped_function_count"],
        ghidra_only_function_count=counts["ghidra_only_function_count"],
        bridge_candidate_count=counts["bridge_candidate_count"],
        testable_now_count=len(rows),
        top_candidate_count=len(rows),
        ready_to_reopen_domain_count=0,
        source_patch_authorized_count=0,
        next_ticket="RE-310",
        next_topic="ghidra-bridge-candidate-readiness-gate",
        selected_domain="none",
        selected_pivot="none",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="gate the safe Ghidra bridge candidates before domain selection or source patching",
    )
    return BridgeBundle(rows=rows, summary=summary)


def write_csv(path: Path, rows: list[object], row_type: type) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(row_type)], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def render_markdown(bundle: BridgeBundle) -> str:
    summary = bundle.summary
    lines = [
        "# RE-309 Ghidra unmapped bridge candidates",
        "",
        "## Summary",
        "",
        f"Consumed the Ghidra function export and repo function map to identify `{summary.bridge_candidate_count}` unmapped Ghidra functions that are connected to mapped source symbols.",
        f"The top `{summary.top_candidate_count}` candidates are emitted as safe metadata for the next readiness gate.",
        "",
        "No raw Ghidra function names or entry addresses are emitted in the versioned artifacts; candidate handles are hashed and source context uses repo symbols only.",
        "",
        "## Top bridge classes",
        "",
    ]
    class_counts: dict[str, int] = {}
    for row in bundle.rows:
        class_counts[row.bridge_class] = class_counts.get(row.bridge_class, 0) + 1
    for bridge, count in sorted(class_counts.items()):
        lines.append(f"- `{bridge}`: `{count}`")
    lines.extend(
        [
            "",
            "## Readiness decision",
            "",
            "The export is metadata-ready for a candidate readiness gate. It does not reopen proof-domain selection and does not authorize source or marker patches.",
            "",
        ]
    )
    return "\n".join(lines)


def render_story(bundle: BridgeBundle) -> str:
    summary = bundle.summary
    lines = [
        "# RE-309 Ghidra unmapped bridge candidates",
        "",
        "## Goal",
        "",
        "Use the available Ghidra function export proactively after RE-308 to produce a safe source-symbolic candidate list for further reverse-engineering exploration.",
        "",
        "## Inputs",
        "",
        f"- Upstream handoff: `{RE308_HANDOFF}`",
        f"- Ghidra export: `{GHIDRA_FUNCTIONS}`",
        f"- Repo mapping: `{REPO_FUNCTION_MAP}`",
        f"- Mapping summary: `{FUNCTION_MAP_SUMMARY}`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-308 handoff validated.",
        "- [x] Ghidra function export consumed as source-symbolic metadata.",
        "- [x] Repo mapped symbols joined to unmapped Ghidra caller/callee bridges.",
        "- [x] Raw Ghidra names and entry addresses excluded from versioned candidate rows.",
        "- [x] Source/code readiness remains blocked pending a readiness gate.",
        "",
        "## Generated artifacts",
        "",
        f"- `{CANDIDATES_CSV}`",
        f"- `{SUMMARY_CSV}`",
        f"- `{HANDOFF_CSV}`",
        f"- `{MD_OUTPUT}`",
        "",
        "## Findings",
        "",
        f"- Ghidra functions: `{summary.ghidra_function_count}`",
        f"- Ghidra-only functions: `{summary.ghidra_only_function_count}`",
        f"- Bridge candidates: `{summary.bridge_candidate_count}`",
        f"- Top testable-now candidates emitted: `{summary.testable_now_count}`",
        f"- Ready to reopen proof-domain selection: `{summary.ready_to_reopen_domain_count}`",
        f"- Source patch authorized rows: `{summary.source_patch_authorized_count}`",
        "",
        "## Readiness decision",
        "",
        "The new source-symbolic export is ready for gating, but it is not yet a proof-domain selection. No production source or marker change is authorized.",
        "",
        "## Follow-up ticket breakdown",
        "",
        "- `RE-310` / `ghidra-bridge-candidate-readiness-gate`: gate the top bridge candidates, group them by source-symbolic context, and decide whether one can open a proof-first domain.",
        "  - Inputs: RE-309 candidate CSV plus the existing Ghidra/repo map exports.",
        "  - Stop condition: if every candidate remains generic helper context, keep selected domain/pivot `none` and request a narrower Ghidra export.",
        "",
        "## Validation commands",
        "",
        "- `python -m pytest tests/reverse/test_re309_ghidra_unmapped_bridge_candidates.py -q`",
        "- `python scripts/reverse/re309_ghidra_unmapped_bridge_candidates.py --repo .`",
        "- `python -m pytest tests/reverse -q`",
        "",
    ]
    return "\n".join(lines)


def write_all_artifacts(bundle: BridgeBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "candidates_csv": repo / CANDIDATES_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_csv(paths["candidates_csv"], bundle.rows, BridgeCandidate)
    write_csv(paths["summary_csv"], [bundle.summary], BridgeSummary)
    write_csv(paths["handoff_csv"], [bundle.summary], BridgeSummary)
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
    bundle = build_ghidra_unmapped_bridge_candidates(repo)
    written = write_all_artifacts(bundle, repo)
    for key, path in written.items():
        print(f"{key}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
