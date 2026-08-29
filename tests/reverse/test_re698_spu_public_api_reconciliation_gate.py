import csv
from pathlib import Path


def test_re698_emits_a_complete_blocked_spu_api_reconciliation_gate(tmp_path):
    from scripts.reverse.re698_spu_public_api_reconciliation_gate import (
        FORBIDDEN,
        build_inventory,
        write_artifacts,
    )

    repo = Path(__file__).resolve().parents[2]
    inventory = build_inventory(repo)

    assert inventory.header_declaration_count == 116
    assert inventory.source_definition_count == 38
    assert inventory.unmatched_declaration_count == 78
    assert inventory.patch_ready_count == 0
    assert inventory.rows == tuple(sorted(inventory.rows, key=lambda row: row.api_name))
    assert all(row.proof_status == "absent" for row in inventory.rows)
    assert all(row.code_change_readiness == "blocked" for row in inventory.rows)

    written = write_artifacts(inventory, tmp_path)
    rows = list(csv.DictReader(written["inventory_csv"].open(newline="", encoding="utf-8")))
    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == 78
    assert handoff == [
        {
            "story_id": "RE-698",
            "topic": "spu-public-api-reconciliation-gate",
            "predecessor": "RE-697",
            "unmatched_declaration_count": "78",
            "source_behavior_proof_count": "0",
            "source_patch_authorized_count": "0",
            "code_change_readiness": "blocked",
            "next_ticket": "TBD",
            "next_topic": "none",
            "stop_condition": "source-backed behavior and ABI proof required before any implementation",
        }
    ]
    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        for fragment in FORBIDDEN:
            assert fragment not in text


def test_re698_rejects_non_spu_header_source_or_re697_terminal_drift(tmp_path):
    from scripts.reverse.re698_spu_public_api_reconciliation_gate import build_inventory

    root = tmp_path
    (root / "EMULATOR").mkdir(parents=True)
    (root / "docs/reverse/generated").mkdir(parents=True)
    (root / "EMULATOR/LIBSPU.H").write_text("extern void SpuOnly(void);\n", encoding="utf-8")
    (root / "EMULATOR/LIBSPU.C").write_text("void SpuOnly(void) {}\n", encoding="utf-8")
    (root / "docs/reverse/generated/re697-ghidra-unmapped-proof-acquisition-policy-handoff.csv").write_text(
        "story_id,topic,code_change_readiness,next_ticket,next_topic,stop_condition\n"
        "RE-697,ghidra-unmapped-proof-acquisition-policy,blocked,TBD,none,terminal\n",
        encoding="utf-8",
    )

    try:
        build_inventory(root)
    except ValueError as error:
        assert "RE-697" in str(error)
    else:
        raise AssertionError("RE-698 must fail closed when the terminal handoff drifts")


def test_re698_rejects_every_re697_handoff_field_drift(tmp_path):
    from scripts.reverse.re698_spu_public_api_reconciliation_gate import build_inventory

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    handoff_path = generated / "re697-ghidra-unmapped-proof-acquisition-policy-handoff.csv"
    handoff_path.write_text(
        (source / "docs/reverse/generated/re697-ghidra-unmapped-proof-acquisition-policy-handoff.csv").read_text(
            encoding="utf-8"
        ),
        encoding="utf-8",
    )
    (tmp_path / "EMULATOR").mkdir()
    (tmp_path / "EMULATOR/LIBSPU.H").write_text(
        (source / "EMULATOR/LIBSPU.H").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (tmp_path / "EMULATOR/LIBSPU.C").write_text(
        (source / "EMULATOR/LIBSPU.C").read_text(encoding="utf-8"), encoding="utf-8"
    )
    with handoff_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        values = next(reader)
    assert fields is not None
    for field in fields:
        mutated = values.copy()
        mutated[field] = "drift"
        with handoff_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerow(mutated)
        try:
            build_inventory(tmp_path)
        except ValueError as error:
            assert field in str(error)
        else:
            raise AssertionError(f"RE-698 must reject RE-697 handoff drift in {field}")
