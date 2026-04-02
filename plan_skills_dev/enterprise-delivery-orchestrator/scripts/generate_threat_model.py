#!/usr/bin/env python3
"""Generate a bounded threat model template for defensive tools."""

from __future__ import annotations

import argparse
from pathlib import Path


def render_section(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- "


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a threat model markdown file.")
    parser.add_argument("--output", required=True)
    parser.add_argument("--system-name", required=True)
    parser.add_argument("--asset", action="append", default=[])
    parser.add_argument("--trust-boundary", action="append", default=[])
    parser.add_argument("--capability", action="append", default=[])
    parser.add_argument("--abuse-case", action="append", default=[])
    parser.add_argument("--mitigation", action="append", default=[])
    parser.add_argument("--residual-risk", action="append", default=[])
    args = parser.parse_args()

    path = Path(args.output).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    content = "\n".join(
        [
            "Threat Review:",
            f"- System: {args.system_name}",
            "",
            "## Assets",
            render_section(args.asset),
            "",
            "## Trust Boundaries",
            render_section(args.trust_boundary),
            "",
            "## Allowed Capabilities",
            render_section(args.capability),
            "",
            "## Abuse Cases",
            render_section(args.abuse_case),
            "",
            "## Mitigations",
            render_section(args.mitigation),
            "",
            "## Residual Risks",
            render_section(args.residual_risk),
            "",
        ]
    )
    path.write_text(content, encoding="utf-8")
    print(f"Threat model written to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
