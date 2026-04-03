#!/usr/bin/env python3
"""Validate capability routing for critical work classes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


CRITICAL_CLASSES = {
    "pm_planning",
    "product_definition",
    "architecture",
    "core_coding",
    "bounded_coding",
    "complex_debugging",
    "migration_refactor",
    "test_design",
    "code_review",
    "ui_design_review",
    "security_review",
    "systems_review",
    "release_verdict",
}

LIGHT_CLASSES = {
    "repo_retrieval",
    "doc_extraction",
    "artifact_packaging",
    "test_execution",
    "smoke_test",
    "screenshot_capture",
}


def collect_text(root: Path) -> str:
    chunks: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        try:
            chunks.append(path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            continue
    return "\n\n".join(chunks)


def parse_entries(text: str) -> list[dict[str, str]]:
    marker = "Capability Routing Table:"
    start = text.find(marker)
    if start == -1:
        return []
    section = text[start + len(marker):]
    lines = section.splitlines()

    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw_line in lines:
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if line.startswith("- work_item_id:"):
            if current:
                entries.append(current)
            current = {"work_item_id": line.split(":", 1)[1].strip()}
            continue
        if current is None:
            continue
        match = re.match(r"\s+([a-z_]+):\s*(.*)$", line)
        if match:
            current[match.group(1)] = match.group(2).strip()
    if current:
        entries.append(current)
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description="Check capability routing against the policy.")
    parser.add_argument("--artifact-dir", required=True)
    parser.add_argument("--format", choices={"markdown", "json"}, default="markdown")
    args = parser.parse_args()

    root = Path(args.artifact_dir).resolve()
    if not root.exists():
        print(f"Artifact directory does not exist: {root}", file=sys.stderr)
        return 2

    text = collect_text(root)
    entries = parse_entries(text)
    findings: list[str] = []

    if not entries:
        findings.append("Capability Routing Table is missing or empty")

    for entry in entries:
        work_id = entry.get("work_item_id", "<unknown>")
        work_class = entry.get("work_class", "")
        tier = entry.get("required_model_tier", "")
        reasoning = entry.get("reasoning_effort", "")
        downgrade = entry.get("downgrade_allowed", "")
        escalation = entry.get("escalation_trigger", "")

        if not work_class:
            findings.append(f"{work_id}: work_class is missing")
            continue

        if work_class in CRITICAL_CLASSES:
            if tier != "frontier":
                findings.append(f"{work_id}: critical work class {work_class} must use frontier tier")
            if reasoning not in {"high", "xhigh"}:
                findings.append(f"{work_id}: critical work class {work_class} must use high or xhigh reasoning")
            if downgrade != "no":
                findings.append(f"{work_id}: critical work class {work_class} must not allow downgrade")
        elif work_class in LIGHT_CLASSES:
            if tier not in {"fast", "standard"}:
                findings.append(f"{work_id}: light work class {work_class} should use fast or standard tier")
            if reasoning not in {"low", "medium"}:
                findings.append(f"{work_id}: light work class {work_class} should use low or medium reasoning")
        else:
            findings.append(f"{work_id}: unknown work class {work_class}")

        if not escalation:
            findings.append(f"{work_id}: escalation_trigger is missing")

    if args.format == "json":
        print(
            json.dumps(
                {
                    "artifact_dir": str(root),
                    "entry_count": len(entries),
                    "findings": findings,
                    "gate_result": "fail" if findings else "pass",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print("Capability Routing Check:")
        print(f"- gate_result: {'fail' if findings else 'pass'}")
        print(f"- entry_count: {len(entries)}")
        print("Findings:")
        if findings:
            for finding in findings:
                print(f"- {finding}")
        else:
            print("- none")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
