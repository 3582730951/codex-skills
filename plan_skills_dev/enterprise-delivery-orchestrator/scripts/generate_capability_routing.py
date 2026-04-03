#!/usr/bin/env python3
"""Generate a capability-routing table for a delivery task."""

from __future__ import annotations

import argparse
from pathlib import Path


WORK_CLASS_POLICY = {
    "pm_planning": ("frontier", "gpt-5.4", "xhigh", "no", "main_agent_or_frontier", "2", "frontier", "gpt-5.4", "xhigh", "repeat blocker twice", "PM-FRONTIER-XHIGH"),
    "product_definition": ("frontier", "gpt-5.4", "high", "no", "main_agent_or_frontier", "2", "frontier", "gpt-5.4", "xhigh", "output remains vague after one pass", "PRODUCT-FRONTIER-HIGH"),
    "architecture": ("frontier", "gpt-5.4", "xhigh", "no", "main_agent_or_frontier", "2", "frontier", "gpt-5.4", "xhigh", "contract gap appears", "ARCH-FRONTIER-XHIGH"),
    "core_coding": ("frontier", "gpt-5.4", "xhigh", "no", "delegated_frontier", "2", "frontier", "gpt-5.4", "xhigh", "same bug or design confusion twice", "CODE-FRONTIER-XHIGH"),
    "bounded_coding": ("frontier", "gpt-5.4", "high", "no", "delegated_frontier", "2", "frontier", "gpt-5.4", "xhigh", "same bug or design confusion twice", "CODE-FRONTIER-XHIGH"),
    "complex_debugging": ("frontier", "gpt-5.4", "xhigh", "no", "delegated_frontier", "2", "frontier", "gpt-5.4", "xhigh", "same blocker twice", "CODE-FRONTIER-XHIGH"),
    "migration_refactor": ("frontier", "gpt-5.4", "xhigh", "no", "delegated_frontier", "2", "frontier", "gpt-5.4", "xhigh", "behavioral uncertainty appears", "ARCH-FRONTIER-XHIGH"),
    "test_design": ("frontier", "gpt-5.4", "high", "no", "main_agent_or_frontier", "2", "frontier", "gpt-5.4", "high", "coverage gaps remain unclear", "REVIEW-FRONTIER-HIGH"),
    "code_review": ("frontier", "gpt-5.4", "high", "no", "delegated_frontier", "2", "frontier", "gpt-5.4", "high", "review findings stay ambiguous", "REVIEW-FRONTIER-HIGH"),
    "ui_design_review": ("frontier", "gpt-5.4", "xhigh", "no", "delegated_frontier", "2", "frontier", "gpt-5.4", "xhigh", "visual direction stays generic", "REVIEW-FRONTIER-HIGH"),
    "security_review": ("frontier", "gpt-5.4", "xhigh", "no", "main_agent_or_frontier", "2", "frontier", "gpt-5.4", "xhigh", "threat boundary unclear", "SEC-FRONTIER-XHIGH"),
    "systems_review": ("frontier", "gpt-5.4", "xhigh", "no", "main_agent_or_frontier", "2", "frontier", "gpt-5.4", "xhigh", "lifetime or concurrency risk appears", "SYS-FRONTIER-XHIGH"),
    "release_verdict": ("frontier", "gpt-5.4", "xhigh", "no", "main_agent_or_frontier", "2", "frontier", "gpt-5.4", "xhigh", "evidence or risk is incomplete", "PM-FRONTIER-XHIGH"),
    "repo_retrieval": ("fast", "gpt-5.1-codex-mini", "medium", "yes", "delegated_fast", "2", "standard", "gpt-5.2", "high", "missing context after one pass", "RETRIEVAL-FAST-MEDIUM"),
    "doc_extraction": ("fast", "gpt-5.1-codex-mini", "medium", "yes", "delegated_fast", "2", "standard", "gpt-5.2", "high", "missing context after one pass", "RETRIEVAL-FAST-MEDIUM"),
    "artifact_packaging": ("fast", "gpt-5.1-codex-mini", "low", "yes", "delegated_fast", "2", "standard", "gpt-5.2", "medium", "packaging mismatch", "PACKAGING-FAST-LOW"),
    "test_execution": ("fast", "gpt-5.1-codex-mini", "medium", "yes", "delegated_fast", "2", "standard", "gpt-5.2", "high", "test output unclear", "TEST-EXEC-FAST-MEDIUM"),
    "smoke_test": ("fast", "gpt-5.1-codex-mini", "low", "yes", "delegated_fast", "2", "standard", "gpt-5.2", "medium", "smoke result unclear", "TEST-EXEC-FAST-MEDIUM"),
    "screenshot_capture": ("fast", "gpt-5.1-codex-mini", "low", "yes", "delegated_fast", "2", "standard", "gpt-5.2", "medium", "capture missing required view", "PACKAGING-FAST-LOW"),
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
        (
            tier,
            model,
            reasoning,
            downgrade,
            execution_preference,
            stall_attempt_limit,
            escalation_target_tier,
            escalation_target_model,
            escalation_target_reasoning,
            escalation,
            delegation_template_id,
        ) = WORK_CLASS_POLICY[work_class]
        entries.append(
            [
                f"- work_item_id: {work_id}",
                f"  work_class: {work_class}",
                f"  owner_role: {owner_role}",
                f"  required_model_tier: {tier}",
                f"  preferred_model: {model}",
                f"  reasoning_effort: {reasoning}",
                f"  downgrade_allowed: {downgrade}",
                f"  execution_preference: {execution_preference}",
                f"  stall_attempt_limit: {stall_attempt_limit}",
                f"  escalation_target_tier: {escalation_target_tier}",
                f"  escalation_target_model: {escalation_target_model}",
                f"  escalation_target_reasoning: {escalation_target_reasoning}",
                f"  escalation_trigger: {escalation}",
                f"  delegation_template_id: {delegation_template_id}",
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
            "  execution_preference:",
            "  stall_attempt_limit:",
            "  escalation_target_tier:",
            "  escalation_target_model:",
            "  escalation_target_reasoning:",
            "  escalation_trigger:",
            "  delegation_template_id:",
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
