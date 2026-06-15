#!/usr/bin/env python3
"""Generate RE-150 item-lighting interaction caller/side-effect map artifacts."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path

RE149_PLAN_CSV = "docs/reverse/generated/re149-item-lighting-interaction-ticket-plan.csv"
RE149_AUDIT_CSV = "docs/reverse/generated/re149-item-lighting-interaction-proof-first-audit.csv"
SCOPE_CSV = "docs/reverse/generated/re150-item-lighting-interaction-scope.csv"
CALLSITE_CSV = "docs/reverse/generated/re150-item-lighting-interaction-callsite-map.csv"
MD_OUTPUT = "docs/reverse/functions/re150-item-lighting-interaction-caller-side-effect-map.md"
STORY_OUTPUT = "docs/stories/RE-150-item-lighting-interaction-caller-side-effect-map.md"

C_KEYWORD_ARTIFACTS = {"if", "for", "while", "switch", "else", "do"}
FORBIDDEN_FRAGMENTS = ("0x", "payload", "opcode", "machine word", "raw call target")
ORDER = {"DoFlameTorch": 0, "TriggerAlertLight": 1}


@dataclass(frozen=True)
class ScopeRow:
    function: str
    file: str
    role: str
    implementation_status: str
    interaction_family: str
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
    argument_kinds: str
    state_fields: str
    side_effects: str
    proof_status: str
    patch_ready: str
    blocker: str


@dataclass(frozen=True)
class ItemLightingCallsiteMap:
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


def source_files(repo: Path) -> list[Path]:
    return sorted((repo / "GAME").glob("*.C"))


def rel(path: Path, repo: Path) -> str:
    return path.relative_to(repo).as_posix()


def strip_comments(line: str) -> str:
    return line.split("//", 1)[0]


def verify_re149_plan(repo: Path) -> None:
    rows = read_csv(repo / RE149_PLAN_CSV)
    ids = tuple(row.get("story_id", "") for row in rows)
    expected = ("RE-150", "RE-151", "RE-152", "RE-153", "RE-154", "RE-155", "RE-156")
    if ids != expected:
        raise ValueError("RE-149 plan no longer matches RE-150..RE-156 expectations")


def target_rows(repo: Path) -> tuple[dict[str, str], ...]:
    rows = [row for row in read_csv(repo / RE149_AUDIT_CSV) if row.get("cluster") == "item-lighting-interaction" and row.get("function") not in C_KEYWORD_ARTIFACTS]
    rows.sort(key=lambda row: (ORDER.get(row.get("function", ""), 99), row.get("function", "")))
    selected = tuple(row.get("function", "") for row in rows)
    if selected != ("DoFlameTorch", "TriggerAlertLight"):
        raise ValueError(f"RE-150 item-lighting scope drifted: {selected}")
    return tuple(rows)


def find_function_file(repo: Path, function: str) -> str:
    pattern = re.compile(rf"\b{re.escape(function)}\s*\(")
    for path in source_files(repo):
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            clean = strip_comments(line).strip()
            if not pattern.search(clean) or clean.endswith(";"):
                continue
            if clean.startswith(("if", "while", "for", "return", "else", "switch")):
                continue
            return rel(path, repo)
    return "unknown"


def function_body(repo: Path, function: str) -> str:
    file_name = find_function_file(repo, function)
    path = repo / file_name
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(rf"\b{re.escape(function)}\s*\([^)]*\)", text)
    if not match:
        return ""
    brace = text.find("{", match.end())
    if brace < 0:
        return ""
    pos = brace + 1
    depth = 1
    while pos < len(text) and depth:
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
        pos += 1
    return text[brace + 1:pos - 1]


def side_effect_surface(function: str) -> str:
    if function == "DoFlameTorch":
        return "lara-torch-state;left-arm-state;item-flame-state;torch-particle-state"
    if function == "TriggerAlertLight":
        return "alert-light-state;dynamic-light-state;room-light-state"
    return "item-lighting-state"


def source_contract(function: str) -> str:
    if function == "DoFlameTorch":
        return "Torch-in-hand update from Lara gun state to flame/light side effects"
    if function == "TriggerAlertLight":
        return "Alert-light emission from position/color/angle/room parameters"
    return "Item lighting interaction source contract"


def state_fields_from_body(body: str, function: str) -> str:
    if not body.strip():
        return "source-body-missing"
    probes = (
        ("lara", "lara-state"),
        ("left_arm", "lara-left-arm-state"),
        ("gun_type", "lara-gun-state"),
        ("item", "item-state"),
        ("TriggerDynamic", "dynamic-light-state"),
        ("TriggerAlertLight", "alert-light-state"),
        ("spark", "particle-state"),
        ("room", "room-light-state"),
    )
    fields: list[str] = []
    for needle, label in probes:
        if needle in body and label not in fields:
            fields.append(label)
    if fields:
        return ";".join(fields)
    return "torch-item-state" if function == "DoFlameTorch" else "alert-light-state"


def classify_args(args: list[str]) -> str:
    joined = ";".join(arg.strip() for arg in args if arg.strip())
    if not joined:
        return "void"
    if "item" in joined:
        return "item-derived-arguments"
    if any(token in joined for token in ("x", "y", "z", "r", "g", "b", "angle", "room")):
        return "position-color-room-arguments"
    return "symbolic-item-lighting-arguments"


def shape_for(callee: str, arg_count: int) -> str:
    if callee == "DoFlameTorch":
        return "shape-item-lighting-void-torch-update"
    if callee == "TriggerAlertLight":
        return "shape-item-lighting-alert-light-parameters"
    return f"shape-item-lighting-{arg_count}-arg"


def build_scope_rows(repo: Path) -> tuple[ScopeRow, ...]:
    rows: list[ScopeRow] = []
    for row in target_rows(repo):
        function = row["function"]
        rows.append(ScopeRow(
            function=function,
            file=row["file"],
            role=row["role"],
            implementation_status=row["implementation_status"],
            interaction_family=row["interaction_family"],
            side_effect_surface=side_effect_surface(function),
            source_contract=source_contract(function),
            proof_status="source-body-missing" if row["implementation_status"] == "unimplemented-stub" else "source-needs-equivalence-proof",
            patch_ready="no",
            blocker="missing-item-lighting-state-contract-and-symbolic-equivalence-proof",
        ))
    return tuple(rows)


def direct_calls(repo: Path, wanted: tuple[str, ...]) -> list[CallsiteRow]:
    wanted_re = re.compile(r"\b(" + "|".join(map(re.escape, wanted)) + r")\s*\(([^)]*)\)")
    function_re = re.compile(r"^\s*(?:void|int|long|short|char|bool|struct\s+\w+)\s*\*?\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^;]*\)\s*(?://.*)?$")
    rows: list[CallsiteRow] = []
    for path in source_files(repo):
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        current = "unknown-caller"
        pending = ""
        for idx, line in enumerate(lines):
            clean = strip_comments(line).rstrip()
            sig = function_re.match(clean)
            is_definition = False
            if sig and sig.group(1) not in C_KEYWORD_ARTIFACTS:
                pending = sig.group(1)
                is_definition = True
            if pending and "{" in clean:
                current = pending
                pending = ""
            if is_definition:
                continue
            for match in wanted_re.finditer(clean):
                callee = match.group(1)
                if current == callee or current == "unknown-caller" or current in C_KEYWORD_ARTIFACTS:
                    continue
                args = [arg.strip() for arg in match.group(2).split(",") if arg.strip()]
                body = function_body(repo, callee)
                rows.append(CallsiteRow(
                    caller=current,
                    callee=callee,
                    caller_file=rel(path, repo),
                    callee_file=find_function_file(repo, callee),
                    line=idx + 1,
                    shape_id=shape_for(callee, len(args)),
                    arg_count=len(args),
                    argument_kinds=classify_args(args),
                    state_fields=state_fields_from_body(body, callee),
                    side_effects=side_effect_surface(callee),
                    proof_status="source-callsite-mapped-only",
                    patch_ready="no",
                    blocker="missing-symbolic-equivalence-proof",
                ))
    return rows


def build_callsite_rows(repo: Path, scope_rows: tuple[ScopeRow, ...]) -> tuple[CallsiteRow, ...]:
    wanted = tuple(row.function for row in scope_rows)
    rows = direct_calls(repo, wanted)
    rows.sort(key=lambda row: (row.callee, row.caller_file, row.line, row.caller))
    return tuple(rows)


def build_item_lighting_callsite_map(repo: Path) -> ItemLightingCallsiteMap:
    repo = Path(repo)
    verify_re149_plan(repo)
    scope_rows = build_scope_rows(repo)
    callsite_rows = build_callsite_rows(repo, scope_rows)
    return ItemLightingCallsiteMap(
        story_id="RE-150",
        upstream_ticket="RE-149",
        cluster="item-lighting-interaction",
        status="caller-side-effect-map-blocked",
        next_ticket="RE-151",
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


def write_all_artifacts(audit: ItemLightingCallsiteMap, repo: Path) -> dict[str, Path]:
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
        "# RE-150 — Item lighting interaction caller and side-effect map",
        "",
        "Cluster: `item-lighting-interaction`",
        "Decision: `caller-side-effect-map-blocked`",
        "Next: `RE-151`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-149 ticket plan consumed.",
        "- [x] Item-lighting callsites mapped.",
        "- [x] Torch and alert-light side-effect surfaces classified.",
        "- [x] Patch and marker readiness kept blocked.",
        "",
        "## Findings",
        "",
    ]
    for row in audit.callsite_rows:
        md.append(f"- `{row.caller}` -> `{row.callee}` in `{row.caller_file}`; shape `{row.shape_id}`; patch `{row.patch_ready}`")
    md.extend(["", "No production source or marker change is authorized by this map."])
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text("\n".join(md) + "\n", encoding="utf-8")

    story = [
        "# RE-150 — Item lighting interaction caller and side-effect map",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Map callers and side-effect surfaces for `DoFlameTorch` and `TriggerAlertLight` without authorizing source or marker changes.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-149 ticket plan consumed.",
        "- [x] Item-lighting callsites mapped.",
        "- [x] Torch and alert-light side-effect surfaces classified.",
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
        "- next ticket: `RE-151`",
        "- blocker: `missing-item-lighting-state-contract-and-symbolic-equivalence-proof`",
        "",
        "## Validation",
        "",
        "- `python3 -m pytest tests/reverse/test_re150_item_lighting_callsite_map.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over RE-150 artifacts",
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
    audit = build_item_lighting_callsite_map(args.repo)
    for key, path in write_all_artifacts(audit, args.repo).items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
