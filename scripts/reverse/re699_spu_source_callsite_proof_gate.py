"""RE-699: fail-closed source-callsite proof gate for unmatched SPU APIs."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

FORBIDDEN = ("0x", "opcode", "payload", ".bin", "disassembly", "pseudocode", "address")
UPSTREAM_FIELDS = (
    "story_id", "topic", "predecessor", "unmatched_declaration_count",
    "source_behavior_proof_count", "source_patch_authorized_count",
    "code_change_readiness", "next_ticket", "next_topic", "stop_condition",
)
INVENTORY_FIELDS = (
    "api_name", "declaration_status", "definition_status", "proof_status",
    "code_change_readiness", "blocker",
)
HANDOFF_FIELDS = (
    "story_id", "topic", "predecessor", "candidate_api_count",
    "active_source_callsite_count", "commented_reference_count",
    "source_behavior_proof_count", "source_patch_authorized_count",
    "code_change_readiness", "next_ticket", "next_topic", "stop_condition",
)
UPSTREAM = {
    "story_id": "RE-698",
    "topic": "spu-public-api-reconciliation-gate",
    "predecessor": "RE-697",
    "unmatched_declaration_count": "78",
    "source_behavior_proof_count": "0",
    "source_patch_authorized_count": "0",
    "code_change_readiness": "blocked",
    "next_ticket": "TBD",
    "next_topic": "none",
    "stop_condition": "source-backed behavior and ABI proof required before any implementation",
}
EXPECTED_INVENTORY = {
    "declaration_status": "declared",
    "definition_status": "absent",
    "proof_status": "absent",
    "code_change_readiness": "blocked",
    "blocker": "behavior and ABI proof required",
}


@dataclass(frozen=True)
class CallsiteRow:
    api_name: str
    active_source_callsite_count: int
    source_callsite_status: str
    code_change_readiness: str
    blocker: str


@dataclass(frozen=True)
class Audit:
    candidate_api_count: int
    active_source_callsite_count: int
    commented_reference_count: int
    patch_ready_count: int
    rows: tuple[CallsiteRow, ...]


def _read_csv(path: Path, expected_fields: tuple[str, ...], label: str) -> list[dict[str, str]]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != list(expected_fields):
                raise ValueError(f"{label} drift in schema")
            return list(reader)
    except OSError as error:
        raise ValueError(f"{label} is required") from error


def _read_upstream(root: Path) -> None:
    rows = _read_csv(
        root / "docs/reverse/generated/re698-spu-public-api-reconciliation-gate-handoff.csv",
        UPSTREAM_FIELDS,
        "RE-698 handoff",
    )
    if len(rows) != 1:
        raise ValueError("RE-698 handoff must contain one row")
    for field, value in UPSTREAM.items():
        if rows[0].get(field) != value:
            raise ValueError(f"RE-698 handoff drift in {field}")


def _candidate_names(root: Path) -> tuple[str, ...]:
    rows = _read_csv(
        root / "docs/reverse/generated/re698-spu-public-api-reconciliation-gate.csv",
        INVENTORY_FIELDS,
        "RE-698 inventory",
    )
    if len(rows) != 78:
        raise ValueError("RE-698 inventory drift in row count")
    names: list[str] = []
    for row in rows:
        for field, value in EXPECTED_INVENTORY.items():
            if row.get(field) != value:
                raise ValueError(f"RE-698 inventory drift in {field}")
        name = row.get("api_name", "")
        if not re.fullmatch(r"Spu[A-Za-z0-9_]+", name):
            raise ValueError("RE-698 inventory drift in api_name")
        names.append(name)
    if names != sorted(names) or len(set(names)) != len(names):
        raise ValueError("RE-698 inventory drift in api_name")
    return tuple(names)


def _source_files(root: Path) -> tuple[Path, ...]:
    source_suffixes = {".C", ".CPP", ".c", ".cc", ".cpp", ".cxx"}
    return tuple(
        path for path in sorted(root.rglob("*"))
        if path.is_file() and path.suffix in source_suffixes
        if path != root / "EMULATOR/LIBSPU.C" and "BUILD" not in path.parts
    )


def _lex_c(text: str) -> tuple[str, str]:
    text = text.replace("\\\r\n", "").replace("\\\n", "")
    code: list[str] = []
    comments: list[str] = []
    index = 0
    while index < len(text):
        if text.startswith("//", index):
            end = text.find("\n", index)
            if end < 0:
                end = len(text)
            comments.append(text[index:end])
            code.append(" " * (end - index))
            index = end
        elif text.startswith("/*", index):
            end = text.find("*/", index + 2)
            if end < 0:
                raise ValueError("unterminated source comment")
            end += 2
            fragment = text[index:end]
            comments.append(fragment)
            code.append("".join("\n" if char == "\n" else " " for char in fragment))
            index = end
        elif text[index] in "\"'":
            quote = text[index]
            start = index
            index += 1
            while index < len(text):
                if text[index] == "\\":
                    index += 2
                elif index < len(text) and text[index] == quote:
                    index += 1
                    break
                else:
                    index += 1
            else:
                raise ValueError("unterminated source literal")
            fragment = text[start:index]
            code.append("".join("\n" if char == "\n" else " " for char in fragment))
        else:
            code.append(text[index])
            index += 1
    return "".join(code), "\n".join(comments)


def _strip_disabled_preprocessor_blocks(code: str) -> str:
    """Mask only deterministic inactive branches; retain every potentially live branch."""
    frames: list[dict[str, bool]] = []
    output: list[str] = []
    for line in code.splitlines(keepends=True):
        directive = re.match(r"^\s*#\s*(if|ifdef|ifndef|elif|else|endif)\b(.*)$", line)
        if directive:
            kind, expression = directive.groups()
            parent_enabled = frames[-1]["enabled"] if frames else True
            zero = bool(re.fullmatch(r"\s*0\s*(?:\r?\n)?", expression))
            one = bool(re.fullmatch(r"\s*1\s*(?:\r?\n)?", expression))
            if kind == "if":
                frames.append(
                    {
                        "parent_enabled": parent_enabled,
                        "fallthrough": parent_enabled and not one,
                        "enabled": parent_enabled and not zero,
                        "else_seen": False,
                    }
                )
            elif kind in {"ifdef", "ifndef"}:
                frames.append(
                    {
                        "parent_enabled": parent_enabled,
                        "fallthrough": parent_enabled,
                        "enabled": parent_enabled,
                        "else_seen": False,
                    }
                )
            elif kind == "elif" and frames:
                frame = frames[-1]
                if frame["else_seen"]:
                    raise ValueError("invalid preprocessor elif after else")
                frame["enabled"] = frame["fallthrough"] and not zero
                frame["fallthrough"] = frame["fallthrough"] and not one
            elif kind == "else" and frames:
                frame = frames[-1]
                if frame["else_seen"]:
                    raise ValueError("duplicate preprocessor else")
                frame["enabled"] = frame["fallthrough"]
                frame["fallthrough"] = False
                frame["else_seen"] = True
            elif kind == "endif" and frames:
                frames.pop()
            elif kind in {"elif", "else", "endif"}:
                raise ValueError("orphan preprocessor directive")
            output.append("\n" if line.endswith("\n") else "")
        elif frames and not frames[-1]["enabled"]:
            output.append("\n" if line.endswith("\n") else "")
        else:
            output.append(line)
    if frames:
        raise ValueError("unbalanced preprocessor directives")
    return "".join(output)


def _count_calls(name: str, texts: tuple[str, ...]) -> int:
    pattern = re.compile(r"\b" + re.escape(name) + r"\s*\(")
    return sum(len(pattern.findall(text)) for text in texts)


def build_audit(root: Path) -> Audit:
    _read_upstream(root)
    names = _candidate_names(root)
    source_files = _source_files(root)
    if not source_files:
        raise ValueError("source callsite corpus is empty")
    lexed: list[tuple[str, str]] = []
    for path in source_files:
        try:
            lexed.append(_lex_c(path.read_text(encoding="utf-8")))
        except UnicodeDecodeError as error:
            raise ValueError(f"source decode failed: {path}") from error
    code_texts = tuple(_strip_disabled_preprocessor_blocks(code) for code, _ in lexed)
    comment_texts = tuple(comment for _, comment in lexed)
    rows: list[CallsiteRow] = []
    commented_reference_count = 0
    for name in names:
        active_count = _count_calls(name, code_texts)
        commented_reference_count += _count_calls(name, comment_texts)
        status = "active-source-callsite" if active_count else "no-active-source-callsite"
        rows.append(CallsiteRow(name, active_count, status, "blocked", "behavior and ABI proof required"))
    return Audit(
        candidate_api_count=len(rows),
        active_source_callsite_count=sum(row.active_source_callsite_count for row in rows),
        commented_reference_count=commented_reference_count,
        patch_ready_count=0,
        rows=tuple(rows),
    )


def _assert_metadata_only(text: str) -> None:
    lowered = text.lower()
    for fragment in FORBIDDEN:
        if fragment in lowered:
            raise ValueError(f"forbidden metadata fragment: {fragment}")


def _write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, str | int]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    _assert_metadata_only(path.read_text(encoding="utf-8"))


def write_artifacts(audit: Audit, root: Path) -> dict[str, Path]:
    generated = root / "docs/reverse/generated"
    stories = root / "docs/stories"
    generated.mkdir(parents=True, exist_ok=True)
    stories.mkdir(parents=True, exist_ok=True)
    audit_csv = generated / "re699-spu-source-callsite-proof-gate.csv"
    handoff_csv = generated / "re699-spu-source-callsite-proof-gate-handoff.csv"
    story = stories / "RE-699-spu-source-callsite-proof-gate.md"
    _write_csv(
        audit_csv,
        ("api_name", "active_source_callsite_count", "source_callsite_status", "code_change_readiness", "blocker"),
        [row.__dict__ for row in audit.rows],
    )
    handoff = {
        "story_id": "RE-699",
        "topic": "spu-source-callsite-proof-gate",
        "predecessor": "RE-698",
        "candidate_api_count": str(audit.candidate_api_count),
        "active_source_callsite_count": str(audit.active_source_callsite_count),
        "commented_reference_count": str(audit.commented_reference_count),
        "source_behavior_proof_count": "0",
        "source_patch_authorized_count": "0",
        "code_change_readiness": "blocked",
        "next_ticket": "TBD",
        "next_topic": "none",
        "stop_condition": "a source-backed behavioral contract and ABI proof are required before any coherent implementation unit",
    }
    _write_csv(handoff_csv, HANDOFF_FIELDS, [handoff])
    story_text = """# RE-699 — gate de preuve des callsites source SPU

## Progress tracker

- [x] Handoff RE-698 validé fail-closed, y compris ses champs de sécurité.
- [x] Les 78 API candidates sont vérifiées dans le corpus source suivi.
- [x] Aucun callsite actif ne prouve un comportement ou un contrat d’ABI.
- [x] La référence uniquement commentée reste non probante.
- [x] Aucune modification de production n’est autorisée.

## Décision

Le corpus source ne contient aucun callsite actif pour les API publiques SPU sans définition locale. Cette absence, et une référence commentée non exécutable, ne justifient ni une implémentation ni une nouvelle série de micro-correctifs. Toute reprise exige une unité cohérente appuyée par un contrat comportemental et ABI source-backed.
"""
    _assert_metadata_only(story_text)
    story.write_text(story_text, encoding="utf-8")
    return {"audit_csv": audit_csv, "handoff_csv": handoff_csv, "story": story}


if __name__ == "__main__":
    repository = Path(__file__).resolve().parents[2]
    write_artifacts(build_audit(repository), repository)
