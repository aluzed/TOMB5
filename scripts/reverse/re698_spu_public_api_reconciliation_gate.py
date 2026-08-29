"""RE-698: fail-closed public SPU API reconciliation metadata."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

FORBIDDEN = ("0x", "opcode", "payload", ".bin", "disassembly", "pseudocode", "address")
HANDOFF_FIELDS = (
    "story_id", "topic", "predecessor", "unmatched_declaration_count",
    "source_behavior_proof_count", "source_patch_authorized_count",
    "code_change_readiness", "next_ticket", "next_topic", "stop_condition",
)
API_PATTERN = re.compile(
    r"(?:extern\s+)?(?:void|long|short|int|unsigned\s+long|unsigned\s+short)\s+"
    r"(Spu[A-Za-z0-9_]+)\s*\("
)


@dataclass(frozen=True)
class ApiRow:
    api_name: str
    declaration_status: str
    definition_status: str
    proof_status: str
    code_change_readiness: str
    blocker: str


@dataclass(frozen=True)
class Inventory:
    header_declaration_count: int
    source_definition_count: int
    unmatched_declaration_count: int
    patch_ready_count: int
    rows: tuple[ApiRow, ...]


def _read_re697_handoff(root: Path) -> None:
    path = root / "docs/reverse/generated/re697-ghidra-unmapped-proof-acquisition-policy-handoff.csv"
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    except OSError as error:
        raise ValueError("RE-697 handoff is required") from error
    if len(rows) != 1:
        raise ValueError("RE-697 handoff must contain one row")
    row = rows[0]
    expected = {
        "story_id": "RE-697",
        "topic": "ghidra-unmapped-proof-acquisition-policy",
        "predecessor": "RE-696",
        "unmapped_function_count": "723",
        "physical_cluster_count": "112",
        "aggregate_lane_count": "8",
        "identity_proof_count": "0",
        "raw_evidence_versioned": "no",
        "code_change_readiness": "blocked",
        "next_ticket": "TBD",
        "next_topic": "none",
        "stop_condition": "the finite mapping backlog is complete; a new source-backed identity or behavior proof input is required before reopening a lane",
    }
    if set(row) != set(expected):
        raise ValueError("RE-697 handoff drift in schema")
    for field, value in expected.items():
        if row.get(field) != value:
            raise ValueError(f"RE-697 handoff drift in {field}")


def _names(path: Path) -> set[str]:
    return set(API_PATTERN.findall(path.read_text(encoding="utf-8")))


def build_inventory(root: Path) -> Inventory:
    _read_re697_handoff(root)
    declarations = _names(root / "EMULATOR/LIBSPU.H")
    definitions = _names(root / "EMULATOR/LIBSPU.C")
    if not declarations or not definitions:
        raise ValueError("SPU declaration/definition inventory is empty")
    unmatched = sorted(declarations - definitions)
    rows = tuple(
        ApiRow(
            api_name=name,
            declaration_status="declared",
            definition_status="absent",
            proof_status="absent",
            code_change_readiness="blocked",
            blocker="behavior and ABI proof required",
        )
        for name in unmatched
    )
    return Inventory(len(declarations), len(definitions), len(rows), 0, rows)


def _assert_metadata_only(text: str) -> None:
    lowered = text.lower()
    for fragment in FORBIDDEN:
        if fragment in lowered:
            raise ValueError(f"forbidden metadata fragment: {fragment}")


def _write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    _assert_metadata_only(path.read_text(encoding="utf-8"))


def write_artifacts(inventory: Inventory, root: Path) -> dict[str, Path]:
    generated = root / "docs/reverse/generated"
    stories = root / "docs/stories"
    generated.mkdir(parents=True, exist_ok=True)
    stories.mkdir(parents=True, exist_ok=True)
    inventory_csv = generated / "re698-spu-public-api-reconciliation-gate.csv"
    handoff_csv = generated / "re698-spu-public-api-reconciliation-gate-handoff.csv"
    story = stories / "RE-698-spu-public-api-reconciliation-gate.md"
    _write_csv(
        inventory_csv,
        ("api_name", "declaration_status", "definition_status", "proof_status", "code_change_readiness", "blocker"),
        [row.__dict__ for row in inventory.rows],
    )
    handoff = {
        "story_id": "RE-698",
        "topic": "spu-public-api-reconciliation-gate",
        "predecessor": "RE-697",
        "unmatched_declaration_count": str(inventory.unmatched_declaration_count),
        "source_behavior_proof_count": "0",
        "source_patch_authorized_count": "0",
        "code_change_readiness": "blocked",
        "next_ticket": "TBD",
        "next_topic": "none",
        "stop_condition": "source-backed behavior and ABI proof required before any implementation",
    }
    _write_csv(handoff_csv, HANDOFF_FIELDS, [handoff])
    story_text = """# RE-698 — gate de réconciliation de l’API publique SPU

## Progress tracker

- [x] Handoff terminal RE-697 validé fail-closed.
- [x] Inventaire déterministe des déclarations publiques et définitions locales réalisé.
- [x] Chaque déclaration sans définition locale reste bloquée.
- [x] Aucune modification de production n’est autorisée.

## Décision

Cet inventaire est une entrée de preuve source-backed minimale après RE-697. Il ne démontre ni comportement ni ABI pour les API non définies localement. Une implémentation groupée ne peut commencer qu’après une preuve de comportement et d’ABI pour une unité cohérente; aucun getter/setter isolé ne doit être sélectionné.
"""
    _assert_metadata_only(story_text)
    story.write_text(story_text, encoding="utf-8")
    return {"inventory_csv": inventory_csv, "handoff_csv": handoff_csv, "story": story}


if __name__ == "__main__":
    repository = Path(__file__).resolve().parents[2]
    write_artifacts(build_inventory(repository), repository)
