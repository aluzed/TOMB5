import csv
from pathlib import Path


def test_re695_nonisolated_gate_is_complete_blocked_and_metadata_only(tmp_path):
    from scripts.reverse.re695_ghidra_unmapped_nonisolated_cluster_proof_gate import (
        FORBIDDEN,
        build_gate,
        write_artifacts,
    )

    repo = Path(__file__).resolve().parents[2]
    gate = build_gate(repo)
    assert gate.unmapped_function_count == 644
    assert gate.cluster_count == 72
    assert sum(row.function_count for row in gate.rows) == 644
    assert [row.category for row in gate.rows] == ["leaf", "helper", "large-block", "hub"]
    assert all(row.identity_proof_status == "absent" for row in gate.rows)
    assert all(row.code_change_readiness == "blocked" for row in gate.rows)

    written = write_artifacts(gate, tmp_path)
    rows = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == 4
    assert handoff[0]["next_ticket"] == "RE-696"
    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "0x800" not in text
        for fragment in FORBIDDEN:
            assert fragment not in text


def test_re695_rejects_every_re694_handoff_field_drift(tmp_path):
    from scripts.reverse.re695_ghidra_unmapped_nonisolated_cluster_proof_gate import build_gate

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    for name in ("re694-ghidra-unmapped-boundary-exposure-backlog-handoff.csv", "re691-ghidra-unmapped-completion-matrix.csv"):
        (generated / name).write_text((source / "docs/reverse/generated" / name).read_text(encoding="utf-8"), encoding="utf-8")
    handoff_path = generated / "re694-ghidra-unmapped-boundary-exposure-backlog-handoff.csv"
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
            build_gate(tmp_path)
        except ValueError as error:
            assert field in str(error)
        else:
            raise AssertionError(f"RE-695 must reject RE-694 handoff drift in {field}")
