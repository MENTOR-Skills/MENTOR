#!/usr/bin/env python3
"""Render an F3 Markdown report to a same-name PDF with Pandoc and XeLaTeX."""

from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE = SKILL_DIR / "assets" / "paper-note.tex"
METADATA = SKILL_DIR / "assets" / "metadata.yaml"


def _fallback_dirs(name: str) -> list[Path]:
    directories = [
        Path.home() / "AppData" / "Local" / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64",
        Path("C:/Program Files/MiKTeX/miktex/bin/x64"),
        Path("C:/Program Files (x86)/MiKTeX/miktex/bin/x64"),
    ]
    if name == "pandoc":
        winget = Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Packages"
        if winget.is_dir():
            directories.extend(path.parent for path in winget.glob("JohnMacFarlane.Pandoc_*/*/pandoc.exe"))
    return directories


def find_executable(name: str) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    for directory in _fallback_dirs(name):
        found = shutil.which(name, path=str(directory))
        if found:
            return found
    return None


def quote_command(command: list[str]) -> str:
    if sys.platform == "win32":
        return subprocess.list2cmdline(command)
    return " ".join(shlex.quote(part) for part in command)


def retry_command(note_path: Path) -> str:
    return quote_command([sys.executable, str(Path(__file__).resolve()), str(note_path)])


def build_command(pandoc: str, note_path: Path, output_path: Path, build_dir: Path) -> list[str]:
    return [
        pandoc,
        str(note_path),
        "-o",
        str(output_path),
        "--pdf-engine=xelatex",
        f"--template={TEMPLATE}",
        f"--metadata-file={METADATA}",
        "--toc",
        "--toc-depth=3",
        "--shift-heading-level-by=-1",
        "--syntax-highlighting=tango",
        "--standalone",
        f"--resource-path={note_path.parent}",
        f"--pdf-engine-opt=-output-directory={build_dir}",
    ]


def explain_missing_dependency(name: str) -> str:
    if name == "pandoc":
        return "Pandoc is missing. Install it with: winget install --id JohnMacFarlane.Pandoc"
    if name == "xelatex":
        return "XeLaTeX is missing. Install MiKTeX with: winget install --id MiKTeX.MiKTeX"
    return f"Missing dependency: {name}"


def report_render_failure(reason: str, note_path: Path, details: list[str] | None = None) -> None:
    print("Markdown saved, but PDF rendering failed.", file=sys.stderr)
    print(reason, file=sys.stderr)
    print(f"Retry: {retry_command(note_path)}", file=sys.stderr)
    for line in details or []:
        print(line, file=sys.stderr)


def render(note_path: Path, output_path: Path | None = None) -> int:
    note_path = note_path.resolve()
    if not note_path.is_file():
        print(f"ERROR: note file not found: {note_path}", file=sys.stderr)
        return 2

    output_path = (output_path or note_path.with_suffix(".pdf")).resolve()
    if output_path == note_path:
        print("ERROR: output path must differ from the Markdown input.", file=sys.stderr)
        return 2
    if output_path.suffix.lower() != ".pdf":
        print("ERROR: output path must end in .pdf.", file=sys.stderr)
        return 2
    if not output_path.parent.is_dir():
        print(f"ERROR: output directory not found: {output_path.parent}", file=sys.stderr)
        return 2
    if not TEMPLATE.is_file() or not METADATA.is_file():
        missing = TEMPLATE if not TEMPLATE.is_file() else METADATA
        print(f"ERROR: rendering resource missing: {missing}", file=sys.stderr)
        return 4

    executables: dict[str, str] = {}
    for name in ("pandoc", "xelatex"):
        found = find_executable(name)
        if not found:
            report_render_failure(explain_missing_dependency(name), note_path)
            return 3
        executables[name] = found

    with tempfile.TemporaryDirectory(prefix=".paper-deep-read-", dir=output_path.parent) as temp_dir:
        temp_root = Path(temp_dir)
        build_dir = temp_root / "build"
        build_dir.mkdir()
        temp_pdf = temp_root / output_path.name
        command = build_command(executables["pandoc"], note_path, temp_pdf, build_dir)

        env = os.environ.copy()
        xelatex_dir = str(Path(executables["xelatex"]).parent)
        path_parts = [part for part in env.get("PATH", "").split(os.pathsep) if part and Path(part).is_dir()]
        env["PATH"] = os.pathsep.join([xelatex_dir, *path_parts])
        result = subprocess.run(
            command,
            cwd=note_path.parent,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )

        if result.returncode != 0 or not temp_pdf.is_file() or temp_pdf.stat().st_size == 0:
            details: list[str] = []
            if result.stdout.strip():
                details.extend(("--- pandoc stdout ---", result.stdout[-4000:]))
            if result.stderr.strip():
                details.extend(("--- pandoc stderr ---", result.stderr[-4000:]))
            report_render_failure("Pandoc or XeLaTeX did not produce a valid PDF.", note_path, details)
            return result.returncode or 5

        try:
            os.replace(temp_pdf, output_path)
        except OSError as exc:
            print("Markdown saved, but final PDF write failed.", file=sys.stderr)
            print("The target PDF may be open or locked.", file=sys.stderr)
            print(f"System error: {exc}", file=sys.stderr)
            return 6

    print(f"PDF written: {output_path}")
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass
    parser = argparse.ArgumentParser(description="Render an F3 Markdown report to PDF")
    parser.add_argument("note", help="Path to reading-reports/<id>.md")
    parser.add_argument("-o", "--output", help="Optional output PDF path")
    args = parser.parse_args()
    return render(Path(args.note), Path(args.output) if args.output else None)


if __name__ == "__main__":
    raise SystemExit(main())
