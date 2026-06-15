#!/usr/bin/env python3
"""Generate RE-178..RE-184 frontend-sequence epic artifacts."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path

RE177_HANDOFF_CSV = "docs/reverse/generated/re177-module-spec-psxpc-n-post-geometry-handoff.csv"
RE177_SELECTION_CSV = "docs/reverse/generated/re177-module-spec-psxpc-n-post-geometry-next-cluster-selection.csv"
RE163_AUDIT_CSV = "docs/reverse/generated/re163-module-spec-psxpc-n-proof-first-audit.csv"
RE163_CLUSTERS_CSV = "docs/reverse/generated/re163-module-spec-psxpc-n-clusters.csv"
AUDIT_CSV = "docs/reverse/generated/re178-frontend-sequence-proof-first-audit.csv"
PLAN_CSV = "docs/reverse/generated/re178-frontend-sequence-ticket-plan.csv"
CALLSITE_CSV = "docs/reverse/generated/re179-frontend-sequence-caller-state-map.csv"
TAXONOMY_CSV = "docs/reverse/generated/re180-frontend-sequence-argument-taxonomy.csv"
CONTRACT_CSV = "docs/reverse/generated/re181-frontend-sequence-state-contract.csv"
EQUIVALENCE_CSV = "docs/reverse/generated/re182-frontend-sequence-equivalence-gate.csv"
SOURCE_PATCH_CSV = "docs/reverse/generated/re183-frontend-sequence-source-patch-gate.csv"
NEXT_SELECTION_CSV = "docs/reverse/generated/re184-module-spec-psxpc-n-post-frontend-sequence-next-cluster-selection.csv"
HANDOFF_CSV = "docs/reverse/generated/re184-module-spec-psxpc-n-post-frontend-sequence-handoff.csv"
CHAIN_CSV = "docs/reverse/generated/re178-re184-frontend-sequence-epic.csv"
MD_OUTPUT = "docs/reverse/functions/re178-re184-frontend-sequence-epic.md"
STORY_DIR = "docs/stories"

FORBIDDEN_FRAGMENTS = ("0x", "payload", "opcode", "machine word", "raw call target", "word_le_hex", "call_address")
STALE_FRAGMENTS = ("ui text rendering", "ui-text-rendering", "item-lighting", "geometry support chain")
EXPECTED_SCOPE = ("S_PlayFMV", "sub_1054")
EXPECTED_PLAN = ("RE-179", "RE-180", "RE-181", "RE-182", "RE-183", "RE-184")
C_KEYWORD_ARTIFACTS = {"if", "for", "while", "switch", "else", "do"}

FAMILY = {
    "S_PlayFMV": ("fmv-sequence-playback", "sequence id and playback flag", "fmv-trigger-mask;vram-reset;display-environment;disc-version-gates", "plays or suppresses frontend FMV sequence"),
    "sub_1054": ("cutscene-selector-menu", "menu navigation state", "raw-input-edge;cutscene-selector-flag;selected-cutscene;menu-text-index", "updates cutscene selector and launches chosen cutscene state"),
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
class CallsiteRow:
    caller: str
    callee: str
    caller_file: str
    callee_file: str
    line: int
    source_line_text: str
    relationship: str
    state_surface: str
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
class NextSelectionRow:
    rank: int
    cluster: str
    top_function: str
    selection_decision: str
    next_ticket: str
    next_topic: str
    blocker: str
    code_change_readiness: str


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
class FrontendSequenceEpic:
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
    callsite_rows: tuple[CallsiteRow, ...]
    taxonomy_rows: tuple[TaxonomyRow, ...]
    contract_rows: tuple[ContractRow, ...]
    equivalence_rows: tuple[EquivalenceRow, ...]
    source_patch_rows: tuple[SourcePatchRow, ...]
    next_selection_rows: tuple[NextSelectionRow, ...]
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


def verify_inputs(repo: Path) -> tuple[dict[str, str], list[dict[str, str]], list[dict[str, str]]]:
    handoff_rows = read_csv(repo / RE177_HANDOFF_CSV)
    if len(handoff_rows) != 1:
        raise ValueError("RE-177 handoff must contain exactly one row")
    handoff = handoff_rows[0]
    expected = {
        "next_ticket": "RE-178",
        "next_topic": "frontend-sequence-proof-first-audit",
        "selected_cluster": "frontend-sequence",
        "selected_pivot": "S_PlayFMV",
        "code_change_readiness": "blocked",
    }
    for key, value in expected.items():
        if handoff.get(key) != value:
            raise ValueError(f"RE-177 handoff drift: {key}={handoff.get(key)!r}")

    selection_rows = read_csv(repo / RE177_SELECTION_CSV)
    selected = [row for row in selection_rows if row.get("selection_decision") == "selected-next-proof-chain"]
    if len(selected) != 1 or selected[0].get("cluster") != "frontend-sequence":
        raise ValueError("RE-177 selection must pick exactly frontend-sequence")

    cluster_rows = [row for row in read_csv(repo / RE163_CLUSTERS_CSV) if row.get("cluster") == "frontend-sequence"]
    if len(cluster_rows) != 1 or cluster_rows[0].get("top_function") != "S_PlayFMV":
        raise ValueError("RE-163 frontend-sequence cluster metadata drifted")
    reps = tuple(cluster_rows[0].get("representative_functions", "").split(";"))
    if reps != EXPECTED_SCOPE:
        raise ValueError(f"frontend-sequence scope drifted: {reps}")
    return handoff, selection_rows, read_csv(repo / RE163_AUDIT_CSV)


def build_audit_rows(audit_rows: list[dict[str, str]]) -> tuple[AuditRow, ...]:
    by_function = {row.get("function", ""): row for row in audit_rows if row.get("cluster") == "frontend-sequence"}
    missing = [function for function in EXPECTED_SCOPE if function not in by_function]
    extra = sorted(function for function in by_function if function not in EXPECTED_SCOPE)
    if missing or extra:
        raise ValueError(f"frontend-sequence audit scope drift: missing={missing}, extra={extra}")
    rows: list[AuditRow] = []
    for function in EXPECTED_SCOPE:
        source = by_function[function]
        rows.append(AuditRow(
            function=function,
            file=source["file"],
            line=int(source["line"]),
            role="pivot" if function == "S_PlayFMV" else "runtime-context",
            source_status=source.get("status", ""),
            prior_code_ready=source.get("code_change_ready", "no"),
            prior_marker_ready=source.get("marker_ready", "no"),
            proof_status="source-scope-inventory-only",
            code_change_ready="no",
            marker_ready="no",
            blocker="missing-frontend-sequence-caller-state-and-non-raw-equivalence-proof",
        ))
    return tuple(rows)


def caller_for_line(path: Path, line_index: int) -> str:
    function_re = re.compile(r"^\s*(?:static\s+)?(?:int|void|long|short|char|bool|struct\s+\w+|unsigned\s+char)\s+\*?\s*([A-Za-z_][A-Za-z0-9_]*)\s*\([^;]*\)\s*(?://.*)?$")
    current = "file-scope-reference"
    pending = ""
    depth = 0
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines()[: line_index + 1]:
        clean = strip_comments(line).rstrip()
        sig = function_re.match(clean)
        if sig and sig.group(1) not in C_KEYWORD_ARTIFACTS:
            pending = sig.group(1)
        if pending and "{" in clean:
            current = pending
            pending = ""
            depth = 1
            continue
        if current != "file-scope-reference":
            depth += clean.count("{")
            depth -= clean.count("}")
            if depth <= 0 and clean.strip() == "}":
                current = "file-scope-reference"
    return current


def is_definition_line(clean: str, function: str) -> bool:
    return bool(re.match(rf"^\s*(?:static\s+)?(?:int|void|long|short|char|bool|struct\s+\w+|unsigned\s+char)\s+\*?\s*{re.escape(function)}\s*\(", clean))


def build_plan_rows() -> tuple[TicketPlanRow, ...]:
    data = (
        ("RE-179", "frontend-sequence-caller-state-map", "Map source-backed frontend sequence callers and state surfaces.", "S_PlayFMV and sub_1054 source-backed caller/state surfaces", "Caller/state map published with no synthetic edges"),
        ("RE-180", "frontend-sequence-argument-taxonomy", "Classify FMV playback and cutscene selector argument/state families.", "frontend-sequence argument families", "Taxonomy separates source-backed shapes from unproven runtime assumptions"),
        ("RE-181", "frontend-sequence-state-contract", "Document frontend sequence state contracts required before reconstruction or marker updates.", "frontend-sequence source state and helper contract rows", "State contract records exact blockers"),
        ("RE-182", "frontend-sequence-equivalence-gate", "Compare source-level contracts against non-raw binary metadata without versioning raw evidence.", "frontend-sequence contract rows", "Readiness matrix names ready rows or remains blocked"),
        ("RE-183", "frontend-sequence-source-patch-gate", "Apply a minimal patch only if RE-182 marks rows ready; otherwise emit a no-patch gate.", "patch-ready frontend-sequence rows only", "Patch/build/tests pass or no-patch blocker is published"),
        ("RE-184", "module-spec-psxpc-n-post-frontend-sequence-next-cluster-selection", "Select the next SPEC_PSXPC_N cluster after frontend-sequence closes or blocks.", "remaining SPEC_PSXPC_N clusters after frontend-sequence", "Next cluster handoff artifact names the next objective"),
    )
    return tuple(TicketPlanRow(story_id, topic, goal, scope, "blocked-until-proof", exit_condition) for story_id, topic, goal, scope, exit_condition in data)


def build_callsite_rows(repo: Path, audit_rows: tuple[AuditRow, ...]) -> tuple[CallsiteRow, ...]:
    by_function = {row.function: row for row in audit_rows}
    search_roots = [repo / "SPEC_PSXPC_N", repo / "GAME"]
    rows: list[CallsiteRow] = []
    for root in search_roots:
        for path in sorted(root.glob("*.C")):
            rel = path.relative_to(repo).as_posix()
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
            for idx, line in enumerate(lines):
                clean = strip_comments(line)
                for function, audit in by_function.items():
                    if not re.search(rf"\b{re.escape(function)}\s*\(", clean):
                        continue
                    if is_definition_line(clean, function):
                        continue
                    caller = caller_for_line(path, idx)
                    if caller in C_KEYWORD_ARTIFACTS:
                        raise ValueError(f"keyword caller artifact for {function}: {caller}")
                    rows.append(CallsiteRow(
                        caller=caller,
                        callee=function,
                        caller_file=rel,
                        callee_file=audit.file,
                        line=idx + 1,
                        source_line_text="source-line-contains-callee-call",
                        relationship="source-backed-callsite",
                        state_surface=FAMILY[function][2],
                        proof_status="source-callsite-mapped-only",
                        patch_ready="no",
                        blocker="missing-non-raw-binary-equivalence-proof",
                    ))
    seen = {row.callee for row in rows}
    if seen != set(EXPECTED_SCOPE):
        raise ValueError(f"expected source-backed callsites for all frontend-sequence functions, saw {seen}")
    return tuple(sorted(rows, key=lambda row: (EXPECTED_SCOPE.index(row.callee), row.caller_file, row.line, row.caller)))


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
        blocker="missing-non-raw-binary-equivalence-proof",
    ) for row in audit_rows)


def build_contract_rows(taxonomy_rows: tuple[TaxonomyRow, ...]) -> tuple[ContractRow, ...]:
    return tuple(ContractRow(
        function=row.function,
        contract_id=f"contract-frontend-sequence-{row.argument_family}",
        required_source_state=row.state_fields,
        required_binary_metadata="non-raw-behavior-equivalence-metadata-required",
        contract_status="blocked-source-contract-only",
        code_change_ready="no",
        marker_ready="no",
        blocker="missing-non-raw-binary-equivalence-proof",
    ) for row in taxonomy_rows)


def build_equivalence_rows(contract_rows: tuple[ContractRow, ...]) -> tuple[EquivalenceRow, ...]:
    return tuple(EquivalenceRow(
        function=row.function,
        contract_id=row.contract_id,
        source_evidence="source-contract-and-callsite-metadata",
        binary_evidence="not-versioned-non-raw-equivalence-proof-missing",
        equivalence_status="blocked-missing-non-raw-binary-equivalence-proof",
        code_change_ready="no",
        marker_ready="no",
        blocker="missing-non-raw-binary-equivalence-proof",
    ) for row in contract_rows)


def build_source_patch_rows(equivalence_rows: tuple[EquivalenceRow, ...]) -> tuple[SourcePatchRow, ...]:
    return tuple(SourcePatchRow(
        function=row.function,
        source_patch_allowed="no",
        marker_change_allowed="no",
        decision="deny-source-and-marker-change",
        dependency="RE-182 equivalence gate reported zero ready rows",
        blocker=row.blocker,
    ) for row in equivalence_rows)


def normalized_post_frontend_sequence_blocker(cluster: str) -> str:
    if cluster.startswith("platform-"):
        return "ND marker rows require a dedicated post-frontend-sequence behavior audit after non-ND proof clusters"
    return "cluster needs source-level state contract and non-raw binary equivalence proof"


def build_next_selection(selection_rows: list[dict[str, str]]) -> tuple[NextSelectionRow, ...]:
    remaining = [row for row in selection_rows if row.get("cluster") != "frontend-sequence"]
    selected_cluster = "frontend-loadsave"
    rows: list[NextSelectionRow] = []
    for index, row in enumerate(remaining, start=1):
        cluster = row.get("cluster", "")
        selected = cluster == selected_cluster
        rows.append(NextSelectionRow(
            rank=index,
            cluster=cluster,
            top_function=row.get("top_function", ""),
            selection_decision="selected-next-proof-chain" if selected else "deferred-after-selected-cluster",
            next_ticket="RE-185" if selected else "TBD",
            next_topic="frontend-loadsave-proof-first-audit" if selected else "deferred",
            blocker=normalized_post_frontend_sequence_blocker(cluster),
            code_change_readiness="blocked",
        ))
    if not rows or rows[0].cluster != selected_cluster:
        raise ValueError(f"post-frontend-sequence selection did not select {selected_cluster}: {rows}")
    return tuple(rows)


def build_tickets(handoff: Handoff) -> tuple[Ticket, ...]:
    specs = (
        ("RE-178", "frontend-sequence-proof-first-audit", "RE-179", (AUDIT_CSV, PLAN_CSV), ("RE-177 handoff consumed", "frontend-sequence proof chain opened with no source or marker changes")),
        ("RE-179", "frontend-sequence-caller-state-map", "RE-180", (CALLSITE_CSV,), ("source-backed callsites mapped without synthetic edges", "caller keyword artifacts rejected")),
        ("RE-180", "frontend-sequence-argument-taxonomy", "RE-181", (TAXONOMY_CSV,), ("FMV playback and cutscene selector families classified", "taxonomy remains source-backed only")),
        ("RE-181", "frontend-sequence-state-contract", "RE-182", (CONTRACT_CSV,), ("state contracts published for every scoped function", "binary equivalence metadata remains missing")),
        ("RE-182", "frontend-sequence-equivalence-gate", "RE-183", (EQUIVALENCE_CSV,), ("equivalence gate has zero code-change-ready rows", "non-raw binary equivalence proof remains the blocker")),
        ("RE-183", "frontend-sequence-source-patch-gate", "RE-184", (SOURCE_PATCH_CSV,), ("RE-183 source-patch gate denied source and marker changes", "no production source or marker files are modified")),
        ("RE-184", "module-spec-psxpc-n-post-frontend-sequence-next-cluster-selection", handoff.next_ticket, (NEXT_SELECTION_CSV, HANDOFF_CSV), ("RE-183 source-patch gate denied source and marker changes", "frontend-sequence closed as proof-blocked", f"next ticket: `{handoff.next_ticket}`", f"selected cluster: `{handoff.selected_cluster}`")),
    )
    tickets: list[Ticket] = []
    for story_id, title, next_ticket, artifacts, findings in specs:
        tickets.append(Ticket(
            story_id=story_id,
            title=title,
            status="completed-documentation-only",
            decision="blocked-no-source-or-marker-change" if story_id != "RE-184" else "next-cluster-selected-source-patch-blocked",
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


def build_frontend_sequence_epic(repo: Path) -> FrontendSequenceEpic:
    _, selection_rows, source_audit_rows = verify_inputs(repo)
    audit_rows = build_audit_rows(source_audit_rows)
    plan_rows = build_plan_rows()
    callsite_rows = build_callsite_rows(repo, audit_rows)
    taxonomy_rows = build_taxonomy_rows(audit_rows)
    contract_rows = build_contract_rows(taxonomy_rows)
    equivalence_rows = build_equivalence_rows(contract_rows)
    source_patch_rows = build_source_patch_rows(equivalence_rows)
    next_selection_rows = build_next_selection(selection_rows)
    selected = next(row for row in next_selection_rows if row.selection_decision == "selected-next-proof-chain")
    handoff = Handoff(
        next_ticket=selected.next_ticket,
        next_topic=selected.next_topic,
        selected_cluster=selected.cluster,
        selected_pivot=selected.top_function,
        outcome="frontend-sequence-proof-blocked-next-cluster-selected",
        reason="frontend-sequence reached a documentation-only terminal blocker; frontend-loadsave is the next non-ND proof cluster in the current ordering",
        dependency="RE-184 post-frontend-sequence next-cluster selection",
        code_change_readiness="blocked",
        stop_condition="frontend-loadsave proof-first audit emitted",
    )
    tickets = build_tickets(handoff)
    return FrontendSequenceEpic(
        domain_id="module-spec_psxpc_n",
        cluster="frontend-sequence",
        upstream_ticket="RE-177",
        pivot="S_PlayFMV",
        status="frontend-sequence-epic-closed-with-proof-blocker",
        final_decision="documentation-only-terminal-blocker",
        next_ticket=handoff.next_ticket,
        code_change_ready_count=sum(row.code_change_ready == "yes" for row in equivalence_rows),
        marker_ready_count=sum(row.marker_ready == "yes" for row in equivalence_rows),
        source_patch_ready_count=sum(row.source_patch_allowed == "yes" for row in source_patch_rows),
        audit_rows=audit_rows,
        plan_rows=plan_rows,
        callsite_rows=callsite_rows,
        taxonomy_rows=taxonomy_rows,
        contract_rows=contract_rows,
        equivalence_rows=equivalence_rows,
        source_patch_rows=source_patch_rows,
        next_selection_rows=next_selection_rows,
        handoff=handoff,
        tickets=tickets,
    )


def write_story(ticket: Ticket, epic: FrontendSequenceEpic, out_dir: Path) -> Path:
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
        "- `python3 -m pytest tests/reverse/test_re178_re184_frontend_sequence_epic.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over generated RE-178..RE-184 artifacts",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_all_artifacts(epic: FrontendSequenceEpic, out_dir: Path) -> dict[str, Path]:
    written: dict[str, Path] = {}
    csv_specs = (
        ("audit_csv", AUDIT_CSV, AuditRow, epic.audit_rows),
        ("plan_csv", PLAN_CSV, TicketPlanRow, epic.plan_rows),
        ("callsite_csv", CALLSITE_CSV, CallsiteRow, epic.callsite_rows),
        ("taxonomy_csv", TAXONOMY_CSV, TaxonomyRow, epic.taxonomy_rows),
        ("contract_csv", CONTRACT_CSV, ContractRow, epic.contract_rows),
        ("equivalence_csv", EQUIVALENCE_CSV, EquivalenceRow, epic.equivalence_rows),
        ("source_patch_csv", SOURCE_PATCH_CSV, SourcePatchRow, epic.source_patch_rows),
        ("next_selection_csv", NEXT_SELECTION_CSV, NextSelectionRow, epic.next_selection_rows),
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
        "# RE-178..RE-184 frontend-sequence epic",
        "",
        f"status: `{epic.status}`",
        f"final decision: `{epic.final_decision}`",
        f"source-patch-ready rows: `{epic.source_patch_ready_count}`",
        f"marker-ready rows: `{epic.marker_ready_count}`",
        f"next ticket: `{epic.handoff.next_ticket}`",
        f"next cluster: `{epic.handoff.selected_cluster}` / `{epic.handoff.selected_pivot}`",
        "",
        "## Scope",
        *[f"- `{row.function}` — {row.proof_status}; blocker `{row.blocker}`" for row in epic.audit_rows],
        "",
        "## Gate result",
        "No source or marker patch is authorized because the non-raw binary equivalence proof is still missing.",
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
    epic = build_frontend_sequence_epic(args.repo)
    written = write_all_artifacts(epic, args.repo)
    ensure_metadata_only(list(written.values()))
    print(f"generated {len(written)} RE-178..RE-184 frontend-sequence artifacts; next={epic.handoff.next_ticket} {epic.handoff.next_topic}")


if __name__ == "__main__":
    main()
