#!/usr/bin/env python3
"""Generate RE-171..RE-177 geometry-support closure artifacts."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path

RE170_PLAN_CSV = "docs/reverse/generated/re170-geometry-support-ticket-plan.csv"
RE170_SCOPE_CSV = "docs/reverse/generated/re170-module-spec-psxpc-n-geometry-support-scope.csv"
RE169_SELECTION_CSV = "docs/reverse/generated/re169-module-spec-psxpc-n-next-cluster-selection.csv"
AUDIT_CSV = "docs/reverse/generated/re171-geometry-support-proof-first-audit.csv"
CALLSITE_CSV = "docs/reverse/generated/re172-geometry-support-caller-state-map.csv"
TAXONOMY_CSV = "docs/reverse/generated/re173-geometry-support-argument-taxonomy.csv"
CONTRACT_CSV = "docs/reverse/generated/re174-geometry-support-state-contract.csv"
EQUIVALENCE_CSV = "docs/reverse/generated/re175-geometry-support-equivalence-gate.csv"
SOURCE_PATCH_CSV = "docs/reverse/generated/re176-geometry-support-source-patch-gate.csv"
NEXT_SELECTION_CSV = "docs/reverse/generated/re177-module-spec-psxpc-n-post-geometry-next-cluster-selection.csv"
HANDOFF_CSV = "docs/reverse/generated/re177-module-spec-psxpc-n-post-geometry-handoff.csv"
CHAIN_CSV = "docs/reverse/generated/re171-re177-geometry-support-chain.csv"
MD_OUTPUT = "docs/reverse/functions/re171-re177-geometry-support-chain.md"
STORY_DIR = "docs/stories"

FORBIDDEN_FRAGMENTS = ("0x", "payload", "opcode", "machine word", "raw call target", "word_le_hex", "call_address")
EXPECTED_PLAN = ("RE-171", "RE-172", "RE-173", "RE-174", "RE-175", "RE-176", "RE-177")
EXPECTED_SCOPE = (
    "GetBoundsAccurate",
    "CalcClipWindow_ONGTE",
    "InterpolateMatrix_CL",
    "GetFrames_CL",
    "GetBestFrame",
    "GetChange",
    "DecodeTrack",
)
C_KEYWORD_ARTIFACTS = {"if", "for", "while", "switch", "else", "do"}

FAMILY = {
    "GetBoundsAccurate": ("bounds-item", "ITEM_INFO pointer", "interpolated-bounds-buffer;frame-pair;animation-frame-number", "returns frame-accurate bounds pointer"),
    "CalcClipWindow_ONGTE": ("clip-window", "screen clip window inputs", "clip-window-edges;gte-projected-extents", "computes on-screen clipping window"),
    "InterpolateMatrix_CL": ("matrix-interpolation", "matrix source and output pointers", "gte-matrix-registers;interpolated-matrix-buffer", "interpolates transform matrix rows"),
    "GetFrames_CL": ("frame-pair", "ITEM_INFO plus frame output slots", "animation-table;frame-pointer-pair;interpolation-count", "selects frame pair and interpolation remainder"),
    "GetBestFrame": ("best-frame", "ITEM_INFO pointer", "animation-frame;bounds-selection;frame-pointer", "selects best available frame metadata"),
    "GetChange": ("animation-change", "ITEM_INFO and ANIM_STRUCT pointers", "change-table;range-table;goal-state", "applies animation change when range matches"),
    "DecodeTrack": ("track-decode", "packed track and RTDECODE pointers", "decode-counter;decode-type;track-offset", "decodes packed track stream state"),
}


@dataclass(frozen=True)
class AuditRow:
    function: str
    file: str
    line: int
    role: str
    source_status: str
    proof_status: str
    code_change_ready: str
    marker_ready: str
    blocker: str


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
class GeometrySupportChain:
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


def verify_inputs(repo: Path) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    plan_ids = tuple(row.get("story_id", "") for row in read_csv(repo / RE170_PLAN_CSV))
    if plan_ids != EXPECTED_PLAN:
        raise ValueError(f"RE-170 plan drifted before RE-171..RE-177: {plan_ids}")
    scope_rows = read_csv(repo / RE170_SCOPE_CSV)
    scope_ids = tuple(row.get("function", "") for row in scope_rows)
    if scope_ids != EXPECTED_SCOPE:
        raise ValueError(f"RE-170 geometry scope drifted: {scope_ids}")
    if any(row.get("code_change_readiness") != "blocked" for row in scope_rows):
        raise ValueError("RE-171 refuses an already-ready geometry-support scope")
    return scope_rows, read_csv(repo / RE169_SELECTION_CSV)


def caller_for_line(path: Path, line_index: int) -> str:
    function_re = re.compile(r"^\s*(?:static\s+)?(?:int|void|long|short|char|bool|struct\s+\w+|short\s*\*)\s*\*?\s*([A-Za-z_][A-Za-z0-9_]*)\s*\([^;]*\)\s*(?://.*)?$")
    current = "unknown-caller"
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
        if current != "unknown-caller":
            depth += clean.count("{")
            depth -= clean.count("}")
            if depth <= 0 and clean.strip() == "}":
                current = "unknown-caller"
    if current == "unknown-caller":
        return "file-scope-reference"
    return current


def is_definition_line(clean: str, function: str) -> bool:
    return bool(re.match(rf"^\s*(?:static\s+)?(?:int|void|long|short|char|bool|struct\s+\w+|short\s*\*)\s*\*?\s*{re.escape(function)}\s*\(", clean))


def build_audit_rows(scope_rows: list[dict[str, str]]) -> tuple[AuditRow, ...]:
    rows: list[AuditRow] = []
    for source in scope_rows:
        function = source["function"]
        rows.append(AuditRow(
            function=function,
            file=source["file"],
            line=int(source["line"]),
            role=source["role"],
            source_status=source["source_status"],
            proof_status="source-scope-inventory-only",
            code_change_ready="no",
            marker_ready="no",
            blocker="missing-geometry-support-caller-state-and-non-raw-equivalence-proof",
        ))
    return tuple(rows)


def build_callsite_rows(repo: Path, audit_rows: tuple[AuditRow, ...]) -> tuple[CallsiteRow, ...]:
    by_function = {row.function: row for row in audit_rows}
    rows: list[CallsiteRow] = []
    for path in sorted((repo / "SPEC_PSXPC_N").glob("*.C")):
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
                    relationship="source-backed-callsite" if caller != function else "source-backed-helper-self-scope",
                    state_surface=FAMILY[function][2],
                    proof_status="source-callsite-mapped-only",
                    patch_ready="no",
                    blocker="missing-non-raw-binary-equivalence-proof",
                ))
    seen = {row.callee for row in rows}
    # Some leaf helpers have no callers in this source snapshot; keep their scope in the audit/taxonomy instead of inventing edges.
    if "GetBoundsAccurate" not in seen:
        raise ValueError("expected at least one source-backed GetBoundsAccurate callsite")
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
        contract_id=f"contract-geometry-support-{row.argument_family}",
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
        dependency="RE-175 equivalence gate reported zero ready rows",
        blocker=row.blocker,
    ) for row in equivalence_rows)


def normalized_post_geometry_blocker(cluster: str) -> str:
    if cluster.startswith("platform-"):
        return "ND marker rows require a dedicated post-geometry behavior audit after non-ND proof clusters"
    return "cluster needs source-level state contract and non-raw binary equivalence proof"


def build_next_selection(selection_rows: list[dict[str, str]]) -> tuple[NextSelectionRow, ...]:
    remaining = [row for row in selection_rows if row.get("cluster") != "geometry-support"]
    selected_cluster = "frontend-sequence"
    rows: list[NextSelectionRow] = []
    for index, row in enumerate(remaining, start=1):
        cluster = row.get("cluster", "")
        selected = cluster == selected_cluster
        rows.append(NextSelectionRow(
            rank=index,
            cluster=cluster,
            top_function=row.get("top_function", ""),
            selection_decision="selected-next-proof-chain" if selected else "deferred-after-selected-cluster",
            next_ticket="RE-178" if selected else "TBD",
            next_topic="frontend-sequence-proof-first-audit" if selected else "deferred",
            blocker=normalized_post_geometry_blocker(cluster),
            code_change_readiness="blocked",
        ))
    if not rows or rows[0].cluster != selected_cluster:
        raise ValueError(f"post-geometry selection did not select {selected_cluster}: {rows}")
    return tuple(rows)


def build_tickets(handoff: Handoff) -> tuple[Ticket, ...]:
    specs = (
        ("RE-171", "geometry-support-proof-first-audit", "RE-172", (AUDIT_CSV,), ("RE-170 geometry scope consumed", "all geometry-support rows remain documentation-only")),
        ("RE-172", "geometry-support-caller-state-map", "RE-173", (CALLSITE_CSV,), ("source-backed callsites mapped without synthetic edges", "caller keyword artifacts rejected")),
        ("RE-173", "geometry-support-argument-taxonomy", "RE-174", (TAXONOMY_CSV,), ("argument families split by bounds, clip, matrix, frame, change, and track roles", "taxonomy remains source-backed only")),
        ("RE-174", "geometry-support-state-contract", "RE-175", (CONTRACT_CSV,), ("state contracts published for every scoped function", "binary equivalence metadata remains missing")),
        ("RE-175", "geometry-support-equivalence-gate", "RE-176", (EQUIVALENCE_CSV,), ("equivalence gate has zero code-change-ready rows", "non-raw binary equivalence proof remains the blocker")),
        ("RE-176", "geometry-support-source-patch-gate", "RE-177", (SOURCE_PATCH_CSV,), ("RE-176 source-patch gate denied source and marker changes", "no production source or marker files are modified")),
        ("RE-177", "module-spec-psxpc-n-post-geometry-next-cluster-selection", handoff.next_ticket, (NEXT_SELECTION_CSV, HANDOFF_CSV), ("RE-176 source-patch gate denied source and marker changes", "geometry-support closed as proof-blocked", f"next ticket: `{handoff.next_ticket}`", f"selected cluster: `{handoff.selected_cluster}`")),
    )
    tickets: list[Ticket] = []
    for story_id, title, next_ticket, artifacts, findings in specs:
        tickets.append(Ticket(
            story_id=story_id,
            title=title,
            status="completed-documentation-only",
            decision="blocked-no-source-or-marker-change" if story_id != "RE-177" else "next-cluster-selected-source-patch-blocked",
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


def build_geometry_support_chain(repo: Path) -> GeometrySupportChain:
    scope_rows, selection_rows = verify_inputs(repo)
    audit_rows = build_audit_rows(scope_rows)
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
        outcome="geometry-support-proof-blocked-next-cluster-selected",
        reason="geometry-support reached a documentation-only terminal blocker; frontend-sequence is the next non-ND proof cluster in the RE-169 ordering",
        dependency="RE-177 post-geometry next-cluster selection",
        code_change_readiness="blocked",
        stop_condition="frontend-sequence proof-first audit emitted",
    )
    tickets = build_tickets(handoff)
    ready_count = sum(row.code_change_ready == "yes" for row in equivalence_rows)
    marker_count = sum(row.marker_ready == "yes" for row in equivalence_rows)
    patch_count = sum(row.source_patch_allowed == "yes" for row in source_patch_rows)
    return GeometrySupportChain(
        domain_id="module-spec_psxpc_n",
        cluster="geometry-support",
        upstream_ticket="RE-170",
        pivot="GetBoundsAccurate",
        status="geometry-support-chain-closed-with-proof-blocker",
        final_decision="documentation-only-terminal-blocker",
        next_ticket=handoff.next_ticket,
        code_change_ready_count=ready_count,
        marker_ready_count=marker_count,
        source_patch_ready_count=patch_count,
        audit_rows=audit_rows,
        callsite_rows=callsite_rows,
        taxonomy_rows=taxonomy_rows,
        contract_rows=contract_rows,
        equivalence_rows=equivalence_rows,
        source_patch_rows=source_patch_rows,
        next_selection_rows=next_selection_rows,
        handoff=handoff,
        tickets=tickets,
    )


def write_story(ticket: Ticket, chain: GeometrySupportChain, out_dir: Path) -> Path:
    path = out_dir / STORY_DIR / f"{ticket.story_id}-{ticket.title}.md"
    lines = [
        f"# {ticket.story_id} — {ticket.title}",
        "",
        "## Goal",
        f"Advance `{chain.cluster}` in `{chain.domain_id}` using metadata-only proof artifacts.",
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
        "- `python3 -m pytest tests/reverse/test_re171_re177_geometry_support_chain.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over generated RE-171..RE-177 artifacts",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_all_artifacts(chain: GeometrySupportChain, out_dir: Path) -> dict[str, Path]:
    written: dict[str, Path] = {}
    write_dict_csv(out_dir / AUDIT_CSV, list(AuditRow.__dataclass_fields__), [row.__dict__ for row in chain.audit_rows])
    written["audit_csv"] = out_dir / AUDIT_CSV
    write_dict_csv(out_dir / CALLSITE_CSV, list(CallsiteRow.__dataclass_fields__), [row.__dict__ for row in chain.callsite_rows])
    written["callsite_csv"] = out_dir / CALLSITE_CSV
    write_dict_csv(out_dir / TAXONOMY_CSV, list(TaxonomyRow.__dataclass_fields__), [row.__dict__ for row in chain.taxonomy_rows])
    written["taxonomy_csv"] = out_dir / TAXONOMY_CSV
    write_dict_csv(out_dir / CONTRACT_CSV, list(ContractRow.__dataclass_fields__), [row.__dict__ for row in chain.contract_rows])
    written["contract_csv"] = out_dir / CONTRACT_CSV
    write_dict_csv(out_dir / EQUIVALENCE_CSV, list(EquivalenceRow.__dataclass_fields__), [row.__dict__ for row in chain.equivalence_rows])
    written["equivalence_csv"] = out_dir / EQUIVALENCE_CSV
    write_dict_csv(out_dir / SOURCE_PATCH_CSV, list(SourcePatchRow.__dataclass_fields__), [row.__dict__ for row in chain.source_patch_rows])
    written["source_patch_csv"] = out_dir / SOURCE_PATCH_CSV
    write_dict_csv(out_dir / NEXT_SELECTION_CSV, list(NextSelectionRow.__dataclass_fields__), [row.__dict__ for row in chain.next_selection_rows])
    written["next_selection_csv"] = out_dir / NEXT_SELECTION_CSV
    write_dict_csv(out_dir / HANDOFF_CSV, list(Handoff.__dataclass_fields__), [chain.handoff.__dict__])
    written["handoff_csv"] = out_dir / HANDOFF_CSV
    write_dict_csv(out_dir / CHAIN_CSV, list(Ticket.__dataclass_fields__), [{**ticket.__dict__, "progress": ";".join(ticket.progress), "generated_artifacts": ";".join(ticket.generated_artifacts), "findings": ";".join(ticket.findings)} for ticket in chain.tickets])
    written["chain_csv"] = out_dir / CHAIN_CSV

    md_path = out_dir / MD_OUTPUT
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join([
        "# RE-171..RE-177 geometry-support chain",
        "",
        f"status: `{chain.status}`",
        f"final decision: `{chain.final_decision}`",
        f"source-patch-ready rows: `{chain.source_patch_ready_count}`",
        f"marker-ready rows: `{chain.marker_ready_count}`",
        f"next ticket: `{chain.handoff.next_ticket}`",
        f"next cluster: `{chain.handoff.selected_cluster}` / `{chain.handoff.selected_pivot}`",
        "",
        "## Scope",
        *[f"- `{row.function}` — {row.proof_status}; blocker `{row.blocker}`" for row in chain.audit_rows],
        "",
        "## Gate result",
        "No source or marker patch is authorized because the non-raw binary equivalence proof is still missing.",
        "",
    ]), encoding="utf-8")
    written["md"] = md_path

    for ticket in chain.tickets:
        written[ticket.story_id] = write_story(ticket, chain, out_dir)
    return written


def ensure_metadata_only(paths: list[Path]) -> None:
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_FRAGMENTS:
            if fragment in text:
                raise ValueError(f"forbidden fragment {fragment!r} in {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    chain = build_geometry_support_chain(args.repo)
    written = write_all_artifacts(chain, args.repo)
    ensure_metadata_only(list(written.values()))
    print(f"generated {len(written)} RE-171..RE-177 geometry-support artifacts; next={chain.handoff.next_ticket} {chain.handoff.next_topic}")


if __name__ == "__main__":
    main()
