#!/usr/bin/env python3
"""Check whether execution artifacts stay aligned with the locked plan."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


MARKERS = [
    "Requirement-to-Change Map:",
    "Claim-to-Evidence Map:",
    "Test Matrix + Evidence Log:",
    "Execution Contract:",
    "Plan Coverage Matrix:",
    "Execution Ledger:",
]


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


def extract_section(text: str, marker: str) -> str:
    start = text.find(marker)
    if start == -1:
        return ""
    start += len(marker)
    next_positions = [text.find(other, start) for other in MARKERS if other != marker and text.find(other, start) != -1]
    end = min(next_positions) if next_positions else len(text)
    return text[start:end]


def parse_token_list(value: str) -> set[str]:
    raw = value.replace("[", " ").replace("]", " ").replace("|", " ").replace("/", " ")
    tokens = {token.strip(",") for token in re.split(r"[\s,]+", raw) if token.strip(",")}
    return {token for token in tokens if token not in {"-", "none", "n/a"}}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check execution alignment against the locked plan.")
    parser.add_argument("--artifact-dir", required=True)
    parser.add_argument("--format", choices={"markdown", "json"}, default="markdown")
    args = parser.parse_args()

    root = Path(args.artifact_dir).resolve()
    if not root.exists():
        print(f"Artifact directory does not exist: {root}", file=sys.stderr)
        return 2

    text = collect_text(root)
    req_section = extract_section(text, "Requirement-to-Change Map:")
    claim_section = extract_section(text, "Claim-to-Evidence Map:")
    test_section = extract_section(text, "Test Matrix + Evidence Log:")
    coverage_section = extract_section(text, "Plan Coverage Matrix:")
    ledger_section = extract_section(text, "Execution Ledger:")

    requirement_ids = set(re.findall(r"(?m)^\s*-\s*requirement_id:\s*(\S+)", req_section))
    coverage_ids = set(re.findall(r"(?m)^\s*-\s*requirement_id:\s*(\S+)", coverage_section))

    coverage_step_ids: set[str] = set()
    for value in re.findall(r"(?m)^\s*plan_step_ids:\s*(.+)$", coverage_section):
        coverage_step_ids.update(parse_token_list(value))

    ledger_step_ids = set(re.findall(r"(?m)^\s*plan_step_id:\s*(\S+)", ledger_section))

    evidence_requirement_ids: set[str] = set()
    for value in re.findall(r"(?m)^\s*related_requirements:\s*(.+)$", claim_section):
        evidence_requirement_ids.update(parse_token_list(value))
    for value in re.findall(r"(?m)^\s*requirement_ids:\s*(.+)$", test_section):
        evidence_requirement_ids.update(parse_token_list(value))
    for value in re.findall(r"(?m)^\s*requirement_ids:\s*(.+)$", ledger_section):
        evidence_requirement_ids.update(parse_token_list(value))

    drift_values = [value.strip() for value in re.findall(r"(?m)^\s*drift_status:\s*(.+)$", ledger_section)]
    invalid_drift = [value for value in drift_values if value not in {"in_plan", "replanned", ""}]

    findings: list[str] = []
    if not requirement_ids:
        findings.append("no requirement_id entries found in Requirement-to-Change Map")
    if not coverage_ids:
        findings.append("no requirement_id entries found in Plan Coverage Matrix")
    if not ledger_step_ids:
        findings.append("no plan_step_id entries found in Execution Ledger")

    missing_coverage = sorted(requirement_ids - coverage_ids)
    missing_evidence = sorted(requirement_ids - evidence_requirement_ids)
    unknown_steps = sorted(step for step in ledger_step_ids if step not in coverage_step_ids)

    for requirement_id in missing_coverage:
        findings.append(f"requirement missing plan coverage: {requirement_id}")
    for requirement_id in missing_evidence:
        findings.append(f"requirement missing evidence linkage: {requirement_id}")
    for step_id in unknown_steps:
        findings.append(f"execution step not present in Plan Coverage Matrix: {step_id}")
    for drift in invalid_drift:
        findings.append(f"invalid drift_status value: {drift}")

    if args.format == "json":
        print(
            json.dumps(
                {
                    "artifact_dir": str(root),
                    "requirement_ids": sorted(requirement_ids),
                    "coverage_ids": sorted(coverage_ids),
                    "ledger_step_ids": sorted(ledger_step_ids),
                    "findings": findings,
                    "gate_result": "fail" if findings else "pass",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print("Execution Alignment Check:")
        print(f"- gate_result: {'fail' if findings else 'pass'}")
        print(f"- requirement_count: {len(requirement_ids)}")
        print(f"- covered_requirement_count: {len(coverage_ids)}")
        print(f"- ledger_step_count: {len(ledger_step_ids)}")
        print("Findings:")
        if findings:
            for finding in findings:
                print(f"- {finding}")
        else:
            print("- none")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
