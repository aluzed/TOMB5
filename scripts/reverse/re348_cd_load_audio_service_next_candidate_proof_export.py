#!/usr/bin/env python3
"""Generate RE-348 next-candidate proof metadata for the cd/load/audio service."""

from __future__ import annotations

import argparse
import csv
import hashlib
from collections import defaultdict
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE347_HANDOFF = "docs/reverse/generated/re347-cd-load-audio-service-callsite-readiness-handoff.csv"
RE344_CANDIDATES = "docs/reverse/generated/re344-cd-load-audio-service-readiness-gate-candidates.csv"
GHIDRA_FUNCTIONS = "docs/reverse/generated/ghidra-functions.csv"
REPO_FUNCTION_MAP = "docs/reverse/generated/repo-function-map.csv"
CONTEXTS_CSV = "docs/reverse/generated/re348-cd-load-audio-service-next-candidate-proof-contexts.csv"
PROOF_CSV = "docs/reverse/generated/re348-cd-load-audio-service-next-candidate-proof-gate.csv"
SUMMARY_CSV = "docs/reverse/generated/re348-cd-load-audio-service-next-candidate-proof-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re348-cd-load-audio-service-next-candidate-proof-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re348-cd-load-audio-service-next-candidate-proof-export.md"
STORY = "docs/stories/RE-348-cd-load-audio-service-next-candidate-proof-export.md"

FORBIDDEN_OUTPUT_FRAGMENTS = (
    "0x",
    "fun_",
    "sub_",
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
    "ghidra_entry",
    "ghidra_name",
    "source_line_text",
    "unimplemented();",
)

PREVIOUS_CANDIDATE_ID = "1e35f3f4fb97"
SELECTED_CANDIDATE_ID = "653df7c5909b"
PARSER_ARTIFACT_NAMES = {"if", "for", "while", "switch"}


@dataclass(frozen=True)
class CandidateProofContextRow:
    rank: int
    candidate_id: str
    context_kind: str
    source_symbol: str
    source_module: str
    source_file: str
    cd_load_audio_role: str
    context_family: str
    candidate_level_proof: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    blocker_class: str


@dataclass(frozen=True)
class CandidateProofGateRow:
    rank: int
    candidate_id: str
    previous_candidate_id: str
    source_symbol_context_count: int
    caller_context_count: int
    callee_context_count: int
    direct_repo_symbol_count: int
    candidate_level_proof_count: int
    proof_gate: str
    candidate_level_proof: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    next_ticket: str
    next_topic: str
    stop_condition: str


@dataclass(frozen=True)
class CandidateProofSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    selected_candidate_id: str
    previous_candidate_id: str
    source_symbol_context_count: int
    caller_context_count: int
    callee_context_count: int
    direct_repo_symbol_count: int
    candidate_level_proof_count: int
    ready_to_reopen_domain_count: int
    source_patch_authorized_count: int
    selected_domain: str
    selected_pivot: str
    next_ticket: str
    next_topic: str
    metadata_work_readiness: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class CandidateProofBundle:
    context_rows: list[CandidateProofContextRow]
    proof_rows: list[CandidateProofGateRow]
    summary: CandidateProofSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def one_row(repo: Path, rel_path: str) -> dict[str, str]:
    rows = read_csv(repo / rel_path)
    if len(rows) != 1:
        raise ValueError(f"{rel_path} must contain exactly one row")
    return rows[0]


