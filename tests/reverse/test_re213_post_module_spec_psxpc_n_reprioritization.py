from pathlib import Path
import csv

from scripts.reverse.re213_post_module_spec_psxpc_n_reprioritization import (
    CLOSED_DOMAINS,
    FORBIDDEN,
    STALE_FRAGMENTS,
    build_reprioritization,
    write_all_artifacts,
)


def test_re213_consumes_module_spec_psxpc_n_exhaustion_and_selects_maths_render_support():
    repo = Path(__file__).resolve().parents[2]
    plan = build_reprioritization(repo)

    assert plan.story_id == "RE-213"
    assert plan.upstream_ticket == "RE-212"
    assert plan.upstream_status == "module-spec-psxpc-n-exhausted"
    assert plan.status == "post-module-spec-psxpc-n-domain-selection-ready"
    assert plan.next_ticket == "RE-214"
    assert plan.code_change_readiness == "documentation-only-selection-gate"
    assert plan.selected_domain == "maths-render-support"
    assert plan.selected_pivot == "mTranslateXYZ"
    assert plan.excluded_domains == tuple(sorted(CLOSED_DOMAINS))

    source_rows = list(csv.DictReader((repo / "docs/reverse/generated/re162-post-module-game-domain-reprioritization.csv").open(newline="", encoding="utf-8")))
    assert len(plan.rows) == sum(1 for row in source_rows if row["domain_id"] not in CLOSED_DOMAINS)

    domain_ids = [row.domain_id for row in plan.rows]
    assert domain_ids == [
        "maths-render-support",
        "traps-switches-doors",
        "module-spec_psxpc",
        "module-spec_psx",
        "lara-combat",
        "inventory",
        "input",
        "camera",
    ]
    assert "module-spec_psxpc_n" not in domain_ids

    top = plan.rows[0]
    assert top.rank == 1
    assert top.score == 22930
    assert top.candidate_count == 92
    assert top.mapped_count == 92
    assert top.nd_count == 4
    assert top.runtime_count == 0
    assert top.top_function == "mTranslateXYZ"
    assert top.top_file == "SPEC_PSXPC_N/MATHS.C"
    assert top.next_action == "open RE-214 maths-render-support proof-first audit"
    assert top.next_ticket == "RE-214"
    assert top.rationale.startswith("next-ranked domain after module-spec_psxpc_n exhaustion")
    assert all(row.code_change_readiness == "blocked" for row in plan.rows)


def test_re213_outputs_metadata_only_artifacts_and_progress_tracker(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    plan = build_reprioritization(repo)
    written = write_all_artifacts(plan, tmp_path)

    assert written["csv"].name == "re213-post-module-spec-psxpc-n-domain-selection.csv"
    assert written["md"].name == "re213-post-module-spec-psxpc-n-domain-selection.md"
    assert written["story"].name == "RE-213-post-module-spec-psxpc-n-domain-selection.md"
    assert written["handoff"].name == "re213-post-module-spec-psxpc-n-domain-selection-handoff.csv"

    rows = list(csv.DictReader(written["csv"].open(newline="", encoding="utf-8")))
    assert rows[0]["domain_id"] == "maths-render-support"
    assert rows[0]["top_function"] == "mTranslateXYZ"
    assert rows[0]["next_ticket"] == "RE-214"
    assert rows[0]["next_action"] == "open RE-214 maths-render-support proof-first audit"
    assert rows[0]["code_change_readiness"] == "blocked"

    handoff = list(csv.DictReader(written["handoff"].open(newline="", encoding="utf-8")))[0]
    assert handoff["next_ticket"] == "RE-214"
    assert handoff["next_topic"] == "maths-render-support-proof-first-audit"
    assert handoff["selected_domain"] == "maths-render-support"
    assert handoff["selected_pivot"] == "mTranslateXYZ"
    assert handoff["code_change_readiness"] == "blocked"

    story_text = written["story"].read_text(encoding="utf-8")
    assert "# RE-213 — Post-module-spec_psxpc_n domain selection" in story_text
    assert "Status: Done" in story_text
    assert "## Progress tracker" in story_text
    assert "RE-212 module-spec_psxpc_n exhaustion handoff consumed" in story_text
    assert "Closed/exhausted domains excluded" in story_text
    assert "Recommended next ticket: `RE-214`" in story_text
    assert "No production source or marker change is authorized" in story_text

    md_text = written["md"].read_text(encoding="utf-8")
    assert "Selected next domain: `maths-render-support`" in md_text
    assert "Selected pivot: `mTranslateXYZ`" in md_text
    assert "RE-214" in md_text
    assert "defer until higher-ranked post-module-spec_psxpc_n domain is selected" in md_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN + STALE_FRAGMENTS:
            assert fragment not in text
