from pathlib import Path
import csv

from scripts.reverse.re162_post_module_game_reprioritization import (
    FORBIDDEN,
    build_reprioritization,
    write_all_artifacts,
)


def test_re162_consumes_module_game_exhaustion_and_selects_next_domain():
    repo = Path(__file__).resolve().parents[2]
    plan = build_reprioritization(repo)

    assert plan.story_id == "RE-162"
    assert plan.upstream_ticket == "RE-161"
    assert plan.upstream_status == "module-game-exhausted"
    assert plan.status == "post-module-game-domain-reprioritization-ready"
    assert plan.next_ticket == "RE-163"
    assert plan.code_change_readiness == "documentation-only-selection-gate"
    assert plan.selected_domain == "module-spec_psxpc_n"
    assert plan.selected_pivot == "PrintString"

    source_rows = list(csv.DictReader((repo / "docs/reverse/generated/re044-domain-reprioritization.csv").open(newline="", encoding="utf-8")))
    closed_domains = {"audio-effects", "collision", "module-game"}
    assert len(plan.rows) == sum(1 for row in source_rows if row["domain_id"] not in closed_domains)

    domain_ids = [row.domain_id for row in plan.rows]
    assert domain_ids[0] == "module-spec_psxpc_n"
    assert "maths-render-support" in domain_ids
    assert "traps-switches-doors" in domain_ids
    assert "module-spec_psxpc" in domain_ids
    assert "module-spec_psx" in domain_ids
    assert "audio-effects" not in domain_ids
    assert "collision" not in domain_ids
    assert "module-game" not in domain_ids

    top = plan.rows[0]
    assert top.rank == 1
    assert top.next_action == "open RE-163 module-spec_psxpc_n proof-first audit"
    assert top.code_change_readiness == "blocked"
    assert top.rationale.startswith("next-ranked domain after module-game exhaustion")


def test_re162_outputs_metadata_only_artifacts_and_progress_tracker(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    plan = build_reprioritization(repo)
    written = write_all_artifacts(plan, tmp_path)

    assert written["csv"].name == "re162-post-module-game-domain-reprioritization.csv"
    assert written["md"].name == "re162-post-module-game-domain-reprioritization.md"
    assert written["story"].name == "RE-162-post-module-game-domain-reprioritization.md"

    rows = list(csv.DictReader(written["csv"].open(newline="", encoding="utf-8")))
    assert rows[0]["domain_id"] == "module-spec_psxpc_n"
    assert rows[0]["top_function"] == "PrintString"
    assert rows[0]["next_ticket"] == "RE-163"
    assert rows[0]["code_change_readiness"] == "blocked"

    story_text = written["story"].read_text(encoding="utf-8")
    assert "# RE-162 — Post-module-game domain reprioritization" in story_text
    assert "Status: Done" in story_text
    assert "## Progress tracker" in story_text
    assert "RE-161 module-game exhaustion handoff consumed" in story_text
    assert "Closed domains excluded" in story_text
    assert "Recommended next ticket: `RE-163`" in story_text
    assert "No production source or marker change is authorized" in story_text

    md_text = written["md"].read_text(encoding="utf-8")
    assert "Selected next domain: `module-spec_psxpc_n`" in md_text
    assert "Selected pivot: `PrintString`" in md_text
    assert "RE-163" in md_text

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text
