#!/usr/bin/env python3
"""Build a review package markdown file from structured CLI inputs."""

from __future__ import annotations

import argparse
from pathlib import Path
def markdown_list(items: list[str]) -> str:
    if not items:
        return "- none"
    return "\n".join(f"- {item}" for item in items)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a review package markdown file.")
    parser.add_argument("--output", required=True, help="Output markdown path")
    parser.add_argument("--scope-summary", required=True)
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--changed-file", action="append", default=[])
    parser.add_argument("--command", action="append", default=[])
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--screenshot", action="append", default=[])
    parser.add_argument("--residual-risk", action="append", default=[])
    parser.add_argument("--reviewer-instruction", action="append", default=[])
    args = parser.parse_args()

    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    content = "\n".join(
        [
            "Review Package:",
            f"- Scope summary: {args.scope_summary}",
            "",
            "## Changed Files",
            markdown_list(args.changed_file),
            "",
            "## Relevant Artifacts",
            markdown_list(args.artifact),
            "",
            "## Executed Commands",
            markdown_list(args.command),
            "",
            "## Evidence Summary",
            markdown_list(args.evidence),
            "",
            "## Screenshots Or Recordings",
            markdown_list(args.screenshot),
            "",
            "## Residual Risks",
            markdown_list(args.residual_risk),
            "",
            "## Reviewer Instructions",
            markdown_list(args.reviewer_instruction),
            "",
        ]
    )

    output_path.write_text(content, encoding="utf-8")
    print(f"Review package written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
