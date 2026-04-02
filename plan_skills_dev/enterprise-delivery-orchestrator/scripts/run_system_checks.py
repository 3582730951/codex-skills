#!/usr/bin/env python3
"""Run bounded static checks for defensive system-tool projects."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SKIP_DIRS = {".git", ".venv", "node_modules", "dist", "build", "target", "__pycache__"}
SHELL_TRUE = re.compile(r"shell\s*=\s*True")
OS_SYSTEM = re.compile(r"\bos\.system\s*\(")
POWERFUL_WINDOWS = re.compile(r"\b(CreateRemoteThread|WriteProcessMemory|SetWindowsHookEx)\b")
LINUX_STEALTH = re.compile(r"\b(insmod|modprobe|LD_PRELOAD)\b")
RUST_UNSAFE = re.compile(r"\bunsafe\b")


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
    return sorted(files)


def scan_file(root: Path, path: Path) -> list[str]:
    rel = path.relative_to(root)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return []

    findings: list[str] = []
    for index, line in enumerate(lines, start=1):
        if SHELL_TRUE.search(line):
            findings.append(f"{rel}:{index}: shell=True requires explicit justification")
        if OS_SYSTEM.search(line):
            findings.append(f"{rel}:{index}: os.system detected; prefer direct APIs")
        if POWERFUL_WINDOWS.search(line):
            findings.append(f"{rel}:{index}: sensitive Windows process-manipulation API detected")
        if LINUX_STEALTH.search(line):
            findings.append(f"{rel}:{index}: stealthy or invasive Linux mechanism detected")
        if path.suffix == ".rs" and RUST_UNSAFE.search(line):
            findings.append(f"{rel}:{index}: unsafe Rust requires manual safety review")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Run bounded static checks for defensive system tools.")
    parser.add_argument("--root", required=True)
    parser.add_argument("--format", choices={"markdown", "json"}, default="markdown")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Path does not exist: {root}", file=sys.stderr)
        return 2

    findings: list[str] = []
    for path in iter_files(root):
        findings.extend(scan_file(root, path))

    docs_findings = []
    if not (root / "docs" / "permission-model.md").exists():
        docs_findings.append("docs/permission-model.md is missing")
    if not (root / "docs" / "threat-model.md").exists():
        docs_findings.append("docs/threat-model.md is missing")
    findings.extend(docs_findings)

    if args.format == "json":
        print(json.dumps({"root": str(root), "findings": findings}, ensure_ascii=False, indent=2))
    else:
        print("System Checks:")
        if findings:
            print("- gate_result: fail")
            for finding in findings:
                print(f"- {finding}")
        else:
            print("- gate_result: pass")
            print("- no findings")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
