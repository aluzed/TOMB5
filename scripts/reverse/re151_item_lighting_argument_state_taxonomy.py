#!/usr/bin/env python3
"""Generate RE-151 item-lighting interaction argument/state taxonomy artifacts."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

RE149_PLAN_CSV = "docs/reverse/generated/re149-item-lighting-interaction-ticket-plan.csv"
RE150_CALLSITE_CSV = "docs/reverse/generated/re150-item-lighting-interaction-callsite-map.csv"
RE150_SCOPE_CSV = "docs/reverse/generated/re150-item-lighting-interaction-scope.csv"
TAXONOMY_CSV = "docs/reverse/generated/re151-item-lighting-interaction-argument-state-taxonomy.csv"
MD_OUTPUT = "docs/reverse/functions/re151-item-lighting-interaction-argument-state-taxonomy.md"
STORY_OUTPUT = "docs/stories/RE-151-item-lighting-interaction-argument-state-taxonomy.md"
FORBIDDEN_FRAGMENTS = ("0x", "payload", "opcode", "machine word", "raw call target")
EXPECTED_PLAN = ("RE-150", "RE-151", "RE-152", "RE-153", "RE-154", "RE-155", "RE-156")
EXPECTED_SHAPES = (
    "shape-item-lighting-alert-light-parameters",
    "shape-item-lighting-void-torch-update",
)


@dataclass(frozen=True)
class TaxonomyRow:
    shape_id: str
    site_count: int
    callees: str
    argument_kinds: str
    state_fields: str
    side_effects: str
    source_backed: str
    patch_ready: str
    blocker: str
    next_probe: str


@dataclass(frozen=True)
class ItemLightingArgumentStateTaxonomy:
    story_id: str
    upstream_ticket: str
    cluster: str
    status: str
    next_ticket: str
    code_change_ready_count: int
    marker_ready_count: int
    rows: tuple[TaxonomyRow, ...]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def verify_inputs(repo: Path) -> None:
    plan_ids = tuple(row.get("story_id", "") for row in read_csv(repo / RE149_PLAN_CSV))
    if plan_ids != EXPECTED_PLAN:
        raise ValueError("RE-149 plan no longer matches RE-150..RE-156 expectations")
    scope_functions = tuple(row.get("function", "") for row in read_csv(repo / RE150_SCOPE_CSV))
    if scope_functions != ("DoFlameTorch", "TriggerAlertLight"):
        raise ValueError(f"RE-150 scope drifted before RE-151 taxonomy: {scope_functions}")


def split_fields(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def canonical_argument_kinds(shape_id: str, group: list[dict[str, str]]) -> str:
    if shape_id == "shape-item-lighting-alert-light-parameters":
        return "position-color-room-arguments"
    if shape_id == "shape-item-lighting-void-torch-update":
        return "void"
    return ";".join(sorted({row["argument_kinds"] for row in group if row["argument_kinds"]}))


def canonical_state_fields(shape_id: str, group: list[dict[str, str]]) -> str:
    fields = {field for row in group for field in split_fields(row["state_fields"])}
    effects = {field for row in group for field in split_fields(row["side_effects"])}
    fields |= effects
    if shape_id == "shape-item-lighting-alert-light-parameters":
        fields |= {"alert-light-state", "dynamic-light-state", "room-light-state"}
    if shape_id == "shape-item-lighting-void-torch-update":
        fields |= {"torch-item-state", "lara-torch-state"}
    return ";".join(sorted(fields))


def build_rows(repo: Path) -> tuple[TaxonomyRow, ...]:
    callsites = read_csv(repo / RE150_CALLSITE_CSV)
    if not callsites:
        raise ValueError("RE-150 callsite map is empty")
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in callsites:
        if row.get("line") in {"", "0"}:
            raise ValueError(f"RE-151 refuses non-source-backed callsite row: {row}")
        if row.get("proof_status") != "source-callsite-mapped-only" or row.get("patch_ready") != "no":
            raise ValueError(f"RE-151 refuses drifted RE-150 readiness row: {row}")
        grouped.setdefault(row["shape_id"], []).append(row)
    if tuple(sorted(grouped)) != EXPECTED_SHAPES:
        raise ValueError(f"RE-151 shape set drifted: {tuple(sorted(grouped))}")
    rows: list[TaxonomyRow] = []
    for shape_id in EXPECTED_SHAPES:
        group = grouped[shape_id]
        callees = ";".join(sorted({row["callee"] for row in group}))
        arg_kinds = canonical_argument_kinds(shape_id, group)
        state_fields = canonical_state_fields(shape_id, group)
        side_effects = ";".join(sorted({field for row in group for field in split_fields(row["side_effects"])}))
        rows.append(TaxonomyRow(
            shape_id=shape_id,
            site_count=len(group),
            callees=callees,
            argument_kinds=arg_kinds,
            state_fields=state_fields,
            side_effects=side_effects,
            source_backed="source-callsite-only",
            patch_ready="no",
            blocker="missing-item-lighting-state-contract-and-symbolic-equivalence-proof",
            next_probe="RE-152 item-lighting comparison gate",
        ))
    return tuple(rows)


def build_item_lighting_argument_state_taxonomy(repo: Path) -> ItemLightingArgumentStateTaxonomy:
    repo = Path(repo)
    verify_inputs(repo)
    rows = build_rows(repo)
    return ItemLightingArgumentStateTaxonomy(
        story_id="RE-151",
        upstream_ticket="RE-150",
        cluster="item-lighting-interaction",
        status="argument-state-taxonomy-blocked",
        next_ticket="RE-152",
        code_change_ready_count=0,
        marker_ready_count=0,
        rows=rows,
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


def write_all_artifacts(taxonomy: ItemLightingArgumentStateTaxonomy, repo: Path) -> dict[str, Path]:
    repo = Path(repo)
    paths = {
        "taxonomy_csv": repo / TAXONOMY_CSV,
        "md": repo / MD_OUTPUT,
        "story": repo / STORY_OUTPUT,
    }
    write_dict_csv(paths["taxonomy_csv"], list(TaxonomyRow.__dataclass_fields__), [row.__dict__ for row in taxonomy.rows])

    md = [
        "# RE-151 — Item lighting interaction argument and state taxonomy",
        "",
        "Cluster: `item-lighting-interaction`",
        "Decision: `argument-state-taxonomy-blocked`",
        "Next: `RE-152`",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-150 callsite map consumed.",
        "- [x] Argument and state taxonomy emitted.",
        "- [x] Alert-light source call arguments canonicalized to position/color/room taxonomy.",
        "- [x] Patch and marker readiness kept blocked.",
        "",
        "## Findings",
        "",
    ]
    for row in taxonomy.rows:
        md.append(f"- `{row.shape_id}` — callees `{row.callees}`; arguments `{row.argument_kinds}`; state `{row.state_fields}`; patch `{row.patch_ready}`")
    md.extend(["", "No production source or marker change is authorized by this taxonomy."])
    paths["md"].parent.mkdir(parents=True, exist_ok=True)
    paths["md"].write_text("\n".join(md) + "\n", encoding="utf-8")

    story = [
        "# RE-151 — Item lighting interaction argument and state taxonomy",
        "",
        "Status: Done",
        "",
        "## Goal",
        "",
        "Classify item-lighting argument shapes, state fields, and side-effect surfaces from the source-backed RE-150 callsite map.",
        "",
        "## Progress tracker",
        "",
        "- [x] RE-150 callsite map consumed.",
        "- [x] Argument and state taxonomy emitted.",
        "- [x] State and side-effect labels consolidated.",
        "- [x] Forbidden evidence excluded from generated artifacts.",
        "",
        "## Generated artifacts",
        "",
        f"- `{TAXONOMY_CSV}`",
        f"- `{MD_OUTPUT}`",
        "",
        "## Readiness decision",
        "",
        "- decision: `argument-state-taxonomy-blocked`",
        "- code change readiness: `blocked`",
        "- marker readiness: `blocked`",
        "- next ticket: `RE-152`",
        "- blocker: `missing-item-lighting-state-contract-and-symbolic-equivalence-proof`",
        "",
        "## Validation",
        "",
        "- `python3 -m pytest tests/reverse/test_re151_item_lighting_argument_state_taxonomy.py -q`",
        "- `python3 -m pytest tests/reverse -q`",
        "- metadata-only guard over RE-151 artifacts",
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
    taxonomy = build_item_lighting_argument_state_taxonomy(args.repo)
    for key, path in write_all_artifacts(taxonomy, args.repo).items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
