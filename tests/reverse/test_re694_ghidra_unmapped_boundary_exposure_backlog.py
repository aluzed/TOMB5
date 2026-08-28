import csv
from pathlib import Path


def test_re694_boundary_backlog_is_complete_prioritized_and_metadata_only(tmp_path):
    from scripts.reverse.re694_ghidra_unmapped_boundary_exposure_backlog import (
        FORBIDDEN,
        build_backlog,
        write_artifacts,
    )

    repo = Path(__file__).resolve().parents[2]
    backlog = build_backlog(repo)

    assert backlog.isolated_cluster_count == 79
    assert len(backlog.rows) == 4
    assert sum(row.cluster_count for row in backlog.rows) == 79
    assert [row.exposure_class for row in backlog.rows] == [
        "boundary-exposed", "callee-exposed", "caller-exposed", "unconnected",
    ]
    assert all(row.confidence == "medium" for row in backlog.rows)
    assert all(row.identity_proof_status == "absent" for row in backlog.rows)
    assert all(row.code_change_readiness == "blocked" for row in backlog.rows)

    written = write_artifacts(backlog, tmp_path)
    assert set(written) == {"backlog_csv", "summary_csv", "handoff_csv", "dashboard_html", "story"}
    rows = list(csv.DictReader(written["backlog_csv"].open(newline="", encoding="utf-8")))
    handoff = list(csv.DictReader(written["handoff_csv"].open(newline="", encoding="utf-8")))
    assert len(rows) == 4
    assert handoff[0]["next_ticket"] == "RE-695"
    assert handoff[0]["code_change_readiness"] == "blocked"

    for path in written.values():
        text = path.read_text(encoding="utf-8").lower()
        assert "0x800" not in text
        for fragment in FORBIDDEN:
            assert fragment not in text


def test_re694_rejects_every_re693_handoff_field_drift(tmp_path):
    from scripts.reverse.re694_ghidra_unmapped_boundary_exposure_backlog import build_backlog

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    for name in (
        "re693-ghidra-unmapped-isolated-cluster-proof-gate.csv",
        "re693-ghidra-unmapped-isolated-cluster-proof-gate-handoff.csv",
    ):
        (generated / name).write_text(
            (source / "docs/reverse/generated" / name).read_text(encoding="utf-8"), encoding="utf-8"
        )

    handoff_path = generated / "re693-ghidra-unmapped-isolated-cluster-proof-gate-handoff.csv"
    original = handoff_path.read_text(encoding="utf-8")
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
            build_backlog(tmp_path)
        except ValueError as error:
            assert field in str(error)
        else:
            raise AssertionError(f"RE-694 must reject RE-693 handoff drift in {field}")
    handoff_path.write_text(original, encoding="utf-8")


def test_re694_rejects_re693_schema_and_inventory_drift(tmp_path):
    from scripts.reverse.re694_ghidra_unmapped_boundary_exposure_backlog import build_backlog

    source = Path(__file__).resolve().parents[2]
    generated = tmp_path / "docs/reverse/generated"
    generated.mkdir(parents=True)
    for name in (
        "re693-ghidra-unmapped-isolated-cluster-proof-gate.csv",
        "re693-ghidra-unmapped-isolated-cluster-proof-gate-handoff.csv",
    ):
        (generated / name).write_text(
            (source / "docs/reverse/generated" / name).read_text(encoding="utf-8"), encoding="utf-8"
        )

    handoff_path = generated / "re693-ghidra-unmapped-isolated-cluster-proof-gate-handoff.csv"
    header, row = handoff_path.read_text(encoding="utf-8").splitlines()
    handoff_path.write_text(",".join(reversed(header.split(","))) + "\n" + row + "\n", encoding="utf-8")
    try:
        build_backlog(tmp_path)
    except ValueError as error:
        assert "schema" in str(error)
    else:
        raise AssertionError("RE-694 must reject RE-693 handoff schema drift")

    (generated / "re693-ghidra-unmapped-isolated-cluster-proof-gate-handoff.csv").write_text(
        (source / "docs/reverse/generated/re693-ghidra-unmapped-isolated-cluster-proof-gate-handoff.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    gate_path = generated / "re693-ghidra-unmapped-isolated-cluster-proof-gate.csv"
    lines = gate_path.read_text(encoding="utf-8").splitlines()
    gate_path.write_text("\n".join(lines[:-1]) + "\n", encoding="utf-8")
    try:
        build_backlog(tmp_path)
    except ValueError as error:
        assert "inventory" in str(error)
    else:
        raise AssertionError("RE-694 must reject RE-693 inventory drift")
