import csv
from pathlib import Path


def test_re699_emits_a_complete_blocked_spu_source_callsite_proof_gate(tmp_path):
    from scripts.reverse.re699_spu_source_callsite_proof_gate import (
        FORBIDDEN,
        build_audit,
        write_artifacts,
    )

    repo = Path(__file__).resolve().parents[2]
    audit = build_audit(repo)

    assert audit.candidate_api_count == 78
    assert audit.active_source_callsite_count == 0
    assert audit.commented_reference_count == 1
    assert audit.patch_ready_count == 0
    assert audit.rows == tuple(sorted(audit.rows, key=lambda row: row.api_name))
    assert all(row.active_source_callsite_count == 0 for row in audit.rows)
    assert all(row.code_change_readiness == "blocked" for row in audit.rows)

    written = write_artifacts(audit, tmp_path)
    rows = list(csv.DictReader(written["audit_csv"].open(newline="", encoding="utf-8")))
    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == 78
    assert handoff == [
        {
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
    ]
    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text


def test_re699_rejects_every_re698_handoff_field_drift(tmp_path):
    from scripts.reverse.re699_spu_source_callsite_proof_gate import build_audit

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    upstream = generated / "re698-spu-public-api-reconciliation-gate-handoff.csv"
    upstream.write_text(
        (source / "docs/reverse/generated/re698-spu-public-api-reconciliation-gate-handoff.csv").read_text(
            encoding="utf-8"
        ),
        encoding="utf-8",
    )
    inventory = generated / "re698-spu-public-api-reconciliation-gate.csv"
    inventory.write_text(
        (source / "docs/reverse/generated/re698-spu-public-api-reconciliation-gate.csv").read_text(
            encoding="utf-8"
        ),
        encoding="utf-8",
    )
    for relative in ("EMULATOR/LIBSPU.H", "EMULATOR/LIBSPU.C", "SPEC_PSXPC/SFX.C"):
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text((source / relative).read_text(encoding="utf-8"), encoding="utf-8")

    with upstream.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        values = next(reader)
    assert fields is not None
    for field in fields:
        with upstream.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerow(values)
        mutated = values.copy()
        mutated[field] = "drift"
        with upstream.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerow(mutated)
        try:
            build_audit(tmp_path)
        except ValueError as error:
            assert field in str(error)
        else:
            raise AssertionError(f"RE-699 must reject RE-698 handoff drift in {field}")


def test_re699_rejects_inventory_schema_and_safety_drift(tmp_path):
    from scripts.reverse.re699_spu_source_callsite_proof_gate import build_audit

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    for name in (
        "re698-spu-public-api-reconciliation-gate-handoff.csv",
        "re698-spu-public-api-reconciliation-gate.csv",
    ):
        (generated / name).write_text((source / "docs/reverse/generated" / name).read_text(encoding="utf-8"), encoding="utf-8")
    for relative in ("EMULATOR/LIBSPU.H", "EMULATOR/LIBSPU.C", "SPEC_PSXPC/SFX.C"):
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text((source / relative).read_text(encoding="utf-8"), encoding="utf-8")

    inventory = generated / "re698-spu-public-api-reconciliation-gate.csv"
    with inventory.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        rows = list(reader)
    assert fields is not None
    for field in fields:
        with inventory.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        mutated_rows = [row.copy() for row in rows]
        mutated_rows[0][field] = "drift"
        with inventory.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(mutated_rows)
        try:
            build_audit(tmp_path)
        except ValueError as error:
            assert field in str(error)
        else:
            raise AssertionError(f"RE-699 must reject RE-698 inventory drift in {field}")


def test_re699_lexes_comments_and_literals_without_masking_a_real_callsite(tmp_path):
    from scripts.reverse.re699_spu_source_callsite_proof_gate import build_audit

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    for name in (
        "re698-spu-public-api-reconciliation-gate-handoff.csv",
        "re698-spu-public-api-reconciliation-gate.csv",
    ):
        (generated / name).write_text((source / "docs/reverse/generated" / name).read_text(encoding="utf-8"), encoding="utf-8")
    callsite = tmp_path / "SPEC_PSXPC/SFX.C"
    callsite.parent.mkdir(parents=True)
    callsite.write_text(
        'const char *url = "http://example"; SpuSetVoicePitch(1, 2);\n'
        'const char *literal = "SpuSetVoicePitch(";\n'
        '/* SpuSetVoicePitch(1, 2); */\n'
        '// SpuSetVoicePitch(1, 2);\n'
        "// continued \\\nSpuSetVoicePitch(1, 2);\n",
        encoding="utf-8",
    )

    audit = build_audit(tmp_path)
    pitch = next(row for row in audit.rows if row.api_name == "SpuSetVoicePitch")
    assert pitch.active_source_callsite_count == 1
    assert audit.active_source_callsite_count == 1
    assert audit.commented_reference_count == 3


def test_re699_counts_a_real_cpp_callsite_and_ignores_a_disabled_preprocessor_branch(tmp_path):
    from scripts.reverse.re699_spu_source_callsite_proof_gate import build_audit

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    for name in (
        "re698-spu-public-api-reconciliation-gate-handoff.csv",
        "re698-spu-public-api-reconciliation-gate.csv",
    ):
        (generated / name).write_text((source / "docs/reverse/generated" / name).read_text(encoding="utf-8"), encoding="utf-8")
    callsite = tmp_path / "SPEC_PSXPC/SFX.CPP"
    callsite.parent.mkdir(parents=True)
    callsite.write_text(
        "#if 0\nSpuSetVoicePitch(1, 2);\n#elif 1\nSpuSetVoicePitch(3, 4);\n#endif\n"
        "#if UNKNOWN_MACRO\nSpuSetVoicePitch(5, 6);\n#else\nSpuSetVoicePitch(7, 8);\n#endif\n"
        "#if 1\nSpuSetVoicePitch(9, 10);\n#elif UNKNOWN_MACRO\nSpuSetVoicePitch(11, 12);\n#else\nSpuSetVoicePitch(13, 14);\n#endif\n",
        encoding="utf-8",
    )

    audit = build_audit(tmp_path)

    pitch = next(row for row in audit.rows if row.api_name == "SpuSetVoicePitch")
    assert pitch.active_source_callsite_count == 4
    assert audit.active_source_callsite_count == 4


def test_re699_rejects_unbalanced_preprocessor_directives(tmp_path):
    from scripts.reverse.re699_spu_source_callsite_proof_gate import build_audit

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    for name in (
        "re698-spu-public-api-reconciliation-gate-handoff.csv",
        "re698-spu-public-api-reconciliation-gate.csv",
    ):
        (generated / name).write_text((source / "docs/reverse/generated" / name).read_text(encoding="utf-8"), encoding="utf-8")
    callsite = tmp_path / "SPEC_PSXPC/SFX.C"
    callsite.parent.mkdir(parents=True)
    callsite.write_text("#if 0\nSpuSetVoicePitch(1, 2);\n", encoding="utf-8")

    try:
        build_audit(tmp_path)
    except ValueError as error:
        assert "preprocessor" in str(error)
    else:
        raise AssertionError("RE-699 must reject unbalanced preprocessor directives")


def test_re699_rejects_undecodable_source_text(tmp_path):
    from scripts.reverse.re699_spu_source_callsite_proof_gate import build_audit

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    for name in (
        "re698-spu-public-api-reconciliation-gate-handoff.csv",
        "re698-spu-public-api-reconciliation-gate.csv",
    ):
        (generated / name).write_text((source / "docs/reverse/generated" / name).read_text(encoding="utf-8"), encoding="utf-8")
    callsite = tmp_path / "SPEC_PSXPC/SFX.C"
    callsite.parent.mkdir(parents=True)
    callsite.write_bytes(b"\xff")

    try:
        build_audit(tmp_path)
    except ValueError as error:
        assert "decode" in str(error)
    else:
        raise AssertionError("RE-699 must fail closed on undecodable source text")
