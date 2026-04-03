#!/usr/bin/env python3
"""Generate a capability-routing table for a delivery task."""

from __future__ import annotations

import argparse
from pathlib import Path


WORK_CLASS_POLICY = {
    "pm_planning": ("frontier", "gpt-5.4", "xhigh", "no", "repeat blocker twice"),
    "product_definition": ("frontier", "gpt-5.4", "high", "no", "output remains vague after one pass"),
    "architecture": ("frontier", "gpt-5.4", "xhigh", "no", "contract gap appears"),
    "core_coding": ("frontier", "gpt-5.4", "xhigh", "no", "same bug or design confusion twice"),
    "bounded_coding": ("frontier", "gpt-5.4", "high", "no", "same bug or design confusion twice"),
    "complex_debugging": ("frontier", "gpt-5.4", "xhigh", "no", "same blocker twice"),
    "migration_refactor": ("frontier", "gpt-5.4", "xhigh", "no", "behavioral uncertainty appears"),
    "test_design": ("frontier", "gpt-5.4", "high", "no", "coverage gaps remain unclear"),
    "code_review": ("frontier", "gpt-5.4", "high", "no", "review findings stay ambiguous"),
    "ui_design_review": ("frontier", "gpt-5.4", "xhigh", "no", "visual direction stays generic"),
    "security_review": ("frontier", "gpt-5.4", "xhigh", "no", "threat boundary unclear"),
    "systems_review": ("frontier", "gpt-5.4", "xhigh", "no", "lifetime or concurrency risk appears"),
    "release_verdict": ("frontier", "gpt-5.4", "xhigh", "no", "evidence or risk is incomplete"),
    "repo_retrieval": ("fast", "gpt-5.1-codex-mini", "medium", "yes", "missing context after one pass"),
    "doc_extraction": ("fast", "gpt-5.1-codex-mini", "medium", "yes", "missing context after one pass"),
    "artifact_packaging": ("fast", "gpt-5.1-codex-mini", "low", "yes", "packaging mismatch"),
    "test_execution": ("fast", "gpt-5.1-codex-mini", "medium", "yes", "test output unclear"),
    "smoke_test": ("fast", "gpt-5.1-codex-mini", "low", "yes", "smoke result unclear"),
    "screenshot_capture": ("fast", "gpt-5.1-codex-mini", "low", "yes", "capture missing required view"),
}


def parse_item(item: str) -> tuple[str, str, str]:
    parts = item.split(":", 2)
    if len(parts) != 3:
        raise ValueError(f"Expected WORK_ID:WORK_CLASS:OWNER_ROLE, got: {item}")
    return parts[0].strip(), parts[1].strip(), parts[2].strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a capability-routing table.")
    parser.add_argument("--artifact-dir", required=True)
    parser.add_argument("--item", action="append", default=[], help="WORK_ID:WORK_CLASS:OWNER_ROLE")
    parser.add_argument("--output-name", default="capability-routing.md")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    root = Path(args.artifact_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    output = root / args.output_name
    if output.exists() and not args.overwrite:
        raise FileExistsError(f"{output} already exists")

    entries: list[list[str]] = []
    for item in args.item:
        work_id, work_class, owner_role = parse_item(item)
        if work_class not in WORK_CLASS_POLICY:
            raise ValueError(f"Unknown work class: {work_class}")
        tier, model, reasoning, downgrade, escalation = WORK_CLASS_POLICY[work_class]
        entries.append(
            [
                f"- work_item_id: {work_id}",
                f"  work_class: {work_class}",
                f"  owner_role: {owner_role}",
                f"  required_model_tier: {tier}",
                f"  preferred_model: {model}",
                f"  reasoning_effort: {reasoning}",
                f"  downgrade_allowed: {downgrade}",
                f"  escalation_trigger: {escalation}",
                "  notes:",
            ]
        )

    if not entries:
        entries = [[
            "- work_item_id:",
            "  work_class:",
            "  owner_role:",
            "  required_model_tier:",
            "  preferred_model:",
            "  reasoning_effort:",
            "  downgrade_allowed:",
            "  escalation_trigger:",
            "  notes:",
        ]]

    lines = ["Capability Routing Table:"]
    for entry in entries:
        lines.extend(entry)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Capability routing written to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
