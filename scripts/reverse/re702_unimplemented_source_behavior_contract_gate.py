"""RE-702: terminal, fail-closed behavior-contract gate for the marker inventory."""

from __future__ import annotations

import csv
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

FORBIDDEN = ("0x", "opcode", "instruction", "payload", "offset", "disassembly", "pseudocode")
UPSTREAM_FIELDS = (
    "story_id", "topic", "predecessor", "source_file_count", "function_row_count", "unimplemented_marker_count",
    "source_behavior_proof_count", "source_patch_authorized_count", "selected_domain", "selected_pivot",
    "code_change_readiness", "next_ticket", "next_topic", "stop_condition",
)
UPSTREAM_VALUES = {
    "story_id": "RE-701",
    "topic": "unimplemented-source-function-identity-export",
    "predecessor": "RE-700",
    "source_file_count": "66",
    "function_row_count": "353",
    "unimplemented_marker_count": "354",
    "source_behavior_proof_count": "0",
    "source_patch_authorized_count": "0",
    "selected_domain": "none",
    "selected_pivot": "none",
    "code_change_readiness": "blocked",
    "next_ticket": "RE-702",
    "next_topic": "unimplemented-source-behavior-contract-gate",
    "stop_condition": "a source-backed behavioral contract and ABI proof are required before selecting any implementation unit",
}
IDENTITY_FIELDS = (
    "source_file", "repo_function", "unimplemented_marker_count", "source_behavior_proof_count", "code_change_readiness",
)
IDENTITY_FINGERPRINT = "f0a683d6c4d77f0016e0e25d0bb10f317c8fae2d95e3bf78d13ed475da7cba4f"
SOURCE_PATH = re.compile(r"(?!.*(?:^|/)\.\.(?:/|$))[A-Za-z0-9_./-]+$")
SOURCE_SYMBOL = re.compile(r"[A-Za-z_][A-Za-z0-9_]*$")


@dataclass(frozen=True)
class GateRow:
    source_file: str
    repo_function: str
    unimplemented_marker_count: int
    behavior_contract_status: str = "missing"
    code_change_readiness: str = "blocked"


@dataclass(frozen=True)
class Gate:
    rows: tuple[GateRow, ...]

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
    def source_behavior_proof_count(self) -> int:
        return 0

    @property
    def source_patch_authorized_count(self) -> int:
        return 0


def _read_one_handoff(repo: Path) -> None:
    path = repo / "docs/reverse/generated/re701-unimplemented-source-function-identity-export-handoff.csv"
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if tuple(reader.fieldnames or ()) != UPSTREAM_FIELDS:
                raise ValueError("RE-701 handoff schema drift")
            rows = list(reader)
    except (OSError, UnicodeDecodeError, csv.Error) as error:
        raise ValueError("RE-701 handoff unavailable") from error
    if len(rows) != 1:
        raise ValueError("RE-701 handoff row-count drift")
    if any(None in row for row in rows):
        raise ValueError("RE-701 handoff schema drift")
    for field, expected in UPSTREAM_VALUES.items():
        if rows[0].get(field) != expected:
            raise ValueError(f"RE-701 handoff drift in {field}")


def _read_identity_rows(repo: Path) -> list[dict[str, str]]:
    path = repo / "docs/reverse/generated/re701-unimplemented-source-function-identity-export.csv"
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if tuple(reader.fieldnames or ()) != IDENTITY_FIELDS:
                raise ValueError("RE-701 identity schema drift")
            rows = list(reader)
    except (OSError, UnicodeDecodeError, csv.Error) as error:
        raise ValueError("RE-701 identity unavailable") from error
    if len(rows) != 353:
        raise ValueError("RE-701 identity row-count drift")
    if any(None in row for row in rows):
        raise ValueError("RE-701 identity schema drift")
    if rows != sorted(rows, key=lambda row: (row["source_file"], row["repo_function"])):
        raise ValueError("RE-701 identity order drift")
    for row in rows:
        if not row["source_file"] or not SOURCE_PATH.fullmatch(row["source_file"]):
            raise ValueError("RE-701 identity drift in source_file")
        if not row["repo_function"] or not SOURCE_SYMBOL.fullmatch(row["repo_function"]):
            raise ValueError("RE-701 identity drift in repo_function")
        try:
            marker_count = int(row["unimplemented_marker_count"])
        except ValueError as error:
            raise ValueError("RE-701 identity drift in unimplemented_marker_count") from error
        if marker_count < 1:
            raise ValueError("RE-701 identity drift in unimplemented_marker_count")
        if row["source_behavior_proof_count"] != "0":
            raise ValueError("RE-701 identity drift in source_behavior_proof_count")
        if row["code_change_readiness"] != "blocked":
            raise ValueError("RE-701 identity drift in code_change_readiness")
    if hashlib.sha256(path.read_bytes()).hexdigest() != IDENTITY_FINGERPRINT:
        raise ValueError("RE-701 identity fingerprint drift")
    return rows


