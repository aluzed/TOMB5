#!/usr/bin/env python3
"""Generate RE-330 source-backed callsite metadata for the weapon-switch-effect helper candidate."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE329_HANDOFF = "docs/reverse/generated/re329-weapon-switch-effect-helper-candidate-proof-handoff.csv"
RE329_CONTEXTS = "docs/reverse/generated/re329-weapon-switch-effect-helper-candidate-proof-contexts.csv"
FUNCTIONS_CSV = "docs/reverse/generated/re330-weapon-switch-effect-helper-candidate-callsite-functions.csv"
CALLSITES_CSV = "docs/reverse/generated/re330-weapon-switch-effect-helper-candidate-callsite-map.csv"
GATE_CSV = "docs/reverse/generated/re330-weapon-switch-effect-helper-candidate-callsite-gate.csv"
SUMMARY_CSV = "docs/reverse/generated/re330-weapon-switch-effect-helper-candidate-callsite-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re330-weapon-switch-effect-helper-candidate-callsite-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re330-weapon-switch-effect-helper-candidate-callsite-map.md"
STORY = "docs/stories/RE-330-weapon-switch-effect-helper-candidate-callsite-map.md"

SELECTED_CANDIDATE_ID = "1ddbda046e37"
CALL_TOKENS = (
    "UNIMPLEMENTED",
    "FireWeapon",
    "HitTarget",
    "SoundEffect",
    "AddActiveItem",
    "ExplodeItemNode",
    "GetFloor",
    "GetHeight",
    "GetSwitchTrigger",
    "LOS",
    "ProcessExplodingSwitchType8",
    "ShatterObject",
    "SmashObject",
    "TestTriggers",
    "SetupPadVibration",
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


def validate_re329_handoff(repo: Path) -> None:
    row = one_row(repo, RE329_HANDOFF)
    expected = {
        "story_id": "RE-329",
        "next_ticket": "RE-330",
        "next_topic": "weapon-switch-effect-helper-candidate-callsite-map",
        "selected_candidate_id": SELECTED_CANDIDATE_ID,
        "source_symbol_context_count": "17",
        "caller_context_count": "1",
        "callee_context_count": "16",
        "candidate_level_proof_count": "0",
        "selected_domain": "none",
        "selected_pivot": "none",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-329 handoff drift: {key}={row.get(key)!r}")


def caller_context_rows(repo: Path) -> list[dict[str, str]]:
    rows = read_csv(repo / RE329_CONTEXTS)
    callers = [row for row in rows if row.get("candidate_id") == SELECTED_CANDIDATE_ID and row.get("context_kind") == "caller"]
    if len(callers) != 1:
        raise ValueError(f"Expected 1 caller context row, got {len(callers)}")
    return callers


def find_function_span(lines: list[str], symbol: str) -> tuple[int, int]:
    start: int | None = None
    pattern = re.compile(r"\b" + re.escape(symbol) + r"\s*\(")
    for index, line in enumerate(lines):
        if pattern.search(line) and line.strip().startswith(("void ", "int ", "long ", "short ", "char ", "struct ", "static ")):
            start = index
            break
    if start is None:
        raise ValueError(f"Could not find function definition for {symbol}")

    depth = 0
    seen_open = False
    for index in range(start, len(lines)):
        depth += lines[index].count("{")
        if "{" in lines[index]:
            seen_open = True
        depth -= lines[index].count("}")
        if seen_open and depth <= 0:
            return start + 1, index + 1
    raise ValueError(f"Could not close function definition for {symbol}")


def callsite_family(callee: str) -> str:
    if callee == "UNIMPLEMENTED":
        return "stub-marker"
    if callee in {"FireWeapon", "HitTarget"}:
        return "weapon-helper"
    if callee in {"SoundEffect", "ExplodeItemNode", "ShatterObject", "SmashObject"}:
        return "effect-helper"
    if callee in {"GetSwitchTrigger", "ProcessExplodingSwitchType8"}:
        return "switch-helper"
    if callee in {"GetFloor", "GetHeight", "LOS"}:
        return "collision-geometry-helper"
    if callee == "AddActiveItem":
        return "item-activation-helper"
    if callee == "SetupPadVibration":
        return "platform-feedback-helper"
    if callee == "TestTriggers":
        return "trigger-helper"
    return "other"


def function_status(hits: list[tuple[int, str]]) -> str:
    if any(callee == "UNIMPLEMENTED" for _, callee in hits):
        return "stub-unimplemented"
    if hits:
        return "source-with-calls"
    return "source-no-callsite"


def discover_callsite_hits(lines: list[str], start: int, end: int) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    for line_number in range(start + 1, end + 1):
        line = lines[line_number - 1]
        for token in CALL_TOKENS:
            if re.search(r"\b" + re.escape(token) + r"\s*\(", line):
                hits.append((line_number, token))
    return hits


def build_weapon_switch_effect_helper_candidate_callsite_map(repo: Path) -> CallsiteBundle:
    repo = Path(repo)
    validate_re329_handoff(repo)
    contexts = caller_context_rows(repo)

    function_rows: list[CallsiteFunctionRow] = []
    callsite_rows: list[SourceBackedCallsiteRow] = []
    for context in contexts:
        source_file = context["source_file"]
        source_module = context["source_module"]
        caller_symbol = context["source_symbol"]
        lines = (repo / source_file).read_text(encoding="utf-8", errors="ignore").splitlines()
        definition_line, end_line = find_function_span(lines, caller_symbol)
        hits = discover_callsite_hits(lines, definition_line, end_line)
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
    if len(callsite_rows) != 1 or implemented_count != 0 or stub_count != 1 or no_callsite_count != 0:
        raise ValueError("RE-330 callsite scope drift")

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
            next_ticket="RE-331",
            next_topic="weapon-switch-effect-helper-callsite-readiness-gate",
            stop_condition="source-backed callsites exist but still need a readiness gate before domain selection",
        )
    ]
    summary = CallsiteSummary(
        story_id="RE-330",
        topic="weapon-switch-effect-helper-candidate-callsite-map",
        upstream_handoff="RE-329",
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
        next_ticket="RE-331",
        next_topic="weapon-switch-effect-helper-callsite-readiness-gate",
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
            "# RE-330 weapon-switch-effect helper candidate callsite map",
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
            "Domain and pivot remain `none`; code readiness remains blocked until RE-331 gates the callsite map.",
            "",
        ]
    )


def render_story(bundle: CallsiteBundle) -> str:
    s = bundle.summary
    return "\n".join(
        [
            "# RE-330 weapon-switch-effect helper candidate callsite map",
            "",
            "## Goal",
            "",
            f"Build a source-backed metadata-only callsite map for candidate `{s.selected_candidate_id}` using RE-329 context rows.",
            "",
            "## Inputs",
            "",
            f"- Upstream handoff: `{RE329_HANDOFF}`",
            f"- Candidate context rows: `{RE329_CONTEXTS}`",
            "- Source files referenced by the context rows.",
            "",
            "## Progress tracker",
            "",
            "- [x] RE-329 callsite-map handoff validated.",
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
            "- `RE-331` / `weapon-switch-effect-helper-callsite-readiness-gate`: gate the source-backed callsite map and decide whether any callsite family can become a proof pivot.",
            "  - Inputs: RE-330 function/callsite/gate rows.",
            "  - Deliverables: readiness gate rows, selected or denied pivot, handoff for either source-patch denial or remaining candidate deferral.",
            "  - Stop condition: if implemented source callsites still do not prove candidate-level behavior, keep source/code readiness blocked.",
            "",
            "## Validation commands",
            "",
            "- `python -m pytest tests/reverse/test_re330_weapon_switch_effect_helper_candidate_callsite_map.py -q`",
            "- `python scripts/reverse/re330_weapon_switch_effect_helper_candidate_callsite_map.py --repo .`",
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
    bundle = build_weapon_switch_effect_helper_candidate_callsite_map(repo)
    written = write_all_artifacts(bundle, repo)
    for key, path in written.items():
        print(f"{key}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
