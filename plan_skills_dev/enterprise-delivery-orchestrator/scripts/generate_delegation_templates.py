#!/usr/bin/env python3
"""Generate reusable delegation templates for roles and work classes."""

from __future__ import annotations

import argparse
from pathlib import Path


TEMPLATES = {
    "PM-FRONTIER-XHIGH": {
        "owner_role": "PM / Delivery Lead",
        "agent_type": "default",
        "model": "gpt-5.4",
        "reasoning_effort": "xhigh",
        "fork_context": "true",
        "execution_preference": "main_agent_or_frontier",
        "use_when": "planning, release truthfulness, scope cuts, final verdict",
        "keep_local_if_unavailable": "yes",
    },
    "PRODUCT-FRONTIER-HIGH": {
        "owner_role": "Product Analyst",
        "agent_type": "default",
        "model": "gpt-5.4",
        "reasoning_effort": "high",
        "fork_context": "true",
        "execution_preference": "main_agent_or_frontier",
        "use_when": "product framing, journeys, non-goals, success metrics",
        "keep_local_if_unavailable": "yes",
    },
    "ARCH-FRONTIER-XHIGH": {
        "owner_role": "Architect",
        "agent_type": "worker",
        "model": "gpt-5.4",
        "reasoning_effort": "xhigh",
        "fork_context": "true",
        "execution_preference": "main_agent_or_frontier",
        "use_when": "architecture, contracts, seams, migration and replan",
        "keep_local_if_unavailable": "yes",
    },
    "CODE-FRONTIER-XHIGH": {
        "owner_role": "Frontend Engineer / Backend Engineer / Systems Engineer",
        "agent_type": "worker",
        "model": "gpt-5.4",
        "reasoning_effort": "xhigh",
        "fork_context": "true",
        "execution_preference": "delegated_frontier",
        "use_when": "critical coding, hard debugging, low-level changes",
        "keep_local_if_unavailable": "no",
    },
    "REVIEW-FRONTIER-HIGH": {
        "owner_role": "Architecture Reviewer / UI Reviewer",
        "agent_type": "default",
        "model": "gpt-5.4",
        "reasoning_effort": "high",
        "fork_context": "true",
        "execution_preference": "delegated_frontier",
        "use_when": "code review and user-facing design review",
        "keep_local_if_unavailable": "no",
    },
    "SEC-FRONTIER-XHIGH": {
        "owner_role": "Security Reviewer",
        "agent_type": "default",
        "model": "gpt-5.4",
        "reasoning_effort": "xhigh",
        "fork_context": "true",
        "execution_preference": "main_agent_or_frontier",
        "use_when": "security review, trust boundaries, exploit paths",
        "keep_local_if_unavailable": "yes",
    },
    "SYS-FRONTIER-XHIGH": {
        "owner_role": "Systems Reviewer",
        "agent_type": "default",
        "model": "gpt-5.4",
        "reasoning_effort": "xhigh",
        "fork_context": "true",
        "execution_preference": "main_agent_or_frontier",
        "use_when": "systems review, concurrency, ABI, lifetime safety",
        "keep_local_if_unavailable": "yes",
    },
    "RETRIEVAL-FAST-MEDIUM": {
        "owner_role": "Repo Retriever",
        "agent_type": "explorer",
        "model": "gpt-5.1-codex-mini",
        "reasoning_effort": "medium",
        "fork_context": "true",
        "execution_preference": "delegated_fast",
        "use_when": "inventory, retrieval, narrow file discovery",
        "keep_local_if_unavailable": "no",
    },
    "TEST-EXEC-FAST-MEDIUM": {
        "owner_role": "Tester",
        "agent_type": "worker",
        "model": "gpt-5.1-codex-mini",
        "reasoning_effort": "medium",
        "fork_context": "true",
        "execution_preference": "delegated_fast",
        "use_when": "test execution, command running, result collection",
        "keep_local_if_unavailable": "no",
    },
    "PACKAGING-FAST-LOW": {
        "owner_role": "Artifact Packager",
        "agent_type": "worker",
        "model": "gpt-5.1-codex-mini",
        "reasoning_effort": "low",
        "fork_context": "true",
        "execution_preference": "delegated_fast",
        "use_when": "artifact packaging, screenshots, review bundle assembly",
        "keep_local_if_unavailable": "no",
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate delegation templates.")
    parser.add_argument("--artifact-dir", required=True)
    parser.add_argument("--template-id", action="append", default=[], help="Template id to include")
    parser.add_argument("--output-name", default="delegation-templates.md")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    root = Path(args.artifact_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    output = root / args.output_name
    if output.exists() and not args.overwrite:
        raise FileExistsError(f"{output} already exists")

    selected = args.template_id or list(TEMPLATES)
    lines = ["Delegation Template Table:"]
    for template_id in selected:
        if template_id not in TEMPLATES:
            raise ValueError(f"Unknown template id: {template_id}")
        template = TEMPLATES[template_id]
        lines.extend(
            [
                f"- template_id: {template_id}",
                f"  owner_role: {template['owner_role']}",
                f"  agent_type: {template['agent_type']}",
                f"  model: {template['model']}",
                f"  reasoning_effort: {template['reasoning_effort']}",
                f"  fork_context: {template['fork_context']}",
                f"  execution_preference: {template['execution_preference']}",
                f"  use_when: {template['use_when']}",
                f"  keep_local_if_unavailable: {template['keep_local_if_unavailable']}",
                "  notes:",
            ]
        )

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Delegation templates written to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
