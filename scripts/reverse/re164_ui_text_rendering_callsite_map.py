#!/usr/bin/env python3
"""Generate RE-164 UI text rendering caller/side-effect map artifacts."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path

RE163_PLAN_CSV = "docs/reverse/generated/re163-module-spec-psxpc-n-ticket-plan.csv"
RE163_AUDIT_CSV = "docs/reverse/generated/re163-module-spec-psxpc-n-proof-first-audit.csv"
SCOPE_CSV = "docs/reverse/generated/re164-ui-text-rendering-scope.csv"
CALLSITE_CSV = "docs/reverse/generated/re164-ui-text-rendering-callsite-map.csv"
MD_OUTPUT = "docs/reverse/functions/re164-ui-text-rendering-caller-side-effect-map.md"
STORY_OUTPUT = "docs/stories/RE-164-ui-text-rendering-caller-side-effect-map.md"

C_KEYWORD_ARTIFACTS = {"if", "for", "while", "switch", "else", "do", "return", "sizeof"}
FORBIDDEN_FRAGMENTS = ("0x", "payload", "opcode", "machine word", "raw call target")
ORDER = {"PrintString": 0, "GetStringLength": 1}


@dataclass(frozen=True)
class ScopeRow:
    function: str
    file: str
    role: str
    implementation_status: str
    text_surface: str
    side_effect_surface: str
    source_contract: str
    proof_status: str
    patch_ready: str
    blocker: str


@dataclass(frozen=True)
class CallsiteRow:
    caller: str
    callee: str
    caller_file: str
    callee_file: str
    line: int
    shape_id: str
    arg_count: int
    coordinate_source: str
    colour_source: str
    text_source: str
    flag_source: str
    state_fields: str
    visible_side_effects: str
    proof_status: str
    patch_ready: str
    blocker: str


@dataclass(frozen=True)
class UiTextRenderingCallsiteMap:
    story_id: str
    upstream_ticket: str
    cluster: str
    status: str
    next_ticket: str
    code_change_ready_count: int
    marker_ready_count: int
    scope_rows: tuple[ScopeRow, ...]
    callsite_rows: tuple[CallsiteRow, ...]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def rel(path: Path, repo: Path) -> str:
    return path.relative_to(repo).as_posix()


def source_files(repo: Path) -> list[Path]:
    return sorted((repo / "SPEC_PSXPC_N").glob("*.C"))


def strip_comments(line: str) -> str:
    return line.split("//", 1)[0]


def verify_re163_plan(repo: Path) -> None:
    rows = read_csv(repo / RE163_PLAN_CSV)
    ids = tuple(row.get("story_id", "") for row in rows)
    expected = ("RE-164", "RE-165", "RE-166", "RE-167", "RE-168", "RE-169", "RE-170")
    if ids != expected:
        raise ValueError("RE-163 plan no longer matches RE-164..RE-170 expectations")
    first = rows[0]
    if first.get("topic") != "ui-text-rendering-caller-side-effect-map":
        raise ValueError("RE-163 first follow-up is no longer the UI text callsite map")


def target_rows(repo: Path) -> tuple[dict[str, str], ...]:
    rows = [
        row for row in read_csv(repo / RE163_AUDIT_CSV)
        if row.get("cluster") == "ui-text-rendering" and row.get("function") not in C_KEYWORD_ARTIFACTS
    ]
    rows.sort(key=lambda row: (ORDER.get(row.get("function", ""), 99), row.get("function", "")))
    selected = tuple(row.get("function", "") for row in rows)
    if selected != ("PrintString", "GetStringLength"):
        raise ValueError(f"RE-164 UI text scope drifted: {selected}")
    return tuple(rows)


def function_signature_name(line: str) -> str | None:
    clean = strip_comments(line).strip()
    if not clean or clean.endswith(";"):
        return None
    pattern = re.compile(
        r"^(?:static\s+)?(?:void|int|long|short|char|bool|unsigned\s+short|unsigned\s+char|unsigned\s+int|struct\s+\w+)\s+\*?\s*"
        r"([A-Za-z_][A-Za-z0-9_]*)\s*\([^;]*\)\s*(?:\{)?\s*$"
    )
    match = pattern.match(clean)
    if match and match.group(1) not in C_KEYWORD_ARTIFACTS:
        return match.group(1)
    return None


def function_spans(lines: list[str]) -> list[tuple[str, int, int]]:
    spans: list[tuple[str, int, int]] = []
    pending: tuple[str, int] | None = None
    current_name: str | None = None
    start_line = 0
    depth = 0
    for idx, line in enumerate(lines, start=1):
        clean = strip_comments(line)
        if current_name is None:
            name = function_signature_name(clean)
            if name:
                pending = (name, idx)
            if pending and "{" in clean:
                current_name, start_line = pending
                pending = None
                depth = clean.count("{") - clean.count("}")
                if depth <= 0:
                    spans.append((current_name, start_line, idx))
                    current_name = None
                    depth = 0
                continue
        else:
            depth += clean.count("{") - clean.count("}")
            if depth <= 0:
                spans.append((current_name, start_line, idx))
                current_name = None
                depth = 0
    return spans


def caller_at_line(spans: list[tuple[str, int, int]], line: int) -> str:
    for name, start, end in spans:
        if start <= line <= end:
            return name
    return "unknown-caller"


def find_function_file(repo: Path, function: str) -> str:
    for path in source_files(repo):
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        for name, _start, _end in function_spans(lines):
            if name == function:
                return rel(path, repo)
    return "unknown"


def function_body(repo: Path, function: str) -> str:
    file_name = find_function_file(repo, function)
    path = repo / file_name
    if not path.exists():
        return ""
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    for name, start, end in function_spans(lines):
        if name == function:
            return "\n".join(lines[start:end])
    return ""


def split_args(arg_text: str) -> list[str]:
    args: list[str] = []
    current: list[str] = []
    depth = 0
    for ch in arg_text:
        if ch == "(":
            depth += 1
        elif ch == ")" and depth:
            depth -= 1
        if ch == "," and depth == 0:
            value = "".join(current).strip()
            if value:
                args.append(value)
            current = []
        else:
            current.append(ch)
    value = "".join(current).strip()
    if value:
        args.append(value)
    return args


def extract_call_args(line: str, callee: str) -> list[str] | None:
    clean = strip_comments(line)
    marker = re.search(rf"\b{re.escape(callee)}\s*\(", clean)
    if not marker:
        return None
    start = marker.end()
    depth = 1
    pos = start
    while pos < len(clean):
        ch = clean[pos]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return split_args(clean[start:pos])
        pos += 1
    return []


def is_definition_line(line: str, callee: str) -> bool:
    clean = strip_comments(line).strip()
    if clean.startswith("extern "):
        return True
    return function_signature_name(clean) == callee


def text_surface(function: str) -> str:
    if function == "PrintString":
        return "draw-queue-text-rendering"
    if function == "GetStringLength":
        return "font-metric-measurement"
    return "ui-text-rendering"


def side_effect_surface(function: str) -> str:
    if function == "PrintString":
        return "font-scale-state;draw-char-primitives;text-positioning"
    if function == "GetStringLength":
        return "font-metric-scan;optional-bounds-output;scale-state-read"
    return "ui-text-state"


def source_contract(function: str) -> str:
    if function == "PrintString":
        return "Render source text to font glyph primitives using alignment and scale flags"
    if function == "GetStringLength":
        return "Measure source text width and optional vertical bounds using font metrics"
    return "UI text rendering source contract"


def state_fields_from_body(body: str, function: str) -> str:
    probes = (
        ("ScaleFlag", "scale-flag-state"),
        ("FontShades", "font-shade-table"),
        ("DrawChar", "glyph-draw-call"),
        ("db.polyptr", "draw-buffer-pointer"),
        ("db.ot", "ordering-table"),
        ("gfStringWad", "string-wad-source"),
        ("CharDef", "font-definition-table"),
        ("AccentTable", "accent-table"),
        ("GnFrameCounter", "blink-frame-counter"),
    )
    labels: list[str] = []
    for needle, label in probes:
        if needle in body and label not in labels:
            labels.append(label)
    if labels:
        return ";".join(labels)
    return "ui-text-rendering-state" if function == "PrintString" else "font-metric-state"


def classify_coordinate(args: list[str]) -> str:
    if len(args) < 2:
        return "not-applicable"
    joined = ";".join(args[:2])
    if "SCREEN_WIDTH" in joined or "256" in joined:
        return "screen-centered-or-absolute"
    if re.search(r"\b(?:x|y|rx|rw|ypos)\b", joined):
        return "caller-layout-derived"
    return "literal-or-expression-coordinate"


def classify_colour(args: list[str]) -> str:
    if len(args) < 3:
        return "not-applicable"
    colour = args[2]
    if re.fullmatch(r"\d+", colour.strip()):
        return "literal-colour-index"
    if "Col" in colour or "colour" in colour.lower():
        return "request-colour-field"
    return "expression-colour"


def classify_text(args: list[str]) -> str:
    joined = ";".join(args)
    if "gfStringWad" in joined:
        return "string-wad-offset"
    if "buf" in joined or "textbuf" in joined or "txbuf" in joined:
        return "formatted-buffer"
    if "\"" in joined:
        return "inline-control-string"
    if "current_options" in joined:
        return "inventory-option-pointer"
    if "string" in joined:
        return "caller-string-pointer"
    return "source-expression"


def classify_flags(args: list[str]) -> str:
    if len(args) < 5:
        return "not-applicable"
    flag = args[4].strip()
    if "FF_BLINK" in flag or ("|" in flag and flag.count("FF_") > 1):
        return "blink-or-composite-flags"
    if "FF_CENTER" in flag or flag == "0x8000":
        return "center-alignment-flags"
    if "FF_R_JUSTIFY" in flag or flag == "0x4000":
        return "right-alignment-flags"
    if "FF_NONE" in flag or flag == "0":
        return "no-alignment-flags"
    if "flags" in flag:
        return "caller-provided-flags"
    return "literal-or-composite-flags"


def shape_for(callee: str, args: list[str]) -> str:
    if callee == "PrintString":
        return "shape-ui-text-printstring-five-arg"
    if callee == "GetStringLength" and len(args) == 3:
        if any(arg == "NULL" or arg == "0" for arg in args[1:]):
            return "shape-ui-text-length-with-optional-bound"
        return "shape-ui-text-length-with-bounds"
    return f"shape-ui-text-{callee.lower()}-{len(args)}-arg"


def build_scope_rows(repo: Path) -> tuple[ScopeRow, ...]:
    rows: list[ScopeRow] = []
    for row in target_rows(repo):
        function = row["function"]
        rows.append(ScopeRow(
            function=function,
            file=row["file"],
            role=row["role"],
            implementation_status=row["status"],
            text_surface=text_surface(function),
            side_effect_surface=side_effect_surface(function),
            source_contract=source_contract(function),
            proof_status="source-needs-state-contract-and-equivalence-proof",
            patch_ready="no",
            blocker="missing-ui-text-rendering-state-contract-and-non-raw-equivalence-proof",
        ))
    return tuple(rows)


def direct_calls(repo: Path, wanted: tuple[str, ...]) -> list[CallsiteRow]:
    rows: list[CallsiteRow] = []
    for path in source_files(repo):
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        spans = function_spans(lines)
        for idx, line in enumerate(lines, start=1):
            for callee in wanted:
                args = extract_call_args(line, callee)
                if args is None or is_definition_line(line, callee):
                    continue
                caller = caller_at_line(spans, idx)
                if caller == "unknown-caller" or caller in C_KEYWORD_ARTIFACTS:
                    continue
                body = function_body(repo, callee)
                rows.append(CallsiteRow(
                    caller=caller,
                    callee=callee,
                    caller_file=rel(path, repo),
                    callee_file=find_function_file(repo, callee),
                    line=idx,
                    shape_id=shape_for(callee, args),
                    arg_count=len(args),
                    coordinate_source=classify_coordinate(args),
                    colour_source=classify_colour(args),
                    text_source=classify_text(args),
                    flag_source=classify_flags(args),
                    state_fields=state_fields_from_body(body, callee),
                    visible_side_effects=side_effect_surface(callee),
                    proof_status="source-callsite-mapped-only",
                    patch_ready="no",
                    blocker="missing-ui-text-rendering-state-contract-and-symbolic-equivalence-proof",
                ))
    return rows


def build_callsite_rows(repo: Path, scope_rows: tuple[ScopeRow, ...]) -> tuple[CallsiteRow, ...]:
    wanted = tuple(row.function for row in scope_rows)
    rows = direct_calls(repo, wanted)
    rows.sort(key=lambda row: (ORDER.get(row.callee, 99), row.caller_file, row.line, row.caller))
    return tuple(rows)


def build_ui_text_rendering_callsite_map(repo: Path) -> UiTextRenderingCallsiteMap:
    repo = Path(repo)
    verify_re163_plan(repo)
    scope_rows = build_scope_rows(repo)
    callsite_rows = build_callsite_rows(repo, scope_rows)
    return UiTextRenderingCallsiteMap(
        story_id="RE-164",
        upstream_ticket="RE-163",
        cluster="ui-text-rendering",
        status="caller-side-effect-map-blocked",
        next_ticket="RE-165",
        code_change_ready_count=0,
        marker_ready_count=0,
        scope_rows=scope_rows,
        callsite_rows=callsite_rows,
    )


def write_dict_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def assert_clean(path: Path) -> None:
    text = path.read_text(encoding="utf-8").lower()
    hits = [item for item in FORBIDDEN_FRAGMENTS if item in text]
    if hits:
        raise ValueError(f"forbidden metadata fragments in {path}: {hits}")


def write_all_artifacts(audit: UiTextRenderingCallsiteMap, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "scope_csv": repo / SCOPE_CSV,
        "callsite_csv": repo / CALLSITE_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY_OUTPUT,
    }
    write_dict_csv(paths["scope_csv"], list(ScopeRow.__dataclass_fields__), [row.__dict__ for row in audit.scope_rows])
    write_dict_csv(paths["callsite_csv"], list(CallsiteRow.__dataclass_fields__), [row.__dict__ for row in audit.callsite_rows])

    md = [
        "# RE-164 — UI text rendering caller and side-effect map",
        "",
        "Cluster: `ui-text-rendering`",
        "Decision: `caller-side-effect-map-blocked`",
        "Next: `RE-165`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-163 ticket plan consumed.",
        "- [x] UI text rendering callsites mapped.",
        "- [x] Text-source, flag-source, and visible side-effect categories classified.",
        "- [x] Patch and marker readiness kept blocked.",
        "",
        "## Summary",
        "",
        f"- scoped functions: `{', '.join(row.function for row in audit.scope_rows)}`",
        f"- source-backed callsite rows: `{len(audit.callsite_rows)}`",
        "- source patch authorized: `no`",
        "",
        "## Findings",
        "",
    ]
    for row in audit.callsite_rows:
        md.append(f"- `{row.caller}` -> `{row.callee}` in `{row.caller_file}`; shape `{row.shape_id}`; text `{row.text_source}`; flag `{row.flag_source}`; patch `{row.patch_ready}`")
    md.extend(["", "No production source or marker change is authorized by this map."])
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text("\n".join(md) + "\n", encoding="utf-8")

    story = [
        "# RE-164 — UI text rendering caller and side-effect map",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Map source-backed callers, text sources, flag families, and visible side-effect surfaces for `PrintString` and `GetStringLength` without authorizing source or marker changes.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-163 ticket plan consumed.",
        "- [x] UI text rendering callsites mapped.",
        "- [x] Source-backed rows verified against real source lines.",
        "- [x] Forbidden evidence excluded from generated artifacts.",
        "",
        "## Generated artifacts",
        "",
        f"- `{SCOPE_CSV}`",
        f"- `{CALLSITE_CSV}`",
        f"- `{MD_OUTPUT}`",
        "",
        "## Readiness decision",
        "",
        "- decision: `caller-side-effect-map-blocked`",
        "- code change readiness: `blocked`",
        "- marker readiness: `blocked`",
        "- next ticket: `RE-165`",
        "- blocker: `missing-ui-text-rendering-state-contract-and-symbolic-equivalence-proof`",
        "",
        "## Follow-up breakdown",
        "",
        "- `RE-165`: classify PrintString argument and flag taxonomy from this callsite map.",
        "- `RE-166`: document font, draw-buffer, scale, and string-table state contracts.",
        "- `RE-167`: run the non-raw equivalence/readiness gate.",
        "",
        "## Validation",
        "",
        "- `python3 -m pytest tests/reverse/test_re164_ui_text_rendering_callsite_map.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over RE-164 artifacts",
        "",
    ]
    paths["story"].parent.mkdir(parents=True, exist_ok=True)
    paths["story"].write_text("\n".join(story), encoding="utf-8")

    for path in paths.values():
        assert_clean(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    audit = build_ui_text_rendering_callsite_map(args.repo)
    for key, path in write_all_artifacts(audit, args.repo).items():
        print(f"{key}: {path}")
    print(f"callsites={len(audit.callsite_rows)}")
    print(f"next_ticket={audit.next_ticket}")


if __name__ == "__main__":
    main()
