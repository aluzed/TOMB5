"""RE-700: fail-closed, metadata-only intake for tracked UNIMPLEMENTED markers."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

FORBIDDEN = ("0x", "opcode", "instruction", "payload", "offset", "disassembly", "pseudocode")
UPSTREAM_FIELDS = (
    "story_id", "topic", "predecessor", "candidate_api_count", "active_source_callsite_count",
    "commented_reference_count", "source_behavior_proof_count", "source_patch_authorized_count",
    "code_change_readiness", "next_ticket", "next_topic", "stop_condition",
)
UPSTREAM_VALUES = {
    "story_id": "RE-699",
    "topic": "spu-source-callsite-proof-gate",
    "predecessor": "RE-698",
    "candidate_api_count": "78",
    "active_source_callsite_count": "0",
    "commented_reference_count": "1",
    "source_behavior_proof_count": "0",
    "source_patch_authorized_count": "0",
    "code_change_readiness": "blocked",
    "next_ticket": "TBD",
    "next_topic": "none",
    "stop_condition": "a source-backed behavioral contract and ABI proof are required before any coherent implementation unit",
}


@dataclass(frozen=True)
class IntakeRow:
    module: str
    unimplemented_marker_count: int
    source_behavior_proof_count: int = 0
    code_change_readiness: str = "blocked"


@dataclass(frozen=True)
class Intake:
    rows: tuple[IntakeRow, ...]

    @property
    def source_file_count(self) -> int:
        return len(self.rows)

    @property
    def unimplemented_marker_count(self) -> int:
        return sum(row.unimplemented_marker_count for row in self.rows)

    @property
    def patch_ready_count(self) -> int:
        return 0


def _validate_upstream(repo: Path) -> None:
    path = repo / "docs/reverse/generated/re699-spu-source-callsite-proof-gate-handoff.csv"
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if tuple(reader.fieldnames or ()) != UPSTREAM_FIELDS:
                raise ValueError("RE-699 handoff schema drift")
            rows = list(reader)
    except (OSError, UnicodeDecodeError, csv.Error) as error:
        raise ValueError("RE-699 handoff unavailable") from error
    if len(rows) != 1:
        raise ValueError("RE-699 handoff row-count drift")
    if any(None in row for row in rows):
        raise ValueError("RE-699 handoff schema drift")
    for field, expected in UPSTREAM_VALUES.items():
        if rows[0].get(field) != expected:
            raise ValueError(f"RE-699 handoff drift in {field}")


def _without_comments_and_literals(text: str) -> str:
    result: list[str] = []
    index = 0
    state = "code"
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if state == "code" and char == "R" and next_char == "\"":
            delimiter_end = text.find("(", index + 2, index + 19)
            delimiter = text[index + 2:delimiter_end] if delimiter_end != -1 else ""
            if delimiter_end != -1 and not any(character in delimiter for character in " ()\\\t\r\n"):
                terminator = ")" + delimiter + "\""
                literal_end = text.find(terminator, delimiter_end + 1)
                if literal_end != -1:
                    literal = text[index:literal_end + len(terminator)]
                    result.extend("\n" if character == "\n" else " " for character in literal)
                    index = literal_end + len(terminator)
                    continue
            result.append(char)
            index += 1
        elif state == "code" and char == "/" and next_char == "/":
            state = "line-comment"
            result.extend("  ")
            index += 2
        elif state == "code" and char == "/" and next_char == "*":
            state = "block-comment"
            result.extend("  ")
            index += 2
        elif state == "code" and char in "\"'":
            state = char
            result.append(" ")
            index += 1
        elif state == "line-comment":
            result.append("\n" if char == "\n" else " ")
            if char == "\n":
                state = "code"
            index += 1
        elif state == "block-comment":
            if char == "*" and next_char == "/":
                state = "code"
                result.extend("  ")
                index += 2
            else:
                result.append("\n" if char == "\n" else " ")
                index += 1
        elif state in ("\"", "'"):
            if char == "\\":
                result.extend("  ")
                index += 2
            elif char == state:
                state = "code"
                result.append(" ")
                index += 1
            else:
                result.append("\n" if char == "\n" else " ")
                index += 1
        else:
            result.append(char)
            index += 1
    return "".join(result)


def _is_known_false_preprocessor_expression(expression: str) -> bool:
    normalized = expression.strip()
    while normalized.startswith("(") and normalized.endswith(")"):
        normalized = normalized[1:-1].strip()
    return re.fullmatch(r"0+[uUlL]*", normalized) is not None


def _without_inactive_preprocessor_regions(text: str) -> str:
    text = re.sub(r"\\[ \t]*\r?\n", " ", text)
    output: list[str] = []
    stack: list[tuple[bool, bool, bool]] = []
    active = True
    for line in text.splitlines(keepends=True):
        directive = re.match(r"^\s*#\s*(if|ifdef|ifndef|elif|else|endif)\b(.*)$", line)
        if directive:
            command, expression = directive.groups()
            if command in {"if", "ifdef", "ifndef"}:
                known_false = _is_known_false_preprocessor_expression(expression)
                branch_active = active and not known_false
                stack.append((active, known_false, branch_active))
                active = branch_active
            elif command == "elif":
                if not stack:
                    raise ValueError("unbalanced preprocessor directive")
                parent, all_prior_branches_known_false, _ = stack.pop()
                known_false = _is_known_false_preprocessor_expression(expression)
                branch_active = parent and not known_false
                stack.append((parent, all_prior_branches_known_false and known_false, branch_active))
                active = branch_active
            elif command == "else":
                if not stack:
                    raise ValueError("unbalanced preprocessor directive")
                parent, _, _ = stack.pop()
                branch_active = parent
                stack.append((parent, False, branch_active))
                active = branch_active
            else:
                if not stack:
                    raise ValueError("unbalanced preprocessor directive")
                stack.pop()
                active = stack[-1][2] if stack else True
            output.append("\n" if line.endswith("\n") else "")
        elif active:
            if re.match(r"^\s*#", line):
                output.append("\n" if line.endswith("\n") else "")
            else:
                output.append(line)
        else:
            output.append("\n" if line.endswith("\n") else "")
    if stack:
        raise ValueError("unbalanced preprocessor directive")
    return "".join(output)


def build_intake(repo: Path) -> Intake:
    _validate_upstream(repo)
    rows = []
    for path in repo.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".c", ".cpp", ".cc"}:
            continue
        try:
            clean = _without_inactive_preprocessor_regions(_without_comments_and_literals(path.read_text(encoding="utf-8")))
        except UnicodeDecodeError as error:
            raise ValueError(f"source decode failure: {path.relative_to(repo)}") from error
        count = len(re.findall(r"\bUNIMPLEMENTED\s*\(\s*\)\s*;", clean))
        if count:
            rows.append(IntakeRow(path.relative_to(repo).as_posix(), count))
    return Intake(tuple(sorted(rows, key=lambda row: row.module)))


def _write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_artifacts(intake: Intake, repo: Path) -> dict[str, Path]:
    generated = repo / "docs/reverse/generated"
    stories = repo / "docs/stories"
    intake_csv = generated / "re700-unimplemented-source-callsite-proof-intake.csv"
    handoff_csv = generated / "re700-unimplemented-source-callsite-proof-intake-handoff.csv"
    story = stories / "RE-700-unimplemented-source-callsite-proof-intake.md"
    _write_csv(intake_csv, ("source_file", "unimplemented_marker_count", "source_behavior_proof_count", "code_change_readiness"), [
        {"source_file": row.module, "unimplemented_marker_count": str(row.unimplemented_marker_count),
         "source_behavior_proof_count": "0", "code_change_readiness": "blocked"} for row in intake.rows
    ])
    handoff = {
        "story_id": "RE-700", "topic": "unimplemented-source-callsite-proof-intake", "predecessor": "RE-699",
        "source_file_count": str(intake.source_file_count), "unimplemented_marker_count": str(intake.unimplemented_marker_count),
        "source_behavior_proof_count": "0", "source_patch_authorized_count": "0", "selected_domain": "none",
        "selected_pivot": "none", "code_change_readiness": "blocked", "next_ticket": "TBD", "next_topic": "none",
        "stop_condition": "a source-backed behavioral contract and ABI proof are required before selecting any implementation unit",
    }
    _write_csv(handoff_csv, tuple(handoff), [handoff])
    stories.mkdir(parents=True, exist_ok=True)
    story.write_text("""# RE-700 — intake des marqueurs source non implémentés\n\n## Progress tracker\n\n- [x] Handoff RE-699 validé fail-closed.\n- [x] Marqueurs `UNIMPLEMENTED()` actifs inventoriés par fichier, sans texte source ni preuve binaire.\n- [x] Aucun contrat comportemental ou ABI source-backed n’est établi.\n- [x] Aucune unité de production n’est sélectionnée ni autorisée.\n\n## Décision\n\nCet inventaire est un signal de triage seulement. Il ne démontre ni identité, ni comportement, ni ABI ; aucun patch ne doit en être déduit. Une reprise exige une preuve comportementale et ABI source-backed pour une unité cohérente.\n""", encoding="utf-8")
    for path in (intake_csv, handoff_csv, story):
        text = path.read_text(encoding="utf-8").lower()
        if any(fragment in text for fragment in FORBIDDEN):
            raise ValueError("generated artifact violates metadata-only guard")
    return {"intake_csv": intake_csv, "handoff_csv": handoff_csv, "story": story}


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    write_artifacts(build_intake(root), root)
