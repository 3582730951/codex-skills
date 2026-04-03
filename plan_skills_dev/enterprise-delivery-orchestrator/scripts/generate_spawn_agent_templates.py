#!/usr/bin/env python3
"""Generate spawn-agent templates from routing and delegation artifacts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SECTION_MARKERS = [
    "Capability Routing Table:",
    "Delegation Template Table:",
    "Spawn Agent Template Table:",
]


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


def extract_section(text: str, marker: str) -> str:
    start = text.find(marker)
    if start == -1:
        return ""
    start += len(marker)
    next_positions = [text.find(other, start) for other in SECTION_MARKERS if other != marker and text.find(other, start) != -1]
    end = min(next_positions) if next_positions else len(text)
    return text[start:end]


def parse_flat_entries(section_text: str, key_name: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw_line in section_text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if line.startswith(f"- {key_name}:"):
            if current:
                entries.append(current)
            current = {key_name: line.split(":", 1)[1].strip()}
            continue
        if current is None:
            continue
        match = re.match(r"\s+([a-z_]+):\s*(.*)$", line)
        if match:
            current[match.group(1)] = match.group(2).strip()
    if current:
        entries.append(current)
    return entries


def spawn_mode_for(execution_preference: str) -> tuple[str, str]:
    if execution_preference in {"delegated_frontier", "delegated_fast", "delegated_standard"}:
        return "spawn", "yes"
    if execution_preference == "main_agent_or_frontier":
        return "keep_local_or_spawn", "no"
    return "keep_local", "no"


def fallback_policy_for(keep_local_if_unavailable: str, spawn_mode: str) -> str:
    if keep_local_if_unavailable == "yes":
        return "keep_local_if_runtime_cannot_honor"
    if spawn_mode == "spawn":
        return "block_or_reassign"
    return "keep_local"


def message_template(entry: dict[str, str], template: dict[str, str], fallback_policy: str) -> str:
    lines = [
        f"Role: {entry.get('owner_role', template.get('owner_role', ''))}",
        f"Work item: {entry.get('work_item_id', '')}",
        f"Work class: {entry.get('work_class', '')}",
        "Use the locked plan, capability routing, and execution ledger.",
        "Cite plan_step_id and requirement_id in progress updates.",
        "Own only the files assigned by the plan and return evidence with changed files.",
    ]
    if fallback_policy == "keep_local_if_runtime_cannot_honor":
        lines.append("If the runtime cannot honor this model or reasoning setting, keep the work local.")
    elif fallback_policy == "block_or_reassign":
        lines.append("If the runtime cannot honor this template, stop and reassign instead of downgrading.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate spawn-agent templates from routing artifacts.")
    parser.add_argument("--artifact-dir", required=True)
    parser.add_argument("--output-name", default="spawn-agent-templates.md")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    root = Path(args.artifact_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    output = root / args.output_name
    if output.exists() and not args.overwrite:
        raise FileExistsError(f"{output} already exists")

    text = collect_text(root)
    routing_entries = parse_flat_entries(extract_section(text, "Capability Routing Table:"), "work_item_id")
    template_entries = parse_flat_entries(extract_section(text, "Delegation Template Table:"), "template_id")
    template_map = {entry["template_id"]: entry for entry in template_entries}

    if not routing_entries:
        raise ValueError("Capability Routing Table is missing or empty")
    if not template_entries:
        raise ValueError("Delegation Template Table is missing or empty")

    lines = ["Spawn Agent Template Table:"]
    for entry in routing_entries:
        template_id = entry.get("delegation_template_id", "")
        if template_id not in template_map:
            raise ValueError(f"Missing delegation template for {entry.get('work_item_id', '<unknown>')}: {template_id}")
        template = template_map[template_id]
        spawn_mode, should_spawn = spawn_mode_for(entry.get("execution_preference", ""))
        fallback_policy = fallback_policy_for(template.get("keep_local_if_unavailable", ""), spawn_mode)
        spawn_params = {
            "agent_type": template.get("agent_type", "default"),
            "model": template.get("model", entry.get("preferred_model", "")),
            "reasoning_effort": template.get("reasoning_effort", entry.get("reasoning_effort", "")),
            "fork_context": template.get("fork_context", "true").lower() == "true",
        }
        message = message_template(entry, template, fallback_policy)
        lines.extend(
            [
                f"- work_item_id: {entry.get('work_item_id', '')}",
                f"  work_class: {entry.get('work_class', '')}",
                f"  template_id: {template_id}",
                f"  spawn_mode: {spawn_mode}",
                f"  should_spawn_by_default: {should_spawn}",
                f"  fallback_policy: {fallback_policy}",
                f"  spawn_agent_json: {json.dumps(spawn_params, ensure_ascii=True, separators=(',', ':'))}",
                "  message_template: |",
            ]
        )
        for message_line in message.splitlines():
            lines.append(f"    {message_line}")

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Spawn agent templates written to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