def validate_re347_handoff(repo: Path) -> None:
    row = one_row(repo, RE347_HANDOFF)
    expected = {
        "story_id": "RE-347",
        "next_ticket": "RE-348",
        "next_topic": "cd-load-audio-service-next-candidate-proof-export",
        "selected_candidate_id": PREVIOUS_CANDIDATE_ID,
        "next_candidate_id": SELECTED_CANDIDATE_ID,
        "candidate_level_proof_count": "0",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "selected_domain": "none",
        "selected_pivot": "none",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-347 handoff drift: {key}={row.get(key)!r}")


def validate_re344_candidate(repo: Path) -> None:
    rows = read_csv(repo / RE344_CANDIDATES)
    candidate_ids = [row.get("candidate_id") for row in rows]
    if candidate_ids != [PREVIOUS_CANDIDATE_ID, SELECTED_CANDIDATE_ID]:
        raise ValueError(f"RE-344 candidate order drift: {candidate_ids!r}")
    row = rows[1]
    expected = {
        "candidate_id": SELECTED_CANDIDATE_ID,
        "selected_narrow_subcluster": "cd-load-audio-service",
        "next_probe": "defer-after-re345",
        "ready_to_reopen_domain": "no",
        "source_patch_authorized": "no",
        "readiness_gate": "blocked-needs-candidate-level-proof",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-344 next candidate drift: {key}={row.get(key)!r}")


def candidate_hash(entry: str, name: str) -> str:
    return hashlib.sha1(f"{entry}|{name}".encode("utf-8")).hexdigest()[:12]


def split_symbols(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def module_from_file(file_name: str) -> str:
    return file_name.split("/", 1)[0] if "/" in file_name else file_name


def safe_symbol(row: dict[str, str]) -> str | None:
    symbol = row.get("repo_function", "")
    if not symbol or symbol.lower() in PARSER_ARTIFACT_NAMES:
        return None
    return symbol


def unique_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    result: list[dict[str, str]] = []
    for row in rows:
        symbol = safe_symbol(row)
        if not symbol:
            continue
        key = (row.get("file", ""), symbol)
        if key not in seen:
            seen.add(key)
            result.append(row)
    return sorted(result, key=lambda row: (row.get("file", ""), row.get("repo_function", "")))


def family_from_symbol(symbol: str) -> str:
    lowered = symbol.lower()
    if "cdfs" in lowered or "cd" in lowered or "audio" in lowered or "synced" in lowered:
        return "cd-audio-service"
    if "load" in lowered:
        return "level-load-service"
    if "fmv" in lowered or "movie" in lowered:
        return "movie-playback"
    if "gpu" in lowered:
        return "gpu-display"
    if "mc" in lowered or "mem" in lowered:
        return "memory-card"
    if lowered == "main":
        return "platform-entry"
    return "other"


def cd_load_audio_role(kind: str, symbol: str) -> str:
    family = family_from_symbol(symbol)
    if family == "cd-audio-service":
        return "cd-audio-caller" if kind == "caller" else "cd-audio-callee"
    if family == "level-load-service":
        return "level-load-caller" if kind == "caller" else "level-load-callee"
    if family == "movie-playback":
        return "movie-playback-context" if kind == "caller" else "movie-playback-callee"
    if family == "gpu-display":
        return "gpu-display-context" if kind == "caller" else "gpu-display-callee"
    if family == "memory-card":
        return "memory-card-context" if kind == "caller" else "memory-card-callee"
    if family == "platform-entry":
        return "platform-entry-context" if kind == "caller" else "platform-entry-callee"
    return f"{kind}-context"


def selected_candidate_context(repo: Path) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    ghidra_rows = read_csv(repo / GHIDRA_FUNCTIONS)
    map_rows = read_csv(repo / REPO_FUNCTION_MAP)
    selected = [row for row in ghidra_rows if candidate_hash(row["entry"], row["name"]) == SELECTED_CANDIDATE_ID]
    if len(selected) != 1:
        raise ValueError("Selected next candidate identity drift")
    candidate_row = selected[0]

    mapped_by_name: dict[str, list[dict[str, str]]] = defaultdict(list)
    direct_repo_symbol_count = 0
    for row in map_rows:
        if row.get("mapping_status") == "mapped" and row.get("ghidra_name"):
            mapped_by_name[row["ghidra_name"]].append(row)
            if row["ghidra_name"] == candidate_row["name"] and safe_symbol(row):
                direct_repo_symbol_count += 1
    if direct_repo_symbol_count != 0:
        raise ValueError("Selected next candidate unexpectedly has direct repo symbol proof")

    callers = unique_rows([row for symbol in split_symbols(candidate_row.get("callers", "")) for row in mapped_by_name.get(symbol, [])])
    callees = unique_rows([row for symbol in split_symbols(candidate_row.get("called_functions", "")) for row in mapped_by_name.get(symbol, [])])
    if len(callers) != 18 or len(callees) != 0:
        raise ValueError(f"Expected 18 caller and 0 callee contexts, got {len(callers)} and {len(callees)}")
    return callers, callees


def build_context_rows(callers: list[dict[str, str]], callees: list[dict[str, str]]) -> list[CandidateProofContextRow]:
    rows: list[CandidateProofContextRow] = []
    for kind, source_rows in [("caller", callers), ("callee", callees)]:
        for source_row in source_rows:
            symbol = safe_symbol(source_row)
            if symbol is None:
                continue
            rows.append(
                CandidateProofContextRow(
                    rank=len(rows) + 1,
                    candidate_id=SELECTED_CANDIDATE_ID,
                    context_kind=kind,
                    source_symbol=symbol,
                    source_module=module_from_file(source_row.get("file", "")),
                    source_file=source_row.get("file", ""),
                    cd_load_audio_role=cd_load_audio_role(kind, symbol),
                    context_family=family_from_symbol(symbol),
                    candidate_level_proof="no",
                    ready_to_reopen_domain="no",
                    source_patch_authorized="no",
                    blocker_class="mapped-context-not-direct-candidate-proof",
                )
            )
    return rows


def build_cd_load_audio_service_next_candidate_proof_export(repo: Path) -> CandidateProofBundle:
    repo = Path(repo)
    validate_re347_handoff(repo)
    validate_re344_candidate(repo)
    callers, callees = selected_candidate_context(repo)
    context_rows = build_context_rows(callers, callees)
    caller_context_count = sum(1 for row in context_rows if row.context_kind == "caller")
    callee_context_count = sum(1 for row in context_rows if row.context_kind == "callee")
    proof_rows = [
        CandidateProofGateRow(
            rank=1,
            candidate_id=SELECTED_CANDIDATE_ID,
            previous_candidate_id=PREVIOUS_CANDIDATE_ID,
            source_symbol_context_count=len(context_rows),
            caller_context_count=caller_context_count,
            callee_context_count=callee_context_count,
            direct_repo_symbol_count=0,
            candidate_level_proof_count=0,
            proof_gate="blocked-unmapped-candidate-identity",
            candidate_level_proof="no",
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            next_ticket="RE-349",
            next_topic="cd-load-audio-service-next-candidate-callsite-map",
            stop_condition="next cd/load/audio candidate still lacks direct repo symbol proof; build a source-backed callsite map next",
        )
    ]
    summary = CandidateProofSummary(
        story_id="RE-348",
        topic="cd-load-audio-service-next-candidate-proof-export",
        upstream_handoff="RE-347",
        selected_candidate_id=SELECTED_CANDIDATE_ID,
        previous_candidate_id=PREVIOUS_CANDIDATE_ID,
        source_symbol_context_count=len(context_rows),
        caller_context_count=caller_context_count,
        callee_context_count=callee_context_count,
        direct_repo_symbol_count=0,
        candidate_level_proof_count=0,
        ready_to_reopen_domain_count=0,
        source_patch_authorized_count=0,
        selected_domain="none",
        selected_pivot="none",
        next_ticket="RE-349",
        next_topic="cd-load-audio-service-next-candidate-callsite-map",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="next cd/load/audio candidate-scoped context still lacks direct source-backed proof; build a callsite map next",
    )
    return CandidateProofBundle(context_rows=context_rows, proof_rows=proof_rows, summary=summary)


def write_csv(path: Path, rows: list[object], row_type: type[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(row_type)], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def render_markdown(bundle: CandidateProofBundle) -> str:
    s = bundle.summary
    lines = [
        "# RE-348 cd-load-audio service next candidate proof export",
        "",
        "## Summary",
        "",
        f"Exported `{s.source_symbol_context_count}` source-symbolic context rows for next candidate `{s.selected_candidate_id}` after previous candidate `{s.previous_candidate_id}` stayed blocked.",
        "No proof-domain is reopened by this export; the candidate hash still lacks direct source-backed proof.",
        "",
        "## Proof gate",
        "",
    ]
    for row in bundle.proof_rows:
        lines.append(
            f"- candidate `{row.candidate_id}`: contexts `{row.source_symbol_context_count}`, direct repo symbols `{row.direct_repo_symbol_count}`, gate `{row.proof_gate}`, next `{row.next_topic}`"
        )
    lines.extend(["", "## Context families", ""])
    families = sorted({row.context_family for row in bundle.context_rows})
    for family in families:
        count = sum(1 for row in bundle.context_rows if row.context_family == family)
        lines.append(f"- `{family}`: `{count}` rows")
    lines.extend(
        [
            "",
            "## Readiness decision",
            "",
            "The export is metadata-ready, but source/domain readiness remains blocked until a source-backed callsite map can prove candidate-level behavior without raw binary evidence.",
            "",
        ]
    )
    return "\n".join(lines)


def render_story(bundle: CandidateProofBundle) -> str:
    s = bundle.summary
    return "\n".join(
        [
            "# RE-348 cd-load-audio service next candidate proof export",
            "",
            "## Goal",
            "",
            f"Produce a candidate-scoped metadata-only proof export for deferred cd/load/audio service candidate `{s.selected_candidate_id}` without committing raw local identity.",
            "",
            "## Inputs",
            "",
            f"- Upstream handoff: `{RE347_HANDOFF}`",
            f"- RE-344 candidates: `{RE344_CANDIDATES}`",
            f"- Local function export: `{GHIDRA_FUNCTIONS}`",
            f"- Local repo function map: `{REPO_FUNCTION_MAP}`",
            "",
            "## Progress tracker",
            "",
            "- [x] RE-347 next-candidate handoff validated.",
            "- [x] Deferred RE-344 candidate row verified fail-closed.",
            "- [x] Selected next-candidate context reconstructed inside the generator only.",
            "- [x] Candidate-scoped source-symbolic rows emitted without raw identity columns.",
            "- [x] Domain/pivot/source-patch readiness kept blocked.",
            "- [x] Source-backed next-candidate callsite-map follow-up selected.",
            "",
            "## Generated artifacts",
            "",
            f"- `{CONTEXTS_CSV}`",
            f"- `{PROOF_CSV}`",
            f"- `{SUMMARY_CSV}`",
            f"- `{HANDOFF_CSV}`",
            f"- `{MD_OUTPUT}`",
            "",
            "## Findings",
            "",
            f"- Selected candidate id: `{s.selected_candidate_id}`",
            f"- Previous candidate id: `{s.previous_candidate_id}`",
            f"- Source-symbolic context rows: `{s.source_symbol_context_count}`",
            f"- Caller context rows: `{s.caller_context_count}`",
            f"- Callee context rows: `{s.callee_context_count}`",
            f"- Direct repo symbol rows: `{s.direct_repo_symbol_count}`",
            f"- Candidate-level proof rows: `{s.candidate_level_proof_count}`",
            f"- Ready to reopen domain selection: `{s.ready_to_reopen_domain_count}`",
            f"- Source patch authorized rows: `{s.source_patch_authorized_count}`",
            "",
            "## Readiness decision",
            "",
            "The next candidate has useful source-symbolic caller context across cd/audio and movie playback modules, but no direct source-backed candidate proof. Domain and pivot remain `none`, and code readiness remains blocked.",
            "",
            "## Follow-up ticket breakdown",
            "",
            f"- `RE-349` / `cd-load-audio-service-next-candidate-callsite-map`: build a source-backed callsite map for candidate `{s.selected_candidate_id}`.",
            "  - Inputs: RE-348 context/proof rows plus local source files and repo map metadata.",
            "  - Deliverables: source-backed callsite rows with file/line references, proof/blocker rows, and a handoff that either selects a proof pivot or marks the cd/load/audio candidate queue exhausted.",
            "  - Stop condition: if source-backed callsites cannot prove candidate-level behavior without raw evidence, keep source/code readiness blocked and close or reprioritize from the parent queue.",
            "",
            "## Validation commands",
            "",
            "- `python -m pytest tests/reverse/test_re348_cd_load_audio_service_next_candidate_proof_export.py -q`",
            "- `python scripts/reverse/re348_cd_load_audio_service_next_candidate_proof_export.py --repo .`",
            "- `python -m pytest tests/reverse -q`",
            "",
        ]
    )


def assert_metadata_only(paths: dict[str, Path]) -> None:
    for path in paths.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            if fragment in text:
                raise ValueError(f"Forbidden output fragment {fragment!r} in {path}")


def write_all_artifacts(bundle: CandidateProofBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "contexts_csv": repo / CONTEXTS_CSV,
        "proof_csv": repo / PROOF_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_csv(paths["contexts_csv"], bundle.context_rows, CandidateProofContextRow)
    write_csv(paths["proof_csv"], bundle.proof_rows, CandidateProofGateRow)
    write_csv(paths["summary_csv"], [bundle.summary], CandidateProofSummary)
    write_csv(paths["handoff_csv"], [bundle.summary], CandidateProofSummary)
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text(render_markdown(bundle), encoding="utf-8")
    paths["story"].parent.mkdir(parents=True, exist_ok=True)
    paths["story"].write_text(render_story(bundle), encoding="utf-8")
    assert_metadata_only(paths)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository root")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    bundle = build_cd_load_audio_service_next_candidate_proof_export(repo)
    written = write_all_artifacts(bundle, repo)
    for key, path in written.items():
        print(f"{key}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
