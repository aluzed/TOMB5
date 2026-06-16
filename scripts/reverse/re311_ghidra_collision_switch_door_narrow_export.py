#!/usr/bin/env python3
"""Generate RE-311 narrowed metadata export for the collision/switch/door Ghidra bridge cluster."""

from __future__ import annotations

import argparse
import csv
import hashlib
from collections import defaultdict
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE310_HANDOFF = "docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-handoff.csv"
RE310_CANDIDATES = "docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-candidates.csv"
GHIDRA_FUNCTIONS = "docs/reverse/generated/ghidra-functions.csv"
REPO_FUNCTION_MAP = "docs/reverse/generated/repo-function-map.csv"

SUBCLUSTERS_CSV = "docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-subclusters.csv"
CANDIDATES_CSV = "docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-candidates.csv"
SUMMARY_CSV = "docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re311-ghidra-collision-switch-door-narrow-export.md"
STORY = "docs/stories/RE-311-ghidra-collision-switch-door-narrow-export.md"

FORBIDDEN_OUTPUT_FRAGMENTS = (
    "0x",
    "fun_",
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
)

PARSER_ARTIFACT_NAMES = {"if", "for", "while", "switch"}
SUBCLUSTER_PRIORITY = {
    "collision-geometry-helper": 0,
    "switch-door-control-helper": 1,
    "weapon-switch-effect-helper": 2,
    "door-save-runtime-helper": 3,
    "camera-collision-helper": 4,
}


@dataclass(frozen=True)
class NarrowCandidateRow:
    rank: int
    source_rank: int
    candidate_id: str
    narrow_subcluster: str
    hidden_local_identity_resolved: str
    bridge_class: str
    body_size_bucket: str
    mapped_caller_count: int
    mapped_callee_count: int
    mapped_source_file_count: int
    mapped_source_module_count: int
    caller_family_count: int
    callee_family_count: int
    representative_callers: str
    representative_callees: str
    blocker_class: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    next_topic: str
    stop_condition: str


@dataclass(frozen=True)
class NarrowSubclusterRow:
    rank: int
    narrow_subcluster: str
    candidate_count: int
    hidden_local_identity_resolved_count: int
    mapped_caller_total: int
    mapped_callee_total: int
    source_file_count: int
    source_module_count: int
    representative_callers: str
    representative_callees: str
    gate_decision: str
    ready_to_reopen_domain: str
    source_patch_authorized: str
    next_ticket: str
    next_topic: str
    stop_condition: str


@dataclass(frozen=True)
class NarrowSummary:
    story_id: str
    topic: str
    upstream_handoff: str
    focus_cluster: str
    focus_candidate_count: int
    hidden_local_identity_resolved_count: int
    narrow_subcluster_count: int
    selected_narrow_subcluster: str
    selected_narrow_candidate_count: int
    ready_to_reopen_domain_count: int
    source_patch_authorized_count: int
    selected_domain: str
    selected_pivot: str
    next_ticket: str
    next_topic: str
    metadata_work_readiness: str
    code_change_readiness: str
    stop_condition: str


@dataclass(frozen=True)
class NarrowBundle:
    subcluster_rows: list[NarrowSubclusterRow]
    candidate_rows: list[NarrowCandidateRow]
    summary: NarrowSummary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def one_row(repo: Path, rel_path: str) -> dict[str, str]:
    rows = read_csv(repo / rel_path)
    if len(rows) != 1:
        raise ValueError(f"{rel_path} must contain exactly one row")
    return rows[0]


def validate_re310_handoff(repo: Path) -> None:
    row = one_row(repo, RE310_HANDOFF)
    expected = {
        "story_id": "RE-310",
        "next_ticket": "RE-311",
        "next_topic": "ghidra-collision-switch-door-cluster-narrow-export",
        "selected_followup_cluster": "collision-switch-door-cluster",
        "metadata_work_readiness": "ready",
        "code_change_readiness": "blocked",
        "ready_to_reopen_domain_count": "0",
        "source_patch_authorized_count": "0",
        "selected_domain": "none",
        "selected_pivot": "none",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"RE-310 handoff drift: {key}={row.get(key)!r}")


def candidate_hash(entry: str, name: str) -> str:
    return hashlib.sha1(f"{entry}|{name}".encode("utf-8")).hexdigest()[:12]


