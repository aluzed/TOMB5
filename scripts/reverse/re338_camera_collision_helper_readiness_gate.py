#!/usr/bin/env python3
"""Gate RE-337 camera-collision helper candidate before reopening a proof domain."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE337_HANDOFF = "docs/reverse/generated/re337-collision-switch-door-post-door-save-next-subcluster-selection-handoff.csv"
RE337_CANDIDATES = "docs/reverse/generated/re337-collision-switch-door-post-door-save-next-subcluster-selection-candidates.csv"
RE311_CANDIDATES = "docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-candidates.csv"
CANDIDATES_CSV = "docs/reverse/generated/re338-camera-collision-helper-readiness-gate-candidates.csv"
GATES_CSV = "docs/reverse/generated/re338-camera-collision-helper-readiness-gate-gates.csv"
SUMMARY_CSV = "docs/reverse/generated/re338-camera-collision-helper-readiness-gate-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re338-camera-collision-helper-readiness-gate-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re338-camera-collision-helper-readiness-gate.md"
STORY = "docs/stories/RE-338-camera-collision-helper-readiness-gate.md"

SELECTED_SUBCLUSTER = "camera-collision-helper"
FOLLOWUP_CANDIDATE_ID = "95c41ac597d6"
CAMERA_COLLISION_TOKENS = ("Camera", "Collision")

FORBIDDEN_OUTPUT_FRAGMENTS = (
    "0x",
    "fun_",
    "sub_",
    "word_le_hex",
    "payload_offset",
    "dump row",
    "opcode",
    "machine word",
    "call_address",
    "branch target",
    "call target",
    "hex-address-fragment",
    "raw_evidence",
    "ghidra_entry",
    "ghidra_name",
    "source_line_text",
    "unimplemented();",
)


@dataclass(frozen=True)
class ReadinessCandidateRow:
    rank: int
    source_rank: int
    candidate_id: str
    selected_narrow_subcluster: str
    bridge_class: str
    body_size_bucket: str
    mapped_caller_count: int
    mapped_callee_count: int
    mapped_source_file_count: int
    mapped_source_module_count: int
    caller_camera_collision_context_count: int
    callee_camera_collision_context_count: int
    proof_signal_class: str
    readiness_gate: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    next_probe: str
    stop_condition: str


@dataclass(frozen=True)
class ReadinessGateRow:
    rank: int
    gate_class: str
    candidate_count: int
    representative_candidates: str
    gate_decision: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    next_ticket: str
    next_topic: str
    stop_condition: str


@dataclass(frozen=True)
class ReadinessSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    selected_narrow_subcluster: str
    input_candidate_count: int
    candidate_gate_count: int
    ready_to_reopen_domain_count: int
    source_patch_authorized_count: int
    selected_domain: str
    selected_pivot: str
    selected_followup_candidate_id: str
    next_ticket: str
    next_topic: str
    metadata_work_readiness: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class ReadinessBundle:
    candidate_rows: list[ReadinessCandidateRow]
    gate_rows: list[ReadinessGateRow]
    summary: ReadinessSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def one_row(repo: Path, rel_path: str) -> dict[str, str]:
    rows = read_csv(repo / rel_path)
    if len(rows) != 1:
        raise ValueError(f"{rel_path} must contain exactly one row")
    return rows[0]


def validate_re337_handoff(repo: Path) -> None:
    row = one_row(repo, RE337_HANDOFF)
    expected = {
        "story_id": "RE-337",
        "next_ticket": "RE-338",
        "next_topic": "camera-collision-helper-readiness-gate",
        "selected_narrow_subcluster": SELECTED_SUBCLUSTER,
        "selected_narrow_candidate_count": "1",
        "selected_candidate_ids": FOLLOWUP_CANDIDATE_ID,
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "selected_domain": "none",
        "selected_pivot": "none",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-337 handoff drift: {key}={row.get(key)!r}")


def split_symbols(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def count_camera_collision_context(value: str) -> int:
    symbols = split_symbols(value)
    return sum(1 for symbol in symbols if any(token.lower() in symbol.lower() for token in CAMERA_COLLISION_TOKENS))


def proof_signal_class(row: dict[str, str]) -> str:
    caller_hits = count_camera_collision_context(row.get("representative_callers", ""))
    callee_hits = count_camera_collision_context(row.get("representative_callees", ""))
    if callee_hits and caller_hits:
        return "caller-and-callee-camera-collision-context-only"
    if callee_hits:
        return "callee-camera-collision-context-only"
    if caller_hits:
        return "caller-camera-collision-context-only"
    return "broad-camera-collision-context-only"


def selected_candidate_rows(repo: Path) -> tuple[dict[str, str], dict[str, str]]:
    re337_rows = read_csv(repo / RE337_CANDIDATES)
    if len(re337_rows) != 1:
        raise ValueError("RE-337 candidate handoff must contain exactly one candidate row")
    re337_row = re337_rows[0]
    expected_re337 = {
        "candidate_id": FOLLOWUP_CANDIDATE_ID,
        "narrow_subcluster": SELECTED_SUBCLUSTER,
        "readiness_gate": "blocked-needs-candidate-level-proof",
        "ready_to_reopen_domain": "no",
        "source_patch_authorized": "no",
        "next_probe": "readiness-gate",
    }
    for key, value in expected_re337.items():
        if re337_row.get(key) != value:
            raise ValueError(f"RE-337 candidate drift: {key}={re337_row.get(key)!r}")

    re311_rows = [
        row
        for row in read_csv(repo / RE311_CANDIDATES)
        if row.get("candidate_id") == FOLLOWUP_CANDIDATE_ID
    ]
    if len(re311_rows) != 1:
        raise ValueError("RE-311 camera-collision helper candidate set drift")
    re311_row = re311_rows[0]
    expected_re311 = {
        "narrow_subcluster": SELECTED_SUBCLUSTER,
        "ready_to_reopen_domain": "no",
        "source_patch_authorized": "no",
        "blocker_class": "needs-candidate-level-source-symbolic-proof",
    }
    for key, value in expected_re311.items():
        if re311_row.get(key) != value:
            raise ValueError(f"RE-311 candidate drift: {key}={re311_row.get(key)!r}")
    return re337_row, re311_row


def build_camera_collision_helper_readiness_gate(repo: Path) -> ReadinessBundle:
    repo = Path(repo)
    validate_re337_handoff(repo)
    re337_row, source_row = selected_candidate_rows(repo)

    candidate_rows = [
        ReadinessCandidateRow(
            rank=1,
            source_rank=int(source_row["source_rank"]),
            candidate_id=FOLLOWUP_CANDIDATE_ID,
            selected_narrow_subcluster=SELECTED_SUBCLUSTER,
            bridge_class=source_row["bridge_class"],
            body_size_bucket=source_row["body_size_bucket"],
            mapped_caller_count=int(source_row["mapped_caller_count"]),
            mapped_callee_count=int(source_row["mapped_callee_count"]),
            mapped_source_file_count=int(source_row["mapped_source_file_count"]),
            mapped_source_module_count=int(source_row["mapped_source_module_count"]),
            caller_camera_collision_context_count=count_camera_collision_context(source_row.get("representative_callers", "")),
            callee_camera_collision_context_count=count_camera_collision_context(source_row.get("representative_callees", "")),
            proof_signal_class=proof_signal_class(source_row),
            readiness_gate="blocked-needs-candidate-level-proof",
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            next_probe="candidate-proof-export",
            stop_condition="candidate-level source-symbolic proof is required before proof-domain selection",
        )
    ]
    if int(re337_row["mapped_caller_count"]) != candidate_rows[0].mapped_caller_count:
        raise ValueError("RE-337/RE-311 mapped caller count drift")
    if int(re337_row["mapped_callee_count"]) != candidate_rows[0].mapped_callee_count:
        raise ValueError("RE-337/RE-311 mapped callee count drift")

    gate_rows = [
        ReadinessGateRow(
            rank=1,
            gate_class="candidate-level-source-symbolic-proof-missing",
            candidate_count=len(candidate_rows),
            representative_candidates=FOLLOWUP_CANDIDATE_ID,
            gate_decision="request-still-narrower-export",
            ready_to_reopen_domain="no",
            source_patch_authorized="no",
            next_ticket="RE-339",
            next_topic="camera-collision-helper-candidate-proof-export",
            stop_condition="candidate-level source-symbolic proof is required before proof-domain selection",
        )
    ]
    summary = ReadinessSummary(
        story_id="RE-338",
        topic="camera-collision-helper-readiness-gate",
        upstream_handoff="RE-337",
        selected_narrow_subcluster=SELECTED_SUBCLUSTER,
        input_candidate_count=1,
        candidate_gate_count=len(candidate_rows),
        ready_to_reopen_domain_count=0,
        source_patch_authorized_count=0,
        selected_domain="none",
        selected_pivot="none",
        selected_followup_candidate_id=FOLLOWUP_CANDIDATE_ID,
        next_ticket="RE-339",
        next_topic="camera-collision-helper-candidate-proof-export",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="candidate-level source-symbolic proof missing; request a still narrower camera-collision candidate proof export",
    )
    return ReadinessBundle(candidate_rows=candidate_rows, gate_rows=gate_rows, summary=summary)


def write_csv(path: Path, rows: list[object], row_type: type[object]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(row_type)], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
    return path


def render_markdown(bundle: ReadinessBundle) -> str:
    lines = [
        "# RE-338 camera-collision helper readiness gate",
        "",
        "## Summary",
        "",
        f"Gated `{bundle.summary.input_candidate_count}` camera-collision helper candidate from RE-337.",
        "No proof-domain is reopened by this gate; every row still needs candidate-level source-symbolic proof.",
        "",
        "## Candidate gates",
        "",
    ]
    for row in bundle.candidate_rows:
        lines.append(
            f"- rank `{row.rank}` candidate `{row.candidate_id}`: gate `{row.readiness_gate}`, proof signal `{row.proof_signal_class}`, next `{row.next_probe}`"
        )
    lines.extend(
        [
            "",
            "## Readiness decision",
            "",
            "The selected subcluster has source-symbolic camera/collision context, but not candidate-level proof sufficient to select a proof domain, pivot, source patch, or marker update.",
            f"The next safe action is `{bundle.summary.next_ticket}` / `{bundle.summary.next_topic}` for candidate `{bundle.summary.selected_followup_candidate_id}`.",
            "",
        ]
    )
    return "\n".join(lines)


def render_story(bundle: ReadinessBundle) -> str:
    summary = bundle.summary
    return "\n".join(
        [
            "# RE-338 camera-collision helper readiness gate",
            "",
            "## Goal",
            "",
            "Gate the RE-337 selected camera-collision helper subcluster before reopening any proof domain or authorizing source/marker changes.",
            "",
            "## Inputs",
            "",
            f"- Upstream handoff: `{RE337_HANDOFF}`",
            f"- RE-337 candidates: `{RE337_CANDIDATES}`",
            f"- RE-311 candidates: `{RE311_CANDIDATES}`",
            "",
            "## Progress tracker",
            "",
            "- [x] RE-337 camera-collision helper handoff validated.",
            "- [x] Selected candidate set checked fail-closed against RE-311 metadata.",
            "- [x] Candidate-level readiness row emitted without raw identity columns.",
            "- [x] Domain/pivot/source-patch readiness kept blocked.",
            "- [x] Still-narrower follow-up export selected.",
            "",
            "## Generated artifacts",
            "",
            f"- `{CANDIDATES_CSV}`",
            f"- `{GATES_CSV}`",
            f"- `{SUMMARY_CSV}`",
            f"- `{HANDOFF_CSV}`",
            f"- `{MD_OUTPUT}`",
            "",
            "## Findings",
            "",
            f"- Selected narrow subcluster: `{summary.selected_narrow_subcluster}`",
            f"- Input candidates: `{summary.input_candidate_count}`",
            f"- Candidate gate rows: `{summary.candidate_gate_count}`",
            f"- Ready to reopen domain selection: `{summary.ready_to_reopen_domain_count}`",
            f"- Source patch authorized rows: `{summary.source_patch_authorized_count}`",
            f"- Selected domain: `{summary.selected_domain}`",
            f"- Selected pivot: `{summary.selected_pivot}`",
            f"- Follow-up candidate id: `{summary.selected_followup_candidate_id}`",
            "",
            "## Readiness decision",
            "",
            "The camera-collision helper remains blocked because the current metadata only proves source-symbolic context, not candidate-level proof. Domain and pivot remain `none`, and code readiness remains blocked.",
            "",
            "## Follow-up ticket breakdown",
            "",
            "- `RE-339` / `camera-collision-helper-candidate-proof-export`: produce a still narrower metadata-only proof export for candidate `95c41ac597d6`.",
            "  - Inputs: RE-338 candidate readiness rows plus local source-symbolic maps.",
            "  - Deliverables: candidate-scoped source-symbolic proof metadata, proof/blocker rows, and a handoff that either names a proof-first domain/pivot or stays blocked.",
            "  - Stop condition: if candidate-level proof is still absent, keep source/code readiness blocked and defer to the next camera-collision candidate action.",
            "",
            "## Validation commands",
            "",
            "- `python -m pytest tests/reverse/test_re338_camera_collision_helper_readiness_gate.py -q`",
            "- `python scripts/reverse/re338_camera_collision_helper_readiness_gate.py --repo .`",
            "- `python -m pytest tests/reverse -q`",
            "",
        ]
    )


def assert_metadata_only(paths: dict[str, Path]) -> None:
    for path in paths.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
            if fragment in text:
                raise ValueError(f"Forbidden output fragment {fragment!r} in {path}")


def write_all_artifacts(bundle: ReadinessBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "candidates_csv": repo / CANDIDATES_CSV,
        "gates_csv": repo / GATES_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_csv(paths["candidates_csv"], bundle.candidate_rows, ReadinessCandidateRow)
    write_csv(paths["gates_csv"], bundle.gate_rows, ReadinessGateRow)
    write_csv(paths["summary_csv"], [bundle.summary], ReadinessSummary)
    write_csv(paths["handoff_csv"], [bundle.summary], ReadinessSummary)
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text(render_markdown(bundle), encoding="utf-8")
    paths["story"].parent.mkdir(parents=True, exist_ok=True)
    paths["story"].write_text(render_story(bundle), encoding="utf-8")
    assert_metadata_only(paths)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository root")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    bundle = build_camera_collision_helper_readiness_gate(repo)
    written = write_all_artifacts(bundle, repo)
    for key, path in written.items():
        print(f"{key}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
