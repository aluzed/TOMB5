#!/usr/bin/env python3
"""Generate RE-165 UI text rendering argument taxonomy artifacts."""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

RE163_PLAN_CSV = "docs/reverse/generated/re163-module-spec-psxpc-n-ticket-plan.csv"
RE164_CALLSITE_CSV = "docs/reverse/generated/re164-ui-text-rendering-callsite-map.csv"
RE164_SCOPE_CSV = "docs/reverse/generated/re164-ui-text-rendering-scope.csv"
TAXONOMY_CSV = "docs/reverse/generated/re165-ui-text-rendering-argument-taxonomy.csv"
MD_OUTPUT = "docs/reverse/functions/re165-ui-text-rendering-argument-taxonomy.md"
STORY_OUTPUT = "docs/stories/RE-165-ui-text-rendering-argument-taxonomy.md"

FORBIDDEN_FRAGMENTS = ("0x", "pay" + "load", "op" + "code", "machine" + " word", "raw" + " call target")
REQUIRED_CALLSITE_COLUMNS = {
    "caller", "callee", "caller_file", "callee_file", "line", "shape_id", "arg_count",
    "coordinate_source", "colour_source", "text_source", "flag_source", "state_fields",
    "visible_side_effects", "proof_status", "patch_ready", "blocker",
}
ORDER = {"PrintString": 0, "GetStringLength": 1}


@dataclass(frozen=True)
class TaxonomyRow:
    family_id: str
    callee: str
    argument_shape: str
    callsite_count: int
    coordinate_family: str
    colour_family: str
    text_family: str
    flag_family: str
    state_fields: str
    visible_side_effects: str
    source_backing: str
    proof_status: str
    patch_ready: str
    blocker: str
    next_probe: str


@dataclass(frozen=True)
class UiTextRenderingArgumentTaxonomy:
    story_id: str
    upstream_ticket: str
    cluster: str
    status: str
    next_ticket: str
    source_callsite_count: int
    code_change_ready_count: int
    marker_ready_count: int
    taxonomy_rows: tuple[TaxonomyRow, ...]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def verify_re163_plan(repo: Path) -> None:
    rows = read_csv(repo / RE163_PLAN_CSV)
    ids = tuple(row.get("story_id", "") for row in rows)
    expected = ("RE-164", "RE-165", "RE-166", "RE-167", "RE-168", "RE-169", "RE-170")
    if ids != expected:
        raise ValueError("RE-163 plan no longer matches RE-164..RE-170 expectations")
    re165 = rows[1]
    if re165.get("topic") != "ui-text-rendering-argument-taxonomy":
        raise ValueError("RE-163 second follow-up is no longer the RE-165 taxonomy")


def verify_re164_scope(repo: Path) -> None:
    rows = read_csv(repo / RE164_SCOPE_CSV)
    functions = tuple(row.get("function", "") for row in rows)
    if functions != ("PrintString", "GetStringLength"):
        raise ValueError(f"RE-164 scope drifted: {functions}")
    for row in rows:
        if row.get("patch_ready") != "no" or "state-contract" not in row.get("blocker", ""):
            raise ValueError("RE-164 scope readiness is not blocked as expected")


def load_verified_callsites(repo: Path) -> list[dict[str, str]]:
    rows = read_csv(repo / RE164_CALLSITE_CSV)
    if not rows:
        raise ValueError("RE-164 callsite map is empty")
    missing = REQUIRED_CALLSITE_COLUMNS - set(rows[0])
    if missing:
        raise ValueError(f"RE-164 callsite map missing columns: {sorted(missing)}")
    for row in rows:
        if row["callee"] not in {"PrintString", "GetStringLength"}:
            raise ValueError(f"unexpected callee in RE-164 callsite map: {row['callee']}")
        if row["proof_status"] != "source-callsite-mapped-only":
            raise ValueError("RE-164 proof status is not source-callsite-mapped-only")
        if row["patch_ready"] != "no":
            raise ValueError("RE-164 unexpectedly marked a callsite patch-ready")
        line = int(row["line"])
        if line <= 0:
            raise ValueError("RE-164 callsite row is not source-backed")
        source_line = (repo / row["caller_file"]).read_text(encoding="utf-8", errors="ignore").splitlines()[line - 1]
        if row["callee"] not in source_line:
            raise ValueError("RE-164 callsite row does not point at a source callee occurrence")
    return rows


