#!/usr/bin/env python3
"""Generate RE-134..RE-140 gameplay mixed chain artifacts.

This range consumes the RE-133 gameplay-mixed audit and emits metadata-only
scope, dispatch/callsite, argument/state taxonomy, readiness gates, validation
notes, and a handoff for the gameplay-mixed subcluster.
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path


RE133_PLAN_CSV = "docs/reverse/generated/re133-gameplay-mixed-ticket-plan.csv"
RE133_AUDIT_CSV = "docs/reverse/generated/re133-gameplay-mixed-proof-first-audit.csv"
RE133_CLUSTER_CSV = "docs/reverse/generated/re133-gameplay-mixed-clusters.csv"
RE061_CLUSTER_CSV = "docs/reverse/generated/re061-module-game-clusters.csv"
CHAIN_CSV = "docs/reverse/generated/re134-re140-gameplay-mixed-chain.csv"
SCOPE_CSV = "docs/reverse/generated/re134-gameplay-mixed-scope.csv"
CALLSITE_CSV = "docs/reverse/generated/re134-gameplay-mixed-callsite-map.csv"
TAXONOMY_CSV = "docs/reverse/generated/re135-gameplay-mixed-argument-state-taxonomy.csv"
HANDOFF_CSV = "docs/reverse/generated/re140-gameplay-mixed-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re134-re140-gameplay-mixed-chain.md"
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
class GameplayMixedChain:
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


def verify_re133_plan(repo: Path) -> None:
    plan_path = repo / RE133_PLAN_CSV
    if not plan_path.exists():
        from scripts.reverse.re133_gameplay_mixed_audit import build_gameplay_mixed_audit, write_all_artifacts as write_re133_artifacts

        write_re133_artifacts(build_gameplay_mixed_audit(repo), repo)
    rows = read_csv(plan_path)
    ids = tuple(row.get("story_id", "") for row in rows)
    expected = ("RE-134", "RE-135", "RE-136", "RE-137", "RE-138", "RE-139", "RE-140")
    if ids != expected:
        raise ValueError("RE-133 plan no longer matches RE-134..RE-140 chain expectations")


def target_rows(repo: Path) -> tuple[dict[str, str], ...]:
    rows = [row for row in read_csv(repo / RE133_AUDIT_CSV) if row.get("cluster") == "gameplay-mixed" and row.get("function") not in C_KEYWORD_ARTIFACTS]
    order = {
        "Load_and_Init_Cutseq": 0,
        "CreateZone": 1,
        "special4_init": 2,
        "init_water_table": 3,
        "InitialiseSqrtTable": 4,
        "InitTarget": 5,
        "InitBinoculars": 6,
        "InitialiseFootPrints": 7,
        "LoadLevel": 8,
        "EscapeBox": 9,
        "InitPackNodes": 10,
    }
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


def implementation_status(repo: Path, function: str) -> str:
    body = function_body(repo, function)
    if "UNIMPLEMENTED" in body or "Unimpl" in body:
        return "unimplemented-stub"
    return "implemented-source" if body.strip() else "missing-source"


def role_for(function: str) -> str:
    return "pivot-gameplay-mixed" if function == "Load_and_Init_Cutseq" else "gameplay-mixed-support"


def source_contract(function: str) -> str:
    contracts = {
        "Load_and_Init_Cutseq": "Gameplay cutscene loading and cutscene actor initialization state",
        "CreateZone": "Gameplay zone and creature pathing setup state",
        "special4_init": "Gameplay special cutscene initialization state",
        "init_water_table": "Gameplay water table setup state",
        "InitialiseSqrtTable": "Gameplay sqrt table setup state",
        "InitTarget": "Gameplay target setup state",
        "InitBinoculars": "Gameplay binocular setup state",
        "InitialiseFootPrints": "Gameplay footprint setup state",
        "LoadLevel": "Gameplay level load orchestration state",
        "EscapeBox": "Gameplay AI escape box state",
        "InitPackNodes": "Gameplay pack node initialization state",
    }
    return contracts.get(function, "Gameplay mixed source contract")


def side_effect_surface(function: str) -> str:
    if function == "Load_and_Init_Cutseq":
        return "cutscene-state;camera-state;lara-position-state;file-load-state"
    if function == "CreateZone":
        return "zone-state;creature-state;room-state"
    if function in {"init_water_table", "InitialiseSqrtTable", "InitTarget", "InitBinoculars", "InitialiseFootPrints", "LoadLevel", "InitPackNodes"}:
        return "setup-table-state;level-load-state;gameplay-global-state"
    if function == "special4_init":
        return "cutscene-state;special-sequence-state"
    if function == "EscapeBox":
        return "ai-pathing-state;box-state"
    return "gameplay-mixed-state"


def shape_for(callee: str, arg_count: int) -> str:
    if callee == "Load_and_Init_Cutseq":
        return "shape-gameplay-mixed-cutseq-number"
    if callee == "CreateZone":
        return "shape-gameplay-mixed-item-pointer"
    if arg_count == 0:
        return "shape-gameplay-mixed-void-setup"
    return f"shape-gameplay-mixed-{arg_count}-arg"


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
            object_family=row.get("object_family", "gameplay-state"),
            side_effect_surface=side_effect_surface(function),
            source_contract=source_contract(function),
            proof_status=proof_status,
            patch_ready="no",
            blocker="missing-gameplay-mixed-state-contract-and-symbolic-equivalence-proof" if impl == "unimplemented-stub" else "missing-gameplay-mixed-state-contract-and-symbolic-equivalence-proof",
        ))
    return tuple(rows)


def classify_args(args: str | list[str]) -> str:
    if isinstance(args, list):
        joined = ";".join(arg.strip() for arg in args if arg.strip())
    else:
        joined = args.strip()
    if not joined:
        return "void-or-dispatch"
    if "cutseq" in joined or "num" in joined:
        return "cutscene-number"
    if "item" in joined:
        return "item-pointer"
    return "symbolic-gameplay-argument"


def state_fields_from_body(body: str) -> str:
    if not body.strip():
        return "source-body-missing"
    fields = []
    probes = (
        ("GLOBAL_cutme", "cutscene-state"),
        ("cutseq", "cutscene-state"),
        ("camera", "camera-state"),
        ("lara_item", "lara-position-state"),
        ("CreateZone", "zone-state"),
        ("zone", "zone-state"),
        ("creature", "creature-state"),
        ("WaterTable", "water-table-state"),
        ("OurSqrt", "sqrt-table-state"),
        ("Level", "level-load-state"),
        ("LoadLevel", "level-load-state"),
        ("InitPackNodes", "pack-node-state"),
        ("footprint", "footprint-state"),
        ("Binocular", "binocular-state"),
        ("target", "target-state"),
        ("box", "box-state"),
    )
    for needle, label in probes:
        if needle in body and label not in fields:
            fields.append(label)
    return ";".join(fields) if fields else "gameplay-mixed-state"


def write_surfaces_from_body(body: str) -> str:
    surfaces = []
    probes = (
        ("GLOBAL_cutme", "cutscene-write-surface"),
        ("camera", "camera-write-surface"),
        ("WaterTable", "water-table-write-surface"),
        ("OurSqrt", "sqrt-table-write-surface"),
        ("zone", "zone-write-surface"),
        ("creature", "creature-write-surface"),
        ("LoadLevel", "level-load-write-surface"),
        ("InitPackNodes", "pack-node-write-surface"),
    )
    for needle, label in probes:
        if needle in body and label not in surfaces:
            surfaces.append(label)
    return ";".join(surfaces) if surfaces else "gameplay-mixed-symbolic-surface"


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
        dispatch = ("gameplay-mixed-dispatch-table", scope.function, 0)
        if dispatch in seen:
            continue
        body = function_body(repo, scope.function)
        rows.append(
            CallsiteRow(
                caller="gameplay-mixed-dispatch-table",
                callee=scope.function,
                caller_file="GAME/OBJECTS.H",
                callee_file=scope.file,
                line=0,
                shape_id=shape_for(scope.function, 1),
                arg_count=1,
                argument_kinds="gameplay-mixed-dispatch",
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
                blocker="missing-gameplay-mixed-state-contract-and-symbolic-equivalence-proof" if "source-body-missing" in state_fields else "missing-symbolic-equivalence-proof",
            )
        )
    output.sort(key=lambda row: (-row.site_count, row.shape_id))
    return tuple(output)


def choose_handoff(repo: Path) -> Handoff:
    closed_clusters = {
        "debris-object-breakage",
        "lara-movement-support",
        "gameflow-runtime-control",
        "gameplay-mixed",
    }
    rows = read_csv(repo / RE061_CLUSTER_CSV)
    remaining = [row for row in rows if row.get("cluster", "") not in closed_clusters]
    if not remaining:
        raise ValueError("No remaining module-game cluster after gameplay-mixed")
    nxt = remaining[0]
    if nxt.get("cluster") != "object-interaction" or nxt.get("top_function") != "FindPlinth":
        raise ValueError(f"Unexpected next module-game cluster after gameplay-mixed: {nxt}")
    return Handoff(
        next_ticket="RE-141",
        next_cluster="object-interaction",
        next_subcluster="object-interaction",
        reason="gameplay-mixed closed with proof blocker; next RE-061 module-game cluster is object-interaction with FindPlinth pivot",
        code_change_readiness="blocked",
        blocker="Gameplay mixed lacks state contract and symbolic equivalence proof for safe source or marker changes",
    )


def build_tickets(handoff: Handoff) -> tuple[Ticket, ...]:
    common = (CHAIN_CSV, SCOPE_CSV, CALLSITE_CSV, TAXONOMY_CSV, HANDOFF_CSV, MD_OUTPUT)
    specs = (
        ("RE-134", "Gameplay mixed caller and side-effect map", "caller-side-effect-map", "RE-135"),
        ("RE-135", "Gameplay mixed argument and state taxonomy", "argument-state-taxonomy", "RE-136"),
        ("RE-136", "Gameplay mixed comparison gate", "no-patch-proof-blocker", "RE-137"),
        ("RE-137", "Gameplay mixed reconstruction plan", "documentation-only-plan", "RE-138"),
        ("RE-138", "Gameplay mixed source patch gate", "source-patch-denied", "RE-139"),
        ("RE-139", "Gameplay mixed validation regression", "metadata-validation-published", "RE-140"),
        ("RE-140", "Gameplay mixed closure or handoff", "handoff-to-object-interaction", handoff.next_ticket),
    )
    tickets = []
    for story_id, title, decision, next_ticket in specs:
        progress = (
            "RE-133 ticket plan consumed.",
            "Gameplay-mixed metadata mapped.",
            "Patch and marker readiness checked.",
            "Forbidden evidence excluded from generated artifacts.",
        )
        if story_id == "RE-140":
            progress += ("Object-interaction handoff recorded.",)
        findings = (
            "gameplay-mixed rows remain blocked by missing state contract and symbolic equivalence proof",
            "no source or marker patch is admitted without gameplay mixed state proof and symbolic equivalence proof",
            f"handoff target: {handoff.next_ticket} {handoff.next_cluster}" if story_id == "RE-140" else "continue current chain",
        )
        tickets.append(Ticket(story_id, title, "done", decision, next_ticket, "blocked", progress, common, findings))
    return tuple(tickets)


def build_gameplay_mixed_chain(repo: Path) -> GameplayMixedChain:
    repo = Path(repo)
    verify_re133_plan(repo)
    scope_rows = build_scope_rows(repo)
    callsites = build_callsite_rows(repo, scope_rows)
    taxonomy_rows = build_taxonomy_rows(callsites, repo)
    handoff = choose_handoff(repo)
    return GameplayMixedChain(
        domain_id="module-game",
        cluster="gameplay-mixed",
        subcluster="gameplay-mixed",
        status="gameplay-mixed-chain-closed-with-proof-blocker",
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


def write_chain_csv(path: Path, chain: GameplayMixedChain) -> None:
    fields = ["story_id", "title", "status", "decision", "next_ticket", "code_change_readiness", "generated_artifacts", "findings"]
    write_dict_csv(path, fields, [{**t.__dict__, "generated_artifacts": ";".join(t.generated_artifacts), "findings": ";".join(t.findings)} for t in chain.tickets])


def write_scope_csv(path: Path, chain: GameplayMixedChain) -> None:
    fields = ["function", "file", "role", "implementation_status", "object_family", "side_effect_surface", "source_contract", "proof_status", "patch_ready", "blocker"]
    write_dict_csv(path, fields, [row.__dict__ for row in chain.scope_rows])


def write_callsite_csv(path: Path, chain: GameplayMixedChain) -> None:
    fields = ["caller", "callee", "caller_file", "callee_file", "line", "shape_id", "arg_count", "argument_kinds", "state_fields", "side_effects", "proof_status", "patch_ready", "blocker"]
    write_dict_csv(path, fields, [row.__dict__ for row in chain.callsites])


def write_taxonomy_csv(path: Path, chain: GameplayMixedChain) -> None:
    fields = ["shape_id", "site_count", "argument_kinds", "state_fields", "write_surfaces", "source_backed", "patch_ready", "blocker"]
    write_dict_csv(path, fields, [row.__dict__ for row in chain.taxonomy_rows])


def write_handoff_csv(path: Path, chain: GameplayMixedChain) -> None:
    fields = ["next_ticket", "next_cluster", "next_subcluster", "reason", "code_change_readiness", "blocker"]
    write_dict_csv(path, fields, [chain.handoff.__dict__])


def write_markdown(path: Path, chain: GameplayMixedChain) -> None:
    lines = [
        "# RE-134..RE-140 — Gameplay mixed chain",
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
        "- [x] RE-133 ticket plan consumed.",
        "- [x] RE-134 caller and side-effect map published.",
        "- [x] RE-135 argument/state taxonomy published.",
        "- [x] RE-136 comparison gate evaluated.",
        "- [x] RE-137 reconstruction plan reduced to documentation-only blocker.",
        "- [x] RE-138 source patch gate denied safely.",
        "- [x] RE-139 validation/regression metadata recorded.",
        "- [x] RE-140 closure/handoff recorded.",
        "",
        "## Readiness",
        "",
        f"- code-change-ready rows: `{chain.code_change_ready_count}`",
        f"- marker-ready rows: `{chain.marker_ready_count}`",
        f"- source-patch-ready rows: `{chain.source_patch_ready_count}`",
        "- terminal blocker: `missing gameplay mixed state contract and symbolic equivalence proof`",
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


def write_story(path: Path, chain: GameplayMixedChain, ticket: Ticket) -> None:
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
        "- `python3 -m pytest tests/reverse/test_re134_re140_gameplay_mixed_chain.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over generated RE-134..RE-140 artifacts",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_all_artifacts(chain: GameplayMixedChain, repo: Path) -> dict[str, Path]:
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
    chain = build_gameplay_mixed_chain(args.repo)
    for key, path in write_all_artifacts(chain, args.repo).items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
