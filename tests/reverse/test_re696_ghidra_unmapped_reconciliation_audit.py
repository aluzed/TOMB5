import csv
import shutil
from pathlib import Path


def test_re696_reconciliation_audit_is_conserved_blocked_and_metadata_only(tmp_path):
    from scripts.reverse.re696_ghidra_unmapped_reconciliation_audit import (
        FORBIDDEN,
        build_audit,
        write_artifacts,
    )

    repo = Path(__file__).resolve().parents[2]
    audit = build_audit(repo)

    assert audit.unmapped_function_count == 723
    assert audit.physical_cluster_count == 112
    assert audit.isolated_function_count == 79
    assert audit.nonisolated_function_count == 644
    assert audit.reconciliation_status == "no-metadata-detectable-reconciliation-discrepancy"
    assert audit.reconciliation_candidate_cluster_count == 0
    assert audit.reconciliation_ambiguous_cluster_count == 0
    assert audit.identity_proof_count == 0
    assert audit.code_change_readiness == "blocked"

    written = write_artifacts(audit, tmp_path)
    summary_rows = list(csv.DictReader(written["summary_csv"].open(newline="", encoding="utf-8")))
    handoff_rows = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))
    assert summary_rows == handoff_rows
    assert summary_rows[0]["next_ticket"] == "RE-697"
    assert summary_rows[0]["next_topic"] == "ghidra-unmapped-proof-acquisition-policy"
    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "0x800" not in text
        for fragment in FORBIDDEN:
            assert fragment not in text


def test_re696_rejects_every_re695_handoff_field_drift(tmp_path):
    from scripts.reverse.re696_ghidra_unmapped_reconciliation_audit import build_audit

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    for name in (
        "re690-global-ghidra-coverage-summary.csv",
        "re692-ghidra-unmapped-cluster-ledger.csv",
        "re693-ghidra-unmapped-isolated-cluster-proof-gate.csv",
        "re695-ghidra-unmapped-nonisolated-cluster-proof-gate.csv",
        "re695-ghidra-unmapped-nonisolated-cluster-proof-gate-handoff.csv",
    ):
        (generated / name).write_text(
            (source / "docs/reverse/generated" / name).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
    handoff_path = generated / "re695-ghidra-unmapped-nonisolated-cluster-proof-gate-handoff.csv"
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
            build_audit(tmp_path)
        except ValueError as error:
            assert field in str(error)
        else:
            raise AssertionError(f"RE-696 must reject RE-695 handoff drift in {field}")


def test_re696_rejects_every_consumed_metadata_field_drift(tmp_path):
    from scripts.reverse.re696_ghidra_unmapped_reconciliation_audit import build_audit

    source = Path(__file__).resolve().parents[2]
    input_names = (
        "re690-global-ghidra-coverage-summary.csv",
        "re692-ghidra-unmapped-cluster-ledger.csv",
        "re693-ghidra-unmapped-isolated-cluster-proof-gate.csv",
        "re695-ghidra-unmapped-nonisolated-cluster-proof-gate.csv",
    )
    for name in input_names:
        original_path = source / "docs/reverse/generated" / name
        with original_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            fields = reader.fieldnames
        assert fields is not None
        for field in fields:
            sandbox = tmp_path / f"{name}-{field}"
            generated = sandbox / "docs/reverse/generated"
            generated.mkdir(parents=True)
            for copy_name in (*input_names, "re695-ghidra-unmapped-nonisolated-cluster-proof-gate-handoff.csv"):
                shutil.copyfile(source / "docs/reverse/generated" / copy_name, generated / copy_name)
            target_path = generated / name
            with target_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            rows[0][field] = "drift"
            with target_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)
            try:
                build_audit(sandbox)
            except ValueError as error:
                assert field in str(error)
            else:
                raise AssertionError(f"RE-696 must reject {name} drift in {field}")
