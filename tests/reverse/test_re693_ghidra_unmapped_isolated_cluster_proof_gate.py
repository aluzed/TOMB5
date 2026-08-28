import csv
from pathlib import Path


def test_re693_isolated_cluster_gate_is_complete_blocked_and_metadata_only(tmp_path):
    from scripts.reverse.re693_ghidra_unmapped_isolated_cluster_proof_gate import (
        FORBIDDEN,
        build_gate,
        write_artifacts,
    )

    repo = Path(__file__).resolve().parents[2]
    gate = build_gate(repo)

    assert gate.isolated_cluster_count == 79
    assert len(gate.rows) == 79
    assert sum(row.member_count for row in gate.rows) == 79
    assert {row.exposure_class for row in gate.rows} <= {
        "unconnected", "callee-exposed", "caller-exposed", "boundary-exposed"
    }
    assert all(row.reconciliation_status == "none" for row in gate.rows)
    assert all(row.identity_proof_status == "absent" for row in gate.rows)
    assert all(row.code_change_readiness == "blocked" for row in gate.rows)

    written = write_artifacts(gate, tmp_path)
    assert set(written) == {"gate_csv", "summary_csv", "handoff_csv", "dashboard_html", "story"}
    rows = list(csv.DictReader(written["gate_csv"].open(newline="", encoding="utf-8")))
    summary = list(csv.DictReader(written["summary_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == 79
    assert summary == [summary[0]]
    assert summary[0]["next_ticket"] == "RE-694"
    assert summary[0]["code_change_readiness"] == "blocked"

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "0x800" not in text
        for fragment in FORBIDDEN:
            assert fragment not in text


def test_re693_gate_rejects_raw_evidence_like_upstream_ledger_value(tmp_path):
    from scripts.reverse.re693_ghidra_unmapped_isolated_cluster_proof_gate import build_gate

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    for name in (
        "re690-global-ghidra-coverage-summary.csv",
        "re692-ghidra-unmapped-cluster-ledger-handoff.csv",
        "re692-ghidra-unmapped-cluster-ledger.csv",
    ):
        text = (source / "docs/reverse/generated" / name).read_text(encoding="utf-8")
        if name.endswith("ledger.csv"):
            text = text.replace("cluster-001", "0x80010000", 1)
        (generated / name).write_text(text, encoding="utf-8")

    try:
        build_gate(tmp_path)
    except ValueError as error:
        assert "forbidden" in str(error).lower()
    else:
        raise AssertionError("RE-693 must reject raw-evidence-like ledger content")


def test_re693_gate_rejects_safety_escalation_in_re692_handoff(tmp_path):
    from scripts.reverse.re693_ghidra_unmapped_isolated_cluster_proof_gate import build_gate

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    for name in (
        "re690-global-ghidra-coverage-summary.csv",
        "re692-ghidra-unmapped-cluster-ledger.csv",
        "re692-ghidra-unmapped-cluster-ledger-handoff.csv",
    ):
        text = (source / "docs/reverse/generated" / name).read_text(encoding="utf-8")
        if name.endswith("handoff.csv"):
            text = text.replace(",no,blocked,RE-693,", ",yes,blocked,RE-693,")
        (generated / name).write_text(text, encoding="utf-8")

    try:
        build_gate(tmp_path)
    except ValueError as error:
        assert "raw_evidence_versioned" in str(error)
    else:
        raise AssertionError("RE-693 must reject an upstream safety escalation")
