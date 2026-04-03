#!/usr/bin/env python3
"""Validate generated spawn-agent templates against routing and delegation artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
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
    in_message_block = False

    for raw_line in section_text.splitlines():
        line = raw_line.rstrip()
        if line.startswith(f"- {key_name}:"):
            if current:
                entries.append(current)
            current = {key_name: line.split(":", 1)[1].strip()}
            in_message_block = False
            continue
        if current is None:
            continue
        if line.startswith("  message_template: |"):
            current["message_template"] = "present"
            in_message_block = True
            continue
        if in_message_block and line.startswith("    "):
            continue
        in_message_block = False
        if not line.strip():
            continue
        match = re.match(r"\s+([a-z_]+):\s*(.*)$", line)
        if match:
            current[match.group(1)] = match.group(2).strip()
    if current:
        entries.append(current)
    return entries


def expected_spawn_mode(execution_preference: str) -> tuple[str, str]:
    if execution_preference in {"delegated_frontier", "delegated_fast", "delegated_standard"}:
        return "spawn", "yes"
    if execution_preference == "main_agent_or_frontier":
        return "keep_local_or_spawn", "no"
    return "keep_local", "no"


def expected_fallback(keep_local_if_unavailable: str, spawn_mode: str) -> str:
    if keep_local_if_unavailable == "yes":
        return "keep_local_if_runtime_cannot_honor"
    if spawn_mode == "spawn":
        return "block_or_reassign"
    return "keep_local"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate generated spawn-agent templates.")
    parser.add_argument("--artifact-dir", required=True)
    parser.add_argument("--format", choices={"markdown", "json"}, default="markdown")
    args = parser.parse_args()

    root = Path(args.artifact_dir).resolve()
    if not root.exists():
        print(f"Artifact directory does not exist: {root}", file=sys.stderr)
        return 2

    text = collect_text(root)
    routing_entries = parse_flat_entries(extract_section(text, "Capability Routing Table:"), "work_item_id")
    template_entries = parse_flat_entries(extract_section(text, "Delegation Template Table:"), "template_id")
    spawn_entries = parse_flat_entries(extract_section(text, "Spawn Agent Template Table:"), "work_item_id")

    routing_map = {entry["work_item_id"]: entry for entry in routing_entries}
    template_map = {entry["template_id"]: entry for entry in template_entries}
    spawn_map = {entry["work_item_id"]: entry for entry in spawn_entries}

    findings: list[str] = []
    if not spawn_entries:
        findings.append("Spawn Agent Template Table is missing or empty")

    for work_item_id, routing in routing_map.items():
        if work_item_id not in spawn_map:
            findings.append(f"{work_item_id}: missing spawn-agent template entry")
            continue
        spawn_entry = spawn_map[work_item_id]
        template_id = routing.get("delegation_template_id", "")
        template = template_map.get(template_id)
        if template is None:
            findings.append(f"{work_item_id}: missing delegation template {template_id}")
            continue
        if spawn_entry.get("template_id", "") != template_id:
            findings.append(f"{work_item_id}: spawn template id does not match routing template id")

        expected_mode, expected_default = expected_spawn_mode(routing.get("execution_preference", ""))
        if spawn_entry.get("spawn_mode", "") != expected_mode:
            findings.append(f"{work_item_id}: spawn_mode should be {expected_mode}")
        if spawn_entry.get("should_spawn_by_default", "") != expected_default:
            findings.append(f"{work_item_id}: should_spawn_by_default should be {expected_default}")

        expected_fallback_policy = expected_fallback(template.get("keep_local_if_unavailable", ""), expected_mode)
        if spawn_entry.get("fallback_policy", "") != expected_fallback_policy:
            findings.append(f"{work_item_id}: fallback_policy should be {expected_fallback_policy}")

        spawn_json = spawn_entry.get("spawn_agent_json", "")
        if not spawn_json:
            findings.append(f"{work_item_id}: spawn_agent_json is missing")
            continue
        try:
            payload = json.loads(spawn_json)
        except json.JSONDecodeError as exc:
            findings.append(f"{work_item_id}: spawn_agent_json is invalid: {exc.msg}")
            continue

        if payload.get("agent_type") != template.get("agent_type", ""):
            findings.append(f"{work_item_id}: agent_type does not match delegation template")
        if payload.get("model") != template.get("model", ""):
            findings.append(f"{work_item_id}: model does not match delegation template")
        if payload.get("reasoning_effort") != template.get("reasoning_effort", ""):
            findings.append(f"{work_item_id}: reasoning_effort does not match delegation template")
        if payload.get("fork_context") is not True:
            findings.append(f"{work_item_id}: fork_context must be true")

        if "message_template" not in spawn_entry:
            findings.append(f"{work_item_id}: message_template block is missing")

    if args.format == "json":
        print(
            json.dumps(
                {
                    "artifact_dir": str(root),
                    "routing_count": len(routing_entries),
                    "spawn_count": len(spawn_entries),
                    "findings": findings,
                    "gate_result": "fail" if findings else "pass",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print("Spawn Agent Template Check:")
        print(f"- gate_result: {'fail' if findings else 'pass'}")
        print(f"- routing_count: {len(routing_entries)}")
        print(f"- spawn_count: {len(spawn_entries)}")
        print("Findings:")
        if findings:
            for finding in findings:
                print(f"- {finding}")
        else:
            print("- none")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
