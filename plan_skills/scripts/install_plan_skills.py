#!/usr/bin/env python3
"""Install planning skills from a local plan_skills directory."""

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


def plan_root_from_script() -> Path:
    return Path(__file__).resolve().parent.parent


def discover_skills(plan_root: Path) -> list[Path]:
    skills = []
    for skill_md in plan_root.rglob("SKILL.md"):
        skill_dir = skill_md.parent
        if "scripts" in skill_dir.parts:
            continue
        skills.append(skill_dir)
    skills.sort(key=lambda p: p.name)
    return skills


def install_skill(skill_dir: Path, dest_root: Path, overwrite: bool) -> str:
    dest_dir = dest_root / skill_dir.name
    if dest_dir.exists():
        if not overwrite:
            return f"skip: {skill_dir.name} already exists at {dest_dir}"
        shutil.rmtree(dest_dir)
    shutil.copytree(skill_dir, dest_dir)
    return f"ok: {skill_dir.name} -> {dest_dir}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Install skills from the local plan_skills directory.")
    parser.add_argument(
        "--plan-root",
        default=str(plan_root_from_script()),
        help="Path to the plan_skills directory. Defaults to this script's parent directory.",
    )
    parser.add_argument(
        "--dest",
        default=str(codex_home() / "skills"),
        help="Destination skills directory. Defaults to $CODEX_HOME/skills or ~/.codex/skills.",
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

    plan_root = Path(args.plan_root).resolve()
    dest_root = Path(args.dest).expanduser().resolve()
    selected = set(args.skill)

    discovered = discover_skills(plan_root)
    if selected:
        discovered = [skill for skill in discovered if skill.name in selected]

    if args.list:
        if not discovered:
            print("No skills found.")
            return 0
        print("Discovered planning skills:")
        for skill in discovered:
            print(f"- {skill.name}")
        return 0

    if not discovered:
        print("No matching planning skills found.", file=sys.stderr)
        return 1

    dest_root.mkdir(parents=True, exist_ok=True)
    print(f"Installing to: {dest_root}")
    for skill in discovered:
        print(install_skill(skill, dest_root, args.overwrite))
    print("Restart Codex to pick up installed skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
