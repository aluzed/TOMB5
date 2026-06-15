#!/usr/bin/env python3
"""Generate RE-166 UI text rendering state-contract artifacts."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path

RE163_PLAN_CSV = "docs/reverse/generated/re163-module-spec-psxpc-n-ticket-plan.csv"
RE165_TAXONOMY_CSV = "docs/reverse/generated/re165-ui-text-rendering-argument-taxonomy.csv"
CONTRACT_CSV = "docs/reverse/generated/re166-ui-text-rendering-state-contract.csv"
MD_OUTPUT = "docs/reverse/functions/re166-ui-text-rendering-state-contract.md"
STORY_OUTPUT = "docs/stories/RE-166-ui-text-rendering-state-contract.md"
TEXT_SOURCE = "SPEC_PSXPC_N/TEXT_S.C"

FORBIDDEN_FRAGMENTS = ("0x", "pay" + "load", "op" + "code", "machine" + " word", "raw" + " call target")
EXPECTED_PLAN_IDS = ("RE-164", "RE-165", "RE-166", "RE-167", "RE-168", "RE-169", "RE-170")
EXPECTED_TAXONOMY_FAMILIES = 20
EXPECTED_RE165_FAMILY_IDS = (
    "ui-text-printstring-caller-layout-literal-colour-inline-control-string-center",
    "ui-text-printstring-caller-layout-literal-colour-inline-control-string-none",
    "ui-text-printstring-caller-layout-literal-colour-string-wad-center",
    "ui-text-printstring-caller-layout-literal-colour-string-wad-none",
    "ui-text-printstring-caller-layout-literal-colour-string-wad-right",
    "ui-text-printstring-caller-layout-request-colour-string-wad-center",
    "ui-text-printstring-caller-layout-request-colour-string-wad-none",
    "ui-text-printstring-caller-layout-request-colour-string-wad-right",
    "ui-text-printstring-literal-coordinate-literal-colour-formatted-buffer-none",
    "ui-text-printstring-literal-coordinate-literal-colour-string-wad-center",
    "ui-text-printstring-literal-coordinate-literal-colour-string-wad-right",
    "ui-text-printstring-screen-centered-literal-colour-formatted-buffer-blink-composite",
    "ui-text-printstring-screen-centered-literal-colour-formatted-buffer-caller-provided",
    "ui-text-printstring-screen-centered-literal-colour-formatted-buffer-right",
    "ui-text-printstring-screen-centered-literal-colour-string-wad-blink-composite",
    "ui-text-printstring-screen-centered-literal-colour-string-wad-center",
    "ui-text-printstring-screen-centered-request-colour-string-wad-center",
    "ui-text-getstringlength-caller-string-optional-bound",
    "ui-text-getstringlength-caller-string-with-bounds",
    "ui-text-getstringlength-string-wad-optional-bound",
)


@dataclass(frozen=True)
class ContractRow:
    contract_id: str
    function: str
    state_surface: str
    source_tokens: str
    source_contract: str
    proof_input: str
    contract_status: str
    code_change_ready: str
    marker_ready: str
    blocker: str
    next_probe: str
    source_backing: str


@dataclass(frozen=True)
class UiTextRenderingStateContract:
    story_id: str
    upstream_ticket: str
    cluster: str
    status: str
    next_ticket: str
    source_taxonomy_family_count: int
    code_change_ready_count: int
    marker_ready_count: int
    contract_rows: tuple[ContractRow, ...]


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


def verify_re163_plan(repo: Path) -> None:
    ids = tuple(row.get("story_id", "") for row in read_csv(repo / RE163_PLAN_CSV))
    if ids != EXPECTED_PLAN_IDS:
        raise ValueError(f"RE-163 plan drifted before RE-166: {ids}")
    re166 = read_csv(repo / RE163_PLAN_CSV)[2]
    if re166.get("topic") != "ui-text-rendering-state-contract":
        raise ValueError("RE-163 plan no longer names RE-166 as the state contract")


def verify_re165_taxonomy(repo: Path) -> list[dict[str, str]]:
    rows = read_csv(repo / RE165_TAXONOMY_CSV)
    if len(rows) != EXPECTED_TAXONOMY_FAMILIES:
        raise ValueError(f"RE-165 taxonomy family count drifted: {len(rows)}")
    required = {"family_id", "callee", "proof_status", "patch_ready", "blocker", "state_fields", "visible_side_effects"}
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"RE-165 taxonomy missing columns: {sorted(missing)}")
    family_ids = tuple(row["family_id"] for row in rows)
    if family_ids != EXPECTED_RE165_FAMILY_IDS:
        raise ValueError(f"RE-165 taxonomy family/order drifted before RE-166: {family_ids}")
    for row in rows:
        if row["callee"] not in {"PrintString", "GetStringLength"}:
            raise ValueError(f"unexpected RE-165 callee: {row['callee']}")
        if row["proof_status"] != "argument-taxonomy-blocked-until-state-contract":
            raise ValueError("RE-165 proof status is not blocked until state contract")
        if row["patch_ready"] != "no":
            raise ValueError("RE-165 unexpectedly marked a taxonomy row patch-ready")
    print_rows = [row for row in rows if row["callee"] == "PrintString"]
    length_rows = [row for row in rows if row["callee"] == "GetStringLength"]
    print_state = ";".join(row["state_fields"] + ";" + row["visible_side_effects"] for row in print_rows)
    length_state = ";".join(row["state_fields"] + ";" + row["visible_side_effects"] for row in length_rows)
    for token in ("scale-flag-state", "glyph-draw-call", "font-scale-state", "draw-char-primitives"):
        if token not in print_state:
            raise ValueError(f"RE-165 PrintString taxonomy no longer supports RE-166 state token: {token}")
    for token in ("scale-flag-state", "font-definition-table", "accent-table", "optional-bounds-output"):
        if token not in length_state:
            raise ValueError(f"RE-165 GetStringLength taxonomy no longer supports RE-166 state token: {token}")
    return rows


def extract_function_body(source: str, function: str) -> str:
    match = re.search(rf"\b{re.escape(function)}\s*\([^;]*\)\s*(?://[^\n]*)?\n\{{", source)
    if not match:
        raise ValueError(f"function body not found: {function}")
    start = match.end() - 1
    depth = 0
    for index in range(start, len(source)):
        char = source[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[start:index + 1]
    raise ValueError(f"unterminated function body: {function}")


def require_tokens(bodies: dict[str, str], function: str, tokens: tuple[str, ...]) -> None:
    body = bodies[function]
    missing = [token for token in tokens if token not in body]
    if missing:
        raise ValueError(f"{function} missing expected state-contract tokens: {missing}")


def contract_specs() -> tuple[tuple[str, str, str, tuple[str, ...], str, str, str], ...]:
    return (
        (
            "ui-text-printstring-scale-flag-lifecycle", "PrintString", "scale-flag-state",
            ("ScaleFlag", "GetStringLength", "DrawChar"),
            "ScaleFlag is derived from the caller flag, shared with measurement and drawing, then cleared after rendering.",
            "RE-165 PrintString families with alignment and scale-related state fields.",
            "prove scale lifetime and per-call isolation before source or marker changes",
        ),
        (
            "ui-text-printstring-blink-frame-gate", "PrintString", "blink-frame-counter",
            ("GnFrameCounter", "return", "flag"),
            "Blink/composite flags can suppress visible rendering for a frame based on the global frame counter.",
            "RE-165 blink-or-composite flag families.",
            "prove frame counter timing and flag semantics in the comparison gate",
        ),
        (
            "ui-text-printstring-alignment-bounds-contract", "PrintString", "text-positioning-state",
            ("GetStringLength", "var_30", "var_2E", "var_2C"),
            "Initial and newline alignment depend on measured width plus optional top and bottom bounds.",
            "RE-165 center/right/no-alignment taxonomy families.",
            "prove alignment arithmetic and newline bounds state symbolically",
        ),
        (
            "ui-text-printstring-glyph-table-contract", "PrintString", "font-glyph-table-state",
            ("loc_92020", "word_9230E", "DrawChar"),
            "Rendering chooses glyph definitions from font tables and forwards them to DrawChar.",
            "RE-165 text-source families that reach glyph drawing.",
            "prove glyph table identity and special-control character handling",
        ),
        (
            "ui-text-getstringlength-scale-read-contract", "GetStringLength", "scale-flag-state",
            ("ScaleFlag", "t0", "a33->w"),
            "String measurement reads ScaleFlag and changes accumulated width for spaces and glyph metrics.",
            "RE-165 GetStringLength families and PrintString internal measurements.",
            "prove measurement uses the same scale state as rendering",
        ),
        (
            "ui-text-getstringlength-font-metric-contract", "GetStringLength", "font-metric-state",
            ("CharDef", "AccentTable", "YOffset", "h"),
            "String measurement derives width and vertical bounds from font and accent metric tables.",
            "RE-165 GetStringLength bounds families.",
            "prove font metric table identity and accent behavior",
        ),
        (
            "ui-text-getstringlength-bounds-output-contract", "GetStringLength", "optional-bounds-output",
            ("a1", "a2", "t1", "t2"),
            "Optional output pointers receive top and bottom bounds only when provided by the caller.",
            "RE-165 optional-bound and with-bounds families.",
            "prove nullable output pointer behavior before changing callers or markers",
        ),
        (
            "ui-text-getstringlength-control-character-contract", "GetStringLength", "control-character-state",
            ("c", "t0", "goto loc_8DF18"),
            "Spaces, tabs, newlines, and control characters alter measurement flow without emitting draw primitives.",
            "RE-165 GetStringLength caller-string and string-wad measurement families.",
            "prove control-character flow before equivalence readiness can rise",
        ),
        (
            "ui-text-drawchar-draw-buffer-contract", "DrawChar", "draw-buffer-state",
            ("db.polyptr", "db.polybuf_limit", "db.ot", "FontShades", "ScaleFlag"),
            "Glyph drawing consumes the shared draw buffer, ordering table, font shades, and scale state.",
            "RE-164 visible side effects and RE-165 PrintString glyph families.",
            "prove draw-buffer side effects and ordering-table insertion in the comparison gate",
        ),
    )


def build_contract_rows(repo: Path) -> tuple[ContractRow, ...]:
    source = (repo / TEXT_SOURCE).read_text(encoding="utf-8", errors="ignore")
    bodies = {name: extract_function_body(source, name) for name in ("PrintString", "GetStringLength", "DrawChar")}
    rows: list[ContractRow] = []
    for contract_id, function, state_surface, tokens, source_contract, proof_input, next_probe in contract_specs():
        require_tokens(bodies, function, tokens)
        rows.append(ContractRow(
            contract_id=contract_id,
            function=function,
            state_surface=state_surface,
            source_tokens=";".join(tokens),
            source_contract=source_contract,
            proof_input=proof_input,
            contract_status="contract-documented-equivalence-blocked",
            code_change_ready="no",
            marker_ready="no",
            blocker="missing-ui-text-rendering-non-raw-symbolic-equivalence-proof",
            next_probe=next_probe,
            source_backing="source-contract-only",
        ))
    return tuple(rows)


def build_ui_text_rendering_state_contract(repo: Path) -> UiTextRenderingStateContract:
    repo = Path(repo)
    verify_re163_plan(repo)
    taxonomy_rows = verify_re165_taxonomy(repo)
    contract_rows = build_contract_rows(repo)
    return UiTextRenderingStateContract(
        story_id="RE-166",
        upstream_ticket="RE-165",
        cluster="ui-text-rendering",
        status="state-contract-documented-equivalence-blocked",
        next_ticket="RE-167",
        source_taxonomy_family_count=len(taxonomy_rows),
        code_change_ready_count=0,
        marker_ready_count=0,
        contract_rows=contract_rows,
    )


def assert_clean(path: Path) -> None:
    text = path.read_text(encoding="utf-8").lower()
    hits = [item for item in FORBIDDEN_FRAGMENTS if item in text]
    if hits:
        raise ValueError(f"forbidden metadata fragments in {path}: {hits}")


def write_all_artifacts(audit: UiTextRenderingStateContract, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "contract_csv": repo / CONTRACT_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY_OUTPUT,
    }
    write_dict_csv(paths["contract_csv"], list(ContractRow.__dataclass_fields__), [row.__dict__ for row in audit.contract_rows])

    md_lines = [
        "# RE-166 — UI text rendering state contract",
        "",
        "Cluster: `ui-text-rendering`",
        "Decision: `state-contract-documented-equivalence-blocked`",
        "Next: `RE-167`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-165 taxonomy consumed.",
        "- [x] UI text state contract emitted.",
        "- [x] Source-backed contract surfaces recorded.",
        "- [x] Patch and marker readiness kept blocked.",
        "",
        "## Summary",
        "",
        f"- taxonomy families consumed: `{audit.source_taxonomy_family_count}`",
        f"- state contract rows: `{len(audit.contract_rows)}`",
        "- source patch authorized: `no`",
        "",
        "## Contract rows",
        "",
    ]
    for row in audit.contract_rows:
        md_lines.append(f"- `{row.contract_id}`: `{row.function}` surface `{row.state_surface}` status `{row.contract_status}` readiness `{row.code_change_ready}`")
    md_lines.extend([
        "",
        "No production source or marker change is authorized by this state contract.",
    ])
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    story_lines = [
        "# RE-166 — UI text rendering state contract",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Document source-backed state contracts for `PrintString`, `GetStringLength`, and `DrawChar` before the non-raw equivalence gate.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-165 taxonomy consumed.",
        "- [x] UI text state contract emitted.",
        "- [x] Draw-buffer, font, string, flag, bounds, and scale surfaces classified.",
        "- [x] Forbidden evidence excluded from generated artifacts.",
        "",
        "## Generated artifacts",
        "",
        f"- `{CONTRACT_CSV}`",
        f"- `{MD_OUTPUT}`",
        "",
        "## Readiness decision",
        "",
        "- decision: `state-contract-documented-equivalence-blocked`",
        "- code change readiness: `blocked`",
        "- marker readiness: `blocked`",
        "- next ticket: `RE-167`",
        "- blocker: `missing-ui-text-rendering-non-raw-symbolic-equivalence-proof`",
        "",
        "## Follow-up breakdown",
        "",
        "- `RE-167`: compare these source-backed contracts against non-raw symbolic evidence and emit readiness rows.",
        "- `RE-168`: only consider source or marker changes if RE-167 marks rows ready.",
        "- `RE-169`: select the next SPEC_PSXPC_N cluster after this UI text rendering chain closes or blocks.",
        "",
        "## Validation",
        "",
        "- `python3 -m pytest tests/reverse/test_re166_ui_text_rendering_state_contract.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over RE-166 artifacts",
        "",
        "No production source or marker change is authorized by this state contract.",
        "",
    ]
    paths["story"].parent.mkdir(parents=True, exist_ok=True)
    paths["story"].write_text("\n".join(story_lines), encoding="utf-8")

    for path in paths.values():
        assert_clean(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    audit = build_ui_text_rendering_state_contract(args.repo)
    for key, path in write_all_artifacts(audit, args.repo).items():
        print(f"{key}: {path}")
    print(f"state_contract_rows={len(audit.contract_rows)}")
    print(f"next_ticket={audit.next_ticket}")


if __name__ == "__main__":
    main()