def build_gate(repo: Path) -> Gate:
    _read_one_handoff(repo)
    identity_rows = _read_identity_rows(repo)
    rows = tuple(GateRow(
        source_file=row["source_file"],
        repo_function=row["repo_function"],
        unimplemented_marker_count=int(row["unimplemented_marker_count"]),
    ) for row in identity_rows)
    gate = Gate(rows)
    if (gate.source_file_count, gate.function_row_count, gate.unimplemented_marker_count) != (66, 353, 354):
        raise ValueError("RE-701 identity aggregate drift")
    return gate


def _write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_artifacts(gate: Gate, repo: Path) -> dict[str, Path]:
    generated = repo / "docs/reverse/generated"
    stories = repo / "docs/stories"
    gate_csv = generated / "re702-unimplemented-source-behavior-contract-gate.csv"
    handoff_csv = generated / "re702-unimplemented-source-behavior-contract-gate-handoff.csv"
    story = stories / "RE-702-unimplemented-source-behavior-contract-gate.md"
    _write_csv(gate_csv, (
        "source_file", "repo_function", "unimplemented_marker_count", "behavior_contract_status", "code_change_readiness",
    ), [{
        "source_file": row.source_file, "repo_function": row.repo_function,
        "unimplemented_marker_count": str(row.unimplemented_marker_count),
        "behavior_contract_status": row.behavior_contract_status, "code_change_readiness": row.code_change_readiness,
    } for row in gate.rows])
    handoff = {
        "story_id": "RE-702", "topic": "unimplemented-source-behavior-contract-gate", "predecessor": "RE-701",
        "source_file_count": str(gate.source_file_count), "function_row_count": str(gate.function_row_count),
        "unimplemented_marker_count": str(gate.unimplemented_marker_count), "source_behavior_proof_count": "0",
        "source_patch_authorized_count": "0", "selected_domain": "none", "selected_pivot": "none",
        "code_change_readiness": "blocked", "next_ticket": "TBD", "next_topic": "none",
        "stop_condition": "external source-backed behavioral contracts and ABI proof are required before reopening this inventory",
    }
    _write_csv(handoff_csv, tuple(handoff), [handoff])
    stories.mkdir(parents=True, exist_ok=True)
    story.write_text("""# RE-702 — gate de contrat comportemental des fonctions non implémentées\n\n## Progress tracker\n\n- [x] Handoff et inventaire RE-701 validés fail-closed, y compris schéma, ordre, compteurs et champs de sécurité.\n- [x] Les 353 identités fonctionnelles restent des marqueurs source, sans contrat comportemental ni preuve ABI.\n- [x] Les 354 marqueurs sont maintenus bloqués ; aucune fonction, domaine ou pivot n’est sélectionné.\n- [x] Le sous-backlog est clôturé de façon terminale pour éviter toute implémentation spéculative.\n\n## Décision\n\nAucune preuve de contrat comportemental source-backed n’est disponible dans cet inventaire. Toute réouverture exige un contrat externe attribuable et une preuve ABI ; sans ces deux entrées, aucun patch source n’est autorisé.\n""", encoding="utf-8")
    for path in (gate_csv, handoff_csv, story):
        text = path.read_text(encoding="utf-8").lower()
        if any(fragment in text for fragment in FORBIDDEN):
            raise ValueError("generated artifact violates metadata-only guard")
    return {"gate_csv": gate_csv, "handoff_csv": handoff_csv, "story": story}


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    write_artifacts(build_gate(root), root)
