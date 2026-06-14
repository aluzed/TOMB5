from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.reverse.saveleveldata_original_audit import (
    audit_save_level_data,
    write_markdown,
)


def _write_dump(path: Path, instructions: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["index", "ram_address", "payload_offset", "word_le_hex", "instruction"],
            lineterminator="\n",
        )
        writer.writeheader()
        for index, instruction in enumerate(instructions):
            writer.writerow({
                "index": index,
                "ram_address": f"0x80053f{index:02x}",
                "payload_offset": f"0x043f{index:02x}",
                "word_le_hex": f"0x{index + 1:08x}",
                "instruction": instruction,
            })


def test_audit_counts_original_writes_and_source_sites_without_recording_bytes(tmp_path):
    dump = tmp_path / "SaveLevelData_80053f10.csv"
    _write_dump(dump, [
        "addiu $sp, $sp, -32",
        "jal 0x80053b04",
        "nop",
        "jal 0x80053b04",
    ])

    audit = audit_save_level_data(
        repo=ROOT,
        original_dump=dump,
        source=ROOT / "GAME" / "SAVEGAME.C",
        write_sg_address="0x80053b04",
    )

    assert audit.original_instruction_count == 4
    assert audit.original_write_sg_call_count == 2
    assert audit.source_write_site_count >= 30
    assert audit.status == "needs-control-flow-audit"
    assert all(not text.startswith("0x000000") for text in audit.versionable_lines())


def test_markdown_report_has_tracker_and_no_original_instruction_rows(tmp_path):
    dump = tmp_path / "SaveLevelData_80053f10.csv"
    _write_dump(dump, ["jal 0x80053b04"])
    audit = audit_save_level_data(
        repo=ROOT,
        original_dump=dump,
        source=ROOT / "GAME" / "SAVEGAME.C",
        write_sg_address="0x80053b04",
    )
    out = tmp_path / "report.md"

    write_markdown(audit, out)
    text = out.read_text(encoding="utf-8")

    assert "## Progress tracker" in text
    assert "- [x] Count original `WriteSG` calls" in text
    assert "original `WriteSG` call count: `1`" in text
    assert "source `Write(...)` site count:" in text
    assert "jal 0x80053b04" not in text
    assert "word_le_hex" not in text
