#!/usr/bin/env python3
"""Score plan completeness for execution readiness."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SECTION_MARKERS = [
    "Task Charter:",
    "Product/Experience Brief:",
    "Architecture Contract:",
    "Requirement-to-Change Map:",
    "Test Matrix + Evidence Log:",
    "Release Readiness Checklist:",
    "Execution Contract:",
    "Capability Routing Table:",
    "Delegation Template Table:",
    "Spawn Agent Template Table:",
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


def has_all(text: str, fields: list[str]) -> list[str]:
    return [field for field in fields if field not in text]


def clamp(value: float) -> float:
    return max(0.0, min(5.0, round(value, 2)))


def analyze(text: str) -> tuple[dict[str, float], list[str]]:
    findings: list[str] = []
    scores = {
        "scope_clarity": 5.0,
        "contract_completeness": 5.0,
        "execution_readiness": 5.0,
        "validation_readiness": 5.0,
        "de_scope_honesty": 5.0,
    }

    missing_scope = has_all(
        text,
        [
            "Task Charter:",
            "- Objective:",
            "- Deliverables:",
            "- In Scope:",
            "- Out of Scope:",
            "- Acceptance criteria:",
            "Product/Experience Brief:",
            "- Target user:",
        ],
    )
    if missing_scope:
        scores["scope_clarity"] -= 0.4 * len(missing_scope)
        findings.extend(f"scope missing: {field}" for field in missing_scope)

    missing_contracts = has_all(
        text,
        [
            "Architecture Contract:",
            "- Boundaries:",
            "- Owned modules / files:",
            "- APIs / contracts:",
            "- Function boundaries:",
            "- Regression perimeter:",
        ],
    )
    if missing_contracts:
        scores["contract_completeness"] -= 0.5 * len(missing_contracts)
        findings.extend(f"contract missing: {field}" for field in missing_contracts)

    missing_execution = has_all(
        text,
        [
            "Execution Contract:",
            "Capability Routing Table:",
            "Delegation Template Table:",
            "Spawn Agent Template Table:",
            "- release_slice:",
            "- plan_lock_version:",
            "- ordered_steps:",
            "Plan Coverage Matrix:",
            "Execution Ledger:",
        ],
    )
    if missing_execution:
        scores["execution_readiness"] -= 0.6 * len(missing_execution)
        findings.extend(f"execution missing: {field}" for field in missing_execution)

    missing_validation = has_all(
        text,
        [
            "Requirement-to-Change Map:",
            "Test Matrix + Evidence Log:",
            "Claim-to-Evidence Map:",
            "Release Readiness Checklist:",
            "- Tests executed:",
            "- Delivery status:",
        ],
    )
    if missing_validation:
        scores["validation_readiness"] -= 0.5 * len(missing_validation)
        findings.extend(f"validation missing: {field}" for field in missing_validation)

    missing_honesty = has_all(
        text,
        [
            "- Out of Scope:",
            "- Non-goals:",
            "- blocked_by:",
        ],
    )
    if missing_honesty:
        scores["de_scope_honesty"] -= 0.7 * len(missing_honesty)
        findings.extend(f"de-scope missing: {field}" for field in missing_honesty)

    requirement_count = len(re.findall(r"(?m)^\s*-\s*requirement_id:\s*\S+", text))
    step_count = len(re.findall(r"(?m)^\s*-\s*step_id:\s*\S*", text))
    test_count = len(re.findall(r"(?m)^\s*-\s*test_id:\s*\S*", text))
    if requirement_count == 0:
        scores["scope_clarity"] -= 1.2
        scores["execution_readiness"] -= 1.2
        findings.append("no requirement_id entries found")
    if step_count == 0:
        scores["execution_readiness"] -= 1.5
        findings.append("no step_id entries found in Execution Contract")
    if test_count == 0:
        scores["validation_readiness"] -= 1.2
        findings.append("no test_id entries found")

    for key in list(scores):
        scores[key] = clamp(scores[key])
    return scores, findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Score plan completeness for execution readiness.")
    parser.add_argument("--artifact-dir", required=True)
    parser.add_argument("--fail-under", type=float, default=4.0)
    parser.add_argument("--format", choices={"markdown", "json"}, default="markdown")
    args = parser.parse_args()

    root = Path(args.artifact_dir).resolve()
    if not root.exists():
        print(f"Artifact directory does not exist: {root}", file=sys.stderr)
        return 2

    text = collect_text(root)
    scores, findings = analyze(text)
    failing_dimensions = [name for name, value in scores.items() if value < args.fail_under]

    if args.format == "json":
        print(
            json.dumps(
                {
                    "artifact_dir": str(root),
                    "scores": scores,
                    "failing_dimensions": failing_dimensions,
                    "findings": findings,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print("Plan Quality Scorecard:")
        for name, value in scores.items():
            print(f"- {name}: {value}")
        print(f"- fail_under: {args.fail_under}")
        print(f"- gate_result: {'fail' if failing_dimensions else 'pass'}")
        print("Findings:")
        if findings:
            for finding in findings:
                print(f"- {finding}")
        else:
            print("- none")

    return 1 if failing_dimensions else 0


if __name__ == "__main__":
    raise SystemExit(main())
