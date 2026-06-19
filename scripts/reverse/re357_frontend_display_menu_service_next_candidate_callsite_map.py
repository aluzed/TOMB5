#!/usr/bin/env python3
"""Generate RE-357 source-backed callsite metadata for the next frontend display/menu service candidate."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE356_HANDOFF = "docs/reverse/generated/re356-frontend-display-menu-service-next-candidate-proof-handoff.csv"
RE356_CONTEXTS = "docs/reverse/generated/re356-frontend-display-menu-service-next-candidate-proof-contexts.csv"
FUNCTIONS_CSV = "docs/reverse/generated/re357-frontend-display-menu-service-next-candidate-callsite-functions.csv"
CALLSITES_CSV = "docs/reverse/generated/re357-frontend-display-menu-service-next-candidate-callsite-map.csv"
GATE_CSV = "docs/reverse/generated/re357-frontend-display-menu-service-next-candidate-callsite-gate.csv"
SUMMARY_CSV = "docs/reverse/generated/re357-frontend-display-menu-service-next-candidate-callsite-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re357-frontend-display-menu-service-next-candidate-callsite-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re357-frontend-display-menu-service-next-candidate-callsite-map.md"
STORY = "docs/stories/RE-357-frontend-display-menu-service-next-candidate-callsite-map.md"

PREVIOUS_CANDIDATE_ID = "de919274685f"
SELECTED_CANDIDATE_ID = "4c90c6af8f9d"
CALL_TOKENS = (
    "CDDA_SetMasterVolume",
    "CdInit",
    "CdSetDebug",
    "ClearImage",
    "ClearOTagR",
    "DEL_CDFS_OpenFile",
    "DEL_CDFS_Read",
    "DEL_CDFS_Seek",
    "DoGameflow",
    "DrawOTagEnv",
    "DrawSync",
    "Emulator_Initialise",
    "Emulator_ShutDown",
    "Emulator_StoreFrameBuffer",
    "FILE_Length",
    "FILE_Read",
    "GPU_BeginScene",
    "GPU_ClearVRAM",
    "GPU_EndScene",
    "GPU_FlipToBuffer",
    "GPU_GetScreenPosition",
    "GPU_SyncBothScreens",
    "GPU_UseOrderingTables",
    "GPU_UsePolygonBuffers",
    "GetFloor",
    "GetHeight",
    "InitFont",
    "InitGeom",
    "InitNewCDSystem",
    "InitObjGTE",
    "InitialisePickUpDisplay",
    "LOAD_DrawEnable",
    "LOAD_Start",
    "LOAD_Stop",
    "LoadImage",
    "LoadImagePSX",
    "LoadLevel",
    "MakeMono",
    "MemCardInit",
    "MoveImage",
    "PCclose",
    "PCopen",
    "PadInitDirect",
    "PadSetAct",
    "PadStartCom",
    "PrintString",
    "ProfileAddDrawOT",
    "ProfileAddOT",
    "ProfileInit",
    "ProfileRGB",
    "ProfileStartCount",
    "PutDispEnv",
    "PutDrawEnv",
    "RelocateModule",
    "ResetCallback",
    "ResetGraph",
    "SOUND_Init",
    "SOUND_Stop",
    "SPU_Init",
    "S_CDPause",
    "S_CDRestart",
    "S_DumpScreen",
    "S_LongMemCpy",
    "S_SetReverbType",
    "S_UpdateInput",
    "SetDefDispEnv",
    "SetDefDrawEnv",
    "SetDispMask",
    "SetGraphDebug",
    "SetSp",
    "SoundEffect",
    "StoreImage",
    "TestTriggers",
    "UpdatePulseColour",
    "VSync",
    "VSyncCallback",
    "clear_a_rect",
    "dels_give_lara_guns_cheat",
    "dels_give_lara_items_cheat",
    "do_debounced_joystick_poo",
    "do_examine_mode",
    "do_keypad_mode",
    "do_playstation_button_prompts_v1",
    "do_stats_mode",
    "draw_ammo_selector",
    "draw_current_object_list",
    "draw_outlines",
    "fade_ammo_selector",
    "fclose",
    "fopen",
    "game_free",
    "game_malloc",
    "go_and_load_game",
    "go_and_save_game",
    "handle_inventry_menu",
    "init_game_malloc",
    "init_new_inventry",
    "mcClose",
    "mcOpen",
    "printf",
    "setRECT",
    "setRECT16",
    "strcat",
    "strcpy",
    "strlen",
    "update_laras_weapons_status",
    "use_current_item",
)
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
    "source_line_text",
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
    previous_candidate_id: str
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
    previous_candidate_id: str
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


def validate_re356_handoff(repo: Path) -> None:
    row = one_row(repo, RE356_HANDOFF)
    expected = {
        "story_id": "RE-356",
        "next_ticket": "RE-357",
        "next_topic": "frontend-display-menu-service-next-candidate-callsite-map",
        "selected_candidate_id": SELECTED_CANDIDATE_ID,
        "previous_candidate_id": PREVIOUS_CANDIDATE_ID,
        "source_symbol_context_count": "18",
        "caller_context_count": "18",
        "callee_context_count": "0",
        "candidate_level_proof_count": "0",
        "selected_domain": "none",
        "selected_pivot": "none",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-356 handoff drift: {key}={row.get(key)!r}")


def caller_context_rows(repo: Path) -> list[dict[str, str]]:
    rows = read_csv(repo / RE356_CONTEXTS)
    callers = [
        row
        for row in rows
        if row.get("candidate_id") == SELECTED_CANDIDATE_ID and row.get("context_kind") == "caller"
    ]
    if len(callers) != 18:
        raise ValueError(f"Expected 18 caller context rows, got {len(callers)}")
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
    if callee in {"handle_inventry_menu", "init_new_inventry", "draw_current_object_list", "draw_ammo_selector", "fade_ammo_selector", "InitialisePickUpDisplay", "use_current_item", "update_laras_weapons_status", "go_and_load_game", "go_and_save_game", "do_stats_mode", "do_examine_mode", "do_keypad_mode", "do_playstation_button_prompts_v1", "do_debounced_joystick_poo", "dels_give_lara_guns_cheat", "dels_give_lara_items_cheat"}:
        return "inventory-menu-helper"
    if callee in {"GPU_BeginScene", "GPU_EndScene", "GPU_ClearVRAM", "GPU_FlipToBuffer", "GPU_GetScreenPosition", "GPU_SyncBothScreens", "GPU_UseOrderingTables", "GPU_UsePolygonBuffers", "DrawSync", "VSync", "DrawOTagEnv", "PutDispEnv", "PutDrawEnv", "SetDefDispEnv", "SetDefDrawEnv", "SetDispMask", "ResetGraph", "SetGraphDebug", "InitGeom", "VSyncCallback", "LoadImage", "LoadImagePSX", "StoreImage", "ClearImage", "ClearOTagR", "MoveImage", "MakeMono", "S_LongMemCpy", "clear_a_rect", "setRECT", "setRECT16", "ProfileRGB", "ProfileAddOT", "ProfileAddDrawOT", "ProfileStartCount", "ProfileInit", "InitObjGTE", "GetFloor", "GetHeight", "draw_outlines", "UpdatePulseColour"}:
        return "gpu-display-helper"
    if callee in {"PrintString", "InitFont", "strlen", "strcpy", "strcat"}:
        return "text-ui-helper"
    if callee in {"SOUND_Stop", "SoundEffect", "S_SetReverbType", "S_CDPause", "S_CDRestart", "SOUND_Init", "SPU_Init", "CDDA_SetMasterVolume"}:
        return "audio-sound-helper"
    if callee in {"mcOpen", "mcClose", "MemCardInit"}:
        return "memory-card-helper"
    if callee in {"S_UpdateInput", "PadInitDirect", "PadSetAct", "PadStartCom"}:
        return "input-pad-helper"
    if callee in {"DEL_CDFS_OpenFile", "DEL_CDFS_Read", "DEL_CDFS_Seek", "PCopen", "PCclose", "FILE_Read", "FILE_Length", "fopen", "fclose", "LOAD_Start", "LOAD_Stop", "LOAD_DrawEnable", "LoadLevel", "RelocateModule", "init_game_malloc", "game_malloc", "game_free"}:
        return "level-load-service-helper"
    if callee in {"DoGameflow", "SetSp", "ResetCallback", "CdInit", "CdSetDebug", "InitNewCDSystem", "Emulator_Initialise", "Emulator_ShutDown", "Emulator_StoreFrameBuffer", "TestTriggers"}:
        return "platform-lifecycle-helper"
    if callee in {"S_DumpScreen", "printf"}:
        return "diagnostic-helper"
    return "other"


def function_status(hits: list[tuple[int, str]]) -> str:
    if any(callee == "UNIMPLEMENTED" for _, callee in hits):
        return "stub-unimplemented"
    if hits:
        return "source-with-calls"
    return "source-no-callsite"


def discover_callsite_hits(lines: list[str], start: int, end: int, symbol: str) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    token_pattern = re.compile(r"\b(" + "|".join(re.escape(token) for token in CALL_TOKENS) + r")\s*\(")
    for line_number in range(start + 1, end + 1):
        code = source_code_part(lines[line_number - 1])
        for match in token_pattern.finditer(code):
            token = match.group(1)
            if token == symbol:
                continue
            hits.append((line_number, token))
    return hits


def build_frontend_display_menu_service_next_candidate_callsite_map(repo: Path) -> CallsiteBundle:
    repo = Path(repo)
    validate_re356_handoff(repo)
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
            callsite_rows.append(
                SourceBackedCallsiteRow(
                    rank=len(callsite_rows) + 1,
                    candidate_id=SELECTED_CANDIDATE_ID,
                    caller_symbol=caller_symbol,
                    source_module=source_module,
                    source_file=source_file,
                    source_line=line_number,
                    callee_symbol=callee,
                    callsite_family=callsite_family(callee),
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
    if len(function_rows) != 18 or len(callsite_rows) != 126 or implemented_count != 17 or stub_count != 0 or no_callsite_count != 1:
        raise ValueError("RE-357 callsite scope drift")

    gate_rows = [
        CallsiteGateRow(
            rank=1,
            candidate_id=SELECTED_CANDIDATE_ID,
            previous_candidate_id=PREVIOUS_CANDIDATE_ID,
            source_context_function_count=len(function_rows),
            source_backed_callsite_count=len(callsite_rows),
            implemented_context_function_count=implemented_count,
            stub_context_function_count=stub_count,
            candidate_level_proof_count=0,
            readiness_gate="blocked-next-candidate-callsite-map-needs-readiness-gate",
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            next_ticket="RE-358",
            next_topic="frontend-display-menu-service-next-candidate-callsite-readiness-gate",
            stop_condition="next frontend display/menu candidate has source-backed callsites but still needs a readiness gate before domain selection",
        )
    ]
    summary = CallsiteSummary(
        story_id="RE-357",
        topic="frontend-display-menu-service-next-candidate-callsite-map",
        upstream_handoff="RE-356",
        selected_candidate_id=SELECTED_CANDIDATE_ID,
        previous_candidate_id=PREVIOUS_CANDIDATE_ID,
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
        next_ticket="RE-358",
        next_topic="frontend-display-menu-service-next-candidate-callsite-readiness-gate",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="next frontend display/menu candidate source-backed callsites need a readiness gate before selecting any proof domain or pivot",
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
            "# RE-357 frontend display/menu service next candidate callsite map",
            "",
            "## Summary",
            "",
            f"Mapped `{s.source_backed_callsite_count}` source-backed callsite metadata rows across `{s.source_context_function_count}` candidate context functions.",
            "Source-backed callsite rows are still not source-patch authorization; they are an input to the next readiness gate.",
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
            "Domain and pivot remain `none`; code readiness remains blocked until RE-358 gates the next-candidate callsite map.",
            "",
        ]
    )


def render_story(bundle: CallsiteBundle) -> str:
    s = bundle.summary
    return "\n".join(
        [
            "# RE-357 frontend display/menu service next candidate callsite map",
            "",
            "## Goal",
            "",
            f"Build a source-backed metadata-only callsite map for next candidate `{s.selected_candidate_id}` using RE-356 context rows.",
            "",
            "## Inputs",
            "",
            f"- Upstream handoff: `{RE356_HANDOFF}`",
            f"- Candidate context rows: `{RE356_CONTEXTS}`",
            "- Source files referenced by the context rows.",
            "",
            "## Progress tracker",
            "",
            "- [x] RE-356 next-candidate proof-export handoff validated.",
            "- [x] Caller context function set verified fail-closed.",
            "- [x] Function spans and source-backed callsite line metadata emitted.",
            "- [x] Raw line text and local reverse identity omitted from generated artifacts.",
            "- [x] Next-candidate callsite readiness gate follow-up selected.",
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
            "The next-candidate callsite map is source-backed and metadata-ready, but it is not yet a proof-domain decision. Domain and pivot stay `none`; code readiness remains blocked.",
            "",
            "## Follow-up ticket breakdown",
            "",
            "- `RE-358` / `frontend-display-menu-service-next-candidate-callsite-readiness-gate`: gate the next-candidate source-backed callsite map and decide whether any frontend display/menu callsite family can become a proof pivot.",
            "  - Inputs: RE-357 function/callsite/gate rows.",
            "  - Deliverables: readiness gate rows, selected or denied pivot, and handoff for either source-patch denial or candidate/subcluster exhaustion.",
            "  - Stop condition: if source-backed callsites still do not prove candidate-level behavior, keep source/code readiness blocked.",
            "",
            "## Validation commands",
            "",
            "- `python -m pytest tests/reverse/test_re357_frontend_display_menu_service_next_candidate_callsite_map.py -q`",
            "- `python scripts/reverse/re357_frontend_display_menu_service_next_candidate_callsite_map.py --repo .`",
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
    bundle = build_frontend_display_menu_service_next_candidate_callsite_map(repo)
    written = write_all_artifacts(bundle, repo)
    for key, path in written.items():
        print(f"{key}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
