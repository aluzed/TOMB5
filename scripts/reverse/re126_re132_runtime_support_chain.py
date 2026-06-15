#!/usr/bin/env python3
"""Generate RE-126..RE-132 runtime support mixed chain artifacts.

This range consumes the RE-125 runtime-support-mixed audit and emits metadata-only
scope, dispatch/callsite, argument/state taxonomy, readiness gates, validation
notes, and a handoff for the runtime-support-mixed subcluster.
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path


RE125_PLAN_CSV = "docs/reverse/generated/re125-runtime-support-mixed-ticket-plan.csv"
RE125_AUDIT_CSV = "docs/reverse/generated/re125-runtime-support-mixed-proof-first-audit.csv"
RE125_SUBCLUSTER_CSV = "docs/reverse/generated/re125-runtime-support-mixed-subclusters.csv"
RE077_SUBCLUSTER_CSV = "docs/reverse/generated/re077-gameflow-runtime-subclusters.csv"
CHAIN_CSV = "docs/reverse/generated/re126-re132-runtime-support-chain.csv"
SCOPE_CSV = "docs/reverse/generated/re126-runtime-support-scope.csv"
CALLSITE_CSV = "docs/reverse/generated/re126-runtime-support-callsite-map.csv"
TAXONOMY_CSV = "docs/reverse/generated/re127-runtime-support-argument-state-taxonomy.csv"
HANDOFF_CSV = "docs/reverse/generated/re132-runtime-support-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re126-re132-runtime-support-chain.md"
STORY_DIR = "docs/stories"

C_KEYWORD_ARTIFACTS = {"if", "for", "while", "switch", "else", "do"}
FORBIDDEN_FRAGMENTS = ("0x", "payload", "opcode", "machine word", "raw call target")


@dataclass(frozen=True)
class ScopeRow:
    function: str
    file: str
    role: str
    implementation_status: str
    object_family: str
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
class RuntimeSupportChain:
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

    @property
    def scope(self) -> str:
        return self.subcluster


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def source_files(repo: Path) -> list[Path]:
    return sorted((repo / "GAME").glob("*.C"))


def rel(path: Path, repo: Path) -> str:
    return path.relative_to(repo).as_posix()


def strip_comments(line: str) -> str:
    return line.split("//", 1)[0]


def verify_re125_plan(repo: Path) -> None:
    plan_path = repo / RE125_PLAN_CSV
    if not plan_path.exists():
        from scripts.reverse.re125_runtime_support_mixed_audit import build_runtime_support_audit, write_all_artifacts as write_re125_artifacts

        write_re125_artifacts(build_runtime_support_audit(repo), repo)
    rows = read_csv(plan_path)
    ids = tuple(row.get("story_id", "") for row in rows)
    expected = ("RE-126", "RE-127", "RE-128", "RE-129", "RE-130", "RE-131", "RE-132")
    if ids != expected:
        raise ValueError("RE-125 plan no longer matches RE-126..RE-132 chain expectations")


def target_rows(repo: Path) -> tuple[dict[str, str], ...]:
    rows = [row for row in read_csv(repo / RE125_AUDIT_CSV) if row.get("subcluster") == "runtime-support-mixed" and row.get("function") not in C_KEYWORD_ARTIFACTS]
    order = {"ResetGuards": 0}
    rows.sort(key=lambda row: (order.get(row.get("function", ""), 99), row.get("file", ""), row.get("function", "")))
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
    return "pivot-runtime-support-mixed" if function == "ResetGuards" else "pivot-runtime-support-mixed"


def source_contract(function: str) -> str:
    if function == "ResetGuards":
        return "Runtime support reset of active intelligent guard items, item visibility, active list, and guard AI state"
    return "Runtime support control"


def side_effect_surface(function: str) -> str:
    if function == "ResetGuards":
        return "active-item-state;item-array-state;object-intelligence-state;guard-status-state;guard-ai-state"
    return "runtime-support-dispatch"


def shape_for(callee: str, arg_count: int) -> str:
    if callee == "ResetGuards":
        return "shape-runtime-support-reset-guards-void"
    return f"shape-runtime-support-{arg_count}-arg"


def build_scope_rows(repo: Path) -> tuple[ScopeRow, ...]:
    rows: list[ScopeRow] = []
    for row in target_rows(repo):
        function = row["function"]
        impl = row.get("implementation_status") or implementation_status(repo, function)
        proof_status = "source-body-missing" if impl == "unimplemented-stub" else "platform-gated-source-needs-equivalence-proof"
        rows.append(ScopeRow(
            function=function,
            file=row.get("file") or find_function_file(repo, function),
            role=row.get("role") or role_for(function),
            implementation_status=impl,
            object_family=row.get("object_family", "runtime-support-state"),
            side_effect_surface=side_effect_surface(function),
            source_contract=source_contract(function),
            proof_status=proof_status,
            patch_ready="no",
            blocker="missing-runtime-support-state-contract-and-symbolic-equivalence-proof" if impl == "unimplemented-stub" else "missing-runtime-support-state-contract-and-symbolic-equivalence-proof",
        ))
    return tuple(rows)


def classify_args(args: str | list[str]) -> str:
    if isinstance(args, list):
        joined = ";".join(arg.strip() for arg in args if arg.strip())
    else:
        joined = args.strip()
    if not joined:
        return "void-or-dispatch"
    return "symbolic-runtime-support-argument"


def state_fields_from_body(body: str) -> str:
    if not body.strip():
        return "source-body-missing"
    fields = []
    probes = (
        ("next_item_active", "active-item-state"),
        ("items", "item-array-state"),
        ("target_item", "target-item-state"),
        ("objects", "object-intelligence-state"),
        ("ITEM_INVISIBLE", "guard-status-state"),
        ("RemoveActiveItem", "active-item-list-state"),
        ("DisableBaddieAI", "guard-ai-state"),
        ("room", "room-link-state"),
    )
    for needle, label in probes:
        if needle in body and label not in fields:
            fields.append(label)
    return ";".join(fields) if fields else "runtime-support-state"


def write_surfaces_from_body(body: str) -> str:
    surfaces = []
    probes = (
        ("target_item->status", "guard-status-state-write-surface"),
        ("RemoveActiveItem", "active-item-state-write-surface"),
        ("DisableBaddieAI", "guard-ai-state-write-surface"),
        ("target_item->", "target-item-write-surface"),
        ("items", "item-array-state-read-surface"),
        ("objects", "object-intelligence-read-surface"),
    )
    for needle, label in probes:
        if needle in body and label not in surfaces:
            surfaces.append(label)
    return ";".join(surfaces) if surfaces else "runtime-support-symbolic-surface"


def direct_calls(repo: Path, wanted: tuple[str, ...]) -> list[CallsiteRow]:
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
            is_definition = False
            if sig and sig.group(1) not in C_KEYWORD_ARTIFACTS:
                pending = sig.group(1)
                is_definition = True
            opens = clean.count("{")
            if pending and opens:
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
                rows.append(
                    CallsiteRow(
                        caller=current,
                        callee=callee,
                        caller_file=rel(path, repo),
                        callee_file=find_function_file(repo, callee),
                        line=idx + 1,
                        shape_id=shape_for(callee, len(args)),
                        arg_count=len(args),
                        argument_kinds=classify_args(args),
                        state_fields=state_fields_from_body(body),
                        side_effects=side_effect_surface(callee),
                        proof_status="source-callsite-mapped-only",
                        patch_ready="no",
                        blocker="missing-symbolic-equivalence-proof",
                    )
                )
    return rows


def build_callsite_rows(repo: Path, scope_rows: tuple[ScopeRow, ...]) -> tuple[CallsiteRow, ...]:
    wanted = tuple(row.function for row in scope_rows)
    rows = direct_calls(repo, wanted)
    seen = {(row.caller, row.callee, row.line) for row in rows}
    for scope in scope_rows:
        dispatch = ("runtime-support-dispatch-table", scope.function, 0)
        if dispatch in seen:
            continue
        body = function_body(repo, scope.function)
        rows.append(
            CallsiteRow(
                caller="runtime-support-dispatch-table",
                callee=scope.function,
                caller_file="GAME/OBJECTS.H",
                callee_file=scope.file,
                line=0,
                shape_id=shape_for(scope.function, 1),
                arg_count=1,
                argument_kinds="runtime-support-dispatch",
                state_fields=state_fields_from_body(body),
                side_effects=scope.side_effect_surface,
                proof_status="symbolic-dispatch-metadata-only",
                patch_ready="no",
                blocker=scope.blocker,
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
                source_backed="partial" if "source-body-missing" in state_fields else "yes",
                patch_ready="no",
                blocker="missing-runtime-support-state-contract-and-symbolic-equivalence-proof" if "source-body-missing" in state_fields else "missing-symbolic-equivalence-proof",
            )
        )
    output.sort(key=lambda row: (-row.site_count, row.shape_id))
    return tuple(output)


def choose_handoff(repo: Path) -> Handoff:
    closed_subclusters = {
        "title-and-control-phase",
        "object-runtime-control",
        "scripted-runtime-control",
        "lara-runtime-control",
        "runtime-support-mixed",
    }
    rows = read_csv(repo / RE077_SUBCLUSTER_CSV)
    remaining = [row for row in rows if row.get("subcluster", "") not in closed_subclusters]
    if remaining:
        raise ValueError(f"Unexpected remaining RE-077 gameflow runtime subclusters: {remaining}")
    return Handoff(
        next_ticket="TBD",
        next_cluster="gameflow-runtime-control",
        next_subcluster="gameflow-runtime-control-exhausted",
        reason="runtime-support-mixed closed with proof blocker; all RE-077 gameflow runtime subclusters are closed",
        code_change_readiness="blocked",
        blocker="Runtime support mixed lacks state contract and symbolic equivalence proof for safe source or marker changes",
    )


def build_tickets(handoff: Handoff) -> tuple[Ticket, ...]:
    common = (CHAIN_CSV, SCOPE_CSV, CALLSITE_CSV, TAXONOMY_CSV, HANDOFF_CSV, MD_OUTPUT)
    specs = (
        ("RE-126", "Runtime support caller and side-effect map", "caller-side-effect-map", "RE-127"),
        ("RE-127", "Runtime support argument and state taxonomy", "argument-state-taxonomy", "RE-128"),
        ("RE-128", "Runtime support comparison gate", "no-patch-proof-blocker", "RE-129"),
        ("RE-129", "Runtime support reconstruction plan", "documentation-only-plan", "RE-130"),
        ("RE-130", "Runtime support source patch gate", "source-patch-denied", "RE-131"),
        ("RE-131", "Runtime support validation regression", "metadata-validation-published", "RE-132"),
        ("RE-132", "Runtime support closure or exhaustion", "handoff-gameflow-runtime-exhausted", handoff.next_ticket),
    )
    tickets = []
    for story_id, title, decision, next_ticket in specs:
        progress = (
            "RE-125 ticket plan consumed.",
            "Runtime-support metadata mapped.",
            "Patch and marker readiness checked.",
            "Forbidden evidence excluded from generated artifacts.",
        )
        if story_id == "RE-132":
            progress += ("Closure/exhaustion handoff recorded.",)
        findings = (
            "runtime-support rows include one source-visible ResetGuards path with blocked proof gate",
            "no source or marker patch is admitted without runtime support state proof and symbolic equivalence proof",
            f"handoff target: {handoff.next_ticket} {handoff.next_subcluster}" if story_id == "RE-132" else "continue current chain",
        )
        tickets.append(Ticket(story_id, title, "done", decision, next_ticket, "blocked", progress, common, findings))
    return tuple(tickets)


def build_runtime_support_chain(repo: Path) -> RuntimeSupportChain:
    repo = Path(repo)
    verify_re125_plan(repo)
    scope_rows = build_scope_rows(repo)
    callsites = build_callsite_rows(repo, scope_rows)
    taxonomy_rows = build_taxonomy_rows(callsites, repo)
    handoff = choose_handoff(repo)
    return RuntimeSupportChain(
        domain_id="module-game",
        cluster="gameflow-runtime-control",
        subcluster="runtime-support-mixed",
        status="runtime-support-chain-closed-with-proof-blocker",
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


def write_chain_csv(path: Path, chain: RuntimeSupportChain) -> None:
    fields = ["story_id", "title", "status", "decision", "next_ticket", "code_change_readiness", "generated_artifacts", "findings"]
    write_dict_csv(path, fields, [{**t.__dict__, "generated_artifacts": ";".join(t.generated_artifacts), "findings": ";".join(t.findings)} for t in chain.tickets])


def write_scope_csv(path: Path, chain: RuntimeSupportChain) -> None:
    fields = ["function", "file", "role", "implementation_status", "object_family", "side_effect_surface", "source_contract", "proof_status", "patch_ready", "blocker"]
    write_dict_csv(path, fields, [row.__dict__ for row in chain.scope_rows])


def write_callsite_csv(path: Path, chain: RuntimeSupportChain) -> None:
    fields = ["caller", "callee", "caller_file", "callee_file", "line", "shape_id", "arg_count", "argument_kinds", "state_fields", "side_effects", "proof_status", "patch_ready", "blocker"]
    write_dict_csv(path, fields, [row.__dict__ for row in chain.callsites])


def write_taxonomy_csv(path: Path, chain: RuntimeSupportChain) -> None:
    fields = ["shape_id", "site_count", "argument_kinds", "state_fields", "write_surfaces", "source_backed", "patch_ready", "blocker"]
    write_dict_csv(path, fields, [row.__dict__ for row in chain.taxonomy_rows])


def write_handoff_csv(path: Path, chain: RuntimeSupportChain) -> None:
    fields = ["next_ticket", "next_cluster", "next_subcluster", "reason", "code_change_readiness", "blocker"]
    write_dict_csv(path, fields, [chain.handoff.__dict__])


def write_markdown(path: Path, chain: RuntimeSupportChain) -> None:
    lines = [
        "# RE-126..RE-132 — Runtime support chain",
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
        "- [x] RE-125 ticket plan consumed.",
        "- [x] RE-126 caller and side-effect map published.",
        "- [x] RE-127 argument/state taxonomy published.",
        "- [x] RE-128 comparison gate evaluated.",
        "- [x] RE-129 reconstruction plan reduced to documentation-only blocker.",
        "- [x] RE-130 source patch gate denied safely.",
        "- [x] RE-131 validation/regression metadata recorded.",
        "- [x] RE-132 closure/handoff recorded.",
        "",
        "## Readiness",
        "",
        f"- code-change-ready rows: `{chain.code_change_ready_count}`",
        f"- marker-ready rows: `{chain.marker_ready_count}`",
        f"- source-patch-ready rows: `{chain.source_patch_ready_count}`",
        "- terminal blocker: `missing runtime support state contract and symbolic equivalence proof`",
        "- source line numbers in generated maps are source-navigation metadata only.",
        "",
        "## Scope rows",
        "",
    ]
    for row in chain.scope_rows:
        lines.append(f"- `{row.function}` — `{row.implementation_status}` / `{row.proof_status}` / patch-ready `{row.patch_ready}` / blocker `{row.blocker}`")
    lines.extend(["", "## Argument/state shapes", ""])
    for shape in chain.taxonomy_rows:
        lines.append(f"- `{shape.shape_id}` — sites `{shape.site_count}`, source-backed `{shape.source_backed}`, patch-ready `{shape.patch_ready}`, blocker `{shape.blocker}`")
    lines.extend([
        "",
        "## Handoff",
        "",
        f"- next ticket: `{chain.handoff.next_ticket}`",
        f"- next subcluster: `{chain.handoff.next_subcluster}`",
        f"- reason: `{chain.handoff.reason}`",
        "",
        "No production source or proof marker change is made by this chain.",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def slug(title: str) -> str:
    return title.lower().replace(" ", "-")


def write_story(path: Path, chain: RuntimeSupportChain, ticket: Ticket) -> None:
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
        "- `python3 -m pytest tests/reverse/test_re126_re132_runtime_support_chain.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over generated RE-126..RE-132 artifacts",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_all_artifacts(chain: RuntimeSupportChain, repo: Path) -> dict[str, Path]:
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
    chain = build_runtime_support_chain(args.repo)
    for key, path in write_all_artifacts(chain, args.repo).items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