def split_symbols(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def safe_repo_symbol(row: dict[str, str]) -> str | None:
    name = row.get("repo_function", "")
    if not name or name.lower() in PARSER_ARTIFACT_NAMES:
        return None
    file_name = row.get("file", "")
    module = file_name.split("/", 1)[0] if "/" in file_name else file_name
    return f"{module}:{name}" if module else name


def unique_sorted(values: list[str]) -> list[str]:
    return sorted(dict.fromkeys(values))


def family_from_symbol(symbol: str) -> str:
    lowered = symbol.lower()
    if "collision" in lowered or "testcollision" in lowered:
        return "collision"
    if "door" in lowered:
        return "door"
    if "switch" in lowered:
        return "switch"
    if "floor" in lowered or "height" in lowered:
        return "floor-height"
    if "matrix" in lowered or "mpop" in lowered or "mpush" in lowered:
        return "matrix"
    if "sound" in lowered:
        return "sound"
    if "save" in lowered or "restore" in lowered:
        return "save-restore"
    if "camera" in lowered:
        return "camera"
    if "fire" in lowered or "weapon" in lowered or "explod" in lowered or "smash" in lowered:
        return "weapon-effect"
    if "lara" in lowered:
        return "lara"
    return "other"


def classify_narrow_subcluster(callers: list[str], callees: list[str], source_files: list[str]) -> str:
    del source_files  # File paths are emitted as metadata but are too broad for subcluster decisions.
    caller_text = ";".join(callers).lower()
    callee_text = ";".join(callees).lower()
    joined = f"{caller_text};{callee_text}"
    if "fireweapon" in joined or "explod" in joined or "shatter" in joined or "smas" in joined:
        return "weapon-switch-effect-helper"
    if "save" in joined or "restore" in joined or "openthatdoor" in joined:
        return "door-save-runtime-helper"
    if any(token in caller_text for token in ["calculatecamera", "movecamera", "creaturecollision", "larawatercurrent", "controlrollingball"]):
        return "camera-collision-helper"
    if any(token in callee_text for token in ["getfloor", "getheight", "testcollision", "mpopmatrix", "mpushunitmatrix"]):
        return "collision-geometry-helper"
    if "control" in caller_text and ("switch" in caller_text or "door" in caller_text):
        return "switch-door-control-helper"
    return "collision-geometry-helper"


def context_slice(values: list[str], max_items: int = 8) -> str:
    return ";".join(unique_sorted(values)[:max_items])


def build_raw_identity_index(repo: Path) -> dict[str, dict[str, object]]:
    ghidra_rows = read_csv(repo / GHIDRA_FUNCTIONS)
    map_rows = read_csv(repo / REPO_FUNCTION_MAP)
    mapped_by_name: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in map_rows:
        if row.get("mapping_status") == "mapped" and row.get("ghidra_name"):
            mapped_by_name[row["ghidra_name"]].append(row)
    result: dict[str, dict[str, object]] = {}
    for ghidra in ghidra_rows:
        cid = candidate_hash(ghidra["entry"], ghidra["name"])
        caller_symbols = split_symbols(ghidra.get("callers", ""))
        callee_symbols = split_symbols(ghidra.get("called_functions", ""))
        mapped_callers = [row for symbol in caller_symbols for row in mapped_by_name.get(symbol, [])]
        mapped_callees = [row for symbol in callee_symbols for row in mapped_by_name.get(symbol, [])]
        caller_context = [value for row in mapped_callers for value in [safe_repo_symbol(row)] if value]
        callee_context = [value for row in mapped_callees for value in [safe_repo_symbol(row)] if value]
        source_files = unique_sorted([row.get("file", "") for row in mapped_callers + mapped_callees if row.get("file")])
        result[cid] = {
            "caller_context": unique_sorted(caller_context),
            "callee_context": unique_sorted(callee_context),
            "source_files": source_files,
        }
    return result


def build_collision_switch_door_narrow_export(repo: Path) -> NarrowBundle:
    repo = Path(repo)
    validate_re310_handoff(repo)
    re310_rows = read_csv(repo / RE310_CANDIDATES)
    focus_rows = [row for row in re310_rows if row.get("focus_cluster") == "yes" and row.get("source_cluster") == "collision-switch-door-cluster"]
    if len(focus_rows) != 7:
        raise ValueError(f"Expected 7 RE-310 focus rows, got {len(focus_rows)}")
    identity_index = build_raw_identity_index(repo)

    candidate_rows: list[NarrowCandidateRow] = []
    for row in sorted(focus_rows, key=lambda item: int(item["rank"])):
        cid = row["candidate_id"]
        identity = identity_index.get(cid)
        if identity is None:
            raise ValueError(f"Could not resolve local identity for candidate {cid}")
        callers = list(identity["caller_context"])
        callees = list(identity["callee_context"])
        source_files = list(identity["source_files"])
        subcluster = classify_narrow_subcluster(callers, callees, source_files)
        caller_families = unique_sorted([family_from_symbol(value) for value in callers])
        callee_families = unique_sorted([family_from_symbol(value) for value in callees])
        modules = unique_sorted([file_name.split("/", 1)[0] for file_name in source_files if file_name])
        decision = "collision-geometry-helper-readiness-gate" if subcluster == "collision-geometry-helper" else "defer-after-collision-geometry-gate"
        candidate_rows.append(
            NarrowCandidateRow(
                rank=len(candidate_rows) + 1,
                source_rank=int(row["rank"]),
                candidate_id=cid,
                narrow_subcluster=subcluster,
                hidden_local_identity_resolved="yes",
                bridge_class=row["bridge_class"],
                body_size_bucket=row["body_size_bucket"],
                mapped_caller_count=int(row["mapped_caller_count"]),
                mapped_callee_count=int(row["mapped_callee_count"]),
                mapped_source_file_count=len(source_files),
                mapped_source_module_count=len(modules),
                caller_family_count=len(caller_families),
                callee_family_count=len(callee_families),
                representative_callers=context_slice(callers),
                representative_callees=context_slice(callees),
                blocker_class="needs-candidate-level-source-symbolic-proof",
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                next_topic=decision,
                stop_condition="requires candidate-level source-symbolic proof before domain selection",
            )
        )

    grouped: dict[str, list[NarrowCandidateRow]] = defaultdict(list)
    for row in candidate_rows:
        grouped[row.narrow_subcluster].append(row)

    def subcluster_sort(item: tuple[str, list[NarrowCandidateRow]]) -> tuple[int, int, str]:
        name, rows = item
        return (SUBCLUSTER_PRIORITY.get(name, 99), -len(rows), name)

    subcluster_rows: list[NarrowSubclusterRow] = []
    for rank, (name, rows) in enumerate(sorted(grouped.items(), key=subcluster_sort), start=1):
        caller_values = [value for row in rows for value in row.representative_callers.split(";") if value]
        callee_values = [value for row in rows for value in row.representative_callees.split(";") if value]
        source_files = sum((int(row.mapped_source_file_count) for row in rows), 0)
        modules = sum((int(row.mapped_source_module_count) for row in rows), 0)
        focus = name == "collision-geometry-helper"
        subcluster_rows.append(
            NarrowSubclusterRow(
                rank=rank,
                narrow_subcluster=name,
                candidate_count=len(rows),
                hidden_local_identity_resolved_count=sum(1 for row in rows if row.hidden_local_identity_resolved == "yes"),
                mapped_caller_total=sum(row.mapped_caller_count for row in rows),
                mapped_callee_total=sum(row.mapped_callee_count for row in rows),
                source_file_count=source_files,
                source_module_count=modules,
                representative_callers=context_slice(caller_values),
                representative_callees=context_slice(callee_values),
                gate_decision="gate-before-proof-domain" if focus else "defer-after-selected-subcluster",
                ready_to_reopen_domain="no",
                source_patch_authorized="no",
                next_ticket="RE-312" if focus else "TBD",
                next_topic="collision-geometry-helper-readiness-gate" if focus else "defer-after-re312",
                stop_condition="candidate-level source-symbolic proof required before proof-domain selection" if focus else "wait for selected subcluster readiness gate",
            )
        )

    selected_count = next(row.candidate_count for row in subcluster_rows if row.narrow_subcluster == "collision-geometry-helper")
    summary = NarrowSummary(
        story_id="RE-311",
        topic="ghidra-collision-switch-door-cluster-narrow-export",
        upstream_handoff="RE-310",
        focus_cluster="collision-switch-door-cluster",
        focus_candidate_count=len(focus_rows),
        hidden_local_identity_resolved_count=len(candidate_rows),
        narrow_subcluster_count=len(subcluster_rows),
        selected_narrow_subcluster="collision-geometry-helper",
        selected_narrow_candidate_count=selected_count,
        ready_to_reopen_domain_count=0,
        source_patch_authorized_count=0,
        selected_domain="none",
        selected_pivot="none",
        next_ticket="RE-312",
        next_topic="collision-geometry-helper-readiness-gate",
        metadata_work_readiness="ready",
        code_change_readiness="blocked",
        stop_condition="gate the collision-geometry helper subcluster before selecting a proof domain or patching source",
    )
    return NarrowBundle(subcluster_rows=subcluster_rows, candidate_rows=candidate_rows, summary=summary)


def write_csv(path: Path, rows: list[object], row_type: type) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(row_type)], lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def render_markdown(bundle: NarrowBundle) -> str:
    lines = [
        "# RE-311 Ghidra collision/switch/door narrow export",
        "",
        "## Summary",
        "",
        f"Narrowed `{bundle.summary.focus_candidate_count}` focus candidates into `{bundle.summary.narrow_subcluster_count}` source-symbolic subclusters.",
        "The raw Ghidra identity remains local-only; versioned rows use hashed candidate IDs and repo-symbol context.",
        "",
        "## Subcluster decisions",
        "",
    ]
    for row in bundle.subcluster_rows:
        lines.append(
            f"- rank `{row.rank}` `{row.narrow_subcluster}`: candidates `{row.candidate_count}`, decision `{row.gate_decision}`, next `{row.next_topic}`"
        )
    lines.extend(
        [
            "",
            "## Readiness decision",
            "",
            "The narrow export is metadata-ready, but proof-domain selection and source/marker changes remain blocked until the selected subcluster is gated.",
            "",
        ]
    )
    return "\n".join(lines)


