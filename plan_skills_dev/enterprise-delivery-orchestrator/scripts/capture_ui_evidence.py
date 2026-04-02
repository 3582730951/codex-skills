#!/usr/bin/env python3
"""Capture multi-viewport screenshots and Lighthouse metrics for a web UI."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


VIEWPORTS = {
    "desktop": "1440,960",
    "tablet": "1024,1366",
    "mobile": "390,844",
}


def run_command(command: list[str], timeout: int) -> tuple[int, str]:
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=timeout,
        check=False,
    )
    return result.returncode, result.stdout


def capture_screenshots(url: str, output_dir: Path, wait_selector: str | None, wait_timeout: int) -> list[tuple[str, Path]]:
    screenshots: list[tuple[str, Path]] = []
    for name, viewport in VIEWPORTS.items():
        target = output_dir / f"{name}.png"
        command = [
            "npx",
            "playwright",
            "screenshot",
            "--browser",
            "chromium",
            "--viewport-size",
            viewport,
            "--full-page",
            "--timeout",
            str(max(wait_timeout, 1000) + 15000),
            "--wait-for-timeout",
            str(wait_timeout),
        ]
        if wait_selector:
            command.extend(["--wait-for-selector", wait_selector])
        command.extend([url, str(target)])
        code, output = run_command(command, timeout=max(60, wait_timeout // 1000 + 60))
        if code != 0:
            raise RuntimeError(f"Playwright screenshot failed for {name}:\n{output}")
        screenshots.append((name, target))
    return screenshots


def run_lighthouse(url: str, output_dir: Path, timeout: int) -> dict[str, int] | None:
    json_path = output_dir / "lighthouse.json"
    command = [
        "npx",
        "lighthouse",
        url,
        "--quiet",
        "--chrome-flags=--headless --no-sandbox",
        "--output=json",
        f"--output-path={json_path}",
    ]
    code, output = run_command(command, timeout=timeout)
    if code != 0:
        (output_dir / "lighthouse-error.log").write_text(output, encoding="utf-8")
        return None

    data = json.loads(json_path.read_text(encoding="utf-8"))
    categories = data.get("categories", {})
    return {
        name: round(value.get("score", 0) * 100)
        for name, value in categories.items()
        if isinstance(value, dict)
    }


def build_summary(
    *,
    url: str,
    output_dir: Path,
    screenshots: list[tuple[str, Path]],
    lighthouse_scores: dict[str, int] | None,
) -> Path:
    lines = [
        "UI Evidence Summary:",
        f"- URL: {url}",
        "",
        "## Screenshots",
    ]
    lines.extend(f"- {name}: {path.name}" for name, path in screenshots)
    lines.append("")
    lines.append("## Lighthouse")
    if lighthouse_scores is None:
        lines.append("- Lighthouse not available; inspect `lighthouse-error.log` if present.")
    else:
        lines.extend(f"- {name}: {score}" for name, score in lighthouse_scores.items())
    lines.append("")

    summary_path = output_dir / "ui-evidence-summary.md"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    return summary_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture UI evidence with Playwright screenshots and Lighthouse.")
    parser.add_argument("--url", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--wait-selector")
    parser.add_argument("--wait-timeout-ms", type=int, default=1500)
    parser.add_argument("--skip-lighthouse", action="store_true")
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        screenshots = capture_screenshots(
            args.url,
            output_dir,
            wait_selector=args.wait_selector,
            wait_timeout=args.wait_timeout_ms,
        )
    except Exception as exc:  # pragma: no cover - CLI failure path
        print(str(exc), file=sys.stderr)
        return 1

    lighthouse_scores = None
    if not args.skip_lighthouse:
        lighthouse_scores = run_lighthouse(args.url, output_dir, timeout=180)

    summary_path = build_summary(
        url=args.url,
        output_dir=output_dir,
        screenshots=screenshots,
        lighthouse_scores=lighthouse_scores,
    )
    print(f"UI evidence captured in {output_dir}")
    print(f"Summary: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
