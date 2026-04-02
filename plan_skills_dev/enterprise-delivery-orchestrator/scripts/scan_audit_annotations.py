#!/usr/bin/env python3
"""Check that sensitive code carries audit and authorization annotations."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SUPPORTED_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".java", ".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".rs"}
SKIP_DIRS = {".git", ".venv", "node_modules", "dist", "build", "target", "__pycache__"}
SENSITIVE_PATTERN = re.compile(
    r"\b(unsafe|ffi|syscall|ioctl|ptrace|mprotect|OpenProcess|LoadLibrary|VirtualAlloc|CreateService|registry|launchd|systemd|setuid|cap_set|driver|kernel|auditd|ebpf|netlink)\b",
    re.IGNORECASE,
)
REQUIRED_TAGS = ("AUTHORIZATION:", "AUDIT:")
OPTIONAL_GROUPS = (("SECURITY-BOUNDARY:", "PROVENANCE:"),)
REQUIRED_DOCS = (
    "docs/authorization-manifest.md",
    "docs/audit-annotation-register.md",
    "docs/source-provenance-register.md",
)


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)
    return sorted(files)


def scan_header(lines: list[str]) -> str:
    return "\n".join(lines[:60])


def file_is_sensitive(path: Path, lines: list[str]) -> bool:
    rel = str(path).lower()
    if any(keyword in rel for keyword in ("vmp", "protect", "security", "kernel", "driver", "runtime", "daemon", "service")):
        return True
    return any(SENSITIVE_PATTERN.search(line) for line in lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan audit annotations in sensitive code.")
    parser.add_argument("--root", required=True)
    parser.add_argument("--format", choices={"markdown", "json"}, default="markdown")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Path does not exist: {root}", file=sys.stderr)
        return 2

    findings: list[str] = []
    sensitive_files: list[str] = []
    for relative_doc in REQUIRED_DOCS:
        if not (root / relative_doc).exists():
            findings.append(f"{relative_doc} is missing")

    for path in iter_files(root):
        rel = str(path.relative_to(root))
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue

        if not file_is_sensitive(path.relative_to(root), lines):
            continue

        sensitive_files.append(rel)
        header = scan_header(lines)
        for tag in REQUIRED_TAGS:
            if tag not in header:
                findings.append(f"{rel}: missing {tag} annotation near file header")
        for group in OPTIONAL_GROUPS:
            if not any(tag in header for tag in group):
                group_text = " or ".join(group)
                findings.append(f"{rel}: missing one of {group_text} near file header")

    if args.format == "json":
        print(
            json.dumps(
                {
                    "root": str(root),
                    "sensitive_files": sensitive_files,
                    "findings": findings,
                    "gate_result": "fail" if findings else "pass",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print("Audit Annotation Checks:")
        print(f"- gate_result: {'fail' if findings else 'pass'}")
        if sensitive_files:
            print("- sensitive_files:")
            for rel in sensitive_files:
                print(f"- {rel}")
        else:
            print("- sensitive_files: none")
        if findings:
            print("Findings:")
            for finding in findings:
                print(f"- {finding}")
        else:
            print("Findings:")
            print("- none")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
