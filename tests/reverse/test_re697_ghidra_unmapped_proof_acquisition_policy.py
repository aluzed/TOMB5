import csv
from pathlib import Path


def test_re697_emits_complete_aggregate_proof_policy_and_terminal_handoff(tmp_path):
    from scripts.reverse.re697_ghidra_unmapped_proof_acquisition_policy import (
        FORBIDDEN,
        build_policy,
        write_artifacts,
    )

    repo = Path(__file__).resolve().parents[2]
    policy = build_policy(repo)
    assert policy.unmapped_function_count == 723
    assert policy.physical_cluster_count == 112
    assert sum(row.function_count for row in policy.rows) == 723
    assert [row.lane for row in policy.rows] == [
        "isolated-boundary", "isolated-callee", "isolated-caller", "nonisolated-leaf",
        "nonisolated-helper", "nonisolated-large-block", "nonisolated-hub", "isolated-unconnected",
    ]
    assert all(row.identity_proof_status == "absent" for row in policy.rows)
    assert all(row.code_change_readiness == "blocked" for row in policy.rows)

    written = write_artifacts(policy, tmp_path)
    rows = list(csv.DictReader(written["policy_csv"].open(newline="", encoding="utf-8")))
    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == 8
    assert handoff[0]["next_ticket"] == "TBD"
    assert handoff[0]["next_topic"] == "none"
    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "0x800" not in text
        for fragment in FORBIDDEN:
            assert fragment not in text


def test_re697_rejects_every_re696_handoff_field_drift(tmp_path):
    from scripts.reverse.re697_ghidra_unmapped_proof_acquisition_policy import build_policy

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    handoff_path = generated / "re696-ghidra-unmapped-reconciliation-audit-handoff.csv"
    handoff_path.write_text(
        (source / "docs/reverse/generated/re696-ghidra-unmapped-reconciliation-audit-handoff.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
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
            build_policy(tmp_path)
        except ValueError as error:
            assert field in str(error)
        else:
            raise AssertionError(f"RE-697 must reject RE-696 handoff drift in {field}")
