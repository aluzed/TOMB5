#!/usr/bin/env python3
"""Export Ghidra functions and map them to TOMB5 repo address comments.

The repo annotates many PSX functions with comments such as:

    void main()//10064(<), 10064(<) (F) (*) (D) (ND)

This script exports Ghidra's function list headlessly, parses those comments,
normalizes final PSX addresses to 0x80xxxxxx, and writes CSV/Markdown reports
that can be used without opening Ghidra manually.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

PSX_RAM_PREFIX = 0x80000000
SOURCE_SUFFIXES = {".C", ".H", ".CPP", ".CC", ".CXX", ".HPP"}
SKIP_DIR_PARTS = {".git", "build", "docs", "TOOLS"}
FUNCTION_COMMENT_RE = re.compile(
    r"^\s*(?P<prefix>[^/#;{}][^/;{}]*?)\b(?P<name>[A-Za-z_]\w*)\s*\([^;{}]*\)\s*//(?P<comment>.*)$"
)
ADDRESS_RE = re.compile(r"(?<![0-9A-Fa-f])(?:0x)?([0-9A-Fa-f]{4,8})(?![0-9A-Fa-f])")
MARKER_RE = re.compile(r"\(([A-Za-z*<>]+)\)")
AUTO_GHIDRA_NAME_RE = re.compile(r"^(FUN|SUB|LAB|loc|DAT|PTR|switchD)_", re.IGNORECASE)


@dataclass(frozen=True)
class RepoFunction:
    file: str
    line: int
    function: str
    beta_address: str
    final_address: str
    markers: str
    comment: str


def run(cmd: list[str], log_file: Path | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a", encoding="utf-8") as f:
            f.write("\n$ " + " ".join(cmd) + "\n")
            f.write(proc.stdout)
    if proc.returncode != 0:
        raise SystemExit(f"Command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stdout}\nSee log: {log_file}")
    return proc


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"Required tool not found in PATH: {name}")
    return path


def normalize_psx_addr_text(text: str) -> str:
    value = int(text, 16)
    if value < PSX_RAM_PREFIX:
        value |= PSX_RAM_PREFIX
    return f"0x{value:08x}"


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def iter_source_files(repo: Path):
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        parts = set(path.relative_to(repo).parts)
        if parts & SKIP_DIR_PARTS:
            continue
        if path.suffix.upper() in SOURCE_SUFFIXES:
            yield path


def parse_repo_functions(repo: Path) -> list[RepoFunction]:
    results: list[RepoFunction] = []
    for path in iter_source_files(repo):
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for idx, line in enumerate(lines, start=1):
            match = FUNCTION_COMMENT_RE.match(line)
            if not match:
                continue
            comment = match.group("comment").strip()
            addresses = [normalize_psx_addr_text(m.group(1)) for m in ADDRESS_RE.finditer(comment)]
            if not addresses:
                continue
            # Project convention observed in SPEC_PSX comments: first address is beta,
            # second address is final. If only one exists, use it for both fields.
            beta = addresses[0]
            final = addresses[1] if len(addresses) >= 2 else addresses[0]
            markers = ";".join(m.group(1) for m in MARKER_RE.finditer(comment))
            results.append(
                RepoFunction(
                    file=rel(path, repo),
                    line=idx,
                    function=match.group("name"),
                    beta_address=beta,
                    final_address=final,
                    markers=markers,
                    comment=comment,
                )
            )
    results.sort(key=lambda item: (item.final_address, item.file, item.line, item.function))
    return results


def read_ghidra_functions(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda row: row["entry"])
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(text: object) -> str:
    return str(text).replace("|", "\\|")


def write_markdown_table(path: Path, title: str, fieldnames: list[str], rows: list[dict[str, object]], limit: int | None = None) -> None:
    shown = rows if limit is None else rows[:limit]
    lines = [f"# {title}", "", f"Generated: {datetime.now(timezone.utc).isoformat()}", "", f"Rows: {len(rows)}"]
    if limit is not None and len(rows) > limit:
        lines.append(f"Showing first {limit} rows.")
    lines.extend(["", "| " + " | ".join(fieldnames) + " |", "| " + " | ".join(["---"] * len(fieldnames)) + " |"])
    for row in shown:
        lines.append("| " + " | ".join(md_escape(row.get(field, "")) for field in fieldnames) + " |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def ensure_payload(repo: Path, generated_dir: Path, skip_prepare: bool) -> tuple[Path, str]:
    summary_file = generated_dir / "prepare_ghidra_psx_summary.json"
    if not skip_prepare:
        run([sys.executable, "scripts/reverse/prepare_ghidra_psx.py", "--skip-ghidra"], cwd=repo, log_file=generated_dir / "map_ghidra_to_repo.log")
    if not summary_file.exists():
        raise SystemExit(f"Missing prepare summary: {summary_file}; run prepare_ghidra_psx.py first or omit --skip-prepare")
    summary = json.loads(summary_file.read_text(encoding="utf-8"))
    payload = Path(summary["payload"])
    if not payload.exists():
        raise SystemExit(f"Missing Ghidra payload: {payload}")
    return payload, str(summary["text_base"])


def export_ghidra(repo: Path, payload: Path, text_base: str, generated_dir: Path, project_name: str, timeout: str, keep_project: bool) -> Path:
    require_tool("analyzeHeadless")
    ghidra_csv = generated_dir / "ghidra-functions.csv"
    script_path = repo / "scripts" / "reverse"
    project_dir = repo / "build" / "reverse" / "ghidra-projects"
    project_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "analyzeHeadless",
        str(project_dir),
        project_name,
        "-import", str(payload),
        "-processor", "MIPS:LE:32:default",
        "-cspec", "default",
        "-loader", "BinaryLoader",
        "-loader-baseAddr", text_base,
        "-analysisTimeoutPerFile", str(timeout),
        "-scriptPath", str(script_path),
        "-postScript", "ExportGhidraFunctions.java", str(ghidra_csv),
    ]
    if not keep_project:
        cmd.append("-deleteProject")
    run(cmd, cwd=repo, log_file=generated_dir / "map_ghidra_to_repo.log")
    if not ghidra_csv.exists():
        raise SystemExit(f"Ghidra CSV was not created: {ghidra_csv}")
    return ghidra_csv


def mirror_reports_to_docs(repo: Path, generated_dir: Path) -> None:
    docs_dir = repo / "docs" / "reverse" / "generated"
    docs_dir.mkdir(parents=True, exist_ok=True)
    for name in [
        "ghidra-functions.csv",
        "repo-functions.csv",
        "repo-function-map.csv",
        "mapped-functions.md",
        "repo-only-functions.md",
        "unmapped-ghidra-functions.md",
        "function-map-summary.json",
    ]:
        src = generated_dir / name
        if src.exists():
            shutil.copy2(src, docs_dir / name)


def build_reports(repo: Path, repo_rows: list[RepoFunction], ghidra_rows: list[dict[str, str]], generated_dir: Path) -> dict[str, int]:
    repo_by_addr: dict[str, list[RepoFunction]] = defaultdict(list)
    for item in repo_rows:
        repo_by_addr[item.final_address].append(item)
    ghidra_by_addr = {row["entry"].lower(): row for row in ghidra_rows}

    repo_csv_rows = []
    for item in repo_rows:
        ghidra = ghidra_by_addr.get(item.final_address.lower(), {})
        mapped = bool(ghidra)
        rename_candidate = mapped and AUTO_GHIDRA_NAME_RE.search(ghidra.get("name", "")) is not None
        repo_csv_rows.append({
            "final_psx_address": item.final_address,
            "beta_psx_address": item.beta_address,
            "repo_function": item.function,
            "file": item.file,
            "line": item.line,
            "markers": item.markers,
            "comment": item.comment,
            "mapping_status": "mapped" if mapped else "repo_only",
            "ghidra_entry": ghidra.get("entry", ""),
            "ghidra_name": ghidra.get("name", ""),
            "body_size": ghidra.get("body_size", ""),
            "called_functions": ghidra.get("called_functions", ""),
            "callers": ghidra.get("callers", ""),
            "rename_candidate": "yes" if rename_candidate else "",
        })

    mapped_rows = [row for row in repo_csv_rows if row["mapping_status"] == "mapped"]
    repo_only_rows = [row for row in repo_csv_rows if row["mapping_status"] == "repo_only"]
    ghidra_only_rows = []
    for ghidra in ghidra_rows:
        repo_matches = repo_by_addr.get(ghidra["entry"].lower(), [])
        if repo_matches:
            continue
        ghidra_only_rows.append({
            "entry": ghidra["entry"],
            "ghidra_name": ghidra["name"],
            "body_size": ghidra["body_size"],
            "called_functions": ghidra.get("called_functions", ""),
            "callers": ghidra.get("callers", ""),
            "auto_named": "yes" if AUTO_GHIDRA_NAME_RE.search(ghidra.get("name", "")) else "",
        })

    write_csv(
        generated_dir / "repo-function-map.csv",
        [
            "final_psx_address", "beta_psx_address", "repo_function", "file", "line", "markers", "comment",
            "mapping_status", "ghidra_entry", "ghidra_name", "body_size", "called_functions", "callers", "rename_candidate",
        ],
        repo_csv_rows,
    )
    write_csv(
        generated_dir / "repo-functions.csv",
        ["final_psx_address", "beta_psx_address", "repo_function", "file", "line", "markers", "comment"],
        [
            {
                "final_psx_address": item.final_address,
                "beta_psx_address": item.beta_address,
                "repo_function": item.function,
                "file": item.file,
                "line": item.line,
                "markers": item.markers,
                "comment": item.comment,
            }
            for item in repo_rows
        ],
    )

    common_fields = ["final_psx_address", "repo_function", "file", "line", "markers", "ghidra_name", "body_size", "rename_candidate"]
    write_markdown_table(generated_dir / "mapped-functions.md", "Mapped Ghidra ↔ repo functions", common_fields, mapped_rows, limit=300)
    write_markdown_table(generated_dir / "repo-only-functions.md", "Repo functions without exact Ghidra match", common_fields, repo_only_rows, limit=300)
    write_markdown_table(generated_dir / "unmapped-ghidra-functions.md", "Ghidra functions without exact repo match", ["entry", "ghidra_name", "body_size", "auto_named", "called_functions", "callers"], ghidra_only_rows, limit=300)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ghidra_functions": len(ghidra_rows),
        "repo_functions": len(repo_rows),
        "mapped_functions": len(mapped_rows),
        "repo_only_functions": len(repo_only_rows),
        "ghidra_only_functions": len(ghidra_only_rows),
        "rename_candidates": sum(1 for row in mapped_rows if row.get("rename_candidate") == "yes"),
    }
    (generated_dir / "function-map-summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    mirror_reports_to_docs(repo, generated_dir)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="TOMB5 repo root; default: current directory")
    parser.add_argument("--project-name", default="tomb5_psx_ntsc_map", help="temporary Ghidra project name")
    parser.add_argument("--analysis-timeout", default="300", help="Ghidra analysis timeout per file in seconds")
    parser.add_argument("--keep-project", action="store_true", help="keep the temporary Ghidra project")
    parser.add_argument("--skip-prepare", action="store_true", help="reuse existing prepare_ghidra_psx_summary.json and payload")
    parser.add_argument("--skip-ghidra", action="store_true", help="reuse existing ghidra-functions.csv")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    generated_dir = repo / "build" / "reverse" / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)
    (generated_dir / "map_ghidra_to_repo.log").write_text(f"map_ghidra_to_repo started {datetime.now(timezone.utc).isoformat()}\n", encoding="utf-8")

    payload, text_base = ensure_payload(repo, generated_dir, skip_prepare=args.skip_prepare)
    ghidra_csv = generated_dir / "ghidra-functions.csv"
    if not args.skip_ghidra or not ghidra_csv.exists():
        ghidra_csv = export_ghidra(repo, payload, text_base, generated_dir, args.project_name, args.analysis_timeout, args.keep_project)

    ghidra_rows = read_ghidra_functions(ghidra_csv)
    repo_rows = parse_repo_functions(repo)
    if not repo_rows:
        raise SystemExit("No repo function address comments were parsed")
    summary = build_reports(repo, repo_rows, ghidra_rows, generated_dir)

    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"\nGenerated reports under: {generated_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
