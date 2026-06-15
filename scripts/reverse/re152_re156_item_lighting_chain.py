#!/usr/bin/env python3
"""Generate RE-152..RE-156 item-lighting interaction closure artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

RE149_PLAN_CSV = "docs/reverse/generated/re149-item-lighting-interaction-ticket-plan.csv"
RE150_SCOPE_CSV = "docs/reverse/generated/re150-item-lighting-interaction-scope.csv"
RE151_TAXONOMY_CSV = "docs/reverse/generated/re151-item-lighting-interaction-argument-state-taxonomy.csv"
CHAIN_CSV = "docs/reverse/generated/re152-re156-item-lighting-interaction-chain.csv"
COMPARISON_CSV = "docs/reverse/generated/re152-item-lighting-interaction-comparison-gate.csv"
PLAN_CSV = "docs/reverse/generated/re153-item-lighting-interaction-reconstruction-plan.csv"
HANDOFF_CSV = "docs/reverse/generated/re156-item-lighting-interaction-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re152-re156-item-lighting-interaction-chain.md"
STORY_DIR = "docs/stories"

FORBIDDEN_FRAGMENTS = ("0x", "payload", "opcode", "machine word", "raw call target")
EXPECTED_PLAN = ("RE-150", "RE-151", "RE-152", "RE-153", "RE-154", "RE-155", "RE-156")
EXPECTED_SCOPE = ("DoFlameTorch", "TriggerAlertLight")
EXPECTED_SHAPES = {
    "DoFlameTorch": "shape-item-lighting-void-torch-update",
    "TriggerAlertLight": "shape-item-lighting-alert-light-parameters",
}


@dataclass(frozen=True)
class ComparisonRow:
    function: str
    file: str
    shape_id: str
    argument_kinds: str
    state_fields: str
    source_evidence: str
    binary_evidence: str
    equivalence_status: str
    code_change_ready: str
    marker_ready: str
    blocker: str
    next_action: str


@dataclass(frozen=True)
class ReconstructionPlanRow:
    ticket: str
    cluster: str
    goal: str
    deliverable: str
    dependency: str
    stop_condition: str


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
class ItemLightingChain:
    cluster: str
    upstream_ticket: str
    status: str
    final_decision: str
    next_ticket: str
    code_change_ready_count: int
    marker_ready_count: int
    source_patch_ready_count: int
    comparison_rows: tuple[ComparisonRow, ...]
    reconstruction_plan: tuple[ReconstructionPlanRow, ...]
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


def verify_inputs(repo: Path) -> None:
    plan_ids = tuple(row.get("story_id", "") for row in read_csv(repo / RE149_PLAN_CSV))
    if plan_ids != EXPECTED_PLAN:
        raise ValueError("RE-149 plan no longer matches RE-150..RE-156 expectations")
    scope_ids = tuple(row.get("function", "") for row in read_csv(repo / RE150_SCOPE_CSV))
    if scope_ids != EXPECTED_SCOPE:
        raise ValueError(f"RE-150 scope drifted before RE-152..RE-156 chain: {scope_ids}")
    taxonomy_shapes = tuple(row.get("shape_id", "") for row in read_csv(repo / RE151_TAXONOMY_CSV))
    if set(taxonomy_shapes) != set(EXPECTED_SHAPES.values()):
        raise ValueError(f"RE-151 taxonomy shape set drifted: {taxonomy_shapes}")


def taxonomy_by_callee(repo: Path) -> dict[str, dict[str, str]]:
    rows = read_csv(repo / RE151_TAXONOMY_CSV)
    output: dict[str, dict[str, str]] = {}
    for row in rows:
        callee = row.get("callees", "")
        if ";" in callee:
            raise ValueError(f"RE-152 expects one item-lighting callee per shape: {row}")
        output[callee] = row
    if tuple(sorted(output)) != tuple(sorted(EXPECTED_SCOPE)):
        raise ValueError(f"RE-151 taxonomy callee set drifted: {tuple(sorted(output))}")
    return output


def build_comparison_rows(repo: Path) -> tuple[ComparisonRow, ...]:
    taxonomy = taxonomy_by_callee(repo)
    scope = {row["function"]: row for row in read_csv(repo / RE150_SCOPE_CSV)}
    rows: list[ComparisonRow] = []
    for function in EXPECTED_SCOPE:
        tax = taxonomy[function]
        scope_row = scope[function]
        if tax.get("patch_ready") != "no" or tax.get("source_backed") != "source-callsite-only":
            raise ValueError(f"RE-152 refuses drifted RE-151 readiness row: {tax}")
        rows.append(ComparisonRow(
            function=function,
            file=scope_row.get("file", "unknown"),
            shape_id=tax["shape_id"],
            argument_kinds=tax["argument_kinds"],
            state_fields=tax["state_fields"],
            source_evidence="source-callsite-and-taxonomy-only",
            binary_evidence="non-raw-symbolic-equivalence-missing",
            equivalence_status="blocked-missing-symbolic-equivalence-proof",
            code_change_ready="no",
            marker_ready="no",
            blocker="missing-item-lighting-state-contract-and-symbolic-equivalence-proof",
            next_action="defer-source-patch-and-open-ui-text-support-proof-first-audit" if function == "TriggerAlertLight" else "keep-comparison-blocked",
        ))
    return tuple(rows)


def build_reconstruction_plan() -> tuple[ReconstructionPlanRow, ...]:
    return (
        ReconstructionPlanRow("RE-157", "ui-text-support", "Open proof-first audit for InitFont and the ui-text-support cluster.", "scope CSV, story, and bounded ticket plan", "RE-156 handoff", "audit published or blocker recorded"),
        ReconstructionPlanRow("RE-158", "ui-text-support", "Map InitFont callers, marker status, and text/font state surfaces.", "source-backed callsite and side-effect map", "RE-157 audit", "metadata-only map published"),
        ReconstructionPlanRow("RE-159", "ui-text-support", "Classify InitFont arguments, global text state, and marker proof needs.", "argument/state taxonomy", "RE-158 callsite map", "taxonomy published with readiness rows"),
        ReconstructionPlanRow("RE-160", "ui-text-support", "Decide whether InitFont has enough non-raw equivalence proof for marker or source changes.", "comparison gate", "RE-159 taxonomy", "patch-ready rows or explicit blocker"),
        ReconstructionPlanRow("RE-161", "ui-text-support", "Close ui-text-support or hand off to the next module-game backlog domain.", "closure or next-domain handoff", "RE-160 comparison gate", "handoff recorded"),
    )


def build_handoff() -> Handoff:
    return Handoff(
        next_ticket="RE-157",
        next_cluster="ui-text-support",
        next_subcluster="ui-text-support",
        pivot="InitFont",
        reason="item-lighting-interaction closed with proof blocker; next RE-061 module-game cluster is ui-text-support with InitFont pivot",
        code_change_readiness="blocked",
        blocker="Item lighting lacks state contract and symbolic equivalence proof for safe source or marker changes",
    )


def build_tickets(handoff: Handoff) -> tuple[Ticket, ...]:
    common = (CHAIN_CSV, COMPARISON_CSV, PLAN_CSV, HANDOFF_CSV, MD_OUTPUT)
    specs = (
        ("RE-152", "Item lighting interaction comparison gate", "no-patch-proof-blocker", "RE-153"),
        ("RE-153", "Item lighting interaction reconstruction plan", "documentation-only-plan", "RE-154"),
        ("RE-154", "Item lighting interaction source patch gate", "source-patch-denied", "RE-155"),
        ("RE-155", "Item lighting interaction validation regression", "metadata-validation-published", "RE-156"),
        ("RE-156", "Item lighting interaction closure or handoff", "handoff-to-ui-text-support", handoff.next_ticket),
    )
    tickets: list[Ticket] = []
    for story_id, title, decision, next_ticket in specs:
        progress = (
            "RE-151 taxonomy consumed.",
            "Item-lighting comparison gate evaluated.",
            "Patch and marker readiness checked.",
            "Forbidden evidence excluded from generated artifacts.",
        )
        if story_id == "RE-156":
            progress += ("Item-lighting metadata closed with blocker.", "UI text support handoff recorded.")
        findings = (
            "item-lighting rows remain blocked by missing item lighting state contract and symbolic equivalence proof",
            "no production source or proof marker patch is admitted by this chain",
            f"handoff target: {handoff.next_ticket} {handoff.next_cluster}" if story_id == "RE-156" else "continue current item-lighting closure chain",
        )
        tickets.append(Ticket(story_id, title, "done", decision, next_ticket, "blocked", progress, common, findings))
    return tuple(tickets)


def build_item_lighting_chain(repo: Path) -> ItemLightingChain:
    repo = Path(repo)
    verify_inputs(repo)
    comparison_rows = build_comparison_rows(repo)
    handoff = build_handoff()
    return ItemLightingChain(
        cluster="item-lighting-interaction",
        upstream_ticket="RE-151",
        status="item-lighting-interaction-chain-closed-with-proof-blocker",
        final_decision="documentation-only-terminal-blocker",
        next_ticket=handoff.next_ticket,
        code_change_ready_count=0,
        marker_ready_count=0,
        source_patch_ready_count=0,
        comparison_rows=comparison_rows,
        reconstruction_plan=build_reconstruction_plan(),
        handoff=handoff,
        tickets=build_tickets(handoff),
    )


def assert_metadata_only(path: Path) -> None:
    text = path.read_text(encoding="utf-8").lower()
    hits = [fragment for fragment in FORBIDDEN_FRAGMENTS if fragment in text]
    if hits:
        raise ValueError(f"forbidden evidence fragments in {path}: {hits}")


def write_chain_csv(path: Path, chain: ItemLightingChain) -> None:
    fields = ["story_id", "title", "status", "decision", "next_ticket", "code_change_readiness", "generated_artifacts", "findings"]
    write_dict_csv(path, fields, [{**ticket.__dict__, "generated_artifacts": ";".join(ticket.generated_artifacts), "findings": ";".join(ticket.findings)} for ticket in chain.tickets])


def write_comparison_csv(path: Path, chain: ItemLightingChain) -> None:
    fields = list(ComparisonRow.__dataclass_fields__)
    write_dict_csv(path, fields, [row.__dict__ for row in chain.comparison_rows])


def write_plan_csv(path: Path, chain: ItemLightingChain) -> None:
    fields = list(ReconstructionPlanRow.__dataclass_fields__)
    write_dict_csv(path, fields, [row.__dict__ for row in chain.reconstruction_plan])


def write_handoff_csv(path: Path, chain: ItemLightingChain) -> None:
    fields = list(Handoff.__dataclass_fields__)
    write_dict_csv(path, fields, [chain.handoff.__dict__])


def write_markdown(path: Path, chain: ItemLightingChain) -> None:
    lines = [
        "# RE-152..RE-156 — Item lighting interaction chain",
        "",
        f"Cluster: `{chain.cluster}`",
        f"Status: `{chain.status}`",
        f"Decision: `{chain.final_decision}`",
        f"Next ticket: `{chain.next_ticket}`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-151 taxonomy consumed.",
        "- [x] RE-152 comparison gate evaluated.",
        "- [x] RE-153 reconstruction plan reduced to documentation-only blocker.",
        "- [x] RE-154 source patch gate denied safely.",
        "- [x] RE-155 validation/regression metadata recorded.",
        "- [x] RE-156 closure/handoff recorded.",
        "",
        "## Readiness",
        "",
        f"- code-change-ready rows: `{chain.code_change_ready_count}`",
        f"- marker-ready rows: `{chain.marker_ready_count}`",
        f"- source-patch-ready rows: `{chain.source_patch_ready_count}`",
        "- terminal blocker: `missing item lighting state contract and symbolic equivalence proof`",
        "",
        "## Comparison rows",
        "",
    ]
    for row in chain.comparison_rows:
        lines.append(f"- `{row.function}` — `{row.shape_id}` / `{row.equivalence_status}` / source-ready `{row.code_change_ready}` / marker-ready `{row.marker_ready}`")
    lines.extend(["", "## Handoff", ""])
    lines.append(f"- next ticket: `{chain.handoff.next_ticket}`")
    lines.append(f"- next subcluster: `{chain.handoff.next_subcluster}`")
    lines.append(f"- pivot: `{chain.handoff.pivot}`")
    lines.append(f"- reason: `{chain.handoff.reason}`")
    lines.extend(["", "No production source or proof marker change is made by this chain."])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def slug(title: str) -> str:
    return title.lower().replace(" ", "-")


def write_story(path: Path, chain: ItemLightingChain, ticket: Ticket) -> None:
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
    ])
    for row in chain.reconstruction_plan:
        lines.append(f"- `{row.ticket}` — `{row.cluster}` — {row.goal} Deliverable: `{row.deliverable}`; dependency: `{row.dependency}`; stop: `{row.stop_condition}`.")
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
        "- `python3 -m pytest tests/reverse/test_re152_re156_item_lighting_chain.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over generated RE-152..RE-156 artifacts",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_all_artifacts(chain: ItemLightingChain, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "chain_csv": repo / CHAIN_CSV,
        "comparison_csv": repo / COMPARISON_CSV,
        "plan_csv": repo / PLAN_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
    }
    write_chain_csv(paths["chain_csv"], chain)
    write_comparison_csv(paths["comparison_csv"], chain)
    write_plan_csv(paths["plan_csv"], chain)
    write_handoff_csv(paths["handoff_csv"], chain)
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
    chain = build_item_lighting_chain(args.repo)
    for key, path in write_all_artifacts(chain, args.repo).items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
