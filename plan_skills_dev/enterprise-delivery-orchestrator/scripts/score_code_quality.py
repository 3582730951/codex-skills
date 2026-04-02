#!/usr/bin/env python3
"""Heuristic code-quality scorer aligned with the delivery rubric."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SUPPORTED_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".java", ".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".rs"}
SKIP_DIRS = {".git", ".venv", "node_modules", "dist", "build", "target", "__pycache__"}

GENERIC_NAME_PATTERN = re.compile(
    r"\b(processData|handleThing|doStuff|foo|bar|baz|ServiceManager|HelperUtil|CardGridSection|tempValue)\b"
)
TODO_PATTERN = re.compile(r"\b(TODO|FIXME|XXX)\b")
BROAD_EXCEPT_PATTERN = re.compile(r"^\s*except(\s+Exception)?\s*:\s*$|^\s*except\s+Exception\b")
TS_ANY_PATTERN = re.compile(r"\bany\b|as unknown as")
CPP_RAW_PATTERN = re.compile(r"\b(new|delete)\b")
JAVA_GENERIC_CLASS_PATTERN = re.compile(r"\bclass\s+\w*(Manager|Helper|Util)\b")
AUDIT_TAG_PATTERN = re.compile(r"(AUTHORIZATION:|AUDIT:|SECURITY-BOUNDARY:|PROVENANCE:)")
SENSITIVE_SURFACE_PATTERN = re.compile(
    r"\b(unsafe|ffi|syscall|ioctl|ptrace|mprotect|OpenProcess|LoadLibrary|VirtualAlloc|CreateService|registry|launchd|systemd|setuid|cap_set|driver|kernel|auditd|ebpf|netlink)\b",
    re.IGNORECASE,
)


@dataclass
class Finding:
    path: str
    line: int
    message: str


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)
    return sorted(files)


def safe_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return []


def clamp(score: float) -> float:
    return max(0.0, min(5.0, score))


def analyze(root: Path) -> tuple[dict[str, float], list[Finding]]:
    findings: list[Finding] = []
    scores = {
        "naming_quality": 5.0,
        "function_responsibility": 5.0,
        "api_predictability": 5.0,
        "error_handling_consistency": 5.0,
        "resource_lifetime_safety": 5.0,
        "testability": 5.0,
        "auditability": 5.0,
        "repository_consistency": 5.0,
        "low_ai_smell": 5.0,
    }

    files = iter_files(root)
    test_files = [path for path in files if "test" in path.name.lower() or "tests" in path.parts]
    if not test_files:
        scores["testability"] -= 2.0
        findings.append(Finding(path=".", line=1, message="No test files detected"))

    for path in files:
        lines = safe_lines(path)
        rel_path = str(path.relative_to(root))
        header = "\n".join(lines[:60])
        sensitive_file = any(keyword in rel_path.lower() for keyword in ("protect", "security", "kernel", "driver", "runtime", "daemon", "service", "vmp"))

        if len(lines) > 600:
            scores["function_responsibility"] -= 0.5
            scores["repository_consistency"] -= 0.5
            findings.append(Finding(rel_path, 1, "File exceeds 600 lines; verify boundary and scope"))

        for index, line in enumerate(lines, start=1):
            if GENERIC_NAME_PATTERN.search(line):
                scores["naming_quality"] -= 0.6
                scores["low_ai_smell"] -= 0.6
                findings.append(Finding(rel_path, index, "Generic or template-like naming"))

            if TODO_PATTERN.search(line):
                scores["repository_consistency"] -= 0.2
                findings.append(Finding(rel_path, index, "TODO/FIXME left in code"))

            if path.suffix == ".py" and BROAD_EXCEPT_PATTERN.search(line):
                scores["error_handling_consistency"] -= 1.0
                findings.append(Finding(rel_path, index, "Broad Python exception handling"))

            if path.suffix in {".ts", ".tsx", ".js", ".jsx"} and TS_ANY_PATTERN.search(line):
                scores["api_predictability"] -= 0.8
                scores["low_ai_smell"] -= 0.4
                findings.append(Finding(rel_path, index, "TypeScript any-cast or loose type escape"))

            if path.suffix in {".cpp", ".cc", ".cxx", ".hpp", ".h"} and CPP_RAW_PATTERN.search(line):
                scores["resource_lifetime_safety"] -= 0.4
                findings.append(Finding(rel_path, index, "C++ raw new/delete detected"))

            if path.suffix == ".java" and JAVA_GENERIC_CLASS_PATTERN.search(line):
                scores["naming_quality"] -= 0.5
                scores["low_ai_smell"] -= 0.5
                findings.append(Finding(rel_path, index, "Generic Java class name such as Manager/Helper/Util"))

            if path.suffix == ".rs" and "unsafe" in line:
                context = "\n".join(lines[max(0, index - 3): index + 1])
                if "SAFETY:" not in context:
                    scores["resource_lifetime_safety"] -= 1.2
                    findings.append(Finding(rel_path, index, "Rust unsafe without nearby SAFETY explanation"))

            if SENSITIVE_SURFACE_PATTERN.search(line):
                sensitive_file = True

        if sensitive_file and not AUDIT_TAG_PATTERN.search(header):
            scores["auditability"] -= 1.5
            scores["repository_consistency"] -= 0.5
            findings.append(Finding(rel_path, 1, "Sensitive file lacks audit annotations near file header"))

    for key, value in list(scores.items()):
        scores[key] = clamp(round(value, 2))
    return scores, findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Score code quality heuristically.")
    parser.add_argument("--root", required=True)
    parser.add_argument("--fail-under", type=float, default=4.0)
    parser.add_argument("--format", choices={"markdown", "json"}, default="markdown")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Path does not exist: {root}", file=sys.stderr)
        return 2

    scores, findings = analyze(root)
    failing_dimensions = [name for name, value in scores.items() if value < args.fail_under]

    if args.format == "json":
        payload = {
            "root": str(root),
            "scores": scores,
            "failing_dimensions": failing_dimensions,
            "findings": [finding.__dict__ for finding in findings],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("Code Quality Scorecard:")
        for name, value in scores.items():
            print(f"- {name}: {value}")
        print(f"- fail_under: {args.fail_under}")
        print(f"- gate_result: {'fail' if failing_dimensions else 'pass'}")
        print("Findings:")
        if findings:
            for finding in findings:
                print(f"- {finding.path}:{finding.line}: {finding.message}")
        else:
            print("- none")

    return 1 if failing_dimensions else 0


if __name__ == "__main__":
    raise SystemExit(main())
