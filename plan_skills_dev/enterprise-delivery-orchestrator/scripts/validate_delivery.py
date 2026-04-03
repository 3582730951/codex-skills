#!/usr/bin/env python3
"""Validate whether required delivery artifacts are present in an artifact bundle."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_MARKERS = {
    "task_charter": "Task Charter:",
    "engineering_baseline": "Engineering Baseline:",
    "product_brief": "Product/Experience Brief:",
    "architecture_contract": "Architecture Contract:",
    "adr": "ADR:",
    "api_contract_table": "API Contract Table:",
    "function_boundary_table": "Function Boundary Table:",
    "execution_contract": "Execution Contract:",
    "capability_routing_table": "Capability Routing Table:",
    "delegation_template_table": "Delegation Template Table:",
    "plan_coverage_matrix": "Plan Coverage Matrix:",
    "execution_ledger": "Execution Ledger:",
    "requirement_to_change_map": "Requirement-to-Change Map:",
    "test_matrix": "Test Matrix + Evidence Log:",
    "threat_review": "Threat Review:",
    "claim_to_evidence_map": "Claim-to-Evidence Map:",
    "review_package": "Review Package:",
    "release_readiness": "Release Readiness Checklist:",
    "decision_log": "Decision Log:",
    "state_snapshot": "State Snapshot:",
}


OPTIONAL_MARKERS = {
    "greenfield_bootstrap": "Greenfield Bootstrap Plan:",
    "design_direction_review": "Design Direction Review:",
    "concurrency_model": "Concurrency Model:",
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate delivery artifacts by scanning markdown/text bundles.")
    parser.add_argument("--artifact-dir", required=True, help="Directory containing artifacts")
    parser.add_argument("--require-greenfield", action="store_true")
    parser.add_argument("--require-ui", action="store_true")
    parser.add_argument("--require-system", action="store_true")
    args = parser.parse_args()

    root = Path(args.artifact_dir).resolve()
    if not root.exists():
        print(f"Artifact directory does not exist: {root}", file=sys.stderr)
        return 2

    bundle_text = collect_text(root)
    required = dict(REQUIRED_MARKERS)
    if args.require_greenfield:
        required["greenfield_bootstrap"] = OPTIONAL_MARKERS["greenfield_bootstrap"]
    if args.require_ui:
        required["design_direction_review"] = OPTIONAL_MARKERS["design_direction_review"]
    if args.require_system:
        required["concurrency_model"] = OPTIONAL_MARKERS["concurrency_model"]

    missing = [name for name, marker in required.items() if marker not in bundle_text]
    if missing:
        print("Delivery validation: FAIL")
        for name in missing:
            print(f"- missing: {name}")
        return 1

    print("Delivery validation: PASS")
    for name in required:
        print(f"- present: {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
