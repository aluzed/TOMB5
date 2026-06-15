#!/usr/bin/env python3
"""Generate RE-062..RE-068 module-game debris/object-breakage chain artifacts.

The chain is intentionally metadata-only. It reads source file names, function
names, implementation categories, and symbolic callsite shapes, but it does not
publish raw reverse-engineering addresses, opcodes, machine words, call targets,
payload offsets, or copied dump rows.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


RE061_PLAN_CSV = "docs/reverse/generated/re061-module-game-ticket-plan.csv"
RE061_AUDIT_CSV = "docs/reverse/generated/re061-module-game-proof-first-audit.csv"
CHAIN_CSV = "docs/reverse/generated/re062-re068-module-game-chain.csv"
SCOPE_CSV = "docs/reverse/generated/re062-debris-object-breakage-scope.csv"
CALLSITE_CSV = "docs/reverse/generated/re062-debris-object-breakage-callsite-map.csv"
TAXONOMY_CSV = "docs/reverse/generated/re063-debris-object-breakage-argument-taxonomy.csv"
HANDOFF_CSV = "docs/reverse/generated/re068-module-game-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re062-re068-module-game-chain.md"
STORY_DIR = "docs/stories"

TARGET_FUNCTIONS = (
    "ShatterObject",
    "TriggerDebris",
    "GetFreeDebris",
    "UpdateDebris",
    "ExplodeItemNode",
    "ExplodeFX",
)

FORBIDDEN_FRAGMENTS = ("0x", "36A3C", "36F3C", "3675C", "36C5C", "366B0", "36BB0", "207DC", "209F0")


@dataclass(frozen=True)
class ScopeRow:
    function: str
    file: str
    caller_or_callee_role: str
    implementation_status: str
    side_effect_surface: str
    source_contract: str
    proof_status: str
    blocker: str


@dataclass(frozen=True)
class CallsiteRow:
    caller: str
    callee: str
    caller_file: str
    callee_file: str
    line: int
    shape_id: str
    room_source: str
    bits_source: str
    side_effects: str
    proof_status: str
    patch_ready: str
    blocker: str


@dataclass(frozen=True)
class ArgumentShape:
    shape_id: str
    site_count: int
    arg1_kind: str
    arg2_kind: str
    arg3_kind: str
    arg4_kind: str
    arg5_kind: str
    source_backed: str
    patch_ready: str
    blocker: str


@dataclass(frozen=True)
class Handoff:
    next_ticket: str
    next_cluster: str
    reason: str
    code_change_readiness: str
    blocker: str


@dataclass(frozen=True)
class Ticket:
    story_id: str
    title: str
    status: str
    decision: str
    next_ticket: str
    code_change_readiness: str
    progress: tuple[str, ...]
    generated_artifacts: tuple[str, ...]
    findings: tuple[str, ...]


@dataclass(frozen=True)
class ModuleGameChain:
    domain_id: str
    cluster: str
    status: str
    final_decision: str
    next_ticket: str
    code_change_ready_count: int
    marker_ready_count: int
    source_patch_ready_count: int
    scope_rows: tuple[ScopeRow, ...]
    callsites: tuple[CallsiteRow, ...]
    argument_shapes: tuple[ArgumentShape, ...]
    handoff: Handoff
    tickets: tuple[Ticket, ...]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def strip_comments(line: str) -> str:
    return line.split("//", 1)[0]


def source_files(repo: Path) -> list[Path]:
    roots = [repo / "GAME"]
    files: list[Path] = []
    for root in roots:
        files.extend(sorted(root.glob("*.C")))
    return files


def relative(path: Path, repo: Path) -> str:
    return path.relative_to(repo).as_posix()


def find_function_file(repo: Path, function: str) -> str:
    pattern = re.compile(rf"\b{re.escape(function)}\s*\(")
    for path in source_files(repo):
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            clean = strip_comments(line)
            if pattern.search(clean) and not clean.lstrip().startswith(("if", "while", "for", "return")):
                if clean.rstrip().endswith(";"):
                    continue
                return relative(path, repo)
    return "unknown"


def function_body(repo: Path, function: str) -> str:
    path = repo / find_function_file(repo, function)
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore")
    start = re.search(rf"\b{re.escape(function)}\s*\([^)]*\)\s*(?://[^\n]*)?\n\{{", text)
    if not start:
        return ""
    idx = start.end()
    depth = 1
    pos = idx
    while pos < len(text) and depth:
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
        pos += 1
    return text[idx:pos - 1]


def implementation_status(repo: Path, function: str) -> str:
    body = function_body(repo, function)
    if "UNIMPLEMENTED" in body or "Unimpl" in body:
        return "unimplemented-stub"
    if body.strip():
        return "implemented-source"
    return "missing-source"


def role_for(function: str) -> str:
    if function == "ShatterObject":
        return "pivot"
    if function in {"TriggerDebris", "GetFreeDebris"}:
        return "callee-or-helper"
    if function == "UpdateDebris":
        return "runtime-updater"
    return "caller"


def side_effect_surface(function: str) -> str:
    return {
        "ShatterObject": "debris-allocation;mesh-bit-updates;room-scoped-spawn",
        "TriggerDebris": "debris-slot-write;velocity-rgb-texture-inputs",
        "GetFreeDebris": "debris-ring-selection;next-debris-write",
        "UpdateDebris": "runtime-debris-update-loop",
        "ExplodeItemNode": "item-mesh-bit-clear;shatter-item-global-setup",
        "ExplodeFX": "fx-derived-shatter-item;debris-flags-temporary-write",
    }.get(function, "debris-adjacent")


def source_contract(function: str) -> str:
    return {
        "ShatterObject": "item-or-static-mesh plus mesh-bits room and xz-velocity policy",
        "TriggerDebris": "position texture offsets velocity vector and rgb inputs",
        "GetFreeDebris": "debris pool scan and reusable slot selection",
        "UpdateDebris": "runtime debris integration",
        "ExplodeItemNode": "item node to shatter-item conversion",
        "ExplodeFX": "effect instance to shatter-item conversion",
    }.get(function, "supporting source contract")


def build_scope_rows(repo: Path) -> tuple[ScopeRow, ...]:
    rows = []
    for function in TARGET_FUNCTIONS:
        status = implementation_status(repo, function)
        proof = "source-contract-visible"
        blocker = "missing-non-raw-binary-equivalence"
        if status == "unimplemented-stub":
            proof = "source-stub-no-behavior-body"
            blocker = "implementation body absent and non-raw binary equivalence not available"
        rows.append(
            ScopeRow(
                function=function,
                file=find_function_file(repo, function),
                caller_or_callee_role=role_for(function),
                implementation_status=status,
                side_effect_surface=side_effect_surface(function),
                source_contract=source_contract(function),
                proof_status=proof,
                blocker=blocker,
            )
        )
    order = {name: index for index, name in enumerate(TARGET_FUNCTIONS)}
    return tuple(sorted(rows, key=lambda row: order[row.function]))


def split_args(text: str) -> list[str]:
    args: list[str] = []
    current: list[str] = []
    depth = 0
    for ch in text:
        if ch == "," and depth == 0:
            args.append("".join(current).strip())
            current = []
            continue
        if ch in "([":
            depth += 1
        elif ch in ")]" and depth:
            depth -= 1
        current.append(ch)
    if current:
        args.append("".join(current).strip())
    return args


def classify_arg(arg: str) -> str:
    compact = re.sub(r"\s+", "", arg)
    if compact in {"0", "NULL"}:
        return "null-or-zero"
    if "ShatterItem" in compact:
        return "shatter-item-global"
    if "item->room_number" in compact:
        return "item-room"
    if "fx->room_number" in compact:
        return "fx-room"
    if "NoXZVel" in compact:
        return "xz-velocity-policy"
    if "bits" in compact or "num" in compact or compact.isdigit():
        return "mesh-bit-mask"
    if "mesh" in compact:
        return "static-mesh"
    return "source-expression"


def shape_for(caller: str, callee: str, args: list[str]) -> tuple[str, str, str]:
    if callee == "UpdateDebris":
        return "shape-runtime-tick-no-args", "runtime-room-context", "not-applicable"
    arg_text = ";".join(args)
    if caller == "ExplodeItemNode":
        return "shape-item-derived-room-and-bits", "item-room", "item-node-mask"
    if caller == "ExplodeFX":
        return "shape-fx-derived-room-and-bits", "fx-room", "fx-bits-input"
    if "StaticMesh" in arg_text or "mesh" in arg_text:
        return "shape-static-mesh-room-and-fixed-bits", "static-mesh-room", "fixed-or-mesh-bits"
    return "shape-debris-support-call", "source-context", "source-context"


def build_callsites(repo: Path) -> tuple[CallsiteRow, ...]:
    wanted = ("ShatterObject", "TriggerDebris", "GetFreeDebris", "UpdateDebris")
    rows: list[CallsiteRow] = []
    call_re = re.compile(r"\b(" + "|".join(map(re.escape, wanted)) + r")\s*\((.*)\)")
    function_re = re.compile(
        r"^\s*(?:void|int|long|short|char|bool|struct\s+\w+\s*\*?)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^;]*\)\s*(?://.*)?$"
    )
    control_keywords = {"if", "for", "while", "switch"}
    for path in source_files(repo):
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        rel = relative(path, repo)
        current_function = "unknown-caller"
        pending_function = ""
        brace_depth = 0
        for idx, line in enumerate(lines):
            clean = strip_comments(line).rstrip()
            signature = function_re.match(clean)
            if signature and signature.group(1) not in control_keywords:
                pending_function = signature.group(1)
            opens = clean.count("{")
            closes = clean.count("}")
            if pending_function and opens:
                current_function = pending_function
                pending_function = ""
            if brace_depth <= 0 and not opens and pending_function:
                current_function = pending_function
            caller = current_function
            brace_depth += opens - closes
            match = call_re.search(clean)
            if not match:
                continue
            callee = match.group(1)
            if caller == callee or clean.lstrip().startswith("///") or caller in control_keywords:
                continue
            if caller == "unknown-caller":
                continue
            args = split_args(match.group(2)) if match.group(2).strip() else []
            shape_id, room_source, bits_source = shape_for(caller, callee, args)
            rows.append(
                CallsiteRow(
                    caller=caller,
                    callee=callee,
                    caller_file=rel,
                    callee_file=find_function_file(repo, callee),
                    line=idx + 1,
                    shape_id=shape_id,
                    room_source=room_source,
                    bits_source=bits_source,
                    side_effects=side_effect_surface(callee),
                    proof_status="source-callsite-mapped-only",
                    patch_ready="no",
                    blocker="missing-non-raw-binary-equivalence",
                )
            )
    rows.sort(key=lambda row: (row.callee, row.caller_file, row.line, row.caller))
    return tuple(rows)


def build_argument_shapes(callsites: tuple[CallsiteRow, ...]) -> tuple[ArgumentShape, ...]:
    counts = Counter(row.shape_id for row in callsites if row.callee == "ShatterObject")
    rows: list[ArgumentShape] = []
    for shape_id, count in counts.items():
        if shape_id == "shape-item-derived-room-and-bits":
            kinds = ("shatter-item-global", "null-or-zero", "item-node-mask", "item-room", "xz-velocity-policy")
        elif shape_id == "shape-fx-derived-room-and-bits":
            kinds = ("shatter-item-global", "null-or-zero", "fx-bits-input", "fx-room", "xz-velocity-policy")
        elif shape_id == "shape-static-mesh-room-and-fixed-bits":
            kinds = ("null-or-zero", "static-mesh", "fixed-or-mesh-bits", "static-mesh-room", "zero-policy")
        else:
            kinds = ("source-expression", "source-expression", "source-expression", "source-expression", "source-expression")
        rows.append(
            ArgumentShape(
                shape_id=shape_id,
                site_count=count,
                arg1_kind=kinds[0],
                arg2_kind=kinds[1],
                arg3_kind=kinds[2],
                arg4_kind=kinds[3],
                arg5_kind=kinds[4],
                source_backed="yes",
                patch_ready="no",
                blocker="missing-non-raw-binary-equivalence;stubbed-pivot-body",
            )
        )
    rows.sort(key=lambda row: (-row.site_count, row.shape_id))
    return tuple(rows)


def choose_handoff(repo: Path) -> Handoff:
    audit_rows = read_csv(repo / RE061_AUDIT_CSV)
    cluster_counts = Counter(row.get("cluster", "") for row in audit_rows if row.get("cluster") != "debris-object-breakage")
    next_cluster = "object-interaction"
    if cluster_counts:
        next_cluster = cluster_counts.most_common(1)[0][0]
    return Handoff(
        next_ticket="RE-069",
        next_cluster=next_cluster,
        reason="initial-cluster-terminal-blocker",
        code_change_readiness="blocked",
        blocker="debris/object-breakage has source stubs and no non-raw binary equivalence proof for safe patching",
    )


def verify_re061_plan(repo: Path) -> None:
    rows = read_csv(repo / RE061_PLAN_CSV)
    ids = tuple(row.get("story_id", "") for row in rows)
    expected = ("RE-062", "RE-063", "RE-064", "RE-065", "RE-066", "RE-067", "RE-068")
    if ids != expected:
        raise ValueError("RE-061 plan no longer matches RE-062..RE-068 chain expectations")


def build_tickets(chain: "ModuleGameChain | None", handoff: Handoff) -> tuple[Ticket, ...]:
    common_artifacts = (
        CHAIN_CSV,
        SCOPE_CSV,
        CALLSITE_CSV,
        TAXONOMY_CSV,
        HANDOFF_CSV,
        MD_OUTPUT,
    )
    specs = (
        ("RE-062", "Debris object breakage caller side-effect map", "caller-side-effect-map-published", "RE-063"),
        ("RE-063", "Debris object breakage argument data taxonomy", "argument-taxonomy-published", "RE-064"),
        ("RE-064", "Debris object breakage comparison gate", "no-patch-proof-blocker", "RE-065"),
        ("RE-065", "Debris object breakage reconstruction plan", "documentation-only-plan", "RE-066"),
        ("RE-066", "Debris object breakage source patch gate", "source-patch-denied", "RE-067"),
        ("RE-067", "Debris object breakage validation regression", "metadata-validation-published", "RE-068"),
        ("RE-068", "Module-game closure or next cluster handoff", "handoff-to-next-module-game-cluster", handoff.next_ticket),
    )
    tickets: list[Ticket] = []
    for story_id, title, decision, next_ticket in specs:
        progress = (
            "RE-061 plan consumed.",
            "Source-level metadata mapped.",
            "Patch readiness checked.",
            "Forbidden raw evidence excluded.",
        )
        if story_id == "RE-068":
            progress = progress + ("Closure/handoff recorded.",)
        tickets.append(
            Ticket(
                story_id=story_id,
                title=title,
                status="done",
                decision=decision,
                next_ticket=next_ticket,
                code_change_readiness="blocked",
                progress=progress,
                generated_artifacts=common_artifacts,
                findings=(
                    "source-level call/data metadata is available",
                    "no source or marker patch is admitted without non-raw binary equivalence proof",
                    f"handoff target: {handoff.next_ticket} {handoff.next_cluster}" if story_id == "RE-068" else "continue current chain",
                ),
            )
        )
    return tuple(tickets)


def build_module_game_chain(repo: Path) -> ModuleGameChain:
    repo = Path(repo)
    verify_re061_plan(repo)
    scope_rows = build_scope_rows(repo)
    callsites = build_callsites(repo)
    argument_shapes = build_argument_shapes(callsites)
    handoff = choose_handoff(repo)
    chain = ModuleGameChain(
        domain_id="module-game",
        cluster="debris-object-breakage",
        status="module-game-debris-chain-closed-with-proof-blocker",
        final_decision="documentation-only-terminal-blocker",
        next_ticket=handoff.next_ticket,
        code_change_ready_count=0,
        marker_ready_count=0,
        source_patch_ready_count=0,
        scope_rows=scope_rows,
        callsites=callsites,
        argument_shapes=argument_shapes,
        handoff=handoff,
        tickets=(),
    )
    tickets = build_tickets(chain, handoff)
    return ModuleGameChain(**{**chain.__dict__, "tickets": tickets})


def write_dict_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def assert_metadata_only(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    hits = [fragment for fragment in FORBIDDEN_FRAGMENTS if fragment in text]
    if hits:
        raise ValueError(f"forbidden raw evidence fragments in {path}: {hits}")


def write_chain_csv(path: Path, chain: ModuleGameChain) -> None:
    fields = ["story_id", "title", "status", "decision", "next_ticket", "code_change_readiness", "generated_artifacts", "findings"]
    rows = []
    for ticket in chain.tickets:
        rows.append({**ticket.__dict__, "generated_artifacts": ";".join(ticket.generated_artifacts), "findings": ";".join(ticket.findings)})
    write_dict_csv(path, fields, rows)


def write_scope_csv(path: Path, chain: ModuleGameChain) -> None:
    fields = ["function", "file", "caller_or_callee_role", "implementation_status", "side_effect_surface", "source_contract", "proof_status", "blocker"]
    write_dict_csv(path, fields, [row.__dict__ for row in chain.scope_rows])


def write_callsite_csv(path: Path, chain: ModuleGameChain) -> None:
    fields = ["caller", "callee", "caller_file", "callee_file", "line", "shape_id", "room_source", "bits_source", "side_effects", "proof_status", "patch_ready", "blocker"]
    write_dict_csv(path, fields, [row.__dict__ for row in chain.callsites])


def write_taxonomy_csv(path: Path, chain: ModuleGameChain) -> None:
    fields = ["shape_id", "site_count", "arg1_kind", "arg2_kind", "arg3_kind", "arg4_kind", "arg5_kind", "source_backed", "patch_ready", "blocker"]
    write_dict_csv(path, fields, [row.__dict__ for row in chain.argument_shapes])


def write_handoff_csv(path: Path, chain: ModuleGameChain) -> None:
    fields = ["next_ticket", "next_cluster", "reason", "code_change_readiness", "blocker"]
    write_dict_csv(path, fields, [chain.handoff.__dict__])


def write_markdown(path: Path, chain: ModuleGameChain) -> None:
    lines = [
        "# RE-062..RE-068 — Module-game debris/object-breakage chain",
        "",
        f"Domain: `{chain.domain_id}`",
        f"Cluster: `{chain.cluster}`",
        f"Status: `{chain.status}`",
        f"Decision: `{chain.final_decision}`",
        f"Next ticket: `{chain.next_ticket}`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-061 multi-ticket plan consumed.",
        "- [x] RE-062 caller and side-effect map published.",
        "- [x] RE-063 argument/data taxonomy published.",
        "- [x] RE-064 comparison gate evaluated.",
        "- [x] RE-065 reconstruction plan reduced to documentation-only blocker.",
        "- [x] RE-066 source patch gate denied safely.",
        "- [x] RE-067 validation/regression metadata recorded.",
        "- [x] RE-068 closure/handoff recorded.",
        "",
        "## Readiness",
        "",
        f"- code-change-ready rows: `{chain.code_change_ready_count}`",
        f"- marker-ready rows: `{chain.marker_ready_count}`",
        f"- source-patch-ready rows: `{chain.source_patch_ready_count}`",
        "- terminal blocker: `source stubs and missing non-raw binary equivalence proof`",
        "",
        "## Scope rows",
        "",
    ]
    for row in chain.scope_rows:
        lines.append(f"- `{row.function}` — `{row.implementation_status}` / `{row.proof_status}` / blocker `{row.blocker}`")
    lines.extend([
        "",
        "## Argument shapes",
        "",
    ])
    for shape in chain.argument_shapes:
        lines.append(f"- `{shape.shape_id}` — sites `{shape.site_count}`, patch-ready `{shape.patch_ready}`, blocker `{shape.blocker}`")
    lines.extend([
        "",
        "## Handoff",
        "",
        f"- next ticket: `{chain.handoff.next_ticket}`",
        f"- next cluster: `{chain.handoff.next_cluster}`",
        f"- reason: `{chain.handoff.reason}`",
        "",
        "No production source, marker, binary, asset, opcode, machine-word, raw call-target, or payload-offset change is made by this chain.",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_story(path: Path, chain: ModuleGameChain, ticket: Ticket) -> None:
    lines = [
        f"# {ticket.story_id} — {ticket.title}",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        f"Advance `{chain.cluster}` within `module-game` using metadata-only evidence for {ticket.story_id}.",
        "",
        "## Progress tracker",
        "",
    ]
    for item in ticket.progress:
        lines.append(f"- [x] {item}")
    lines.extend([
        "",
        "## Generated artifacts",
        "",
    ])
    for artifact in ticket.generated_artifacts:
        lines.append(f"- `{artifact}`")
    lines.extend([
        "",
        "## Findings",
        "",
    ])
    for finding in ticket.findings:
        lines.append(f"- {finding}")
    lines.extend([
        "",
        "## Readiness decision",
        "",
        f"- decision: `{ticket.decision}`",
        f"- code change readiness: `{ticket.code_change_readiness}`",
        f"- next ticket: `{ticket.next_ticket}`",
        "",
        "Do not patch production source or add/remove proof markers from this story alone.",
        "",
        "## Validation",
        "",
        "- `python3 -m pytest tests/reverse/test_re062_re068_module_game_chain.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over generated RE-062..RE-068 artifacts",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_all_artifacts(chain: ModuleGameChain, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "chain_csv": repo / CHAIN_CSV,
        "scope_csv": repo / SCOPE_CSV,
        "callsite_csv": repo / CALLSITE_CSV,
        "taxonomy_csv": repo / TAXONOMY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
    }
    write_chain_csv(paths["chain_csv"], chain)
    write_scope_csv(paths["scope_csv"], chain)
    write_callsite_csv(paths["callsite_csv"], chain)
    write_taxonomy_csv(paths["taxonomy_csv"], chain)
    write_handoff_csv(paths["handoff_csv"], chain)
    write_markdown(paths["md"], chain)
    for ticket in chain.tickets:
        key = ticket.story_id
        path = repo / STORY_DIR / f"{ticket.story_id}-{ticket.title.lower().replace(' ', '-')}.md"
        write_story(path, chain, ticket)
        paths[key] = path
    for path in paths.values():
        assert_metadata_only(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    chain = build_module_game_chain(args.repo)
    written = write_all_artifacts(chain, args.repo)
    for key, path in written.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
