#!/usr/bin/env python3
"""Install Codex skills from a local repository clone."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


def codex_home() -> Path:
    raw = os.environ.get("CODEX_HOME")
    if raw:
        return Path(raw).expanduser()
    return Path.home() / ".codex"


def discover_skills(repo_root: Path) -> list[tuple[str, Path]]:
    results: list[tuple[str, Path]] = []
    for skill_md in repo_root.rglob("SKILL.md"):
        skill_dir = skill_md.parent
        if ".git" in skill_dir.parts:
            continue
        rel = skill_dir.relative_to(repo_root)
        results.append((rel.as_posix(), skill_dir))
    results.sort(key=lambda item: item[0])
    return results


def filter_skills(
    discovered: list[tuple[str, Path]],
    groups: set[str],
    skill_names: set[str],
) -> list[tuple[str, Path]]:
    filtered: list[tuple[str, Path]] = []
    for rel, path in discovered:
        parts = Path(rel).parts
        top_group = parts[0] if parts else ""
        skill_name = path.name
        if groups and top_group not in groups:
            continue
        if skill_names and skill_name not in skill_names:
            continue
        filtered.append((rel, path))
    return filtered


def install_skill(skill_dir: Path, dest_root: Path, overwrite: bool) -> str:
    dest_dir = dest_root / skill_dir.name
    if dest_dir.exists():
        if not overwrite:
            return f"skip: {skill_dir.name} already exists at {dest_dir}"
        shutil.rmtree(dest_dir)
    shutil.copytree(skill_dir, dest_dir)
    return f"ok: {skill_dir.name} -> {dest_dir}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Install skills from this repo clone.")
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parent.parent),
        help="Path to the repository root. Defaults to this script's parent repo.",
    )
    parser.add_argument(
        "--dest",
        default=str(codex_home() / "skills"),
        help="Destination skills directory. Defaults to $CODEX_HOME/skills or ~/.codex/skills.",
    )
    parser.add_argument(
        "--group",
        action="append",
        default=[],
        help="Install only skills from the given top-level group directory. Repeatable.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Install only the given skill directory name. Repeatable.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List discovered skills and exit.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing destination skill directories.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    dest_root = Path(args.dest).expanduser().resolve()
    groups = set(args.group)
    skill_names = set(args.skill)

    discovered = discover_skills(repo_root)
    filtered = filter_skills(discovered, groups, skill_names)

    if args.list:
        if not filtered:
            print("No skills found.")
            return 0
        print("Discovered skills:")
        for rel, skill_dir in filtered:
            print(f"- {skill_dir.name}: {rel}")
        return 0

    if not filtered:
        print("No matching skills found.", file=sys.stderr)
        return 1

    dest_root.mkdir(parents=True, exist_ok=True)
    print(f"Installing to: {dest_root}")
    for _, skill_dir in filtered:
        print(install_skill(skill_dir, dest_root, args.overwrite))
    print("Restart Codex to pick up installed skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
