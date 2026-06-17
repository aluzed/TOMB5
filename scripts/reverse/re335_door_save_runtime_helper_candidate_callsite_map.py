#!/usr/bin/env python3
"""Generate RE-335 source-backed callsite metadata for the door-save-runtime helper candidate."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE334_HANDOFF = "docs/reverse/generated/re334-door-save-runtime-helper-candidate-proof-handoff.csv"
RE334_CONTEXTS = "docs/reverse/generated/re334-door-save-runtime-helper-candidate-proof-contexts.csv"
FUNCTIONS_CSV = "docs/reverse/generated/re335-door-save-runtime-helper-candidate-callsite-functions.csv"
CALLSITES_CSV = "docs/reverse/generated/re335-door-save-runtime-helper-candidate-callsite-map.csv"
GATE_CSV = "docs/reverse/generated/re335-door-save-runtime-helper-candidate-callsite-gate.csv"
SUMMARY_CSV = "docs/reverse/generated/re335-door-save-runtime-helper-candidate-callsite-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re335-door-save-runtime-helper-candidate-callsite-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re335-door-save-runtime-helper-candidate-callsite-map.md"
STORY = "docs/stories/RE-335-door-save-runtime-helper-candidate-callsite-map.md"

SELECTED_CANDIDATE_ID = "f457f2772655"
C_KEYWORD_CALLS = {"if", "for", "while", "switch", "sizeof", "return"}
FUNCTION_PREFIXES = (
    "void ",
    "int ",
    "long ",
    "short ",
    "char ",
    "struct ",
    "static ",
    "BOOL ",
    "unsigned ",
    "signed ",
)
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
    "ghidra_entry",
    "ghidra_name",
    "sub_",
    "unimplemented();",
)


@dataclass(frozen=True)
class CallsiteFunctionRow:
    rank: int
    candidate_id: str
    caller_symbol: str
    source_module: str
    source_file: str
    definition_line: int
    end_line: int
    source_backed_callsite_count: int
    function_status: str
    candidate_level_proof: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    blocker_class: str


@dataclass(frozen=True)
class SourceBackedCallsiteRow:
    rank: int
    candidate_id: str
    caller_symbol: str
    source_module: str
    source_file: str
    source_line: int
    callee_symbol: str
    callsite_family: str
    function_status: str
    candidate_level_proof: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    blocker_class: str


@dataclass(frozen=True)
class CallsiteGateRow:
    rank: int
    candidate_id: str
    source_context_function_count: int
    source_backed_callsite_count: int
    implemented_context_function_count: int
    stub_context_function_count: int
    candidate_level_proof_count: int
    readiness_gate: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    next_ticket: str
    next_topic: str
    stop_condition: str


@dataclass(frozen=True)
class CallsiteSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    selected_candidate_id: str
    source_context_function_count: int
    source_backed_callsite_count: int
    implemented_context_function_count: int
    stub_context_function_count: int
    no_callsite_context_function_count: int
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
class CallsiteBundle:
    function_rows: list[CallsiteFunctionRow]
    callsite_rows: list[SourceBackedCallsiteRow]
    gate_rows: list[CallsiteGateRow]
    summary: CallsiteSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def one_row(repo: Path, rel_path: str) -> dict[str, str]:
    rows = read_csv(repo / rel_path)
    if len(rows) != 1:
        raise ValueError(f"{rel_path} must contain exactly one row")
    return rows[0]


def validate_re334_handoff(repo: Path) -> None:
    row = one_row(repo, RE334_HANDOFF)
    expected = {
        "story_id": "RE-334",
        "next_ticket": "RE-335",
        "next_topic": "door-save-runtime-helper-candidate-callsite-map",
        "selected_candidate_id": SELECTED_CANDIDATE_ID,
        "source_symbol_context_count": "14",
        "caller_context_count": "14",
        "callee_context_count": "0",
        "candidate_level_proof_count": "0",
        "selected_domain": "none",
        "selected_pivot": "none",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-334 handoff drift: {key}={row.get(key)!r}")


def caller_context_rows(repo: Path) -> list[dict[str, str]]:
    rows = read_csv(repo / RE334_CONTEXTS)
    callers = [
        row
        for row in rows
        if row.get("candidate_id") == SELECTED_CANDIDATE_ID and row.get("context_kind") == "caller"
    ]
    if len(callers) != 14:
        raise ValueError(f"Expected 14 caller context rows, got {len(callers)}")
    return callers


def source_code_part(line: str) -> str:
    return line.split("//", 1)[0]


def looks_like_function_definition(line: str, symbol: str) -> bool:
    stripped = line.strip()
    if not re.search(r"\b" + re.escape(symbol) + r"\s*\(", stripped):
        return False
    if stripped.startswith(FUNCTION_PREFIXES):
        return True
    return bool(re.match(r"^[A-Za-z_][\w\s\*]+\b" + re.escape(symbol) + r"\s*\(", stripped))


def find_function_span(lines: list[str], symbol: str) -> tuple[int, int]:
    start: int | None = None
    for index, line in enumerate(lines):
        if looks_like_function_definition(line, symbol):
            start = index
            break
    if start is None:
        raise ValueError(f"Could not find function definition for {symbol}")

    depth = 0
    seen_open = False
    for index in range(start, len(lines)):
        code = source_code_part(lines[index])
        depth += code.count("{")
        if "{" in code:
            seen_open = True
        depth -= code.count("}")
        if seen_open and depth <= 0:
            return start + 1, index + 1
    raise ValueError(f"Could not close function definition for {symbol}")


def callsite_family(callee: str) -> str:
    if callee == "address-derived-helper":
        return "address-derived-symbol-omitted"
    if callee == "UNIMPLEMENTED":
        return "stub-marker"
    if callee in {"SaveLaraData", "SaveLevelData", "sgRestoreGame", "memcpy", "memset", "S_MemCpy"}:
        return "savegame-memory-helper"
    if callee in {"LoadFile", "FILE_Load", "FILE_Length", "game_malloc", "strlen"}:
        return "gameflow-load-helper"
    if callee.startswith("S_CD") or callee.startswith("Cd") or callee in {"DEL_ChangeCDMode", "VSync", "DECODE_BCD"}:
        return "platform-cd-helper"
    if callee in {"fopen", "fread", "fseek", "ftell", "fclose", "assert", "sprintf", "eprintf"}:
        return "platform-file-helper"
    if callee in {"CalculateCamera", "AlterFOV", "SetFadeClip", "SetScreenFadeIn", "SetScreenFadeOut", "Spline", "phd_sqrt_asm", "phd_QuickW2VMatrix", "phd_LookAt"}:
        return "camera-runtime-helper"
    if callee in {"GetFloor", "GetCollisionInfo", "ShiftItem", "LaraTestWaterDepth", "IsRoomOutside", "TestTriggersAtXYZ"}:
        return "collision-trigger-helper"
    if callee in {"S_LoadLevelFile", "InitialiseFXArray", "InitialiseLOTarray", "ClearFXFogBulbs", "InitSpotCamSequences", "InitialisePickUpDisplay", "S_InitialiseScreen", "InitialiseCamera", "ControlPhase", "QuickControlPhase", "DrawPhaseGame", "handle_cutseq_triggering"}:
        return "level-runtime-helper"
    if callee in {"SoundEffect", "SOUND_Stop", "S_SoundStopAllSamples"}:
        return "audio-helper"
    if callee in {"LaraBurn", "CreateItem", "GetRandomControl", "ANGLE", "ABS", "SIN"}:
        return "lara-state-helper"
    if callee in {"GPU_BeginScene", "phd_InitWindow", "PrintString", "show_game_malloc_totals", "S_CallInventory2", "S_PlayFMV", "InitCutPlayed", "CheckCutPlayed", "SetFade"}:
        return "frontend-runtime-helper"
    return "other"


def safe_callee_symbol(callee: str) -> str:
    if re.fullmatch(r"sub_[0-9A-Fa-f]+", callee):
        return "address-derived-helper"
    return callee


def function_status(hits: list[tuple[int, str]]) -> str:
    if any(callee == "UNIMPLEMENTED" for _, callee in hits):
        return "stub-unimplemented"
    if hits:
        return "source-with-calls"
    return "source-no-callsite"


def discover_callsite_hits(lines: list[str], start: int, end: int, symbol: str) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    for line_number in range(start + 1, end + 1):
        code = source_code_part(lines[line_number - 1])
        for match in re.finditer(r"\b([A-Za-z_]\w*)\s*\(", code):
            token = match.group(1)
            if token in C_KEYWORD_CALLS or token == symbol:
                continue
            hits.append((line_number, token))
    return hits


def build_door_save_runtime_helper_candidate_callsite_map(repo: Path) -> CallsiteBundle:
    repo = Path(repo)
    validate_re334_handoff(repo)
    contexts = caller_context_rows(repo)

    function_rows: list[CallsiteFunctionRow] = []
    callsite_rows: list[SourceBackedCallsiteRow] = []
    for context in contexts:
        source_file = context["source_file"]
        source_module = context["source_module"]
        caller_symbol = context["source_symbol"]
        lines = (repo / source_file).read_text(encoding="utf-8", errors="ignore").splitlines()
        definition_line, end_line = find_function_span(lines, caller_symbol)
        hits = discover_callsite_hits(lines, definition_line, end_line, caller_symbol)
        status = function_status(hits)
        function_rows.append(
            CallsiteFunctionRow(
                rank=len(function_rows) + 1,
                candidate_id=SELECTED_CANDIDATE_ID,
                caller_symbol=caller_symbol,
                source_module=source_module,
                source_file=source_file,
                definition_line=definition_line,
                end_line=end_line,
                source_backed_callsite_count=len(hits),
                function_status=status,
                candidate_level_proof="no",
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                blocker_class="callsite-map-not-yet-gated",
            )
        )
        for line_number, callee in hits:
            safe_callee = safe_callee_symbol(callee)
            callsite_rows.append(
                SourceBackedCallsiteRow(
                    rank=len(callsite_rows) + 1,
                    candidate_id=SELECTED_CANDIDATE_ID,
                    caller_symbol=caller_symbol,
                    source_module=source_module,
                    source_file=source_file,
                    source_line=line_number,
                    callee_symbol=safe_callee,
                    callsite_family=callsite_family(safe_callee),
                    function_status=status,
                    candidate_level_proof="no",
                    ready_to_reopen_domain="no",
                    source_patch_authorized="no",
                    blocker_class="source-backed-callsite-needs-readiness-gate",
                )
            )

    implemented_count = sum(row.function_status == "source-with-calls" for row in function_rows)
    stub_count = sum(row.function_status == "stub-unimplemented" for row in function_rows)
    no_callsite_count = sum(row.function_status == "source-no-callsite" for row in function_rows)
    if len(function_rows) != 14 or len(callsite_rows) != 185 or implemented_count != 13 or stub_count != 1 or no_callsite_count != 0:
        raise ValueError("RE-335 callsite scope drift")

    gate_rows = [
        CallsiteGateRow(
            rank=1,
            candidate_id=SELECTED_CANDIDATE_ID,
            source_context_function_count=len(function_rows),
            source_backed_callsite_count=len(callsite_rows),
            implemented_context_function_count=implemented_count,
            stub_context_function_count=stub_count,
            candidate_level_proof_count=0,
            readiness_gate="blocked-callsite-map-needs-readiness-gate",
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            next_ticket="RE-336",
            next_topic="door-save-runtime-helper-callsite-readiness-gate",
            stop_condition="source-backed callsites exist but still need a readiness gate before domain selection",
        )
    ]
    summary = CallsiteSummary(
        story_id="RE-335",
        topic="door-save-runtime-helper-candidate-callsite-map",
        upstream_handoff="RE-334",
        selected_candidate_id=SELECTED_CANDIDATE_ID,
        source_context_function_count=len(function_rows),
        source_backed_callsite_count=len(callsite_rows),
        implemented_context_function_count=implemented_count,
        stub_context_function_count=stub_count,
        no_callsite_context_function_count=no_callsite_count,
        candidate_level_proof_count=0,
        ready_to_reopen_domain_count=0,
        source_patch_authorized_count=0,
        selected_domain="none",
        selected_pivot="none",
        next_ticket="RE-336",
        next_topic="door-save-runtime-helper-callsite-readiness-gate",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="source-backed callsites need a readiness gate before selecting any proof domain or pivot",
    )
    return CallsiteBundle(function_rows=function_rows, callsite_rows=callsite_rows, gate_rows=gate_rows, summary=summary)


def write_csv(path: Path, rows: list[object], row_type: type) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(row_type)], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def render_markdown(bundle: CallsiteBundle) -> str:
    s = bundle.summary
    return "\n".join(
        [
            "# RE-335 door-save-runtime helper candidate callsite map",
            "",
            "## Summary",
            "",
            f"Mapped `{s.source_backed_callsite_count}` source-backed callsite metadata rows across `{s.source_context_function_count}` candidate context functions.",
            "Source-backed callsite rows are not source-patch authorization; they are an input to the next readiness gate.",
            "",
            "## Counts",
            "",
            f"- implemented context functions: `{s.implemented_context_function_count}`",
            f"- stub context functions: `{s.stub_context_function_count}`",
            f"- no-callsite context functions: `{s.no_callsite_context_function_count}`",
            f"- candidate-level proof rows: `{s.candidate_level_proof_count}`",
            "",
            "## Readiness decision",
            "",
            "Domain and pivot remain `none`; code readiness remains blocked until RE-336 gates the callsite map.",
            "",
        ]
    )


def render_story(bundle: CallsiteBundle) -> str:
    s = bundle.summary
    return "\n".join(
        [
            "# RE-335 door-save-runtime helper candidate callsite map",
            "",
            "## Goal",
            "",
            f"Build a source-backed metadata-only callsite map for candidate `{s.selected_candidate_id}` using RE-334 context rows.",
            "",
            "## Inputs",
            "",
            f"- Upstream handoff: `{RE334_HANDOFF}`",
            f"- Candidate context rows: `{RE334_CONTEXTS}`",
            "- Source files referenced by the context rows.",
            "",
            "## Progress tracker",
            "",
            "- [x] RE-334 proof-export handoff validated.",
            "- [x] Caller context function set verified fail-closed.",
            "- [x] Function spans and source-backed callsite line metadata emitted.",
            "- [x] Raw line text and local reverse identity omitted from generated artifacts.",
            "- [x] Callsite readiness gate follow-up selected.",
            "",
            "## Generated artifacts",
            "",
            f"- `{FUNCTIONS_CSV}`",
            f"- `{CALLSITES_CSV}`",
            f"- `{GATE_CSV}`",
            f"- `{SUMMARY_CSV}`",
            f"- `{HANDOFF_CSV}`",
            f"- `{MD_OUTPUT}`",
            "",
            "## Findings",
            "",
            f"- Source context functions: `{s.source_context_function_count}`",
            f"- Source-backed callsite rows: `{s.source_backed_callsite_count}`",
            f"- Implemented context functions: `{s.implemented_context_function_count}`",
            f"- Stub context functions: `{s.stub_context_function_count}`",
            f"- No-callsite context functions: `{s.no_callsite_context_function_count}`",
            f"- Candidate-level proof rows: `{s.candidate_level_proof_count}`",
            f"- Ready to reopen domain selection: `{s.ready_to_reopen_domain_count}`",
            f"- Source patch authorized rows: `{s.source_patch_authorized_count}`",
            "",
            "## Readiness decision",
            "",
            "The callsite map is source-backed and metadata-ready, but it is not yet a proof-domain decision. Domain and pivot stay `none`; code readiness remains blocked.",
            "",
            "## Follow-up ticket breakdown",
            "",
            "- `RE-336` / `door-save-runtime-helper-callsite-readiness-gate`: gate the source-backed callsite map and decide whether any callsite family can become a proof pivot.",
            "  - Inputs: RE-335 function/callsite/gate rows.",
            "  - Deliverables: readiness gate rows, selected or denied pivot, and handoff for either source-patch denial or narrow-queue exhaustion.",
            "  - Stop condition: if source-backed callsites still do not prove candidate-level behavior, keep source/code readiness blocked.",
            "",
            "## Validation commands",
            "",
            "- `python -m pytest tests/reverse/test_re335_door_save_runtime_helper_candidate_callsite_map.py -q`",
            "- `python scripts/reverse/re335_door_save_runtime_helper_candidate_callsite_map.py --repo .`",
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


def write_all_artifacts(bundle: CallsiteBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "functions_csv": repo / FUNCTIONS_CSV,
        "callsites_csv": repo / CALLSITES_CSV,
        "gate_csv": repo / GATE_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_csv(paths["functions_csv"], bundle.function_rows, CallsiteFunctionRow)
    write_csv(paths["callsites_csv"], bundle.callsite_rows, SourceBackedCallsiteRow)
    write_csv(paths["gate_csv"], bundle.gate_rows, CallsiteGateRow)
    write_csv(paths["summary_csv"], [bundle.summary], CallsiteSummary)
    write_csv(paths["handoff_csv"], [bundle.summary], CallsiteSummary)
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
    bundle = build_door_save_runtime_helper_candidate_callsite_map(repo)
    written = write_all_artifacts(bundle, repo)
    for key, path in written.items():
        print(f"{key}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
