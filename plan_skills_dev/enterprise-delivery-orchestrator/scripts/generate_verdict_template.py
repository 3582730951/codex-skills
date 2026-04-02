#!/usr/bin/env python3
"""Generate a standard review verdict template."""

from __future__ import annotations

import argparse
from pathlib import Path


def build_template(role: str) -> str:
    return "\n".join(
        [
            "Review Verdict:",
            f"- Reviewer role: {role}",
            "- Verdict: pass | fail",
            "",
            "## Blocking Issues",
            "- ",
            "",
            "## Non-Blocking Improvements",
            "- ",
            "",
            "## Evidence References",
            "- file/path or command output reference:",
            "",
            "## Residual Risks",
            "- ",
            "",
            "## Contamination Declaration",
            "- Read another reviewer's verdict before writing this one? yes/no",
            "- Relied on implementer summary instead of primary artifacts? yes/no",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a reviewer verdict template.")
    parser.add_argument("--role", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    content = build_template(args.role)
    if args.output:
        path = Path(args.output).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Verdict template written to {path}")
    else:
        print(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