def render_story(bundle: NarrowBundle) -> str:
    summary = bundle.summary
    return "\n".join(
        [
            "# RE-311 Ghidra collision/switch/door narrow export",
            "",
            "## Goal",
            "",
            "Produce a narrower metadata-only source-symbolic export for the RE-310 collision/switch/door focus cluster without committing raw Ghidra identity.",
            "",
            "## Inputs",
            "",
            f"- Upstream handoff: `{RE310_HANDOFF}`",
            f"- RE-310 candidates: `{RE310_CANDIDATES}`",
            f"- Local Ghidra export: `{GHIDRA_FUNCTIONS}`",
            f"- Local repo function map: `{REPO_FUNCTION_MAP}`",
            "",
            "## Progress tracker",
            "",
            "- [x] RE-310 focus cluster validated.",
            "- [x] Local raw Ghidra identity resolved only inside the generator.",
            "- [x] Narrow source-symbolic subclusters emitted without raw identity columns.",
            "- [x] Collision-geometry helper subcluster selected for a readiness gate.",
            "- [x] Source/domain readiness kept blocked.",
            "",
            "## Generated artifacts",
            "",
            f"- `{SUBCLUSTERS_CSV}`",
            f"- `{CANDIDATES_CSV}`",
            f"- `{SUMMARY_CSV}`",
            f"- `{HANDOFF_CSV}`",
            f"- `{MD_OUTPUT}`",
            "",
            "## Findings",
            "",
            f"- Focus cluster: `{summary.focus_cluster}`",
            f"- Focus candidates: `{summary.focus_candidate_count}`",
            f"- Local identities resolved inside generator: `{summary.hidden_local_identity_resolved_count}`",
            f"- Narrow subclusters: `{summary.narrow_subcluster_count}`",
            f"- Selected narrow subcluster: `{summary.selected_narrow_subcluster}`",
            f"- Selected candidate count: `{summary.selected_narrow_candidate_count}`",
            f"- Ready to reopen domain selection: `{summary.ready_to_reopen_domain_count}`",
            f"- Source patch authorized rows: `{summary.source_patch_authorized_count}`",
            "",
            "## Readiness decision",
            "",
            "This export narrows the candidate space but still does not select a proof domain. Domain/pivot remain `none`, and code readiness remains blocked.",
            "",
            "## Follow-up ticket breakdown",
            "",
            "- `RE-312` / `collision-geometry-helper-readiness-gate`: gate the selected collision-geometry helper subcluster and decide whether it can produce a proof-first pivot.",
            "  - Inputs: RE-311 subcluster and candidate CSVs plus local Ghidra/repo maps.",
            "  - Deliverables: candidate-level readiness rows and a handoff that either names a proof-first pivot or keeps domain/pivot `none`.",
            "  - Stop condition: if every row still lacks candidate-level source-symbolic proof, keep source/code readiness blocked and request a still narrower export.",
            "",
            "## Validation commands",
            "",
            "- `python -m pytest tests/reverse/test_re311_ghidra_collision_switch_door_narrow_export.py -q`",
            "- `python scripts/reverse/re311_ghidra_collision_switch_door_narrow_export.py --repo .`",
            "- `python -m pytest tests/reverse -q`",
            "",
        ]
    )


def write_all_artifacts(bundle: NarrowBundle, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "subclusters_csv": repo / SUBCLUSTERS_CSV,
        "candidates_csv": repo / CANDIDATES_CSV,
        "summary_csv": repo / SUMMARY_CSV,
        "handoff_csv": repo / HANDOFF_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY,
    }
    write_csv(paths["subclusters_csv"], bundle.subcluster_rows, NarrowSubclusterRow)
    write_csv(paths["candidates_csv"], bundle.candidate_rows, NarrowCandidateRow)
    write_csv(paths["summary_csv"], [bundle.summary], NarrowSummary)
    write_csv(paths["handoff_csv"], [bundle.summary], NarrowSummary)
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text(render_markdown(bundle), encoding="utf-8")
    paths["story"].parent.mkdir(parents=True, exist_ok=True)
    paths["story"].write_text(render_story(bundle), encoding="utf-8")
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository root")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    bundle = build_collision_switch_door_narrow_export(repo)
    written = write_all_artifacts(bundle, repo)
    for key, path in written.items():
        print(f"{key}: {path.relative_to(repo)}")


if __name__ == "__main__":
    main()