def slug(value: str) -> str:
    value = value.lower().replace("getstringlength", "getstringlength").replace("printstring", "printstring")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value


def short_coordinate(value: str) -> str:
    mapping = {
        "screen-centered-or-absolute": "screen-centered",
        "caller-layout-derived": "caller-layout",
        "literal-or-expression-coordinate": "literal-coordinate",
    }
    return mapping.get(value, slug(value))


def short_colour(value: str) -> str:
    mapping = {
        "literal-colour-index": "literal-colour",
        "request-colour-field": "request-colour",
        "expression-colour": "expression-colour",
    }
    return mapping.get(value, slug(value))


def short_text(value: str) -> str:
    mapping = {
        "string-wad-offset": "string-wad",
        "formatted-buffer": "formatted-buffer",
        "inline-control-string": "inline-control-string",
        "caller-string-pointer": "caller-string",
        "source-expression": "source-expression",
    }
    return mapping.get(value, slug(value))


def short_flag(value: str) -> str:
    mapping = {
        "center-alignment-flags": "center",
        "right-alignment-flags": "right",
        "no-alignment-flags": "none",
        "blink-or-composite-flags": "blink-composite",
        "caller-provided-flags": "caller-provided",
        "literal-or-composite-flags": "literal-composite",
        "not-applicable": "not-applicable",
    }
    return mapping.get(value, slug(value))


def family_id_for(row: dict[str, str]) -> str:
    if row["callee"] == "PrintString":
        return "ui-text-printstring-{}-{}-{}-{}".format(
            short_coordinate(row["coordinate_source"]),
            short_colour(row["colour_source"]),
            short_text(row["text_source"]),
            short_flag(row["flag_source"]),
        )
    if row["callee"] == "GetStringLength":
        # Canonicalize required-bounds length calls together: the RE-166 state
        # contract must prove the bounds-output side effect regardless of
        # whether the string pointer came directly from a caller or a WAD slot.
        # Optional-bound calls remain split by source because only one WAD-slot
        # callsite exercises that narrower argument path.
        if row["shape_id"].endswith("with-bounds"):
            return "ui-text-getstringlength-caller-string-with-bounds"
        return "ui-text-getstringlength-{}-optional-bound".format(short_text(row["text_source"]))
    return f"ui-text-{slug(row['callee'])}-{slug(row['shape_id'])}"


def next_probe_for(callee: str) -> str:
    if callee == "PrintString":
        return "RE-166 font/draw-buffer/string-table state contract"
    return "RE-166 font-metric and ScaleFlag state contract"


def canonical_dimension(items: list[dict[str, str]], key: str) -> str:
    values = list(dict.fromkeys(row[key] for row in items))
    if len(values) == 1:
        return values[0]
    if key == "text_source" and set(values) == {"caller-string-pointer", "string-wad-offset"}:
        return "caller-string-or-string-wad"
    return ";".join(values)


def build_taxonomy_rows(callsites: list[dict[str, str]]) -> tuple[TaxonomyRow, ...]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in callsites:
        groups[family_id_for(row)].append(row)

    rows: list[TaxonomyRow] = []
    for family_id, items in groups.items():
        first = items[0]
        state_fields = list(dict.fromkeys(part for row in items for part in row["state_fields"].split(";") if part))
        side_effects = list(dict.fromkeys(part for row in items for part in row["visible_side_effects"].split(";") if part))
        shape_ids = list(dict.fromkeys(row["shape_id"] for row in items))
        rows.append(TaxonomyRow(
            family_id=family_id,
            callee=first["callee"],
            argument_shape=";".join(shape_ids),
            callsite_count=len(items),
            coordinate_family=canonical_dimension(items, "coordinate_source"),
            colour_family=canonical_dimension(items, "colour_source"),
            text_family=canonical_dimension(items, "text_source"),
            flag_family=canonical_dimension(items, "flag_source"),
            state_fields=";".join(state_fields),
            visible_side_effects=";".join(side_effects),
            source_backing="source-callsite-only",
            proof_status="argument-taxonomy-blocked-until-state-contract",
            patch_ready="no",
            blocker="missing-ui-text-rendering-state-contract-and-symbolic-equivalence-proof",
            next_probe=next_probe_for(first["callee"]),
        ))
    rows.sort(key=lambda row: (ORDER.get(row.callee, 99), row.callee, row.family_id))
    return tuple(rows)


