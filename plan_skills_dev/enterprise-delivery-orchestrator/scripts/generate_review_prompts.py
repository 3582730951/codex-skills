#!/usr/bin/env python3
"""Generate reviewer-specific prompt files from a review package."""

from __future__ import annotations

import argparse
from pathlib import Path


ROLE_MAP = {
    "product-ui": ["architecture-reviewer", "ui-reviewer", "security-reviewer"],
    "system": ["architecture-reviewer", "systems-reviewer", "security-reviewer"],
    "mixed-ui": ["architecture-reviewer", "ui-reviewer", "security-reviewer"],
    "mixed-system": ["architecture-reviewer", "systems-reviewer", "security-reviewer"],
}


ROLE_GUIDANCE = {
    "architecture-reviewer": "Focus on boundaries, contracts, ownership, and long-term maintainability.",
    "ui-reviewer": "Focus on hierarchy, interaction quality, responsive behavior, accessibility, and visual distinctiveness.",
    "systems-reviewer": "Focus on concurrency, resource lifetime, performance assumptions, and low-level boundary safety.",
    "security-reviewer": "Focus on trust boundaries, unsafe defaults, secrets, validation, and exploit paths.",
}


OUTPUT_FORMAT = """Respond in this exact structure:
1. verdict: pass/fail
2. blocking issues
3. non-blocking improvements
4. evidence references
5. contamination declaration
- Did you read another reviewer's verdict before writing this one? yes/no
- Did you rely on the implementer summary instead of primary artifacts? yes/no
"""


def write_prompt(path: Path, role: str, scope_summary: str, review_package: str) -> None:
    content = "\n".join(
        [
            f"Reviewer Role: {role}",
            f"Scope Summary: {scope_summary}",
            f"Review Package: {review_package}",
            "",
            ROLE_GUIDANCE[role],
            "",
            OUTPUT_FORMAT,
            "",
            "Use the review package as the primary evidence source.",
        ]
    )
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate reviewer prompt files.")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--scope-summary", required=True)
    parser.add_argument("--review-package", required=True)
    parser.add_argument(
        "--work-type",
        required=True,
        choices=sorted(ROLE_MAP),
        help="Review routing profile",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    for role in ROLE_MAP[args.work_type]:
        target = output_dir / f"{role}.txt"
        write_prompt(target, role, args.scope_summary, args.review_package)

    print(f"Generated reviewer prompts in {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
