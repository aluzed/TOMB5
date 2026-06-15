#!/usr/bin/env python3
"""Generate RE-070..RE-076 lara movement chain artifacts.

This range consumes the RE-069 lara movement audit and emits metadata-only
caller maps, argument/state taxonomy, readiness gates, validation notes, and a
handoff. It intentionally publishes symbolic summaries only.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


RE069_PLAN_CSV = "docs/reverse/generated/re069-lara-movement-ticket-plan.csv"
RE069_AUDIT_CSV = "docs/reverse/generated/re069-lara-movement-proof-first-audit.csv"
RE069_SUBCLUSTER_CSV = "docs/reverse/generated/re069-lara-movement-subclusters.csv"
RE061_CLUSTER_CSV = "docs/reverse/generated/re061-module-game-clusters.csv"
CHAIN_CSV = "docs/reverse/generated/re070-re076-lara-movement-chain.csv"
SCOPE_CSV = "docs/reverse/generated/re070-lara-movement-scope.csv"
CALLSITE_CSV = "docs/reverse/generated/re070-lara-movement-callsite-map.csv"
TAXONOMY_CSV = "docs/reverse/generated/re071-lara-movement-argument-state-taxonomy.csv"
HANDOFF_CSV = "docs/reverse/generated/re076-lara-movement-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re070-re076-lara-movement-chain.md"
STORY_DIR = "docs/stories"

C_KEYWORD_ARTIFACTS = {"if", "for", "while", "switch", "else", "do"}
FORBIDDEN_FRAGMENTS = ("0x", "payload", "opcode", "machine word", "raw call target")


@dataclass(frozen=True)
class ScopeRow:
    function: str
    file: str
    role: str
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
    arg1_kind: str
    arg2_kind: str
    state_fields: str
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
    state_fields: str
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
class LaraMovementChain:
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
    argument_shapes: tuple[ArgumentShape, ...]
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


def target_functions(repo: Path) -> tuple[str, ...]:
    rows = read_csv(repo / RE069_AUDIT_CSV)
    targets = [row["function"] for row in rows if row.get("subcluster") == "ledge-and-vault-tests" and row.get("function") not in C_KEYWORD_ARTIFACTS]
    targets.sort(key=lambda name: (0 if name == "TestLaraSlide" else 1, name))
    return tuple(targets)


def find_function_file(repo: Path, function: str) -> str:
    pattern = re.compile(rf"\b{re.escape(function)}\s*\(")
    for path in source_files(repo):
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            clean = strip_comments(line).strip()
            if not pattern.search(clean) or clean.endswith(";"):
                continue
            if clean.startswith(("if", "while", "for", "return", "else")):
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
    if function == "TestLaraSlide":
        return "pivot"
    if "Vault" in function:
        return "ledge-vault-predicate"
    if "Hang" in function or "Corner" in function or "Climb" in function:
        return "corner-predicate"
    return "movement-predicate"


def source_contract(function: str) -> str:
    if "Slide" in function:
        return "item and collision predicate for slope/slide movement"
    if "Vault" in function:
        return "item and collision predicate for vault transition"
    if "Hang" in function or "Corner" in function or "Climb" in function:
        return "item and collision predicate for ledge/corner transition"
    return "item and collision movement predicate"


def side_effect_surface(function: str) -> str:
    if "Slide" in function:
        return "collision-floor-query;movement-state-decision"
    if "Vault" in function:
        return "collision-height-query;animation-transition-decision"
    if "Hang" in function or "Corner" in function or "Climb" in function:
        return "corner-probe;orientation-transition-decision"
    return "movement-state-decision"


def state_fields_from_body(body: str) -> str:
    fields = []
    for token, label in (("item->pos", "item-position"), ("item->anim_number", "item-animation"), ("item->goal_anim_state", "item-goal-state"), ("item->current_anim_state", "item-current-state"), ("coll->", "collision-info"), ("lara.", "lara-global-state")):
        if token in body:
            fields.append(label)
    return ";".join(dict.fromkeys(fields)) or "source-state-not-classified"


def build_scope_rows(repo: Path) -> tuple[ScopeRow, ...]:
    rows: list[ScopeRow] = []
    for function in target_functions(repo):
        status = implementation_status(repo, function)
        proof_status = "source-contract-visible" if status == "implemented-source" else "source-body-missing"
        rows.append(ScopeRow(function, find_function_file(repo, function), role_for(function), status, side_effect_surface(function), source_contract(function), proof_status, "missing-non-raw-binary-equivalence"))
    rows.sort(key=lambda row: (0 if row.function == "TestLaraSlide" else 1, row.file, row.function))
    return tuple(rows)


def current_function_calls(repo: Path, wanted: tuple[str, ...]) -> tuple[CallsiteRow, ...]:
    wanted_re = re.compile(r"\b(" + "|".join(map(re.escape, wanted)) + r")\s*\(([^)]*)\)")
    function_re = re.compile(r"^\s*(?:void|int|long|short|char|bool|struct\s+\w+\s*\*?)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^;]*\)\s*(?://.*)?$")
    rows: list[CallsiteRow] = []
    for path in source_files(repo):
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        current = "unknown-caller"
        pending = ""
        depth = 0
        for idx, line in enumerate(lines):
            clean = strip_comments(line).rstrip()
            sig = function_re.match(clean)
            if sig and sig.group(1) not in C_KEYWORD_ARTIFACTS:
                pending = sig.group(1)
            opens = clean.count("{")
            closes = clean.count("}")
            if pending and opens:
                current = pending
                pending = ""
            caller = current
            depth += opens - closes
            for match in wanted_re.finditer(clean):
                callee = match.group(1)
                if caller == callee or caller == "unknown-caller" or caller in C_KEYWORD_ARTIFACTS:
                    continue
                args = [arg.strip() for arg in match.group(2).split(",") if arg.strip()]
                shape_id = "shape-item-coll-predicate" if len(args) == 2 and "item" in args[0] and "coll" in args[1] else "shape-movement-predicate"
                body = function_body(repo, callee)
                rows.append(CallsiteRow(caller, callee, rel(path, repo), find_function_file(repo, callee), idx + 1, shape_id, "item-pointer" if args else "none", "collision-info-pointer" if len(args) > 1 else "none", state_fields_from_body(body), side_effect_surface(callee), "source-callsite-mapped-only", "no", "missing-non-raw-binary-equivalence"))
    rows.sort(key=lambda row: (row.callee, row.caller_file, row.line, row.caller))
    return tuple(rows)


def build_argument_shapes(callsites: tuple[CallsiteRow, ...]) -> tuple[ArgumentShape, ...]:
    grouped: dict[str, list[CallsiteRow]] = {}
    for row in callsites:
        grouped.setdefault(row.shape_id, []).append(row)
    output: list[ArgumentShape] = []
    for shape_id, rows in grouped.items():
        state_fields = ";".join(sorted({field for row in rows for field in row.state_fields.split(";") if field}))
        first = rows[0]
        output.append(ArgumentShape(shape_id, len(rows), first.arg1_kind, first.arg2_kind, state_fields, "yes", "no", "missing-non-raw-binary-equivalence"))
    output.sort(key=lambda row: (-row.site_count, row.shape_id))
    return tuple(output)


def verify_re069_plan(repo: Path) -> None:
    rows = read_csv(repo / RE069_PLAN_CSV)
    ids = tuple(row.get("story_id", "") for row in rows)
    expected = ("RE-070", "RE-071", "RE-072", "RE-073", "RE-074", "RE-075", "RE-076")
    if ids != expected:
        raise ValueError("RE-069 plan no longer matches RE-070..RE-076 chain expectations")


def choose_handoff(repo: Path) -> Handoff:
    rows = read_csv(repo / RE061_CLUSTER_CSV)
    closed = {"debris-object-breakage", "lara-movement-support"}
    candidates = [row for row in rows if row.get("cluster") not in closed]
    candidates.sort(key=lambda row: (0 if "nd-marker" in row.get("readiness", "") else 1, -int(row.get("candidate_count", "0") or 0), row.get("cluster", "")))
    next_cluster = candidates[0].get("cluster", "gameflow-runtime-control") if candidates else "gameflow-runtime-control"
    return Handoff("RE-077", next_cluster, "initial-subcluster-terminal-blocker", "blocked", "lara movement subcluster lacks non-raw binary equivalence proof for safe patching")


def build_tickets(handoff: Handoff) -> tuple[Ticket, ...]:
    common = (CHAIN_CSV, SCOPE_CSV, CALLSITE_CSV, TAXONOMY_CSV, HANDOFF_CSV, MD_OUTPUT)
    specs = (
        ("RE-070", "Lara movement caller side-effect map", "caller-side-effect-map-published", "RE-071"),
        ("RE-071", "Lara movement argument state taxonomy", "argument-state-taxonomy-published", "RE-072"),
        ("RE-072", "Lara movement comparison gate", "no-patch-proof-blocker", "RE-073"),
        ("RE-073", "Lara movement reconstruction plan", "documentation-only-plan", "RE-074"),
        ("RE-074", "Lara movement source patch gate", "source-patch-denied", "RE-075"),
        ("RE-075", "Lara movement validation regression", "metadata-validation-published", "RE-076"),
        ("RE-076", "Lara movement closure or handoff", "handoff-to-next-module-game-cluster", handoff.next_ticket),
    )
    tickets = []
    for story_id, title, decision, next_ticket in specs:
        progress = ("RE-069 plan consumed.", "Source-level movement metadata mapped.", "Patch readiness checked.", "Forbidden raw evidence excluded.")
        if story_id == "RE-076":
            progress += ("Closure/handoff recorded.",)
        tickets.append(Ticket(story_id, title, "done", decision, next_ticket, "blocked", progress, common, ("source-level caller/state metadata is available", "no source or marker patch is admitted without non-raw binary equivalence proof", f"handoff target: {handoff.next_ticket} {handoff.next_cluster}" if story_id == "RE-076" else "continue current chain")))
    return tuple(tickets)


def build_lara_movement_chain(repo: Path) -> LaraMovementChain:
    repo = Path(repo)
    verify_re069_plan(repo)
    scope_rows = build_scope_rows(repo)
    callsites = current_function_calls(repo, tuple(row.function for row in scope_rows))
    argument_shapes = build_argument_shapes(callsites)
    handoff = choose_handoff(repo)
    return LaraMovementChain("module-game", "lara-movement-support", "ledge-and-vault-tests", "lara-movement-chain-closed-with-proof-blocker", "documentation-only-terminal-blocker", handoff.next_ticket, 0, 0, 0, scope_rows, callsites, argument_shapes, handoff, build_tickets(handoff))


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
        raise ValueError(f"forbidden raw evidence fragments in {path}: {hits}")


def write_chain_csv(path: Path, chain: LaraMovementChain) -> None:
    fields = ["story_id", "title", "status", "decision", "next_ticket", "code_change_readiness", "generated_artifacts", "findings"]
    write_dict_csv(path, fields, [{**t.__dict__, "generated_artifacts": ";".join(t.generated_artifacts), "findings": ";".join(t.findings)} for t in chain.tickets])


def write_scope_csv(path: Path, chain: LaraMovementChain) -> None:
    fields = ["function", "file", "role", "implementation_status", "side_effect_surface", "source_contract", "proof_status", "blocker"]
    write_dict_csv(path, fields, [row.__dict__ for row in chain.scope_rows])


def write_callsite_csv(path: Path, chain: LaraMovementChain) -> None:
    fields = ["caller", "callee", "caller_file", "callee_file", "line", "shape_id", "arg1_kind", "arg2_kind", "state_fields", "side_effects", "proof_status", "patch_ready", "blocker"]
    write_dict_csv(path, fields, [row.__dict__ for row in chain.callsites])


def write_taxonomy_csv(path: Path, chain: LaraMovementChain) -> None:
    fields = ["shape_id", "site_count", "arg1_kind", "arg2_kind", "state_fields", "source_backed", "patch_ready", "blocker"]
    write_dict_csv(path, fields, [row.__dict__ for row in chain.argument_shapes])


def write_handoff_csv(path: Path, chain: LaraMovementChain) -> None:
    fields = ["next_ticket", "next_cluster", "reason", "code_change_readiness", "blocker"]
    write_dict_csv(path, fields, [chain.handoff.__dict__])


def write_markdown(path: Path, chain: LaraMovementChain) -> None:
    lines = ["# RE-070..RE-076 — Lara movement chain", "", f"Domain: `{chain.domain_id}`", f"Cluster: `{chain.cluster}`", f"Subcluster: `{chain.subcluster}`", f"Status: `{chain.status}`", f"Decision: `{chain.final_decision}`", f"Next ticket: `{chain.next_ticket}`", "", "## Progress tracker", "", "- [x] RE-069 ticket plan consumed.", "- [x] RE-070 caller and side-effect map published.", "- [x] RE-071 argument/state taxonomy published.", "- [x] RE-072 comparison gate evaluated.", "- [x] RE-073 reconstruction plan reduced to documentation-only blocker.", "- [x] RE-074 source patch gate denied safely.", "- [x] RE-075 validation/regression metadata recorded.", "- [x] RE-076 closure/handoff recorded.", "", "## Readiness", "", f"- code-change-ready rows: `{chain.code_change_ready_count}`", f"- marker-ready rows: `{chain.marker_ready_count}`", f"- source-patch-ready rows: `{chain.source_patch_ready_count}`", "- terminal blocker: `missing non-raw binary equivalence proof`", "", "## Scope rows", ""]
    for row in chain.scope_rows:
        lines.append(f"- `{row.function}` — `{row.implementation_status}` / `{row.proof_status}` / blocker `{row.blocker}`")
    lines.extend(["", "## Argument shapes", ""])
    for shape in chain.argument_shapes:
        lines.append(f"- `{shape.shape_id}` — sites `{shape.site_count}`, patch-ready `{shape.patch_ready}`, blocker `{shape.blocker}`")
    lines.extend(["", "## Handoff", "", f"- next ticket: `{chain.handoff.next_ticket}`", f"- next cluster: `{chain.handoff.next_cluster}`", f"- reason: `{chain.handoff.reason}`", "", "No production source or proof marker change is made by this chain."])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def slug(title: str) -> str:
    return title.lower().replace(" ", "-")


def write_story(path: Path, chain: LaraMovementChain, ticket: Ticket) -> None:
    lines = [f"# {ticket.story_id} — {ticket.title}", "", "Status: Done", "", "## Goal", "", f"Advance `{chain.subcluster}` within `{chain.cluster}` using metadata-only evidence for {ticket.story_id}.", "", "## Progress tracker", ""]
    for item in ticket.progress:
        lines.append(f"- [x] {item}")
    lines.extend(["", "## Generated artifacts", ""])
    for artifact in ticket.generated_artifacts:
        lines.append(f"- `{artifact}`")
    lines.extend(["", "## Findings", ""])
    for finding in ticket.findings:
        lines.append(f"- {finding}")
    lines.extend(["", "## Readiness decision", "", f"- decision: `{ticket.decision}`", f"- code change readiness: `{ticket.code_change_readiness}`", f"- next ticket: `{ticket.next_ticket}`", "", "Do not patch production source or add/remove proof markers from this story alone.", "", "## Validation", "", "- `python3 -m pytest tests/reverse/test_re070_re076_lara_movement_chain.py -q`", "- `python3 -m pytest tests/reverse -q`", "- metadata-only guard over generated RE-070..RE-076 artifacts"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_all_artifacts(chain: LaraMovementChain, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {"chain_csv": repo / CHAIN_CSV, "scope_csv": repo / SCOPE_CSV, "callsite_csv": repo / CALLSITE_CSV, "taxonomy_csv": repo / TAXONOMY_CSV, "handoff_csv": repo / HANDOFF_CSV, "md": repo / MD_OUTPUT}
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
    chain = build_lara_movement_chain(args.repo)
    for key, path in write_all_artifacts(chain, args.repo).items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