def build_ui_text_rendering_argument_taxonomy(repo: Path) -> UiTextRenderingArgumentTaxonomy:
    repo = Path(repo)
    verify_re163_plan(repo)
    verify_re164_scope(repo)
    callsites = load_verified_callsites(repo)
    taxonomy_rows = build_taxonomy_rows(callsites)
    return UiTextRenderingArgumentTaxonomy(
        story_id="RE-165",
        upstream_ticket="RE-164",
        cluster="ui-text-rendering",
        status="argument-taxonomy-blocked",
        next_ticket="RE-166",
        source_callsite_count=len(callsites),
        code_change_ready_count=0,
        marker_ready_count=0,
        taxonomy_rows=taxonomy_rows,
    )


def write_dict_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def assert_clean(path: Path) -> None:
    text = path.read_text(encoding="utf-8").lower()
    hits = [item for item in FORBIDDEN_FRAGMENTS if item in text]
    if hits:
        raise ValueError(f"forbidden metadata fragments in {path}: {hits}")


def write_all_artifacts(audit: UiTextRenderingArgumentTaxonomy, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "taxonomy_csv": repo / TAXONOMY_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY_OUTPUT,
    }
    write_dict_csv(paths["taxonomy_csv"], list(TaxonomyRow.__dataclass_fields__), [row.__dict__ for row in audit.taxonomy_rows])

    md = [
        "# RE-165 — UI text rendering argument taxonomy",
        "",
        "Cluster: `ui-text-rendering`",
        "Decision: `argument-taxonomy-blocked`",
        "Next: `RE-166`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-164 callsite map consumed.",
        "- [x] UI text argument taxonomy emitted.",
        "- [x] Upstream source-backed readiness propagated fail-closed.",
        "- [x] Patch and marker readiness kept blocked.",
        "",
        "## Summary",
        "",
        f"- source-backed callsites consumed: `{audit.source_callsite_count}`",
        f"- taxonomy families: `{len(audit.taxonomy_rows)}`",
        "- source patch authorized: `no`",
        "",
        "## Families",
        "",
    ]
    for row in audit.taxonomy_rows:
        md.append(f"- `{row.family_id}`: `{row.callee}` count `{row.callsite_count}` text `{row.text_family}` flag `{row.flag_family}` patch `{row.patch_ready}`")
    md.extend(["", "No production source or marker change is authorized by this taxonomy."])
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text("\n".join(md) + "\n", encoding="utf-8")

    story = [
        "# RE-165 — UI text rendering argument taxonomy",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Classify the `PrintString` and `GetStringLength` callsite families from RE-164 into stable metadata categories without authorizing source or marker changes.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-164 callsite map consumed.",
        "- [x] UI text argument taxonomy emitted.",
        "- [x] Source-backed callsite-only proof propagated.",
        "- [x] Forbidden evidence excluded from generated artifacts.",
        "",
        "## Generated artifacts",
        "",
        f"- `{TAXONOMY_CSV}`",
        f"- `{MD_OUTPUT}`",
        "",
        "## Readiness decision",
        "",
        "- decision: `argument-taxonomy-blocked`",
        "- code change readiness: `blocked`",
        "- marker readiness: `blocked`",
        "- next ticket: `RE-166`",
        "- blocker: `missing-ui-text-rendering-state-contract-and-symbolic-equivalence-proof`",
        "",
        "## Follow-up breakdown",
        "",
        "- `RE-166`: document font buffers, string tables, scale state, draw queues, and bounds-output contracts.",
        "- `RE-167`: use the state contract to run the non-raw equivalence/readiness gate.",
        "- `RE-168`: only consider source or marker changes if RE-167 marks rows ready.",
        "",
        "## Validation",
        "",
        "- `python3 -m pytest tests/reverse/test_re165_ui_text_rendering_argument_taxonomy.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over RE-165 artifacts",
        "",
    ]
    paths["story"].parent.mkdir(parents=True, exist_ok=True)
    paths["story"].write_text("\n".join(story), encoding="utf-8")

    for path in paths.values():
        assert_clean(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    audit = build_ui_text_rendering_argument_taxonomy(args.repo)
    for key, path in write_all_artifacts(audit, args.repo).items():
        print(f"{key}: {path}")
    print(f"taxonomy_families={len(audit.taxonomy_rows)}")
    print(f"next_ticket={audit.next_ticket}")


if __name__ == "__main__":
    main()
