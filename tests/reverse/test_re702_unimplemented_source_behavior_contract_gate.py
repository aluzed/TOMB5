import csv
from pathlib import Path


def test_re702_emits_terminal_blocked_behavior_contract_gate(tmp_path):
    from scripts.reverse.re702_unimplemented_source_behavior_contract_gate import (
        FORBIDDEN,
        build_gate,
        write_artifacts,
    )

    repo = Path(__file__).resolve().parents[2]
    gate = build_gate(repo)

    assert gate.source_file_count == 66
    assert gate.function_row_count == 353
    assert gate.unimplemented_marker_count == 354
    assert gate.source_behavior_proof_count == 0
    assert gate.source_patch_authorized_count == 0
    assert gate.rows == tuple(sorted(gate.rows, key=lambda row: (row.source_file, row.repo_function)))
    assert all(row.behavior_contract_status == "missing" for row in gate.rows)
    assert all(row.code_change_readiness == "blocked" for row in gate.rows)

    written = write_artifacts(gate, tmp_path)
    rows = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))

    assert len(rows) == gate.function_row_count
    assert handoff == [
        {
            "story_id": "RE-702",
            "topic": "unimplemented-source-behavior-contract-gate",
            "predecessor": "RE-701",
            "source_file_count": "66",
            "function_row_count": "353",
            "unimplemented_marker_count": "354",
            "source_behavior_proof_count": "0",
            "source_patch_authorized_count": "0",
            "selected_domain": "none",
            "selected_pivot": "none",
            "code_change_readiness": "blocked",
            "next_ticket": "TBD",
            "next_topic": "none",
            "stop_condition": "external source-backed behavioral contracts and ABI proof are required before reopening this inventory",
        }
    ]
    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text


def test_re702_rejects_every_re701_handoff_field_drift(tmp_path):
    from scripts.reverse.re702_unimplemented_source_behavior_contract_gate import build_gate

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    upstream = generated / "re701-unimplemented-source-function-identity-export-handoff.csv"
    upstream.write_text(
        (source / "docs/reverse/generated/re701-unimplemented-source-function-identity-export-handoff.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    identity = generated / "re701-unimplemented-source-function-identity-export.csv"
    identity.write_text(
        (source / "docs/reverse/generated/re701-unimplemented-source-function-identity-export.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
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
            build_gate(tmp_path)
        except ValueError as error:
            assert field in str(error)
        else:
            raise AssertionError(f"RE-702 must reject RE-701 handoff drift in {field}")


def test_re702_rejects_identity_schema_row_and_safety_drift(tmp_path):
    from scripts.reverse.re702_unimplemented_source_behavior_contract_gate import build_gate

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    (generated / "re701-unimplemented-source-function-identity-export-handoff.csv").write_text(
        (source / "docs/reverse/generated/re701-unimplemented-source-function-identity-export-handoff.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    identity = generated / "re701-unimplemented-source-function-identity-export.csv"
    baseline = (source / "docs/reverse/generated/re701-unimplemented-source-function-identity-export.csv").read_text(encoding="utf-8")

    identity.write_text(baseline.rstrip() + ",unexpected\n", encoding="utf-8")
    try:
        build_gate(tmp_path)
    except ValueError as error:
        assert "schema" in str(error)
    else:
        raise AssertionError("RE-702 must reject identity schema drift")

    identity.write_text(baseline + baseline.splitlines()[1] + "\n", encoding="utf-8")
    try:
        build_gate(tmp_path)
    except ValueError as error:
        assert "row-count" in str(error)
    else:
        raise AssertionError("RE-702 must reject identity row-count drift")

    fields = baseline.splitlines()[0].split(",")
    rows = list(csv.DictReader(baseline.splitlines()))
    rows[0]["code_change_readiness"] = "ready"
    with identity.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    try:
        build_gate(tmp_path)
    except ValueError as error:
        assert "code_change_readiness" in str(error)
    else:
        raise AssertionError("RE-702 must reject identity readiness escalation")


def test_re702_rejects_identity_formula_and_aggregate_preserving_count_drift(tmp_path):
    from scripts.reverse.re702_unimplemented_source_behavior_contract_gate import build_gate

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    for name in (
        "re701-unimplemented-source-function-identity-export-handoff.csv",
        "re701-unimplemented-source-function-identity-export.csv",
    ):
        (generated / name).write_text((source / "docs/reverse/generated" / name).read_text(encoding="utf-8"), encoding="utf-8")
    identity = generated / "re701-unimplemented-source-function-identity-export.csv"
    with identity.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
        fields = tuple(csv.DictReader((source / "docs/reverse/generated/re701-unimplemented-source-function-identity-export.csv").open(newline="", encoding="utf-8")).fieldnames or ())

    rows[0]["repo_function"] = '=HYPERLINK("https://example.invalid","x")'
    with identity.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    try:
        build_gate(tmp_path)
    except ValueError as error:
        assert "repo_function" in str(error)
    else:
        raise AssertionError("RE-702 must reject formula-like source symbols")

    rows[0]["repo_function"] = "Emulator_DestroyTexture"
    donor = next(row for row in rows if row["unimplemented_marker_count"] == "2")
    rows[0]["unimplemented_marker_count"] = "2"
    donor["unimplemented_marker_count"] = "1"
    with identity.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    try:
        build_gate(tmp_path)
    except ValueError as error:
        assert "fingerprint" in str(error)
    else:
        raise AssertionError("RE-702 must reject aggregate-preserving marker-count drift")
