import csv
import subprocess
import sys
from pathlib import Path


def test_re701_emits_metadata_only_blocked_function_identity_rows(tmp_path):
    from scripts.reverse.re701_unimplemented_source_function_identity_export import (
        FORBIDDEN,
        build_export,
        write_artifacts,
    )

    repo = Path(__file__).resolve().parents[2]
    export = build_export(repo)

    assert export.source_file_count > 0
    assert export.function_row_count > 0
    assert export.unimplemented_marker_count > 0
    assert export.patch_ready_count == 0
    assert export.rows == tuple(sorted(export.rows, key=lambda row: (row.source_file, row.repo_function)))
    assert sum(row.unimplemented_marker_count for row in export.rows) == export.unimplemented_marker_count
    assert all(row.source_behavior_proof_count == 0 for row in export.rows)
    assert all(row.code_change_readiness == "blocked" for row in export.rows)

    written = write_artifacts(export, tmp_path)
    rows = list(csv.DictReader(written["identity_csv"].open(newline="", encoding="utf-8")))
    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))

    assert len(rows) == export.function_row_count
    assert sum(int(row["unimplemented_marker_count"]) for row in rows) == export.unimplemented_marker_count
    assert handoff == [
        {
            "story_id": "RE-701",
            "topic": "unimplemented-source-function-identity-export",
            "predecessor": "RE-700",
            "source_file_count": str(export.source_file_count),
            "function_row_count": str(export.function_row_count),
            "unimplemented_marker_count": str(export.unimplemented_marker_count),
            "source_behavior_proof_count": "0",
            "source_patch_authorized_count": "0",
            "selected_domain": "none",
            "selected_pivot": "none",
            "code_change_readiness": "blocked",
            "next_ticket": "RE-702",
            "next_topic": "unimplemented-source-behavior-contract-gate",
            "stop_condition": "a source-backed behavioral contract and ABI proof are required before selecting any implementation unit",
        }
    ]
    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text


def test_re701_rejects_every_re700_handoff_field_drift(tmp_path):
    from scripts.reverse.re701_unimplemented_source_function_identity_export import build_export

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    upstream = generated / "re700-unimplemented-source-callsite-proof-intake-handoff.csv"
    upstream.write_text(
        (source / "docs/reverse/generated/re700-unimplemented-source-callsite-proof-intake-handoff.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    source_file = tmp_path / "GAME/TEST.C"
    source_file.parent.mkdir(parents=True)
    source_file.write_text("void example(void) { UNIMPLEMENTED(); }\n", encoding="utf-8")

    with upstream.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        values = next(reader)
    assert fields is not None
    for field in fields:
        mutated = values.copy()
        mutated[field] = "drift"
        with upstream.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerow(mutated)
        try:
            build_export(tmp_path)
        except ValueError as error:
            assert field in str(error)
        else:
            raise AssertionError(f"RE-701 must reject RE-700 handoff drift in {field}")


def test_re701_rejects_re700_handoff_schema_and_row_count_drift(tmp_path):
    from scripts.reverse.re701_unimplemented_source_function_identity_export import build_export

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    upstream = generated / "re700-unimplemented-source-callsite-proof-intake-handoff.csv"
    baseline = (source / "docs/reverse/generated/re700-unimplemented-source-callsite-proof-intake-handoff.csv").read_text(encoding="utf-8")
    source_file = tmp_path / "GAME/TEST.C"
    source_file.parent.mkdir(parents=True)
    source_file.write_text("void example(void) { UNIMPLEMENTED(); }\n", encoding="utf-8")

    upstream.write_text(baseline.rstrip() + ",unexpected\n", encoding="utf-8")
    try:
        build_export(tmp_path)
    except ValueError as error:
        assert "schema" in str(error)
    else:
        raise AssertionError("RE-701 must reject an extra RE-700 handoff data cell")

    upstream.write_text(baseline + baseline.splitlines()[1] + "\n", encoding="utf-8")
    try:
        build_export(tmp_path)
    except ValueError as error:
        assert "row-count" in str(error)
    else:
        raise AssertionError("RE-701 must reject an extra RE-700 handoff row")


def test_re701_groups_active_markers_by_enclosing_function_and_ignores_non_code(tmp_path):
    from scripts.reverse.re701_unimplemented_source_function_identity_export import build_export

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    (generated / "re700-unimplemented-source-callsite-proof-intake-handoff.csv").write_text(
        (source / "docs/reverse/generated/re700-unimplemented-source-callsite-proof-intake-handoff.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    game = tmp_path / "GAME"
    game.mkdir()
    (game / "TEST.C").write_text(
        "#define PLACEHOLDER UNIMPLEMENTED();\n"
        "// UNIMPLEMENTED();\n"
        "void alpha(void) { UNIMPLEMENTED(); }\n"
        "int beta(int value) {\n"
        "  const char *text = \"UNIMPLEMENTED();\";\n"
        "  if (value) { UNIMPLEMENTED(); }\n"
        "  return value;\n"
        "}\n"
        "#if 0\nvoid inactive(void) { UNIMPLEMENTED(); }\n#endif\n",
        encoding="utf-8",
    )

    export = build_export(tmp_path)

    assert [(row.source_file, row.repo_function, row.unimplemented_marker_count) for row in export.rows] == [
        ("GAME/TEST.C", "alpha", 1),
        ("GAME/TEST.C", "beta", 1),
    ]


def test_re701_runs_directly_as_a_repo_script():
    repo = Path(__file__).resolve().parents[2]

    completed = subprocess.run(
        [sys.executable, "scripts/reverse/re701_unimplemented_source_function_identity_export.py"],
        cwd=repo,
        text=True,
        capture_output=True,
    )

    assert completed.returncode == 0, completed.stderr
