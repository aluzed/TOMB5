import csv
from pathlib import Path


def test_re700_emits_a_metadata_only_blocked_unimplemented_intake(tmp_path):
    from scripts.reverse.re700_unimplemented_source_callsite_proof_intake import (
        FORBIDDEN,
        build_intake,
        write_artifacts,
    )

    repo = Path(__file__).resolve().parents[2]
    intake = build_intake(repo)

    assert intake.source_file_count > 0
    assert intake.unimplemented_marker_count > 0
    assert intake.patch_ready_count == 0
    assert intake.rows == tuple(sorted(intake.rows, key=lambda row: row.module))
    assert all(row.code_change_readiness == "blocked" for row in intake.rows)
    assert all(row.source_behavior_proof_count == 0 for row in intake.rows)

    written = write_artifacts(intake, tmp_path)
    rows = list(csv.DictReader(written["intake_csv"].open(newline="", encoding="utf-8")))
    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))

    assert len(rows) == intake.source_file_count
    assert sum(int(row["unimplemented_marker_count"]) for row in rows) == intake.unimplemented_marker_count
    assert handoff == [
        {
            "story_id": "RE-700",
            "topic": "unimplemented-source-callsite-proof-intake",
            "predecessor": "RE-699",
            "source_file_count": str(intake.source_file_count),
            "unimplemented_marker_count": str(intake.unimplemented_marker_count),
            "source_behavior_proof_count": "0",
            "source_patch_authorized_count": "0",
            "selected_domain": "none",
            "selected_pivot": "none",
            "code_change_readiness": "blocked",
            "next_ticket": "TBD",
            "next_topic": "none",
            "stop_condition": "a source-backed behavioral contract and ABI proof are required before selecting any implementation unit",
        }
    ]
    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text


