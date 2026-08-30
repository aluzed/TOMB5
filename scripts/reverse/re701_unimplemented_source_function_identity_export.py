"""RE-701: metadata-only function identity for active UNIMPLEMENTED markers."""

from __future__ import annotations

import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts.reverse.re700_unimplemented_source_callsite_proof_intake import (
    _without_comments_and_literals,
    _without_inactive_preprocessor_regions,
)

FORBIDDEN = ("0x", "opcode", "instruction", "payload", "offset", "disassembly", "pseudocode")
UPSTREAM_FIELDS = (
    "story_id", "topic", "predecessor", "source_file_count", "unimplemented_marker_count",
    "source_behavior_proof_count", "source_patch_authorized_count", "selected_domain", "selected_pivot",
    "code_change_readiness", "next_ticket", "next_topic", "stop_condition",
)
UPSTREAM_VALUES = {
    "story_id": "RE-700",
    "topic": "unimplemented-source-callsite-proof-intake",
    "predecessor": "RE-699",
    "source_file_count": "66",
    "unimplemented_marker_count": "354",
    "source_behavior_proof_count": "0",
    "source_patch_authorized_count": "0",
    "selected_domain": "none",
    "selected_pivot": "none",
    "code_change_readiness": "blocked",
    "next_ticket": "TBD",
    "next_topic": "none",
    "stop_condition": "a source-backed behavioral contract and ABI proof are required before selecting any implementation unit",
}


@dataclass(frozen=True)
class IdentityRow:
    source_file: str
    repo_function: str
    unimplemented_marker_count: int
    source_behavior_proof_count: int = 0
    code_change_readiness: str = "blocked"


@dataclass(frozen=True)
class IdentityExport:
    rows: tuple[IdentityRow, ...]

    @property
    def source_file_count(self) -> int:
        return len({row.source_file for row in self.rows})

    @property
    def function_row_count(self) -> int:
        return len(self.rows)

    @property
    def unimplemented_marker_count(self) -> int:
        return sum(row.unimplemented_marker_count for row in self.rows)

    @property
    def patch_ready_count(self) -> int:
        return 0


def _validate_upstream(repo: Path) -> None:
    path = repo / "docs/reverse/generated/re700-unimplemented-source-callsite-proof-intake-handoff.csv"
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if tuple(reader.fieldnames or ()) != UPSTREAM_FIELDS:
                raise ValueError("RE-700 handoff schema drift")
            rows = list(reader)
    except (OSError, UnicodeDecodeError, csv.Error) as error:
        raise ValueError("RE-700 handoff unavailable") from error
    if len(rows) != 1:
        raise ValueError("RE-700 handoff row-count drift")
    if any(None in row for row in rows):
        raise ValueError("RE-700 handoff schema drift")
    for field, expected in UPSTREAM_VALUES.items():
        if rows[0].get(field) != expected:
            raise ValueError(f"RE-700 handoff drift in {field}")


def _function_spans(clean: str) -> list[tuple[int, int, str]]:
    """Return simple C/C++ function body spans, using sanitized source only."""
    spans: list[tuple[int, int, str]] = []
    pattern = re.compile(r"\b([A-Za-z_]\w*)\s*\([^;{}]*\)\s*(?:const\s*)?\{")
    control_words = {"if", "for", "while", "switch", "catch"}
    for match in pattern.finditer(clean):
        name = match.group(1)
        if name in control_words:
            continue
        depth = 0
        end = None
        for index in range(match.end() - 1, len(clean)):
            if clean[index] == "{":
                depth += 1
            elif clean[index] == "}":
                depth -= 1
                if depth == 0:
                    end = index + 1
                    break
        if end is not None:
            spans.append((match.start(), end, name))
    return spans


