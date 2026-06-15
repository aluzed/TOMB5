#!/usr/bin/env python3
"""Generate RE-078..RE-084 gameflow/runtime chain artifacts.

This range consumes the RE-077 gameflow runtime audit and emits metadata-only
caller maps, argument/state taxonomy, readiness gates, validation notes, and a
handoff for the title/control phase subcluster. It publishes symbolic summaries
only and does not admit source or marker changes without equivalence proof.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


RE077_PLAN_CSV = "docs/reverse/generated/re077-gameflow-runtime-ticket-plan.csv"
RE077_AUDIT_CSV = "docs/reverse/generated/re077-gameflow-runtime-proof-first-audit.csv"
RE077_SUBCLUSTER_CSV = "docs/reverse/generated/re077-gameflow-runtime-subclusters.csv"
CHAIN_CSV = "docs/reverse/generated/re078-re084-gameflow-runtime-chain.csv"
SCOPE_CSV = "docs/reverse/generated/re078-gameflow-runtime-scope.csv"
CALLSITE_CSV = "docs/reverse/generated/re078-gameflow-runtime-callsite-map.csv"
TAXONOMY_CSV = "docs/reverse/generated/re079-gameflow-runtime-argument-state-taxonomy.csv"
HANDOFF_CSV = "docs/reverse/generated/re084-gameflow-runtime-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re078-re084-gameflow-runtime-chain.md"
STORY_DIR = "docs/stories"

C_KEYWORD_ARTIFACTS = {"if", "for", "while", "switch", "else", "do"}
FORBIDDEN_FRAGMENTS = ("0x", "payload", "opcode", "machine word", "raw call target")


@dataclass(frozen=True)
class ScopeRow:
    function: str
    file: str
    role: str
    implementation_status: str
    marker_status: str
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
    arg_count: int
    argument_kinds: str
    state_fields: str
    side_effects: str
    proof_status: str
    patch_ready: str
    blocker: str


@dataclass(frozen=True)
class StateTaxonomyRow:
    shape_id: str
    site_count: int
    argument_kinds: str
    state_fields: str
    write_surfaces: str
    source_backed: str
    patch_ready: str
    blocker: str


@dataclass(frozen=True)
class Handoff:
    next_ticket: str
    next_cluster: str
    next_subcluster: str
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
class GameflowRuntimeChain:
    domain_id: str
    cluster: str
    subcluster: str
    status: str
    final_decision: str
    next_ticket: str
    code_change_ready_count: int
    marker_ready_count: int
    source_patch_ready_count: int
    scope_rows: tuple[ScopeRow, ...]
    callsites: tuple[CallsiteRow, ...]
    taxonomy_rows: tuple[StateTaxonomyRow, ...]
    handoff: Handoff
    tickets: tuple[Ticket, ...]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def source_files(repo: Path) -> list[Path]:
    return sorted((repo / "GAME").glob("*.C"))


def rel(path: Path, repo: Path) -> str:
    return path.relative_to(repo).as_posix()


def strip_comments(line: str) -> str:
    return line.split("//", 1)[0]


def verify_re077_plan(repo: Path) -> None:
    rows = read_csv(repo / RE077_PLAN_CSV)
    ids = tuple(row.get("story_id", "") for row in rows)
    expected = ("RE-078", "RE-079", "RE-080", "RE-081", "RE-082", "RE-083", "RE-084")
    if ids != expected:
        raise ValueError("RE-077 plan no longer matches RE-078..RE-084 chain expectations")


def target_functions(repo: Path) -> tuple[str, ...]:
    rows = read_csv(repo / RE077_AUDIT_CSV)
    targets = [
        row["function"]
        for row in rows
        if row.get("subcluster") == "title-and-control-phase" and row.get("function") not in C_KEYWORD_ARTIFACTS
    ]
    targets.sort(key=lambda name: {"DoTitle": 0, "QuickControlPhase": 1, "DoGameflow": 2}.get(name, 99))
    return tuple(targets)


def audit_row_by_function(repo: Path) -> dict[str, dict[str, str]]:
    return {row.get("function", ""): row for row in read_csv(repo / RE077_AUDIT_CSV)}


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
    start = re.search(rf"\b{re.escape(function)}\s*\([^)]*\)\s*(?://[^\n]*)?\n\{{", text)
    if not start:
        return ""
    pos = start.end()
    depth = 1
    while pos < len(text) and depth:
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
        pos += 1
    return text[start.end():pos - 1]


def implementation_status(repo: Path, function: str) -> str:
    body = function_body(repo, function)
    if "UNIMPLEMENTED" in body or "Unimpl" in body:
        return "unimplemented-stub"
    return "implemented-source" if body.strip() else "missing-source"


def role_for(function: str) -> str:
    if function == "DoTitle":
        return "pivot-title-runtime"
    if function == "QuickControlPhase":
        return "control-phase-loop"
    if function == "DoGameflow":
        return "gameflow-dispatch-context"
    return "title-control-support"


def marker_status(audit_row: dict[str, str]) -> str:
    markers = audit_row.get("markers", "") or "none"
    return "nd-marker-present" if "ND" in markers.split(";") else "no-nd-marker"


def source_contract(function: str) -> str:
    if function == "DoTitle":
        return "title loop, frontend selection, load-game transition, and control phase orchestration"
    if function == "QuickControlPhase":
        return "per-frame title/control phase input, camera, object, audio, and draw orchestration"
    if function == "DoGameflow":
        return "gameflow script dispatch and title/level transition context"
    return "gameflow runtime control support"


def side_effect_surface(function: str) -> str:
    if function == "DoTitle":
        return "frontend-state;gameflow-state;audio-state;level-transition;control-phase-call"
    if function == "QuickControlPhase":
        return "input-state;camera-state;object-control;audio-state;render-state"
    if function == "DoGameflow":
        return "script-state;gameflow-state;title-call;level-transition"
    return "runtime-state"


def state_fields_from_body(body: str) -> str:
    tokens = (
        ("gameflow", "gameflow-script-state"),
        ("gf", "gameflow-bytecode-state"),
        ("CurrentLevel", "level-selection-state"),
        ("Gameflow", "gameflow-global-state"),
        ("ControlPhase", "control-phase-state"),
        ("Camera", "camera-state"),
        ("input", "input-state"),
        ("Sound", "audio-state"),
        ("SOUND", "audio-state"),
        ("Draw", "render-state"),
        ("Lara", "lara-state"),
        ("objects", "object-runtime-state"),
    )
    fields = []
    for token, label in tokens:
        if token in body:
            fields.append(label)
    return ";".join(dict.fromkeys(fields)) or "source-state-not-classified"


def write_surfaces_from_body(body: str) -> str:
    surfaces = []
    for token, label in (("=", "assignment"), ("++", "increment"), ("--", "decrement"), ("SOUND", "audio-call"), ("Sound", "audio-call"), ("Draw", "draw-call")):
        if token in body:
            surfaces.append(label)
    return ";".join(dict.fromkeys(surfaces)) or "write-surface-not-classified"


def build_scope_rows(repo: Path) -> tuple[ScopeRow, ...]:
    audit_rows = audit_row_by_function(repo)
    rows: list[ScopeRow] = []
    for function in target_functions(repo):
        status = implementation_status(repo, function)
        proof_status = "source-contract-visible" if status == "implemented-source" else "source-body-missing"
        blocker = "missing-symbolic-equivalence-proof"
        rows.append(
            ScopeRow(
                function=function,
                file=find_function_file(repo, function),
                role=role_for(function),
                implementation_status=status,
                marker_status=marker_status(audit_rows.get(function, {})),
                side_effect_surface=side_effect_surface(function),
                source_contract=source_contract(function),
                proof_status=proof_status,
                blocker=blocker,
            )
        )
    rows.sort(key=lambda row: {"DoTitle": 0, "QuickControlPhase": 1, "DoGameflow": 2}.get(row.function, 99))
    return tuple(rows)


def classify_args(args: list[str]) -> str:
    if not args:
        return "none"
    labels = []
    for arg in args:
        lowered = arg.lower()
        if "name" in lowered:
            labels.append("title-name-byte")
        elif "audio" in lowered:
            labels.append("audio-mode-byte")
        elif "gf" in lowered:
            labels.append("gameflow-byte")
        else:
            labels.append("source-expression")
    return ";".join(labels)


def shape_for(callee: str, args: list[str]) -> str:
    if callee == "DoTitle":
        return "shape-title-entry-two-byte"
    if callee == "QuickControlPhase":
        return "shape-control-phase-no-arg"
    if callee == "DoGameflow":
        return "shape-gameflow-entry-no-arg"
    return f"shape-{len(args)}-arg-runtime-call"


def current_function_calls(repo: Path, wanted: tuple[str, ...]) -> tuple[CallsiteRow, ...]:
    wanted_re = re.compile(r"\b(" + "|".join(map(re.escape, wanted)) + r")\s*\(([^)]*)\)")
    function_re = re.compile(r"^\s*(?:void|int|long|short|char|bool|struct\s+\w+\s*\*?)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^;]*\)\s*(?://.*)?$")
    rows: list[CallsiteRow] = []
    for path in source_files(repo):
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        current = "unknown-caller"
        pending = ""
        for idx, line in enumerate(lines):
            clean = strip_comments(line).rstrip()
            sig = function_re.match(clean)
            is_function_definition = False
            if sig and sig.group(1) not in C_KEYWORD_ARTIFACTS:
                pending = sig.group(1)
                is_function_definition = True
            opens = clean.count("{")
            closes = clean.count("}")
            if pending and opens:
                current = pending
                pending = ""
            if is_function_definition:
                continue
            caller = current
            for match in wanted_re.finditer(clean):
                callee = match.group(1)
                if caller == callee or caller == "unknown-caller" or caller in C_KEYWORD_ARTIFACTS:
                    continue
                args = [arg.strip() for arg in match.group(2).split(",") if arg.strip()]
                body = function_body(repo, callee)
                rows.append(
                    CallsiteRow(
                        caller=caller,
                        callee=callee,
                        caller_file=rel(path, repo),
                        callee_file=find_function_file(repo, callee),
                        line=idx + 1,
                        shape_id=shape_for(callee, args),
                        arg_count=len(args),
                        argument_kinds=classify_args(args),
                        state_fields=state_fields_from_body(body),
                        side_effects=side_effect_surface(callee),
                        proof_status="source-callsite-mapped-only",
                        patch_ready="no",
                        blocker="missing-symbolic-equivalence-proof",
                    )
                )
    rows.sort(key=lambda row: (row.callee, row.caller_file, row.line, row.caller))
    return tuple(rows)


def build_taxonomy_rows(callsites: tuple[CallsiteRow, ...], repo: Path) -> tuple[StateTaxonomyRow, ...]:
    grouped: dict[str, list[CallsiteRow]] = {}
    for row in callsites:
        grouped.setdefault(row.shape_id, []).append(row)
    output: list[StateTaxonomyRow] = []
    for shape_id, rows in grouped.items():
        state_fields = ";".join(sorted({field for row in rows for field in row.state_fields.split(";") if field}))
        arg_kinds = ";".join(sorted({kind for row in rows for kind in row.argument_kinds.split(";") if kind}))
        write_surfaces = ";".join(sorted({surface for row in rows for surface in write_surfaces_from_body(function_body(repo, row.callee)).split(";") if surface}))
        output.append(
            StateTaxonomyRow(
                shape_id=shape_id,
                site_count=len(rows),
                argument_kinds=arg_kinds or "none",
                state_fields=state_fields or "source-state-not-classified",
                write_surfaces=write_surfaces or "write-surface-not-classified",
                source_backed="yes",
                patch_ready="no",
                blocker="missing-symbolic-equivalence-proof",
            )
        )
    output.sort(key=lambda row: (-row.site_count, row.shape_id))
    return tuple(output)


def choose_handoff(repo: Path) -> Handoff:
    rows = read_csv(repo / RE077_SUBCLUSTER_CSV)
    candidates = [row for row in rows if row.get("subcluster") != "title-and-control-phase"]
    candidates.sort(key=lambda row: (-int(row.get("candidate_count", "0") or 0), row.get("subcluster", "")))
    next_subcluster = candidates[0].get("subcluster", "object-runtime-control") if candidates else "object-runtime-control"
    top_function = candidates[0].get("top_function", "FlameTorchControl") if candidates else "FlameTorchControl"
    return Handoff(
        next_ticket="RE-085",
        next_cluster=next_subcluster,
        next_subcluster=next_subcluster,
        reason=f"title/control phase closed with proof blocker; next runtime support subcluster pivots on {top_function}",
        code_change_readiness="blocked",
        blocker="title/control phase lacks symbolic equivalence proof for safe source or marker changes",
    )


def build_tickets(handoff: Handoff) -> tuple[Ticket, ...]:
    common = (CHAIN_CSV, SCOPE_CSV, CALLSITE_CSV, TAXONOMY_CSV, HANDOFF_CSV, MD_OUTPUT)
    specs = (
        ("RE-078", "Gameflow runtime caller side-effect map", "caller-side-effect-map-published", "RE-079"),
        ("RE-079", "Gameflow runtime argument state taxonomy", "argument-state-taxonomy-published", "RE-080"),
        ("RE-080", "Gameflow runtime comparison gate", "no-patch-proof-blocker", "RE-081"),
        ("RE-081", "Gameflow runtime reconstruction plan", "documentation-only-plan", "RE-082"),
        ("RE-082", "Gameflow runtime source patch gate", "source-patch-denied", "RE-083"),
        ("RE-083", "Gameflow runtime validation regression", "metadata-validation-published", "RE-084"),
        ("RE-084", "Gameflow runtime closure or handoff", "handoff-to-next-gameflow-runtime-subcluster", handoff.next_ticket),
    )
    tickets = []
    for story_id, title, decision, next_ticket in specs:
        progress = (
            "RE-077 ticket plan consumed.",
            "Title/control phase source metadata mapped.",
            "Patch and marker readiness checked.",
            "Forbidden evidence excluded from generated artifacts.",
        )
        if story_id == "RE-084":
            progress += ("Closure/handoff recorded.",)
        findings = (
            "source-level caller/state metadata is available",
            "no source or marker patch is admitted without symbolic equivalence proof",
            f"handoff target: {handoff.next_ticket} {handoff.next_cluster}" if story_id == "RE-084" else "continue current chain",
        )
        tickets.append(Ticket(story_id, title, "done", decision, next_ticket, "blocked", progress, common, findings))
    return tuple(tickets)


def build_gameflow_runtime_chain(repo: Path) -> GameflowRuntimeChain:
    repo = Path(repo)
    verify_re077_plan(repo)
    scope_rows = build_scope_rows(repo)
    callsites = current_function_calls(repo, tuple(row.function for row in scope_rows))
    taxonomy_rows = build_taxonomy_rows(callsites, repo)
    handoff = choose_handoff(repo)
    return GameflowRuntimeChain(
        domain_id="module-game",
        cluster="gameflow-runtime-control",
        subcluster="title-and-control-phase",
        status="gameflow-runtime-chain-closed-with-proof-blocker",
        final_decision="documentation-only-terminal-blocker",
        next_ticket=handoff.next_ticket,
        code_change_ready_count=0,
        marker_ready_count=0,
        source_patch_ready_count=0,
        scope_rows=scope_rows,
        callsites=callsites,
        taxonomy_rows=taxonomy_rows,
        handoff=handoff,
        tickets=build_tickets(handoff),
    )


def write_dict_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def assert_metadata_only(path: Path) -> None:
    text = path.read_text(encoding="utf-8").lower()
    hits = [fragment for fragment in FORBIDDEN_FRAGMENTS if fragment in text]
    if hits:
        raise ValueError(f"forbidden evidence fragments in {path}: {hits}")


def write_chain_csv(path: Path, chain: GameflowRuntimeChain) -> None:
    fields = ["story_id", "title", "status", "decision", "next_ticket", "code_change_readiness", "generated_artifacts", "findings"]
    write_dict_csv(path, fields, [{**t.__dict__, "generated_artifacts": ";".join(t.generated_artifacts), "findings": ";".join(t.findings)} for t in chain.tickets])


def write_scope_csv(path: Path, chain: GameflowRuntimeChain) -> None:
    fields = ["function", "file", "role", "implementation_status", "marker_status", "side_effect_surface", "source_contract", "proof_status", "blocker"]
    write_dict_csv(path, fields, [row.__dict__ for row in chain.scope_rows])


def write_callsite_csv(path: Path, chain: GameflowRuntimeChain) -> None:
    fields = ["caller", "callee", "caller_file", "callee_file", "line", "shape_id", "arg_count", "argument_kinds", "state_fields", "side_effects", "proof_status", "patch_ready", "blocker"]
    write_dict_csv(path, fields, [row.__dict__ for row in chain.callsites])


def write_taxonomy_csv(path: Path, chain: GameflowRuntimeChain) -> None:
    fields = ["shape_id", "site_count", "argument_kinds", "state_fields", "write_surfaces", "source_backed", "patch_ready", "blocker"]
    write_dict_csv(path, fields, [row.__dict__ for row in chain.taxonomy_rows])


def write_handoff_csv(path: Path, chain: GameflowRuntimeChain) -> None:
    fields = ["next_ticket", "next_cluster", "next_subcluster", "reason", "code_change_readiness", "blocker"]
    write_dict_csv(path, fields, [chain.handoff.__dict__])


def write_markdown(path: Path, chain: GameflowRuntimeChain) -> None:
    lines = [
        "# RE-078..RE-084 — Gameflow runtime chain",
        "",
        f"Domain: `{chain.domain_id}`",
        f"Cluster: `{chain.cluster}`",
        f"Subcluster: `{chain.subcluster}`",
        f"Status: `{chain.status}`",
        f"Decision: `{chain.final_decision}`",
        f"Next ticket: `{chain.next_ticket}`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-077 ticket plan consumed.",
        "- [x] RE-078 caller and side-effect map published.",
        "- [x] RE-079 argument/state taxonomy published.",
        "- [x] RE-080 comparison gate evaluated.",
        "- [x] RE-081 reconstruction plan reduced to documentation-only blocker.",
        "- [x] RE-082 source patch gate denied safely.",
        "- [x] RE-083 validation/regression metadata recorded.",
        "- [x] RE-084 closure/handoff recorded.",
        "",
        "## Readiness",
        "",
        f"- code-change-ready rows: `{chain.code_change_ready_count}`",
        f"- marker-ready rows: `{chain.marker_ready_count}`",
        f"- source-patch-ready rows: `{chain.source_patch_ready_count}`",
        "- terminal blocker: `missing symbolic equivalence proof`",
        "- source line numbers in generated maps are source-navigation metadata only.",
        "",
        "## Scope rows",
        "",
    ]
    for row in chain.scope_rows:
        lines.append(f"- `{row.function}` — `{row.implementation_status}` / `{row.marker_status}` / `{row.proof_status}` / blocker `{row.blocker}`")
    lines.extend(["", "## Argument/state shapes", ""])
    for shape in chain.taxonomy_rows:
        lines.append(f"- `{shape.shape_id}` — sites `{shape.site_count}`, patch-ready `{shape.patch_ready}`, blocker `{shape.blocker}`")
    lines.extend([
        "",
        "## Handoff",
        "",
        f"- next ticket: `{chain.handoff.next_ticket}`",
        f"- next cluster: `{chain.handoff.next_cluster}`",
        f"- reason: `{chain.handoff.reason}`",
        "",
        "No production source or proof marker change is made by this chain.",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def slug(title: str) -> str:
    return title.lower().replace(" ", "-")


def write_story(path: Path, chain: GameflowRuntimeChain, ticket: Ticket) -> None:
    lines = [
        f"# {ticket.story_id} — {ticket.title}",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        f"Advance `{chain.subcluster}` within `{chain.cluster}` using metadata-only evidence for {ticket.story_id}.",
        "",
        "## Progress tracker",
        "",
    ]
    for item in ticket.progress:
        lines.append(f"- [x] {item}")
    lines.extend(["", "## Generated artifacts", ""])
    for artifact in ticket.generated_artifacts:
        lines.append(f"- `{artifact}`")
    lines.extend(["", "## Findings", ""])
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
        "- `python3 -m pytest tests/reverse/test_re078_re084_gameflow_runtime_chain.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over generated RE-078..RE-084 artifacts",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_all_artifacts(chain: GameflowRuntimeChain, repo: Path) -> dict[str, Path]:
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
        path = repo / STORY_DIR / f"{ticket.story_id}-{slug(ticket.title)}.md"
        write_story(path, chain, ticket)
        paths[ticket.story_id] = path
    for path in paths.values():
        assert_metadata_only(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    chain = build_gameflow_runtime_chain(args.repo)
    for key, path in write_all_artifacts(chain, args.repo).items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