def test_re700_rejects_re699_handoff_drift(tmp_path):
    from scripts.reverse.re700_unimplemented_source_callsite_proof_intake import build_intake

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    upstream = generated / "re699-spu-source-callsite-proof-gate-handoff.csv"
    upstream.write_text(
        (source / "docs/reverse/generated/re699-spu-source-callsite-proof-gate-handoff.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    source_file = tmp_path / "EMULATOR/LIBGPU.C"
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
            build_intake(tmp_path)
        except ValueError as error:
            assert field in str(error)
        else:
            raise AssertionError(f"RE-700 must reject RE-699 handoff drift in {field}")


def test_re700_rejects_re699_handoff_with_an_extra_data_cell(tmp_path):
    from scripts.reverse.re700_unimplemented_source_callsite_proof_intake import build_intake

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    upstream = generated / "re699-spu-source-callsite-proof-gate-handoff.csv"
    upstream.write_text(
        (source / "docs/reverse/generated/re699-spu-source-callsite-proof-gate-handoff.csv").read_text(encoding="utf-8").rstrip()
        + ",unexpected\n",
        encoding="utf-8",
    )
    source_file = tmp_path / "EMULATOR/LIBGPU.C"
    source_file.parent.mkdir(parents=True)
    source_file.write_text("void example(void) { UNIMPLEMENTED(); }\n", encoding="utf-8")

    try:
        build_intake(tmp_path)
    except ValueError as error:
        assert "schema" in str(error)
    else:
        raise AssertionError("RE-700 must reject an extra RE-699 handoff data cell")


def test_re700_counts_marker_statements_but_not_comments_or_macro_definition(tmp_path):
    from scripts.reverse.re700_unimplemented_source_callsite_proof_intake import build_intake

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    (generated / "re699-spu-source-callsite-proof-gate-handoff.csv").write_text(
        (source / "docs/reverse/generated/re699-spu-source-callsite-proof-gate-handoff.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    emulator = tmp_path / "EMULATOR"
    emulator.mkdir()
    (emulator / "LIBGPU.C").write_text(
        "#define PLACEHOLDER UNIMPLEMENTED();\n"
        "#if 0\nUNIMPLEMENTED();\n#endif\n"
        "// UNIMPLEMENTED();\nvoid a(void) { UNIMPLEMENTED(); }\nconst char *s = \"UNIMPLEMENTED();\";\n",
        encoding="utf-8",
    )

    intake = build_intake(tmp_path)
    assert intake.source_file_count == 1
    assert intake.unimplemented_marker_count == 1


def test_re700_strips_a_raw_literal_with_a_maximum_length_delimiter():
    from scripts.reverse.re700_unimplemented_source_callsite_proof_intake import _without_comments_and_literals

    clean = _without_comments_and_literals(
        'const char *raw = R"abcdefghijklmnop(a " UNIMPLEMENTED(); b)abcdefghijklmnop";\n'
    )

    assert "UNIMPLEMENTED();" not in clean


def test_re700_keeps_all_possible_branches_of_an_unknown_preprocessor_condition():
    from scripts.reverse.re700_unimplemented_source_callsite_proof_intake import _without_inactive_preprocessor_regions

    clean = _without_inactive_preprocessor_regions(
        "#if FEATURE_ENABLED\nUNIMPLEMENTED();\n#else\nUNIMPLEMENTED();\n#endif\n"
    )

    assert clean.count("UNIMPLEMENTED();") == 2


def test_re700_discards_known_false_elif_and_zero_with_leading_zeroes():
    from scripts.reverse.re700_unimplemented_source_callsite_proof_intake import _without_inactive_preprocessor_regions

    clean = _without_inactive_preprocessor_regions(
        "#if FEATURE_ENABLED\nUNIMPLEMENTED();\n#elif 0L\nUNIMPLEMENTED();\n#endif\n"
        "#if 00\nUNIMPLEMENTED();\n#endif\n"
    )

    assert clean.count("UNIMPLEMENTED();") == 1


def test_re700_ignores_multiline_preprocessor_directives(tmp_path):
    from scripts.reverse.re700_unimplemented_source_callsite_proof_intake import build_intake

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    (generated / "re699-spu-source-callsite-proof-gate-handoff.csv").write_text(
        (source / "docs/reverse/generated/re699-spu-source-callsite-proof-gate-handoff.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    emulator = tmp_path / "EMULATOR"
    emulator.mkdir()
    (emulator / "LIBGPU.C").write_text(
        "#define PLACEHOLDER \\\nUNIMPLEMENTED();\n"
        "#if \\\n0\nUNIMPLEMENTED();\n#endif\n"
        "void a(void) { UNIMPLEMENTED(); }\n",
        encoding="utf-8",
    )

    intake = build_intake(tmp_path)
    assert intake.source_file_count == 1
    assert intake.unimplemented_marker_count == 1


def test_re700_ignores_raw_literals_and_common_false_preprocessor_forms(tmp_path):
    from scripts.reverse.re700_unimplemented_source_callsite_proof_intake import build_intake

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    (generated / "re699-spu-source-callsite-proof-gate-handoff.csv").write_text(
        (source / "docs/reverse/generated/re699-spu-source-callsite-proof-gate-handoff.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    emulator = tmp_path / "EMULATOR"
    emulator.mkdir()
    (emulator / "LIBGPU.C").write_text(
        'const char *raw = R"tag(a " UNIMPLEMENTED(); b)tag";\n'
        'const char *max_delimiter = R"abcdefghijklmnop(a " UNIMPLEMENTED(); b)abcdefghijklmnop";\n'
        "#if (0)\nUNIMPLEMENTED();\n#endif\n"
        "#if 0L\nUNIMPLEMENTED();\n#endif\n"
        "void a(void) { UNIMPLEMENTED(); }\n",
        encoding="utf-8",
    )

    intake = build_intake(tmp_path)
    assert intake.source_file_count == 1
    assert intake.unimplemented_marker_count == 1
