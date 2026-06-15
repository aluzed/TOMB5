#!/usr/bin/env python3
"""Generate RE-206..RE-212 platform-main-lifecycle epic artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

RE205_HANDOFF_CSV = "docs/reverse/generated/re205-module-spec-psxpc-n-post-platform-memory-handoff.csv"
RE205_SELECTION_CSV = "docs/reverse/generated/re205-module-spec-psxpc-n-post-platform-memory-next-cluster-selection.csv"
RE163_AUDIT_CSV = "docs/reverse/generated/re163-module-spec-psxpc-n-proof-first-audit.csv"
RE163_CLUSTERS_CSV = "docs/reverse/generated/re163-module-spec-psxpc-n-clusters.csv"
AUDIT_CSV = "docs/reverse/generated/re206-platform-main-lifecycle-proof-first-audit.csv"
PLAN_CSV = "docs/reverse/generated/re206-platform-main-lifecycle-ticket-plan.csv"
LIFECYCLE_CSV = "docs/reverse/generated/re207-platform-main-lifecycle-source-surface-map.csv"
TAXONOMY_CSV = "docs/reverse/generated/re208-platform-main-lifecycle-argument-taxonomy.csv"
CONTRACT_CSV = "docs/reverse/generated/re209-platform-main-lifecycle-state-contract.csv"
EQUIVALENCE_CSV = "docs/reverse/generated/re210-platform-main-lifecycle-equivalence-gate.csv"
SOURCE_PATCH_CSV = "docs/reverse/generated/re211-platform-main-lifecycle-source-patch-gate.csv"
HANDOFF_CSV = "docs/reverse/generated/re212-module-spec-psxpc-n-platform-main-lifecycle-exhaustion-handoff.csv"
CHAIN_CSV = "docs/reverse/generated/re206-re212-platform-main-lifecycle-epic.csv"
MD_OUTPUT = "docs/reverse/functions/re206-re212-platform-main-lifecycle-epic.md"
STORY_DIR = "docs/stories"

FORBIDDEN_FRAGMENTS = ("0x", "payload", "opcode", "machine word", "raw call target", "word_le_hex", "call_address", "raw-source-dump")
STALE_FRAGMENTS = ("ui text rendering", "ui-text-rendering", "item-lighting", "geometry support chain", "frontend-loadsave", "platform-gpu-display")
EXPECTED_SCOPE = ("main", "InitNewCDSystem", "VSyncFunc")
EXPECTED_PLAN = ("RE-207", "RE-208", "RE-209", "RE-210", "RE-211", "RE-212")

FAMILY = {
    "main": (
        "program-entrypoint",
        "argc;argv;boot-sequence",
        "startup-sequence;gpu-init;input-init;audio-init;gameflow-dispatch;shutdown",
        "coordinates emulator, platform, gameflow, and shutdown lifecycle state",
        "SPEC_PSXPC_N/PSXMAIN.C",
    ),
    "InitNewCDSystem": (
        "disc-system-initialization",
        "disc-mode;wad-header;xa-track-index",
        "disc-index;gamewad-header;xa-track-list;xa-request-state",
        "initializes disc lookup and XA playback lifecycle state",
        "SPEC_PSXPC_N/CD.C",
    ),
    "VSyncFunc": (
        "vertical-sync-callback",
        "callback-frame-state;loading-bar-state",
        "frame-counters;loading-bar-callback;vsync-callback",
        "updates platform frame counters and optional loading callback state",
        "SPEC_PSXPC_N/PSXMAIN.C",
    ),
}


@dataclass(frozen=True)
class AuditRow:
    function: str
    file: str
    line: int
    role: str
    source_status: str
    prior_code_ready: str
    prior_marker_ready: str
    proof_status: str
    code_change_ready: str
    marker_ready: str
    blocker: str


@dataclass(frozen=True)
class TicketPlanRow:
    story_id: str
    topic: str
    goal: str
    scope: str
    code_change_readiness: str
    exit_condition: str


@dataclass(frozen=True)
class LifecycleRow:
    function: str
    source_file: str
    source_line_range: str
    lifecycle_family: str
    entry_surface: str
    state_surface: str
    source_contract: str
    proof_status: str
    patch_ready: str
    blocker: str


@dataclass(frozen=True)
class TaxonomyRow:
    function: str
    argument_family: str
    argument_kinds: str
    state_fields: str
    source_contract: str
    proof_status: str
    code_change_ready: str
    marker_ready: str
    blocker: str


@dataclass(frozen=True)
class ContractRow:
    function: str
    contract_id: str
    required_source_state: str
    required_binary_metadata: str
    contract_status: str
    code_change_ready: str
    marker_ready: str
    blocker: str


@dataclass(frozen=True)
class EquivalenceRow:
    function: str
    contract_id: str
    source_evidence: str
    binary_evidence: str
    equivalence_status: str
    code_change_ready: str
    marker_ready: str
    blocker: str


@dataclass(frozen=True)
class SourcePatchRow:
    function: str
    source_patch_allowed: str
    marker_change_allowed: str
    decision: str
    dependency: str
    blocker: str


@dataclass(frozen=True)
class Handoff:
    next_ticket: str
    next_topic: str
    selected_cluster: str
    selected_pivot: str
    outcome: str
    reason: str
    dependency: str
    code_change_readiness: str
    stop_condition: str


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
class PlatformMainLifecycleEpic:
    domain_id: str
    cluster: str
    upstream_ticket: str
    pivot: str
    status: str
    final_decision: str
    next_ticket: str
    code_change_ready_count: int
    marker_ready_count: int
    source_patch_ready_count: int
    audit_rows: tuple[AuditRow, ...]
    plan_rows: tuple[TicketPlanRow, ...]
    lifecycle_rows: tuple[LifecycleRow, ...]
    taxonomy_rows: tuple[TaxonomyRow, ...]
    contract_rows: tuple[ContractRow, ...]
    equivalence_rows: tuple[EquivalenceRow, ...]
    source_patch_rows: tuple[SourcePatchRow, ...]
    next_selection_rows: tuple[()]
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


def verify_inputs(repo: Path) -> tuple[dict[str, str], list[dict[str, str]], list[dict[str, str]]]:
    handoff_rows = read_csv(repo / RE205_HANDOFF_CSV)
    if len(handoff_rows) != 1:
        raise ValueError("RE-205 handoff must contain exactly one row")
    handoff = handoff_rows[0]
    expected = {
        "next_ticket": "RE-206",
        "next_topic": "platform-main-lifecycle-proof-first-audit",
        "selected_cluster": "platform-main-lifecycle",
        "selected_pivot": "main",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if handoff.get(key) != value:
            raise ValueError(f"RE-205 handoff drift: {key}={handoff.get(key)!r}")

    selection_rows = read_csv(repo / RE205_SELECTION_CSV)
    selected = [row for row in selection_rows if row.get("selection_decision") == "selected-next-proof-chain"]
    if len(selected) != 1 or selected[0].get("cluster") != "platform-main-lifecycle":
        raise ValueError("RE-205 selection must pick exactly platform-main-lifecycle")

    cluster_rows = [row for row in read_csv(repo / RE163_CLUSTERS_CSV) if row.get("cluster") == "platform-main-lifecycle"]
    if len(cluster_rows) != 1 or cluster_rows[0].get("top_function") != "main":
        raise ValueError("RE-163 platform-main-lifecycle cluster metadata drifted")
    reps = tuple(cluster_rows[0].get("representative_functions", "").split(";"))
    if reps != EXPECTED_SCOPE:
        raise ValueError(f"platform-main-lifecycle scope drifted: {reps}")
    return handoff, selection_rows, read_csv(repo / RE163_AUDIT_CSV)


def build_audit_rows(source_rows: list[dict[str, str]]) -> tuple[AuditRow, ...]:
    by_function = {row.get("function", ""): row for row in source_rows if row.get("cluster") == "platform-main-lifecycle"}
    missing = [function for function in EXPECTED_SCOPE if function not in by_function]
    extra = sorted(function for function in by_function if function not in EXPECTED_SCOPE)
    if missing or extra:
        raise ValueError(f"platform-main-lifecycle audit scope drift: missing={missing}, extra={extra}")
    rows: list[AuditRow] = []
    for function in EXPECTED_SCOPE:
        source = by_function[function]
        rows.append(AuditRow(
            function=function,
            file=source["file"],
            line=int(source["line"]),
            role="pivot" if function == "main" else "lifecycle-context",
            source_status=source.get("status", ""),
            prior_code_ready=source.get("code_change_ready", "no"),
            prior_marker_ready=source.get("marker_ready", "no"),
            proof_status="source-scope-inventory-only",
            code_change_ready="no",
            marker_ready="no",
            blocker="missing-platform-main-lifecycle-source-surface-and-non-raw-nd-equivalence-proof",
        ))
    return tuple(rows)


def build_plan_rows() -> tuple[TicketPlanRow, ...]:
    data = (
        ("RE-207", "platform-main-lifecycle-source-surface-map", "Map source-backed lifecycle surfaces for the entrypoint, disc bootstrap, and vertical-sync callback.", "main, InitNewCDSystem, and VSyncFunc lifecycle source surfaces", "Lifecycle surface map published with no source dumps"),
        ("RE-208", "platform-main-lifecycle-argument-taxonomy", "Classify entrypoint, disc bootstrap, and callback state families.", "platform-main-lifecycle argument and state families", "Taxonomy separates source-backed shapes from unproven runtime assumptions"),
        ("RE-209", "platform-main-lifecycle-state-contract", "Document lifecycle state contracts required before reconstruction or marker updates.", "platform-main-lifecycle source state and helper contract rows", "State contract records exact blockers"),
        ("RE-210", "platform-main-lifecycle-equivalence-gate", "Compare source-level contracts against non-raw ND lifecycle metadata without versioning raw evidence.", "platform-main-lifecycle contract rows", "Readiness matrix names ready rows or remains blocked"),
        ("RE-211", "platform-main-lifecycle-source-patch-gate", "Apply a minimal patch only if RE-210 marks rows ready; otherwise emit a no-patch gate.", "patch-ready platform-main-lifecycle rows only", "Patch/build/tests pass or no-patch blocker is published"),
        ("RE-212", "module-spec-psxpc-n-platform-main-lifecycle-exhaustion-handoff", "Close the SPEC_PSXPC_N cluster queue when every cluster is closed or proof-blocked.", "remaining SPEC_PSXPC_N clusters after platform-main-lifecycle", "Handoff records parent-domain exhaustion instead of inventing a new ticket"),
    )
    return tuple(TicketPlanRow(story_id, topic, goal, scope, "blocked-until-proof", exit_condition) for story_id, topic, goal, scope, exit_condition in data)


def build_lifecycle_rows(audit_rows: tuple[AuditRow, ...]) -> tuple[LifecycleRow, ...]:
    rows: list[LifecycleRow] = []
    for audit in audit_rows:
        family, entry, state, contract, source_file = FAMILY[audit.function]
        if audit.file != source_file:
            raise ValueError(f"{audit.function} source file drift: {audit.file!r}")
        rows.append(LifecycleRow(
            function=audit.function,
            source_file=audit.file,
            source_line_range="function-body-summarized-metadata-only",
            lifecycle_family=family,
            entry_surface=entry,
            state_surface=state,
            source_contract=contract,
            proof_status="source-lifecycle-surface-mapped-only",
            patch_ready="no",
            blocker="missing-non-raw-nd-lifecycle-equivalence-proof",
        ))
    return tuple(rows)


def build_taxonomy_rows(audit_rows: tuple[AuditRow, ...]) -> tuple[TaxonomyRow, ...]:
    return tuple(TaxonomyRow(
        function=row.function,
        argument_family=FAMILY[row.function][0],
        argument_kinds=FAMILY[row.function][1],
        state_fields=FAMILY[row.function][2],
        source_contract=FAMILY[row.function][3],
        proof_status="taxonomy-source-backed-only",
        code_change_ready="no",
        marker_ready="no",
        blocker="missing-non-raw-nd-lifecycle-equivalence-proof",
    ) for row in audit_rows)


def build_contract_rows(taxonomy_rows: tuple[TaxonomyRow, ...]) -> tuple[ContractRow, ...]:
    return tuple(ContractRow(
        function=row.function,
        contract_id=f"contract-platform-main-lifecycle-{row.argument_family}",
        required_source_state=row.state_fields,
        required_binary_metadata="non-raw-nd-lifecycle-equivalence-metadata-required",
        contract_status="blocked-source-contract-only",
        code_change_ready="no",
        marker_ready="no",
        blocker="missing-non-raw-nd-lifecycle-equivalence-proof",
    ) for row in taxonomy_rows)


def build_equivalence_rows(contract_rows: tuple[ContractRow, ...]) -> tuple[EquivalenceRow, ...]:
    return tuple(EquivalenceRow(
        function=row.function,
        contract_id=row.contract_id,
        source_evidence="source-contract-and-lifecycle-surface-metadata",
        binary_evidence="not-versioned-non-raw-nd-equivalence-proof-missing",
        equivalence_status="blocked-missing-non-raw-nd-lifecycle-equivalence-proof",
        code_change_ready="no",
        marker_ready="no",
        blocker="missing-non-raw-nd-lifecycle-equivalence-proof",
    ) for row in contract_rows)


def build_source_patch_rows(equivalence_rows: tuple[EquivalenceRow, ...]) -> tuple[SourcePatchRow, ...]:
    return tuple(SourcePatchRow(
        function=row.function,
        source_patch_allowed="no",
        marker_change_allowed="no",
        decision="deny-source-and-marker-change",
        dependency="RE-210 equivalence gate reported zero ready rows",
        blocker=row.blocker,
    ) for row in equivalence_rows)


def build_handoff() -> Handoff:
    return Handoff(
        next_ticket="TBD",
        next_topic="module-spec-psxpc-n-exhausted",
        selected_cluster="module-spec_psxpc_n",
        selected_pivot="all-clusters-proof-blocked-or-closed",
        outcome="module-spec-psxpc-n-exhausted-after-platform-main-lifecycle",
        reason="All SPEC_PSXPC_N clusters from the authoritative RE-163 queue are now closed or proof-blocked by metadata-only gates",
        dependency="RE-212 platform-main-lifecycle exhaustion handoff",
        code_change_readiness="blocked",
        stop_condition="parent domain exhausted; choose a new proof domain before assigning another numbered ticket",
    )


def build_tickets(handoff: Handoff) -> tuple[Ticket, ...]:
    specs = (
        ("RE-206", "platform-main-lifecycle-proof-first-audit", "RE-207", (AUDIT_CSV, PLAN_CSV), ("RE-205 handoff consumed", "platform-main-lifecycle proof chain opened with no source or marker changes")),
        ("RE-207", "platform-main-lifecycle-source-surface-map", "RE-208", (LIFECYCLE_CSV,), ("source lifecycle surfaces mapped without source dumps", "entrypoint, disc bootstrap, and vertical-sync callback state summarized")),
        ("RE-208", "platform-main-lifecycle-argument-taxonomy", "RE-209", (TAXONOMY_CSV,), ("entrypoint, disc-system, and callback families classified", "taxonomy remains source-backed only")),
        ("RE-209", "platform-main-lifecycle-state-contract", "RE-210", (CONTRACT_CSV,), ("state contracts published for every scoped function", "ND lifecycle equivalence metadata remains missing")),
        ("RE-210", "platform-main-lifecycle-equivalence-gate", "RE-211", (EQUIVALENCE_CSV,), ("equivalence gate has zero code-change-ready rows", "non-raw ND lifecycle proof remains the blocker")),
        ("RE-211", "platform-main-lifecycle-source-patch-gate", "RE-212", (SOURCE_PATCH_CSV,), ("RE-211 source-patch gate denied source and marker changes", "no production source or marker files are modified")),
        ("RE-212", "module-spec-psxpc-n-platform-main-lifecycle-exhaustion-handoff", handoff.next_ticket, (HANDOFF_CSV,), ("RE-211 source-patch gate denied source and marker changes", "module-spec_psxpc_n exhausted", f"next ticket: `{handoff.next_ticket}`", f"selected pivot: `{handoff.selected_pivot}`")),
    )
    tickets: list[Ticket] = []
    for story_id, title, next_ticket, artifacts, findings in specs:
        tickets.append(Ticket(
            story_id=story_id,
            title=title,
            status="completed-documentation-only",
            decision="blocked-no-source-or-marker-change" if story_id != "RE-212" else "parent-domain-exhausted-proof-blocked",
            next_ticket=next_ticket,
            code_change_readiness="blocked",
            progress=(
                "[x] consumed upstream scope/plan",
                "[x] emitted deterministic metadata-only artifacts",
                "[x] kept source and marker changes blocked",
                "[x] recorded validation path and next dependency",
            ),
            generated_artifacts=tuple(artifacts) + (CHAIN_CSV, MD_OUTPUT),
            findings=findings,
        ))
    return tuple(tickets)


def build_platform_main_lifecycle_epic(repo: Path) -> PlatformMainLifecycleEpic:
    verify_inputs(repo)
    audit_rows = build_audit_rows(read_csv(repo / RE163_AUDIT_CSV))
    plan_rows = build_plan_rows()
    lifecycle_rows = build_lifecycle_rows(audit_rows)
    taxonomy_rows = build_taxonomy_rows(audit_rows)
    contract_rows = build_contract_rows(taxonomy_rows)
    equivalence_rows = build_equivalence_rows(contract_rows)
    source_patch_rows = build_source_patch_rows(equivalence_rows)
    handoff = build_handoff()
    tickets = build_tickets(handoff)
    return PlatformMainLifecycleEpic(
        domain_id="module-spec_psxpc_n",
        cluster="platform-main-lifecycle",
        upstream_ticket="RE-205",
        pivot="main",
        status="platform-main-lifecycle-epic-closed-with-proof-blocker",
        final_decision="documentation-only-terminal-blocker",
        next_ticket=handoff.next_ticket,
        code_change_ready_count=sum(row.code_change_ready == "yes" for row in equivalence_rows),
        marker_ready_count=sum(row.marker_ready == "yes" for row in equivalence_rows),
        source_patch_ready_count=sum(row.source_patch_allowed == "yes" for row in source_patch_rows),
        audit_rows=audit_rows,
        plan_rows=plan_rows,
        lifecycle_rows=lifecycle_rows,
        taxonomy_rows=taxonomy_rows,
        contract_rows=contract_rows,
        equivalence_rows=equivalence_rows,
        source_patch_rows=source_patch_rows,
        next_selection_rows=(),
        handoff=handoff,
        tickets=tickets,
    )


def write_story(ticket: Ticket, epic: PlatformMainLifecycleEpic, out_dir: Path) -> Path:
    path = out_dir / STORY_DIR / f"{ticket.story_id}-{ticket.title}.md"
    lines = [
        f"# {ticket.story_id} — {ticket.title}",
        "",
        "## Goal",
        f"Advance `{epic.cluster}` in `{epic.domain_id}` using metadata-only proof artifacts.",
        "",
        "## Progress tracker",
        *[f"- {item}" for item in ticket.progress],
        "",
        "## Generated artifacts",
        *[f"- `{artifact}`" for artifact in ticket.generated_artifacts],
        "",
        "## Findings",
        *[f"- {finding}" for finding in ticket.findings],
        "",
        "## Readiness decision",
        f"- status: `{ticket.status}`",
        f"- decision: `{ticket.decision}`",
        f"- code change readiness: `{ticket.code_change_readiness}`",
        f"- next ticket: `{ticket.next_ticket}`",
        "",
        "## Validation",
        "- `python3 -m pytest tests/reverse/test_re206_re212_platform_main_lifecycle_epic.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over generated RE-206..RE-212 artifacts",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_all_artifacts(epic: PlatformMainLifecycleEpic, out_dir: Path) -> dict[str, Path]:
    written: dict[str, Path] = {}
    csv_specs = (
        ("audit_csv", AUDIT_CSV, AuditRow, epic.audit_rows),
        ("plan_csv", PLAN_CSV, TicketPlanRow, epic.plan_rows),
        ("lifecycle_csv", LIFECYCLE_CSV, LifecycleRow, epic.lifecycle_rows),
        ("taxonomy_csv", TAXONOMY_CSV, TaxonomyRow, epic.taxonomy_rows),
        ("contract_csv", CONTRACT_CSV, ContractRow, epic.contract_rows),
        ("equivalence_csv", EQUIVALENCE_CSV, EquivalenceRow, epic.equivalence_rows),
        ("source_patch_csv", SOURCE_PATCH_CSV, SourcePatchRow, epic.source_patch_rows),
    )
    for key, rel, cls, rows in csv_specs:
        path = out_dir / rel
        write_dict_csv(path, list(cls.__dataclass_fields__), [row.__dict__ for row in rows])
        written[key] = path
    write_dict_csv(out_dir / HANDOFF_CSV, list(Handoff.__dataclass_fields__), [epic.handoff.__dict__])
    written["handoff_csv"] = out_dir / HANDOFF_CSV
    write_dict_csv(out_dir / CHAIN_CSV, list(Ticket.__dataclass_fields__), [{**ticket.__dict__, "progress": ";".join(ticket.progress), "generated_artifacts": ";".join(ticket.generated_artifacts), "findings": ";".join(ticket.findings)} for ticket in epic.tickets])
    written["chain_csv"] = out_dir / CHAIN_CSV

    md_path = out_dir / MD_OUTPUT
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join([
        "# RE-206..RE-212 platform-main-lifecycle epic",
        "",
        f"status: `{epic.status}`",
        f"final decision: `{epic.final_decision}`",
        f"source-patch-ready rows: `{epic.source_patch_ready_count}`",
        f"marker-ready rows: `{epic.marker_ready_count}`",
        f"next ticket: `{epic.handoff.next_ticket}`",
        f"next objective: `{epic.handoff.selected_cluster}` / `{epic.handoff.selected_pivot}`",
        "",
        "## Scope",
        *[f"- `{row.function}` — {row.proof_status}; blocker `{row.blocker}`" for row in epic.audit_rows],
        "",
        "## Gate result",
        "No source or marker patch is authorized because the non-raw ND lifecycle equivalence proof is still missing.",
        "",
        "## Parent-domain handoff",
        "module-spec_psxpc_n exhausted; choose a new proof domain before assigning another numbered ticket.",
        "",
    ]), encoding="utf-8")
    written["md"] = md_path

    for ticket in epic.tickets:
        written[ticket.story_id] = write_story(ticket, epic, out_dir)
    return written


def ensure_metadata_only(paths: list[Path]) -> None:
    fragments = FORBIDDEN_FRAGMENTS + STALE_FRAGMENTS
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        for fragment in fragments:
            if fragment in text:
                raise ValueError(f"forbidden fragment {fragment!r} in {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    epic = build_platform_main_lifecycle_epic(args.repo)
    written = write_all_artifacts(epic, args.repo)
    ensure_metadata_only(list(written.values()))
    print(f"generated {len(written)} RE-206..RE-212 platform-main-lifecycle artifacts; next={epic.handoff.next_ticket} {epic.handoff.next_topic}")


if __name__ == "__main__":
    main()
