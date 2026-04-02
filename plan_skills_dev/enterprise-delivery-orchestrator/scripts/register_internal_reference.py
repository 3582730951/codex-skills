#!/usr/bin/env python3
"""Register an internal source root as a provenance-tracked reference bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


SKIP_DIRS = {".git", ".venv", "node_modules", "dist", "build", "target", "__pycache__"}
DEFAULT_EXTENSIONS = {
    ".c",
    ".cc",
    ".cpp",
    ".cxx",
    ".h",
    ".hpp",
    ".rs",
    ".py",
    ".java",
    ".kt",
    ".go",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
}


def iter_files(root: Path, extensions: set[str]) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in extensions:
            files.append(path)
    return sorted(files)


def sha256_for(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def line_count(path: Path) -> int:
    try:
        return len(path.read_text(encoding="utf-8").splitlines())
    except UnicodeDecodeError:
        return 0


def markdown_payload(data: dict) -> str:
    lines = [
        "Source Provenance Register:",
        f"- Label: {data['label']}",
        f"- Source root: {data['source_root']}",
        f"- Owner: {data['owner']}",
        f"- Sensitivity: {data['sensitivity']}",
        f"- Allowed use: {', '.join(data['allowed_use']) if data['allowed_use'] else ''}",
        f"- File count: {data['file_count']}",
        f"- Extension summary: {data['extension_summary']}",
        "",
        "## Files",
    ]
    for entry in data["files"]:
        lines.extend(
            [
                f"- path: {entry['path']}",
                f"  sha256: {entry['sha256']}",
                f"  lines: {entry['lines']}",
                f"  extension: {entry['extension']}",
            ]
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Register an internal source reference bundle.")
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--sensitivity", default="internal")
    parser.add_argument("--allowed-use", action="append", default=[])
    parser.add_argument("--format", choices={"markdown", "json"}, default="markdown")
    parser.add_argument("--max-files", type=int, default=500)
    parser.add_argument("--include-ext", action="append", default=[])
    args = parser.parse_args()

    root = Path(args.source_root).resolve()
    output = Path(args.output).resolve()
    extensions = {ext if ext.startswith(".") else f".{ext}" for ext in (args.include_ext or DEFAULT_EXTENSIONS)}

    files = iter_files(root, extensions)
    file_entries = []
    extension_counter: Counter[str] = Counter()
    for path in files[: args.max_files]:
        rel_path = str(path.relative_to(root))
        extension_counter[path.suffix.lower() or "<none>"] += 1
        file_entries.append(
            {
                "path": rel_path,
                "sha256": sha256_for(path),
                "lines": line_count(path),
                "extension": path.suffix.lower() or "<none>",
            }
        )

    payload = {
        "label": args.label,
        "source_root": str(root),
        "owner": args.owner,
        "sensitivity": args.sensitivity,
        "allowed_use": args.allowed_use,
        "file_count": len(file_entries),
        "extension_summary": ", ".join(f"{ext}:{count}" for ext, count in extension_counter.most_common()),
        "files": file_entries,
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    if args.format == "json":
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        output.write_text(markdown_payload(payload), encoding="utf-8")

    print(f"Registered internal reference at {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