def _marker_rows(path: Path, repo: Path) -> list[IdentityRow]:
    try:
        clean = _without_inactive_preprocessor_regions(_without_comments_and_literals(path.read_text(encoding="utf-8")))
    except UnicodeDecodeError as error:
        raise ValueError(f"source decode failure: {path.relative_to(repo)}") from error
    markers = list(re.finditer(r"\bUNIMPLEMENTED\s*\(\s*\)\s*;", clean))
    if not markers:
        return []
    spans = _function_spans(clean)
    counts: dict[str, int] = {}
    for marker in markers:
        containing = [span for span in spans if span[0] <= marker.start() < span[1]]
        if not containing:
            raise ValueError(f"unbound active marker in {path.relative_to(repo).as_posix()}")
        _, _, function = min(containing, key=lambda span: span[1] - span[0])
        counts[function] = counts.get(function, 0) + 1
    source_file = path.relative_to(repo).as_posix()
    return [IdentityRow(source_file, function, count) for function, count in counts.items()]


def build_export(repo: Path) -> IdentityExport:
    _validate_upstream(repo)
    rows: list[IdentityRow] = []
    for path in repo.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".c", ".cc", ".cpp"}:
            rows.extend(_marker_rows(path, repo))
    return IdentityExport(tuple(sorted(rows, key=lambda row: (row.source_file, row.repo_function))))


def _write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_artifacts(export: IdentityExport, repo: Path) -> dict[str, Path]:
    generated = repo / "docs/reverse/generated"
    stories = repo / "docs/stories"
    identity_csv = generated / "re701-unimplemented-source-function-identity-export.csv"
    handoff_csv = generated / "re701-unimplemented-source-function-identity-export-handoff.csv"
    story = stories / "RE-701-unimplemented-source-function-identity-export.md"
    _write_csv(identity_csv, (
        "source_file", "repo_function", "unimplemented_marker_count", "source_behavior_proof_count", "code_change_readiness",
    ), [{
        "source_file": row.source_file, "repo_function": row.repo_function,
        "unimplemented_marker_count": str(row.unimplemented_marker_count), "source_behavior_proof_count": "0",
        "code_change_readiness": "blocked",
    } for row in export.rows])
    handoff = {
        "story_id": "RE-701", "topic": "unimplemented-source-function-identity-export", "predecessor": "RE-700",
        "source_file_count": str(export.source_file_count), "function_row_count": str(export.function_row_count),
        "unimplemented_marker_count": str(export.unimplemented_marker_count), "source_behavior_proof_count": "0",
        "source_patch_authorized_count": "0", "selected_domain": "none", "selected_pivot": "none",
        "code_change_readiness": "blocked", "next_ticket": "RE-702",
        "next_topic": "unimplemented-source-behavior-contract-gate",
        "stop_condition": "a source-backed behavioral contract and ABI proof are required before selecting any implementation unit",
    }
    _write_csv(handoff_csv, tuple(handoff), [handoff])
    stories.mkdir(parents=True, exist_ok=True)
    story.write_text("""# RE-701 — identité fonctionnelle des marqueurs source non implémentés\n\n## Progress tracker\n\n- [x] Handoff RE-700 validé fail-closed, y compris ses compteurs et ses blocages.\n- [x] Chaque marqueur `UNIMPLEMENTED()` actif est rattaché à une fonction source par son périmètre lexical.\n- [x] L’export ne contient que chemin, symbole source et compteurs ; il n’ajoute aucune preuve comportementale, ABI ou binaire.\n- [x] Aucune unité de production n’est sélectionnée ou autorisée.\n\n## Décision\n\nL’identité lexicale réduit l’inventaire à des fonctions nommées, mais elle ne prouve pas leur comportement ni leur ABI. RE-702 devra refuser toute sélection tant qu’un contrat comportemental source-backed manque.\n""", encoding="utf-8")
    for path in (identity_csv, handoff_csv, story):
        text = path.read_text(encoding="utf-8").lower()
        if any(fragment in text for fragment in FORBIDDEN):
            raise ValueError("generated artifact violates metadata-only guard")
    return {"identity_csv": identity_csv, "handoff_csv": handoff_csv, "story": story}


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    write_artifacts(build_export(root), root)
