#!/usr/bin/env python3
"""Generate RE-158..RE-161 ui-text-support closure artifacts."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path

RE157_PLAN_CSV = "docs/reverse/generated/re157-ui-text-support-ticket-plan.csv"
RE157_AUDIT_CSV = "docs/reverse/generated/re157-ui-text-support-proof-first-audit.csv"
CALLSITE_CSV = "docs/reverse/generated/re158-ui-text-support-caller-side-effect-map.csv"
TAXONOMY_CSV = "docs/reverse/generated/re159-ui-text-support-argument-state-taxonomy.csv"
COMPARISON_CSV = "docs/reverse/generated/re160-ui-text-support-comparison-gate.csv"
CHAIN_CSV = "docs/reverse/generated/re158-re161-ui-text-support-chain.csv"
HANDOFF_CSV = "docs/reverse/generated/re161-ui-text-support-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re158-re161-ui-text-support-chain.md"
STORY_DIR = "docs/stories"

FORBIDDEN_FRAGMENTS = ("0x", "payload", "opcode", "machine word", "raw call target")
EXPECTED_PLAN = ("RE-158", "RE-159", "RE-160", "RE-161")
EXPECTED_FUNCTION = "InitFont"
CANONICAL_CALLER_FILE = "SPEC_PSX/PSXMAIN.C"
C_KEYWORD_ARTIFACTS = {"if", "for", "while", "switch", "else", "do"}


@dataclass(frozen=True)
class CallsiteRow:
    caller: str
    callee: str
    caller_file: str
    callee_file: str
    line: int
    source_line_text: str
    shape_id: str
    arg_count: int
    argument_kinds: str
    state_fields: str
    side_effects: str
    proof_status: str
    patch_ready: str
    blocker: str


@dataclass(frozen=True)
class TaxonomyRow:
    function: str
    shape_id: str
    argument_kinds: str
    state_fields: str
    source_contract: str
    source_evidence: str
    proof_status: str
    code_change_ready: str
    marker_ready: str
    blocker: str


@dataclass(frozen=True)
class ComparisonRow:
    function: str
    shape_id: str
    source_evidence: str
    binary_evidence: str
    equivalence_status: str
    code_change_ready: str
    marker_ready: str
    source_patch_allowed: str
    marker_change_allowed: str
    blocker: str
    next_action: str


@dataclass(frozen=True)
class Handoff:
    next_ticket: str
    next_cluster: str
    next_subcluster: str
    pivot: str
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
class UiTextSupportChain:
    cluster: str
    upstream_ticket: str
    pivot: str
    status: str
    final_decision: str
    next_ticket: str
    code_change_ready_count: int
    marker_ready_count: int
    source_patch_ready_count: int
    callsite_rows: tuple[CallsiteRow, ...]
    taxonomy_rows: tuple[TaxonomyRow, ...]
    comparison_rows: tuple[ComparisonRow, ...]
    handoff: Handoff
    tickets: tuple[Ticket, ...]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_dict_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def strip_comments(line: str) -> str:
    return line.split("//", 1)[0]


def verify_inputs(repo: Path) -> dict[str, str]:
    plan_ids = tuple(row.get("story_id", "") for row in read_csv(repo / RE157_PLAN_CSV))
    if plan_ids != EXPECTED_PLAN:
        raise ValueError(f"RE-157 plan no longer matches RE-158..RE-161 expectations: {plan_ids}")
    audit_rows = read_csv(repo / RE157_AUDIT_CSV)
    if len(audit_rows) != 1:
        raise ValueError(f"RE-158 expects one ui-text-support audit row: {len(audit_rows)}")
    row = audit_rows[0]
    if row.get("function") != EXPECTED_FUNCTION or row.get("cluster") != "ui-text-support":
        raise ValueError(f"RE-158 scope drifted: {row}")
    if row.get("code_change_ready") != "no" or row.get("marker_ready") != "no":
        raise ValueError(f"RE-158 refuses an already-ready RE-157 row: {row}")
    return row


def function_body(repo: Path, file_name: str, function: str) -> str:
    path = repo / file_name
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


def caller_for_line(repo: Path, path: Path, line_index: int) -> str:
    function_re = re.compile(r"^\s*(?:int|void|long|short|char|bool|struct\s+\w+)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^;]*\)\s*(?://.*)?$")
    current = "unknown-caller"
    pending = ""
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines()[: line_index + 1]:
        clean = strip_comments(line).rstrip()
        sig = function_re.match(clean)
        if sig and sig.group(1) not in C_KEYWORD_ARTIFACTS:
            pending = sig.group(1)
        if pending and "{" in clean:
            current = pending
            pending = ""
    if current == "unknown-caller":
        raise ValueError(f"could not identify caller for {path.relative_to(repo)} line {line_index + 1}")
    return current


def build_callsite_rows(repo: Path, audit_row: dict[str, str]) -> tuple[CallsiteRow, ...]:
    caller_path = repo / CANONICAL_CALLER_FILE
    lines = caller_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    rows: list[CallsiteRow] = []
    pattern = re.compile(rf"\b{EXPECTED_FUNCTION}\s*\(([^)]*)\)")
    body = function_body(repo, audit_row["file"], EXPECTED_FUNCTION)
    if not body.strip():
        raise ValueError("InitFont source body is missing")
    for idx, line in enumerate(lines):
        clean = strip_comments(line).strip()
        match = pattern.search(clean)
        if not match:
            continue
        args = [arg.strip() for arg in match.group(1).split(",") if arg.strip()]
        rows.append(CallsiteRow(
            caller=caller_for_line(repo, caller_path, idx),
            callee=EXPECTED_FUNCTION,
            caller_file=CANONICAL_CALLER_FILE,
            callee_file=audit_row["file"],
            line=idx + 1,
            source_line_text="source-line-contains-callee-call",
            shape_id="shape-ui-text-initfont-void-font-shade-init",
            arg_count=len(args),
            argument_kinds="void" if not args else "unexpected-arguments",
            state_fields="font-shade-table;shade-gradient-inputs;per-channel-clamp",
            side_effects="font-shade-table-initialization",
            proof_status="source-callsite-mapped-only",
            patch_ready="no",
            blocker="missing-initfont-behavior-equivalence-proof",
        ))
    if len(rows) != 1:
        raise ValueError(f"expected one canonical PSX InitFont callsite, found {len(rows)}")
    return tuple(rows)


def build_taxonomy_rows(callsites: tuple[CallsiteRow, ...]) -> tuple[TaxonomyRow, ...]:
    if tuple(row.callee for row in callsites) != (EXPECTED_FUNCTION,):
        raise ValueError("RE-159 expects the RE-158 InitFont callsite only")
    row = callsites[0]
    return (TaxonomyRow(
        function=EXPECTED_FUNCTION,
        shape_id=row.shape_id,
        argument_kinds=row.argument_kinds,
        state_fields=row.state_fields,
        source_contract="initializes font shade lookup table from shade endpoints",
        source_evidence="source-body-and-callsite-only",
        proof_status="taxonomy-needs-equivalence-proof",
        code_change_ready="no",
        marker_ready="no",
        blocker="missing-initfont-behavior-equivalence-proof",
    ),)


def build_comparison_rows(taxonomy: tuple[TaxonomyRow, ...]) -> tuple[ComparisonRow, ...]:
    row = taxonomy[0]
    if row.code_change_ready != "no" or row.marker_ready != "no":
        raise ValueError(f"RE-160 refuses ready taxonomy without separate proof: {row}")
    return (ComparisonRow(
        function=row.function,
        shape_id=row.shape_id,
        source_evidence=row.source_evidence,
        binary_evidence="non-raw-behavior-equivalence-missing",
        equivalence_status="blocked-missing-initfont-behavior-equivalence-proof",
        code_change_ready="no",
        marker_ready="no",
        source_patch_allowed="no",
        marker_change_allowed="no",
        blocker="missing-initfont-behavior-equivalence-proof",
        next_action="close-ui-text-support-and-record-module-game-exhaustion",
    ),)


def build_handoff() -> Handoff:
    return Handoff(
        next_ticket="TBD",
        next_cluster="module-game-exhausted",
        next_subcluster="module-game-exhausted",
        pivot="TBD",
        reason="all RE-061 module-game clusters have reached metadata-only closure or proof blockers",
        code_change_readiness="blocked",
        blocker="InitFont still needs non-raw behavior equivalence proof before source or marker changes",
    )


def build_tickets(handoff: Handoff) -> tuple[Ticket, ...]:
    common = (CALLSITE_CSV, TAXONOMY_CSV, COMPARISON_CSV, CHAIN_CSV, HANDOFF_CSV, MD_OUTPUT)
    specs = (
        ("RE-158", "UI text support caller side-effect map", "caller-side-effect-map-blocked", "RE-159"),
        ("RE-159", "UI text support argument state taxonomy", "taxonomy-proof-blocked", "RE-160"),
        ("RE-160", "UI text support comparison gate", "source-and-marker-patch-denied", "RE-161"),
        ("RE-161", "UI text support closure or handoff", "module-game-exhaustion-handoff", handoff.next_ticket),
    )
    tickets: list[Ticket] = []
    for story_id, title, decision, next_ticket in specs:
        progress = (
            "RE-157 ticket plan consumed.",
            "InitFont canonical PSX caller mapped.",
            "InitFont argument and font state taxonomy recorded.",
            "RE-160 comparison gate kept marker/source changes blocked.",
            "Forbidden evidence excluded from generated artifacts.",
        )
        if story_id == "RE-161":
            progress += ("UI text support closed with proof blocker.", "Module-game exhaustion handoff recorded.")
        findings = (
            "InitFont remains source-visible but blocked by missing behavior equivalence proof",
            "no production source or proof marker patch is admitted by this chain",
            f"handoff target: {handoff.next_ticket} {handoff.next_cluster}" if story_id == "RE-161" else "continue current ui text support closure chain",
        )
        tickets.append(Ticket(story_id, title, "done", decision, next_ticket, "blocked", progress, common, findings))
    return tuple(tickets)


def build_ui_text_support_chain(repo: Path) -> UiTextSupportChain:
    repo = Path(repo)
    audit_row = verify_inputs(repo)
    callsites = build_callsite_rows(repo, audit_row)
    taxonomy = build_taxonomy_rows(callsites)
    comparison = build_comparison_rows(taxonomy)
    handoff = build_handoff()
    return UiTextSupportChain(
        cluster="ui-text-support",
        upstream_ticket="RE-157",
        pivot=EXPECTED_FUNCTION,
        status="ui-text-support-chain-closed-with-proof-blocker",
        final_decision="documentation-only-terminal-blocker",
        next_ticket=handoff.next_ticket,
        code_change_ready_count=0,
        marker_ready_count=0,
        source_patch_ready_count=0,
        callsite_rows=callsites,
        taxonomy_rows=taxonomy,
        comparison_rows=comparison,
        handoff=handoff,
        tickets=build_tickets(handoff),
    )


def assert_metadata_only(path: Path) -> None:
    text = path.read_text(encoding="utf-8").lower()
    hits = [fragment for fragment in FORBIDDEN_FRAGMENTS if fragment in text]
    if hits:
        raise ValueError(f"forbidden evidence fragments in {path}: {hits}")


def write_chain_csv(path: Path, chain: UiTextSupportChain) -> None:
    fields = ["story_id", "title", "status", "decision", "next_ticket", "code_change_readiness", "generated_artifacts", "findings"]
    write_dict_csv(path, fields, [{**ticket.__dict__, "generated_artifacts": ";".join(ticket.generated_artifacts), "findings": ";".join(ticket.findings)} for ticket in chain.tickets])


def write_markdown(path: Path, chain: UiTextSupportChain) -> None:
    lines = [
        "# RE-158..RE-161 — UI text support chain",
        "",
        f"Cluster: `{chain.cluster}`",
        f"Pivot: `{chain.pivot}`",
        f"Status: `{chain.status}`",
        f"Decision: `{chain.final_decision}`",
        f"Next ticket: `{chain.next_ticket}`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-157 ticket plan consumed.",
        "- [x] RE-158 canonical caller side-effect map emitted.",
        "- [x] RE-159 argument and font state taxonomy emitted.",
        "- [x] RE-160 comparison gate kept source and marker changes blocked.",
        "- [x] RE-161 closure/handoff recorded.",
        "",
        "## Readiness",
        "",
        f"- code-change-ready rows: `{chain.code_change_ready_count}`",
        f"- marker-ready rows: `{chain.marker_ready_count}`",
        f"- source-patch-ready rows: `{chain.source_patch_ready_count}`",
        "- terminal blocker: `missing InitFont behavior equivalence proof`",
        "",
        "## Comparison rows",
        "",
    ]
    for row in chain.comparison_rows:
        lines.append(f"- `{row.function}` — `{row.shape_id}` / `{row.equivalence_status}` / source-ready `{row.code_change_ready}` / marker-ready `{row.marker_ready}`")
    lines.extend(["", "## Handoff", ""])
    lines.append(f"- next ticket: `{chain.handoff.next_ticket}`")
    lines.append(f"- next cluster: `{chain.handoff.next_cluster}`")
    lines.append(f"- reason: `{chain.handoff.reason}`")
    lines.extend(["", "No production source or proof marker change is made by this chain."])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def slug(title: str) -> str:
    return title.lower().replace(" ", "-")


def write_story(path: Path, chain: UiTextSupportChain, ticket: Ticket) -> None:
    lines = [
        f"# {ticket.story_id} — {ticket.title}",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        f"Advance `{chain.cluster}` using metadata-only evidence for {ticket.story_id}.",
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
        "## Follow-up ticket breakdown",
        "",
        "- `TBD` — select a new backlog outside the exhausted RE-061 module-game cluster set, or add a dedicated InitFont behavior-equivalence proof if new non-raw evidence becomes available.",
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
        "- `python3 -m pytest tests/reverse/test_re158_re161_ui_text_support_chain.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over generated RE-158..RE-161 artifacts",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_all_artifacts(chain: UiTextSupportChain, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "callsite_csv": repo / CALLSITE_CSV,
        "taxonomy_csv": repo / TAXONOMY_CSV,
        "comparison_csv": repo / COMPARISON_CSV,
        "chain_csv": repo / CHAIN_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
    }
    write_dict_csv(paths["callsite_csv"], list(CallsiteRow.__dataclass_fields__), [row.__dict__ for row in chain.callsite_rows])
    write_dict_csv(paths["taxonomy_csv"], list(TaxonomyRow.__dataclass_fields__), [row.__dict__ for row in chain.taxonomy_rows])
    write_dict_csv(paths["comparison_csv"], list(ComparisonRow.__dataclass_fields__), [row.__dict__ for row in chain.comparison_rows])
    write_chain_csv(paths["chain_csv"], chain)
    write_dict_csv(paths["handoff_csv"], list(Handoff.__dataclass_fields__), [chain.handoff.__dict__])
    write_markdown(paths["md"], chain)
    for ticket in chain.tickets:
        story_path = repo / STORY_DIR / f"{ticket.story_id}-{slug(ticket.title)}.md"
        write_story(story_path, chain, ticket)
        paths[ticket.story_id] = story_path
    for path in paths.values():
        assert_metadata_only(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    chain = build_ui_text_support_chain(args.repo)
    for key, path in write_all_artifacts(chain, args.repo).items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
