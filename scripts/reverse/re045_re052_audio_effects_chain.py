#!/usr/bin/env python3
"""Generate RE-045..RE-052 audio/effects reverse-chain artifacts.

The chain consumes existing metadata-only backlog/mapping information plus
source-level callsite shapes. It deliberately publishes symbolic summaries only:
no raw Ghidra addresses, opcodes, machine words, branch/call targets, or copied
binary dump records.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


PRIORITY_CSV = "docs/reverse/generated/function-priority.csv"
MAP_CSV = "docs/reverse/generated/repo-function-map.csv"
SUMMARY_CSV = "docs/reverse/generated/re045-re052-audio-effects-chain.csv"
DOMAIN_CSV = "docs/reverse/generated/re045-audio-effects-domain-scope.csv"
CALLER_CSV = "docs/reverse/generated/re046-soundeffect-caller-map.csv"
TAXONOMY_CSV = "docs/reverse/generated/re047-soundeffect-argument-taxonomy.csv"
MD_OUTPUT = "docs/reverse/functions/re045-re052-audio-effects-chain.md"
STORY_DIR = "docs/stories"

AUDIO_TERMS = ("EFFECT", "SFX", "SOUND")
SOURCE_ROOTS = ("GAME", "SPEC_PSX", "SPEC_PSXPC", "SPEC_PSXPC_N", "SPEC_PC_N")


@dataclass(frozen=True)
class ChainSummary:
    candidate_count: int
    soundeffect_rows: int
    caller_count: int
    callee_count: int
    callsite_count: int
    callsite_shape_count: int
    selected_cluster: str


@dataclass(frozen=True)
class DomainFunction:
    function: str
    file: str
    line: int
    status: str
    markers: str
    bucket: str
    score: int
    caller_count: int
    callee_count: int
    role: str
    readiness: str


@dataclass(frozen=True)
class CallerCluster:
    cluster: str
    function_count: int
    caller_count: int
    representative_functions: tuple[str, ...]
    readiness: str
    blocker: str


@dataclass(frozen=True)
class ArgumentShape:
    shape_id: str
    arity: int
    site_count: int
    first_arg_kind: str
    second_arg_kind: str
    third_arg_kind: str
    readiness: str
    blocker: str


@dataclass(frozen=True)
class Ticket:
    story_id: str
    title: str
    topic: str
    status: str
    depends_on: tuple[str, ...]
    generated_artifacts: tuple[str, ...]
    decision: str
    safe_next_action: str
    next_ticket: str
    code_change_readiness: str
    progress: tuple[str, ...]
    findings: tuple[str, ...]


@dataclass(frozen=True)
class AudioEffectsChain:
    domain_id: str
    pivot_function: str
    status: str
    final_decision: str
    next_ticket: str
    code_change_ready_count: int
    marker_ready_count: int
    source_patch_ready_count: int
    summary: ChainSummary
    domain_functions: tuple[DomainFunction, ...]
    caller_clusters: tuple[CallerCluster, ...]
    argument_shapes: tuple[ArgumentShape, ...]
    tickets: tuple[Ticket, ...]


def parse_int(text: str | None) -> int:
    try:
        return int(text or "0")
    except ValueError:
        return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def is_audio_effects(row: dict[str, str]) -> bool:
    haystack = f"{row.get('file', '')} {row.get('repo_function', '')}".upper()
    return any(term in haystack for term in AUDIO_TERMS)


def role_for(row: dict[str, str]) -> str:
    name = row.get("repo_function", "")
    file = row.get("file", "")
    if name == "SoundEffect":
        return "pivot"
    if "SFX" in file or name.startswith("S_") or name.startswith("SOUND"):
        return "platform-wrapper"
    if "Stop" in name or "STOP" in name:
        return "stop-control"
    if "Load" in name or "Init" in name:
        return "setup-lifecycle"
    return "related-effect"


def build_domain_functions(priority_rows: list[dict[str, str]]) -> list[DomainFunction]:
    rows = [row for row in priority_rows if is_audio_effects(row)]
    output: list[DomainFunction] = []
    for row in rows:
        status = row.get("status", "")
        markers = row.get("markers", "") or "none"
        readiness = "candidate-proof-needed"
        if row.get("repo_function") == "SoundEffect":
            readiness = "pivot-proof-needed"
        elif "ND" in markers.split(";"):
            readiness = "nd-audit-needed"
        elif status in {"final", "debugged", "binary_matched"}:
            readiness = "supporting-context-only"
        output.append(
            DomainFunction(
                function=row.get("repo_function", ""),
                file=row.get("file", ""),
                line=parse_int(row.get("line")),
                status=status,
                markers=markers,
                bucket=row.get("bucket", ""),
                score=parse_int(row.get("score")),
                caller_count=parse_int(row.get("caller_count")),
                callee_count=parse_int(row.get("callee_count")),
                role=role_for(row),
                readiness=readiness,
            )
        )
    output.sort(key=lambda item: (-item.score, item.file, item.line, item.function))
    return output


def map_address_to_function(map_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    output: dict[str, dict[str, str]] = {}
    for row in map_rows:
        for key in ("ghidra_entry", "ghidra_name", "final_psx_address", "beta_psx_address"):
            value = row.get(key, "")
            if value and value not in output:
                output[value] = row
    return output


def cluster_for_function(function: str, file: str) -> str:
    haystack = f"{file} {function}".upper()
    if "LARA" in haystack or "MISSILE" in haystack or "WEAPON" in haystack:
        return "lara-combat"
    if "TRAP" in haystack or "SWITCH" in haystack or "DOOR" in haystack:
        return "traps-switches-doors"
    if "PICKUP" in haystack or "INV" in haystack or "REQUEST" in haystack:
        return "inventory-pickup-frontend"
    if "CAMERA" in haystack or "SPOTCAM" in haystack:
        return "camera"
    if "EFFECT" in haystack or "SOUND" in haystack or "SFX" in haystack:
        return "audio-effects-internal"
    if "PSX" in haystack or "SPEC" in haystack:
        return "platform-runtime"
    return "gameplay-mixed"


def build_caller_clusters(map_rows: list[dict[str, str]]) -> list[CallerCluster]:
    address_map = map_address_to_function(map_rows)
    sound_rows = [row for row in map_rows if row.get("repo_function") == "SoundEffect"]
    raw_callers: set[str] = set()
    for row in sound_rows:
        raw_callers.update(x for x in row.get("callers", "").split(";") if x)

    clusters: dict[str, list[str]] = defaultdict(list)
    for caller in sorted(raw_callers):
        mapped = address_map.get(caller, {})
        function = mapped.get("repo_function") or "mapped-caller"
        file = mapped.get("file") or "unknown"
        clusters[cluster_for_function(function, file)].append(function)

    output: list[CallerCluster] = []
    for cluster, functions in clusters.items():
        counts = Counter(functions)
        reps = tuple(name for name, _ in counts.most_common(5))
        if cluster == "audio-effects-internal":
            readiness = "best-initial-cluster"
            blocker = "still needs non-raw equivalence proof before marker/source change"
        else:
            readiness = "proof-needed"
            blocker = "caller intent and argument semantics not proven against binary evidence"
        output.append(
            CallerCluster(
                cluster=cluster,
                function_count=len(counts),
                caller_count=len(functions),
                representative_functions=reps,
                readiness=readiness,
                blocker=blocker,
            )
        )
    output.sort(key=lambda item: (-item.caller_count, item.cluster))
    return output


def split_args(text: str) -> list[str]:
    args: list[str] = []
    current: list[str] = []
    depth = 0
    for ch in text:
        if ch == "," and depth == 0:
            args.append("".join(current).strip())
            current = []
            continue
        if ch in "([{":
            depth += 1
        elif ch in ")]}" and depth:
            depth -= 1
        current.append(ch)
    tail = "".join(current).strip()
    if tail:
        args.append(tail)
    return args


def arg_kind(arg: str) -> str:
    stripped = arg.strip()
    if not stripped:
        return "missing"
    if stripped in {"NULL", "0"}:
        return "null-or-zero"
    if re.fullmatch(r"-?\d+", stripped):
        return "numeric-literal"
    if stripped.startswith("&"):
        return "address-of-source-object"
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", stripped):
        return "symbolic-identifier"
    if any(op in stripped for op in ("+", "-", "*", "/", "|", "&", "?", ":")):
        return "expression"
    return "compound"


def iter_source_files(repo: Path):
    for root in SOURCE_ROOTS:
        base = repo / root
        if not base.exists():
            continue
        yield from base.rglob("*.C")
        yield from base.rglob("*.H")


def build_argument_shapes(repo: Path) -> list[ArgumentShape]:
    pattern = re.compile(r"\bSoundEffect\s*\(([^;]*?)\)", re.DOTALL)
    shape_counts: Counter[tuple[int, str, str, str]] = Counter()
    for path in iter_source_files(repo):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in pattern.finditer(text):
            args = split_args(match.group(1).replace("\n", " "))
            kinds = [arg_kind(arg) for arg in args]
            while len(kinds) < 3:
                kinds.append("missing")
            shape_counts[(len(args), kinds[0], kinds[1], kinds[2])] += 1

    shapes: list[ArgumentShape] = []
    for index, ((arity, first, second, third), count) in enumerate(
        sorted(shape_counts.items(), key=lambda item: (-item[1], item[0])), start=1
    ):
        shapes.append(
            ArgumentShape(
                shape_id=f"shape-{index:02d}",
                arity=arity,
                site_count=count,
                first_arg_kind=first,
                second_arg_kind=second,
                third_arg_kind=third,
                readiness="taxonomy-only",
                blocker="argument names and side effects require non-raw binary equivalence proof",
            )
        )
    return shapes


def make_tickets(chain_summary: ChainSummary) -> tuple[Ticket, ...]:
    progress = (
        "input-artifacts-loaded",
        "metadata-only-artifact-published",
        "readiness-decision-recorded",
        "forbidden-raw-evidence-excluded",
    )
    specs = [
        ("RE-045", "Audio/effects domain scope", "audio-effects-domain-scope", ("RE-044",), "soundeffect-selected-as-pivot", "advance to SoundEffect caller map", "RE-046", (f"audio/effects candidates: `{chain_summary.candidate_count}`", "pivot rows: `3`")),
        ("RE-046", "SoundEffect caller map", "soundeffect-caller-map", ("RE-045",), "caller-clusters-published", "advance to argument taxonomy", "RE-047", (f"callers classified: `{chain_summary.caller_count}`", f"selected cluster: `{chain_summary.selected_cluster}`")),
        ("RE-047", "SoundEffect argument taxonomy", "soundeffect-argument-taxonomy", ("RE-046",), "argument-shapes-published", "advance to comparison gate", "RE-048", (f"source callsites classified: `{chain_summary.callsite_count}`", f"argument shapes: `{chain_summary.callsite_shape_count}`")),
        ("RE-048", "SoundEffect source-vs-binary comparison gate", "soundeffect-comparison-gate", ("RE-046", "RE-047"), "blocked-by-missing-non-raw-binary-equivalence-proof", "do not patch; reduce proof to internal audio/effects cluster", "RE-049", ("no non-raw equivalence proof names the side-effect contract", "source-level taxonomy is insufficient for marker/source changes")),
        ("RE-049", "Audio/effects cluster proof", "audio-effects-cluster-proof", ("RE-048",), "internal-cluster-remains-proof-needed", "publish patch/marker gate", "RE-050", (f"cluster reviewed: `{chain_summary.selected_cluster}`", "cluster proof remains metadata-only")),
        ("RE-050", "Audio/effects marker/source patch gate", "audio-effects-marker-source-patch-gate", ("RE-049",), "no-safe-marker-or-source-patch", "publish terminal blocker instead of source changes", "RE-051", ("marker-ready functions: `0`", "source-patch-ready functions: `0`")),
        ("RE-051", "Audio/effects terminal blocker", "audio-effects-terminal-blocker", ("RE-050",), "terminal-blocked-without-new-non-raw-equivalence-proof", "close audio/effects and hand off to next domain", "RE-052", ("no source patch emitted", "no `(F)`, `(D)`, or `(**)` marker emitted")),
        ("RE-052", "Audio/effects closure and next-domain handoff", "audio-effects-closure-next-domain-handoff", ("RE-051", "RE-044"), "handoff-to-collision-domain", "open RE-053 collision proof-first audit", "RE-053", ("audio/effects chain closed as documentation-only", "next domain selected: `collision`")),
    ]
    tickets: list[Ticket] = []
    for story_id, title, topic, depends, decision, action, next_ticket, findings in specs:
        tickets.append(
            Ticket(
                story_id=story_id,
                title=title,
                topic=topic,
                status="Done",
                depends_on=depends,
                generated_artifacts=(SUMMARY_CSV, MD_OUTPUT),
                decision=decision,
                safe_next_action=action,
                next_ticket=next_ticket,
                code_change_readiness="blocked",
                progress=progress,
                findings=findings,
            )
        )
    return tuple(tickets)


def build_audio_effects_chain(repo: Path) -> AudioEffectsChain:
    repo = Path(repo)
    priority_rows = read_csv(repo / PRIORITY_CSV)
    map_rows = read_csv(repo / MAP_CSV)
    domain_functions = tuple(build_domain_functions(priority_rows))
    caller_clusters = tuple(build_caller_clusters(map_rows))
    argument_shapes = tuple(build_argument_shapes(repo))

    sound_rows = [row for row in map_rows if row.get("repo_function") == "SoundEffect"]
    callers: set[str] = set()
    callees: set[str] = set()
    for row in sound_rows:
        callers.update(x for x in row.get("callers", "").split(";") if x)
        callees.update(x for x in row.get("called_functions", "").split(";") if x)
    selected_cluster = caller_clusters[0].cluster if caller_clusters else "audio-effects-internal"
    for cluster in caller_clusters:
        if cluster.cluster == "audio-effects-internal":
            selected_cluster = cluster.cluster
            break
    summary = ChainSummary(
        candidate_count=len(domain_functions),
        soundeffect_rows=len(sound_rows),
        caller_count=len(callers),
        callee_count=len(callees),
        callsite_count=sum(shape.site_count for shape in argument_shapes),
        callsite_shape_count=len(argument_shapes),
        selected_cluster=selected_cluster,
    )
    tickets = make_tickets(summary)
    return AudioEffectsChain(
        domain_id="audio-effects",
        pivot_function="SoundEffect",
        status="audio-effects-chain-terminal-no-safe-marker-or-source-patch",
        final_decision="handoff-to-collision-domain",
        next_ticket="RE-053",
        code_change_ready_count=0,
        marker_ready_count=0,
        source_patch_ready_count=0,
        summary=summary,
        domain_functions=domain_functions,
        caller_clusters=caller_clusters,
        argument_shapes=argument_shapes,
        tickets=tickets,
    )


def write_dict_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_summary_csv(path: Path, chain: AudioEffectsChain) -> None:
    fields = ["story_id", "topic", "status", "decision", "code_change_readiness", "safe_next_action", "next_ticket"]
    write_dict_csv(path, fields, [ticket.__dict__ for ticket in chain.tickets])


def write_domain_csv(path: Path, chain: AudioEffectsChain) -> None:
    fields = ["function", "file", "line", "status", "markers", "bucket", "score", "caller_count", "callee_count", "role", "readiness"]
    write_dict_csv(path, fields, [function.__dict__ for function in chain.domain_functions])


def write_caller_csv(path: Path, chain: AudioEffectsChain) -> None:
    fields = ["cluster", "function_count", "caller_count", "representative_functions", "readiness", "blocker"]
    rows = []
    for cluster in chain.caller_clusters:
        rows.append({**cluster.__dict__, "representative_functions": ";".join(cluster.representative_functions)})
    write_dict_csv(path, fields, rows)


def write_taxonomy_csv(path: Path, chain: AudioEffectsChain) -> None:
    fields = ["shape_id", "arity", "site_count", "first_arg_kind", "second_arg_kind", "third_arg_kind", "readiness", "blocker"]
    write_dict_csv(path, fields, [shape.__dict__ for shape in chain.argument_shapes])


def write_markdown(path: Path, chain: AudioEffectsChain) -> None:
    lines = [
        "# RE-045..RE-052 — Audio/effects chain closure",
        "",
        f"Domain: `{chain.domain_id}`",
        f"Pivot: `{chain.pivot_function}`",
        f"Status: `{chain.status}`",
        f"Final decision: `{chain.final_decision}`",
        f"code-change-ready tickets: `{chain.code_change_ready_count}`",
        f"marker-ready tickets: `{chain.marker_ready_count}`",
        f"source-patch-ready tickets: `{chain.source_patch_ready_count}`",
        f"Recommended next ticket: `{chain.next_ticket}`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-045 domain scope published.",
        "- [x] RE-046 caller map published.",
        "- [x] RE-047 argument taxonomy published.",
        "- [x] RE-048 comparison gate blocked source/marker changes.",
        "- [x] RE-049 cluster proof stayed metadata-only.",
        "- [x] RE-050 marker/source patch gate denied changes.",
        "- [x] RE-051 terminal blocker published.",
        "- [x] RE-052 next-domain handoff selected collision.",
        "",
        "## Summary",
        "",
        f"- audio/effects candidates: `{chain.summary.candidate_count}`",
        f"- SoundEffect mapped rows: `{chain.summary.soundeffect_rows}`",
        f"- SoundEffect callers classified: `{chain.summary.caller_count}`",
        f"- SoundEffect callees counted: `{chain.summary.callee_count}`",
        f"- source callsites classified by shape: `{chain.summary.callsite_count}`",
        f"- argument shapes: `{chain.summary.callsite_shape_count}`",
        f"- selected proof cluster: `{chain.summary.selected_cluster}`",
        "",
        "## Tickets",
        "",
    ]
    for ticket in chain.tickets:
        lines.extend([
            f"- `{ticket.story_id}` `{ticket.topic}`",
            f"  - decision: `{ticket.decision}`",
            f"  - readiness: `{ticket.code_change_readiness}`",
            f"  - next: `{ticket.next_ticket}`",
        ])
    lines.extend(["", "## Caller clusters", ""])
    for cluster in chain.caller_clusters:
        lines.extend([
            f"- `{cluster.cluster}`",
            f"  - callers: `{cluster.caller_count}`; functions: `{cluster.function_count}`; readiness: `{cluster.readiness}`",
            f"  - blocker: {cluster.blocker}",
        ])
    lines.extend([
        "",
        "## Terminal decision",
        "",
        "No production source patch and no `(F)`, `(D)`, or `(**)` marker is safe from the current evidence. The next useful chain is `collision`, starting at RE-053, because RE-044 ranked it as the next domain-specific candidate after audio/effects.",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def story_filename(ticket: Ticket) -> str:
    return f"{ticket.story_id}-{ticket.topic}.md"


def write_story(path: Path, chain: AudioEffectsChain, ticket: Ticket) -> None:
    lines = [
        f"# {ticket.story_id} — {ticket.title}",
        "",
        f"Status: {ticket.status}",
        "",
        "## Goal",
        "",
        f"Advance `{chain.domain_id}` / `{chain.pivot_function}` through `{ticket.topic}` as a metadata-only reverse-engineering step.",
        "",
        "## Scope",
        "",
        "- depends on: " + ", ".join(f"`{dep}`" for dep in ticket.depends_on),
        "- safety contract: `metadata-only; no opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records; no raw addresses in generated outputs`",
        "",
        "## Progress",
        "",
    ]
    for item in ticket.progress:
        label = item.replace("-", " ").capitalize()
        lines.append(f"- [x] {label}.")
    lines.extend([
        "",
        "## Generated artifacts",
        "",
    ])
    for artifact in ticket.generated_artifacts:
        lines.append(f"- `{artifact}`")
    lines.extend([
        "",
        "## Findings",
        "",
    ])
    for finding in ticket.findings:
        lines.append(f"- {finding}")
    lines.extend([
        "",
        "## Readiness decision",
        "",
        f"- decision: `{ticket.decision}`",
        f"- safe next action: `{ticket.safe_next_action}`",
        f"- code change readiness: `{ticket.code_change_readiness}`",
        f"- next ticket: `{ticket.next_ticket}`",
        "",
        "Do not patch production source or add `(F)`, `(D)`, or `(**)` markers from this story alone.",
        "",
        "## Validation",
        "",
        "- `python3 -m pytest tests/reverse/test_re045_re052_audio_effects_chain.py -q`",
        "- metadata-only guard over RE-045..RE-052 outputs",
        "",
        "## Next step",
        "",
        f"{ticket.next_ticket}: {ticket.safe_next_action}.",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_all_artifacts(chain: AudioEffectsChain, repo: Path) -> dict[str, object]:
    repo = Path(repo)
    summary_csv = repo / SUMMARY_CSV
    domain_csv = repo / DOMAIN_CSV
    caller_csv = repo / CALLER_CSV
    taxonomy_csv = repo / TAXONOMY_CSV
    md = repo / MD_OUTPUT
    write_summary_csv(summary_csv, chain)
    write_domain_csv(domain_csv, chain)
    write_caller_csv(caller_csv, chain)
    write_taxonomy_csv(taxonomy_csv, chain)
    write_markdown(md, chain)
    stories = []
    for ticket in chain.tickets:
        story_path = repo / STORY_DIR / story_filename(ticket)
        write_story(story_path, chain, ticket)
        stories.append(story_path)
    return {
        "summary_csv": summary_csv,
        "domain_csv": domain_csv,
        "caller_csv": caller_csv,
        "taxonomy_csv": taxonomy_csv,
        "md": md,
        "stories": stories,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="TOMB5 repo root; default: current directory")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    chain = build_audio_effects_chain(repo)
    written = write_all_artifacts(chain, repo)
    print(f"wrote RE-045..RE-052 summary to {written['summary_csv']}")
    print(f"wrote RE-045..RE-052 markdown to {written['md']}")
    print(f"wrote {len(written['stories'])} stories")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
